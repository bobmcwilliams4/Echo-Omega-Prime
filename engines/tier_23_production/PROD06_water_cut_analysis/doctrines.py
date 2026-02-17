from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

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
        topic="Water Cut Definition and Calculation",
        keywords=["water cut", "produced fluids", "oil production", "measurement"],
        conclusion_template="Water cut is calculated as the ratio of water produced to total liquid produced, expressed as a percentage.",
        reasoning_framework=(
            "Water cut is a fundamental metric in oil production operations, representing the proportion of water in the produced fluids. "
            "The calculation is performed by dividing the volume of water produced by the total volume of liquids (oil + water) produced, then multiplying by 100 to obtain a percentage. "
            "Accurate measurement requires reliable sampling and separation techniques. Water cut trends are used to assess reservoir performance, waterflood effectiveness, and potential water breakthrough. "
            "The doctrine relies on industry standards such as API RP 13B-1 and SPE technical papers. "
            "Measurement errors may arise from emulsion formation, incomplete separation, or sampling bias. "
            "Operators must ensure calibration of measurement devices and periodic validation against laboratory methods."
        ),
        key_factors=["Sampling accuracy", "Separation efficiency", "Measurement device calibration", "Fluid properties", "Emulsion presence"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Water cut measurements are often inaccurate due to sampling bias and device limitations.",
        counter_arguments=[
            "Regular calibration and validation against laboratory methods mitigate measurement errors.",
            "Industry standards prescribe best practices for sampling and measurement."
        ],
        resolution_strategy="Implement periodic device calibration, cross-check with laboratory analysis, and adhere to API and ISO standards.",
        entity_scope="Oil production operations",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 4"
    ),
    DoctrineBlock(
        topic="BSW Measurement Techniques - Centrifuge Method",
        keywords=["BSW", "basic sediment and water", "centrifuge", "measurement", "laboratory"],
        conclusion_template="The centrifuge method is a standard laboratory technique for determining BSW in produced fluids.",
        reasoning_framework=(
            "The centrifuge method involves placing a sample of produced fluid in a calibrated centrifuge tube and spinning it at a specified speed and duration. "
            "This process separates water and sediment from oil, allowing visual determination of BSW volume. "
            "The method is governed by API standards and is widely used for custody transfer and quality control. "
            "Accuracy depends on sample handling, centrifuge calibration, and operator skill. "
            "Limitations include emulsion stability and inability to distinguish dissolved water. "
            "Results are typically reported as a percentage of BSW in the total sample volume."
        ),
        key_factors=["Sample integrity", "Centrifuge calibration", "Spin speed and duration", "Emulsion stability", "Tube graduation accuracy"],
        primary_authority=["API MPMS Chapter 10.4", "ISO 3734"],
        burden_holder="Laboratory technician",
        adversary_position="Centrifuge method underestimates BSW in emulsified samples.",
        counter_arguments=[
            "Emulsion-breaking agents can be used to improve separation.",
            "Alternative methods (e.g., Karl Fischer titration) can cross-validate results."
        ],
        resolution_strategy="Use emulsion breakers, validate with alternative methods, and follow API procedures.",
        entity_scope="Laboratory measurement",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API MPMS Chapter 10.4"
    ),
    DoctrineBlock(
        topic="Karl Fischer Titration for Water Content",
        keywords=["Karl Fischer", "titration", "water content", "chemical analysis", "accuracy"],
        conclusion_template="Karl Fischer titration provides precise quantification of water content in oil samples.",
        reasoning_framework=(
            "Karl Fischer titration is a chemical method for determining water content in oil and petroleum products. "
            "The technique involves reacting water in the sample with iodine and sulfur dioxide in the presence of a base, with endpoint detection via electrometric or colorimetric methods. "
            "It is highly sensitive and can detect water levels down to ppm. "
            "The method is suitable for custody transfer, quality control, and laboratory validation of field measurements. "
            "Sample preparation and handling are critical to avoid contamination or evaporation. "
            "Results are reported as mass or volume percentage."
        ),
        key_factors=["Sample preparation", "Reagent purity", "Instrument calibration", "Operator skill", "Detection sensitivity"],
        primary_authority=["ASTM D6304", "ISO 760"],
        burden_holder="Laboratory analyst",
        adversary_position="Karl Fischer titration is too complex and costly for routine field measurements.",
        counter_arguments=[
            "Field-adapted Karl Fischer kits are available for rapid testing.",
            "Laboratory validation is essential for high-value custody transfer."
        ],
        resolution_strategy="Use field kits for routine checks and laboratory titration for critical measurements.",
        entity_scope="Laboratory and field analysis",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASTM D6304 Section 7"
    ),
    DoctrineBlock(
        topic="Waterflood Performance - Buckley-Leverett Theory",
        keywords=["waterflood", "Buckley-Leverett", "displacement", "fractional flow", "reservoir engineering"],
        conclusion_template="Buckley-Leverett theory models waterflood displacement and predicts water breakthrough and recovery efficiency.",
        reasoning_framework=(
            "Buckley-Leverett theory provides a mathematical framework for analyzing immiscible displacement in porous media. "
            "The theory uses fractional flow equations and material balance to predict the advance of the water front, breakthrough time, and ultimate recovery. "
            "Key assumptions include homogeneous reservoir, constant injection rate, and negligible capillary pressure. "
            "The theory is foundational for waterflood design and performance evaluation. "
            "Limitations arise in heterogeneous reservoirs, presence of channels, and variable permeability. "
            "Modern applications incorporate numerical simulation and history matching."
        ),
        key_factors=["Reservoir homogeneity", "Injection rate", "Relative permeability curves", "Fractional flow", "Capillary pressure"],
        primary_authority=["SPE 942", "Buckley-Leverett (1942)", "Lake, Enhanced Oil Recovery"],
        burden_holder="Reservoir engineer",
        adversary_position="Buckley-Leverett theory oversimplifies real reservoir conditions and ignores heterogeneity.",
        counter_arguments=[
            "Theory provides a baseline for performance; numerical simulation accounts for heterogeneity.",
            "History matching adjusts model predictions to observed data."
        ],
        resolution_strategy="Combine Buckley-Leverett analysis with numerical simulation and field data calibration.",
        entity_scope="Reservoir engineering and waterflood management",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Buckley-Leverett (1942) SPE 942"
    ),
    DoctrineBlock(
        topic="Water Breakthrough Prediction - Channel and Frontal Advance",
        keywords=["water breakthrough", "channel advance", "frontal advance", "prediction", "reservoir"],
        conclusion_template="Water breakthrough is predicted using channel and frontal advance models, considering reservoir heterogeneity and injection patterns.",
        reasoning_framework=(
            "Water breakthrough occurs when injected water reaches production wells, leading to increased water cut. "
            "Prediction models include channel advance (preferential flow through high-permeability zones) and frontal advance (uniform displacement). "
            "Reservoir heterogeneity, injection rate, and well spacing influence breakthrough timing. "
            "Diagnostic plots and tracer tests help identify breakthrough mechanisms. "
            "Early breakthrough is often caused by channeling or poor sweep efficiency. "
            "Mitigation strategies include selective injection, pattern balancing, and conformance treatments."
        ),
        key_factors=["Reservoir heterogeneity", "Injection pattern", "Well spacing", "Tracer test results", "Sweep efficiency"],
        primary_authority=["SPE 169934", "Lake, Enhanced Oil Recovery", "API RP 13B-1"],
        burden_holder="Reservoir engineer",
        adversary_position="Breakthrough prediction models are unreliable in highly heterogeneous reservoirs.",
        counter_arguments=[
            "Diagnostic plots and tracer tests improve model reliability.",
            "Pattern balancing and conformance treatments address heterogeneity."
        ],
        resolution_strategy="Integrate diagnostic data and adjust injection patterns to mitigate early breakthrough.",
        entity_scope="Reservoir management",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 169934 Section 5"
    ),
    DoctrineBlock(
        topic="Chan Diagnostic Plots for Water Production Analysis",
        keywords=["Chan plots", "diagnostic", "water production", "analysis", "reservoir"],
        conclusion_template="Chan diagnostic plots are used to analyze water production trends and identify breakthrough mechanisms.",
        reasoning_framework=(
            "Chan diagnostic plots graph water cut versus cumulative oil production or time, revealing patterns indicative of breakthrough, coning, or channeling. "
            "The plots help distinguish between frontal advance, channeling, and coning mechanisms. "
            "Slope changes and inflection points indicate breakthrough events. "
            "Plots are used to optimize waterflood operations and design conformance treatments. "
            "Limitations include data quality and interpretation subjectivity."
        ),
        key_factors=["Water cut trend", "Cumulative oil production", "Slope analysis", "Breakthrough identification", "Data quality"],
        primary_authority=["Chan (1995)", "SPE 169934", "Lake, Enhanced Oil Recovery"],
        burden_holder="Production engineer",
        adversary_position="Chan plots are subjective and depend on data quality.",
        counter_arguments=[
            "Combining plots with tracer tests and simulation improves reliability.",
            "Standardized interpretation guidelines reduce subjectivity."
        ],
        resolution_strategy="Use Chan plots with supporting diagnostic tools and adhere to interpretation standards.",
        entity_scope="Production analysis",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Chan (1995) SPE 169934"
    ),
    DoctrineBlock(
        topic="Water Coning in Vertical Wells",
        keywords=["water coning", "vertical wells", "production", "reservoir", "breakthrough"],
        conclusion_template="Water coning is managed by controlling production rates and optimizing well completions.",
        reasoning_framework=(
            "Water coning occurs when water moves upward from the aquifer into the wellbore due to high production rates. "
            "The phenomenon is modeled using critical rate equations and coning theory. "
            "Mitigation involves reducing production rates below the critical threshold, installing packers, and optimizing perforation intervals. "
            "Reservoir properties such as permeability, thickness, and water-oil contact depth influence coning risk. "
            "Numerical simulation is used for coning prediction and management."
        ),
        key_factors=["Production rate", "Reservoir permeability", "Well completion", "Water-oil contact", "Simulation results"],
        primary_authority=["SPE 169934", "API RP 13B-1", "Lake, Enhanced Oil Recovery"],
        burden_holder="Production engineer",
        adversary_position="Reducing production rate is economically undesirable.",
        counter_arguments=[
            "Optimized completions and selective perforation reduce coning risk without major rate reduction.",
            "Simulation allows for balancing production and coning control."
        ],
        resolution_strategy="Optimize completions and use simulation to determine safe production rates.",
        entity_scope="Vertical well operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 169934 Section 7"
    ),
    DoctrineBlock(
        topic="Produced Water Handling and Treatment",
        keywords=["produced water", "handling", "treatment", "disposal", "regulations"],
        conclusion_template="Produced water must be handled and treated according to regulatory standards before disposal or reuse.",
        reasoning_framework=(
            "Produced water contains oil, solids, chemicals, and dissolved salts. "
            "Treatment processes include separation, filtration, chemical dosing, and biological treatment. "
            "Regulatory standards (EPA, UIC Class II) require removal of oil and contaminants before disposal or injection. "
            "Operators must monitor water quality and maintain treatment systems. "
            "Reuse options include reinjection for waterflood, agricultural use, or industrial applications. "
            "Non-compliance results in penalties and environmental risk."
        ),
        key_factors=["Water quality", "Treatment process", "Regulatory compliance", "Monitoring", "Disposal method"],
        primary_authority=["EPA UIC Class II", "API RP 13B-1", "ISO 14001"],
        burden_holder="Operator",
        adversary_position="Produced water treatment is costly and may not meet all regulatory requirements.",
        counter_arguments=[
            "Advanced treatment technologies improve efficiency and compliance.",
            "Reuse reduces disposal volumes and environmental impact."
        ],
        resolution_strategy="Adopt advanced treatment, monitor compliance, and explore reuse options.",
        entity_scope="Produced water management",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA UIC Class II Section 3"
    ),
    DoctrineBlock(
        topic="Injection Water Quality Requirements",
        keywords=["injection water", "quality", "requirements", "waterflood", "reservoir"],
        conclusion_template="Injection water must meet quality standards to prevent reservoir damage and maintain injectivity.",
        reasoning_framework=(
            "Injection water quality is critical for waterflood operations. "
            "Standards require low suspended solids, minimal oil content, and absence of bacteria and scale-forming ions. "
            "Poor quality water causes plugging, souring, and reduced injectivity. "
            "Treatment includes filtration, de-oiling, biocide dosing, and scale inhibitor addition. "
            "Continuous monitoring ensures compliance and reservoir protection."
        ),
        key_factors=["Suspended solids", "Oil content", "Bacteria", "Scale-forming ions", "Monitoring"],
        primary_authority=["API RP 13B-1", "ISO 14001", "SPE 169934"],
        burden_holder="Operator",
        adversary_position="Injection water quality standards are difficult to achieve in remote operations.",
        counter_arguments=[
            "Mobile treatment units and real-time monitoring improve compliance.",
            "Remote operations can use modular treatment systems."
        ],
        resolution_strategy="Deploy mobile treatment and monitoring systems to ensure quality.",
        entity_scope="Waterflood operations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 8"
    ),
    DoctrineBlock(
        topic="Water-Oil Ratio (WOR) Decline Analysis",
        keywords=["WOR", "water-oil ratio", "decline analysis", "production", "trend"],
        conclusion_template="WOR decline analysis is used to forecast water production and identify breakthrough events.",
        reasoning_framework=(
            "Water-oil ratio (WOR) is the ratio of water produced to oil produced. "
            "Decline analysis involves plotting WOR versus time or cumulative production to identify trends and forecast future water production. "
            "Sudden increases in WOR indicate breakthrough or channeling. "
            "Analysis supports production optimization and conformance treatment design. "
            "Limitations include data variability and interpretation subjectivity."
        ),
        key_factors=["WOR trend", "Production data", "Breakthrough identification", "Forecasting", "Data quality"],
        primary_authority=["SPE 169934", "API RP 13B-1", "Lake, Enhanced Oil Recovery"],
        burden_holder="Production engineer",
        adversary_position="WOR analysis is unreliable due to fluctuating production rates.",
        counter_arguments=[
            "Data smoothing and statistical analysis improve reliability.",
            "Combine WOR analysis with diagnostic plots for robust interpretation."
        ],
        resolution_strategy="Apply statistical smoothing and use supporting diagnostics.",
        entity_scope="Production analysis",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 169934 Section 9"
    ),
    DoctrineBlock(
        topic="Relative Permeability and Fractional Flow",
        keywords=["relative permeability", "fractional flow", "reservoir", "waterflood", "modeling"],
        conclusion_template="Relative permeability curves and fractional flow equations are essential for modeling waterflood displacement.",
        reasoning_framework=(
            "Relative permeability describes the ability of each fluid phase to flow in the presence of others. "
            "Fractional flow equations relate water and oil flow rates to reservoir saturation and permeability. "
            "Laboratory core analysis and history matching are used to derive curves. "
            "Models are used for waterflood design, breakthrough prediction, and recovery estimation. "
            "Limitations include core sample representativeness and scale-up challenges."
        ),
        key_factors=["Core analysis", "Fractional flow", "Reservoir saturation", "History matching", "Model calibration"],
        primary_authority=["SPE 942", "Lake, Enhanced Oil Recovery", "API RP 13B-1"],
        burden_holder="Reservoir engineer",
        adversary_position="Relative permeability curves from core samples may not represent field conditions.",
        counter_arguments=[
            "History matching and field calibration adjust models to real conditions.",
            "Multiple core samples improve representativeness."
        ],
        resolution_strategy="Combine laboratory analysis with field calibration and history matching.",
        entity_scope="Reservoir modeling",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE 942 Section 3"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement - Online Meters vs Manual Sampling",
        keywords=["water cut", "online meters", "manual sampling", "measurement", "accuracy"],
        conclusion_template="Online meters provide real-time water cut measurement but must be validated against manual sampling.",
        reasoning_framework=(
            "Online water cut meters use capacitance, microwave, or infrared sensors to provide continuous measurement. "
            "Manual sampling involves periodic collection and laboratory analysis. "
            "Online meters offer operational efficiency but may suffer from calibration drift and emulsion effects. "
            "Manual sampling is more accurate but less frequent. "
            "Best practice is to validate online meter readings with periodic manual samples and calibrate devices regularly."
        ),
        key_factors=["Meter calibration", "Sampling frequency", "Emulsion effects", "Operational efficiency", "Validation"],
        primary_authority=["API RP 13B-1", "ISO 3170", "SPE 169934"],
        burden_holder="Operator",
        adversary_position="Online meters are unreliable in high-emulsion environments.",
        counter_arguments=[
            "Regular calibration and validation reduce errors.",
            "Hybrid approach combines efficiency and accuracy."
        ],
        resolution_strategy="Use hybrid measurement and maintain calibration schedule.",
        entity_scope="Field operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 10"
    ),
    DoctrineBlock(
        topic="Water Disposal Regulations - UIC Class II Wells",
        keywords=["water disposal", "regulations", "UIC Class II", "EPA", "injection"],
        conclusion_template="Produced water disposal must comply with EPA UIC Class II regulations for injection wells.",
        reasoning_framework=(
            "EPA UIC Class II regulations govern the disposal of produced water via injection wells. "
            "Requirements include well integrity testing, water quality monitoring, and reporting. "
            "Operators must demonstrate compliance to avoid environmental contamination and legal penalties. "
            "Periodic audits and inspections are mandated. "
            "Non-compliance leads to fines, well shutdown, and remediation obligations."
        ),
        key_factors=["Well integrity", "Water quality", "Monitoring", "Reporting", "Compliance audits"],
        primary_authority=["EPA UIC Class II", "API RP 13B-1", "ISO 14001"],
        burden_holder="Operator",
        adversary_position="Regulatory compliance increases operational costs and complexity.",
        counter_arguments=[
            "Compliance ensures environmental protection and legal operation.",
            "Advanced monitoring reduces risk and cost."
        ],
        resolution_strategy="Implement robust monitoring and reporting systems to ensure compliance.",
        entity_scope="Produced water disposal",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA UIC Class II Section 4"
    ),
    DoctrineBlock(
        topic="Declining Oil Rate with Constant Liquid Rate - Artificial Lift Constraints",
        keywords=["oil rate", "liquid rate", "artificial lift", "constraints", "production"],
        conclusion_template="Artificial lift systems must be optimized to manage declining oil rates with constant liquid production.",
        reasoning_framework=(
            "As water cut increases, oil rate declines while total liquid rate remains constant. "
            "Artificial lift systems (e.g., ESP, PCP, gas lift) must be adjusted to maintain production efficiency. "
            "Lift selection depends on fluid properties, well depth, and water cut. "
            "Constraints include pump sizing, gas injection rate, and system reliability. "
            "Optimization involves monitoring performance and adjusting parameters as water cut changes."
        ),
        key_factors=["Lift system selection", "Pump sizing", "Gas injection rate", "Water cut", "System reliability"],
        primary_authority=["API RP 13B-1", "SPE 169934", "Lake, Enhanced Oil Recovery"],
        burden_holder="Production engineer",
        adversary_position="Artificial lift optimization is limited by equipment constraints and high water cut.",
        counter_arguments=[
            "Advanced lift systems and real-time monitoring improve adaptability.",
            "Periodic optimization maintains efficiency."
        ],
        resolution_strategy="Use adaptive lift systems and monitor performance for timely optimization.",
        entity_scope="Production operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 11"
    ),
    DoctrineBlock(
        topic="Waterflood Pattern Balancing - Injection-Production Ratio",
        keywords=["waterflood", "pattern balancing", "injection-production ratio", "reservoir", "optimization"],
        conclusion_template="Pattern balancing is achieved by optimizing the injection-production ratio to maximize sweep efficiency.",
        reasoning_framework=(
            "Pattern balancing involves adjusting injection and production rates to achieve uniform reservoir sweep. "
            "The injection-production ratio is monitored to prevent channeling and early breakthrough. "
            "Reservoir simulation and diagnostic plots guide optimization. "
            "Imbalances are corrected by adjusting well rates or reconfiguring patterns. "
            "Continuous monitoring ensures sustained performance."
        ),
        key_factors=["Injection rate", "Production rate", "Sweep efficiency", "Pattern configuration", "Monitoring"],
        primary_authority=["SPE 169934", "API RP 13B-1", "Lake, Enhanced Oil Recovery"],
        burden_holder="Reservoir engineer",
        adversary_position="Pattern balancing is difficult in heterogeneous reservoirs.",
        counter_arguments=[
            "Simulation and diagnostic tools improve balancing in complex reservoirs.",
            "Selective injection mitigates heterogeneity effects."
        ],
        resolution_strategy="Use simulation and diagnostics to optimize balancing.",
        entity_scope="Waterflood operations",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 169934 Section 12"
    ),
    DoctrineBlock(
        topic="Emulsion Stability and Demulsification",
        keywords=["emulsion", "stability", "demulsification", "water cut", "treatment"],
        conclusion_template="Demulsification is required to break stable emulsions and ensure accurate water cut measurement and efficient treatment.",
        reasoning_framework=(
            "Stable emulsions in produced fluids hinder separation and measurement. "
            "Demulsification involves chemical dosing, heating, and mechanical separation. "
            "Selection of demulsifiers depends on fluid properties and emulsion type. "
            "Treatment effectiveness is monitored via laboratory tests and field performance. "
            "Failure to break emulsions leads to inaccurate water cut and inefficient water treatment."
        ),
        key_factors=["Emulsion type", "Demulsifier selection", "Treatment process", "Monitoring", "Fluid properties"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3734"],
        burden_holder="Operator",
        adversary_position="Demulsification increases chemical costs and may not be effective for all emulsions.",
        counter_arguments=[
            "Optimized chemical selection improves efficiency and reduces cost.",
            "Combination of chemical and mechanical methods enhances performance."
        ],
        resolution_strategy="Optimize demulsifier selection and combine treatment methods.",
        entity_scope="Produced fluid treatment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 13"
    ),
    DoctrineBlock(
        topic="Water Influx from Aquifer - Material Balance",
        keywords=["water influx", "aquifer", "material balance", "reservoir", "modeling"],
        conclusion_template="Material balance equations are used to estimate water influx from aquifers and its impact on reservoir performance.",
        reasoning_framework=(
            "Water influx from aquifers is modeled using material balance equations and aquifer models (e.g., Fetkovich, van Everdingen-Hurst). "
            "Estimation requires reservoir pressure data, production history, and aquifer properties. "
            "Material balance supports reservoir management and forecasting. "
            "Limitations include uncertainty in aquifer size and properties."
        ),
        key_factors=["Reservoir pressure", "Production history", "Aquifer properties", "Material balance", "Model calibration"],
        primary_authority=["SPE 942", "Lake, Enhanced Oil Recovery", "API RP 13B-1"],
        burden_holder="Reservoir engineer",
        adversary_position="Aquifer models are uncertain due to limited data.",
        counter_arguments=[
            "History matching and sensitivity analysis reduce uncertainty.",
            "Multiple models improve reliability."
        ],
        resolution_strategy="Use history matching and sensitivity analysis to refine aquifer models.",
        entity_scope="Reservoir management",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 942 Section 4"
    ),
    DoctrineBlock(
        topic="Water Saturation from Well Logs - Archie Equation",
        keywords=["water saturation", "well logs", "Archie equation", "formation evaluation", "resistivity"],
        conclusion_template="Archie equation is used to calculate water saturation from resistivity logs in clean formations.",
        reasoning_framework=(
            "Archie equation relates formation resistivity to water saturation, porosity, and water resistivity. "
            "It is applicable to clean, non-shaly formations. "
            "Log interpretation requires calibration of parameters (a, m, n) and accurate measurement of resistivity and porosity. "
            "Water saturation estimation supports reservoir evaluation and production planning. "
            "Limitations include applicability to shaly formations and parameter uncertainty."
        ),
        key_factors=["Formation resistivity", "Porosity", "Water resistivity", "Parameter calibration", "Log quality"],
        primary_authority=["Archie (1942)", "API RP 13B-1", "SPE 169934"],
        burden_holder="Petrophysicist",
        adversary_position="Archie equation is unreliable in shaly or complex formations.",
        counter_arguments=[
            "Alternative equations (e.g., Waxman-Smits) address shaly formations.",
            "Calibration and core validation improve reliability."
        ],
        resolution_strategy="Use alternative equations and calibrate parameters for complex formations.",
        entity_scope="Formation evaluation",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Archie (1942) SPE 169934"
    ),
    DoctrineBlock(
        topic="Produced Water Salinity and Water Type Identification",
        keywords=["produced water", "salinity", "water type", "identification", "analysis"],
        conclusion_template="Produced water salinity analysis is used to identify water type and source for reservoir management.",
        reasoning_framework=(
            "Salinity analysis involves measuring dissolved salts in produced water using laboratory techniques (e.g., ion chromatography, titration). "
            "Water type identification supports reservoir characterization, waterflood management, and conformance diagnosis. "
            "Comparison with injection water and aquifer samples helps trace water sources and breakthrough events. "
            "Salinity trends are monitored for operational optimization."
        ),
        key_factors=["Salinity measurement", "Water type", "Source identification", "Laboratory analysis", "Trend monitoring"],
        primary_authority=["API RP 13B-1", "ISO 10304", "SPE 169934"],
        burden_holder="Reservoir engineer",
        adversary_position="Salinity analysis is limited by sample contamination and measurement errors.",
        counter_arguments=[
            "Strict sample handling and laboratory protocols reduce errors.",
            "Cross-validation with multiple methods improves reliability."
        ],
        resolution_strategy="Adhere to laboratory protocols and use multiple analysis methods.",
        entity_scope="Produced water analysis",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 14"
    ),
    DoctrineBlock(
        topic="Waterflood Conformance - Gel and Polymer Treatments",
        keywords=["waterflood", "conformance", "gel treatment", "polymer treatment", "reservoir"],
        conclusion_template="Gel and polymer treatments are applied to improve waterflood conformance and reduce channeling.",
        reasoning_framework=(
            "Conformance treatments involve injecting gels or polymers to block high-permeability channels and improve sweep efficiency. "
            "Treatment design depends on reservoir properties, channel location, and fluid compatibility. "
            "Performance is monitored via water cut trends and tracer tests. "
            "Limitations include treatment longevity and placement accuracy."
        ),
        key_factors=["Treatment design", "Reservoir properties", "Channel location", "Fluid compatibility", "Performance monitoring"],
        primary_authority=["SPE 169934", "API RP 13B-1", "Lake, Enhanced Oil Recovery"],
        burden_holder="Reservoir engineer",
        adversary_position="Gel and polymer treatments may cause formation damage and are difficult to place accurately.",
        counter_arguments=[
            "Advanced placement techniques and compatibility testing reduce risks.",
            "Monitoring ensures treatment effectiveness."
        ],
        resolution_strategy="Use advanced placement and monitor performance post-treatment.",
        entity_scope="Waterflood operations",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 169934 Section 15"
    ),
    DoctrineBlock(
        topic="Economic Limit - Oil Price Sensitivity and Operating Cost",
        keywords=["economic limit", "oil price", "operating cost", "water cut", "production"],
        conclusion_template="Economic limit is determined by oil price sensitivity and operating cost relative to water cut and production rate.",
        reasoning_framework=(
            "Economic limit is reached when operating costs exceed revenue from oil production. "
            "Water cut increases operating cost due to treatment and disposal. "
            "Oil price fluctuations impact economic viability. "
            "Analysis involves forecasting production, water cut, cost, and price scenarios. "
            "Shutdown or conversion to waterflood is considered at economic limit."
        ),
        key_factors=["Operating cost", "Oil price", "Water cut", "Production rate", "Forecasting"],
        primary_authority=["API RP 13B-1", "SPE 169934", "Lake, Enhanced Oil Recovery"],
        burden_holder="Operator",
        adversary_position="Economic limit analysis is uncertain due to unpredictable oil prices.",
        counter_arguments=[
            "Scenario analysis and hedging reduce uncertainty.",
            "Continuous monitoring allows timely decision-making."
        ],
        resolution_strategy="Use scenario analysis and monitor costs and prices for timely action.",
        entity_scope="Production economics",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="API RP 13B-1 Section 16"
    ),
    DoctrineBlock(
        topic="Water Production Forecasting - Koval and X-plot Methods",
        keywords=["water production", "forecasting", "Koval method", "X-plot", "reservoir"],
        conclusion_template="Koval and X-plot methods are used to forecast water production and breakthrough in waterflood operations.",
        reasoning_framework=(
            "Koval method adjusts for reservoir heterogeneity in waterflood forecasting. "
            "X-plot graphs water cut versus cumulative liquid production to identify breakthrough and forecast future water production. "
            "Both methods support waterflood optimization and conformance diagnosis. "
            "Limitations include data quality and model assumptions."
        ),
        key_factors=["Reservoir heterogeneity", "Water cut trend", "Cumulative production", "Model calibration", "Data quality"],
        primary_authority=["Koval (1963)", "SPE 169934", "API RP 13B-1"],
        burden_holder="Reservoir engineer",
        adversary_position="Forecasting methods are limited by data quality and reservoir complexity.",
        counter_arguments=[
            "Data validation and model calibration improve reliability.",
            "Combine multiple forecasting methods for robust results."
        ],
        resolution_strategy="Validate data and calibrate models for improved forecasting.",
        entity_scope="Waterflood operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Koval (1963) SPE 169934"
    ),
    DoctrineBlock(
        topic="Water Cut and BSW Measurement in High-Pressure Environments",
        keywords=["water cut", "BSW", "high-pressure", "measurement", "sampling"],
        conclusion_template="Specialized sampling and measurement techniques are required for accurate water cut and BSW determination in high-pressure environments.",
        reasoning_framework=(
            "High-pressure environments affect fluid properties and separation efficiency. "
            "Sampling must be performed using pressure-maintaining devices to prevent phase changes. "
            "Measurement devices must be rated for high pressure and calibrated accordingly. "
            "Laboratory analysis should replicate field pressure conditions for accuracy."
        ),
        key_factors=["Pressure-maintaining sampling", "Device calibration", "Laboratory replication", "Fluid properties", "Safety protocols"],
        primary_authority=["API RP 13B-1", "ISO 3170", "SPE 169934"],
        burden_holder="Operator",
        adversary_position="High-pressure sampling is costly and prone to safety risks.",
        counter_arguments=[
            "Pressure-maintaining devices and safety protocols mitigate risks.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use specialized devices and adhere to safety protocols.",
        entity_scope="High-pressure operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 17"
    ),
    DoctrineBlock(
        topic="Produced Water Reuse for Waterflood Operations",
        keywords=["produced water", "reuse", "waterflood", "operations", "treatment"],
        conclusion_template="Produced water can be reused for waterflood operations after appropriate treatment to meet injection quality standards.",
        reasoning_framework=(
            "Produced water reuse reduces disposal volumes and supports sustainable waterflood operations. "
            "Treatment processes must remove oil, solids, bacteria, and scale-forming ions. "
            "Quality monitoring ensures compliance with injection standards. "
            "Reuse is governed by regulatory requirements and operational feasibility."
        ),
        key_factors=["Treatment process", "Injection quality", "Regulatory compliance", "Monitoring", "Operational feasibility"],
        primary_authority=["API RP 13B-1", "EPA UIC Class II", "ISO 14001"],
        burden_holder="Operator",
        adversary_position="Reuse increases treatment complexity and may not meet injection standards.",
        counter_arguments=[
            "Advanced treatment technologies ensure compliance.",
            "Reuse supports sustainability and cost reduction."
        ],
        resolution_strategy="Adopt advanced treatment and monitor quality for reuse.",
        entity_scope="Waterflood operations",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 18"
    ),
    DoctrineBlock(
        topic="Water Cut Impact on Artificial Lift Selection",
        keywords=["water cut", "artificial lift", "selection", "production", "optimization"],
        conclusion_template="Artificial lift selection must consider water cut to optimize production and minimize operational issues.",
        reasoning_framework=(
            "High water cut affects artificial lift performance due to increased liquid volume and reduced oil rate. "
            "Lift selection (ESP, PCP, gas lift) depends on fluid properties, well depth, and water cut. "
            "System reliability, pump sizing, and maintenance requirements are key factors. "
            "Optimization involves monitoring water cut and adjusting lift parameters."
        ),
        key_factors=["Water cut", "Lift system", "Pump sizing", "Reliability", "Maintenance"],
        primary_authority=["API RP 13B-1", "SPE 169934", "Lake, Enhanced Oil Recovery"],
        burden_holder="Production engineer",
        adversary_position="High water cut limits artificial lift efficiency and increases maintenance.",
        counter_arguments=[
            "Adaptive lift systems and predictive maintenance improve performance.",
            "Periodic optimization maintains efficiency."
        ],
        resolution_strategy="Use adaptive systems and monitor performance for optimization.",
        entity_scope="Production operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 19"
    ),
    DoctrineBlock(
        topic="Water Cut Trend Analysis for Reservoir Management",
        keywords=["water cut", "trend analysis", "reservoir management", "production", "optimization"],
        conclusion_template="Water cut trend analysis supports reservoir management and production optimization by identifying breakthrough and conformance issues.",
        reasoning_framework=(
            "Trend analysis involves plotting water cut versus time or cumulative production to identify breakthrough, channeling, and conformance issues. "
            "Analysis supports production optimization and conformance treatment design. "
            "Limitations include data variability and interpretation subjectivity."
        ),
        key_factors=["Water cut trend", "Production data", "Breakthrough identification", "Conformance issues", "Data quality"],
        primary_authority=["SPE 169934", "API RP 13B-1", "Lake, Enhanced Oil Recovery"],
        burden_holder="Reservoir engineer",
        adversary_position="Trend analysis is unreliable due to fluctuating production rates.",
        counter_arguments=[
            "Data smoothing and statistical analysis improve reliability.",
            "Combine trend analysis with diagnostic plots for robust interpretation."
        ],
        resolution_strategy="Apply statistical smoothing and use supporting diagnostics.",
        entity_scope="Reservoir management",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="SPE 169934 Section 20"
    ),
    DoctrineBlock(
        topic="Water Cut and BSW Measurement in Multiphase Flow",
        keywords=["water cut", "BSW", "multiphase flow", "measurement", "sampling"],
        conclusion_template="Measurement of water cut and BSW in multiphase flow requires specialized devices and sampling protocols.",
        reasoning_framework=(
            "Multiphase flow complicates water cut and BSW measurement due to phase mixing and emulsion formation. "
            "Specialized meters (e.g., microwave, capacitance) and sampling protocols are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Periodic maintenance and device upgrades are necessary for sustained performance."
        ),
        key_factors=["Multiphase meter", "Sampling protocol", "Calibration", "Validation", "Maintenance"],
        primary_authority=["API RP 13B-1", "ISO 3170", "SPE 169934"],
        burden_holder="Operator",
        adversary_position="Multiphase meters are costly and prone to calibration drift.",
        counter_arguments=[
            "Regular calibration and validation reduce errors.",
            "Hybrid approach combines efficiency and accuracy."
        ],
        resolution_strategy="Use hybrid measurement and maintain calibration schedule.",
        entity_scope="Multiphase flow operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 21"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Heavy Oil Reservoirs",
        keywords=["water cut", "heavy oil", "measurement", "sampling", "accuracy"],
        conclusion_template="Water cut measurement in heavy oil reservoirs requires specialized sampling and separation techniques.",
        reasoning_framework=(
            "Heavy oil complicates water cut measurement due to high viscosity and emulsion stability. "
            "Sampling must be performed using heated devices and emulsion breakers. "
            "Separation efficiency is improved with chemical dosing and mechanical methods. "
            "Laboratory analysis should replicate field conditions for accuracy."
        ),
        key_factors=["Heated sampling", "Emulsion breaker", "Separation efficiency", "Laboratory replication", "Fluid properties"],
        primary_authority=["API RP 13B-1", "ISO 3734", "SPE 169934"],
        burden_holder="Operator",
        adversary_position="Heavy oil sampling is costly and prone to errors.",
        counter_arguments=[
            "Specialized devices and protocols improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use specialized devices and adhere to protocols.",
        entity_scope="Heavy oil operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 22"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Offshore Operations",
        keywords=["water cut", "offshore", "measurement", "sampling", "accuracy"],
        conclusion_template="Water cut measurement in offshore operations requires robust devices and protocols to ensure accuracy under harsh conditions.",
        reasoning_framework=(
            "Offshore operations present challenges for water cut measurement due to harsh environmental conditions and limited access. "
            "Robust devices rated for offshore use and specialized sampling protocols are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Remote monitoring and data transmission support operational efficiency."
        ),
        key_factors=["Offshore-rated device", "Sampling protocol", "Calibration", "Validation", "Remote monitoring"],
        primary_authority=["API RP 13B-1", "ISO 3170", "SPE 169934"],
        burden_holder="Operator",
        adversary_position="Offshore measurement is costly and prone to errors.",
        counter_arguments=[
            "Robust devices and remote monitoring improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use robust devices and remote monitoring.",
        entity_scope="Offshore operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 23"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Unconventional Reservoirs",
        keywords=["water cut", "unconventional reservoir", "measurement", "sampling", "accuracy"],
        conclusion_template="Water cut measurement in unconventional reservoirs requires adaptation of sampling and measurement techniques to account for complex fluid properties.",
        reasoning_framework=(
            "Unconventional reservoirs (e.g., shale, tight oil) present challenges for water cut measurement due to complex fluid properties and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with reservoir models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in unconventional reservoirs is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Unconventional reservoir operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 24"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in High-Temperature Environments",
        keywords=["water cut", "high-temperature", "measurement", "sampling", "accuracy"],
        conclusion_template="High-temperature environments require specialized devices and protocols for accurate water cut measurement.",
        reasoning_framework=(
            "High-temperature environments affect fluid properties and device performance. "
            "Sampling must be performed using temperature-resistant devices and protocols. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Periodic maintenance and device upgrades are necessary for sustained performance."
        ),
        key_factors=["Temperature-resistant device", "Sampling protocol", "Calibration", "Validation", "Maintenance"],
        primary_authority=["API RP 13B-1", "ISO 3170", "SPE 169934"],
        burden_holder="Operator",
        adversary_position="High-temperature measurement is costly and prone to errors.",
        counter_arguments=[
            "Temperature-resistant devices and protocols improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use specialized devices and adhere to protocols.",
        entity_scope="High-temperature operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 25"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Low-Rate Wells",
        keywords=["water cut", "low-rate well", "measurement", "sampling", "accuracy"],
        conclusion_template="Low-rate wells require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Low-rate wells produce small volumes, complicating water cut measurement due to limited sample size and separation efficiency. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in low-rate wells is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Low-rate well operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 26"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in High-Viscosity Fluids",
        keywords=["water cut", "high-viscosity", "measurement", "sampling", "accuracy"],
        conclusion_template="High-viscosity fluids require specialized sampling and separation techniques for accurate water cut measurement.",
        reasoning_framework=(
            "High-viscosity fluids complicate water cut measurement due to emulsion stability and separation challenges. "
            "Sampling must be performed using heated devices and emulsion breakers. "
            "Separation efficiency is improved with chemical dosing and mechanical methods. "
            "Laboratory analysis should replicate field conditions for accuracy."
        ),
        key_factors=["Heated sampling", "Emulsion breaker", "Separation efficiency", "Laboratory replication", "Fluid properties"],
        primary_authority=["API RP 13B-1", "ISO 3734", "SPE 169934"],
        burden_holder="Operator",
        adversary_position="High-viscosity sampling is costly and prone to errors.",
        counter_arguments=[
            "Specialized devices and protocols improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use specialized devices and adhere to protocols.",
        entity_scope="High-viscosity operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 27"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Gas-Lift Wells",
        keywords=["water cut", "gas-lift well", "measurement", "sampling", "accuracy"],
        conclusion_template="Gas-lift wells require specialized sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Gas-lift wells produce multiphase flow, complicating water cut measurement due to gas-liquid mixing and emulsion formation. "
            "Specialized meters (e.g., microwave, capacitance) and sampling protocols are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Periodic maintenance and device upgrades are necessary for sustained performance."
        ),
        key_factors=["Multiphase meter", "Sampling protocol", "Calibration", "Validation", "Maintenance"],
        primary_authority=["API RP 13B-1", "ISO 3170", "SPE 169934"],
        burden_holder="Operator",
        adversary_position="Gas-lift measurement is costly and prone to errors.",
        counter_arguments=[
            "Specialized devices and protocols improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use specialized devices and adhere to protocols.",
        entity_scope="Gas-lift well operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 28"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Horizontal Wells",
        keywords=["water cut", "horizontal well", "measurement", "sampling", "accuracy"],
        conclusion_template="Horizontal wells require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Horizontal wells present challenges for water cut measurement due to variable flow profiles and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in horizontal wells is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Horizontal well operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 29"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Multi-Lateral Wells",
        keywords=["water cut", "multi-lateral well", "measurement", "sampling", "accuracy"],
        conclusion_template="Multi-lateral wells require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Multi-lateral wells present challenges for water cut measurement due to variable flow profiles and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in multi-lateral wells is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Multi-lateral well operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 30"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Commingled Production",
        keywords=["water cut", "commingled production", "measurement", "sampling", "accuracy"],
        conclusion_template="Commingled production requires adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Commingled production presents challenges for water cut measurement due to variable flow profiles and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in commingled production is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Commingled production operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 31"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Enhanced Oil Recovery (EOR) Operations",
        keywords=["water cut", "EOR", "measurement", "sampling", "accuracy"],
        conclusion_template="EOR operations require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "EOR operations present challenges for water cut measurement due to complex fluid properties and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in EOR operations is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="EOR operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 32"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in CO2 Flood Operations",
        keywords=["water cut", "CO2 flood", "measurement", "sampling", "accuracy"],
        conclusion_template="CO2 flood operations require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "CO2 flood operations present challenges for water cut measurement due to complex fluid properties and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in CO2 flood operations is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="CO2 flood operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 33"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Polymer Flood Operations",
        keywords=["water cut", "polymer flood", "measurement", "sampling", "accuracy"],
        conclusion_template="Polymer flood operations require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Polymer flood operations present challenges for water cut measurement due to complex fluid properties and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in polymer flood operations is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Polymer flood operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 34"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Thermal EOR Operations",
        keywords=["water cut", "thermal EOR", "measurement", "sampling", "accuracy"],
        conclusion_template="Thermal EOR operations require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Thermal EOR operations present challenges for water cut measurement due to high temperature, complex fluid properties, and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in thermal EOR operations is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Thermal EOR operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 35"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Chemical EOR Operations",
        keywords=["water cut", "chemical EOR", "measurement", "sampling", "accuracy"],
        conclusion_template="Chemical EOR operations require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Chemical EOR operations present challenges for water cut measurement due to complex fluid properties and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in chemical EOR operations is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Chemical EOR operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 36"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Microbial EOR Operations",
        keywords=["water cut", "microbial EOR", "measurement", "sampling", "accuracy"],
        conclusion_template="Microbial EOR operations require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Microbial EOR operations present challenges for water cut measurement due to complex fluid properties and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in microbial EOR operations is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Microbial EOR operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 37"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Hydraulic Fracturing Operations",
        keywords=["water cut", "hydraulic fracturing", "measurement", "sampling", "accuracy"],
        conclusion_template="Hydraulic fracturing operations require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Hydraulic fracturing operations present challenges for water cut measurement due to complex fluid properties and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in hydraulic fracturing operations is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Hydraulic fracturing operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 38"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Acidizing Operations",
        keywords=["water cut", "acidizing", "measurement", "sampling", "accuracy"],
        conclusion_template="Acidizing operations require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Acidizing operations present challenges for water cut measurement due to complex fluid properties and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in acidizing operations is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Acidizing operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 39"
    ),
    DoctrineBlock(
        topic="Water Cut Measurement in Well Stimulation Operations",
        keywords=["water cut", "well stimulation", "measurement", "sampling", "accuracy"],
        conclusion_template="Well stimulation operations require adapted sampling and measurement techniques for accurate water cut determination.",
        reasoning_framework=(
            "Well stimulation operations present challenges for water cut measurement due to complex fluid properties and multiphase flow. "
            "Adapted sampling protocols and specialized devices are required. "
            "Calibration and validation against laboratory analysis ensure accuracy. "
            "Data integration with production models supports operational optimization."
        ),
        key_factors=["Adapted sampling", "Specialized device", "Calibration", "Validation", "Data integration"],
        primary_authority=["API RP 13B-1", "SPE 169934", "ISO 3170"],
        burden_holder="Operator",
        adversary_position="Measurement in well stimulation operations is costly and prone to errors.",
        counter_arguments=[
            "Adapted protocols and devices improve accuracy.",
            "Accurate measurement is essential for production optimization."
        ],
        resolution_strategy="Use adapted protocols and integrate data with models.",
        entity_scope="Well stimulation operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API RP 13B-1 Section 40"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    results = []
    keyword_lower = keyword.lower()
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]