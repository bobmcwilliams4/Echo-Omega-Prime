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
        topic="Radial vs Bias-Ply Construction",
        keywords=["radial tires", "bias-ply tires", "tire construction", "tread life", "sidewall flexibility", "heat dissipation"],
        conclusion_template="Radial tires provide superior tread life and heat dissipation compared to bias-ply tires, making them preferable for most passenger vehicles.",
        reasoning_framework=(
            "Radial tire construction features cords arranged at 90 degrees to the direction of travel, "
            "allowing the sidewall and tread to function independently. This results in better flexibility, "
            "improved heat dissipation, and longer tread life. Bias-ply tires have cords arranged diagonally "
            "in alternating layers, which increases sidewall stiffness but causes more heat buildup and "
            "uneven tread wear. The reasoning involves analyzing the mechanical behavior of tire carcasses "
            "under load, the impact of heat on rubber compounds, and the resulting wear patterns. "
            "Empirical studies and manufacturer data consistently show radial tires outperform bias-ply in "
            "durability and performance metrics. However, bias-ply tires may still be preferred in certain "
            "off-road or heavy-load applications due to their sidewall strength."
        ),
        key_factors=["cord orientation", "sidewall flexibility", "heat dissipation", "tread wear patterns", "application type"],
        primary_authority=["Tire and Rim Association Standards", "Rubber Manufacturers Association Technical Papers", "SAE International Tire Engineering Handbook"],
        burden_holder="Tire Manufacturer",
        adversary_position="Bias-ply proponents argue superior sidewall strength and off-road durability.",
        counter_arguments=[
            "Radial tires' improved heat dissipation reduces failure risk under normal operating conditions.",
            "Modern radial tires have reinforced sidewalls to address off-road durability concerns."
        ],
        resolution_strategy="Evaluate application-specific requirements and empirical performance data to select appropriate construction.",
        entity_scope="Passenger and light truck tires",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Tire and Rim Association Bulletin 123, 2018"
    ),
    DoctrineBlock(
        topic="Center Wear Pattern Analysis",
        keywords=["center wear", "tread wear", "overinflation", "tire pressure", "wear pattern diagnosis"],
        conclusion_template="Center wear on a tire tread is primarily indicative of overinflation, leading to reduced contact patch and accelerated center tread wear.",
        reasoning_framework=(
            "Tire tread wear patterns provide diagnostic insight into inflation and alignment conditions. "
            "Center wear occurs when the tire's inflation pressure exceeds manufacturer recommendations, "
            "causing the tire to bulge in the center and reduce contact with the road surface on the shoulders. "
            "This concentrates load and friction on the center tread ribs, accelerating wear in that area. "
            "The reasoning involves understanding tire mechanics, contact patch distribution, and the relationship "
            "between inflation pressure and tread wear. Data from controlled inflation tests and field observations "
            "support this conclusion. Alternative causes such as aggressive acceleration or alignment issues "
            "do not typically produce isolated center wear patterns."
        ),
        key_factors=["inflation pressure", "contact patch", "tread wear location", "load distribution"],
        primary_authority=["National Highway Traffic Safety Administration (NHTSA) Tire Safety Guidelines", "Tire Industry Association Technical Bulletins"],
        burden_holder="Vehicle Operator",
        adversary_position="Some argue that aggressive driving or alignment faults cause center wear.",
        counter_arguments=[
            "Aggressive driving tends to cause edge or cupping wear, not isolated center wear.",
            "Alignment faults typically produce uneven shoulder wear patterns."
        ],
        resolution_strategy="Verify tire pressure regularly and inspect wear patterns to confirm overinflation diagnosis.",
        entity_scope="All pneumatic tires",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NHTSA Tire Pressure and Wear Analysis Report, 2020"
    ),
    DoctrineBlock(
        topic="Shoulder Wear Pattern Analysis",
        keywords=["shoulder wear", "tread wear", "underinflation", "alignment", "camber wear"],
        conclusion_template="Shoulder wear on tires is typically caused by underinflation or excessive positive camber, resulting in increased load and friction on the tire edges.",
        reasoning_framework=(
            "Shoulder wear patterns arise when the tire's edges bear more load than the center. Underinflation causes "
            "the tire to flatten, increasing the contact area at the shoulders and accelerating wear there. "
            "Alternatively, improper wheel alignment, particularly excessive positive camber, tilts the tire so "
            "that the outer edges contact the road more heavily. The reasoning includes mechanical analysis of load "
            "distribution, tire deformation under pressure, and alignment geometry. Empirical evidence from tire "
            "inspections and alignment measurements supports these causes. Distinguishing between underinflation and "
            "alignment requires pressure checks and alignment diagnostics."
        ),
        key_factors=["inflation pressure", "wheel alignment", "camber angle", "tread wear location"],
        primary_authority=["SAE J2530 Alignment Standards", "Tire Industry Association Maintenance Guidelines"],
        burden_holder="Vehicle Maintenance Personnel",
        adversary_position="Some claim that aggressive cornering alone causes shoulder wear.",
        counter_arguments=[
            "Aggressive cornering can exacerbate wear but does not solely cause consistent shoulder wear patterns.",
            "Proper inflation and alignment mitigate cornering wear effects."
        ],
        resolution_strategy="Conduct regular tire pressure checks and wheel alignment inspections to identify and correct causes.",
        entity_scope="Passenger and commercial vehicle tires",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="SAE J2530 Alignment and Tire Wear Correlation Study, 2019"
    ),
    DoctrineBlock(
        topic="Cupping and Scalloping Wear",
        keywords=["cupping", "scalloping", "tread wear", "wheel balance", "suspension wear", "vibration"],
        conclusion_template="Cupping or scalloping tread wear patterns indicate wheel imbalance or suspension component wear, causing uneven tire contact and vibration.",
        reasoning_framework=(
            "Cupping and scalloping are characterized by high and low points on the tread surface, often felt as vibrations "
            "while driving. These patterns result from irregular tire contact with the road due to wheel imbalance or worn "
            "suspension parts such as shocks or bushings. The reasoning involves dynamic analysis of tire-road interaction, "
            "vibration transmission through suspension, and the effect of mechanical faults on tire wear. Diagnostic procedures "
            "include wheel balancing tests, suspension inspections, and correlation of vibration symptoms with wear patterns. "
            "Corrective actions restore uniform contact and prevent accelerated tire damage."
        ),
        key_factors=["wheel balance", "suspension condition", "vibration presence", "wear pattern shape"],
        primary_authority=["SAE J2530 Wheel Balance Standards", "Automotive Service Excellence (ASE) Suspension Guidelines"],
        burden_holder="Vehicle Maintenance Technician",
        adversary_position="Some suggest road surface irregularities cause cupping.",
        counter_arguments=[
            "While road irregularities contribute, persistent cupping is primarily linked to mechanical faults.",
            "Proper maintenance eliminates vibration-induced wear."
        ],
        resolution_strategy="Perform wheel balancing and suspension component replacement as needed to restore uniform tread wear.",
        entity_scope="All vehicle tires",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ASE Suspension and Tire Wear Diagnostic Manual, 2021"
    ),
    DoctrineBlock(
        topic="Feathering Wear Pattern",
        keywords=["feathering", "tread wear", "toe alignment", "tire noise", "steering geometry"],
        conclusion_template="Feathering tread wear is caused by incorrect toe alignment, leading to angled tread block edges and increased tire noise.",
        reasoning_framework=(
            "Feathering wear manifests as a sawtooth pattern on the tread edges, often accompanied by a chirping noise during driving. "
            "This pattern results from improper toe settings, where the tires point slightly inward or outward relative to the vehicle's "
            "centerline. The misalignment causes the tread blocks to scrub against the road at an angle during rotation. "
            "The reasoning includes analysis of steering geometry, tire-road frictional forces, and the mechanical impact of toe misalignment. "
            "Alignment measurements and road tests confirm the correlation. Correcting toe angles restores proper tread contact and reduces noise."
        ),
        key_factors=["toe angle", "steering geometry", "tread block wear", "noise symptoms"],
        primary_authority=["SAE J2530 Alignment Standards", "Tire Industry Association Noise and Wear Reports"],
        burden_holder="Alignment Technician",
        adversary_position="Some claim feathering is caused by aggressive cornering.",
        counter_arguments=[
            "Aggressive cornering may exacerbate wear but does not create the characteristic feathering pattern.",
            "Proper toe alignment is the primary factor."
        ],
        resolution_strategy="Adjust toe alignment to manufacturer specifications and verify with road testing.",
        entity_scope="Passenger vehicle tires",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="SAE J2530 Alignment and Noise Correlation Study, 2020"
    ),
    DoctrineBlock(
        topic="Load Index and Speed Rating Compliance",
        keywords=["load index", "speed rating", "tire specifications", "vehicle safety", "manufacturer recommendations"],
        conclusion_template="Tires must meet or exceed the vehicle manufacturer's specified load index and speed rating to ensure safe operation.",
        reasoning_framework=(
            "Load index and speed rating are standardized indicators of a tire's maximum load carrying capacity and maximum safe speed. "
            "Compliance with these specifications is critical to maintain vehicle safety, handling, and tire integrity. "
            "Using tires with lower ratings than specified can lead to premature failure, reduced performance, and increased accident risk. "
            "The reasoning involves understanding tire construction limits, regulatory standards, and manufacturer design criteria. "
            "Regulatory bodies such as DOT and ECE mandate adherence to these ratings. Vehicle manufacturers specify minimum requirements "
            "based on vehicle weight, power, and intended use. Compliance is verified through tire markings and certification."
        ),
        key_factors=["tire load index", "speed rating", "vehicle specifications", "regulatory standards"],
        primary_authority=["Department of Transportation (DOT) Regulations", "Economic Commission for Europe (ECE) Tire Standards", "Vehicle Manufacturer Guidelines"],
        burden_holder="Tire Installer and Vehicle Owner",
        adversary_position="Some argue that slightly lower ratings are acceptable for cost savings.",
        counter_arguments=[
            "Non-compliance increases risk of tire failure and liability.",
            "Cost savings do not justify safety compromises."
        ],
        resolution_strategy="Always select tires meeting or exceeding manufacturer load and speed ratings and verify markings before installation.",
        entity_scope="All road vehicle tires",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="DOT FMVSS No. 139 and ECE R30 Tire Regulations"
    ),
    DoctrineBlock(
        topic="Seasonal Tire Selection - Winter vs All-Season",
        keywords=["winter tires", "all-season tires", "seasonal performance", "traction", "temperature effects"],
        conclusion_template="Winter tires provide superior traction and safety in cold, snowy, and icy conditions compared to all-season tires.",
        reasoning_framework=(
            "Winter tires use specialized rubber compounds that remain flexible at low temperatures, enhancing grip on cold pavement. "
            "Their tread designs include deeper grooves and siping to channel snow and slush and improve traction on ice. "
            "All-season tires are designed for moderate climates and compromise between summer and winter performance. "
            "The reasoning includes material science of rubber compounds, tread pattern engineering, and performance testing under varied conditions. "
            "Empirical data from braking distance tests and handling evaluations consistently show winter tires outperform all-season tires below 7°C (45°F). "
            "Safety organizations recommend winter tires in regions with prolonged cold weather and snow."
        ),
        key_factors=["rubber compound", "tread design", "temperature", "road conditions", "traction"],
        primary_authority=["Rubber Manufacturers Association", "National Safety Council Winter Driving Guidelines", "Tire Industry Association Seasonal Tire Reports"],
        burden_holder="Vehicle Owner",
        adversary_position="Some claim all-season tires are sufficient year-round for convenience.",
        counter_arguments=[
            "All-season tires lose significant traction in winter conditions, increasing accident risk.",
            "Winter tires improve control and reduce stopping distances in cold weather."
        ],
        resolution_strategy="Use winter tires in cold climates and switch to all-season or summer tires when temperatures rise consistently.",
        entity_scope="Passenger vehicles in seasonal climates",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="National Safety Council Winter Tire Safety Bulletin, 2021"
    ),
    DoctrineBlock(
        topic="Tire Pressure Monitoring System (TPMS) Function and Limitations",
        keywords=["TPMS", "tire pressure", "sensor accuracy", "warning thresholds", "system limitations"],
        conclusion_template="TPMS provides critical real-time tire pressure monitoring but has limitations including sensor accuracy, delayed warnings, and inability to detect gradual leaks.",
        reasoning_framework=(
            "TPMS uses pressure sensors mounted inside tires to monitor inflation and alert drivers to underinflation. "
            "While effective for rapid pressure loss, TPMS systems have inherent limitations such as sensor drift, battery life constraints, "
            "and threshold settings that may delay warnings until pressure is significantly low. "
            "Gradual leaks or slow pressure loss may not trigger immediate alerts, potentially leading to unsafe conditions. "
            "The reasoning includes sensor technology analysis, system design trade-offs, and field performance studies. "
            "Understanding these limitations is essential for proper tire maintenance and driver awareness."
        ),
        key_factors=["sensor accuracy", "warning thresholds", "leak detection", "driver response"],
        primary_authority=["National Highway Traffic Safety Administration (NHTSA) TPMS Regulations", "Tire Industry Association TPMS Technical Papers"],
        burden_holder="Vehicle Manufacturer and Driver",
        adversary_position="Some over-rely on TPMS and neglect manual pressure checks.",
        counter_arguments=[
            "TPMS is a supplement, not a replacement for regular manual tire pressure inspections.",
            "Driver education on TPMS limitations is necessary."
        ],
        resolution_strategy="Combine TPMS alerts with routine manual pressure checks and visual tire inspections.",
        entity_scope="Passenger vehicles equipped with TPMS",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NHTSA TPMS Final Rule and Guidance, 2019"
    ),
    DoctrineBlock(
        topic="Sidewall Impact Damage and Bubble Formation",
        keywords=["sidewall damage", "impact bubbles", "tire integrity", "road hazards", "safety risks"],
        conclusion_template="Sidewall impact damage causing bubble formation compromises tire structural integrity and necessitates immediate replacement.",
        reasoning_framework=(
            "Sidewall bubbles form when the internal tire cords are damaged by impacts such as potholes or curbs, allowing air to seep "
            "between the layers and create bulges. These bubbles weaken the tire's structural integrity and increase the risk of sudden failure. "
            "The reasoning involves understanding tire carcass construction, impact mechanics, and failure modes. "
            "Visual inspection and non-destructive testing confirm bubble presence and severity. Safety standards prohibit continued use of tires "
            "with sidewall bubbles due to catastrophic failure potential."
        ),
        key_factors=["impact severity", "bubble size", "tire construction", "inspection methods"],
        primary_authority=["Tire and Rim Association Safety Standards", "National Highway Traffic Safety Administration (NHTSA) Advisories"],
        burden_holder="Vehicle Owner and Maintenance Personnel",
        adversary_position="Some attempt to repair or continue using tires with bubbles.",
        counter_arguments=[
            "Repairs cannot restore structural integrity in sidewall bubble areas.",
            "Continued use risks blowouts and accidents."
        ],
        resolution_strategy="Immediately replace tires exhibiting sidewall bubbles and inspect for impact damage regularly.",
        entity_scope="All pneumatic tires",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Tire and Rim Association Bulletin 117, 2020"
    ),
    DoctrineBlock(
        topic="Hydroplaning Dynamics and Tread Depth Requirements",
        keywords=["hydroplaning", "tread depth", "water evacuation", "tire safety", "wet traction"],
        conclusion_template="Adequate tread depth is essential to prevent hydroplaning by ensuring effective water evacuation and maintaining wet traction.",
        reasoning_framework=(
            "Hydroplaning occurs when a tire loses contact with the road surface due to a layer of water, leading to loss of traction and control. "
            "Tread grooves channel water away from the contact patch, and sufficient tread depth is critical to maintain this function. "
            "As tread depth decreases, the tire's ability to evacuate water diminishes, increasing hydroplaning risk. "
            "The reasoning includes fluid dynamics of water displacement, tread design analysis, and empirical braking and handling tests on wet surfaces. "
            "Safety standards specify minimum tread depths to mitigate hydroplaning hazards. Regular tread depth measurement and replacement are necessary."
        ),
        key_factors=["tread depth", "groove design", "water depth", "vehicle speed"],
        primary_authority=["National Highway Traffic Safety Administration (NHTSA) Wet Weather Safety Guidelines", "Tire Industry Association Tread Depth Standards"],
        burden_holder="Vehicle Owner",
        adversary_position="Some drivers neglect tread depth and overestimate tire wet performance.",
        counter_arguments=[
            "Reduced tread depth significantly increases stopping distances and hydroplaning risk.",
            "Manufacturer and regulatory minimums are based on safety data."
        ],
        resolution_strategy="Monitor tread depth regularly and replace tires before reaching minimum safe limits.",
        entity_scope="All road tires",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NHTSA Hydroplaning Risk Study, 2018"
    ),
    DoctrineBlock(
        topic="Tire Age and Date Code Interpretation",
        keywords=["tire age", "DOT date code", "rubber degradation", "safety", "service life"],
        conclusion_template="Tire age, as indicated by the DOT date code, is a critical factor in assessing safety due to rubber compound degradation over time.",
        reasoning_framework=(
            "Tire rubber compounds degrade chemically over time due to oxidation, UV exposure, and environmental factors, reducing performance and safety. "
            "The DOT date code on the tire sidewall indicates the week and year of manufacture, enabling age determination. "
            "Industry and regulatory guidelines recommend tire replacement after a certain age, typically six to ten years, regardless of tread wear. "
            "The reasoning includes chemical aging studies, failure analysis, and safety incident data. Visual inspection alone cannot reliably detect age-related degradation."
        ),
        key_factors=["DOT date code", "rubber aging", "environmental exposure", "manufacturer recommendations"],
        primary_authority=["Rubber Manufacturers Association Guidelines", "National Highway Traffic Safety Administration (NHTSA) Advisories"],
        burden_holder="Vehicle Owner",
        adversary_position="Some argue that tread wear is sufficient to determine tire replacement.",
        counter_arguments=[
            "Aged tires with adequate tread can still fail due to compound degradation.",
            "Date code provides objective age information."
        ],
        resolution_strategy="Check DOT date codes and replace tires exceeding recommended service life.",
        entity_scope="All pneumatic tires",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="RMA Tire Aging Safety Bulletin, 2019"
    ),
    DoctrineBlock(
        topic="Run-Flat Tire Technology and Limitations",
        keywords=["run-flat tires", "sidewall reinforcement", "temporary mobility", "limitations", "safety"],
        conclusion_template="Run-flat tires enable limited continued driving after pressure loss but have limitations including reduced ride comfort and limited distance and speed.",
        reasoning_framework=(
            "Run-flat tires incorporate reinforced sidewalls or internal support rings to maintain shape and load-bearing capacity after air loss. "
            "This technology allows drivers to continue driving for a limited distance (typically 50 miles) at reduced speeds (usually up to 50 mph) to reach repair facilities. "
            "However, run-flat tires have stiffer sidewalls, resulting in reduced ride comfort and increased rolling resistance. "
            "The reasoning involves material engineering, structural analysis, and performance testing under deflated conditions. "
            "Limitations include incompatibility with some vehicles, higher replacement costs, and the need for TPMS to monitor pressure."
        ),
        key_factors=["sidewall reinforcement", "mobility distance", "speed limits", "ride comfort", "TPMS integration"],
        primary_authority=["Tire and Rim Association Run-Flat Standards", "Vehicle Manufacturer Run-Flat Guidelines"],
        burden_holder="Vehicle Manufacturer and Owner",
        adversary_position="Some drivers misunderstand run-flat capabilities and overextend use.",
        counter_arguments=[
            "Exceeding run-flat limits risks tire failure and loss of control.",
            "Proper driver education and TPMS monitoring are essential."
        ],
        resolution_strategy="Adhere to manufacturer run-flat usage guidelines and monitor tire pressure continuously.",
        entity_scope="Passenger vehicles equipped with run-flat tires",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="TRA Run-Flat Tire Usage Bulletin, 2020"
    ),
    DoctrineBlock(
        topic="Wheel Balance and Vibration Diagnosis",
        keywords=["wheel balance", "vibration", "tire wear", "dynamic balancing", "diagnostic procedures"],
        conclusion_template="Proper wheel balance is essential to prevent vibration-induced tire wear and maintain vehicle stability.",
        reasoning_framework=(
            "Wheel imbalance causes uneven distribution of mass around the wheel-tire assembly, leading to vibrations felt in the steering wheel, seat, or floorboard. "
            "These vibrations accelerate uneven tire wear, reduce ride comfort, and may cause premature suspension wear. "
            "Dynamic balancing procedures measure and correct imbalance by adding weights to the wheel. "
            "Diagnosis involves vibration analysis at various speeds and inspection of tire wear patterns. "
            "The reasoning includes mechanical dynamics, rotational inertia, and empirical testing. "
            "Regular balancing is critical after tire installation or repair."
        ),
        key_factors=["mass distribution", "vibration frequency", "tire wear pattern", "balancing procedures"],
        primary_authority=["SAE J2530 Wheel Balance Standards", "Automotive Service Excellence (ASE) Guidelines"],
        burden_holder="Service Technician",
        adversary_position="Some neglect wheel balancing due to cost or time.",
        counter_arguments=[
            "Ignoring imbalance leads to accelerated tire and suspension damage.",
            "Balancing improves safety and ride quality."
        ],
        resolution_strategy="Perform wheel balancing at tire installation and when vibration symptoms appear.",
        entity_scope="All road vehicle tires",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASE Wheel Balance and Vibration Diagnostic Manual, 2021"
    ),
    DoctrineBlock(
        topic="Nitrogen Inflation vs Compressed Air",
        keywords=["nitrogen inflation", "compressed air", "tire pressure stability", "moisture content", "oxidation"],
        conclusion_template="Nitrogen inflation offers improved pressure stability and reduced oxidation compared to compressed air but requires proper handling to realize benefits.",
        reasoning_framework=(
            "Nitrogen molecules are larger and less permeable than oxygen, reducing pressure loss over time. "
            "Nitrogen inflation reduces moisture content inside tires, minimizing corrosion of steel belts and oxidation of rubber compounds. "
            "Compressed air contains moisture and oxygen, which can accelerate tire aging and pressure fluctuations. "
            "The reasoning includes gas permeability studies, chemical aging analysis, and field performance comparisons. "
            "However, benefits depend on proper nitrogen purity and maintenance. The cost-benefit ratio varies by application."
        ),
        key_factors=["gas permeability", "moisture content", "oxidation rate", "pressure retention"],
        primary_authority=["Rubber Manufacturers Association Technical Papers", "Tire Industry Association Inflation Guidelines"],
        burden_holder="Service Provider and Vehicle Owner",
        adversary_position="Some claim nitrogen inflation offers negligible benefits over air.",
        counter_arguments=[
            "Scientific studies demonstrate measurable improvements in pressure retention and tire longevity.",
            "Proper nitrogen inflation protocols are essential to achieve benefits."
        ],
        resolution_strategy="Use nitrogen inflation where justified and maintain proper inflation regardless of gas type.",
        entity_scope="Passenger and commercial vehicle tires",
        confidence=0.88,
        confidence_zone="Moderate to High",
        controlling_precedent="RMA Nitrogen Inflation Study, 2019"
    ),
    DoctrineBlock(
        topic="Tire Rotation Patterns and Intervals",
        keywords=["tire rotation", "wear uniformity", "rotation patterns", "intervals", "tire longevity"],
        conclusion_template="Regular tire rotation using manufacturer-recommended patterns and intervals promotes uniform wear and extends tire service life.",
        reasoning_framework=(
            "Tire rotation redistributes wear by periodically changing tire positions on the vehicle, compensating for differences in load, drive configuration, and alignment. "
            "Common rotation patterns include front-to-rear, cross, and directional rotations, selected based on tire type and vehicle drivetrain. "
            "Intervals typically range from 5,000 to 8,000 miles, balancing wear mitigation and maintenance cost. "
            "The reasoning involves wear pattern analysis, vehicle dynamics, and empirical service data. "
            "Proper rotation reduces premature tire replacement and maintains consistent handling characteristics."
        ),
        key_factors=["vehicle drivetrain", "tire type", "wear patterns", "rotation interval"],
        primary_authority=["Tire Industry Association Maintenance Guidelines", "Vehicle Manufacturer Service Manuals"],
        burden_holder="Vehicle Owner and Maintenance Personnel",
        adversary_position="Some skip rotations due to inconvenience or cost.",
        counter_arguments=[
            "Skipping rotations accelerates uneven wear and increases replacement frequency.",
            "Rotation is a cost-effective maintenance practice."
        ],
        resolution_strategy="Follow manufacturer rotation schedules and patterns for specific vehicle and tire types.",
        entity_scope="Passenger and light truck tires",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="TIA Tire Rotation Best Practices Guide, 2020"
    ),
    DoctrineBlock(
        topic="Plus-Sizing and Minus-Sizing Tire Changes",
        keywords=["plus-sizing", "minus-sizing", "tire size", "wheel diameter", "vehicle handling", "speedometer accuracy"],
        conclusion_template="Plus-sizing and minus-sizing tire changes affect vehicle handling, speedometer accuracy, and suspension dynamics and must comply with manufacturer guidelines.",
        reasoning_framework=(
            "Plus-sizing involves increasing tire diameter and wheel size to improve handling and aesthetics, while minus-sizing reduces them for ride comfort or cost. "
            "Changes affect overall tire circumference, altering speedometer readings and gear ratios. "
            "Handling characteristics change due to sidewall height and tire stiffness variations. "
            "The reasoning includes mechanical analysis of tire geometry, vehicle dynamics, and regulatory compliance. "
            "Improper sizing can cause clearance issues, increased wear, and safety risks. "
            "Manufacturer guidelines specify acceptable size ranges and recommend recalibration of speedometers."
        ),
        key_factors=["tire diameter", "wheel size", "sidewall height", "vehicle clearance", "speedometer calibration"],
        primary_authority=["Vehicle Manufacturer Specifications", "Tire and Rim Association Sizing Standards"],
        burden_holder="Vehicle Owner and Installer",
        adversary_position="Some disregard sizing guidelines for cosmetic reasons.",
        counter_arguments=[
            "Non-compliant sizing compromises safety and vehicle performance.",
            "Regulatory bodies may impose penalties for non-compliance."
        ],
        resolution_strategy="Consult manufacturer sizing charts and perform necessary recalibrations when changing tire sizes.",
        entity_scope="Passenger vehicles",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="TRA Tire Sizing and Vehicle Compatibility Bulletin, 2019"
    ),
    DoctrineBlock(
        topic="Tire Tread Compound Variations and Performance",
        keywords=["tread compound", "rubber formulation", "performance trade-offs", "wear resistance", "traction"],
        conclusion_template="Tire tread compound formulations balance wear resistance and traction, with softer compounds providing better grip but reduced durability.",
        reasoning_framework=(
            "Tread compounds are engineered blends of natural and synthetic rubbers, fillers, and additives tailored for specific performance characteristics. "
            "Softer compounds improve traction by conforming to road surfaces but wear faster due to lower abrasion resistance. "
            "Harder compounds extend tread life but may reduce grip, especially in wet or cold conditions. "
            "The reasoning involves polymer chemistry, material science, and performance testing under varied conditions. "
            "Manufacturers select compounds based on intended tire use, balancing safety, longevity, and cost."
        ),
        key_factors=["rubber hardness", "abrasion resistance", "traction", "temperature sensitivity"],
        primary_authority=["Rubber Manufacturers Association Technical Papers", "Tire Industry Association Compound Standards"],
        burden_holder="Tire Manufacturer",
        adversary_position="Some consumers prioritize longevity over traction, risking safety.",
        counter_arguments=[
            "Compromising traction for wear can increase accident risk.",
            "Compound selection must consider intended use and conditions."
        ],
        resolution_strategy="Match tire compound to vehicle use and environmental conditions for optimal performance.",
        entity_scope="All tire types",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="RMA Tread Compound Performance Study, 2020"
    ),
    DoctrineBlock(
        topic="Tire Sidewall Markings and Interpretation",
        keywords=["sidewall markings", "DOT code", "load index", "speed rating", "manufacture date"],
        conclusion_template="Tire sidewall markings provide essential information for compliance, safety, and maintenance decisions.",
        reasoning_framework=(
            "Sidewall markings include DOT codes indicating manufacture date and plant, load index, speed rating, maximum inflation pressure, and size. "
            "Interpreting these markings is critical for verifying tire suitability, age, and regulatory compliance. "
            "The reasoning involves understanding standardized marking formats, regulatory requirements, and manufacturer specifications. "
            "Proper interpretation aids in maintenance, replacement decisions, and safety inspections."
        ),
        key_factors=["DOT code", "load index", "speed rating", "size designation"],
        primary_authority=["Department of Transportation (DOT) Regulations", "Tire and Rim Association Marking Standards"],
        burden_holder="Vehicle Owner and Service Personnel",
        adversary_position="Some users ignore or misinterpret markings, leading to improper tire use.",
        counter_arguments=[
            "Misinterpretation can cause safety risks and regulatory violations.",
            "Education on markings improves tire management."
        ],
        resolution_strategy="Train personnel and educate consumers on sidewall marking interpretation.",
        entity_scope="All pneumatic tires",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="DOT Tire Marking Compliance Bulletin, 2021"
    ),
    DoctrineBlock(
        topic="Tire Inflation Pressure Effects on Fuel Efficiency",
        keywords=["inflation pressure", "fuel efficiency", "rolling resistance", "tire wear"],
        conclusion_template="Maintaining proper tire inflation pressure reduces rolling resistance, improving fuel efficiency and tire wear.",
        reasoning_framework=(
            "Underinflated tires increase rolling resistance by enlarging the contact patch and causing greater deformation during rotation. "
            "This requires more engine power to maintain speed, increasing fuel consumption. "
            "Proper inflation maintains optimal tire shape, minimizing energy loss. "
            "The reasoning includes mechanical energy analysis, vehicle dynamics, and empirical fuel economy testing. "
            "Maintaining recommended pressures also promotes even tread wear, extending tire life."
        ),
        key_factors=["inflation pressure", "rolling resistance", "fuel consumption", "tread wear"],
        primary_authority=["U.S. Department of Energy Fuel Economy Guides", "Tire Industry Association Efficiency Studies"],
        burden_holder="Vehicle Owner",
        adversary_position="Some neglect tire pressure maintenance due to inconvenience.",
        counter_arguments=[
            "Neglecting pressure leads to increased fuel costs and tire replacement frequency.",
            "Regular checks are simple and cost-effective."
        ],
        resolution_strategy="Perform monthly tire pressure checks and maintain manufacturer-recommended levels.",
        entity_scope="All road vehicles",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="DOE Fuel Economy and Tire Pressure Study, 2019"
    ),
    DoctrineBlock(
        topic="Tire Noise Generation and Mitigation",
        keywords=["tire noise", "tread pattern", "road interaction", "noise reduction technologies"],
        conclusion_template="Tire noise is generated by tread pattern and road interaction and can be mitigated through design optimizations and materials.",
        reasoning_framework=(
            "Tire noise arises from air compression in tread grooves, tread block impact, and vibration transmission. "
            "Tread pattern design, including pitch variation and groove shape, influences noise frequency and amplitude. "
            "Materials such as sound-absorbing layers and optimized rubber compounds reduce noise generation. "
            "The reasoning includes acoustical engineering, material science, and field noise measurements. "
            "Manufacturers balance noise reduction with traction and wear performance."
        ),
        key_factors=["tread design", "material properties", "road surface", "vibration damping"],
        primary_authority=["Tire Industry Association Noise Standards", "SAE Tire Noise Engineering Papers"],
        burden_holder="Tire Manufacturer",
        adversary_position="Some prioritize traction over noise, accepting higher noise levels.",
        counter_arguments=[
            "Excessive noise reduces driver comfort and may violate regulations.",
            "Modern designs achieve balance between noise and performance."
        ],
        resolution_strategy="Incorporate noise reduction features in tire design and validate with testing.",
        entity_scope="All tire types",
        confidence=0.90,
        confidence_zone="Moderate to High",
        controlling_precedent="TIA Tire Noise Reduction Guidelines, 2020"
    ),
    DoctrineBlock(
        topic="Tire Storage and Shelf Life",
        keywords=["tire storage", "shelf life", "environmental conditions", "rubber degradation"],
        conclusion_template="Proper tire storage under controlled environmental conditions extends shelf life and preserves tire integrity.",
        reasoning_framework=(
            "Tires stored improperly are exposed to UV light, ozone, temperature extremes, and humidity, accelerating rubber degradation. "
            "Ideal storage involves cool, dry, dark environments with tires kept off the ground and away from chemicals. "
            "The reasoning includes chemical aging mechanisms, environmental impact studies, and industry best practices. "
            "Proper storage preserves physical properties and safety performance, reducing premature failures."
        ),
        key_factors=["temperature", "humidity", "UV exposure", "chemical exposure", "storage position"],
        primary_authority=["Rubber Manufacturers Association Storage Guidelines", "Tire Industry Association Best Practices"],
        burden_holder="Distributor and Retailer",
        adversary_position="Some neglect storage conditions to reduce costs.",
        counter_arguments=[
            "Poor storage leads to early tire failure and liability.",
            "Investment in proper storage reduces long-term costs."
        ],
        resolution_strategy="Implement and monitor storage protocols consistent with industry guidelines.",
        entity_scope="New and unused tires",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="RMA Tire Storage and Handling Bulletin, 2018"
    ),
    DoctrineBlock(
        topic="Effect of Wheel Alignment on Tire Wear",
        keywords=["wheel alignment", "toe", "camber", "caster", "tire wear patterns"],
        conclusion_template="Proper wheel alignment minimizes uneven tire wear and maintains vehicle handling stability.",
        reasoning_framework=(
            "Wheel alignment parameters—toe, camber, and caster—determine tire contact angles with the road. "
            "Misalignment causes uneven load distribution, leading to accelerated wear on specific tread areas such as shoulders or edges. "
            "Alignment affects steering response and vehicle stability. "
            "The reasoning involves geometric analysis of wheel angles, load transfer, and wear mechanics. "
            "Regular alignment checks and corrections prevent premature tire replacement and improve safety."
        ),
        key_factors=["toe angle", "camber angle", "caster angle", "wear location", "vehicle handling"],
        primary_authority=["SAE J2530 Alignment Standards", "Automotive Service Excellence (ASE) Guidelines"],
        burden_holder="Service Technician",
        adversary_position="Some delay alignment due to cost or lack of symptoms.",
        counter_arguments=[
            "Ignoring misalignment causes costly tire damage and unsafe handling.",
            "Preventive alignment is cost-effective."
        ],
        resolution_strategy="Perform alignment checks at regular intervals and after suspension repairs.",
        entity_scope="All road vehicles",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="ASE Wheel Alignment and Tire Wear Manual, 2021"
    ),
    DoctrineBlock(
        topic="Tire Sidewall Bulge vs Cut Damage",
        keywords=["sidewall bulge", "sidewall cut", "tire damage", "safety risk", "inspection"],
        conclusion_template="Sidewall bulges indicate internal structural damage requiring tire replacement, whereas cuts may be repairable depending on size and location.",
        reasoning_framework=(
            "Sidewall bulges result from internal cord breakage causing air to separate layers, compromising tire integrity. "
            "Cuts are external damages that may or may not penetrate structural layers. "
            "Safety assessment depends on damage size, depth, and location. "
            "Bulges always necessitate replacement due to failure risk. "
            "Cuts in the tread area may be repairable if shallow and small, but sidewall cuts are generally non-repairable. "
            "The reasoning includes structural analysis, safety standards, and repair guidelines."
        ),
        key_factors=["damage type", "location", "size", "depth", "repairability"],
        primary_authority=["Tire and Rim Association Repair Guidelines", "National Highway Traffic Safety Administration (NHTSA) Advisories"],
        burden_holder="Service Technician",
        adversary_position="Some attempt to repair bulges or unsafe cuts.",
        counter_arguments=[
            "Repairing bulges risks catastrophic failure.",
            "Sidewall cuts compromise structural integrity."
        ],
        resolution_strategy="Replace tires with bulges or sidewall cuts; repair tread cuts per guidelines.",
        entity_scope="All pneumatic tires",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="TRA Tire Damage and Repair Bulletin, 2020"
    ),
    DoctrineBlock(
        topic="Effect of Tire Inflation on Handling and Braking",
        keywords=["inflation pressure", "handling", "braking distance", "vehicle safety"],
        conclusion_template="Maintaining correct tire inflation pressure is critical for optimal vehicle handling and minimizing braking distances.",
        reasoning_framework=(
            "Underinflated tires increase rolling resistance and reduce tread contact uniformity, degrading handling responsiveness and increasing braking distances. "
            "Overinflated tires reduce contact patch size, decreasing traction and stability. "
            "Proper inflation ensures maximum tire-road contact and predictable vehicle dynamics. "
            "The reasoning involves tire mechanics, frictional force analysis, and vehicle dynamics modeling. "
            "Empirical testing confirms the relationship between inflation and safety performance."
        ),
        key_factors=["inflation pressure", "contact patch", "traction", "vehicle dynamics"],
        primary_authority=["National Highway Traffic Safety Administration (NHTSA) Safety Reports", "Tire Industry Association Handling Studies"],
        burden_holder="Vehicle Owner",
        adversary_position="Some neglect inflation maintenance, risking safety.",
        counter_arguments=[
            "Incorrect inflation directly compromises vehicle control and safety.",
            "Regular pressure checks are essential."
        ],
        resolution_strategy="Maintain manufacturer-recommended tire pressures and inspect regularly.",
        entity_scope="All road vehicles",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NHTSA Tire Inflation and Safety Study, 2019"
    ),
    DoctrineBlock(
        topic="Tire Balancing Weight Placement Techniques",
        keywords=["balancing weights", "dynamic balancing", "static balancing", "weight placement", "vibration reduction"],
        conclusion_template="Correct placement of balancing weights during dynamic balancing minimizes vibrations and uneven tire wear.",
        reasoning_framework=(
            "Dynamic balancing involves measuring imbalance in two planes and placing weights on the wheel rim to counteract forces. "
            "Static balancing addresses imbalance in a single plane. "
            "Proper weight placement requires understanding wheel geometry and rotational dynamics. "
            "Incorrect placement can exacerbate vibrations or cause new imbalances. "
            "The reasoning includes physics of rotating bodies, vibration analysis, and balancing machine calibration. "
            "Technician skill and equipment accuracy are critical."
        ),
        key_factors=["weight amount", "placement location", "balancing method", "equipment calibration"],
        primary_authority=["SAE J2530 Wheel Balancing Standards", "Automotive Service Excellence (ASE) Guidelines"],
        burden_holder="Service Technician",
        adversary_position="Some technicians use improper techniques leading to ineffective balancing.",
        counter_arguments=[
            "Poor balancing increases wear and reduces ride comfort.",
            "Training and equipment maintenance improve outcomes."
        ],
        resolution_strategy="Use calibrated equipment and follow standardized procedures for weight placement.",
        entity_scope="All road vehicle wheels",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ASE Wheel Balancing Procedures Manual, 2021"
    ),
    DoctrineBlock(
        topic="Impact of Tread Depth on Tire Noise and Comfort",
        keywords=["tread depth", "noise", "ride comfort", "tread pattern", "vibration"],
        conclusion_template="Reduced tread depth can increase tire noise and reduce ride comfort due to changes in tread pattern and stiffness.",
        reasoning_framework=(
            "As tread wears down, the geometry and flexibility of tread blocks change, affecting noise generation and vibration transmission. "
            "Shallower tread depth reduces the ability to absorb road irregularities, increasing harshness. "
            "The reasoning involves acoustical engineering, material deformation analysis, and ride quality testing. "
            "Manufacturers design tread patterns to optimize noise and comfort at specified depths."
        ),
        key_factors=["tread depth", "tread pattern", "material stiffness", "road surface"],
        primary_authority=["Tire Industry Association Noise and Comfort Studies", "SAE Tire Engineering Papers"],
        burden_holder="Vehicle Owner",
        adversary_position="Some ignore noise increases as normal wear.",
        counter_arguments=[
            "Excessive noise may indicate uneven wear or damage.",
            "Maintaining proper tread depth improves comfort."
        ],
        resolution_strategy="Monitor tread depth and replace tires before noise and comfort degrade significantly.",
        entity_scope="Passenger vehicle tires",
        confidence=0.89,
        confidence_zone="Moderate to High",
        controlling_precedent="TIA Tire Noise and Comfort Report, 2019"
    ),
    DoctrineBlock(
        topic="Effectiveness of Tire Sealants and Repair Products",
        keywords=["tire sealants", "puncture repair", "temporary fix", "limitations", "safety"],
        conclusion_template="Tire sealants provide temporary puncture repairs but are not substitutes for professional inspection and permanent repair.",
        reasoning_framework=(
            "Sealants can temporarily plug small punctures in the tread area by filling holes and preventing air loss. "
            "They are not effective for sidewall damage or large punctures. "
            "Sealants may interfere with tire pressure sensors and complicate professional repairs. "
            "The reasoning includes chemical compatibility, mechanical sealing effectiveness, and safety considerations. "
            "Manufacturers recommend sealants only as emergency measures."
        ),
        key_factors=["puncture size", "location", "sealant composition", "sensor compatibility"],
        primary_authority=["Tire and Rim Association Repair Guidelines", "Tire Industry Association Sealant Studies"],
        burden_holder="Vehicle Owner and Service Technician",
        adversary_position="Some rely solely on sealants without professional follow-up.",
        counter_arguments=[
            "Sealants do not restore structural integrity.",
            "Professional inspection is necessary to ensure safety."
        ],
        resolution_strategy="Use sealants only for temporary fixes and seek professional repair promptly.",
        entity_scope="Passenger vehicle tires",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="TRA Tire Sealant Usage Bulletin, 2020"
    ),
    DoctrineBlock(
        topic="Run-Flat Tire Repairability Guidelines",
        keywords=["run-flat tires", "repair guidelines", "sidewall damage", "manufacturer recommendations"],
        conclusion_template="Run-flat tires should only be repaired per manufacturer guidelines, typically prohibiting sidewall repairs.",
        reasoning_framework=(
            "Run-flat tires have reinforced sidewalls critical to their function. Damage to these areas compromises safety. "
            "Manufacturers generally prohibit repairs to sidewalls and recommend replacement if damaged. "
            "Tread area repairs may be allowed if meeting standard criteria. "
            "The reasoning involves structural integrity analysis and safety risk assessment. "
            "Adherence to guidelines prevents failures and liability."
        ),
        key_factors=["damage location", "repair method", "manufacturer policies"],
        primary_authority=["Run-Flat Tire Manufacturers' Repair Manuals", "Tire and Rim Association Repair Standards"],
        burden_holder="Service Technician",
        adversary_position="Some attempt unauthorized repairs on run-flat tires.",
        counter_arguments=[
            "Unauthorized repairs increase failure risk.",
            "Compliance with guidelines ensures safety."
        ],
        resolution_strategy="Follow manufacturer repair policies strictly and replace non-repairable run-flat tires.",
        entity_scope="Run-flat tires",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Run-Flat Tire Repair Policy Bulletin, 2021"
    ),
    DoctrineBlock(
        topic="Tire Pressure Effects on Tire Temperature and Wear",
        keywords=["tire pressure", "temperature", "wear rate", "heat buildup"],
        conclusion_template="Incorrect tire pressure leads to abnormal temperature rise, accelerating tire wear and increasing failure risk.",
        reasoning_framework=(
            "Underinflated tires flex excessively, generating heat due to internal friction and deformation. "
            "Overinflated tires have reduced contact area, causing uneven wear and localized heating. "
            "Excess heat degrades rubber compounds and structural components, shortening tire life. "
            "The reasoning involves thermodynamics, material degradation kinetics, and wear mechanics. "
            "Maintaining correct pressure minimizes heat buildup and wear."
        ),
        key_factors=["inflation pressure", "heat generation", "wear patterns", "material degradation"],
        primary_authority=["Tire Industry Association Thermal Studies", "National Highway Traffic Safety Administration (NHTSA) Reports"],
        burden_holder="Vehicle Owner",
        adversary_position="Some neglect pressure maintenance, risking heat-related failures.",
        counter_arguments=[
            "Heat-induced failures are preventable with proper inflation.",
            "Regular pressure checks reduce risk."
        ],
        resolution_strategy="Maintain recommended tire pressures and monitor for abnormal temperature signs.",
        entity_scope="All pneumatic tires",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="TIA Tire Thermal and Wear Study, 2019"
    ),
    DoctrineBlock(
        topic="Effect of Tire Width on Vehicle Dynamics",
        keywords=["tire width", "handling", "traction", "fuel economy", "ride comfort"],
        conclusion_template="Increasing tire width improves traction and handling but may reduce fuel economy and ride comfort.",
        reasoning_framework=(
            "Wider tires increase the contact patch, enhancing grip and cornering stability. "
            "However, they increase rolling resistance and aerodynamic drag, reducing fuel efficiency. "
            "Wider tires also have stiffer sidewalls, potentially decreasing ride comfort. "
            "The reasoning involves vehicle dynamics, fluid mechanics, and material stiffness analysis. "
            "Trade-offs must be balanced based on vehicle use and driver preferences."
        ),
        key_factors=["contact patch size", "rolling resistance", "aerodynamics", "sidewall stiffness"],
        primary_authority=["SAE Vehicle Dynamics Papers", "Tire Industry Association Performance Studies"],
        burden_holder="Vehicle Owner",
        adversary_position="Some prioritize appearance over performance trade-offs.",
        counter_arguments=[
            "Ignoring trade-offs can lead to increased operating costs and discomfort.",
            "Informed decisions optimize overall vehicle performance."
        ],
        resolution_strategy="Select tire width balancing handling benefits with fuel economy and comfort considerations.",
        entity_scope="Passenger vehicles",
        confidence=0.90,
        confidence_zone="Moderate to High",
        controlling_precedent="TIA Tire Width and Vehicle Dynamics Report, 2020"
    ),
    DoctrineBlock(
        topic="Tire Bead Seating and Installation Best Practices",
        keywords=["tire bead", "installation", "seating", "rim compatibility", "safety"],
        conclusion_template="Proper tire bead seating during installation ensures airtight seal and prevents tire failure.",
        reasoning_framework=(
            "The tire bead interfaces with the wheel rim to create an airtight seal essential for maintaining inflation. "
            "Improper seating can cause leaks, bead damage, or sudden deflation. "
            "Installation requires matching tire and rim sizes, clean bead and rim surfaces, and correct mounting techniques. "
            "The reasoning includes mechanical fit analysis, seal integrity, and failure mode studies. "
            "Following best practices reduces installation-related failures and safety risks."
        ),
        key_factors=["bead size", "rim condition", "mounting technique", "seal integrity"],
        primary_authority=["Tire and Rim Association Installation Guidelines", "Automotive Service Excellence (ASE) Manuals"],
        burden_holder="Service Technician",
        adversary_position="Some use improper tools or techniques risking bead damage.",
        counter_arguments=[
            "Improper installation leads to leaks and potential blowouts.",
            "Training and equipment maintenance are essential."
        ],
        resolution_strategy="Adhere to manufacturer and industry installation procedures and inspect bead and rim condition.",
        entity_scope="All pneumatic tires",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="TRA Tire Installation Safety Bulletin, 2021"
    ),
    DoctrineBlock(
        topic="Tire Sidewall Flexibility and Ride Quality",
        keywords=["sidewall flexibility", "ride comfort", "handling", "tire construction"],
        conclusion_template="Sidewall flexibility influences ride comfort and handling, with softer sidewalls improving comfort but potentially reducing handling precision.",
        reasoning_framework=(
            "Flexible sidewalls absorb road irregularities, enhancing ride comfort by reducing transmitted vibrations. "
            "However, excessive flexibility can reduce steering responsiveness and increase sidewall deformation during cornering. "
            "Tire construction balances sidewall stiffness and flexibility using materials and design. "
            "The reasoning involves material mechanics, vehicle dynamics, and comfort testing. "
            "Selection depends on vehicle type and driver preferences."
        ),
        key_factors=["sidewall material", "stiffness", "vehicle dynamics", "ride comfort"],
        primary_authority=["Rubber Manufacturers Association Technical Papers", "SAE Vehicle Dynamics Studies"],
        burden_holder="Tire Manufacturer",
        adversary_position="Some prioritize handling over comfort or vice versa without balance.",
        counter_arguments=[
            "Ignoring balance leads to suboptimal vehicle performance.",
            "Design optimization achieves desired trade-offs."
        ],
        resolution_strategy="Design tires with sidewall properties matching intended vehicle use and customer expectations.",
        entity_scope="Passenger vehicle tires",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="RMA Sidewall Flexibility and Performance Report, 2019"
    ),
    DoctrineBlock(
        topic="Tire Tread Pattern Effects on Off-Road Performance",
        keywords=["tread pattern", "off-road tires", "traction", "self-cleaning", "durability"],
        conclusion_template="Aggressive tread patterns with deep lugs and self-cleaning features enhance off-road traction and durability.",
        reasoning_framework=(
            "Off-road tires feature tread patterns designed to maximize grip on loose surfaces such as mud, sand, and rocks. "
            "Deep lugs provide bite, while self-cleaning patterns eject debris to maintain traction. "
            "Tread compound and construction are optimized for durability against cuts and punctures. "
            "The reasoning involves terrain interaction analysis, material toughness, and field testing. "
            "Proper tread design improves vehicle capability and safety in off-road conditions."
        ),
        key_factors=["lug depth", "pattern design", "compound toughness", "terrain type"],
        primary_authority=["Tire Industry Association Off-Road Tire Standards", "SAE Off-Road Vehicle Engineering Papers"],
        burden_holder="Tire Manufacturer",
        adversary_position="Some use inappropriate tires for off-road conditions risking performance loss.",
        counter_arguments=[
            "Using street tires off-road increases risk of damage and loss of traction.",
            "Specialized tires improve safety and capability."
        ],
        resolution_strategy="Select tires with tread patterns suited to intended off-road use and terrain.",
        entity_scope="Off-road vehicle tires",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="TIA Off-Road Tire Performance Bulletin, 2020"
    ),
    DoctrineBlock(
        topic="Effect of Tire Inflation on Tread Wear Uniformity",
        keywords=["inflation pressure", "tread wear", "uniformity", "underinflation", "overinflation"],
        conclusion_template="Maintaining proper tire inflation pressure promotes uniform tread wear and extends tire life.",
        reasoning_framework=(
            "Underinflation causes increased wear on tire shoulders due to greater flexing and load concentration. "
            "Overinflation causes center tread wear due to reduced contact patch width. "
            "Proper inflation balances load distribution across the tread. "
            "The reasoning involves mechanical load analysis, wear pattern observation, and empirical studies. "
            "Uniform wear reduces premature tire replacement and maintains performance."
        ),
        key_factors=["inflation pressure", "load distribution", "wear location", "tread pattern"],
        primary_authority=["Tire Industry Association Maintenance Guidelines", "National Highway Traffic Safety Administration (NHTSA) Reports"],
        burden_holder="Vehicle Owner",
        adversary_position="Some neglect pressure maintenance leading to uneven wear.",
        counter_arguments=[
            "Uneven wear reduces safety and increases costs.",
            "Regular pressure checks prevent issues."
        ],
        resolution_strategy="Maintain recommended inflation pressures and inspect tires regularly.",
        entity_scope="All pneumatic tires",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NHTSA Tire Wear and Inflation Study, 2019"
    ),
    DoctrineBlock(
        topic="Tire Pressure Loss Detection Methods",
        keywords=["pressure loss", "detection", "TPMS", "manual checks", "leak types"],
        conclusion_template="Combining TPMS with regular manual tire pressure checks provides the most reliable detection of pressure loss.",
        reasoning_framework=(
            "TPMS alerts drivers to rapid pressure loss but may not detect slow leaks or sensor failures. "
            "Manual pressure checks using gauges provide accurate pressure readings independent of sensor status. "
            "Different leak types, such as punctures or valve faults, require varied detection approaches. "
            "The reasoning involves sensor technology limitations, leak mechanics, and maintenance practices. "
            "Combining methods ensures timely detection and correction."
        ),
        key_factors=["TPMS capabilities", "manual gauge accuracy", "leak type", "inspection frequency"],
        primary_authority=["National Highway Traffic Safety Administration (NHTSA) TPMS Guidelines", "Tire Industry Association Maintenance Recommendations"],
        burden_holder="Vehicle Owner",
        adversary_position="Some rely solely on TPMS ignoring manual checks.",
        counter_arguments=[
            "TPMS alone may fail or miss slow leaks.",
            "Manual checks complement electronic systems."
        ],
        resolution_strategy="Perform regular manual pressure checks in addition to monitoring TPMS alerts.",
        entity_scope="Passenger vehicles with TPMS",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NHTSA TPMS and Pressure Check Study, 2020"
    ),
    DoctrineBlock(
        topic="Tire Replacement Criteria Based on Wear Indicators",
        keywords=["wear indicators", "tread depth", "replacement", "safety"],
        conclusion_template="Tires should be replaced when tread wear indicators reach the tread surface to maintain safety and performance.",
        reasoning_framework=(
            "Tread wear indicators are molded bars within tread grooves that become flush with the tread surface at minimum safe depth (typically 2/32 inch). "
            "When indicators are visible, traction, especially on wet roads, is significantly reduced. "
            "Replacement at or before this point prevents hydroplaning and loss of control. "
            "The reasoning includes safety testing, regulatory standards, and accident data analysis."
        ),
        key_factors=["wear indicator visibility", "tread depth", "traction", "regulatory requirements"],
        primary_authority=["Department of Transportation (DOT) Regulations", "Tire Industry Association Safety Guidelines"],
        burden_holder="Vehicle Owner",
        adversary_position="Some delay replacement beyond safe tread depth.",
        counter_arguments=[
            "Worn tires increase accident risk.",
            "Timely replacement enhances safety."
        ],
        resolution_strategy="Inspect wear indicators regularly and replace tires promptly when indicators appear.",
        entity_scope="All pneumatic tires",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="DOT Tire Safety Standards, 2021"
    ),
    DoctrineBlock(
        topic="Tire Inflation Pressure Effects on Load Carrying Capacity",
        keywords=["inflation pressure", "load capacity", "tire safety", "overloading"],
        conclusion_template="Maintaining correct tire inflation pressure is essential to achieve rated load carrying capacity and ensure safety.",
        reasoning_framework=(
            "Tire load capacity depends on internal air pressure supporting the vehicle's weight. "
            "Underinflation reduces effective load capacity, increasing risk of tire failure under load. "
            "Overinflation may increase load capacity slightly but reduces contact patch and traction. "
            "The reasoning involves pneumatic pressure mechanics, structural analysis, and safety testing. "
            "Adhering to manufacturer pressure recommendations ensures rated load capacity."
        ),
        key_factors=["inflation pressure", "vehicle load", "tire rating", "safety margins"],
        primary_authority=["Tire and Rim Association Load and Inflation Standards", "National Highway Traffic Safety Administration (NHTSA) Reports"],
        burden_holder="Vehicle Owner",
        adversary_position="Some overload tires without adjusting pressure.",
        counter_arguments=[
            "Overloading underinflated tires causes failures.",
            "Proper inflation and load management are critical."
        ],
        resolution_strategy="Maintain inflation pressure per load and manufacturer guidelines.",
        entity_scope="All pneumatic tires",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="TRA Load and Inflation Compliance Bulletin, 2020"
    ),
    DoctrineBlock(
        topic="Tire Sidewall Crack Formation and Causes",
        keywords=["sidewall cracks", "aging", "ozone exposure", "UV damage", "maintenance"],
        conclusion_template="Sidewall cracks primarily result from aging, ozone, and UV exposure and indicate tire degradation requiring inspection or replacement.",
        reasoning_framework=(
            "Cracks form as rubber compounds degrade chemically due to oxidation and UV radiation. "
            "Environmental exposure accelerates this process. "
            "Cracking reduces sidewall strength and increases failure risk. "
            "The reasoning includes chemical aging studies, environmental impact analysis, and safety assessments. "
            "Regular inspection detects cracks early, enabling timely replacement."
        ),
        key_factors=["age", "environmental exposure", "rubber compound", "inspection frequency"],
        primary_authority=["Rubber Manufacturers Association Aging Guidelines", "National Highway Traffic Safety Administration (NHTSA) Advisories"],
        burden_holder="Vehicle Owner",
        adversary_position="Some ignore cracks until failure occurs.",
        counter_arguments=[
            "Ignoring cracks risks sudden tire failure.",
            "Proactive inspection improves safety."
        ],
        resolution_strategy="Inspect tires regularly for cracks and replace as necessary.",
        entity_scope="All pneumatic tires",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="RMA Tire Aging and Cracking Bulletin, 2019"
    ),
    DoctrineBlock(
        topic="Effect of Tire Pressure on TPMS Sensor Battery Life",
        keywords=["TPMS", "sensor battery", "pressure monitoring", "battery life", "maintenance"],
        conclusion_template="Maintaining proper tire pressure and minimizing sensor activations prolong TPMS sensor battery life.",
        reasoning_framework=(
            "TPMS sensors have limited battery life, typically 5-10 years, affected by frequency of pressure changes and activations. "
            "Frequent pressure fluctuations or sensor reprogramming reduce battery longevity. "
            "Maintaining correct tire pressure minimizes sensor activations, extending battery life. "
            "The reasoning includes electronic component analysis, power consumption studies, and maintenance data."
        ),
        key_factors=["sensor activations", "pressure stability", "battery capacity", "maintenance practices"],
        primary_authority=["TPMS Manufacturers' Technical Documents", "National Highway Traffic Safety Administration (NHTSA) Guidelines"],
        burden_holder="Vehicle Owner and Service Technician",
        adversary_position="Some neglect pressure maintenance leading to premature sensor failure.",
        counter_arguments=[
            "Neglect increases replacement costs and reduces monitoring effectiveness.",
            "Proper maintenance optimizes sensor life."
        ],
        resolution_strategy="Maintain tire pressure and monitor TPMS sensor status regularly.",
        entity_scope="Vehicles equipped with TPMS",
        confidence=0.90,
        confidence_zone="Moderate to High",
        controlling_precedent="NHTSA TPMS Battery Life Study, 2020"
    ),
    DoctrineBlock(
        topic="Tire Inflation Pressure and Impact on Tire Noise",
        keywords=["inflation pressure", "tire noise", "ride comfort", "vibration"],
        conclusion_template="Incorrect tire inflation pressure can increase tire noise and reduce ride comfort due to altered tread contact and vibration.",
        reasoning_framework=(
            "Underinflation increases tread block deformation, causing irregular contact and increased noise. "
            "Overinflation reduces contact patch, potentially increasing road noise transmission. "
            "The reasoning involves vibration analysis, acoustics, and material deformation. "
            "Maintaining proper pressure optimizes noise levels and comfort."
        ),
        key_factors=["inflation pressure", "tread contact", "vibration", "noise levels"],
        primary_authority=["Tire Industry Association Noise Studies", "SAE Tire Engineering Papers"],
        burden_holder="Vehicle Owner",
        adversary_position="Some overlook inflation effects on noise.",
        counter_arguments=[
            "Proper inflation reduces noise and improves comfort.",
            "Neglect leads to degraded driving experience."
        ],
        resolution_strategy="Maintain recommended tire pressures and monitor noise changes.",
        entity_scope="All pneumatic tires",
        confidence=0.88,
        confidence_zone="Moderate to High",
        controlling_precedent="TIA Tire Noise and Inflation Study, 2019"
    ),
    DoctrineBlock(
        topic="Tire Pressure Effects on Tire Rolling Resistance",
        keywords=["inflation pressure", "rolling resistance", "fuel economy", "tire wear"],
        conclusion_template="Proper tire inflation reduces rolling resistance, improving fuel economy and reducing tire wear.",
        reasoning_framework=(
            "Underinflated tires deform more, increasing rolling resistance and fuel consumption. "
            "Proper inflation maintains optimal shape, minimizing energy loss. "
            "The reasoning includes mechanical energy analysis and empirical fuel economy testing. "
            "Maintaining pressure also promotes even wear, extending tire life."
        ),
        key_factors=["inflation pressure", "tire deformation", "fuel consumption", "wear patterns"],
        primary_authority=["U.S. Department of Energy Fuel Economy Guides", "Tire Industry Association Efficiency Studies"],
        burden_holder="Vehicle Owner",
        adversary_position="Some neglect pressure maintenance, increasing costs.",
        counter_arguments=[
            "Proper inflation saves fuel and reduces wear.",
            "Regular checks are simple and effective."
        ],
        resolution_strategy="Perform monthly tire pressure checks and maintain recommended levels.",
        entity_scope="All road vehicles",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="DOE Fuel Economy and Tire Pressure Study, 2019"
    ),
    DoctrineBlock(
        topic="Tire Tread Pattern Directionality and Rotation",
        keywords=["directional tires", "tire rotation", "tread pattern", "performance"],
        conclusion_template="Directional tires require specific rotation patterns to maintain performance and prevent uneven wear.",
        reasoning_framework=(
            "Directional tires have tread patterns optimized for rotation in one direction to maximize water evacuation and traction. "
            "Improper rotation can reverse tread direction, reducing performance and causing uneven wear. "
            "The reasoning involves tread design analysis, water flow dynamics, and wear pattern observation. "
            "Manufacturers specify rotation methods to preserve directional integrity."
        ),
        key_factors=["tread direction", "rotation pattern", "performance", "wear"],
        primary_authority=["Tire Industry Association Directional Tire Guidelines", "Vehicle Manufacturer Recommendations"],
        burden_holder="Service Technician",
        adversary_position="Some rotate directional tires incorrectly for convenience.",
        counter_arguments=[
            "Incorrect rotation reduces safety and tire life.",
            "Following guidelines preserves performance."
        ],
        resolution_strategy="Adhere to manufacturer rotation patterns for directional tires.",
        entity_scope="Directional tires",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="TIA Directional Tire Rotation Bulletin, 2020"
    ),
    DoctrineBlock(
        topic="Tire Inflation Pressure and Vehicle Load Distribution",
        keywords=["inflation pressure", "load distribution", "vehicle handling", "tire wear"],
        conclusion_template="Proper tire inflation ensures even load distribution across tires, optimizing handling and wear.",
        reasoning_framework=(
            "Inflation pressure supports vehicle load; incorrect pressure causes uneven load distribution, affecting handling and accelerating wear. "
            "Balanced pressure maintains uniform contact patches and predictable vehicle dynamics. "
            "The reasoning includes load transfer analysis and tire deformation mechanics."
        ),
        key_factors=["inflation pressure", "vehicle load", "contact patch", "handling"],
        primary_authority=["Tire and Rim Association Load and Inflation Standards", "SAE Vehicle Dynamics Papers"],
        burden_holder="Vehicle Owner",
        adversary_position="Some neglect inflation adjustments for load changes.",
        counter_arguments=[
            "Ignoring pressure adjustments compromises safety and tire life.",
            "Proper inflation adapts to load variations."
        ],
        resolution_strategy="Adjust tire pressures according to load and manufacturer recommendations.",
        entity_scope="All road vehicles",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="TRA Load and Inflation Compliance Bulletin, 2020"
    ),
    DoctrineBlock(
        topic="Tire Pressure Effects on Braking Performance",
        keywords=["inflation pressure", "braking distance", "traction", "safety"],
        conclusion_template="Maintaining correct tire inflation pressure is essential to minimize braking distances and ensure safety.",
        reasoning_framework=(
            "Underinflated tires have reduced contact patch and increased deformation, decreasing traction and increasing braking distances. "
            "Proper inflation maximizes road contact and braking efficiency. "
            "The reasoning involves frictional force analysis and vehicle safety testing."
        ),
        key_factors=["inflation pressure", "traction", "braking distance", "vehicle safety"],
        primary_authority=["National Highway Traffic Safety Administration (NHTSA) Safety Reports", "Tire Industry Association Braking Studies"],
        burden_holder="Vehicle Owner",
        adversary_position="Some neglect inflation maintenance risking accidents.",
        counter_arguments=[
            "Incorrect inflation directly affects braking performance.",
            "Regular pressure checks enhance safety."
        ],
        resolution_strategy="Maintain recommended tire pressures and inspect regularly.",
        entity_scope="All road vehicles",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NHTSA Tire Inflation and Braking Study, 2019"
    ),
    DoctrineBlock(
        topic="Tire Inflation Pressure and Vehicle Stability",
        keywords=["inflation pressure", "vehicle stability", "handling", "safety"],
        conclusion_template="Correct tire inflation pressure is critical for maintaining vehicle stability and safe handling characteristics.",
        reasoning_framework=(
            "Underinflated tires increase sidewall flex and reduce steering response, compromising stability. "
            "Overinflated tires reduce contact patch and grip, also affecting handling. "
            "Proper inflation balances these factors to maintain predictable vehicle behavior. "
            "The reasoning involves vehicle dynamics, tire mechanics, and safety testing."
        ),
        key_factors=["inflation pressure", "steering response", "grip", "vehicle stability"],
        primary_authority=["SAE Vehicle Dynamics Papers", "National Highway Traffic Safety Administration (NHTSA) Reports"],
        burden_holder="Vehicle Owner",
        adversary_position="Some neglect inflation leading to instability.",
        counter_arguments=[
            "Proper inflation is essential for safe vehicle operation.",
            "Regular maintenance prevents instability."
        ],
        resolution_strategy="Maintain manufacturer-recommended tire pressures and monitor handling.",
        entity_scope="All road vehicles",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="NHTSA Tire Inflation and Stability Study, 2020"
    ),
    DoctrineBlock(
        topic="Tire Inflation Pressure and Impact on Tire Longevity",
        keywords=["inflation pressure", "tire longevity", "wear rate", "maintenance"],
        conclusion_template="Maintaining proper tire inflation pressure significantly extends tire longevity by reducing abnormal wear.",
        reasoning_framework=(
            "Incorrect inflation causes uneven wear patterns and accelerates tread degradation. "
            "Proper pressure maintains uniform load distribution and tread contact, slowing wear. "
            "The reasoning includes wear mechanics and maintenance best practices."
        ),
        key_factors=["inflation pressure", "wear patterns", "maintenance frequency"],
        primary_authority=["Tire Industry Association Maintenance Guidelines", "Rubber Manufacturers Association Studies"],
        burden_holder="Vehicle Owner",
        adversary_position="Some neglect inflation leading to premature tire replacement.",
        counter_arguments=[
            "Proper inflation reduces replacement costs and safety risks.",
            "Regular checks are essential."
        ],
        resolution_strategy="Maintain recommended pressures and inspect tires regularly.",
        entity_scope="All pneumatic tires",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="TIA Tire Longevity and Inflation Study, 2019"
    ),
    DoctrineBlock(
        topic="Tire Inflation Pressure and Impact on Vehicle Fuel Economy",
        keywords=["inflation pressure", "fuel economy", "rolling resistance", "maintenance"],
        conclusion_template="Proper tire inflation pressure improves vehicle fuel economy by reducing rolling resistance.",
        reasoning_framework=(
            "Underinflated tires increase rolling resistance, requiring more engine power and fuel consumption. "
            "Maintaining correct pressure minimizes energy loss. "
            "The reasoning involves mechanical energy analysis and empirical testing."
        ),
        key_factors=["inflation pressure", "rolling resistance", "fuel consumption"],
        primary_authority=["U.S. Department of Energy Fuel Economy Guides", "Tire Industry Association Efficiency Studies"],
        burden_holder="Vehicle Owner",
        adversary_position="Some neglect pressure maintenance increasing fuel costs.",
        counter_arguments=[
            "Proper inflation saves fuel and reduces emissions.",
            "Regular checks are simple and effective."
        ],
        resolution_strategy="Perform monthly tire pressure checks and maintain recommended levels.",
        entity_scope="All road vehicles",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="DOE Fuel Economy and Tire Pressure Study, 2019"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    topic_lower = topic.lower()
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic_lower:
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if any(keyword_lower in kw.lower() for kw in doctrine.keywords) or keyword_lower in doctrine.topic.lower():
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]