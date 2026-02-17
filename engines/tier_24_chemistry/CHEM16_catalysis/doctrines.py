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
        topic="Heterogeneous Catalysis: Surface Adsorption and Langmuir Isotherm",
        keywords=["heterogeneous catalysis", "surface adsorption", "Langmuir isotherm", "adsorption equilibrium", "active sites"],
        conclusion_template="The rate of reaction is determined by the surface coverage of reactants, governed by the Langmuir adsorption isotherm.",
        reasoning_framework=(
            "Surface adsorption in heterogeneous catalysis is modeled by the Langmuir isotherm, which assumes a fixed number of equivalent active sites, "
            "monolayer coverage, and no interaction between adsorbed molecules. The equilibrium between adsorbed and free molecules is described by:\n"
            "θ = (K_ads * P) / (1 + K_ads * P), where θ is the fraction of occupied sites, K_ads is the adsorption equilibrium constant, and P is the partial pressure.\n"
            "The catalytic activity depends on θ, and the rate law often exhibits a saturation behavior at high P. Deviations from Langmuir behavior can occur due to "
            "surface heterogeneity, multilayer adsorption, or competitive adsorption. Experimental validation is achieved via spectroscopic and kinetic measurements."
        ),
        key_factors=["adsorption equilibrium constant", "surface coverage", "reactant partial pressure", "active site density", "temperature"],
        primary_authority=["Langmuir (1918)", "Somorjai & Li (2010)", "Campbell & Sellers (2012)"],
        burden_holder="Catalyst designer",
        adversary_position="Langmuir model oversimplifies real catalyst surfaces; ignores lateral interactions and surface heterogeneity.",
        counter_arguments=[
            "Langmuir isotherm is a first-order approximation; more complex models (Temkin, Freundlich) can be used for real surfaces.",
            "Experimental data often fits Langmuir at moderate pressures.",
            "Surface characterization techniques can validate assumptions."
        ],
        resolution_strategy="Apply Langmuir isotherm as baseline; supplement with advanced models and experimental validation for complex systems.",
        entity_scope="Catalyst surface, reactant molecules",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Langmuir, J. Am. Chem. Soc. 1918, 40, 1361"
    ),
    DoctrineBlock(
        topic="Homogeneous Catalysis: Organometallic Mechanisms (Wilkinson, Grubbs)",
        keywords=["homogeneous catalysis", "organometallic", "Wilkinson catalyst", "Grubbs catalyst", "reaction mechanism", "oxidative addition", "reductive elimination"],
        conclusion_template="Organometallic homogeneous catalysts facilitate transformations via well-defined mechanisms involving oxidative addition, ligand exchange, and reductive elimination.",
        reasoning_framework=(
            "Homogeneous catalysis with organometallic complexes (e.g., Wilkinson's RhCl(PPh3)3, Grubbs' Ru-carbene) operates in solution, allowing precise mechanistic studies. "
            "Key steps include oxidative addition (increasing metal oxidation state), ligand exchange (modifying coordination sphere), and reductive elimination (product release). "
            "Wilkinson's catalyst is used for hydrogenation, proceeding via coordination of H2, oxidative addition, and migratory insertion. Grubbs' catalyst enables olefin metathesis, "
            "involving carbene exchange and metallacyclobutane intermediates. Mechanistic understanding guides catalyst optimization and selectivity control."
        ),
        key_factors=["metal center", "ligand environment", "oxidation state", "reaction intermediates", "solvent effects"],
        primary_authority=["Wilkinson (1965)", "Grubbs (1995)", "Hartwig (2010)"],
        burden_holder="Catalyst developer",
        adversary_position="Homogeneous catalysts are less robust and harder to separate than heterogeneous catalysts.",
        counter_arguments=[
            "Homogeneous catalysts offer high selectivity and mechanistic clarity.",
            "Separation challenges can be addressed by immobilization or biphasic systems.",
            "Robustness can be improved by ligand design."
        ],
        resolution_strategy="Choose catalyst type based on process requirements; apply immobilization or separation strategies as needed.",
        entity_scope="Solution-phase catalytic systems",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Wilkinson, J. Am. Chem. Soc. 1965, 87, 393"
    ),
    DoctrineBlock(
        topic="Enzyme Kinetics: Michaelis-Menten and Inhibition",
        keywords=["enzyme kinetics", "Michaelis-Menten", "inhibition", "Km", "Vmax", "competitive inhibition", "noncompetitive inhibition"],
        conclusion_template="Enzyme-catalyzed reactions follow Michaelis-Menten kinetics, with inhibition mechanisms altering apparent Km and Vmax.",
        reasoning_framework=(
            "Michaelis-Menten kinetics describes the rate of enzyme-catalyzed reactions as v = (Vmax * [S]) / (Km + [S]), where [S] is substrate concentration, Km is the Michaelis constant, "
            "and Vmax is the maximum rate. Inhibitors modify kinetics: competitive inhibitors increase apparent Km (bind to active site), noncompetitive inhibitors decrease Vmax (bind elsewhere), "
            "and uncompetitive inhibitors affect both. Kinetic parameters are determined via initial rate experiments and Lineweaver-Burk plots. Mechanistic understanding informs drug design and biocatalyst optimization."
        ),
        key_factors=["substrate concentration", "enzyme concentration", "inhibitor type", "Km", "Vmax"],
        primary_authority=["Michaelis & Menten (1913)", "Cornish-Bowden (2012)", "Nelson & Cox (2021)"],
        burden_holder="Biochemist",
        adversary_position="Michaelis-Menten model assumes steady-state and single substrate; real enzymes may exhibit allosteric effects or multiple substrates.",
        counter_arguments=[
            "Michaelis-Menten is a foundational model; extensions exist for allosteric and multi-substrate enzymes.",
            "Experimental design can isolate single substrate kinetics.",
            "Allosteric effects can be modeled with Hill equation."
        ],
        resolution_strategy="Apply Michaelis-Menten as baseline; use advanced models for complex enzyme systems.",
        entity_scope="Enzyme, substrate, inhibitor",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Michaelis & Menten, Biochem. Z. 1913, 49, 333"
    ),
    DoctrineBlock(
        topic="Catalyst Characterization: XRD, BET, TPR, TPD, XPS",
        keywords=["catalyst characterization", "XRD", "BET", "TPR", "TPD", "XPS", "surface area", "crystallinity", "reduction", "desorption", "surface composition"],
        conclusion_template="Comprehensive catalyst characterization requires multiple techniques: XRD for crystallinity, BET for surface area, TPR/TPD for redox and desorption properties, XPS for surface composition.",
        reasoning_framework=(
            "Catalyst performance is linked to physical and chemical properties. XRD identifies crystalline phases and crystallite size. BET measures surface area and porosity, critical for dispersion and accessibility. "
            "TPR (Temperature Programmed Reduction) assesses reducibility and metal-support interactions. TPD (Temperature Programmed Desorption) reveals adsorption strength and site distribution. XPS (X-ray Photoelectron Spectroscopy) "
            "provides elemental composition and oxidation states at the surface. Combining these techniques enables correlation of structure with activity and stability."
        ),
        key_factors=["crystallinity", "surface area", "porosity", "reducibility", "surface composition"],
        primary_authority=["IUPAC Recommendations", "Somorjai & Li (2010)", "Campbell & Sellers (2012)"],
        burden_holder="Catalyst analyst",
        adversary_position="Single technique cannot provide complete information; interpretation may be ambiguous.",
        counter_arguments=[
            "Multi-technique approach mitigates limitations.",
            "Cross-validation enhances reliability.",
            "Advanced techniques (TEM, EXAFS) can supplement."
        ],
        resolution_strategy="Integrate data from multiple characterization techniques; use advanced methods as needed.",
        entity_scope="Catalyst material",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IUPAC, Pure Appl. Chem. 1982, 54, 2201"
    ),
    DoctrineBlock(
        topic="Reaction Kinetics: Rate Laws and Arrhenius Equation",
        keywords=["reaction kinetics", "rate law", "Arrhenius equation", "activation energy", "temperature dependence", "reaction order"],
        conclusion_template="Reaction rates follow empirical rate laws and temperature dependence described by the Arrhenius equation.",
        reasoning_framework=(
            "The rate law expresses reaction rate as a function of reactant concentrations: rate = k * [A]^m * [B]^n, where k is the rate constant, m and n are reaction orders. "
            "The Arrhenius equation relates k to temperature: k = A * exp(-Ea/(RT)), where A is the pre-exponential factor, Ea is activation energy, R is gas constant, T is temperature. "
            "Experimental determination of rate law and Ea enables prediction and optimization of catalytic processes. Deviations may indicate complex mechanisms or mass transfer limitations."
        ),
        key_factors=["rate constant", "activation energy", "reaction order", "temperature", "catalyst presence"],
        primary_authority=["Arrhenius (1889)", "Levenspiel (1999)", "Somorjai & Li (2010)"],
        burden_holder="Kineticist",
        adversary_position="Empirical rate laws may not capture mechanistic complexity; Arrhenius equation assumes single activation barrier.",
        counter_arguments=[
            "Mechanistic studies can refine rate law.",
            "Arrhenius equation is widely applicable; deviations signal complexity.",
            "Catalyst effects can be incorporated via modified rate expressions."
        ],
        resolution_strategy="Use empirical rate laws and Arrhenius equation as starting point; refine with mechanistic and experimental data.",
        entity_scope="Reactants, catalyst, reaction conditions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Arrhenius, Z. Phys. Chem. 1889, 4, 226"
    ),
    DoctrineBlock(
        topic="Reactor Design: CSTR, PFR, Batch, Semi-batch",
        keywords=["reactor design", "CSTR", "PFR", "batch reactor", "semi-batch reactor", "residence time", "conversion"],
        conclusion_template="Selection of reactor type (CSTR, PFR, batch, semi-batch) is based on process requirements, kinetics, and desired conversion/yield.",
        reasoning_framework=(
            "Continuous Stirred Tank Reactor (CSTR) provides uniform composition, suitable for slow reactions and large-scale production. Plug Flow Reactor (PFR) offers high conversion per unit volume for fast reactions, "
            "with concentration gradients along the reactor. Batch reactors allow flexibility and are used for small-scale or specialty chemicals. Semi-batch reactors combine features, enabling controlled addition of reactants. "
            "Design involves balancing residence time, conversion, yield, and operational constraints. Mathematical models (Levenspiel plots) guide optimization."
        ),
        key_factors=["reaction kinetics", "residence time", "conversion", "yield", "scale"],
        primary_authority=["Levenspiel (1999)", "Fogler (2016)", "IUPAC Recommendations"],
        burden_holder="Process engineer",
        adversary_position="Ideal reactor models ignore mixing, heat transfer, and scale-up issues.",
        counter_arguments=[
            "Real-world reactors require correction factors.",
            "Computational fluid dynamics can model non-idealities.",
            "Pilot-scale testing validates design."
        ],
        resolution_strategy="Use ideal models for initial design; incorporate corrections and experimental validation for scale-up.",
        entity_scope="Reactor system",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Levenspiel, Chemical Reaction Engineering, 3rd Ed."
    ),
    DoctrineBlock(
        topic="Catalyst Deactivation: Sintering, Poisoning, Coking",
        keywords=["catalyst deactivation", "sintering", "poisoning", "coking", "lifetime", "regeneration"],
        conclusion_template="Catalyst deactivation occurs via sintering, poisoning, and coking; mitigation and regeneration strategies are essential for sustained activity.",
        reasoning_framework=(
            "Catalyst deactivation reduces activity and selectivity. Sintering involves particle growth and loss of surface area, accelerated by high temperatures. Poisoning results from strong adsorption of impurities "
            "(e.g., sulfur, lead) blocking active sites. Coking is the deposition of carbonaceous species, especially in hydrocarbon processing. Monitoring deactivation via activity tests and characterization guides "
            "regeneration strategies: thermal treatment, chemical washing, or oxidative removal. Design of robust catalysts and process conditions minimizes deactivation."
        ),
        key_factors=["operating temperature", "impurity concentration", "feed composition", "regeneration method", "catalyst structure"],
        primary_authority=["Bartholomew (2001)", "Somorjai & Li (2010)", "IUPAC Recommendations"],
        burden_holder="Catalyst operator",
        adversary_position="Deactivation is inevitable; regeneration may not fully restore activity.",
        counter_arguments=[
            "Proper design and operation can minimize deactivation.",
            "Regeneration methods are effective for many catalysts.",
            "Continuous monitoring enables timely intervention."
        ],
        resolution_strategy="Implement monitoring and regeneration protocols; optimize catalyst and process design for longevity.",
        entity_scope="Catalyst bed, reactor",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="Bartholomew, Appl. Catal. A 2001, 212, 17"
    ),
    DoctrineBlock(
        topic="Zeolite Catalysis: Shape Selectivity and Acidity",
        keywords=["zeolite catalysis", "shape selectivity", "acidity", "framework", "Brønsted sites", "Lewis sites"],
        conclusion_template="Zeolite catalysts exhibit shape selectivity and acidity, enabling tailored reactions via framework topology and active site distribution.",
        reasoning_framework=(
            "Zeolites are crystalline aluminosilicates with well-defined pore structures. Shape selectivity arises from molecular size exclusion and channel topology, controlling access to active sites. "
            "Acidity is provided by Brønsted (proton donor) and Lewis (electron acceptor) sites, determined by framework composition and extra-framework cations. Zeolite catalysis is used in cracking, isomerization, "
            "and fine chemical synthesis. Characterization of acidity and pore structure guides catalyst selection and process optimization."
        ),
        key_factors=["pore size", "framework topology", "acidity", "active site distribution", "feed composition"],
        primary_authority=["Corma (1995)", "IUPAC Recommendations", "Sauer & Sierka (2012)"],
        burden_holder="Catalyst designer",
        adversary_position="Zeolite catalysts may suffer from diffusion limitations and dealumination.",
        counter_arguments=[
            "Optimized pore structure and acidity minimize limitations.",
            "Post-synthetic modifications enhance stability.",
            "Hierarchical zeolites improve diffusion."
        ],
        resolution_strategy="Select zeolite type based on reaction and feed; apply modifications to enhance performance.",
        entity_scope="Zeolite framework, reactant molecules",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Corma, Chem. Rev. 1995, 95, 559"
    ),
    DoctrineBlock(
        topic="Fischer-Tropsch Synthesis: Cobalt and Iron Catalysts",
        keywords=["Fischer-Tropsch synthesis", "cobalt catalyst", "iron catalyst", "syngas", "hydrocarbon synthesis", "selectivity"],
        conclusion_template="Fischer-Tropsch synthesis employs cobalt or iron catalysts to convert syngas into hydrocarbons, with selectivity governed by catalyst and process conditions.",
        reasoning_framework=(
            "Fischer-Tropsch (FT) synthesis converts CO and H2 (syngas) into hydrocarbons. Cobalt catalysts offer high activity and selectivity for linear paraffins, suitable for low-temperature FT. Iron catalysts "
            "are preferred for high-temperature FT and tolerate higher CO2 and water, producing olefins and oxygenates. Catalyst structure, promoter addition, and support influence activity and selectivity. "
            "Process parameters (temperature, pressure, syngas ratio) are optimized for desired product distribution. Deactivation via sintering and carbon deposition is managed by regeneration."
        ),
        key_factors=["catalyst type", "syngas ratio", "temperature", "pressure", "promoters"],
        primary_authority=["Dry (2002)", "Bartholomew (2001)", "IUPAC Recommendations"],
        burden_holder="Process engineer",
        adversary_position="FT process is energy-intensive and sensitive to catalyst deactivation.",
        counter_arguments=[
            "Advances in catalyst design improve stability and selectivity.",
            "Process integration reduces energy consumption.",
            "Regeneration protocols restore activity."
        ],
        resolution_strategy="Select catalyst and process conditions based on feed and desired products; implement regeneration and process optimization.",
        entity_scope="FT reactor, catalyst bed",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Dry, Catal. Today 2002, 71, 227"
    ),
    DoctrineBlock(
        topic="Hydrocracking, Hydrodesulfurization, and Hydrotreating",
        keywords=["hydrocracking", "hydrodesulfurization", "hydrotreating", "sulfur removal", "hydrogenation", "catalyst"],
        conclusion_template="Hydrocracking, hydrodesulfurization, and hydrotreating employ bifunctional catalysts to upgrade petroleum fractions and remove impurities.",
        reasoning_framework=(
            "Hydrocracking breaks large hydrocarbons into smaller, valuable products using acid and metal sites. Hydrodesulfurization (HDS) removes sulfur via hydrogenation and C-S bond cleavage, "
            "using Co-Mo or Ni-Mo catalysts on alumina. Hydrotreating encompasses HDS, hydrodenitrogenation, and hydrodearomatization, improving fuel quality. Process conditions (temperature, pressure, hydrogen flow) "
            "and catalyst design (metal loading, support) are optimized for activity and selectivity. Monitoring sulfur and nitrogen content ensures compliance with environmental regulations."
        ),
        key_factors=["catalyst composition", "temperature", "pressure", "hydrogen flow", "feedstock impurities"],
        primary_authority=["Speight (2014)", "Bartholomew (2001)", "IUPAC Recommendations"],
        burden_holder="Refinery operator",
        adversary_position="Catalyst deactivation and feedstock variability challenge process stability.",
        counter_arguments=[
            "Robust catalyst design and regeneration protocols mitigate deactivation.",
            "Feedstock analysis enables process adjustment.",
            "Advanced monitoring ensures compliance."
        ],
        resolution_strategy="Optimize catalyst and process parameters; implement monitoring and regeneration strategies.",
        entity_scope="Refinery reactor, catalyst bed",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Speight, Hydroprocessing of Heavy Oils, 2014"
    ),
    DoctrineBlock(
        topic="Fluid Catalytic Cracking (FCC): Riser and Regenerator",
        keywords=["fluid catalytic cracking", "FCC", "riser", "regenerator", "catalyst", "cracking", "regeneration"],
        conclusion_template="FCC employs a riser reactor for cracking and a regenerator for catalyst reactivation, enabling continuous processing of heavy feedstocks.",
        reasoning_framework=(
            "Fluid Catalytic Cracking (FCC) is a cornerstone of petroleum refining, converting heavy fractions into gasoline and olefins. The riser reactor provides short contact time and high temperature, "
            "maximizing conversion and selectivity. Spent catalyst is transported to the regenerator, where coke is burned off, restoring activity. Catalyst design (zeolite content, matrix) and process parameters "
            "(temperature, catalyst-to-oil ratio) are optimized for yield and stability. Environmental controls manage emissions from regeneration."
        ),
        key_factors=["catalyst composition", "riser temperature", "regeneration efficiency", "catalyst-to-oil ratio", "feedstock"],
        primary_authority=["Gary & Handwerk (2017)", "Bartholomew (2001)", "IUPAC Recommendations"],
        burden_holder="Refinery operator",
        adversary_position="FCC generates emissions and faces catalyst attrition.",
        counter_arguments=[
            "Emission controls and improved catalyst design address environmental and attrition issues.",
            "Continuous monitoring ensures process stability.",
            "Regeneration protocols optimize catalyst lifetime."
        ],
        resolution_strategy="Optimize catalyst and process parameters; implement emission controls and monitoring.",
        entity_scope="FCC unit, catalyst bed",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Gary & Handwerk, Petroleum Refining, 2017"
    ),
    DoctrineBlock(
        topic="Haber-Bosch Ammonia Synthesis: Iron Catalyst",
        keywords=["Haber-Bosch", "ammonia synthesis", "iron catalyst", "syngas", "high pressure", "high temperature"],
        conclusion_template="Haber-Bosch process synthesizes ammonia from syngas using promoted iron catalysts under high pressure and temperature.",
        reasoning_framework=(
            "The Haber-Bosch process produces ammonia by reacting N2 and H2 over promoted iron catalysts (e.g., Fe with K2O, Al2O3, CaO) at 150-250 atm and 400-500°C. "
            "Catalyst activity is enhanced by promoters, which increase surface area and prevent sintering. Reaction equilibrium and kinetics are balanced by optimizing temperature and pressure. "
            "Process integration and heat management are critical for efficiency. Catalyst deactivation via sintering and poisoning is managed by feed purification and regeneration."
        ),
        key_factors=["catalyst composition", "pressure", "temperature", "promoters", "feed purity"],
        primary_authority=["Ertl (2008)", "Somorjai & Li (2010)", "IUPAC Recommendations"],
        burden_holder="Process engineer",
        adversary_position="High energy consumption and catalyst deactivation limit efficiency.",
        counter_arguments=[
            "Process optimization and improved catalyst design enhance efficiency.",
            "Feed purification reduces poisoning.",
            "Regeneration protocols restore activity."
        ],
        resolution_strategy="Optimize process parameters and catalyst design; implement feed purification and regeneration.",
        entity_scope="Ammonia synthesis reactor",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Ertl, Angew. Chem. Int. Ed. 2008, 47, 3524"
    ),
    DoctrineBlock(
        topic="Catalytic Converter: TWC (Platinum, Palladium, Rhodium)",
        keywords=["catalytic converter", "three-way catalyst", "platinum", "palladium", "rhodium", "automotive", "emissions"],
        conclusion_template="Automotive catalytic converters use platinum, palladium, and rhodium in three-way catalysts to simultaneously reduce NOx, CO, and hydrocarbons.",
        reasoning_framework=(
            "Three-way catalysts (TWC) in automotive converters facilitate oxidation of CO and hydrocarbons and reduction of NOx. Platinum and palladium catalyze oxidation, rhodium catalyzes NOx reduction. "
            "Optimal performance requires precise control of air-to-fuel ratio. Catalyst aging, poisoning (e.g., by lead, sulfur), and thermal degradation affect efficiency. Regulatory standards drive continuous improvement "
            "in catalyst formulation and durability. Monitoring and replacement protocols ensure compliance."
        ),
        key_factors=["catalyst composition", "air-to-fuel ratio", "temperature", "poisoning", "regulatory compliance"],
        primary_authority=["Shelef & McCabe (2000)", "IUPAC Recommendations", "Somorjai & Li (2010)"],
        burden_holder="Automotive manufacturer",
        adversary_position="Catalyst aging and poisoning reduce converter efficiency.",
        counter_arguments=[
            "Advanced catalyst formulations improve resistance to aging and poisoning.",
            "Monitoring and replacement protocols maintain performance.",
            "Regulatory compliance is enforced."
        ],
        resolution_strategy="Optimize catalyst design; implement monitoring and replacement protocols.",
        entity_scope="Automotive exhaust system",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Shelef & McCabe, Catal. Today 2000, 62, 35"
    ),
    DoctrineBlock(
        topic="Photocatalysis: TiO2, Band Gap, UV/Visible Activation",
        keywords=["photocatalysis", "TiO2", "band gap", "UV activation", "visible light", "semiconductor"],
        conclusion_template="TiO2-based photocatalysts utilize UV or visible light to generate electron-hole pairs, driving redox reactions for environmental and synthetic applications.",
        reasoning_framework=(
            "Photocatalysis employs semiconductors (e.g., TiO2) with suitable band gaps to absorb light and generate electron-hole pairs. UV activation is typical for TiO2 (band gap ~3.2 eV), but doping and modification "
            "enable visible light activity. Electron-hole pairs drive oxidation and reduction reactions, used in pollutant degradation and organic synthesis. Catalyst design focuses on maximizing charge separation and surface reactivity. "
            "Characterization includes UV-Vis spectroscopy, photoluminescence, and activity tests."
        ),
        key_factors=["band gap", "light wavelength", "charge separation", "surface reactivity", "doping"],
        primary_authority=["Fujishima & Honda (1972)", "Somorjai & Li (2010)", "IUPAC Recommendations"],
        burden_holder="Photocatalyst developer",
        adversary_position="Limited visible light activity and rapid charge recombination reduce efficiency.",
        counter_arguments=[
            "Doping and surface modification enhance visible light activity.",
            "Nanostructuring improves charge separation.",
            "Hybrid systems increase efficiency."
        ],
        resolution_strategy="Optimize catalyst design for light absorption and charge separation; apply modifications for visible light activity.",
        entity_scope="Photocatalyst, light source",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Fujishima & Honda, Nature 1972, 238, 37"
    ),
    DoctrineBlock(
        topic="Electrocatalysis: HER, OER, ORR, Overpotential",
        keywords=["electrocatalysis", "HER", "OER", "ORR", "overpotential", "electrode", "energy conversion"],
        conclusion_template="Electrocatalysts facilitate HER, OER, and ORR with minimized overpotential, enabling efficient energy conversion in fuel cells and electrolyzers.",
        reasoning_framework=(
            "Electrocatalysis involves the acceleration of electrochemical reactions (Hydrogen Evolution Reaction - HER, Oxygen Evolution Reaction - OER, Oxygen Reduction Reaction - ORR) at electrode surfaces. "
            "Catalyst design aims to minimize overpotential and maximize activity and stability. Platinum is benchmark for HER and ORR, but alternatives (Ni, Co, Fe, Mn oxides) are developed for cost and durability. "
            "Characterization includes cyclic voltammetry, Tafel plots, and stability tests. Mechanistic understanding guides material selection and electrode architecture."
        ),
        key_factors=["catalyst material", "overpotential", "activity", "stability", "electrode architecture"],
        primary_authority=["Trasatti (1972)", "IUPAC Recommendations", "Somorjai & Li (2010)"],
        burden_holder="Electrocatalyst developer",
        adversary_position="High cost and limited durability of benchmark catalysts hinder commercialization.",
        counter_arguments=[
            "Non-precious metal catalysts offer cost-effective alternatives.",
            "Material design improves durability.",
            "Electrode engineering enhances performance."
        ],
        resolution_strategy="Develop and optimize non-precious metal catalysts; engineer electrodes for stability and activity.",
        entity_scope="Electrochemical cell, electrode",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Trasatti, J. Electroanal. Chem. 1972, 39, 163"
    ),
    DoctrineBlock(
        topic="Biocatalysis: Immobilized Enzymes and Whole Cells",
        keywords=["biocatalysis", "immobilized enzymes", "whole cells", "stability", "reusability", "biotransformation"],
        conclusion_template="Biocatalysis utilizes immobilized enzymes or whole cells for enhanced stability, reusability, and process control in biotransformations.",
        reasoning_framework=(
            "Immobilization of enzymes or whole cells on solid supports improves stability, facilitates reuse, and enables continuous processing. Methods include adsorption, covalent binding, entrapment, and encapsulation. "
            "Whole-cell biocatalysis leverages native metabolic pathways for complex transformations. Immobilization affects activity, diffusion, and operational stability. Process optimization involves balancing activity, stability, and mass transfer."
        ),
        key_factors=["immobilization method", "support material", "enzyme/cell activity", "stability", "mass transfer"],
        primary_authority=["Sheldon (2007)", "IUPAC Recommendations", "Nelson & Cox (2021)"],
        burden_holder="Bioprocess engineer",
        adversary_position="Immobilization may reduce activity and introduce diffusion limitations.",
        counter_arguments=[
            "Optimized immobilization preserves activity.",
            "Support selection mitigates diffusion limitations.",
            "Process design balances trade-offs."
        ],
        resolution_strategy="Select immobilization method and support based on biocatalyst and process requirements; optimize for activity and stability.",
        entity_scope="Biocatalyst, support, reactor",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Sheldon, Adv. Synth. Catal. 2007, 349, 1289"
    ),
    DoctrineBlock(
        topic="Catalyst Selectivity, Conversion, Yield, TON, TOF",
        keywords=["catalyst selectivity", "conversion", "yield", "turnover number", "turnover frequency", "performance metrics"],
        conclusion_template="Catalyst performance is quantified by selectivity, conversion, yield, turnover number (TON), and turnover frequency (TOF).",
        reasoning_framework=(
            "Selectivity measures the fraction of desired product relative to total products. Conversion is the fraction of reactant transformed. Yield is the amount of desired product per reactant. "
            "TON is the number of catalytic cycles per active site, and TOF is TON per unit time. These metrics guide catalyst evaluation and process optimization. Accurate measurement requires careful experimental design and analysis."
        ),
        key_factors=["product distribution", "reactant conversion", "active site count", "reaction time", "process conditions"],
        primary_authority=["IUPAC Recommendations", "Somorjai & Li (2010)", "Hartwig (2010)"],
        burden_holder="Catalyst evaluator",
        adversary_position="Metrics may be affected by side reactions, mass transfer, and measurement errors.",
        counter_arguments=[
            "Rigorous experimental protocols minimize errors.",
            "Side reactions can be quantified and accounted for.",
            "Mass transfer limitations are addressed via reactor design."
        ],
        resolution_strategy="Apply standardized protocols for measurement; account for side reactions and transfer limitations.",
        entity_scope="Catalyst, reactant, product",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IUPAC, Pure Appl. Chem. 1982, 54, 2201"
    ),
    DoctrineBlock(
        topic="Mass Transfer Limitations: Thiele Modulus and Effectiveness Factor",
        keywords=["mass transfer", "Thiele modulus", "effectiveness factor", "internal diffusion", "external diffusion", "reaction rate"],
        conclusion_template="Mass transfer limitations are quantified by Thiele modulus and effectiveness factor, guiding catalyst and reactor design.",
        reasoning_framework=(
            "The Thiele modulus (ϕ) relates reaction rate to internal diffusion: ϕ = (L/2) * sqrt(k/De), where L is particle size, k is rate constant, De is effective diffusivity. "
            "Effectiveness factor (η) is the ratio of observed rate to intrinsic rate, indicating the impact of diffusion limitations. High ϕ means strong diffusion limitation; η < 1. "
            "External diffusion is managed by optimizing flow and mixing. Accurate assessment guides catalyst particle size and reactor design for optimal performance."
        ),
        key_factors=["particle size", "diffusivity", "reaction rate", "flow conditions", "reactor design"],
        primary_authority=["Levenspiel (1999)", "Fogler (2016)", "IUPAC Recommendations"],
        burden_holder="Process engineer",
        adversary_position="Mass transfer limitations reduce observed activity and complicate scale-up.",
        counter_arguments=[
            "Design optimization minimizes limitations.",
            "Advanced modeling predicts performance.",
            "Pilot-scale testing validates design."
        ],
        resolution_strategy="Quantify and minimize mass transfer limitations via design and modeling; validate experimentally.",
        entity_scope="Catalyst particle, reactor",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Levenspiel, Chemical Reaction Engineering, 3rd Ed."
    ),
    DoctrineBlock(
        topic="Catalyst Regeneration: Oxidative and Reductive Methods",
        keywords=["catalyst regeneration", "oxidative regeneration", "reductive regeneration", "activity restoration", "deactivation"],
        conclusion_template="Catalyst regeneration employs oxidative or reductive methods to restore activity after deactivation.",
        reasoning_framework=(
            "Regeneration removes deactivating species (e.g., coke, poisons) via oxidative (burn-off) or reductive (hydrogen treatment) methods. Oxidative regeneration is used for carbon removal; reductive methods restore metal states. "
            "Regeneration protocol depends on catalyst type, deactivation mechanism, and process requirements. Monitoring activity and selectivity guides timing and method selection. Proper regeneration extends catalyst lifetime and process efficiency."
        ),
        key_factors=["deactivation mechanism", "regeneration method", "catalyst type", "process conditions", "activity monitoring"],
        primary_authority=["Bartholomew (2001)", "IUPAC Recommendations", "Somorjai & Li (2010)"],
        burden_holder="Catalyst operator",
        adversary_position="Regeneration may not fully restore original activity; repeated cycles can degrade catalyst.",
        counter_arguments=[
            "Optimized protocols minimize degradation.",
            "Monitoring guides timely intervention.",
            "Catalyst design improves regeneration tolerance."
        ],
        resolution_strategy="Select regeneration method based on catalyst and deactivation; optimize protocol and monitor performance.",
        entity_scope="Catalyst bed, reactor",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Bartholomew, Appl. Catal. A 2001, 212, 17"
    ),
    DoctrineBlock(
        topic="Green Chemistry: Atom Economy and E-Factor",
        keywords=["green chemistry", "atom economy", "E-factor", "sustainability", "waste minimization"],
        conclusion_template="Green chemistry principles prioritize atom economy and low E-factor to minimize waste and maximize resource utilization.",
        reasoning_framework=(
            "Atom economy measures the fraction of reactant atoms incorporated into desired products, guiding reaction selection for minimal waste. E-factor quantifies waste generated per unit product. "
            "Catalytic processes are favored for high atom economy and low E-factor. Process design, solvent selection, and catalyst choice influence sustainability. Regulatory and economic pressures drive adoption of green chemistry metrics."
        ),
        key_factors=["atom economy", "E-factor", "process design", "solvent selection", "catalyst choice"],
        primary_authority=["Anastas & Warner (1998)", "Sheldon (2007)", "IUPAC Recommendations"],
        burden_holder="Process developer",
        adversary_position="Trade-offs between efficiency and sustainability may occur.",
        counter_arguments=[
            "Catalytic processes often offer both efficiency and sustainability.",
            "Process optimization balances trade-offs.",
            "Regulatory incentives encourage green chemistry adoption."
        ],
        resolution_strategy="Prioritize catalytic processes with high atom economy and low E-factor; optimize for sustainability.",
        entity_scope="Process, reactants, products",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Anastas & Warner, Green Chemistry, 1998"
    ),
    DoctrineBlock(
        topic="Catalyst Preparation: Impregnation, Precipitation, Sol-Gel",
        keywords=["catalyst preparation", "impregnation", "precipitation", "sol-gel", "active site dispersion", "support"],
        conclusion_template="Catalyst preparation methods (impregnation, precipitation, sol-gel) determine active site dispersion and performance.",
        reasoning_framework=(
            "Impregnation deposits metal precursors onto supports, followed by drying and calcination. Precipitation forms active phases from solution, enabling control of particle size. Sol-gel produces highly dispersed materials "
            "with tunable porosity. Preparation affects active site distribution, support interaction, and stability. Characterization (XRD, BET, TEM) guides optimization. Process scalability and reproducibility are critical for industrial application."
        ),
        key_factors=["preparation method", "precursor chemistry", "support interaction", "particle size", "porosity"],
        primary_authority=["Somorjai & Li (2010)", "IUPAC Recommendations", "Campbell & Sellers (2012)"],
        burden_holder="Catalyst manufacturer",
        adversary_position="Preparation method may introduce impurities or limit scalability.",
        counter_arguments=[
            "Optimized protocols minimize impurities.",
            "Scale-up strategies ensure reproducibility.",
            "Characterization validates quality."
        ],
        resolution_strategy="Select preparation method based on catalyst and process requirements; optimize for dispersion and scalability.",
        entity_scope="Catalyst material, support",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Somorjai & Li, Introduction to Surface Chemistry, 2010"
    ),
    DoctrineBlock(
        topic="Organocatalysis: Small Molecule Catalysts",
        keywords=["organocatalysis", "small molecule catalyst", "asymmetric synthesis", "selectivity", "green chemistry"],
        conclusion_template="Organocatalysis employs small organic molecules to catalyze reactions, offering selectivity and sustainability.",
        reasoning_framework=(
            "Small molecule organocatalysts (e.g., proline, imidazoles) facilitate a range of transformations, including asymmetric synthesis. Advantages include metal-free processes, mild conditions, and high selectivity. "
            "Mechanistic understanding enables rational catalyst design. Limitations include lower activity compared to metal catalysts and sensitivity to reaction conditions. Applications span pharmaceuticals, fine chemicals, and green chemistry."
        ),
        key_factors=["catalyst structure", "reaction mechanism", "selectivity", "activity", "process conditions"],
        primary_authority=["MacMillan (2008)", "IUPAC Recommendations", "Anastas & Warner (1998)"],
        burden_holder="Synthetic chemist",
        adversary_position="Organocatalysts may exhibit lower activity and limited substrate scope.",
        counter_arguments=[
            "Rational design improves activity and scope.",
            "Combination with other catalytic strategies enhances performance.",
            "Green chemistry principles favor organocatalysis."
        ],
        resolution_strategy="Optimize organocatalyst structure and conditions; combine with other strategies as needed.",
        entity_scope="Organic reactants, catalyst",
        confidence=0.87,
        confidence_zone="Moderate-High",
        controlling_precedent="MacMillan, Nature 2008, 455, 304"
    ),
    DoctrineBlock(
        topic="Metal-Organic Frameworks (MOFs) in Catalysis",
        keywords=["MOF", "metal-organic framework", "catalysis", "porosity", "active site", "heterogeneous catalysis"],
        conclusion_template="MOFs offer tunable porosity and active site distribution for heterogeneous catalysis, enabling selective transformations.",
        reasoning_framework=(
            "Metal-organic frameworks (MOFs) are crystalline materials with high surface area and tunable pore structure. Catalytic activity is introduced via metal nodes, organic linkers, or post-synthetic modification. "
            "MOFs enable selective catalysis, including oxidation, hydrogenation, and CO2 conversion. Stability and scalability are challenges; advances in synthesis and post-modification address these issues. Characterization (XRD, BET, IR) guides application."
        ),
        key_factors=["pore structure", "active site distribution", "stability", "scalability", "modification"],
        primary_authority=["Furukawa (2013)", "IUPAC Recommendations", "Somorjai & Li (2010)"],
        burden_holder="Catalyst developer",
        adversary_position="MOFs may suffer from limited stability and scalability.",
        counter_arguments=[
            "Post-synthetic modification improves stability.",
            "Hybrid materials address scalability.",
            "Application-specific design enhances performance."
        ],
        resolution_strategy="Select MOF based on reaction and stability requirements; apply modifications for scalability.",
        entity_scope="MOF material, reactants",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Furukawa, Science 2013, 341, 1230444"
    ),
    DoctrineBlock(
        topic="Enzyme Engineering: Directed Evolution and Rational Design",
        keywords=["enzyme engineering", "directed evolution", "rational design", "biocatalysis", "activity", "selectivity"],
        conclusion_template="Enzyme engineering via directed evolution and rational design enhances activity, selectivity, and stability for biocatalytic applications.",
        reasoning_framework=(
            "Directed evolution involves iterative mutation and selection to improve enzyme properties. Rational design uses structural and mechanistic knowledge to introduce targeted changes. "
            "Combining both approaches yields biocatalysts with enhanced activity, selectivity, and stability. Screening and characterization guide optimization. Applications include pharmaceuticals, fine chemicals, and sustainable processes."
        ),
        key_factors=["mutation strategy", "selection protocol", "structural knowledge", "activity", "stability"],
        primary_authority=["Arnold (1998)", "Sheldon (2007)", "Nelson & Cox (2021)"],
        burden_holder="Biocatalyst developer",
        adversary_position="Directed evolution may require extensive screening; rational design is limited by structural knowledge.",
        counter_arguments=[
            "Combining approaches maximizes efficiency.",
            "High-throughput screening accelerates evolution.",
            "Structural advances expand rational design."
        ],
        resolution_strategy="Integrate directed evolution and rational design; optimize screening and structural analysis.",
        entity_scope="Enzyme, substrate",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Arnold, Acc. Chem. Res. 1998, 31, 125"
    ),
    DoctrineBlock(
        topic="Solid Acid Catalysis: Sulfated Zirconia, Phosphoric Acid",
        keywords=["solid acid catalysis", "sulfated zirconia", "phosphoric acid", "acid strength", "hydrocarbon conversion"],
        conclusion_template="Solid acid catalysts (sulfated zirconia, phosphoric acid) provide strong acidity for hydrocarbon conversion and fine chemical synthesis.",
        reasoning_framework=(
            "Sulfated zirconia and phosphoric acid on silica are solid acids with high activity for isomerization, alkylation, and cracking. Acid strength and site distribution are tuned by preparation and support. "
            "Catalyst stability and resistance to deactivation are critical for industrial application. Characterization (NH3-TPD, IR) guides optimization. Applications include fuel upgrading and specialty chemicals."
        ),
        key_factors=["acid strength", "site distribution", "stability", "preparation method", "feed composition"],
        primary_authority=["Corma (1995)", "IUPAC Recommendations", "Somorjai & Li (2010)"],
        burden_holder="Catalyst designer",
        adversary_position="Solid acids may suffer from rapid deactivation and limited selectivity.",
        counter_arguments=[
            "Optimized preparation improves stability.",
            "Site tuning enhances selectivity.",
            "Regeneration protocols restore activity."
        ],
        resolution_strategy="Select solid acid based on reaction and stability requirements; optimize preparation and regeneration.",
        entity_scope="Catalyst material, reactants",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Corma, Chem. Rev. 1995, 95, 559"
    ),
    DoctrineBlock(
        topic="Supported Metal Catalysts: Dispersion and Metal-Support Interaction",
        keywords=["supported metal catalyst", "dispersion", "metal-support interaction", "activity", "selectivity"],
        conclusion_template="Supported metal catalysts rely on high dispersion and strong metal-support interaction for optimal activity and selectivity.",
        reasoning_framework=(
            "Dispersion of metal particles on supports increases active site accessibility. Metal-support interaction influences electronic properties, stability, and activity. Preparation methods (impregnation, deposition) and support selection "
            "are critical. Characterization (TEM, XPS, chemisorption) guides optimization. Applications include hydrogenation, oxidation, and environmental catalysis."
        ),
        key_factors=["metal dispersion", "support type", "interaction strength", "preparation method", "activity"],
        primary_authority=["Somorjai & Li (2010)", "IUPAC Recommendations", "Campbell & Sellers (2012)"],
        burden_holder="Catalyst manufacturer",
        adversary_position="Low dispersion and weak interaction reduce activity and stability.",
        counter_arguments=[
            "Optimized preparation maximizes dispersion.",
            "Support selection enhances interaction.",
            "Characterization validates performance."
        ],
        resolution_strategy="Select preparation and support for high dispersion and interaction; characterize and optimize.",
        entity_scope="Catalyst material, support",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Somorjai & Li, Introduction to Surface Chemistry, 2010"
    ),
    DoctrineBlock(
        topic="Homogeneous Catalysis: Ligand Effects and Solvent Influence",
        keywords=["homogeneous catalysis", "ligand effects", "solvent influence", "selectivity", "reaction rate"],
        conclusion_template="Ligand and solvent selection in homogeneous catalysis modulate activity, selectivity, and stability.",
        reasoning_framework=(
            "Ligands control electronic and steric properties of metal centers, affecting activity and selectivity. Solvents influence solubility, reaction rate, and stability. Rational selection of ligands and solvents enables "
            "fine-tuning of catalytic performance. Mechanistic studies and computational modeling guide optimization. Applications span hydrogenation, cross-coupling, and asymmetric synthesis."
        ),
        key_factors=["ligand structure", "solvent polarity", "metal center", "reaction mechanism", "activity"],
        primary_authority=["Hartwig (2010)", "IUPAC Recommendations", "Wilkinson (1965)"],
        burden_holder="Catalyst developer",
        adversary_position="Ligand and solvent effects may complicate optimization and reproducibility.",
        counter_arguments=[
            "Mechanistic studies clarify effects.",
            "Computational modeling aids prediction.",
            "Standardized protocols improve reproducibility."
        ],
        resolution_strategy="Select ligands and solvents based on mechanistic understanding; optimize via experimentation and modeling.",
        entity_scope="Solution-phase catalytic system",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Hartwig, Organotransition Metal Chemistry, 2010"
    ),
    DoctrineBlock(
        topic="Enzyme Immobilization: Methods and Impact",
        keywords=["enzyme immobilization", "adsorption", "covalent binding", "entrapment", "activity", "stability"],
        conclusion_template="Enzyme immobilization methods (adsorption, covalent binding, entrapment) affect activity, stability, and process performance.",
        reasoning_framework=(
            "Adsorption is simple but may suffer from leaching. Covalent binding offers stability but may reduce activity. Entrapment and encapsulation protect enzymes but introduce diffusion limitations. "
            "Selection depends on enzyme, substrate, and process requirements. Characterization (activity assays, stability tests) guides optimization. Applications include biotransformation, biosensors, and medical devices."
        ),
        key_factors=["immobilization method", "support material", "enzyme activity", "stability", "diffusion"],
        primary_authority=["Sheldon (2007)", "Nelson & Cox (2021)", "IUPAC Recommendations"],
        burden_holder="Bioprocess engineer",
        adversary_position="Immobilization may reduce activity and introduce mass transfer limitations.",
        counter_arguments=[
            "Optimized method preserves activity.",
            "Support selection mitigates limitations.",
            "Process design balances trade-offs."
        ],
        resolution_strategy="Select immobilization method based on enzyme and process; optimize for activity and stability.",
        entity_scope="Enzyme, support, reactor",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Sheldon, Adv. Synth. Catal. 2007, 349, 1289"
    ),
    DoctrineBlock(
        topic="Catalyst Poisoning: Sulfur, Lead, and Chlorine Effects",
        keywords=["catalyst poisoning", "sulfur", "lead", "chlorine", "activity loss", "regeneration"],
        conclusion_template="Catalyst poisoning by sulfur, lead, and chlorine causes irreversible activity loss; prevention and regeneration strategies are essential.",
        reasoning_framework=(
            "Poisoning occurs when impurities bind strongly to active sites, blocking catalytic function. Sulfur, lead, and chlorine are common poisons in industrial processes. Prevention involves feed purification and catalyst design. "
            "Regeneration may restore activity, but irreversible poisoning requires catalyst replacement. Monitoring impurity levels and activity guides intervention. Applications include petroleum refining, automotive, and environmental catalysis."
        ),
        key_factors=["impurity concentration", "catalyst design", "feed purification", "regeneration method", "activity monitoring"],
        primary_authority=["Bartholomew (2001)", "IUPAC Recommendations", "Somorjai & Li (2010)"],
        burden_holder="Catalyst operator",
        adversary_position="Poisoning is often irreversible and costly.",
        counter_arguments=[
            "Feed purification reduces risk.",
            "Catalyst design improves resistance.",
            "Monitoring enables timely intervention."
        ],
        resolution_strategy="Implement feed purification and monitoring; design catalysts for resistance; replace as needed.",
        entity_scope="Catalyst bed, reactor",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="Bartholomew, Appl. Catal. A 2001, 212, 17"
    ),
    DoctrineBlock(
        topic="Catalyst Stability: Thermal and Mechanical Effects",
        keywords=["catalyst stability", "thermal stability", "mechanical stability", "activity", "lifetime"],
        conclusion_template="Catalyst stability under thermal and mechanical stress determines activity and lifetime; robust design and monitoring are essential.",
        reasoning_framework=(
            "Thermal stability is critical for high-temperature processes; sintering and phase changes reduce activity. Mechanical stability prevents attrition and loss of active material. Design involves selecting stable supports, optimizing preparation, "
            "and monitoring performance. Applications include FCC, ammonia synthesis, and environmental catalysis. Characterization (TGA, XRD, mechanical tests) guides optimization."
        ),
        key_factors=["operating temperature", "support stability", "mechanical strength", "preparation method", "activity monitoring"],
        primary_authority=["Somorjai & Li (2010)", "IUPAC Recommendations", "Bartholomew (2001)"],
        burden_holder="Catalyst manufacturer",
        adversary_position="Stability challenges limit catalyst lifetime and process efficiency.",
        counter_arguments=[
            "Robust design and monitoring extend lifetime.",
            "Advanced materials improve stability.",
            "Regeneration protocols restore activity."
        ],
        resolution_strategy="Select stable materials and supports; monitor and regenerate as needed.",
        entity_scope="Catalyst material, reactor",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Somorjai & Li, Introduction to Surface Chemistry, 2010"
    ),
    DoctrineBlock(
        topic="Catalyst Testing: Activity, Selectivity, and Lifetime",
        keywords=["catalyst testing", "activity", "selectivity", "lifetime", "performance evaluation"],
        conclusion_template="Catalyst testing evaluates activity, selectivity, and lifetime under relevant conditions; standardized protocols ensure reliability.",
        reasoning_framework=(
            "Testing involves measuring conversion, product distribution, and stability over time. Standardized protocols (e.g., fixed-bed, batch, flow reactors) ensure comparability. Characterization of spent catalysts identifies deactivation mechanisms. "
            "Data guides catalyst selection and process optimization. Applications include industrial, environmental, and fine chemical catalysis."
        ),
        key_factors=["testing protocol", "reaction conditions", "activity measurement", "selectivity", "lifetime"],
        primary_authority=["IUPAC Recommendations", "Somorjai & Li (2010)", "Bartholomew (2001)"],
        burden_holder="Catalyst evaluator",
        adversary_position="Testing under non-representative conditions may mislead performance assessment.",
        counter_arguments=[
            "Protocols are designed for relevance.",
            "Spent catalyst analysis identifies issues.",
            "Continuous improvement ensures accuracy."
        ],
        resolution_strategy="Apply standardized and relevant testing protocols; analyze spent catalysts for improvement.",
        entity_scope="Catalyst, reactor, products",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IUPAC, Pure Appl. Chem. 1982, 54, 2201"
    ),
    DoctrineBlock(
        topic="Catalyst Recycling and Sustainability",
        keywords=["catalyst recycling", "sustainability", "resource utilization", "waste minimization", "green chemistry"],
        conclusion_template="Catalyst recycling enhances sustainability by minimizing waste and maximizing resource utilization.",
        reasoning_framework=(
            "Recycling involves recovery and reuse of catalysts, reducing environmental impact and cost. Methods include separation, regeneration, and reactivation. Process design and catalyst selection influence recyclability. "
            "Sustainability metrics (atom economy, E-factor) guide optimization. Regulatory and economic pressures drive adoption. Applications include industrial, environmental, and fine chemical catalysis."
        ),
        key_factors=["recycling method", "regeneration efficiency", "process design", "sustainability metrics", "regulatory compliance"],
        primary_authority=["Anastas & Warner (1998)", "Sheldon (2007)", "IUPAC Recommendations"],
        burden_holder="Process developer",
        adversary_position="Recycling may reduce activity and introduce impurities.",
        counter_arguments=[
            "Optimized methods preserve activity.",
            "Process design minimizes impurity introduction.",
            "Regulatory incentives encourage recycling."
        ],
        resolution_strategy="Select catalysts and processes for recyclability; optimize recycling and regeneration protocols.",
        entity_scope="Catalyst, process, products",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Anastas & Warner, Green Chemistry, 1998"
    ),
    DoctrineBlock(
        topic="Catalyst Screening: High-Throughput and Computational Methods",
        keywords=["catalyst screening", "high-throughput", "computational screening", "activity", "selectivity"],
        conclusion_template="High-throughput and computational screening accelerate catalyst discovery and optimization.",
        reasoning_framework=(
            "High-throughput screening uses parallel experimentation to rapidly evaluate catalyst libraries. Computational methods (DFT, machine learning) predict activity and selectivity, guiding experimental design. "
            "Integration of both approaches accelerates discovery and optimization. Applications include pharmaceuticals, fine chemicals, and sustainable processes."
        ),
        key_factors=["screening method", "library size", "computational accuracy", "activity measurement", "selectivity"],
        primary_authority=["Sheldon (2007)", "IUPAC Recommendations", "Hartwig (2010)"],
        burden_holder="Catalyst developer",
        adversary_position="Computational predictions may lack accuracy; high-throughput may miss long-term stability.",
        counter_arguments=[
            "Experimental validation ensures reliability.",
            "Integration improves efficiency.",
            "Continuous improvement enhances accuracy."
        ],
        resolution_strategy="Combine computational and high-throughput screening; validate experimentally.",
        entity_scope="Catalyst library, reactants",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Sheldon, Adv. Synth. Catal. 2007, 349, 1289"
    ),
    DoctrineBlock(
        topic="Catalyst Structure-Activity Relationship (SAR)",
        keywords=["structure-activity relationship", "SAR", "catalyst design", "activity", "selectivity"],
        conclusion_template="Structure-activity relationship (SAR) analysis guides catalyst design for optimal activity and selectivity.",
        reasoning_framework=(
            "SAR correlates structural features (e.g., active site geometry, electronic properties) with catalytic performance. Mechanistic studies, computational modeling, and experimental data inform design. "
            "Applications include pharmaceuticals, fine chemicals, and industrial catalysis. Continuous improvement and validation ensure reliability."
        ),
        key_factors=["structural features", "activity", "selectivity", "mechanistic understanding", "modeling"],
        primary_authority=["Hartwig (2010)", "IUPAC Recommendations", "Somorjai & Li (2010)"],
        burden_holder="Catalyst designer",
        adversary_position="SAR may oversimplify complex systems.",
        counter_arguments=[
            "Mechanistic studies refine SAR.",
            "Computational modeling improves prediction.",
            "Experimental validation ensures accuracy."
        ],
        resolution_strategy="Integrate SAR with mechanistic and computational studies; validate experimentally.",
        entity_scope="Catalyst, reactants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Hartwig, Organotransition Metal Chemistry, 2010"
    ),
    DoctrineBlock(
        topic="Catalyst Performance Metrics: Productivity and Efficiency",
        keywords=["catalyst performance", "productivity", "efficiency", "activity", "selectivity"],
        conclusion_template="Catalyst productivity and efficiency are key metrics for process evaluation and optimization.",
        reasoning_framework=(
            "Productivity measures product output per unit catalyst and time. Efficiency combines activity, selectivity, and stability. Accurate measurement guides process optimization and catalyst selection. "
            "Applications include industrial, environmental, and fine chemical catalysis. Standardized protocols and continuous improvement ensure reliability."
        ),
        key_factors=["productivity", "efficiency", "activity", "selectivity", "stability"],
        primary_authority=["IUPAC Recommendations", "Somorjai & Li (2010)", "Hartwig (2010)"],
        burden_holder="Process engineer",
        adversary_position="Metrics may be affected by process variability and measurement errors.",
        counter_arguments=[
            "Standardized protocols minimize errors.",
            "Continuous monitoring improves reliability.",
            "Process optimization balances trade-offs."
        ],
        resolution_strategy="Apply standardized protocols; monitor and optimize for productivity and efficiency.",
        entity_scope="Catalyst, process, products",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IUPAC, Pure Appl. Chem. 1982, 54, 2201"
    ),
    DoctrineBlock(
        topic="Catalyst Lifetime and Replacement Strategies",
        keywords=["catalyst lifetime", "replacement", "activity loss", "process optimization", "cost"],
        conclusion_template="Catalyst lifetime is managed by monitoring activity and implementing replacement strategies for sustained process performance.",
        reasoning_framework=(
            "Lifetime depends on deactivation mechanisms, process conditions, and regeneration protocols. Monitoring activity guides replacement timing. Cost and process optimization influence strategy. Applications include industrial, environmental, and fine chemical catalysis."
        ),
        key_factors=["activity monitoring", "deactivation mechanism", "regeneration efficiency", "cost", "process optimization"],
        primary_authority=["Bartholomew (2001)", "IUPAC Recommendations", "Somorjai & Li (2010)"],
        burden_holder="Process engineer",
        adversary_position="Replacement increases cost and downtime.",
        counter_arguments=[
            "Optimized monitoring minimizes downtime.",
            "Regeneration extends lifetime.",
            "Process design balances cost and performance."
        ],
        resolution_strategy="Monitor activity; optimize regeneration and replacement timing; balance cost and performance.",
        entity_scope="Catalyst, process",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Bartholomew, Appl. Catal. A 2001, 212, 17"
    ),
    DoctrineBlock(
        topic="Catalyst Safety: Handling and Disposal",
        keywords=["catalyst safety", "handling", "disposal", "hazard", "regulatory compliance"],
        conclusion_template="Safe handling and disposal of catalysts are essential for regulatory compliance and environmental protection.",
        reasoning_framework=(
            "Catalysts may pose hazards (toxicity, flammability, environmental impact). Handling protocols include PPE, storage, and spill management. Disposal follows regulatory guidelines, including hazardous waste classification and recycling. "
            "Training and monitoring ensure compliance. Applications include industrial, environmental, and fine chemical catalysis."
        ),
        key_factors=["hazard classification", "handling protocol", "disposal method", "regulatory compliance", "training"],
        primary_authority=["IUPAC Recommendations", "Anastas & Warner (1998)", "Somorjai & Li (2010)"],
        burden_holder="Process operator",
        adversary_position="Improper handling and disposal pose risks.",
        counter_arguments=[
            "Training and protocols minimize risks.",
            "Regulatory compliance is enforced.",
            "Recycling reduces environmental impact."
        ],
        resolution_strategy="Implement handling and disposal protocols; train personnel; comply with regulations.",
        entity_scope="Catalyst, process",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IUPAC, Pure Appl. Chem. 1982, 54, 2201"
    ),
    DoctrineBlock(
        topic="Catalyst Environmental Impact: Life Cycle Assessment",
        keywords=["catalyst environmental impact", "life cycle assessment", "LCA", "sustainability", "green chemistry"],
        conclusion_template="Life cycle assessment (LCA) evaluates catalyst environmental impact, guiding sustainable process design.",
        reasoning_framework=(
            "LCA quantifies environmental impact from catalyst production, use, and disposal. Metrics include energy consumption, emissions, and resource utilization. Sustainable design minimizes impact via recycling, green chemistry, and process optimization. "
            "Regulatory and economic pressures drive adoption. Applications include industrial, environmental, and fine chemical catalysis."
        ),
        key_factors=["LCA metrics", "production impact", "use impact", "disposal impact", "sustainability"],
        primary_authority=["Anastas & Warner (1998)", "Sheldon (2007)", "IUPAC Recommendations"],
        burden_holder="Process developer",
        adversary_position="LCA may be complex and resource-intensive.",
        counter_arguments=[
            "Standardized protocols simplify LCA.",
            "Continuous improvement enhances accuracy.",
            "Regulatory incentives encourage adoption."
        ],
        resolution_strategy="Apply standardized LCA protocols; optimize process for sustainability.",
        entity_scope="Catalyst, process",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Anastas & Warner, Green Chemistry, 1998"
    ),
    DoctrineBlock(
        topic="Catalyst Intellectual Property: Patents and Licensing",
        keywords=["catalyst intellectual property", "patents", "licensing", "innovation", "regulatory compliance"],
        conclusion_template="Catalyst innovation is protected by patents and licensing, ensuring regulatory compliance and commercial advantage.",
        reasoning_framework=(
            "Patents protect novel catalyst compositions, preparation methods, and applications. Licensing enables commercialization and technology transfer. Regulatory compliance ensures safety and environmental protection. "
            "Monitoring patent landscape guides innovation strategy. Applications include industrial, environmental, and fine chemical catalysis."
        ),
        key_factors=["patent protection", "licensing", "innovation", "regulatory compliance", "commercialization"],
        primary_authority=["USPTO Guidelines", "IUPAC Recommendations", "Anastas & Warner (1998)"],
        burden_holder="Catalyst developer",
        adversary_position="Patent disputes and regulatory hurdles may delay commercialization.",
        counter_arguments=[
            "Legal and regulatory expertise mitigates risks.",
            "Continuous monitoring guides strategy.",
            "Licensing enables technology transfer."
        ],
        resolution_strategy="Monitor patent landscape; comply with regulations; optimize licensing and commercialization.",
        entity_scope="Catalyst, process",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="USPTO, Patent Guidelines"
    ),
    DoctrineBlock(
        topic="Catalyst Scale-Up: Pilot and Industrial Processes",
        keywords=["catalyst scale-up", "pilot process", "industrial process", "activity", "selectivity"],
        conclusion_template="Catalyst scale-up from pilot to industrial processes requires optimization of activity, selectivity, and stability.",
        reasoning_framework=(
            "Scale-up involves translating laboratory performance to industrial scale, addressing mixing, heat transfer, and mass transfer limitations. Pilot testing validates design and identifies challenges. Process optimization balances activity, selectivity, stability, and cost. "
            "Applications include industrial, environmental, and fine chemical catalysis."
        ),
        key_factors=["pilot testing", "process optimization", "activity", "selectivity", "stability"],
        primary_authority=["Levenspiel (1999)", "Fogler (2016)", "IUPAC Recommendations"],
        burden_holder="Process engineer",
        adversary_position="Scale-up may introduce performance loss and operational challenges.",
        counter_arguments=[
            "Pilot testing identifies and mitigates issues.",
            "Process optimization improves performance.",
            "Continuous monitoring ensures reliability."
        ],
        resolution_strategy="Pilot test and optimize process; monitor and address challenges during scale-up.",
        entity_scope="Catalyst, process",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Levenspiel, Chemical Reaction Engineering, 3rd Ed."
    ),
    DoctrineBlock(
        topic="Catalyst Process Integration: Upstream and Downstream Effects",
        keywords=["catalyst process integration", "upstream", "downstream", "activity", "selectivity"],
        conclusion_template="Catalyst process integration considers upstream and downstream effects for optimal performance and sustainability.",
        reasoning_framework=(
            "Integration involves aligning catalyst performance with upstream feedstock and downstream product requirements. Process optimization balances activity, selectivity, and sustainability. Applications include industrial, environmental, and fine chemical catalysis."
        ),
        key_factors=["feedstock quality", "product requirements", "activity", "selectivity", "sustainability"],
        primary_authority=["Anastas & Warner (1998)", "Sheldon (2007)", "IUPAC Recommendations"],
        burden_holder="Process developer",
        adversary_position="Integration may introduce complexity and trade-offs.",
        counter_arguments=[
            "Process optimization balances trade-offs.",
            "Continuous monitoring ensures reliability.",
            "Sustainability metrics guide integration."
        ],
        resolution_strategy="Optimize process integration for performance and sustainability; monitor and adjust as needed.",
        entity_scope="Catalyst, process",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Anastas & Warner, Green Chemistry, 1998"
    ),
    DoctrineBlock(
        topic="Catalyst Analytical Methods: Spectroscopy and Microscopy",
        keywords=["catalyst analytical methods", "spectroscopy", "microscopy", "characterization", "activity"],
        conclusion_template="Spectroscopy and microscopy provide critical insights into catalyst structure and activity.",
        reasoning_framework=(
            "Spectroscopic methods (IR, UV-Vis, XPS, EXAFS) reveal electronic structure, composition, and active sites. Microscopy (TEM, SEM, AFM) visualizes morphology, dispersion, and particle size. Integration of both approaches guides catalyst design and optimization."
        ),
        key_factors=["spectroscopic method", "microscopy method", "structure", "activity", "characterization"],
        primary_authority=["IUPAC Recommendations", "Somorjai & Li (2010)", "Campbell & Sellers (2012)"],
        burden_holder="Catalyst analyst",
        adversary_position="Methods may lack resolution or introduce artifacts.",
        counter_arguments=[
            "Multi-technique approach mitigates limitations.",
            "Advanced methods improve accuracy.",
            "Continuous improvement enhances reliability."
        ],
        resolution_strategy="Integrate spectroscopy and microscopy; optimize methods for accuracy and resolution.",
        entity_scope="Catalyst material",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IUPAC, Pure Appl. Chem. 1982, 54, 2201"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    results = []
    kw_lower = keyword.lower()
    for doctrine in DOCTRINE_CACHE:
        if kw_lower in doctrine.topic.lower() or any(kw_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]