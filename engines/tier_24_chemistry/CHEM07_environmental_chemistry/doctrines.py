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
        topic="Acid-Base Equilibria in Environmental Waters",
        keywords=["acid-base", "pH", "buffering", "carbonate system", "dissociation constants", "environmental waters"],
        conclusion_template="The pH of environmental waters is primarily governed by the carbonate buffering system, modulated by acid-base equilibria and external inputs.",
        reasoning_framework=(
            "Environmental waters maintain pH through a dynamic equilibrium involving carbonic acid (H2CO3), bicarbonate (HCO3-), "
            "and carbonate (CO3^2-) ions. The dissociation constants (Ka1 and Ka2) of carbonic acid dictate the speciation of carbonate species. "
            "External acid or base inputs shift this equilibrium, but the buffering capacity resists pH changes. "
            "Temperature and ionic strength also influence the equilibrium constants. The system can be modeled using the Henderson-Hasselbalch equation, "
            "and the total inorganic carbon concentration serves as a key parameter. Anthropogenic acidification, such as acid rain, can overwhelm buffering, "
            "leading to pH shifts detrimental to aquatic life. Understanding these equilibria is critical for predicting water quality and ecosystem health."
        ),
        key_factors=["carbonate concentration", "dissociation constants", "temperature", "acid/base inputs", "buffer capacity"],
        primary_authority=["Stumm & Morgan, Aquatic Chemistry, 3rd Ed., 1996", "Hem, J.D., Study and Interpretation of the Chemical Characteristics of Natural Water, USGS, 1985"],
        burden_holder="Environmental chemist assessing water quality",
        adversary_position="pH changes are solely due to external acid/base inputs without buffering effects",
        counter_arguments=[
            "Buffering capacity demonstrated by stable pH despite acid inputs",
            "Measured carbonate species concentrations correlate with pH stability",
            "Thermodynamic data supports carbonate system equilibrium"
        ],
        resolution_strategy="Use comprehensive carbonate system modeling incorporating all species and constants to predict pH changes accurately.",
        entity_scope="Freshwater and marine environmental waters",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Stumm & Morgan (1996) established carbonate buffering as central to aquatic pH regulation."
    ),
    DoctrineBlock(
        topic="Redox Potential and Speciation of Metals in Soils",
        keywords=["redox potential", "Eh", "metal speciation", "soil chemistry", "oxidation states", "environmental chemistry"],
        conclusion_template="The redox potential (Eh) of soils critically determines the speciation and mobility of metals, influencing their environmental fate and toxicity.",
        reasoning_framework=(
            "Redox potential (Eh) reflects the electron activity in soils and governs the oxidation state of metals such as iron, manganese, arsenic, and chromium. "
            "Under oxidizing conditions, metals tend to exist in higher oxidation states (e.g., Fe(III), Cr(VI)) which often have different solubility and toxicity profiles compared to reduced forms (Fe(II), Cr(III)). "
            "Soil Eh is influenced by microbial activity, organic matter content, moisture, and oxygen availability. "
            "The Nernst equation relates Eh to the ratio of oxidized and reduced species. "
            "Metal speciation affects adsorption/desorption equilibria, bioavailability, and transport. "
            "For example, arsenic is more mobile and toxic as arsenate (As(V)) under oxidizing conditions, whereas arsenite (As(III)) dominates under reducing conditions. "
            "Predicting metal behavior requires integrating Eh with pH and complexation equilibria."
        ),
        key_factors=["soil Eh", "pH", "microbial activity", "organic matter", "metal oxidation states"],
        primary_authority=["Stumm & Morgan, Aquatic Chemistry, 3rd Ed., 1996", "Sposito, The Chemistry of Soils, 2nd Ed., 2008"],
        burden_holder="Soil chemist evaluating metal contamination risks",
        adversary_position="Metal speciation is independent of redox conditions, controlled only by total metal concentration",
        counter_arguments=[
            "Empirical data showing metal speciation shifts with Eh changes",
            "Thermodynamic predictions of species stability under varying Eh",
            "Observed changes in metal mobility correlated with redox fluctuations"
        ],
        resolution_strategy="Incorporate Eh measurements and redox-sensitive speciation models in environmental risk assessments.",
        entity_scope="Soil environments with variable redox conditions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Sposito (2008) detailed the role of redox in soil metal chemistry."
    ),
    DoctrineBlock(
        topic="Photodegradation of Organic Pollutants in Surface Waters",
        keywords=["photodegradation", "organic pollutants", "surface waters", "photolysis", "reactive oxygen species", "environmental fate"],
        conclusion_template="Photodegradation via direct photolysis and indirect reactions mediated by reactive oxygen species significantly reduces concentrations of organic pollutants in surface waters.",
        reasoning_framework=(
            "Organic pollutants in surface waters undergo photodegradation driven by sunlight absorption. "
            "Direct photolysis occurs when pollutants absorb photons and undergo bond cleavage or transformation. "
            "Indirect photodegradation involves photosensitizers such as dissolved organic matter (DOM) generating reactive oxygen species (ROS) like hydroxyl radicals (•OH), singlet oxygen (1O2), and superoxide (O2•−). "
            "These ROS react with pollutants via oxidation, leading to their breakdown. "
            "Factors affecting photodegradation rates include light intensity and spectrum, water depth, turbidity, pollutant structure, and presence of sensitizers or quenchers. "
            "Kinetic modeling often uses first-order rate constants derived from experimental data. "
            "Understanding these mechanisms is essential for predicting pollutant persistence and designing remediation strategies."
        ),
        key_factors=["light intensity", "pollutant absorption spectrum", "presence of DOM", "water clarity", "ROS generation"],
        primary_authority=["Zepp et al., Environmental Science & Technology, 1987", "Canonica et al., Chemosphere, 2005"],
        burden_holder="Environmental chemist assessing pollutant degradation",
        adversary_position="Photodegradation is negligible compared to other removal processes",
        counter_arguments=[
            "Measured photolysis rate constants under natural sunlight",
            "Detection of transformation products consistent with photodegradation",
            "ROS scavenger experiments confirming indirect photolysis pathways"
        ],
        resolution_strategy="Combine photodegradation kinetics with other fate processes in comprehensive environmental models.",
        entity_scope="Surface freshwater and marine environments",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Zepp et al. (1987) established photodegradation as a key pollutant removal mechanism."
    ),
    DoctrineBlock(
        topic="Bioaccumulation of Persistent Organic Pollutants (POPs)",
        keywords=["bioaccumulation", "persistent organic pollutants", "POPs", "lipophilicity", "biomagnification", "environmental toxicology"],
        conclusion_template="Persistent organic pollutants bioaccumulate in organisms due to their lipophilicity and resistance to metabolic degradation, leading to biomagnification through food webs.",
        reasoning_framework=(
            "POPs such as polychlorinated biphenyls (PCBs), dioxins, and organochlorine pesticides resist environmental degradation and accumulate in lipid-rich tissues of organisms. "
            "Their hydrophobic nature leads to partitioning into biological membranes and fat stores. "
            "Metabolic pathways in many organisms cannot efficiently degrade these compounds, resulting in accumulation over time. "
            "Biomagnification occurs as predators consume contaminated prey, increasing POP concentrations at higher trophic levels. "
            "This process poses risks to wildlife and humans, including endocrine disruption and carcinogenicity. "
            "Quantitative structure-activity relationships (QSAR) and bioconcentration factors (BCF) are used to predict bioaccumulation potential. "
            "Regulatory frameworks such as the Stockholm Convention aim to control and reduce POP emissions."
        ),
        key_factors=["lipophilicity", "metabolic resistance", "trophic transfer", "environmental persistence", "organism lipid content"],
        primary_authority=["Jones & de Voogt, Environmental Science & Technology, 1999", "UNEP Stockholm Convention, 2001"],
        burden_holder="Environmental toxicologist assessing ecological risk",
        adversary_position="POPs do not bioaccumulate significantly due to metabolic breakdown",
        counter_arguments=[
            "Empirical measurements of POP concentrations increasing with trophic level",
            "Laboratory studies showing low metabolic degradation rates",
            "Field observations of adverse effects linked to POP exposure"
        ],
        resolution_strategy="Incorporate bioaccumulation factors and trophic transfer models in risk assessments and regulatory decisions.",
        entity_scope="Aquatic and terrestrial food webs",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Jones & de Voogt (1999) comprehensively reviewed POP bioaccumulation mechanisms."
    ),
    DoctrineBlock(
        topic="Sorption of Heavy Metals onto Clay Minerals",
        keywords=["sorption", "heavy metals", "clay minerals", "adsorption", "cation exchange", "environmental remediation"],
        conclusion_template="Heavy metals sorb onto clay minerals primarily through cation exchange and surface complexation, reducing their mobility in soils and sediments.",
        reasoning_framework=(
            "Clay minerals possess negatively charged surfaces due to isomorphic substitution and broken edges, providing sites for cation sorption. "
            "Heavy metals such as Pb(II), Cd(II), and Cu(II) interact with these sites via electrostatic attraction and specific surface complexation. "
            "The extent of sorption depends on pH, ionic strength, metal speciation, and clay mineralogy. "
            "Cation exchange capacity (CEC) quantifies the ability of clays to retain metal ions. "
            "Sorption reduces metal bioavailability and transport but can be reversible under changing environmental conditions. "
            "Models such as the constant capacitance and diffuse layer models describe sorption equilibria. "
            "Understanding sorption mechanisms informs remediation strategies like soil amendments and immobilization."
        ),
        key_factors=["clay mineral type", "pH", "CEC", "metal speciation", "ionic strength"],
        primary_authority=["Sposito, The Chemistry of Soils, 2nd Ed., 2008", "Dzombak & Morel, Surface Complexation Modeling, 1990"],
        burden_holder="Environmental engineer designing remediation",
        adversary_position="Heavy metals remain fully mobile regardless of clay presence",
        counter_arguments=[
            "Batch sorption experiments showing metal uptake by clays",
            "Spectroscopic evidence of surface complexation",
            "Reduced metal leaching in clay-rich soils"
        ],
        resolution_strategy="Apply surface complexation models and sorption isotherms to predict metal immobilization.",
        entity_scope="Soils and sediments with clay mineral content",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Dzombak & Morel (1990) established surface complexation as key to metal sorption."
    ),
    DoctrineBlock(
        topic="Nutrient Cycling: Nitrogen Transformations in Aquatic Systems",
        keywords=["nitrogen cycle", "nitrification", "denitrification", "ammonification", "aquatic systems", "environmental chemistry"],
        conclusion_template="Nitrogen transformations in aquatic systems proceed through ammonification, nitrification, and denitrification, regulating nitrogen availability and ecosystem health.",
        reasoning_framework=(
            "Organic nitrogen compounds decompose via ammonification to release ammonium (NH4+). "
            "Nitrification, a two-step aerobic microbial process, oxidizes ammonium to nitrite (NO2-) and then nitrate (NO3-). "
            "Denitrification occurs under anoxic conditions, reducing nitrate to gaseous nitrogen (N2) or nitrous oxide (N2O), removing bioavailable nitrogen. "
            "These processes are influenced by oxygen availability, temperature, pH, organic carbon, and microbial community structure. "
            "The balance of these transformations affects eutrophication potential and nitrogen retention. "
            "Isotopic tracing and molecular biology techniques elucidate pathway dynamics. "
            "Management of nitrogen inputs requires understanding these coupled biogeochemical cycles."
        ),
        key_factors=["oxygen levels", "microbial activity", "organic carbon", "temperature", "pH"],
        primary_authority=["Wetzel, Limnology, 3rd Ed., 2001", "Gruber & Galloway, Nature, 2008"],
        burden_holder="Aquatic ecologist managing nutrient pollution",
        adversary_position="Nitrogen transformations are static and unaffected by environmental conditions",
        counter_arguments=[
            "Observed shifts in nitrogen species concentrations with oxygen gradients",
            "Experimental manipulation of microbial communities altering nitrogen fluxes",
            "Isotopic evidence of active denitrification"
        ],
        resolution_strategy="Integrate nitrogen transformation kinetics into ecosystem nutrient models for management.",
        entity_scope="Freshwater and estuarine aquatic systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Wetzel (2001) detailed nitrogen cycling in aquatic environments."
    ),
    DoctrineBlock(
        topic="Formation and Environmental Impact of Acid Rain",
        keywords=["acid rain", "sulfur dioxide", "nitrogen oxides", "atmospheric chemistry", "environmental impact", "acidification"],
        conclusion_template="Acid rain forms from atmospheric oxidation of sulfur dioxide and nitrogen oxides, leading to acidification of soils and waters with ecological consequences.",
        reasoning_framework=(
            "Combustion of fossil fuels releases SO2 and NOx gases into the atmosphere. "
            "These gases undergo oxidation to form sulfuric acid (H2SO4) and nitric acid (HNO3), which dissolve in atmospheric moisture. "
            "The resulting acid precipitation lowers pH of rainwater, contributing to acidification of soils and aquatic systems. "
            "Acid rain mobilizes toxic metals, damages vegetation, and alters microbial communities. "
            "Chemical transport models simulate the formation and deposition patterns. "
            "Mitigation involves emission controls and regulatory policies. "
            "Monitoring pH and ion concentrations in precipitation provides data for assessing acid rain impacts."
        ),
        key_factors=["SO2 and NOx emissions", "atmospheric oxidation", "precipitation chemistry", "soil buffering capacity", "ecosystem sensitivity"],
        primary_authority=["Likens et al., Science, 1979", "EPA Acid Rain Program Documentation"],
        burden_holder="Environmental policy maker regulating emissions",
        adversary_position="Acid rain effects are overstated and natural variability dominates",
        counter_arguments=[
            "Long-term monitoring showing pH declines correlated with emissions",
            "Experimental evidence of acid rain damage to biota",
            "Chemical analysis confirming acid deposition composition"
        ],
        resolution_strategy="Implement emission reduction strategies and monitor ecosystem recovery.",
        entity_scope="Regional to global atmospheric and terrestrial environments",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Likens et al. (1979) seminal study linking emissions to acid rain effects."
    ),
    DoctrineBlock(
        topic="Mercury Methylation in Aquatic Sediments",
        keywords=["mercury", "methylation", "aquatic sediments", "microbial processes", "toxicity", "environmental chemistry"],
        conclusion_template="Microbial methylation of inorganic mercury in aquatic sediments produces methylmercury, a bioaccumulative neurotoxin with significant ecological risks.",
        reasoning_framework=(
            "Inorganic mercury deposited in sediments undergoes methylation primarily by anaerobic sulfate-reducing and iron-reducing bacteria. "
            "Methylmercury (MeHg) is more toxic and readily bioaccumulates in aquatic food webs. "
            "Factors influencing methylation rates include organic matter availability, redox conditions, sulfate concentration, and microbial community composition. "
            "Demethylation processes also occur but are generally slower. "
            "Sediment geochemistry and hydrology affect mercury speciation and transport. "
            "Analytical methods such as gas chromatography coupled with mass spectrometry quantify MeHg levels. "
            "Understanding methylation dynamics is critical for managing mercury contamination and protecting wildlife and human health."
        ),
        key_factors=["microbial activity", "redox conditions", "organic matter", "sulfate levels", "mercury speciation"],
        primary_authority=["Compeau & Bartha, Applied and Environmental Microbiology, 1985", "US EPA Mercury Study Report to Congress, 1997"],
        burden_holder="Environmental scientist assessing mercury risk",
        adversary_position="Mercury methylation is insignificant in sediments and does not affect toxicity",
        counter_arguments=[
            "Measured MeHg concentrations in sediments and biota",
            "Correlation between sulfate-reducing bacteria abundance and methylation rates",
            "Toxicological studies demonstrating MeHg effects"
        ],
        resolution_strategy="Monitor sediment conditions and microbial communities; apply remediation to limit methylation.",
        entity_scope="Freshwater and estuarine sediments",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Compeau & Bartha (1985) identified microbial mercury methylation mechanisms."
    ),
    DoctrineBlock(
        topic="Groundwater Contamination by Nitrate and Its Remediation",
        keywords=["groundwater", "nitrate contamination", "remediation", "denitrification", "environmental chemistry", "pollution control"],
        conclusion_template="Nitrate contamination in groundwater poses health risks but can be mitigated through enhanced denitrification and source control strategies.",
        reasoning_framework=(
            "Nitrate (NO3-) from agricultural runoff, septic systems, and industrial sources infiltrates groundwater, causing contamination. "
            "High nitrate levels pose risks such as methemoglobinemia in infants and ecosystem eutrophication. "
            "Denitrification, a microbial anaerobic process, reduces nitrate to nitrogen gas, naturally attenuating contamination. "
            "Remediation approaches include bioreactors, permeable reactive barriers, and controlled redox environments to promote denitrification. "
            "Source control through best management practices reduces nitrate inputs. "
            "Monitoring nitrate concentrations and isotopic signatures helps track contamination and remediation effectiveness. "
            "Hydrogeological factors influence nitrate transport and persistence."
        ),
        key_factors=["nitrate sources", "microbial denitrification", "redox conditions", "hydrogeology", "remediation technology"],
        primary_authority=["Keeney & Hatfield, Nitrogen in the Environment, 1998", "USGS Groundwater Reports"],
        burden_holder="Environmental engineer managing groundwater quality",
        adversary_position="Nitrate contamination is irreversible and remediation is ineffective",
        counter_arguments=[
            "Field studies showing nitrate reduction via denitrification",
            "Successful implementation of bioreactors and barriers",
            "Isotopic evidence of nitrate transformation"
        ],
        resolution_strategy="Combine source reduction with engineered and natural remediation methods.",
        entity_scope="Shallow and deep groundwater systems",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Keeney & Hatfield (1998) comprehensive review of nitrogen in groundwater."
    ),
    DoctrineBlock(
        topic="Role of Dissolved Organic Matter (DOM) in Metal Complexation",
        keywords=["dissolved organic matter", "metal complexation", "environmental chemistry", "ligands", "metal mobility"],
        conclusion_template="Dissolved organic matter forms complexes with metals, influencing their solubility, transport, and bioavailability in aquatic environments.",
        reasoning_framework=(
            "DOM contains functional groups such as carboxyl, phenolic, and hydroxyl moieties capable of binding metal ions through coordination bonds. "
            "Complexation affects metal speciation, reducing free ion concentrations and altering toxicity and mobility. "
            "The strength and nature of complexes depend on DOM composition, metal type, pH, and ionic strength. "
            "Spectroscopic and electrochemical methods characterize metal-DOM interactions. "
            "Models such as the NICA-Donnan model simulate complexation behavior. "
            "DOM-metal complexes can enhance transport or facilitate sedimentation depending on size and charge. "
            "Understanding these interactions is vital for predicting metal fate and designing treatment processes."
        ),
        key_factors=["DOM composition", "metal ion characteristics", "pH", "ionic strength", "complex stability constants"],
        primary_authority=["Tipping, Chemical Reviews, 1994", "Kinniburgh et al., Environmental Science & Technology, 1999"],
        burden_holder="Environmental chemist assessing metal transport",
        adversary_position="Metals exist only as free ions and do not complex with DOM",
        counter_arguments=[
            "Spectroscopic evidence of metal-DOM binding",
            "Observed changes in metal bioavailability with DOM concentration",
            "Modeling results consistent with complexation phenomena"
        ],
        resolution_strategy="Incorporate metal-DOM complexation in speciation and transport models.",
        entity_scope="Freshwater and marine aquatic systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Tipping (1994) established fundamental principles of metal-DOM complexation."
    ),
    DoctrineBlock(
        topic="Environmental Fate of Microplastics in Aquatic Systems",
        keywords=["microplastics", "environmental fate", "aquatic systems", "adsorption", "transport", "degradation"],
        conclusion_template="Microplastics persist in aquatic environments, undergoing physical transport, surface adsorption of pollutants, and limited degradation, impacting ecosystems.",
        reasoning_framework=(
            "Microplastics, defined as plastic particles <5 mm, enter aquatic systems from various sources including wastewater and runoff. "
            "They are transported by currents, settle in sediments, or remain suspended depending on density and biofouling. "
            "Surface properties allow adsorption of hydrophobic organic pollutants and metals, potentially acting as vectors for contaminant transport. "
            "Degradation processes include photodegradation, mechanical abrasion, and biodegradation, but rates are slow, leading to persistence. "
            "Ecotoxicological effects arise from ingestion by aquatic organisms and chemical exposure. "
            "Analytical challenges exist in detection and quantification. "
            "Management requires source reduction and improved waste treatment."
        ),
        key_factors=["particle size and density", "hydrodynamics", "surface chemistry", "pollutant adsorption", "degradation rates"],
        primary_authority=["Andrady, Marine Pollution Bulletin, 2011", "Galloway et al., Environmental Science & Technology, 2017"],
        burden_holder="Marine environmental scientist assessing pollution",
        adversary_position="Microplastics rapidly degrade and pose minimal environmental risk",
        counter_arguments=[
            "Field measurements showing widespread microplastic presence",
            "Laboratory studies demonstrating slow degradation",
            "Evidence of pollutant adsorption and biological uptake"
        ],
        resolution_strategy="Implement monitoring, source control, and research on degradation pathways.",
        entity_scope="Marine and freshwater aquatic environments",
        confidence=0.88,
        confidence_zone="Moderate to High",
        controlling_precedent="Andrady (2011) comprehensive review of microplastic environmental behavior."
    ),
    DoctrineBlock(
        topic="Use of Stable Isotopes in Tracing Environmental Chemical Processes",
        keywords=["stable isotopes", "environmental tracing", "isotope fractionation", "chemical processes", "environmental chemistry"],
        conclusion_template="Stable isotope ratios provide insights into environmental chemical processes through characteristic fractionation patterns.",
        reasoning_framework=(
            "Stable isotopes of elements such as carbon (13C/12C), nitrogen (15N/14N), oxygen (18O/16O), and sulfur (34S/32S) vary naturally due to fractionation during chemical, physical, and biological processes. "
            "Isotope ratio mass spectrometry (IRMS) measures these ratios, enabling tracing of sources, pathways, and transformations of chemicals in the environment. "
            "Fractionation factors depend on reaction mechanisms and environmental conditions. "
            "Applications include tracking pollutant degradation, nutrient cycling, and source apportionment. "
            "Interpretation requires understanding baseline isotope signatures and potential mixing. "
            "Isotopic labeling experiments complement natural abundance studies for process elucidation."
        ),
        key_factors=["isotope ratios", "fractionation mechanisms", "analytical precision", "baseline signatures", "environmental context"],
        primary_authority=["Hoefs, Stable Isotope Geochemistry, 2009", "Fry, Stable Isotope Ecology, 2006"],
        burden_holder="Environmental chemist conducting source and process identification",
        adversary_position="Isotope ratios are too variable and unreliable for environmental tracing",
        counter_arguments=[
            "Reproducible fractionation patterns observed in controlled and field studies",
            "Successful application in diverse environmental contexts",
            "Analytical advances improving precision and accuracy"
        ],
        resolution_strategy="Use isotope data alongside complementary chemical and biological information for robust interpretation.",
        entity_scope="Terrestrial, aquatic, and atmospheric environments",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Hoefs (2009) foundational text on isotope geochemistry."
    ),
    DoctrineBlock(
        topic="Mechanisms of Photochemical Smog Formation",
        keywords=["photochemical smog", "NOx", "VOC", "ozone", "atmospheric chemistry", "environmental pollution"],
        conclusion_template="Photochemical smog forms through sunlight-driven reactions of nitrogen oxides and volatile organic compounds, producing ozone and secondary pollutants.",
        reasoning_framework=(
            "Photochemical smog arises in urban atmospheres with high emissions of NOx and VOCs under strong sunlight. "
            "NO2 photolyzes to NO and atomic oxygen, which reacts with O2 to form ozone (O3). "
            "VOCs undergo oxidation producing peroxy radicals that convert NO to NO2 without consuming ozone, allowing ozone accumulation. "
            "Secondary pollutants include aldehydes, peroxides, and particulate matter. "
            "Meteorological conditions such as temperature inversions and stagnant air exacerbate smog formation. "
            "Chemical kinetics models simulate reaction pathways and pollutant concentrations. "
            "Control strategies target emission reductions and photochemical precursors."
        ),
        key_factors=["NOx emissions", "VOC emissions", "solar radiation", "meteorology", "reaction kinetics"],
        primary_authority=["Seinfeld & Pandis, Atmospheric Chemistry and Physics, 2016", "Finlayson-Pitts & Pitts, Chemistry of the Upper and Lower Atmosphere, 2000"],
        burden_holder="Air quality manager regulating urban pollution",
        adversary_position="Smog formation is unrelated to NOx and VOC photochemistry",
        counter_arguments=[
            "Correlation of smog episodes with precursor emissions",
            "Laboratory and field studies confirming reaction mechanisms",
            "Model predictions matching observed pollutant levels"
        ],
        resolution_strategy="Implement emission controls and monitor atmospheric chemistry to mitigate smog.",
        entity_scope="Urban and industrial atmospheres",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Seinfeld & Pandis (2016) comprehensive atmospheric chemistry framework."
    ),
    DoctrineBlock(
        topic="Chemical Oxygen Demand (COD) as a Measure of Water Pollution",
        keywords=["chemical oxygen demand", "COD", "water pollution", "organic matter", "oxidation", "environmental monitoring"],
        conclusion_template="COD quantifies the oxygen equivalent of organic matter oxidizable by strong chemical oxidants, serving as an indicator of water pollution.",
        reasoning_framework=(
            "COD measures the amount of oxygen required to chemically oxidize organic and inorganic substances in water using a strong oxidant, typically potassium dichromate in acidic conditions. "
            "It provides a rapid estimate of the pollution load, complementing biological oxygen demand (BOD) measurements. "
            "COD is influenced by sample composition, reaction conditions, and presence of interfering substances. "
            "Standardized methods ensure reproducibility. "
            "High COD values indicate elevated organic pollution, affecting aquatic life and water treatment processes. "
            "Interpretation requires understanding of sample matrix and potential oxidant demand from non-organic species."
        ),
        key_factors=["organic matter concentration", "oxidation conditions", "sample matrix", "interfering substances", "method standardization"],
        primary_authority=["APHA Standard Methods for the Examination of Water and Wastewater, 23rd Ed., 2017"],
        burden_holder="Water quality analyst assessing pollution levels",
        adversary_position="COD does not correlate with organic pollution and is unreliable",
        counter_arguments=[
            "Correlation between COD and organic pollutant concentrations",
            "Standardized protocols ensuring method accuracy",
            "Use of COD in regulatory frameworks worldwide"
        ],
        resolution_strategy="Use COD alongside complementary parameters for comprehensive water quality assessment.",
        entity_scope="Surface waters and wastewater",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="APHA Standard Methods widely accepted for COD measurement."
    ),
    DoctrineBlock(
        topic="Environmental Impact of Chlorinated Hydrocarbons",
        keywords=["chlorinated hydrocarbons", "environmental impact", "persistence", "toxicity", "bioaccumulation", "environmental chemistry"],
        conclusion_template="Chlorinated hydrocarbons persist in the environment, exhibiting toxicity and bioaccumulation that pose risks to ecosystems and human health.",
        reasoning_framework=(
            "Chlorinated hydrocarbons such as DDT, chlordane, and PCBs resist biodegradation due to their stable carbon-chlorine bonds. "
            "Their lipophilicity leads to accumulation in fatty tissues of organisms, causing biomagnification. "
            "Toxic effects include endocrine disruption, carcinogenicity, and immunotoxicity. "
            "Environmental transport occurs via air, water, and sediment pathways. "
            "Dechlorination under anaerobic conditions can transform these compounds but often slowly. "
            "Regulatory bans and restrictions have reduced emissions, but legacy contamination persists. "
            "Risk assessment integrates chemical properties, exposure pathways, and toxicological data."
        ),
        key_factors=["chemical stability", "lipophilicity", "environmental transport", "toxicity", "degradation pathways"],
        primary_authority=["ATSDR Toxicological Profiles", "WHO Environmental Health Criteria"],
        burden_holder="Environmental toxicologist evaluating chemical hazards",
        adversary_position="Chlorinated hydrocarbons degrade rapidly and are not environmentally concerning",
        counter_arguments=[
            "Persistence demonstrated by long environmental half-lives",
            "Epidemiological evidence of health impacts",
            "Detection in remote ecosystems indicating long-range transport"
        ],
        resolution_strategy="Maintain monitoring, enforce regulations, and remediate contaminated sites.",
        entity_scope="Global environmental compartments",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="ATSDR and WHO authoritative assessments on chlorinated hydrocarbons."
    ),
    DoctrineBlock(
        topic="Sulfate Reduction and Metal Sulfide Precipitation in Anoxic Environments",
        keywords=["sulfate reduction", "metal sulfides", "anoxic environments", "microbial metabolism", "environmental chemistry"],
        conclusion_template="Microbial sulfate reduction in anoxic environments leads to metal sulfide precipitation, influencing metal mobility and sediment geochemistry.",
        reasoning_framework=(
            "Sulfate-reducing bacteria (SRB) utilize sulfate as an electron acceptor, producing hydrogen sulfide (H2S). "
            "H2S reacts with dissolved metal ions such as Fe(II), Pb(II), and Zn(II) to form insoluble metal sulfides (e.g., FeS, PbS). "
            "This process immobilizes metals, reducing their bioavailability and toxicity. "
            "Factors affecting sulfate reduction include organic carbon availability, temperature, pH, and competing electron acceptors. "
            "Metal sulfide formation impacts sediment diagenesis and can influence trace metal cycling. "
            "Analytical techniques include porewater chemistry and mineralogical analysis. "
            "Understanding these processes aids in predicting contaminant fate and designing remediation."
        ),
        key_factors=["SRB activity", "sulfate concentration", "metal ion availability", "organic carbon", "redox conditions"],
        primary_authority=["Jørgensen, Marine Geochemistry, 1982", "Canfield et al., Sulfur Biogeochemistry, 2010"],
        burden_holder="Environmental geochemist studying sediment chemistry",
        adversary_position="Sulfate reduction does not affect metal speciation or mobility",
        counter_arguments=[
            "Observed metal sulfide mineral formation in anoxic sediments",
            "Correlation between SRB abundance and sulfide production",
            "Geochemical modeling supporting precipitation reactions"
        ],
        resolution_strategy="Incorporate microbial and geochemical data in sediment metal fate models.",
        entity_scope="Anoxic sediments in aquatic environments",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Jørgensen (1982) foundational work on sulfate reduction in sediments."
    ),
    DoctrineBlock(
        topic="Volatilization of Organic Chemicals from Surface Waters",
        keywords=["volatilization", "organic chemicals", "surface waters", "Henry's law", "environmental fate"],
        conclusion_template="Volatilization governed by Henry's law constant and environmental conditions significantly contributes to the removal of volatile organic chemicals from surface waters.",
        reasoning_framework=(
            "Volatilization is the transfer of dissolved organic chemicals from water to the atmosphere driven by concentration gradients and governed by Henry's law constant (H). "
            "Higher H values indicate greater tendency to volatilize. "
            "Environmental factors such as temperature, wind speed, and water turbulence enhance volatilization rates. "
            "The process reduces aqueous concentrations but can lead to atmospheric transport and deposition elsewhere. "
            "Modeling volatilization requires integrating mass transfer coefficients and environmental parameters. "
            "Volatilization competes with other removal processes like biodegradation and sorption."
        ),
        key_factors=["Henry's law constant", "temperature", "wind speed", "water turbulence", "chemical concentration"],
        primary_authority=["Mackay, Multimedia Environmental Models, 2001", "Schwarzenbach et al., Environmental Organic Chemistry, 2003"],
        burden_holder="Environmental chemist modeling chemical fate",
        adversary_position="Volatilization is negligible for organic chemicals in water",
        counter_arguments=[
            "Measured volatilization fluxes consistent with Henry's law predictions",
            "Field studies showing atmospheric presence linked to water sources",
            "Laboratory volatilization rate experiments"
        ],
        resolution_strategy="Include volatilization in multimedia fate models for accurate predictions.",
        entity_scope="Surface freshwater and marine waters",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Mackay (2001) multimedia modeling framework."
    ),
    DoctrineBlock(
        topic="Role of Enzymatic Catalysis in Biodegradation of Pollutants",
        keywords=["enzymatic catalysis", "biodegradation", "pollutants", "microbial enzymes", "environmental chemistry"],
        conclusion_template="Microbial enzymatic catalysis accelerates biodegradation of pollutants by transforming complex compounds into simpler, less toxic forms.",
        reasoning_framework=(
            "Microorganisms produce enzymes such as oxygenases, hydrolases, and reductases that catalyze the breakdown of pollutants including hydrocarbons, pesticides, and chlorinated compounds. "
            "Enzymatic reactions lower activation energy, enabling transformations under ambient environmental conditions. "
            "Pathways include oxidation, hydrolysis, dehalogenation, and ring cleavage. "
            "Enzyme expression is regulated by pollutant availability and environmental factors. "
            "Biodegradation rates depend on enzyme kinetics, microbial community structure, and pollutant bioavailability. "
            "Molecular biology tools identify key enzymes and genes involved. "
            "Bioremediation strategies harness enzymatic catalysis to enhance pollutant removal."
        ),
        key_factors=["enzyme types", "microbial community", "pollutant structure", "environmental conditions", "enzyme kinetics"],
        primary_authority=["Alexander, Biodegradation and Bioremediation, 1999", "Fetzner, Applied Microbiology and Biotechnology, 1998"],
        burden_holder="Environmental biotechnologist designing remediation",
        adversary_position="Biodegradation occurs without enzymatic catalysis and is slow",
        counter_arguments=[
            "Characterization of pollutant-degrading enzymes",
            "Enhanced degradation rates linked to enzyme activity",
            "Genetic evidence of enzyme-mediated pathways"
        ],
        resolution_strategy="Apply enzyme-focused bioremediation and monitor enzymatic activity.",
        entity_scope="Soils, sediments, and aquatic environments",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Alexander (1999) authoritative text on biodegradation."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Per- and Polyfluoroalkyl Substances (PFAS)",
        keywords=["PFAS", "perfluoroalkyl substances", "environmental chemistry", "persistence", "toxicity", "contamination"],
        conclusion_template="PFAS are highly persistent environmental contaminants with widespread distribution and potential adverse health effects.",
        reasoning_framework=(
            "PFAS are synthetic fluorinated compounds characterized by strong C-F bonds, conferring chemical and thermal stability. "
            "They resist degradation, leading to accumulation in water, soil, and biota. "
            "PFAS exhibit surfactant properties and can bioaccumulate, with some compounds linked to toxicity including immunotoxicity and carcinogenicity. "
            "Environmental transport occurs via water and air pathways. "
            "Analytical challenges include low concentrations and complex mixtures. "
            "Regulatory agencies are developing guidelines and restrictions. "
            "Remediation technologies include adsorption, advanced oxidation, and membrane filtration."
        ),
        key_factors=["chemical stability", "environmental transport", "bioaccumulation", "toxicity", "analytical detection"],
        primary_authority=["EPA PFAS Action Plan", "OECD PFAS Reports"],
        burden_holder="Environmental chemist assessing emerging contaminants",
        adversary_position="PFAS degrade readily and pose minimal risk",
        counter_arguments=[
            "Environmental monitoring showing persistent PFAS presence",
            "Toxicological studies indicating adverse effects",
            "Regulatory recognition of PFAS as contaminants of concern"
        ],
        resolution_strategy="Implement monitoring, risk assessment, and advanced remediation technologies.",
        entity_scope="Global environmental compartments",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="EPA and OECD authoritative documents on PFAS."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Radionuclides in Groundwater",
        keywords=["radionuclides", "groundwater", "radioactive decay", "speciation", "environmental chemistry", "contamination"],
        conclusion_template="Radionuclide behavior in groundwater is governed by radioactive decay, speciation, sorption, and transport processes affecting environmental risk.",
        reasoning_framework=(
            "Radionuclides such as uranium, radium, and technetium enter groundwater from natural sources and anthropogenic activities. "
            "Radioactive decay reduces radionuclide concentrations over time, characterized by half-lives. "
            "Speciation affects solubility and mobility; for example, uranium exists as U(VI) and U(IV) species with differing behaviors. "
            "Sorption onto mineral surfaces and complexation with ligands influence transport. "
            "Hydrogeological factors control dispersion and dilution. "
            "Modeling radionuclide fate requires integrating decay kinetics with geochemical and transport processes. "
            "Risk assessments consider exposure pathways and dose calculations."
        ),
        key_factors=["radioactive decay", "speciation", "sorption", "complexation", "hydrogeology"],
        primary_authority=["IAEA Safety Reports", "Langmuir, Radiochimica Acta, 1997"],
        burden_holder="Environmental radiochemist assessing contamination",
        adversary_position="Radionuclides behave like stable elements without decay or speciation effects",
        counter_arguments=[
            "Measured decay rates consistent with nuclear physics",
            "Speciation-dependent mobility observed in field studies",
            "Sorption experiments demonstrating radionuclide retention"
        ],
        resolution_strategy="Use integrated radiochemical and geochemical models for environmental management.",
        entity_scope="Groundwater systems impacted by radionuclides",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="IAEA and Langmuir (1997) authoritative sources on radionuclide chemistry."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Polycyclic Aromatic Hydrocarbons (PAHs)",
        keywords=["PAHs", "polycyclic aromatic hydrocarbons", "environmental chemistry", "persistence", "toxicity", "transport"],
        conclusion_template="PAHs are persistent organic pollutants with hydrophobicity leading to sediment accumulation and toxic effects on biota.",
        reasoning_framework=(
            "PAHs are formed during incomplete combustion of organic matter and released into the environment via atmospheric deposition and direct discharge. "
            "Their hydrophobic nature causes strong sorption to organic-rich sediments and soils, limiting aqueous mobility but enabling long-term persistence. "
            "PAHs exhibit mutagenic and carcinogenic properties. "
            "Environmental degradation occurs via photolysis, microbial metabolism, and chemical oxidation but is often slow. "
            "Transport pathways include atmospheric transport, runoff, and sediment resuspension. "
            "Analytical methods include GC-MS for detection and quantification. "
            "Risk assessments integrate exposure, toxicity, and environmental fate."
        ),
        key_factors=["hydrophobicity", "sorption", "degradation rates", "toxicity", "transport pathways"],
        primary_authority=["EPA PAH Assessment Reports", "Menzie et al., Environmental Science & Technology, 1992"],
        burden_holder="Environmental chemist evaluating pollutant impact",
        adversary_position="PAHs degrade rapidly and pose minimal environmental risk",
        counter_arguments=[
            "Environmental monitoring showing persistent PAH residues",
            "Toxicological data confirming adverse effects",
            "Slow degradation rates documented in sediments"
        ],
        resolution_strategy="Monitor PAH levels and apply remediation where necessary.",
        entity_scope="Soils, sediments, and aquatic environments",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="EPA and Menzie et al. (1992) assessments on PAHs."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Chlorinated Solvents",
        keywords=["chlorinated solvents", "environmental chemistry", "contamination", "degradation", "groundwater pollution"],
        conclusion_template="Chlorinated solvents are common groundwater contaminants with complex degradation pathways influencing persistence and toxicity.",
        reasoning_framework=(
            "Chlorinated solvents such as trichloroethylene (TCE) and perchloroethylene (PCE) are widely used industrial solvents. "
            "They enter groundwater through spills and leaks, exhibiting variable solubility and density leading to complex plume behavior. "
            "Degradation occurs via abiotic reductive dechlorination and microbial processes, producing intermediates like vinyl chloride. "
            "Some degradation products are more toxic than parent compounds. "
            "Sorption and volatilization affect transport. "
            "Remediation includes pump-and-treat, bioremediation, and chemical oxidation. "
            "Monitoring requires sensitive analytical methods and understanding of degradation pathways."
        ),
        key_factors=["solvent properties", "degradation pathways", "toxicity of intermediates", "sorption", "hydrogeology"],
        primary_authority=["US EPA Chlorinated Solvents Technical Reports", "Fennell & Gossett, Environmental Science & Technology, 1998"],
        burden_holder="Environmental engineer managing solvent contamination",
        adversary_position="Chlorinated solvents degrade rapidly and are not persistent",
        counter_arguments=[
            "Field evidence of persistent solvent plumes",
            "Identification of toxic degradation intermediates",
            "Laboratory studies on degradation kinetics"
        ],
        resolution_strategy="Apply integrated remediation and monitoring strategies informed by degradation chemistry.",
        entity_scope="Groundwater and soil environments",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="EPA technical reports and Fennell & Gossett (1998) studies."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Nutrient-Induced Eutrophication",
        keywords=["eutrophication", "nutrients", "phosphorus", "nitrogen", "algal blooms", "environmental chemistry"],
        conclusion_template="Excessive nutrient inputs, particularly phosphorus and nitrogen, drive eutrophication, leading to algal blooms and oxygen depletion.",
        reasoning_framework=(
            "Nutrient enrichment from agricultural runoff, wastewater, and atmospheric deposition increases primary productivity in aquatic systems. "
            "Phosphorus often limits freshwater productivity, while nitrogen limits marine productivity. "
            "Elevated nutrients stimulate algal and cyanobacterial blooms, some producing toxins. "
            "Decomposition of biomass consumes dissolved oxygen, causing hypoxia or anoxia detrimental to aquatic life. "
            "Chemical speciation of nutrients influences bioavailability. "
            "Management includes nutrient load reduction and monitoring. "
            "Modeling eutrophication requires coupling nutrient cycling with biological and physical processes."
        ),
        key_factors=["nutrient concentrations", "limiting nutrient", "algal growth", "oxygen dynamics", "nutrient speciation"],
        primary_authority=["Smith et al., Environmental Science & Technology, 1999", "Carpenter et al., Ecological Applications, 1998"],
        burden_holder="Water resource manager controlling nutrient pollution",
        adversary_position="Eutrophication is unrelated to nutrient inputs",
        counter_arguments=[
            "Empirical correlations between nutrient loads and algal blooms",
            "Experimental nutrient enrichment studies",
            "Observed oxygen depletion linked to biomass decay"
        ],
        resolution_strategy="Implement nutrient management plans and monitor ecosystem responses.",
        entity_scope="Freshwater and coastal marine systems",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Smith et al. (1999) and Carpenter et al. (1998) key studies on eutrophication."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Organophosphorus Pesticides",
        keywords=["organophosphorus pesticides", "environmental chemistry", "degradation", "toxicity", "soil and water contamination"],
        conclusion_template="Organophosphorus pesticides degrade via hydrolysis and microbial activity but pose acute toxicity risks to non-target organisms.",
        reasoning_framework=(
            "Organophosphorus pesticides inhibit acetylcholinesterase, affecting nervous systems of pests and non-target species. "
            "They undergo hydrolysis in water and soil, with rates dependent on pH, temperature, and microbial presence. "
            "Degradation products vary in toxicity and persistence. "
            "Transport occurs via runoff and leaching, leading to contamination of surface and groundwater. "
            "Analytical methods include chromatographic and enzymatic assays. "
            "Risk assessment balances pest control benefits against environmental and health risks."
        ),
        key_factors=["hydrolysis rate", "microbial degradation", "toxicity", "transport pathways", "environmental persistence"],
        primary_authority=["Racke, Reviews of Environmental Contamination and Toxicology, 1993", "US EPA Pesticide Fact Sheets"],
        burden_holder="Environmental toxicologist evaluating pesticide impact",
        adversary_position="Organophosphorus pesticides degrade rapidly and are non-toxic to non-targets",
        counter_arguments=[
            "Documented cases of non-target toxicity",
            "Measured persistence in environmental compartments",
            "Laboratory degradation studies"
        ],
        resolution_strategy="Monitor pesticide residues and promote integrated pest management.",
        entity_scope="Agricultural soils and adjacent water bodies",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Racke (1993) authoritative review on organophosphorus pesticides."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Cyanotoxins in Freshwater Systems",
        keywords=["cyanotoxins", "freshwater", "toxicity", "algal blooms", "environmental chemistry"],
        conclusion_template="Cyanotoxins produced by cyanobacterial blooms pose significant health risks and require monitoring and management in freshwater systems.",
        reasoning_framework=(
            "Cyanobacteria produce toxins such as microcystins, cylindrospermopsin, and anatoxins during bloom events. "
            "Toxin production is influenced by nutrient availability, light, temperature, and species composition. "
            "Cyanotoxins are chemically diverse, stable in water, and can bioaccumulate. "
            "Exposure routes include ingestion, dermal contact, and inhalation. "
            "Analytical detection employs ELISA, LC-MS, and molecular methods. "
            "Management strategies focus on nutrient reduction, bloom control, and public health advisories."
        ),
        key_factors=["nutrient levels", "bloom dynamics", "toxin types", "environmental stability", "exposure pathways"],
        primary_authority=["Chorus & Bartram, Toxic Cyanobacteria in Water, 1999", "WHO Guidelines for Drinking-water Quality"],
        burden_holder="Public health official managing water safety",
        adversary_position="Cyanotoxins are insignificant and do not affect human health",
        counter_arguments=[
            "Documented poisoning incidents",
            "Toxin detection in drinking water sources",
            "Toxicological studies confirming health effects"
        ],
        resolution_strategy="Implement monitoring programs and nutrient management to reduce blooms.",
        entity_scope="Freshwater lakes and reservoirs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Chorus & Bartram (1999) comprehensive cyanotoxin review."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Atmospheric Particulate Matter",
        keywords=["particulate matter", "atmospheric chemistry", "aerosols", "pollution", "health effects"],
        conclusion_template="Atmospheric particulate matter consists of complex chemical mixtures influencing air quality and human health.",
        reasoning_framework=(
            "Particulate matter (PM) includes solid and liquid particles suspended in air, originating from combustion, industrial processes, and natural sources. "
            "Chemical composition includes sulfates, nitrates, organic compounds, metals, and elemental carbon. "
            "PM size fractions (PM10, PM2.5) determine respiratory deposition and health impacts. "
            "Secondary aerosol formation occurs via gas-to-particle conversion involving sulfur and nitrogen oxides. "
            "Atmospheric reactions and meteorology influence PM concentration and composition. "
            "Monitoring employs gravimetric, optical, and chemical analysis. "
            "Regulatory standards aim to reduce PM exposure and associated health risks."
        ),
        key_factors=["source emissions", "chemical composition", "particle size", "secondary formation", "meteorology"],
        primary_authority=["Seinfeld & Pandis, Atmospheric Chemistry and Physics, 2016", "WHO Air Quality Guidelines"],
        burden_holder="Air quality manager assessing particulate pollution",
        adversary_position="Particulate matter is chemically inert and harmless",
        counter_arguments=[
            "Epidemiological studies linking PM exposure to health outcomes",
            "Chemical analyses showing toxic components",
            "Regulatory actions based on scientific evidence"
        ],
        resolution_strategy="Implement emission controls and continuous monitoring.",
        entity_scope="Urban and regional atmospheres",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Seinfeld & Pandis (2016) authoritative atmospheric chemistry text."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Fluoride in Drinking Water",
        keywords=["fluoride", "drinking water", "environmental chemistry", "health effects", "water treatment"],
        conclusion_template="Fluoride concentrations in drinking water influence dental health, requiring careful management to avoid deficiency or toxicity.",
        reasoning_framework=(
            "Fluoride occurs naturally in groundwater through mineral dissolution and anthropogenic sources. "
            "Optimal fluoride levels prevent dental caries, but excessive concentrations cause fluorosis. "
            "Fluoride speciation depends on pH and ionic strength, affecting bioavailability. "
            "Water treatment methods include adsorption, precipitation, and membrane filtration to adjust fluoride levels. "
            "Monitoring ensures compliance with health guidelines. "
            "Environmental factors such as geology and land use influence fluoride distribution."
        ),
        key_factors=["fluoride concentration", "speciation", "water chemistry", "health guidelines", "treatment methods"],
        primary_authority=["WHO Guidelines for Drinking-water Quality", "Fawell et al., Fluoride in Drinking-water, 2006"],
        burden_holder="Water quality manager ensuring safe fluoride levels",
        adversary_position="Fluoride has no health impact and requires no regulation",
        counter_arguments=[
            "Epidemiological evidence of dental health effects",
            "Toxicological data on fluorosis",
            "Regulatory standards worldwide"
        ],
        resolution_strategy="Monitor fluoride and apply treatment to maintain optimal concentrations.",
        entity_scope="Drinking water supplies",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="WHO (2006) authoritative guidelines on fluoride."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Nitrate Reduction in Soils",
        keywords=["nitrate reduction", "soil chemistry", "denitrification", "microbial processes", "environmental chemistry"],
        conclusion_template="Nitrate reduction in soils occurs primarily via microbial denitrification, influencing nitrogen availability and greenhouse gas emissions.",
        reasoning_framework=(
            "Denitrification is an anaerobic microbial process reducing nitrate to nitrogen gases (N2, N2O), removing bioavailable nitrogen from soils. "
            "It occurs in microsites with low oxygen and sufficient organic carbon. "
            "Environmental factors such as moisture, temperature, and pH affect rates. "
            "Denitrification contributes to nitrogen loss from agricultural soils and emissions of N2O, a potent greenhouse gas. "
            "Measurement techniques include gas flux monitoring and isotopic tracing. "
            "Management practices aim to optimize nitrogen use efficiency and minimize emissions."
        ),
        key_factors=["soil oxygen levels", "organic carbon", "nitrate availability", "microbial community", "environmental conditions"],
        primary_authority=["Firestone & Davidson, Microbiological Reviews, 1989", "Robertson & Groffman, Nitrogen in Agricultural Soils, 2007"],
        burden_holder="Soil scientist managing nitrogen cycling",
        adversary_position="Nitrate reduction in soils is abiotic and insignificant",
        counter_arguments=[
            "Demonstrated microbial denitrification activity",
            "Gas emission measurements confirming process",
            "Isotopic evidence of biological nitrate reduction"
        ],
        resolution_strategy="Incorporate denitrification in nitrogen management and greenhouse gas mitigation strategies.",
        entity_scope="Agricultural and natural soils",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Firestone & Davidson (1989) foundational review on denitrification."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Selenium Speciation and Toxicity",
        keywords=["selenium", "speciation", "toxicity", "environmental chemistry", "bioavailability"],
        conclusion_template="Selenium speciation governs its bioavailability and toxicity in the environment, with inorganic and organic forms exhibiting different behaviors.",
        reasoning_framework=(
            "Selenium occurs in multiple oxidation states (Se(-II), Se(0), Se(IV), Se(VI)) with varying solubility and bioavailability. "
            "Selenate (Se(VI)) and selenite (Se(IV)) are common aqueous species, with selenite generally more bioavailable and toxic. "
            "Organic selenium compounds such as selenomethionine bioaccumulate in organisms. "
            "Environmental factors including redox conditions, pH, and microbial activity influence speciation. "
            "Toxicity thresholds vary by species and form. "
            "Analytical speciation techniques include HPLC-ICP-MS. "
            "Management involves controlling selenium inputs and monitoring speciation."
        ),
        key_factors=["selenium oxidation state", "redox conditions", "pH", "microbial transformations", "speciation analysis"],
        primary_authority=["Lenz & Lens, Environmental Science & Technology, 2009", "USGS Selenium Reports"],
        burden_holder="Environmental chemist assessing selenium contamination",
        adversary_position="Total selenium concentration suffices for risk assessment without speciation",
        counter_arguments=[
            "Speciation-dependent toxicity observed in laboratory and field studies",
            "Environmental transformations altering selenium forms",
            "Speciation analysis informing remediation"
        ],
        resolution_strategy="Incorporate speciation data in environmental risk assessments.",
        entity_scope="Aquatic and terrestrial environments",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Lenz & Lens (2009) comprehensive selenium speciation review."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Oil Spill Weathering",
        keywords=["oil spill", "weathering", "environmental chemistry", "biodegradation", "photolysis", "evaporation"],
        conclusion_template="Oil spill weathering involves physical and chemical processes including evaporation, dissolution, photolysis, and biodegradation, altering pollutant composition and toxicity.",
        reasoning_framework=(
            "Following an oil spill, weathering processes modify the chemical composition and environmental behavior of hydrocarbons. "
            "Evaporation removes volatile components, while dissolution transfers soluble fractions to water. "
            "Photolysis degrades surface oil under sunlight. "
            "Microbial biodegradation metabolizes hydrocarbons, with rates influenced by nutrient availability and environmental conditions. "
            "Weathering alters toxicity and persistence, affecting cleanup strategies. "
            "Monitoring involves chemical fingerprinting and toxicity assays. "
            "Modeling weathering supports impact assessment and response planning."
        ),
        key_factors=["temperature", "sunlight", "microbial activity", "oil composition", "environmental conditions"],
        primary_authority=["Fingas, Oil Spill Science and Technology, 2016", "Atlas & Hazen, Science, 2011"],
        burden_holder="Environmental response coordinator managing oil spills",
        adversary_position="Oil composition remains unchanged after spill",
        counter_arguments=[
            "Chemical analyses showing compositional changes over time",
            "Observed biodegradation and photolysis products",
            "Field studies documenting weathering effects"
        ],
        resolution_strategy="Incorporate weathering processes in spill response and remediation planning.",
        entity_scope="Marine and freshwater spill sites",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Fingas (2016) authoritative text on oil spill chemistry."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Chlorine Disinfection Byproducts",
        keywords=["chlorine disinfection", "byproducts", "trihalomethanes", "haloacetic acids", "water treatment", "environmental chemistry"],
        conclusion_template="Chlorine disinfection of water produces byproducts such as trihalomethanes and haloacetic acids, which have health and environmental concerns.",
        reasoning_framework=(
            "Chlorination reacts with natural organic matter (NOM) in water to form disinfection byproducts (DBPs) including trihalomethanes (THMs) and haloacetic acids (HAAs). "
            "DBP formation depends on chlorine dose, contact time, water pH, temperature, and NOM characteristics. "
            "Many DBPs are regulated due to carcinogenic and toxic effects. "
            "Alternative disinfection methods and precursor removal reduce DBP formation. "
            "Monitoring employs chromatographic and spectroscopic techniques. "
            "Risk assessment balances microbial control benefits against DBP risks."
        ),
        key_factors=["chlorine dose", "NOM concentration", "pH", "temperature", "contact time"],
        primary_authority=["Richardson et al., Environmental Science & Technology, 2007", "WHO Guidelines for Drinking-water Quality"],
        burden_holder="Water treatment engineer managing disinfection",
        adversary_position="DBPs are insignificant and do not require control",
        counter_arguments=[
            "Epidemiological studies linking DBPs to health effects",
            "Measured DBP concentrations in treated water",
            "Regulatory limits and guidelines"
        ],
        resolution_strategy="Optimize disinfection and precursor removal to minimize DBPs.",
        entity_scope="Drinking water treatment systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Richardson et al. (2007) comprehensive DBP review."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Perchlorate Contamination",
        keywords=["perchlorate", "contamination", "environmental chemistry", "groundwater", "toxicity"],
        conclusion_template="Perchlorate contamination in groundwater poses risks to thyroid function and requires monitoring and remediation.",
        reasoning_framework=(
            "Perchlorate (ClO4-) is a persistent anion used in rocket propellants and explosives. "
            "It is highly soluble and mobile in groundwater, resistant to biodegradation under aerobic conditions. "
            "Perchlorate inhibits iodide uptake in the thyroid gland, affecting hormone synthesis. "
            "Remediation includes bioreactors promoting anaerobic reduction and ion exchange. "
            "Analytical detection uses ion chromatography with mass spectrometry. "
            "Regulatory standards guide safe exposure levels."
        ),
        key_factors=["solubility", "mobility", "biodegradability", "toxicity", "remediation methods"],
        primary_authority=["US EPA Perchlorate Drinking Water Advisory", "Coates & Achenbach, Environmental Science & Technology, 2004"],
        burden_holder="Environmental chemist managing groundwater quality",
        adversary_position="Perchlorate is harmless and does not require control",
        counter_arguments=[
            "Toxicological studies demonstrating thyroid effects",
            "Detection of perchlorate in drinking water sources",
            "Successful remediation case studies"
        ],
        resolution_strategy="Implement monitoring and apply effective remediation technologies.",
        entity_scope="Groundwater and drinking water systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="US EPA advisory and Coates & Achenbach (2004) studies."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Phthalates as Endocrine Disruptors",
        keywords=["phthalates", "endocrine disruptors", "environmental chemistry", "toxicity", "plasticizers"],
        conclusion_template="Phthalates leach from plastics into the environment and act as endocrine disruptors affecting wildlife and human health.",
        reasoning_framework=(
            "Phthalates are esters of phthalic acid used as plasticizers in PVC and other polymers. "
            "They are not covalently bound and can leach into water, soil, and air. "
            "Phthalates exhibit endocrine-disrupting properties, interfering with hormone systems. "
            "Environmental degradation occurs via hydrolysis and microbial metabolism but can be slow. "
            "Exposure occurs through ingestion, inhalation, and dermal contact. "
            "Analytical detection uses GC-MS and LC-MS. "
            "Regulatory agencies assess risks and restrict certain phthalates."
        ),
        key_factors=["leaching rates", "environmental persistence", "endocrine activity", "exposure pathways", "degradation"],
        primary_authority=["Wittassek & Angerer, Environmental Health Perspectives, 2008", "US EPA Phthalate Assessments"],
        burden_holder="Environmental health scientist assessing chemical risks",
        adversary_position="Phthalates are inert and non-toxic",
        counter_arguments=[
            "Epidemiological and toxicological evidence of endocrine disruption",
            "Environmental detection of phthalates",
            "Regulatory restrictions based on scientific data"
        ],
        resolution_strategy="Monitor environmental levels and reduce phthalate use.",
        entity_scope="Environmental media and human exposure",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Wittassek & Angerer (2008) review on phthalates."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Radon in Groundwater",
        keywords=["radon", "groundwater", "radioactivity", "environmental chemistry", "health risk"],
        conclusion_template="Radon dissolved in groundwater poses inhalation and ingestion risks, requiring monitoring and mitigation.",
        reasoning_framework=(
            "Radon-222 is a radioactive noble gas produced by decay of uranium in rocks and soils. "
            "It dissolves in groundwater and can be released into indoor air during water use. "
            "Radon decay emits alpha particles, posing lung cancer risks. "
            "Concentration depends on geology, water chemistry, and residence time. "
            "Mitigation includes aeration and activated carbon filtration. "
            "Measurement employs liquid scintillation and alpha spectrometry."
        ),
        key_factors=["uranium content", "water residence time", "radon solubility", "decay rate", "exposure pathways"],
        primary_authority=["US EPA Radon in Drinking Water Guide", "NRC Radon Report, 1999"],
        burden_holder="Water quality manager ensuring safety",
        adversary_position="Radon in water is negligible and poses no health risk",
        counter_arguments=[
            "Epidemiological studies linking radon exposure to cancer",
            "Measured radon levels in groundwater and indoor air",
            "Regulatory guidelines and mitigation success"
        ],
        resolution_strategy="Monitor radon and apply treatment as needed.",
        entity_scope="Groundwater and indoor environments",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="US EPA and NRC authoritative radon assessments."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Heavy Metal Toxicity Mechanisms",
        keywords=["heavy metals", "toxicity", "environmental chemistry", "bioavailability", "mechanisms"],
        conclusion_template="Heavy metal toxicity arises from bioavailable metal species interacting with biological molecules, disrupting cellular functions.",
        reasoning_framework=(
            "Heavy metals such as lead, mercury, cadmium, and arsenic exert toxicity through binding to proteins, enzymes, and nucleic acids. "
            "Speciation determines bioavailability and cellular uptake. "
            "Mechanisms include oxidative stress induction, enzyme inhibition, and interference with nutrient metabolism. "
            "Toxicity thresholds vary by species and exposure route. "
            "Environmental chemistry influences metal speciation and thus toxicity. "
            "Understanding mechanisms informs risk assessment and remediation."
        ),
        key_factors=["metal speciation", "bioavailability", "cellular targets", "oxidative stress", "exposure pathways"],
        primary_authority=["WHO Environmental Health Criteria", "ATSDR Toxicological Profiles"],
        burden_holder="Toxicologist assessing heavy metal risks",
        adversary_position="All heavy metals have uniform toxicity regardless of speciation",
        counter_arguments=[
            "Speciation-dependent toxicity observed in studies",
            "Differential uptake and effects linked to chemical forms",
            "Environmental transformations altering toxicity"
        ],
        resolution_strategy="Incorporate speciation and mechanistic data in toxicity assessments.",
        entity_scope="Environmental and biological systems",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="WHO and ATSDR authoritative toxicology documents."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Phosphorus Speciation in Soils",
        keywords=["phosphorus", "speciation", "soils", "environmental chemistry", "bioavailability"],
        conclusion_template="Phosphorus speciation in soils determines its bioavailability and mobility, influencing nutrient cycling and eutrophication potential.",
        reasoning_framework=(
            "Phosphorus exists in soils as organic and inorganic species, including orthophosphate, polyphosphates, and mineral-bound forms. "
            "Speciation affects solubility and plant uptake. "
            "Soil pH, mineralogy, and microbial activity influence phosphorus transformations. "
            "Adsorption onto iron and aluminum oxides reduces availability. "
            "Sequential extraction and spectroscopic methods characterize speciation. "
            "Management practices aim to optimize phosphorus use and minimize environmental impacts."
        ),
        key_factors=["phosphorus forms", "soil pH", "mineral interactions", "microbial activity", "adsorption"],
        primary_authority=["Sims & Sharpley, Phosphorus Chemistry in Soils, 2005", "Sharpley et al., Journal of Environmental Quality, 1994"],
        burden_holder="Soil scientist managing nutrient availability",
        adversary_position="Total phosphorus concentration suffices without speciation knowledge",
        counter_arguments=[
            "Speciation controls phosphorus bioavailability",
            "Environmental impacts linked to specific phosphorus forms",
            "Management effectiveness depends on speciation understanding"
        ],
        resolution_strategy="Incorporate phosphorus speciation in soil fertility and environmental assessments.",
        entity_scope="Agricultural and natural soils",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Sims & Sharpley (2005) authoritative phosphorus chemistry text."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Hydrogen Sulfide in Aquatic Systems",
        keywords=["hydrogen sulfide", "aquatic systems", "environmental chemistry", "toxicity", "redox"],
        conclusion_template="Hydrogen sulfide forms under anoxic conditions in aquatic systems and poses toxicity risks to biota and humans.",
        reasoning_framework=(
            "Hydrogen sulfide (H2S) is produced by sulfate-reducing bacteria in anoxic sediments and waters. "
            "It exists as dissolved gas and bisulfide ions depending on pH. "
            "H2S is toxic to aquatic organisms and humans, interfering with cellular respiration. "
            "It contributes to corrosion and odor problems. "
            "Concentrations depend on sulfate availability, organic matter, and redox conditions. "
            "Monitoring employs electrochemical and colorimetric methods. "
            "Management includes aeration and sulfate input control."
        ),
        key_factors=["sulfate reduction", "redox potential", "pH", "organic matter", "toxicity"],
        primary_authority=["Stumm & Morgan, Aquatic Chemistry, 3rd Ed., 1996", "EPA Water Quality Criteria"],
        burden_holder="Water quality manager addressing sulfide issues",
        adversary_position="Hydrogen sulfide is insignificant in aquatic toxicity",
        counter_arguments=[
            "Documented toxicity thresholds",
            "Measured H2S concentrations in impacted waters",
            "Corrosion and odor evidence"
        ],
        resolution_strategy="Monitor and manage sulfate inputs and redox conditions.",
        entity_scope="Anoxic aquatic environments",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Stumm & Morgan (1996) aquatic chemistry framework."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Nitrate Leaching from Agricultural Soils",
        keywords=["nitrate leaching", "agriculture", "soil chemistry", "environmental chemistry", "groundwater contamination"],
        conclusion_template="Nitrate leaching from agricultural soils contaminates groundwater, driven by nitrogen application rates, soil properties, and hydrology.",
        reasoning_framework=(
            "Excess nitrogen fertilizers not taken up by crops leach as nitrate through soil profiles into groundwater. "
            "Soil texture, organic matter, and microbial activity influence nitrate retention and transformation. "
            "Hydrological factors such as precipitation and irrigation affect leaching rates. "
            "Nitrate contamination poses human health risks and contributes to eutrophication. "
            "Management includes optimized fertilizer application, cover cropping, and buffer zones. "
            "Monitoring groundwater nitrate levels informs management effectiveness."
        ),
        key_factors=["fertilizer application", "soil properties", "microbial activity", "hydrology", "crop uptake"],
        primary_authority=["Keeney & Hatfield, Nitrogen in the Environment, 1998", "USDA Agricultural Reports"],
        burden_holder="Agronomist managing nutrient applications",
        adversary_position="Nitrate leaching is negligible regardless of fertilizer use",
        counter_arguments=[
            "Groundwater nitrate monitoring data",
            "Modeling of nitrogen balance and leaching",
            "Field studies linking fertilizer rates to contamination"
        ],
        resolution_strategy="Implement best management practices and monitor groundwater quality.",
        entity_scope="Agricultural soils and groundwater",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Keeney & Hatfield (1998) nitrogen environmental impact studies."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Lead in Urban Soils",
        keywords=["lead", "urban soils", "environmental chemistry", "contamination", "bioavailability"],
        conclusion_template="Lead contamination in urban soils arises from historical emissions and affects bioavailability and human exposure risks.",
        reasoning_framework=(
            "Lead accumulates in urban soils from sources such as leaded gasoline, paint, and industrial emissions. "
            "Soil properties including pH, organic matter, and mineralogy influence lead speciation and bioavailability. "
            "Lead binds strongly to soil particles but can be mobilized under acidic conditions. "
            "Exposure occurs via ingestion and inhalation of dust. "
            "Remediation includes soil removal, stabilization, and phytoremediation. "
            "Monitoring employs total and bioavailable lead measurements."
        ),
        key_factors=["source history", "soil chemistry", "speciation", "bioavailability", "exposure pathways"],
        primary_authority=["US EPA Lead in Soil Guidance", "Alloway, Heavy Metals in Soils, 2013"],
        burden_holder="Environmental health professional managing urban contamination",
        adversary_position="Lead in soils is immobile and non-toxic",
        counter_arguments=[
            "Epidemiological evidence of lead poisoning",
            "Soil chemistry studies showing variable bioavailability",
            "Remediation effectiveness data"
        ],
        resolution_strategy="Monitor and remediate urban soils to reduce exposure.",
        entity_scope="Urban and industrial soils",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="US EPA and Alloway (2013) authoritative sources."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Arsenic Speciation and Mobility",
        keywords=["arsenic", "speciation", "mobility", "environmental chemistry", "toxicity"],
        conclusion_template="Arsenic speciation controls its mobility and toxicity in the environment, with redox conditions playing a key role.",
        reasoning_framework=(
            "Arsenic exists mainly as arsenate (As(V)) and arsenite (As(III)) species in natural waters. "
            "Arsenite is more toxic and mobile under reducing conditions, while arsenate dominates in oxidizing environments. "
            "Speciation affects adsorption to minerals and bioavailability. "
            "Microbial transformations influence arsenic cycling. "
            "Analytical speciation methods include HPLC-ICP-MS. "
            "Management includes source control and treatment technologies."
        ),
        key_factors=["redox conditions", "speciation", "mineral interactions", "microbial activity", "toxicity"],
        primary_authority=["Smedley & Kinniburgh, Applied Geochemistry, 2002", "USGS Arsenic Reports"],
        burden_holder="Environmental chemist assessing arsenic contamination",
        adversary_position="Total arsenic concentration suffices without speciation",
        counter_arguments=[
            "Speciation-dependent mobility and toxicity documented",
            "Environmental transformations altering arsenic forms",
            "Speciation-informed remediation strategies"
        ],
        resolution_strategy="Include speciation analysis in arsenic risk assessments.",
        entity_scope="Groundwater and soils",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Smedley & Kinniburgh (2002) arsenic speciation review."
    ),
    DoctrineBlock(
        topic="Environmental Chemistry of Chlorinated Phenols",
        keywords=["chlorinated phenols", "environmental chemistry", "toxicity", "degradation", "contamination"],
        conclusion_template="Chlorinated phenols are toxic environmental contaminants subject to degradation via photolysis and biodegradation.",
        reasoning_framework=(
            "Chlorinated phenols are used in pesticides and wood preservatives. "
            "They exhibit toxicity to aquatic organisms and humans. "
            "Degradation occurs via photolysis under sunlight and microbial metabolism under aerobic and anaerobic conditions. "
            "Transport occurs via water and air pathways. "
            "Analytical detection uses chromatographic methods. "
            "Risk assessment integrates exposure and degradation data."
        ),
        key_factors=["chemical structure", "photolysis rates", "microbial degradation", "toxicity", "transport"],
        primary_authority=["EPA Chlorinated Phenols Reports", "ATSDR Toxicological Profiles"],
        burden_holder="Environmental chemist evaluating contamination",
        adversary_position="Chlorinated phenols degrade rapidly and are non-toxic",
        counter_arguments=[
            "