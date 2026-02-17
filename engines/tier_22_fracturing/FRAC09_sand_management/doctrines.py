from dataclasses import dataclass, field
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
        topic="Northern White Sand Mine Selection",
        keywords=["northern white", "sand mine", "selection", "Wisconsin", "Minnesota", "Illinois", "sourcing", "quality"],
        conclusion_template="Select Northern White sand mines based on API spec compliance, logistics cost, and mine reliability.",
        reasoning_framework=(
            "1. Evaluate all available Northern White sand mines for API RP 19C compliance (sphericity, roundness, crush resistance). "
            "2. Assess mine production capacity and historical reliability. "
            "3. Analyze proximity to Class I rail lines for cost-effective transport to West Texas. "
            "4. Calculate delivered cost per ton, factoring in mine gate price, rail freight, transload, and last-mile trucking. "
            "5. Consider mine ownership structure and contract flexibility. "
            "6. Review environmental and permitting status to avoid supply disruptions. "
            "7. Prioritize mines with proven track records in proppant supply to Permian operators. "
            "8. Incorporate feedback from completions engineers and procurement on past performance. "
            "9. Select mines that minimize total cost of ownership while maintaining quality and reliability."
        ),
        key_factors=[
            "API RP 19C compliance",
            "Mine production capacity",
            "Rail access and freight rates",
            "Delivered cost per ton",
            "Contract flexibility",
            "Environmental/permitting status",
            "Historical reliability"
        ],
        primary_authority=[
            "API RP 19C",
            "Operator procurement policy",
            "Rail carrier tariffs"
        ],
        burden_holder="Supply Chain Manager",
        adversary_position="Advocates for lowest mine gate price regardless of logistics or reliability",
        counter_arguments=[
            "Lowest mine gate price does not guarantee lowest delivered cost.",
            "Quality and reliability are critical for uninterrupted frac operations.",
            "Permitting issues can cause sudden supply loss."
        ],
        resolution_strategy="Use total delivered cost and reliability weighted scoring matrix for mine selection.",
        entity_scope="Sand procurement and logistics teams",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2018-NWS-001"
    ),
    DoctrineBlock(
        topic="In-Basin Sand Economics West Texas",
        keywords=["in-basin", "west texas", "local sand", "cost", "economics", "permian", "midland", "delaware"],
        conclusion_template="Prioritize in-basin sand for cost efficiency where quality requirements are met.",
        reasoning_framework=(
            "1. Compare delivered cost of in-basin sand (Midland/Delaware) to Northern White. "
            "2. Assess in-basin sand quality vs. API/Operator requirements. "
            "3. Quantify cost savings per well and per lateral foot. "
            "4. Evaluate operational risks: dust, fines, logistics reliability. "
            "5. Factor in local supply/demand dynamics and mine capacity utilization. "
            "6. Consider well performance data for offset wells using in-basin sand. "
            "7. Model logistics flexibility and responsiveness for pad changes. "
            "8. Incorporate environmental and community impact considerations. "
            "9. Recommend in-basin sand where cost savings outweigh quality/performance tradeoffs."
        ),
        key_factors=[
            "Delivered cost comparison",
            "Sand quality (sphericity, crush resistance)",
            "Operational risk (dust, fines)",
            "Well performance data",
            "Supply/demand balance"
        ],
        primary_authority=[
            "Operator completions engineering",
            "API RP 19C",
            "Sand mine production reports"
        ],
        burden_holder="Completions Engineering",
        adversary_position="Insists on Northern White regardless of economics",
        counter_arguments=[
            "In-basin sand may not meet all quality specs.",
            "Potential for increased screen-outs or well performance issues.",
            "Local supply disruptions can impact operations."
        ],
        resolution_strategy="Pilot in-basin sand on select wells, monitor performance, and scale based on results.",
        entity_scope="Permian Basin completions operations",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2019-IBS-002"
    ),
    DoctrineBlock(
        topic="Sand Quality API Specifications",
        keywords=["API", "specifications", "sand quality", "sphericity", "roundness", "crush resistance", "turbidity"],
        conclusion_template="All proppant must meet or exceed API RP 19C specifications prior to delivery to wellsite.",
        reasoning_framework=(
            "1. Review API RP 19C for required sand quality parameters: sphericity, roundness, crush resistance, turbidity, acid solubility. "
            "2. Require mine-provided certificates of analysis (COA) for each batch. "
            "3. Conduct random third-party lab testing for verification. "
            "4. Reject loads failing to meet minimum spec. "
            "5. Maintain traceability from mine to wellsite for quality assurance. "
            "6. Document and communicate non-conformance events to suppliers. "
            "7. Enforce penalties for repeated quality failures. "
            "8. Update procurement contracts to reflect current API standards."
        ),
        key_factors=[
            "API RP 19C parameters",
            "COA documentation",
            "Third-party lab verification",
            "Traceability",
            "Supplier accountability"
        ],
        primary_authority=[
            "API RP 19C",
            "Operator quality control policy"
        ],
        burden_holder="Sand Supplier",
        adversary_position="Argues for relaxed specs to reduce cost",
        counter_arguments=[
            "Non-compliant sand increases risk of screen-outs and formation damage.",
            "Traceability is essential for root cause analysis.",
            "Quality failures can halt frac operations."
        ],
        resolution_strategy="Strict enforcement of API specs and supplier penalties for non-compliance.",
        entity_scope="All sand suppliers and logistics providers",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2020-API-003"
    ),
    DoctrineBlock(
        topic="Proppant Logistics: Truck, Rail, Transload",
        keywords=["logistics", "proppant", "truck", "rail", "transload", "transportation", "supply chain"],
        conclusion_template="Optimize proppant logistics by balancing cost, reliability, and delivery timing across truck, rail, and transload modes.",
        reasoning_framework=(
            "1. Map all available logistics routes from mine to wellsite, including truck, rail, and transload combinations. "
            "2. Calculate total delivered cost and time for each route. "
            "3. Assess reliability based on historical on-time performance and incident rates. "
            "4. Evaluate capacity constraints at each transload facility. "
            "5. Model impact of rail delays and truck driver shortages. "
            "6. Prioritize routes that minimize demurrage and detention charges. "
            "7. Incorporate flexibility for rapid pad changes and schedule shifts. "
            "8. Maintain backup logistics plans for weather or supply disruptions."
        ),
        key_factors=[
            "Delivered cost and time",
            "Route reliability",
            "Transload capacity",
            "Demurrage/detention risk",
            "Flexibility for schedule changes"
        ],
        primary_authority=[
            "Logistics operations team",
            "Rail carrier contracts",
            "DOT regulations"
        ],
        burden_holder="Logistics Coordinator",
        adversary_position="Prefers single-mode transport for simplicity",
        counter_arguments=[
            "Single-mode transport may not be cost-effective or reliable.",
            "Transload bottlenecks can halt deliveries.",
            "Weather and labor disruptions require flexible routing."
        ],
        resolution_strategy="Use multi-modal logistics optimization software and maintain alternate routing options.",
        entity_scope="Proppant supply chain",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2018-LOG-004"
    ),
    DoctrineBlock(
        topic="Last-Mile Delivery: Sand Hauling Truck Management",
        keywords=["last-mile", "sand hauling", "trucking", "delivery", "wellsite", "fleet management"],
        conclusion_template="Implement dynamic scheduling and GPS tracking for last-mile sand hauling to optimize wellsite delivery.",
        reasoning_framework=(
            "1. Maintain real-time GPS tracking of all sand hauling trucks. "
            "2. Use dynamic scheduling algorithms to assign trucks based on wellsite demand and traffic conditions. "
            "3. Monitor loading/unloading times to identify bottlenecks. "
            "4. Enforce driver HOS (Hours of Service) compliance and rest breaks. "
            "5. Communicate ETAs to wellsite and completions teams. "
            "6. Use telematics data to optimize fleet utilization and reduce idle time. "
            "7. Maintain backup drivers and trucks for surge demand or breakdowns. "
            "8. Regularly review and update routing based on changing pad locations."
        ),
        key_factors=[
            "Fleet GPS tracking",
            "Dynamic scheduling",
            "Loading/unloading efficiency",
            "Driver compliance",
            "Communication with wellsite"
        ],
        primary_authority=[
            "DOT HOS regulations",
            "Operator logistics policy"
        ],
        burden_holder="Trucking Fleet Manager",
        adversary_position="Relies on static schedules and manual dispatch",
        counter_arguments=[
            "Static schedules cannot adapt to real-time wellsite changes.",
            "Manual dispatch increases risk of miscommunication.",
            "Non-compliance with HOS can result in fines and safety incidents."
        ],
        resolution_strategy="Deploy fleet management software with real-time data integration.",
        entity_scope="Sand hauling fleet operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2019-LMD-005"
    ),
    DoctrineBlock(
        topic="Wellsite Silo Management: Sand Storage Capacity",
        keywords=["wellsite", "silo", "sand storage", "inventory", "capacity", "operations"],
        conclusion_template="Maintain wellsite sand silo inventory at a minimum of 12 hours of forecasted frac demand.",
        reasoning_framework=(
            "1. Calculate forecasted sand demand based on frac schedule and proppant intensity. "
            "2. Ensure silo storage capacity is sufficient for at least 12 hours of continuous pumping. "
            "3. Monitor real-time inventory levels via silo sensors. "
            "4. Schedule truck deliveries to maintain buffer inventory and avoid pump shutdowns. "
            "5. Coordinate with completions team for schedule changes or pad moves. "
            "6. Document inventory movements for traceability. "
            "7. Implement alarms for low inventory thresholds."
        ),
        key_factors=[
            "Frac schedule and demand forecast",
            "Silo storage capacity",
            "Real-time inventory monitoring",
            "Delivery scheduling",
            "Coordination with completions"
        ],
        primary_authority=[
            "Completions operations",
            "Silo equipment manufacturer specs"
        ],
        burden_holder="Wellsite Logistics Coordinator",
        adversary_position="Minimizes inventory to reduce costs, risking pump shutdowns",
        counter_arguments=[
            "Insufficient inventory can halt frac operations.",
            "Excess inventory increases demurrage but is less costly than downtime.",
            "Real-time monitoring reduces risk of over/under supply."
        ],
        resolution_strategy="Use automated inventory management and maintain minimum buffer as policy.",
        entity_scope="Wellsite logistics and completions",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2020-WSM-006"
    ),
    DoctrineBlock(
        topic="Sand Conveyor Belt Delivery System Operations",
        keywords=["conveyor belt", "sand delivery", "wellsite", "operations", "automation"],
        conclusion_template="Operate sand conveyor belt systems within manufacturer load and speed specifications to ensure safe, efficient delivery.",
        reasoning_framework=(
            "1. Review conveyor belt manufacturer specifications for maximum load and speed. "
            "2. Train operators on safe start-up, shutdown, and emergency procedures. "
            "3. Monitor belt tension, alignment, and wear via sensors. "
            "4. Schedule regular preventive maintenance and inspections. "
            "5. Integrate conveyor controls with wellsite inventory management for automated delivery. "
            "6. Document all maintenance and operational incidents for root cause analysis. "
            "7. Maintain spare parts inventory for critical components."
        ),
        key_factors=[
            "Manufacturer specs",
            "Operator training",
            "Preventive maintenance",
            "Sensor monitoring",
            "Integration with inventory systems"
        ],
        primary_authority=[
            "Conveyor system OEM manuals",
            "Operator safety policy"
        ],
        burden_holder="Wellsite Equipment Supervisor",
        adversary_position="Operates at maximum speed/load for throughput, risking failures",
        counter_arguments=[
            "Overloading increases risk of mechanical failure and downtime.",
            "Untrained operators increase safety risk.",
            "Preventive maintenance reduces unplanned outages."
        ],
        resolution_strategy="Enforce manufacturer specs and require operator certification.",
        entity_scope="Wellsite equipment operations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2018-CBDS-007"
    ),
    DoctrineBlock(
        topic="Proppant On-Location Inventory Management",
        keywords=["inventory", "on-location", "proppant", "sand", "wellsite", "tracking"],
        conclusion_template="Implement real-time digital tracking of on-location proppant inventory for operational visibility.",
        reasoning_framework=(
            "1. Deploy digital inventory management systems with real-time data capture at wellsite. "
            "2. Use RFID/barcode scanning for all inbound and outbound sand loads. "
            "3. Integrate inventory data with completions scheduling and logistics platforms. "
            "4. Set inventory thresholds for reordering and buffer maintenance. "
            "5. Provide dashboard visibility to operations, procurement, and logistics teams. "
            "6. Audit inventory records regularly to reconcile physical and digital counts. "
            "7. Investigate and resolve discrepancies promptly."
        ),
        key_factors=[
            "Digital inventory systems",
            "RFID/barcode tracking",
            "Integration with scheduling/logistics",
            "Threshold-based reordering",
            "Audit and reconciliation"
        ],
        primary_authority=[
            "Operator digitalization policy",
            "Inventory management best practices"
        ],
        burden_holder="Wellsite Inventory Manager",
        adversary_position="Relies on manual tracking and paper tickets",
        counter_arguments=[
            "Manual tracking increases risk of errors and theft.",
            "Lack of real-time data delays decision-making.",
            "Digital systems improve transparency and accountability."
        ],
        resolution_strategy="Mandate digital inventory tracking for all wellsite proppant.",
        entity_scope="Wellsite and central logistics",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2021-OLI-008"
    ),
    DoctrineBlock(
        topic="Multi-Well Pad Sand Logistics Coordination",
        keywords=["multi-well pad", "sand logistics", "coordination", "pad moves", "scheduling"],
        conclusion_template="Coordinate sand deliveries and inventory across multi-well pads to minimize downtime and demurrage.",
        reasoning_framework=(
            "1. Develop integrated sand delivery schedules for all wells on a pad. "
            "2. Use centralized logistics coordination to allocate trucks and inventory dynamically. "
            "3. Monitor frac progress and adjust deliveries in real-time for pad moves. "
            "4. Share inventory and delivery data across all pad teams. "
            "5. Pre-position sand at new pads ahead of schedule where possible. "
            "6. Analyze historical data to optimize pad sequencing and reduce idle time."
        ),
        key_factors=[
            "Integrated delivery schedules",
            "Centralized coordination",
            "Real-time monitoring",
            "Inventory pre-positioning",
            "Historical data analysis"
        ],
        primary_authority=[
            "Pad logistics manager",
            "Completions scheduling team"
        ],
        burden_holder="Pad Logistics Coordinator",
        adversary_position="Manages each well independently, causing inefficiency",
        counter_arguments=[
            "Independent management increases risk of downtime during pad moves.",
            "Centralized coordination reduces truck idle time and demurrage.",
            "Historical data enables continuous improvement."
        ],
        resolution_strategy="Mandate centralized logistics coordination for all multi-well pads.",
        entity_scope="Pad logistics and completions teams",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2020-MWP-009"
    ),
    DoctrineBlock(
        topic="Proppant Procurement Contract and Spot Market Pricing",
        keywords=["procurement", "contract", "spot market", "pricing", "sand", "proppant"],
        conclusion_template="Balance contract and spot market proppant procurement to optimize cost and supply security.",
        reasoning_framework=(
            "1. Analyze historical sand consumption and forecast future demand. "
            "2. Secure base volume via long-term contracts with reliable suppliers. "
            "3. Use spot market purchases to cover demand surges or pad schedule changes. "
            "4. Monitor spot market price trends and volatility. "
            "5. Negotiate contract terms for flexibility and price adjustment mechanisms. "
            "6. Diversify supplier base to reduce single-source risk. "
            "7. Regularly review procurement mix and adjust based on market dynamics."
        ),
        key_factors=[
            "Historical and forecasted demand",
            "Contract vs. spot price trends",
            "Supplier reliability",
            "Contract flexibility",
            "Market volatility"
        ],
        primary_authority=[
            "Procurement policy",
            "Market intelligence reports"
        ],
        burden_holder="Procurement Manager",
        adversary_position="Relies solely on contracts or spot market, ignoring balance",
        counter_arguments=[
            "Sole reliance on contracts can lead to overpayment in falling markets.",
            "Spot market only exposes to supply risk and price spikes.",
            "Balanced approach optimizes cost and security."
        ],
        resolution_strategy="Set policy for minimum contract coverage with spot market flexibility.",
        entity_scope="Sand procurement and supply chain",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2018-PPC-010"
    ),
    DoctrineBlock(
        topic="Sand Consumption Forecasting: Wells Per Month",
        keywords=["forecasting", "sand consumption", "wells per month", "demand planning"],
        conclusion_template="Forecast sand consumption using rolling 12-month well schedule and proppant intensity trends.",
        reasoning_framework=(
            "1. Collect rolling 12-month well schedule from drilling and completions teams. "
            "2. Apply historical proppant intensity (lbs/ft) by well type and stage count. "
            "3. Adjust forecasts for pad moves, schedule changes, and operational delays. "
            "4. Incorporate offset well data and regional trends. "
            "5. Validate forecasts monthly against actuals and update assumptions. "
            "6. Communicate forecast changes to procurement and logistics teams."
        ),
        key_factors=[
            "Well schedule accuracy",
            "Proppant intensity trends",
            "Operational schedule changes",
            "Offset well data",
            "Forecast validation"
        ],
        primary_authority=[
            "Completions planning",
            "Historical consumption data"
        ],
        burden_holder="Demand Planner",
        adversary_position="Uses static annual forecasts, ignoring schedule changes",
        counter_arguments=[
            "Static forecasts miss dynamic changes in well schedule.",
            "Rolling forecasts improve accuracy and supply chain responsiveness.",
            "Regular validation reduces risk of over/under supply."
        ],
        resolution_strategy="Mandate rolling 12-month forecast updates and monthly validation.",
        entity_scope="Demand planning and procurement",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2021-SCF-011"
    ),
    DoctrineBlock(
        topic="Proppant Intensity Trends: Pounds Per Lateral Foot",
        keywords=["proppant intensity", "lateral foot", "sand usage", "trends", "frac design"],
        conclusion_template="Monitor and update proppant intensity assumptions quarterly to reflect evolving frac designs.",
        reasoning_framework=(
            "1. Collect proppant usage data per lateral foot from recent completions. "
            "2. Analyze trends by well type, formation, and operator. "
            "3. Adjust planning assumptions for increasing or decreasing intensity. "
            "4. Communicate changes to procurement and logistics teams. "
            "5. Use updated intensity in sand consumption forecasts and contract negotiations."
        ),
        key_factors=[
            "Recent completions data",
            "Frac design changes",
            "Formation-specific trends",
            "Communication of updates"
        ],
        primary_authority=[
            "Completions engineering",
            "Frac design team"
        ],
        burden_holder="Completions Data Analyst",
        adversary_position="Uses outdated proppant intensity assumptions",
        counter_arguments=[
            "Outdated assumptions lead to forecast errors.",
            "Frac designs evolve rapidly with technology.",
            "Regular updates improve supply chain accuracy."
        ],
        resolution_strategy="Require quarterly review and update of proppant intensity assumptions.",
        entity_scope="Completions, procurement, and logistics",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2019-PIT-012"
    ),
    DoctrineBlock(
        topic="Regional Sand Supply Demand: Permian Midland Delaware",
        keywords=["regional supply", "demand", "permian", "midland", "delaware", "market analysis"],
        conclusion_template="Continuously monitor regional sand supply and demand to anticipate price and availability shifts.",
        reasoning_framework=(
            "1. Collect monthly production and capacity data from all regional sand mines. "
            "2. Track operator well schedules and forecasted sand demand. "
            "3. Monitor inventory levels at mines, transloads, and wellsites. "
            "4. Analyze market trends for new mine openings, closures, and expansions. "
            "5. Assess impact of regulatory or environmental changes. "
            "6. Share supply/demand insights with procurement and logistics teams for proactive planning."
        ),
        key_factors=[
            "Mine production/capacity",
            "Operator demand forecasts",
            "Inventory levels",
            "Market trends",
            "Regulatory changes"
        ],
        primary_authority=[
            "Market intelligence providers",
            "Operator planning teams"
        ],
        burden_holder="Market Analyst",
        adversary_position="Relies on static annual market reports",
        counter_arguments=[
            "Static reports miss dynamic market shifts.",
            "Proactive monitoring enables rapid response to shortages or gluts.",
            "Regulatory changes can rapidly alter supply."
        ],
        resolution_strategy="Mandate monthly market monitoring and reporting.",
        entity_scope="Procurement, logistics, and planning",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2020-RSD-013"
    ),
    DoctrineBlock(
        topic="Sand Mine Capacity Utilization and Market Dynamics",
        keywords=["mine capacity", "utilization", "market dynamics", "supply", "demand", "pricing"],
        conclusion_template="Optimize procurement and logistics based on real-time sand mine capacity utilization data.",
        reasoning_framework=(
            "1. Obtain real-time capacity utilization data from all contracted sand mines. "
            "2. Identify mines operating at or near full capacity, indicating potential supply constraints. "
            "3. Monitor spot market price movements linked to capacity shifts. "
            "4. Adjust procurement mix to avoid over-reliance on constrained mines. "
            "5. Communicate capacity risks to logistics and completions teams. "
            "6. Use data to negotiate price and volume flexibility in contracts."
        ),
        key_factors=[
            "Mine capacity utilization",
            "Spot market pricing",
            "Procurement mix",
            "Communication of risks",
            "Contract flexibility"
        ],
        primary_authority=[
            "Sand mine production reports",
            "Market pricing indices"
        ],
        burden_holder="Procurement Analyst",
        adversary_position="Ignores capacity data, risking supply disruptions",
        counter_arguments=[
            "Ignoring capacity leads to last-minute shortages and price spikes.",
            "Real-time data enables proactive risk management.",
            "Flexible contracts mitigate supply risk."
        ],
        resolution_strategy="Integrate mine capacity data into procurement and logistics planning.",
        entity_scope="Procurement and supply chain",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2019-MCU-014"
    ),
    DoctrineBlock(
        topic="Proppant Cost Per Pound Delivered Economics",
        keywords=["cost per pound", "delivered", "economics", "proppant", "sand", "TCO"],
        conclusion_template="Evaluate all-in delivered proppant cost per pound to optimize supplier and logistics decisions.",
        reasoning_framework=(
            "1. Calculate total delivered cost per pound, including mine gate price, rail/truck freight, transload, and last-mile delivery. "
            "2. Compare costs across all supplier and logistics combinations. "
            "3. Factor in demurrage, detention, and inventory holding costs. "
            "4. Use cost data to inform procurement negotiations and supplier selection. "
            "5. Monitor cost trends and adjust sourcing as market conditions change."
        ),
        key_factors=[
            "Mine gate price",
            "Freight and transload costs",
            "Last-mile delivery costs",
            "Demurrage/detention",
            "Inventory holding costs"
        ],
        primary_authority=[
            "Procurement and logistics cost reports",
            "Finance department"
        ],
        burden_holder="Procurement and Logistics Analyst",
        adversary_position="Focuses only on mine gate price, ignoring full delivery cost",
        counter_arguments=[
            "Mine gate price alone does not reflect true delivered cost.",
            "Ignoring logistics costs can erode margins.",
            "All-in cost analysis supports better decision-making."
        ],
        resolution_strategy="Mandate all-in delivered cost analysis for procurement decisions.",
        entity_scope="Procurement, logistics, and finance",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2021-PCP-015"
    ),
    DoctrineBlock(
        topic="Dual Fuel Truck Fleet: Diesel and CNG Operations",
        keywords=["dual fuel", "truck fleet", "diesel", "CNG", "operations", "emissions", "cost"],
        conclusion_template="Deploy dual fuel (diesel/CNG) trucks where cost and emissions benefits justify investment.",
        reasoning_framework=(
            "1. Assess total cost of ownership for dual fuel trucks vs. diesel-only. "
            "2. Calculate fuel cost savings based on regional CNG pricing and availability. "
            "3. Evaluate emissions reductions and compliance with operator ESG targets. "
            "4. Analyze maintenance and operational complexity. "
            "5. Pilot dual fuel trucks on select routes and monitor performance. "
            "6. Scale deployment where benefits are validated."
        ),
        key_factors=[
            "Total cost of ownership",
            "Fuel cost savings",
            "Emissions reductions",
            "CNG infrastructure availability",
            "Operational complexity"
        ],
        primary_authority=[
            "Fleet management",
            "ESG policy",
            "CNG infrastructure providers"
        ],
        burden_holder="Fleet Manager",
        adversary_position="Prefers diesel-only due to simplicity",
        counter_arguments=[
            "Dual fuel can reduce costs and emissions if infrastructure supports.",
            "Operational complexity can be managed with training.",
            "ESG targets may require emissions reductions."
        ],
        resolution_strategy="Pilot and scale dual fuel where justified by data.",
        entity_scope="Fleet operations and ESG compliance",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="FRAC09-2019-DFT-016"
    ),
    DoctrineBlock(
        topic="Sand Transload Facility: Rail to Truck Operations",
        keywords=["transload", "facility", "rail to truck", "operations", "sand", "proppant"],
        conclusion_template="Operate sand transload facilities to maximize throughput and minimize demurrage.",
        reasoning_framework=(
            "1. Schedule railcar arrivals to match truck loading capacity and wellsite demand. "
            "2. Monitor transload equipment utilization and downtime. "
            "3. Implement real-time tracking of railcar and truck movements. "
            "4. Maintain preventive maintenance schedule for all transload equipment. "
            "5. Coordinate with rail and trucking partners for seamless handoff. "
            "6. Track demurrage and detention charges and identify root causes."
        ),
        key_factors=[
            "Railcar/truck scheduling",
            "Equipment utilization",
            "Real-time tracking",
            "Preventive maintenance",
            "Demurrage/detention management"
        ],
        primary_authority=[
            "Transload facility manager",
            "Rail carrier contracts"
        ],
        burden_holder="Transload Operations Supervisor",
        adversary_position="Ignores real-time data, causing bottlenecks",
        counter_arguments=[
            "Lack of real-time tracking increases demurrage.",
            "Preventive maintenance reduces unplanned downtime.",
            "Coordination improves throughput."
        ],
        resolution_strategy="Mandate real-time tracking and preventive maintenance at all transloads.",
        entity_scope="Transload operations and logistics",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2020-TLF-017"
    ),
    DoctrineBlock(
        topic="Container POD Delivery System: Unit Train Operations",
        keywords=["container POD", "unit train", "delivery system", "sand logistics", "rail"],
        conclusion_template="Utilize container POD unit trains for high-volume sand moves to reduce transload handling and costs.",
        reasoning_framework=(
            "1. Evaluate wellsite and transload infrastructure for container POD compatibility. "
            "2. Assess cost and operational benefits of unit train vs. manifest rail. "
            "3. Model reduction in transload handling and associated costs. "
            "4. Coordinate with rail carriers for dedicated unit train scheduling. "
            "5. Monitor POD inventory and cycle times for optimization. "
            "6. Pilot container POD delivery on high-volume pads and scale as appropriate."
        ),
        key_factors=[
            "Infrastructure compatibility",
            "Cost/benefit analysis",
            "Transload handling reduction",
            "Rail carrier coordination",
            "POD inventory management"
        ],
        primary_authority=[
            "Rail carrier contracts",
            "Logistics engineering"
        ],
        burden_holder="Logistics Project Manager",
        adversary_position="Prefers traditional manifest rail and transload",
        counter_arguments=[
            "Unit trains reduce handling and costs for high-volume moves.",
            "Infrastructure upgrades may be required.",
            "Cycle time optimization is critical."
        ],
        resolution_strategy="Pilot and scale container POD unit trains where justified.",
        entity_scope="Rail logistics and wellsite operations",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="FRAC09-2019-CPD-018"
    ),
    DoctrineBlock(
        topic="Sand Quality Control: Wellsite Testing and Sampling",
        keywords=["quality control", "wellsite", "testing", "sampling", "sand", "proppant"],
        conclusion_template="Conduct wellsite sand quality testing and sampling on every delivery to ensure compliance.",
        reasoning_framework=(
            "1. Require wellsite personnel to collect sand samples from each delivery. "
            "2. Test for sphericity, roundness, crush resistance, and turbidity per API RP 19C. "
            "3. Document and store sample results for traceability. "
            "4. Reject non-compliant loads and notify supplier. "
            "5. Maintain chain of custody for all samples. "
            "6. Audit supplier quality performance quarterly."
        ),
        key_factors=[
            "Wellsite sampling protocol",
            "API RP 19C testing",
            "Documentation and traceability",
            "Supplier notification",
            "Chain of custody"
        ],
        primary_authority=[
            "API RP 19C",
            "Operator quality policy"
        ],
        burden_holder="Wellsite Quality Technician",
        adversary_position="Relies solely on supplier COA, skipping wellsite testing",
        counter_arguments=[
            "Supplier COA may not reflect actual delivered quality.",
            "Wellsite testing provides independent verification.",
            "Traceability is critical for quality assurance."
        ],
        resolution_strategy="Mandate wellsite testing and documentation for all deliveries.",
        entity_scope="Wellsite operations and quality control",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2021-SQC-019"
    ),
    DoctrineBlock(
        topic="Proppant Blending On-The-Fly Mesh Mixing",
        keywords=["proppant blending", "on-the-fly", "mesh mixing", "frac operations", "sand"],
        conclusion_template="Use on-the-fly proppant blending to optimize mesh size mix for well performance and cost.",
        reasoning_framework=(
            "1. Analyze well design and formation characteristics to determine optimal mesh mix. "
            "2. Use automated blending equipment to mix mesh sizes on-the-fly during frac. "
            "3. Monitor blend ratios in real-time and adjust as needed. "
            "4. Track cost savings and well performance improvements. "
            "5. Document blend recipes and performance outcomes for future optimization."
        ),
        key_factors=[
            "Well design and formation data",
            "Automated blending equipment",
            "Real-time monitoring",
            "Performance tracking",
            "Documentation"
        ],
        primary_authority=[
            "Completions engineering",
            "Frac equipment OEM"
        ],
        burden_holder="Frac Supervisor",
        adversary_position="Uses fixed mesh size, ignoring blend optimization",
        counter_arguments=[
            "Fixed mesh may not optimize well performance or cost.",
            "Automated blending enables real-time optimization.",
            "Performance tracking supports continuous improvement."
        ],
        resolution_strategy="Mandate on-the-fly blending for all suitable wells.",
        entity_scope="Frac operations and completions",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2020-PBM-020"
    ),
    DoctrineBlock(
        topic="Sand Delivery Scheduling Optimization",
        keywords=["sand delivery", "scheduling", "optimization", "logistics", "wellsite"],
        conclusion_template="Optimize sand delivery schedules using predictive analytics and real-time wellsite data.",
        reasoning_framework=(
            "1. Integrate predictive analytics models with real-time wellsite frac progress data. "
            "2. Forecast sand demand by stage and adjust truck dispatch accordingly. "
            "3. Use dynamic scheduling to minimize truck idle time and demurrage. "
            "4. Communicate schedule changes instantly to all logistics partners. "
            "5. Continuously refine models based on actual delivery and consumption data."
        ),
        key_factors=[
            "Predictive analytics integration",
            "Real-time frac progress data",
            "Dynamic dispatch scheduling",
            "Communication protocols",
            "Model refinement"
        ],
        primary_authority=[
            "Logistics analytics team",
            "Completions operations"
        ],
        burden_holder="Logistics Scheduler",
        adversary_position="Uses static delivery schedules, ignoring real-time data",
        counter_arguments=[
            "Static schedules cause inefficiency and increased costs.",
            "Predictive analytics improve delivery accuracy.",
            "Real-time adjustments reduce demurrage."
        ],
        resolution_strategy="Implement predictive scheduling platform for all sand deliveries.",
        entity_scope="Logistics and wellsite operations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2021-SDS-021"
    ),
    DoctrineBlock(
        topic="Sand Loss Prevention and Spillage Control",
        keywords=["sand loss", "spillage", "prevention", "wellsite", "logistics", "environment"],
        conclusion_template="Implement strict sand loss prevention and spillage control measures at all transfer points.",
        reasoning_framework=(
            "1. Identify all sand transfer points (mine, transload, truck, wellsite). "
            "2. Train personnel on best practices for loading/unloading and spillage response. "
            "3. Use containment systems and spill kits at all transfer locations. "
            "4. Monitor and document all spillage events. "
            "5. Investigate root causes and implement corrective actions. "
            "6. Report significant spills to regulatory authorities as required."
        ),
        key_factors=[
            "Transfer point identification",
            "Personnel training",
            "Containment systems",
            "Spillage monitoring",
            "Regulatory reporting"
        ],
        primary_authority=[
            "Operator HSE policy",
            "Environmental regulations"
        ],
        burden_holder="HSE Coordinator",
        adversary_position="Downplays minor spills, risking environmental compliance",
        counter_arguments=[
            "Uncontrolled spills can result in regulatory fines.",
            "Containment and training reduce risk.",
            "Documentation supports compliance and improvement."
        ],
        resolution_strategy="Mandate spillage control protocols and regular training.",
        entity_scope="All sand logistics operations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2020-SLP-022"
    ),
    DoctrineBlock(
        topic="Sand Ticket Reconciliation and Digitalization",
        keywords=["sand ticket", "reconciliation", "digitalization", "inventory", "tracking"],
        conclusion_template="Digitalize sand ticketing and automate reconciliation to improve accuracy and reduce fraud.",
        reasoning_framework=(
            "1. Replace paper sand tickets with digital ticketing systems integrated with inventory management. "
            "2. Require GPS and timestamp validation for all deliveries. "
            "3. Automate reconciliation of tickets with inventory movements and wellsite consumption. "
            "4. Audit ticket data regularly for discrepancies. "
            "5. Investigate and resolve any anomalies promptly."
        ),
        key_factors=[
            "Digital ticketing systems",
            "GPS/timestamp validation",
            "Automated reconciliation",
            "Audit protocols",
            "Fraud prevention"
        ],
        primary_authority=[
            "Finance and audit policy",
            "Operator digitalization initiative"
        ],
        burden_holder="Inventory Control Analyst",
        adversary_position="Relies on paper tickets, increasing error and fraud risk",
        counter_arguments=[
            "Paper tickets are prone to loss and manipulation.",
            "Digital systems improve traceability and accuracy.",
            "Automated reconciliation reduces manual workload."
        ],
        resolution_strategy="Mandate digital ticketing and automated reconciliation for all sand deliveries.",
        entity_scope="Inventory, logistics, and finance",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2021-STR-023"
    ),
    DoctrineBlock(
        topic="Sand Hauling Safety and Driver Training",
        keywords=["sand hauling", "safety", "driver training", "fleet", "wellsite"],
        conclusion_template="Enforce comprehensive safety and driver training for all sand hauling personnel.",
        reasoning_framework=(
            "1. Require all drivers to complete sand hauling safety training and certification. "
            "2. Conduct regular safety audits and ride-alongs. "
            "3. Monitor driver performance via telematics and incident reporting. "
            "4. Enforce strict compliance with speed limits and wellsite safety protocols. "
            "5. Investigate all incidents and implement corrective actions."
        ),
        key_factors=[
            "Driver training and certification",
            "Safety audits",
            "Telematics monitoring",
            "Incident investigation",
            "Compliance enforcement"
        ],
        primary_authority=[
            "DOT regulations",
            "Operator HSE policy"
        ],
        burden_holder="Fleet Safety Manager",
        adversary_position="Minimizes training to reduce costs",
        counter_arguments=[
            "Insufficient training increases accident risk.",
            "Telematics data supports proactive safety management.",
            "Compliance reduces liability."
        ],
        resolution_strategy="Mandate annual training and continuous monitoring for all drivers.",
        entity_scope="Fleet and wellsite logistics",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2020-SHS-024"
    ),
    DoctrineBlock(
        topic="Sand Inventory Shrinkage Analysis",
        keywords=["inventory shrinkage", "sand", "loss analysis", "reconciliation", "audit"],
        conclusion_template="Conduct monthly sand inventory shrinkage analysis to identify and address losses.",
        reasoning_framework=(
            "1. Reconcile sand inventory balances monthly across mine, transload, and wellsite. "
            "2. Analyze shrinkage trends and identify patterns or anomalies. "
            "3. Investigate root causes of losses (spillage, theft, misreporting). "
            "4. Implement corrective actions and monitor effectiveness. "
            "5. Report shrinkage findings to management and audit teams."
        ),
        key_factors=[
            "Monthly reconciliation",
            "Shrinkage trend analysis",
            "Root cause investigation",
            "Corrective action tracking",
            "Management reporting"
        ],
        primary_authority=[
            "Finance and audit policy",
            "Inventory management standards"
        ],
        burden_holder="Inventory Analyst",
        adversary_position="Ignores shrinkage, risking unaccounted losses",
        counter_arguments=[
            "Unaddressed shrinkage erodes profitability.",
            "Regular analysis enables loss prevention.",
            "Management oversight improves accountability."
        ],
        resolution_strategy="Mandate monthly shrinkage analysis and management reporting.",
        entity_scope="Inventory and finance",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2021-SISA-025"
    ),
    DoctrineBlock(
        topic="Sand Mine Permitting and Regulatory Compliance",
        keywords=["sand mine", "permitting", "regulatory compliance", "environment", "operations"],
        conclusion_template="Ensure all sand mines supplying proppant are fully permitted and compliant with environmental regulations.",
        reasoning_framework=(
            "1. Require documentation of all relevant permits for each sand mine. "
            "2. Monitor ongoing compliance with environmental, safety, and operational regulations. "
            "3. Audit supplier compliance annually. "
            "4. Suspend sourcing from mines with unresolved regulatory violations. "
            "5. Communicate compliance requirements in procurement contracts."
        ),
        key_factors=[
            "Permit documentation",
            "Ongoing compliance monitoring",
            "Annual audits",
            "Contractual compliance requirements",
            "Supplier communication"
        ],
        primary_authority=[
            "State and federal environmental agencies",
            "Operator procurement policy"
        ],
        burden_holder="Procurement Compliance Officer",
        adversary_position="Sources from non-compliant mines to reduce cost",
        counter_arguments=[
            "Non-compliance risks supply disruptions and legal penalties.",
            "Annual audits ensure ongoing compliance.",
            "Contractual requirements support enforcement."
        ],
        resolution_strategy="Mandate compliance documentation and annual audits for all suppliers.",
        entity_scope="Procurement and supply chain",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2020-SMP-026"
    ),
    DoctrineBlock(
        topic="Sand Delivery Weather Contingency Planning",
        keywords=["weather", "contingency planning", "sand delivery", "logistics", "wellsite"],
        conclusion_template="Develop and maintain weather contingency plans for all sand delivery operations.",
        reasoning_framework=(
            "1. Monitor weather forecasts for all logistics routes and wellsites. "
            "2. Identify critical weather risks (flooding, ice, high winds) for each region. "
            "3. Develop alternate delivery routes and backup inventory plans. "
            "4. Communicate contingency plans to all logistics partners. "
            "5. Conduct annual drills and update plans based on lessons learned."
        ),
        key_factors=[
            "Weather monitoring",
            "Risk identification",
            "Alternate route planning",
            "Communication protocols",
            "Annual drills"
        ],
        primary_authority=[
            "Logistics operations",
            "Operator emergency response policy"
        ],
        burden_holder="Logistics Risk Manager",
        adversary_position="Ignores weather risks, causing delivery disruptions",
        counter_arguments=[
            "Weather disruptions can halt frac operations.",
            "Contingency planning reduces downtime.",
            "Annual drills improve readiness."
        ],
        resolution_strategy="Mandate weather contingency plans and annual drills for all logistics teams.",
        entity_scope="Logistics and wellsite operations",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2021-SDWC-027"
    ),
    DoctrineBlock(
        topic="Sand Supplier Diversification Strategy",
        keywords=["supplier diversification", "sand", "proppant", "procurement", "risk management"],
        conclusion_template="Diversify sand supplier base to mitigate supply risk and improve negotiation leverage.",
        reasoning_framework=(
            "1. Identify all qualified sand suppliers by region and product type. "
            "2. Set maximum volume thresholds for any single supplier. "
            "3. Regularly review supplier performance and reliability. "
            "4. Onboard new suppliers to maintain competitive tension. "
            "5. Adjust procurement mix based on market dynamics and supplier risk assessments."
        ),
        key_factors=[
            "Supplier qualification",
            "Volume thresholds",
            "Performance monitoring",
            "Onboarding process",
            "Risk assessment"
        ],
        primary_authority=[
            "Procurement policy",
            "Risk management standards"
        ],
        burden_holder="Procurement Manager",
        adversary_position="Concentrates volume with lowest-cost supplier, increasing risk",
        counter_arguments=[
            "Supplier concentration increases risk of supply disruption.",
            "Diversification improves negotiation leverage.",
            "Performance monitoring supports continuous improvement."
        ],
        resolution_strategy="Mandate supplier diversification and regular performance reviews.",
        entity_scope="Procurement and supply chain",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2019-SSD-028"
    ),
    DoctrineBlock(
        topic="Sand Logistics Cost Benchmarking",
        keywords=["logistics cost", "benchmarking", "sand", "proppant", "supply chain"],
        conclusion_template="Benchmark sand logistics costs quarterly against industry peers to identify savings opportunities.",
        reasoning_framework=(
            "1. Collect internal logistics cost data for all sand delivery modes. "
            "2. Obtain industry cost benchmarks from market intelligence providers. "
            "3. Analyze variances and identify root causes of cost gaps. "
            "4. Implement targeted cost reduction initiatives. "
            "5. Review benchmarking results with management quarterly."
        ),
        key_factors=[
            "Internal cost data",
            "Industry benchmarks",
            "Variance analysis",
            "Cost reduction initiatives",
            "Management review"
        ],
        primary_authority=[
            "Finance department",
            "Market intelligence providers"
        ],
        burden_holder="Logistics Cost Analyst",
        adversary_position="Ignores benchmarking, missing savings opportunities",
        counter_arguments=[
            "Benchmarking reveals hidden inefficiencies.",
            "Industry data supports negotiation and improvement.",
            "Quarterly reviews drive accountability."
        ],
        resolution_strategy="Mandate quarterly cost benchmarking and management review.",
        entity_scope="Logistics and finance",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2020-SLCB-029"
    ),
    DoctrineBlock(
        topic="Sand Inventory Cycle Count Program",
        keywords=["inventory", "cycle count", "sand", "audit", "reconciliation"],
        conclusion_template="Implement monthly cycle counts for all sand inventory locations to ensure accuracy.",
        reasoning_framework=(
            "1. Schedule monthly cycle counts for all mine, transload, and wellsite inventories. "
            "2. Use independent teams for physical counts and reconciliation. "
            "3. Investigate and resolve discrepancies promptly. "
            "4. Track cycle count accuracy trends and report to management. "
            "5. Adjust inventory processes based on findings."
        ),
        key_factors=[
            "Monthly cycle count schedule",
            "Independent reconciliation",
            "Discrepancy investigation",
            "Accuracy trend tracking",
            "Process improvement"
        ],
        primary_authority=[
            "Inventory management standards",
            "Audit policy"
        ],
        burden_holder="Inventory Control Manager",
        adversary_position="Relies on annual counts, risking inventory inaccuracy",
        counter_arguments=[
            "Annual counts miss ongoing discrepancies.",
            "Monthly cycle counts improve accuracy and accountability.",
            "Process improvement reduces future errors."
        ],
        resolution_strategy="Mandate monthly cycle counts for all sand inventory.",
        entity_scope="Inventory management and audit",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2021-SICC-030"
    ),
    DoctrineBlock(
        topic="Sand Delivery Incident Reporting and Root Cause Analysis",
        keywords=["incident reporting", "root cause analysis", "sand delivery", "logistics", "safety"],
        conclusion_template="Require immediate reporting and root cause analysis for all sand delivery incidents.",
        reasoning_framework=(
            "1. Define incident types (spillage, delay, equipment failure, safety event). "
            "2. Require immediate reporting via digital platform. "
            "3. Assign root cause analysis teams for all significant incidents. "
            "4. Implement corrective actions and track effectiveness. "
            "5. Share lessons learned across all logistics teams."
        ),
        key_factors=[
            "Incident definition",
            "Immediate reporting",
            "Root cause analysis",
            "Corrective action tracking",
            "Knowledge sharing"
        ],
        primary_authority=[
            "HSE policy",
            "Logistics operations"
        ],
        burden_holder="Logistics Safety Officer",
        adversary_position="Delays reporting or skips root cause analysis",
        counter_arguments=[
            "Delayed reporting increases risk of recurrence.",
            "Root cause analysis drives continuous improvement.",
            "Knowledge sharing prevents repeat incidents."
        ],
        resolution_strategy="Mandate digital incident reporting and RCA for all logistics teams.",
        entity_scope="Logistics and HSE",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2021-SDIR-031"
    ),
    DoctrineBlock(
        topic="Sand Delivery Emissions Tracking and Reporting",
        keywords=["emissions", "tracking", "reporting", "sand delivery", "ESG", "fleet"],
        conclusion_template="Track and report sand delivery emissions to support ESG compliance and reduction targets.",
        reasoning_framework=(
            "1. Collect fuel consumption and mileage data for all sand hauling trucks. "
            "2. Calculate CO2 and NOx emissions using EPA emissions factors. "
            "3. Aggregate emissions data by route, supplier, and wellsite. "
            "4. Report emissions monthly to ESG and management teams. "
            "5. Identify and implement emissions reduction initiatives."
        ),
        key_factors=[
            "Fuel consumption data",
            "EPA emissions factors",
            "Data aggregation",
            "Monthly reporting",
            "Reduction initiatives"
        ],
        primary_authority=[
            "ESG policy",
            "EPA regulations"
        ],
        burden_holder="ESG Reporting Analyst",
        adversary_position="Ignores emissions tracking, risking non-compliance",
        counter_arguments=[
            "ESG compliance requires emissions tracking.",
            "Data supports reduction initiatives.",
            "Monthly reporting drives accountability."
        ],
        resolution_strategy="Mandate monthly emissions tracking and reporting for all sand deliveries.",
        entity_scope="Fleet, logistics, and ESG",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2021-SDER-032"
    ),
    DoctrineBlock(
        topic="Sand Delivery Digital Twin Implementation",
        keywords=["digital twin", "sand delivery", "simulation", "logistics", "optimization"],
        conclusion_template="Implement digital twin simulation for sand delivery operations to optimize performance.",
        reasoning_framework=(
            "1. Develop digital twin models of sand delivery routes, inventory, and equipment. "
            "2. Simulate delivery scenarios to identify bottlenecks and inefficiencies. "
            "3. Use simulation outputs to optimize scheduling and resource allocation. "
            "4. Continuously update models with real-world data. "
            "5. Track performance improvements and ROI."
        ),
        key_factors=[
            "Digital twin modeling",
            "Scenario simulation",
            "Optimization outputs",
            "Model updates",
            "Performance tracking"
        ],
        primary_authority=[
            "Digitalization team",
            "Logistics operations"
        ],
        burden_holder="Logistics Optimization Lead",
        adversary_position="Relies solely on historical data, ignoring simulation benefits",
        counter_arguments=[
            "Simulation identifies hidden inefficiencies.",
            "Digital twins enable proactive optimization.",
            "Continuous updates improve accuracy."
        ],
        resolution_strategy="Mandate digital twin implementation for all major sand delivery operations.",
        entity_scope="Logistics and digitalization",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="FRAC09-2022-SDDT-033"
    ),
    DoctrineBlock(
        topic="Sand Delivery Cybersecurity Protocols",
        keywords=["cybersecurity", "sand delivery", "digital systems", "inventory", "logistics"],
        conclusion_template="Enforce cybersecurity protocols for all digital sand delivery and inventory systems.",
        reasoning_framework=(
            "1. Require multi-factor authentication for all users of digital logistics platforms. "
            "2. Conduct regular vulnerability assessments and penetration testing. "
            "3. Encrypt all data transmissions and storage. "
            "4. Train personnel on cybersecurity best practices. "
            "5. Monitor system access and investigate anomalies."
        ),
        key_factors=[
            "Authentication protocols",
            "Vulnerability assessments",
            "Data encryption",
            "Personnel training",
            "System monitoring"
        ],
        primary_authority=[
            "IT security policy",
            "Operator cybersecurity standards"
        ],
        burden_holder="IT Security Officer",
        adversary_position="Minimizes security to reduce system complexity",
        counter_arguments=[
            "Weak security exposes systems to cyberattacks.",
            "Regular assessments reduce risk.",
            "Training improves user compliance."
        ],
        resolution_strategy="Mandate cybersecurity protocols for all sand delivery digital systems.",
        entity_scope="IT, logistics, and inventory",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDCP-034"
    ),
    DoctrineBlock(
        topic="Sand Delivery Sustainability and Community Engagement",
        keywords=["sustainability", "community engagement", "sand delivery", "ESG", "environment"],
        conclusion_template="Engage local communities and implement sustainability measures in sand delivery operations.",
        reasoning_framework=(
            "1. Conduct community impact assessments for all major sand delivery routes. "
            "2. Implement noise, dust, and traffic mitigation measures. "
            "3. Communicate delivery schedules and potential impacts to local residents. "
            "4. Solicit community feedback and address concerns proactively. "
            "5. Track and report sustainability metrics to management and community stakeholders."
        ),
        key_factors=[
            "Community impact assessment",
            "Mitigation measures",
            "Communication protocols",
            "Feedback mechanisms",
            "Sustainability metrics"
        ],
        primary_authority=[
            "ESG policy",
            "Community relations team"
        ],
        burden_holder="Sustainability Officer",
        adversary_position="Ignores community concerns to maximize operational efficiency",
        counter_arguments=[
            "Community engagement reduces opposition and improves reputation.",
            "Mitigation measures reduce environmental impact.",
            "Transparency builds trust."
        ],
        resolution_strategy="Mandate community engagement and sustainability reporting for all sand delivery operations.",
        entity_scope="Logistics, ESG, and community relations",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDSC-035"
    ),
    DoctrineBlock(
        topic="Sand Delivery Real-Time Exception Management",
        keywords=["exception management", "real-time", "sand delivery", "logistics", "incident response"],
        conclusion_template="Implement real-time exception management for sand delivery disruptions to minimize operational impact.",
        reasoning_framework=(
            "1. Deploy real-time monitoring systems for all sand delivery routes and inventory points. "
            "2. Define exception types (delay, equipment failure, route closure) and response protocols. "
            "3. Assign dedicated exception response teams with clear escalation paths. "
            "4. Track resolution times and analyze for continuous improvement. "
            "5. Integrate exception data with scheduling and inventory systems."
        ),
        key_factors=[
            "Real-time monitoring",
            "Exception definition",
            "Response protocols",
            "Resolution time tracking",
            "System integration"
        ],
        primary_authority=[
            "Logistics operations",
            "IT support"
        ],
        burden_holder="Exception Response Coordinator",
        adversary_position="Handles exceptions manually, delaying response",
        counter_arguments=[
            "Manual exception handling increases downtime.",
            "Real-time systems enable rapid response.",
            "Continuous improvement reduces future incidents."
        ],
        resolution_strategy="Mandate real-time exception management for all sand delivery operations.",
        entity_scope="Logistics and IT",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDREM-036"
    ),
    DoctrineBlock(
        topic="Sand Delivery Artificial Intelligence Optimization",
        keywords=["artificial intelligence", "optimization", "sand delivery", "logistics", "machine learning"],
        conclusion_template="Leverage AI and machine learning to optimize sand delivery routes, schedules, and inventory.",
        reasoning_framework=(
            "1. Collect historical and real-time data on sand deliveries, routes, and consumption. "
            "2. Train AI models to predict demand, optimize routes, and minimize costs. "
            "3. Integrate AI recommendations with logistics scheduling platforms. "
            "4. Monitor model performance and retrain as needed. "
            "5. Quantify cost savings and operational improvements."
        ),
        key_factors=[
            "Data collection",
            "AI model training",
            "Platform integration",
            "Performance monitoring",
            "Cost/benefit analysis"
        ],
        primary_authority=[
            "Digitalization team",
            "Logistics analytics"
        ],
        burden_holder="AI Optimization Lead",
        adversary_position="Relies on manual optimization, missing AI benefits",
        counter_arguments=[
            "Manual methods cannot match AI optimization speed and accuracy.",
            "Integration enables real-time decision-making.",
            "Continuous improvement maximizes benefits."
        ],
        resolution_strategy="Mandate AI optimization for all major sand delivery operations.",
        entity_scope="Logistics and digitalization",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDAI-037"
    ),
    DoctrineBlock(
        topic="Sand Delivery Carbon Footprint Reduction Initiatives",
        keywords=["carbon footprint", "reduction", "sand delivery", "emissions", "ESG"],
        conclusion_template="Implement carbon footprint reduction initiatives in sand delivery operations to meet ESG targets.",
        reasoning_framework=(
            "1. Identify major sources of carbon emissions in sand delivery (fuel, idle time, routing). "
            "2. Implement fuel-efficient driving practices and idle reduction policies. "
            "3. Transition to lower-emission vehicles where feasible. "
            "4. Optimize delivery routes to minimize mileage. "
            "5. Track and report emissions reductions to ESG teams."
        ),
        key_factors=[
            "Emissions source identification",
            "Fuel efficiency initiatives",
            "Vehicle transition planning",
            "Route optimization",
            "Reporting"
        ],
        primary_authority=[
            "ESG policy",
            "Fleet management"
        ],
        burden_holder="Fleet Sustainability Manager",
        adversary_position="Prioritizes cost over emissions reduction",
        counter_arguments=[
            "ESG targets require emissions reductions.",
            "Fuel efficiency also reduces costs.",
            "Reporting supports compliance and improvement."
        ],
        resolution_strategy="Mandate carbon reduction initiatives and reporting for all sand delivery operations.",
        entity_scope="Fleet, logistics, and ESG",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDCF-038"
    ),
    DoctrineBlock(
        topic="Sand Delivery Data Integration and Interoperability",
        keywords=["data integration", "interoperability", "sand delivery", "logistics", "digital systems"],
        conclusion_template="Ensure seamless data integration and interoperability across all sand delivery digital platforms.",
        reasoning_framework=(
            "1. Map all digital platforms used in sand delivery and inventory management. "
            "2. Define data exchange standards and protocols. "
            "3. Implement APIs and middleware for real-time data sharing. "
            "4. Test interoperability regularly and resolve integration issues. "
            "5. Maintain data governance and master data management."
        ),
        key_factors=[
            "Platform mapping",
            "Data exchange standards",
            "API/middleware implementation",
            "Interoperability testing",
            "Data governance"
        ],
        primary_authority=[
            "IT architecture team",
            "Digitalization policy"
        ],
        burden_holder="IT Integration Lead",
        adversary_position="Operates siloed systems, causing data delays and errors",
        counter_arguments=[
            "Siloed systems increase errors and reduce efficiency.",
            "Real-time integration improves decision-making.",
            "Data governance ensures accuracy."
        ],
        resolution_strategy="Mandate data integration and interoperability for all sand delivery systems.",
        entity_scope="IT, logistics, and inventory",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDDI-039"
    ),
    DoctrineBlock(
        topic="Sand Delivery Continuous Improvement Program",
        keywords=["continuous improvement", "sand delivery", "logistics", "kaizen", "lean"],
        conclusion_template="Establish a continuous improvement program for sand delivery operations using lean and kaizen principles.",
        reasoning_framework=(
            "1. Set up cross-functional teams to identify sand delivery process inefficiencies. "
            "2. Implement lean and kaizen tools (5S, value stream mapping, root cause analysis). "
            "3. Track improvement initiatives and measure impact on cost, safety, and reliability. "
            "4. Share best practices and lessons learned across teams. "
            "5. Review progress quarterly and set new improvement targets."
        ),
        key_factors=[
            "Cross-functional teams",
            "Lean/kaizen tools",
            "Initiative tracking",
            "Best practice sharing",
            "Quarterly review"
        ],
        primary_authority=[
            "Operations excellence team",
            "Logistics management"
        ],
        burden_holder="Continuous Improvement Lead",
        adversary_position="Resists process changes, maintaining status quo",
        counter_arguments=[
            "Continuous improvement drives cost and safety gains.",
            "Lean tools identify hidden waste.",
            "Quarterly reviews sustain momentum."
        ],
        resolution_strategy="Mandate continuous improvement program participation for all sand delivery teams.",
        entity_scope="Logistics and operations excellence",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDCI-040"
    ),
    DoctrineBlock(
        topic="Sand Delivery Blockchain Traceability",
        keywords=["blockchain", "traceability", "sand delivery", "inventory", "digital ledger"],
        conclusion_template="Implement blockchain-based traceability for sand delivery to enhance transparency and reduce fraud.",
        reasoning_framework=(
            "1. Deploy blockchain digital ledger for all sand inventory movements from mine to wellsite. "
            "2. Record all transactions with timestamps, GPS, and digital signatures. "
            "3. Enable real-time visibility for all stakeholders (operator, supplier, logistics). "
            "4. Audit blockchain records regularly for anomalies. "
            "5. Quantify reduction in reconciliation errors and fraud incidents."
        ),
        key_factors=[
            "Blockchain deployment",
            "Transaction recording",
            "Stakeholder visibility",
            "Regular audits",
            "Error/fraud reduction"
        ],
        primary_authority=[
            "Digitalization team",
            "Audit and compliance"
        ],
        burden_holder="Blockchain Project Lead",
        adversary_position="Relies on traditional systems, missing transparency benefits",
        counter_arguments=[
            "Traditional systems are prone to error and manipulation.",
            "Blockchain enhances traceability and trust.",
            "Audits ensure system integrity."
        ],
        resolution_strategy="Mandate blockchain traceability for all sand delivery inventory movements.",
        entity_scope="Digitalization, logistics, and audit",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDBT-041"
    ),
    DoctrineBlock(
        topic="Sand Delivery Vendor Performance Management",
        keywords=["vendor performance", "management", "sand delivery", "supplier", "logistics"],
        conclusion_template="Establish a vendor performance management program for all sand delivery suppliers and logistics partners.",
        reasoning_framework=(
            "1. Define key performance indicators (KPIs) for all vendors (on-time delivery, quality, safety, cost). "
            "2. Collect and analyze performance data monthly. "
            "3. Conduct quarterly performance reviews with vendors. "
            "4. Implement corrective action plans for underperformance. "
            "5. Use performance data in contract renewal and sourcing decisions."
        ),
        key_factors=[
            "KPI definition",
            "Performance data collection",
            "Quarterly reviews",
            "Corrective action plans",
            "Contract decision integration"
        ],
        primary_authority=[
            "Procurement policy",
            "Vendor management standards"
        ],
        burden_holder="Vendor Performance Manager",
        adversary_position="Ignores performance data, risking recurring issues",
        counter_arguments=[
            "Performance management drives accountability.",
            "Data-driven reviews support improvement.",
            "Contract integration incentivizes results."
        ],
        resolution_strategy="Mandate vendor performance management for all sand delivery partners.",
        entity_scope="Procurement, logistics, and vendor management",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDVP-042"
    ),
    DoctrineBlock(
        topic="Sand Delivery Regulatory Change Management",
        keywords=["regulatory change", "management", "sand delivery", "compliance", "logistics"],
        conclusion_template="Implement regulatory change management process for all sand delivery operations.",
        reasoning_framework=(
            "1. Monitor federal, state, and local regulatory changes impacting sand delivery. "
            "2. Assess operational impact of new or revised regulations. "
            "3. Update policies, procedures, and training accordingly. "
            "4. Communicate changes to all affected personnel and vendors. "
            "5. Track compliance and audit readiness."
        ),
        key_factors=[
            "Regulatory monitoring",
            "Impact assessment",
            "Policy/procedure updates",
            "Communication protocols",
            "Compliance tracking"
        ],
        primary_authority=[
            "Compliance department",
            "Legal counsel"
        ],
        burden_holder="Regulatory Compliance Manager",
        adversary_position="Ignores regulatory changes, risking non-compliance",
        counter_arguments=[
            "Non-compliance can result in fines and operational shutdowns.",
            "Proactive management reduces risk.",
            "Training ensures personnel readiness."
        ],
        resolution_strategy="Mandate regulatory change management for all sand delivery operations.",
        entity_scope="Compliance, logistics, and operations",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDRC-043"
    ),
    DoctrineBlock(
        topic="Sand Delivery Digital Workforce Enablement",
        keywords=["digital workforce", "enablement", "sand delivery", "training", "digital tools"],
        conclusion_template="Enable digital workforce for sand delivery operations through training and technology adoption.",
        reasoning_framework=(
            "1. Assess digital literacy and training needs of all sand delivery personnel. "
            "2. Provide training on digital tools (inventory systems, GPS tracking, scheduling platforms). "
            "3. Monitor adoption and usage rates. "
            "4. Collect feedback and address barriers to adoption. "
            "5. Update training and tools based on evolving needs."
        ),
        key_factors=[
            "Digital literacy assessment",
            "Training program development",
            "Adoption monitoring",
            "Feedback collection",
            "Continuous improvement"
        ],
        primary_authority=[
            "HR and training department",
            "Digitalization team"
        ],
        burden_holder="Digital Workforce Enablement Lead",
        adversary_position="Resists digital tools, relying on manual processes",
        counter_arguments=[
            "Digital tools improve efficiency and accuracy.",
            "Training addresses adoption barriers.",
            "Continuous improvement sustains progress."
        ],
        resolution_strategy="Mandate digital workforce enablement for all sand delivery personnel.",
        entity_scope="HR, logistics, and digitalization",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDDW-044"
    ),
    DoctrineBlock(
        topic="Sand Delivery End-to-End Visibility Initiative",
        keywords=["end-to-end visibility", "sand delivery", "tracking", "logistics", "inventory"],
        conclusion_template="Achieve end-to-end visibility of sand delivery from mine to wellsite through integrated tracking systems.",
        reasoning_framework=(
            "1. Integrate GPS, RFID, and inventory management systems for all sand movements. "
            "2. Provide real-time dashboard visibility to all stakeholders. "
            "3. Set up alerts for exceptions and delays. "
            "4. Use visibility data to optimize scheduling and inventory. "
            "5. Review visibility initiative performance quarterly."
        ),
        key_factors=[
            "System integration",
            "Real-time dashboards",
            "Exception alerting",
            "Optimization based on data",
            "Quarterly review"
        ],
        primary_authority=[
            "Logistics operations",
            "IT integration team"
        ],
        burden_holder="Visibility Program Manager",
        adversary_position="Operates with siloed or delayed data, risking inefficiency",
        counter_arguments=[
            "End-to-end visibility reduces delays and errors.",
            "Integrated systems improve responsiveness.",
            "Quarterly reviews drive continuous improvement."
        ],
        resolution_strategy="Mandate end-to-end visibility for all sand delivery operations.",
        entity_scope="Logistics, IT, and inventory",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRAC09-2022-SDEV-045"
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