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
        topic="Lease Bonus Rate Analysis by County and Formation",
        keywords=["lease bonus", "county", "formation", "market comparables", "valuation", "oil and gas"],
        conclusion_template="The lease bonus rate for {county} in the {formation} formation is determined by recent comparable transactions, adjusted for market conditions and geological factors.",
        reasoning_framework=(
            "Lease bonus rates are primarily influenced by recent comparable transactions within the same county and formation. "
            "The analysis begins by collecting transaction data from public records, industry databases, and broker reports. "
            "Adjustments are made for temporal factors (e.g., market cycles), geological quality, and operator reputation. "
            "Rates are normalized to account for acreage size, lease terms, and bonus payment structures. "
            "Statistical methods such as weighted averages and regression analysis are applied to derive a representative rate. "
            "Outliers are excluded unless justified by unique circumstances. "
            "The final rate is benchmarked against authoritative sources such as state lease auctions and major operator deals. "
            "Market adjustment factors are applied to reflect current commodity prices and regional demand. "
            "The conclusion is validated by cross-referencing with mineral owner associations and legal precedents."
        ),
        key_factors=[
            "Recent comparable transactions",
            "County-specific trends",
            "Formation geological quality",
            "Lease term length",
            "Operator reputation",
            "Market adjustment factors",
            "Commodity price environment",
            "Acreage size"
        ],
        primary_authority=[
            "Texas Railroad Commission",
            "New Mexico State Land Office",
            "Industry transaction databases",
            "Mineral owner associations"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator seeks lower bonus rate citing market softening",
        counter_arguments=[
            "Operator's cited comparables are outdated",
            "Geological quality is superior to referenced transactions",
            "Commodity prices have rebounded"
        ],
        resolution_strategy="Present authoritative comparables, adjust for market factors, negotiate based on current data",
        entity_scope="County and formation-specific",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas State Lease Auction 2022"
    ),
    DoctrineBlock(
        topic="Royalty Rate Negotiation Ranges",
        keywords=["royalty rate", "negotiation", "market comparables", "oil and gas", "lease"],
        conclusion_template="The market-supported royalty rate range for {formation} in {county} is {min_rate}-{max_rate}%, based on recent comparable leases and authoritative guidance.",
        reasoning_framework=(
            "Royalty rate negotiations are anchored in market comparables from recent leases within the same formation and county. "
            "Data is sourced from public lease filings, operator disclosures, and industry surveys. "
            "The range is established by identifying the 25th to 75th percentile rates from the dataset, excluding outliers. "
            "Adjustments are made for lease term, operator financial strength, and production potential. "
            "Legal minimums and maximums are referenced to ensure compliance. "
            "Negotiation strategies include leveraging high-quality geological data and competitive operator interest. "
            "Counterparty arguments are evaluated for validity based on current market conditions. "
            "The conclusion is supported by authoritative sources and controlling precedent from state lease auctions."
        ),
        key_factors=[
            "Recent lease comparables",
            "Formation-specific production potential",
            "Operator financial strength",
            "Lease term",
            "Legal minimums and maximums"
        ],
        primary_authority=[
            "Texas Oil & Gas Lease Database",
            "New Mexico Lease Records",
            "State Land Office guidelines"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator proposes below-market royalty citing lease term length",
        counter_arguments=[
            "Market data supports higher royalty",
            "Production potential justifies premium rate",
            "Operator competition increases leverage"
        ],
        resolution_strategy="Present percentile-based range, negotiate within market-supported bounds",
        entity_scope="County and formation-specific",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Texas State Lease Auction 2021"
    ),
    DoctrineBlock(
        topic="Mineral Deed Dollar per Acre Valuation",
        keywords=["mineral deed", "dollar per acre", "valuation", "market comparables", "oil and gas"],
        conclusion_template="The fair market value for mineral deed transfer in {county} is ${value}/acre, based on comparable sales and adjusted for formation quality and market trends.",
        reasoning_framework=(
            "Mineral deed valuations are based on dollar per acre metrics derived from recent comparable sales within the target county and formation. "
            "Transaction data is collected from county records, industry databases, and broker reports. "
            "Adjustments are made for formation quality, proximity to active drilling, and market trends. "
            "Outlier transactions are excluded unless justified by unique circumstances such as operator premium or distressed sale. "
            "Valuation is cross-checked against authoritative sources and controlling precedent from major transactions. "
            "Market adjustment factors are applied to reflect commodity price fluctuations and regional demand. "
            "The conclusion is validated by triangulating multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Recent comparable sales",
            "Formation quality",
            "Proximity to drilling activity",
            "Market trends",
            "Acreage size"
        ],
        primary_authority=[
            "County deed records",
            "Industry transaction databases",
            "Broker reports"
        ],
        burden_holder="Seller",
        adversary_position="Buyer claims lower value due to market softening",
        counter_arguments=[
            "Recent sales support higher value",
            "Formation quality is superior",
            "Market trends show recovery"
        ],
        resolution_strategy="Present normalized comparables, adjust for market and formation factors",
        entity_scope="County and formation-specific",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="Permian Basin Mineral Sale 2022"
    ),
    DoctrineBlock(
        topic="Producing Property PV-10 Valuation",
        keywords=["producing property", "PV-10", "valuation", "discounted cash flow", "market comparables"],
        conclusion_template="The PV-10 value of the producing property in {county} is ${pv10}, calculated using discounted cash flow analysis and validated by comparable sales.",
        reasoning_framework=(
            "PV-10 valuation is performed by projecting future cash flows from the producing property, discounting at a 10% annual rate. "
            "Cash flow projections are based on historical production, current commodity prices, and estimated decline rates. "
            "Operating expenses, taxes, and royalty payments are deducted to arrive at net cash flows. "
            "Comparable sales are used to validate the PV-10 calculation, adjusting for differences in production profile and property characteristics. "
            "Market adjustment factors are applied to account for commodity price volatility and regional demand. "
            "The conclusion is supported by authoritative sources and controlling precedent from recent producing property transactions."
        ),
        key_factors=[
            "Historical production data",
            "Commodity prices",
            "Estimated decline rates",
            "Operating expenses",
            "Comparable sales"
        ],
        primary_authority=[
            "SEC PV-10 guidelines",
            "Industry transaction databases",
            "Operator disclosures"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes projected cash flows",
        counter_arguments=[
            "Production history supports projections",
            "Comparable sales validate PV-10",
            "Market adjustment factors are reasonable"
        ],
        resolution_strategy="Present detailed PV-10 calculation, validate with comparables",
        entity_scope="Property-specific",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SEC PV-10 Reporting Standard"
    ),
    DoctrineBlock(
        topic="Working Interest vs. ORRI Pricing",
        keywords=["working interest", "ORRI", "pricing", "market comparables", "valuation"],
        conclusion_template="The pricing differential between working interest and ORRI in {formation} is determined by market comparables, adjusted for risk and revenue share.",
        reasoning_framework=(
            "Working interest and ORRI (Overriding Royalty Interest) pricing is analyzed by comparing recent transactions for each interest type within the same formation. "
            "Risk factors, such as exposure to operating expenses and capital costs, are considered for working interest. "
            "Revenue share and payment structure are evaluated for ORRI. "
            "Market comparables are normalized to account for differences in interest percentage, lease terms, and operator reputation. "
            "Adjustments are made for commodity price environment and regional demand. "
            "The conclusion is validated by authoritative sources and controlling precedent from major interest transactions."
        ),
        key_factors=[
            "Interest type",
            "Recent comparable transactions",
            "Risk exposure",
            "Revenue share",
            "Lease terms"
        ],
        primary_authority=[
            "Industry transaction databases",
            "Broker reports",
            "Operator disclosures"
        ],
        burden_holder="Seller",
        adversary_position="Buyer argues for lower ORRI value due to market trends",
        counter_arguments=[
            "Recent ORRI transactions support higher value",
            "Risk exposure is lower for ORRI",
            "Market adjustment factors favor current pricing"
        ],
        resolution_strategy="Normalize comparables, adjust for risk and revenue share",
        entity_scope="Formation-specific",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="Permian Basin ORRI Sale 2021"
    ),
    DoctrineBlock(
        topic="Net Mineral Acre Calculation",
        keywords=["net mineral acre", "calculation", "ownership", "market comparables", "oil and gas"],
        conclusion_template="Net mineral acres for the subject property are calculated by multiplying gross acres by fractional mineral ownership, validated by comparable transactions.",
        reasoning_framework=(
            "Net mineral acre calculation involves multiplying the gross acreage by the fractional mineral ownership held by the party. "
            "Fractional ownership is determined by reviewing title documents, deed records, and division orders. "
            "Comparable transactions are used to validate the calculation methodology and ensure consistency with market standards. "
            "Adjustments are made for undivided interests, overlapping leases, and legal encumbrances. "
            "The conclusion is supported by authoritative sources and controlling precedent from industry-standard calculations."
        ),
        key_factors=[
            "Gross acreage",
            "Fractional mineral ownership",
            "Title documents",
            "Comparable transactions",
            "Legal encumbrances"
        ],
        primary_authority=[
            "County deed records",
            "Division orders",
            "Industry calculation standards"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator disputes ownership fraction",
        counter_arguments=[
            "Title documents support ownership fraction",
            "Comparable transactions validate calculation",
            "Legal review confirms accuracy"
        ],
        resolution_strategy="Present detailed calculation, validate with comparables and legal review",
        entity_scope="Property-specific",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Texas Mineral Ownership Calculation Standard"
    ),
    DoctrineBlock(
        topic="Comparable Transaction Identification",
        keywords=["comparable transaction", "identification", "market comparables", "oil and gas", "valuation"],
        conclusion_template="Comparable transactions are identified based on similarity in location, formation, transaction date, and deal structure, using authoritative databases and industry standards.",
        reasoning_framework=(
            "Identification of comparable transactions begins with defining the relevant parameters: location, formation, transaction date, deal structure, and interest type. "
            "Data is sourced from public records, industry databases, and broker reports. "
            "Transactions are filtered to match the subject property as closely as possible. "
            "Outliers and non-arm's-length transactions are excluded. "
            "The final set of comparables is validated against authoritative sources and controlling precedent. "
            "Statistical methods are used to ensure representativeness and reliability."
        ),
        key_factors=[
            "Location",
            "Formation",
            "Transaction date",
            "Deal structure",
            "Interest type"
        ],
        primary_authority=[
            "Industry transaction databases",
            "Broker reports",
            "Public records"
        ],
        burden_holder="Valuator",
        adversary_position="Counterparty disputes comparability",
        counter_arguments=[
            "Parameters match subject property",
            "Transactions are arm's-length",
            "Authoritative sources validate selection"
        ],
        resolution_strategy="Present parameter-matched comparables, validate with authoritative sources",
        entity_scope="County and formation-specific",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Permian Basin Comparable Transaction Standard"
    ),
    DoctrineBlock(
        topic="Market Adjustment Factors",
        keywords=["market adjustment", "factors", "valuation", "market comparables", "oil and gas"],
        conclusion_template="Market adjustment factors are applied to comparable transactions to account for commodity price changes, regional demand, and macroeconomic trends.",
        reasoning_framework=(
            "Market adjustment factors are used to normalize comparable transaction values to current market conditions. "
            "Adjustments are made for commodity price fluctuations, regional demand shifts, and macroeconomic trends. "
            "Statistical normalization is applied to ensure comparability across different time periods. "
            "Authoritative sources such as commodity price indices and regional market reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying industry-standard adjustment methodologies."
        ),
        key_factors=[
            "Commodity price changes",
            "Regional demand",
            "Macroeconomic trends",
            "Statistical normalization"
        ],
        primary_authority=[
            "Commodity price indices",
            "Regional market reports",
            "Industry adjustment standards"
        ],
        burden_holder="Valuator",
        adversary_position="Counterparty disputes adjustment methodology",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Authoritative sources support methodology",
            "Statistical normalization ensures comparability"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="Market-wide",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="Permian Basin Market Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Time-Based Depreciation of Comparables",
        keywords=["time-based depreciation", "comparables", "valuation", "market comparables", "oil and gas"],
        conclusion_template="Comparable transaction values are depreciated based on elapsed time since transaction, using industry-standard depreciation rates and market trend analysis.",
        reasoning_framework=(
            "Time-based depreciation is applied to comparable transaction values to account for changes in market conditions since the transaction date. "
            "Industry-standard depreciation rates are referenced, adjusted for commodity price trends and regional demand. "
            "Statistical analysis is used to determine appropriate depreciation factors. "
            "Authoritative sources such as market trend reports and state lease auctions are used for validation. "
            "The conclusion is supported by controlling precedent and industry best practices."
        ),
        key_factors=[
            "Elapsed time since transaction",
            "Depreciation rates",
            "Commodity price trends",
            "Regional demand"
        ],
        primary_authority=[
            "Industry depreciation standards",
            "Market trend reports",
            "State lease auctions"
        ],
        burden_holder="Valuator",
        adversary_position="Counterparty disputes depreciation rate",
        counter_arguments=[
            "Depreciation rates are industry-standard",
            "Market trends support adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present time-based depreciation analysis, validate with authoritative sources",
        entity_scope="Market-wide",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="Texas State Lease Auction Depreciation Standard"
    ),
    DoctrineBlock(
        topic="Formation-Specific Valuations: Wolfcamp",
        keywords=["formation-specific", "Wolfcamp", "valuation", "market comparables", "oil and gas"],
        conclusion_template="The market value for Wolfcamp formation interests in {county} is determined by recent comparable transactions, adjusted for geological quality and operator activity.",
        reasoning_framework=(
            "Wolfcamp formation valuations are based on recent comparable transactions within the target county. "
            "Geological quality and operator activity are key factors influencing value. "
            "Transaction data is collected from industry databases and public records. "
            "Adjustments are made for commodity price environment and regional demand. "
            "The conclusion is validated by authoritative sources and controlling precedent from major Wolfcamp transactions."
        ),
        key_factors=[
            "Recent comparable transactions",
            "Geological quality",
            "Operator activity",
            "Commodity price environment"
        ],
        primary_authority=[
            "Industry transaction databases",
            "Public records",
            "Major Wolfcamp operator reports"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes value based on operator activity",
        counter_arguments=[
            "Operator activity supports higher value",
            "Geological quality is superior",
            "Market comparables validate conclusion"
        ],
        resolution_strategy="Present operator-adjusted comparables, validate with authoritative sources",
        entity_scope="Wolfcamp formation-specific",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Wolfcamp Formation Transaction Standard"
    ),
    DoctrineBlock(
        topic="Formation-Specific Valuations: Bone Spring",
        keywords=["formation-specific", "Bone Spring", "valuation", "market comparables", "oil and gas"],
        conclusion_template="The market value for Bone Spring formation interests in {county} is determined by recent comparable transactions, adjusted for geological quality and operator activity.",
        reasoning_framework=(
            "Bone Spring formation valuations are based on recent comparable transactions within the target county. "
            "Geological quality and operator activity are key factors influencing value. "
            "Transaction data is collected from industry databases and public records. "
            "Adjustments are made for commodity price environment and regional demand. "
            "The conclusion is validated by authoritative sources and controlling precedent from major Bone Spring transactions."
        ),
        key_factors=[
            "Recent comparable transactions",
            "Geological quality",
            "Operator activity",
            "Commodity price environment"
        ],
        primary_authority=[
            "Industry transaction databases",
            "Public records",
            "Major Bone Spring operator reports"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes value based on operator activity",
        counter_arguments=[
            "Operator activity supports higher value",
            "Geological quality is superior",
            "Market comparables validate conclusion"
        ],
        resolution_strategy="Present operator-adjusted comparables, validate with authoritative sources",
        entity_scope="Bone Spring formation-specific",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Bone Spring Formation Transaction Standard"
    ),
    DoctrineBlock(
        topic="Formation-Specific Valuations: Spraberry",
        keywords=["formation-specific", "Spraberry", "valuation", "market comparables", "oil and gas"],
        conclusion_template="The market value for Spraberry formation interests in {county} is determined by recent comparable transactions, adjusted for geological quality and operator activity.",
        reasoning_framework=(
            "Spraberry formation valuations are based on recent comparable transactions within the target county. "
            "Geological quality and operator activity are key factors influencing value. "
            "Transaction data is collected from industry databases and public records. "
            "Adjustments are made for commodity price environment and regional demand. "
            "The conclusion is validated by authoritative sources and controlling precedent from major Spraberry transactions."
        ),
        key_factors=[
            "Recent comparable transactions",
            "Geological quality",
            "Operator activity",
            "Commodity price environment"
        ],
        primary_authority=[
            "Industry transaction databases",
            "Public records",
            "Major Spraberry operator reports"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes value based on operator activity",
        counter_arguments=[
            "Operator activity supports higher value",
            "Geological quality is superior",
            "Market comparables validate conclusion"
        ],
        resolution_strategy="Present operator-adjusted comparables, validate with authoritative sources",
        entity_scope="Spraberry formation-specific",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Spraberry Formation Transaction Standard"
    ),
    DoctrineBlock(
        topic="Lease Bonus Rate Adjustment for Commodity Price Volatility",
        keywords=["lease bonus", "commodity price", "volatility", "market adjustment", "valuation"],
        conclusion_template="Lease bonus rates are adjusted for commodity price volatility using industry-standard adjustment factors and recent market trends.",
        reasoning_framework=(
            "Commodity price volatility is a significant factor in lease bonus rate determination. "
            "Adjustment factors are derived from commodity price indices and applied to recent comparable transactions. "
            "Market trends are analyzed to determine the direction and magnitude of adjustment. "
            "Authoritative sources such as state lease auctions and industry reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Commodity price indices",
            "Market trends",
            "Adjustment factors",
            "Recent comparable transactions"
        ],
        primary_authority=[
            "Commodity price indices",
            "State lease auctions",
            "Industry reports"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator disputes adjustment methodology",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Market trends support adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="County and formation-specific",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="Texas State Lease Auction Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Royalty Rate Adjustment for Lease Term Length",
        keywords=["royalty rate", "lease term", "adjustment", "market comparables", "valuation"],
        conclusion_template="Royalty rates are adjusted for lease term length using industry-standard adjustment factors and recent comparable leases.",
        reasoning_framework=(
            "Lease term length influences royalty rate negotiations. "
            "Adjustment factors are derived from industry-standard methodologies and applied to recent comparable leases. "
            "Longer lease terms may justify lower royalty rates, while shorter terms may command a premium. "
            "Authoritative sources such as state lease auctions and industry reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Lease term length",
            "Adjustment factors",
            "Recent comparable leases",
            "Industry standards"
        ],
        primary_authority=[
            "State lease auctions",
            "Industry reports",
            "Lease databases"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator proposes lower royalty for longer lease term",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Recent comparables support higher royalty",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="County and formation-specific",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="Texas State Lease Auction Royalty Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Mineral Deed Valuation Adjustment for Proximity to Drilling Activity",
        keywords=["mineral deed", "valuation", "proximity", "drilling activity", "market comparables"],
        conclusion_template="Mineral deed values are adjusted for proximity to active drilling using industry-standard adjustment factors and recent comparable sales.",
        reasoning_framework=(
            "Proximity to active drilling is a key factor in mineral deed valuation. "
            "Adjustment factors are derived from industry-standard methodologies and applied to recent comparable sales. "
            "Properties closer to active drilling command higher values. "
            "Authoritative sources such as county records and industry reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Proximity to drilling activity",
            "Adjustment factors",
            "Recent comparable sales",
            "Industry standards"
        ],
        primary_authority=[
            "County records",
            "Industry reports",
            "Broker databases"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes adjustment for proximity",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Recent comparables support higher value",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="County and formation-specific",
        confidence=0.82,
        confidence_zone="Medium",
        controlling_precedent="Permian Basin Mineral Sale Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Producing Property Valuation Adjustment for Decline Rate",
        keywords=["producing property", "valuation", "decline rate", "adjustment", "market comparables"],
        conclusion_template="Producing property values are adjusted for decline rate using industry-standard methodologies and recent comparable sales.",
        reasoning_framework=(
            "Decline rate is a critical factor in producing property valuation. "
            "Adjustment factors are derived from industry-standard methodologies and applied to recent comparable sales. "
            "Properties with lower decline rates command higher values. "
            "Authoritative sources such as operator disclosures and industry reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Decline rate",
            "Adjustment factors",
            "Recent comparable sales",
            "Industry standards"
        ],
        primary_authority=[
            "Operator disclosures",
            "Industry reports",
            "Transaction databases"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes adjustment for decline rate",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Recent comparables support higher value",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="Property-specific",
        confidence=0.81,
        confidence_zone="Medium",
        controlling_precedent="SEC PV-10 Decline Rate Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Working Interest Valuation Adjustment for Capital Cost Exposure",
        keywords=["working interest", "valuation", "capital cost", "exposure", "market comparables"],
        conclusion_template="Working interest values are adjusted for capital cost exposure using industry-standard methodologies and recent comparable transactions.",
        reasoning_framework=(
            "Capital cost exposure is a significant factor in working interest valuation. "
            "Adjustment factors are derived from industry-standard methodologies and applied to recent comparable transactions. "
            "Interests with higher capital cost exposure command lower values. "
            "Authoritative sources such as industry reports and operator disclosures are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Capital cost exposure",
            "Adjustment factors",
            "Recent comparable transactions",
            "Industry standards"
        ],
        primary_authority=[
            "Industry reports",
            "Operator disclosures",
            "Transaction databases"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes adjustment for capital cost exposure",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Recent comparables support lower value",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="Formation-specific",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="Permian Basin Working Interest Adjustment Standard"
    ),
    DoctrineBlock(
        topic="ORRI Valuation Adjustment for Revenue Share",
        keywords=["ORRI", "valuation", "revenue share", "adjustment", "market comparables"],
        conclusion_template="ORRI values are adjusted for revenue share percentage using industry-standard methodologies and recent comparable transactions.",
        reasoning_framework=(
            "Revenue share percentage is a key factor in ORRI valuation. "
            "Adjustment factors are derived from industry-standard methodologies and applied to recent comparable transactions. "
            "Interests with higher revenue share command higher values. "
            "Authoritative sources such as industry reports and operator disclosures are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Revenue share percentage",
            "Adjustment factors",
            "Recent comparable transactions",
            "Industry standards"
        ],
        primary_authority=[
            "Industry reports",
            "Operator disclosures",
            "Transaction databases"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes adjustment for revenue share",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Recent comparables support higher value",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="Formation-specific",
        confidence=0.79,
        confidence_zone="Medium",
        controlling_precedent="Permian Basin ORRI Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Net Mineral Acre Calculation Adjustment for Undivided Interests",
        keywords=["net mineral acre", "calculation", "undivided interests", "adjustment", "market comparables"],
        conclusion_template="Net mineral acre calculations are adjusted for undivided interests using industry-standard methodologies and recent comparable transactions.",
        reasoning_framework=(
            "Undivided interests require adjustment in net mineral acre calculations. "
            "Adjustment factors are derived from industry-standard methodologies and applied to recent comparable transactions. "
            "Fractional interests are calculated based on title documents and division orders. "
            "Authoritative sources such as county records and industry reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Undivided interests",
            "Adjustment factors",
            "Title documents",
            "Division orders"
        ],
        primary_authority=[
            "County records",
            "Industry reports",
            "Division orders"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator disputes calculation for undivided interests",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Title documents support calculation",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="Property-specific",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="Texas Mineral Ownership Calculation Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Comparable Transaction Identification Adjustment for Deal Structure",
        keywords=["comparable transaction", "identification", "deal structure", "adjustment", "market comparables"],
        conclusion_template="Comparable transactions are adjusted for deal structure differences using industry-standard methodologies and authoritative databases.",
        reasoning_framework=(
            "Deal structure differences require adjustment in comparable transaction identification. "
            "Adjustment factors are derived from industry-standard methodologies and applied to authoritative databases. "
            "Transactions are normalized to account for differences in payment structure, interest type, and lease terms. "
            "Authoritative sources such as industry databases and broker reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Deal structure differences",
            "Adjustment factors",
            "Payment structure",
            "Interest type",
            "Lease terms"
        ],
        primary_authority=[
            "Industry databases",
            "Broker reports",
            "Public records"
        ],
        burden_holder="Valuator",
        adversary_position="Counterparty disputes adjustment for deal structure",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Transactions are normalized",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="County and formation-specific",
        confidence=0.77,
        confidence_zone="Medium",
        controlling_precedent="Permian Basin Comparable Transaction Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Market Adjustment Factors for Regional Demand Shifts",
        keywords=["market adjustment", "regional demand", "shifts", "valuation", "market comparables"],
        conclusion_template="Market adjustment factors are applied for regional demand shifts using industry-standard methodologies and authoritative market reports.",
        reasoning_framework=(
            "Regional demand shifts require adjustment in market comparables. "
            "Adjustment factors are derived from industry-standard methodologies and applied to authoritative market reports. "
            "Demand trends are analyzed to determine the direction and magnitude of adjustment. "
            "Authoritative sources such as regional market reports and commodity price indices are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Regional demand shifts",
            "Adjustment factors",
            "Market reports",
            "Commodity price indices"
        ],
        primary_authority=[
            "Regional market reports",
            "Commodity price indices",
            "Industry standards"
        ],
        burden_holder="Valuator",
        adversary_position="Counterparty disputes adjustment for regional demand",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Market reports support adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="Market-wide",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="Permian Basin Market Adjustment Regional Demand Standard"
    ),
    DoctrineBlock(
        topic="Time-Based Depreciation Adjustment for Commodity Price Trends",
        keywords=["time-based depreciation", "commodity price", "trends", "adjustment", "market comparables"],
        conclusion_template="Time-based depreciation is adjusted for commodity price trends using industry-standard methodologies and authoritative market reports.",
        reasoning_framework=(
            "Commodity price trends require adjustment in time-based depreciation of comparables. "
            "Adjustment factors are derived from industry-standard methodologies and applied to authoritative market reports. "
            "Depreciation rates are adjusted based on commodity price direction and magnitude. "
            "Authoritative sources such as market trend reports and state lease auctions are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Commodity price trends",
            "Adjustment factors",
            "Depreciation rates",
            "Market reports"
        ],
        primary_authority=[
            "Market trend reports",
            "State lease auctions",
            "Industry standards"
        ],
        burden_holder="Valuator",
        adversary_position="Counterparty disputes adjustment for commodity price trends",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Market reports support adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="Market-wide",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="Texas State Lease Auction Depreciation Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Formation-Specific Valuation Adjustment for Operator Reputation: Wolfcamp",
        keywords=["formation-specific", "Wolfcamp", "operator reputation", "adjustment", "market comparables"],
        conclusion_template="Wolfcamp formation values are adjusted for operator reputation using industry-standard methodologies and recent comparable transactions.",
        reasoning_framework=(
            "Operator reputation is a key factor in Wolfcamp formation valuation. "
            "Adjustment factors are derived from industry-standard methodologies and applied to recent comparable transactions. "
            "Operators with strong reputations command higher values. "
            "Authoritative sources such as major operator reports and industry databases are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Operator reputation",
            "Adjustment factors",
            "Recent comparable transactions",
            "Industry standards"
        ],
        primary_authority=[
            "Major operator reports",
            "Industry databases",
            "Public records"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes adjustment for operator reputation",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Operator reputation supports higher value",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="Wolfcamp formation-specific",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="Wolfcamp Formation Operator Reputation Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Formation-Specific Valuation Adjustment for Geological Quality: Bone Spring",
        keywords=["formation-specific", "Bone Spring", "geological quality", "adjustment", "market comparables"],
        conclusion_template="Bone Spring formation values are adjusted for geological quality using industry-standard methodologies and recent comparable transactions.",
        reasoning_framework=(
            "Geological quality is a key factor in Bone Spring formation valuation. "
            "Adjustment factors are derived from industry-standard methodologies and applied to recent comparable transactions. "
            "Formations with superior geological quality command higher values. "
            "Authoritative sources such as major operator reports and industry databases are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Geological quality",
            "Adjustment factors",
            "Recent comparable transactions",
            "Industry standards"
        ],
        primary_authority=[
            "Major operator reports",
            "Industry databases",
            "Public records"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes adjustment for geological quality",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Geological quality supports higher value",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="Bone Spring formation-specific",
        confidence=0.73,
        confidence_zone="Medium",
        controlling_precedent="Bone Spring Formation Geological Quality Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Formation-Specific Valuation Adjustment for Operator Activity: Spraberry",
        keywords=["formation-specific", "Spraberry", "operator activity", "adjustment", "market comparables"],
        conclusion_template="Spraberry formation values are adjusted for operator activity using industry-standard methodologies and recent comparable transactions.",
        reasoning_framework=(
            "Operator activity is a key factor in Spraberry formation valuation. "
            "Adjustment factors are derived from industry-standard methodologies and applied to recent comparable transactions. "
            "Formations with higher operator activity command higher values. "
            "Authoritative sources such as major operator reports and industry databases are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Operator activity",
            "Adjustment factors",
            "Recent comparable transactions",
            "Industry standards"
        ],
        primary_authority=[
            "Major operator reports",
            "Industry databases",
            "Public records"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes adjustment for operator activity",
        counter_arguments=[
            "Adjustment factors are industry-standard",
            "Operator activity supports higher value",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present adjustment methodology, validate with authoritative sources",
        entity_scope="Spraberry formation-specific",
        confidence=0.72,
        confidence_zone="Medium",
        controlling_precedent="Spraberry Formation Operator Activity Adjustment Standard"
    ),
    DoctrineBlock(
        topic="Lease Bonus Rate Analysis for Multi-Formation Properties",
        keywords=["lease bonus", "multi-formation", "analysis", "market comparables", "valuation"],
        conclusion_template="Lease bonus rates for multi-formation properties are determined by weighted average of formation-specific comparables, adjusted for geological quality and operator activity.",
        reasoning_framework=(
            "Multi-formation properties require lease bonus rate analysis based on weighted average of formation-specific comparables. "
            "Weights are assigned based on acreage distribution and geological quality. "
            "Adjustment factors are applied for operator activity and commodity price environment. "
            "Authoritative sources such as industry databases and state lease auctions are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Acreage distribution",
            "Geological quality",
            "Operator activity",
            "Commodity price environment"
        ],
        primary_authority=[
            "Industry databases",
            "State lease auctions",
            "Major operator reports"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator disputes weighted average methodology",
        counter_arguments=[
            "Weighted average is industry-standard",
            "Formation-specific comparables support conclusion",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present weighted average analysis, validate with authoritative sources",
        entity_scope="Multi-formation properties",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Texas State Lease Auction Multi-Formation Analysis Standard"
    ),
    DoctrineBlock(
        topic="Royalty Rate Negotiation for Multi-Formation Properties",
        keywords=["royalty rate", "multi-formation", "negotiation", "market comparables", "valuation"],
        conclusion_template="Royalty rate negotiation for multi-formation properties is based on formation-specific comparables, adjusted for lease term and operator competition.",
        reasoning_framework=(
            "Multi-formation properties require royalty rate negotiation based on formation-specific comparables. "
            "Adjustment factors are applied for lease term and operator competition. "
            "Authoritative sources such as industry databases and state lease auctions are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Formation-specific comparables",
            "Lease term",
            "Operator competition",
            "Adjustment factors"
        ],
        primary_authority=[
            "Industry databases",
            "State lease auctions",
            "Major operator reports"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator proposes lower royalty for multi-formation property",
        counter_arguments=[
            "Formation-specific comparables support higher royalty",
            "Adjustment factors are industry-standard",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present formation-specific negotiation, validate with authoritative sources",
        entity_scope="Multi-formation properties",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Texas State Lease Auction Multi-Formation Royalty Standard"
    ),
    DoctrineBlock(
        topic="Mineral Deed Valuation for Multi-Formation Properties",
        keywords=["mineral deed", "multi-formation", "valuation", "market comparables", "oil and gas"],
        conclusion_template="Mineral deed valuation for multi-formation properties is based on weighted average of formation-specific comparables, adjusted for proximity to drilling and market trends.",
        reasoning_framework=(
            "Multi-formation properties require mineral deed valuation based on weighted average of formation-specific comparables. "
            "Weights are assigned based on acreage distribution and proximity to drilling activity. "
            "Adjustment factors are applied for market trends and commodity price environment. "
            "Authoritative sources such as county records and industry databases are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Acreage distribution",
            "Proximity to drilling activity",
            "Market trends",
            "Formation-specific comparables"
        ],
        primary_authority=[
            "County records",
            "Industry databases",
            "Broker reports"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes weighted average methodology",
        counter_arguments=[
            "Weighted average is industry-standard",
            "Formation-specific comparables support conclusion",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present weighted average analysis, validate with authoritative sources",
        entity_scope="Multi-formation properties",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="Permian Basin Mineral Sale Multi-Formation Standard"
    ),
    DoctrineBlock(
        topic="Producing Property PV-10 Valuation for Multi-Formation Properties",
        keywords=["producing property", "PV-10", "multi-formation", "valuation", "discounted cash flow"],
        conclusion_template="PV-10 valuation for multi-formation producing properties is based on formation-specific cash flow projections, weighted by production contribution and validated by comparable sales.",
        reasoning_framework=(
            "Multi-formation producing properties require PV-10 valuation based on formation-specific cash flow projections. "
            "Weights are assigned based on production contribution from each formation. "
            "Adjustment factors are applied for decline rates and commodity price environment. "
            "Authoritative sources such as operator disclosures and industry databases are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Production contribution",
            "Decline rates",
            "Commodity price environment",
            "Formation-specific cash flows"
        ],
        primary_authority=[
            "Operator disclosures",
            "Industry databases",
            "Transaction databases"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes weighted cash flow methodology",
        counter_arguments=[
            "Weighted cash flow is industry-standard",
            "Formation-specific comparables support conclusion",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present weighted cash flow analysis, validate with authoritative sources",
        entity_scope="Multi-formation properties",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="SEC PV-10 Multi-Formation Valuation Standard"
    ),
    DoctrineBlock(
        topic="Working Interest vs. ORRI Pricing for Multi-Formation Properties",
        keywords=["working interest", "ORRI", "multi-formation", "pricing", "market comparables"],
        conclusion_template="Pricing differential between working interest and ORRI for multi-formation properties is determined by weighted average of formation-specific comparables, adjusted for risk and revenue share.",
        reasoning_framework=(
            "Multi-formation properties require pricing analysis based on weighted average of formation-specific comparables for working interest and ORRI. "
            "Weights are assigned based on acreage distribution and risk exposure. "
            "Adjustment factors are applied for revenue share and commodity price environment. "
            "Authoritative sources such as industry databases and broker reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Acreage distribution",
            "Risk exposure",
            "Revenue share",
            "Formation-specific comparables"
        ],
        primary_authority=[
            "Industry databases",
            "Broker reports",
            "Transaction databases"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes weighted average methodology",
        counter_arguments=[
            "Weighted average is industry-standard",
            "Formation-specific comparables support conclusion",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present weighted average analysis, validate with authoritative sources",
        entity_scope="Multi-formation properties",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="Permian Basin Working Interest Multi-Formation Pricing Standard"
    ),
    DoctrineBlock(
        topic="Net Mineral Acre Calculation for Multi-Formation Properties",
        keywords=["net mineral acre", "multi-formation", "calculation", "ownership", "market comparables"],
        conclusion_template="Net mineral acre calculation for multi-formation properties is based on weighted average of formation-specific ownership fractions, validated by comparable transactions.",
        reasoning_framework=(
            "Multi-formation properties require net mineral acre calculation based on weighted average of formation-specific ownership fractions. "
            "Weights are assigned based on acreage distribution and title documents. "
            "Adjustment factors are applied for undivided interests and legal encumbrances. "
            "Authoritative sources such as county records and industry databases are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Acreage distribution",
            "Ownership fractions",
            "Undivided interests",
            "Title documents"
        ],
        primary_authority=[
            "County records",
            "Industry databases",
            "Division orders"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator disputes weighted average methodology",
        counter_arguments=[
            "Weighted average is industry-standard",
            "Ownership fractions are validated",
            "Authoritative sources support calculation"
        ],
        resolution_strategy="Present weighted average calculation, validate with authoritative sources",
        entity_scope="Multi-formation properties",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="Texas Mineral Ownership Multi-Formation Calculation Standard"
    ),
    DoctrineBlock(
        topic="Comparable Transaction Identification for Multi-Formation Properties",
        keywords=["comparable transaction", "multi-formation", "identification", "market comparables", "valuation"],
        conclusion_template="Comparable transactions for multi-formation properties are identified based on formation-specific parameters, weighted by acreage distribution and deal structure.",
        reasoning_framework=(
            "Multi-formation properties require comparable transaction identification based on formation-specific parameters. "
            "Weights are assigned based on acreage distribution and deal structure. "
            "Adjustment factors are applied for payment structure and interest type. "
            "Authoritative sources such as industry databases and broker reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Acreage distribution",
            "Deal structure",
            "Payment structure",
            "Interest type"
        ],
        primary_authority=[
            "Industry databases",
            "Broker reports",
            "Public records"
        ],
        burden_holder="Valuator",
        adversary_position="Counterparty disputes weighted average methodology",
        counter_arguments=[
            "Weighted average is industry-standard",
            "Formation-specific parameters support conclusion",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present weighted average analysis, validate with authoritative sources",
        entity_scope="Multi-formation properties",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="Permian Basin Comparable Transaction Multi-Formation Standard"
    ),
    DoctrineBlock(
        topic="Market Adjustment Factors for Multi-Formation Properties",
        keywords=["market adjustment", "multi-formation", "factors", "valuation", "market comparables"],
        conclusion_template="Market adjustment factors for multi-formation properties are applied based on weighted average of formation-specific adjustment factors and regional demand trends.",
        reasoning_framework=(
            "Multi-formation properties require market adjustment factors based on weighted average of formation-specific adjustment factors. "
            "Weights are assigned based on acreage distribution and regional demand trends. "
            "Adjustment factors are derived from industry-standard methodologies and applied to authoritative market reports. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Acreage distribution",
            "Regional demand trends",
            "Formation-specific adjustment factors",
            "Industry standards"
        ],
        primary_authority=[
            "Industry standards",
            "Market reports",
            "Commodity price indices"
        ],
        burden_holder="Valuator",
        adversary_position="Counterparty disputes weighted average adjustment methodology",
        counter_arguments=[
            "Weighted average is industry-standard",
            "Regional demand trends support adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present weighted average adjustment analysis, validate with authoritative sources",
        entity_scope="Multi-formation properties",
        confidence=0.82,
        confidence_zone="Medium",
        controlling_precedent="Permian Basin Market Adjustment Multi-Formation Standard"
    ),
    DoctrineBlock(
        topic="Time-Based Depreciation for Multi-Formation Properties",
        keywords=["time-based depreciation", "multi-formation", "comparables", "valuation", "market comparables"],
        conclusion_template="Time-based depreciation for multi-formation properties is applied based on weighted average of formation-specific depreciation rates and commodity price trends.",
        reasoning_framework=(
            "Multi-formation properties require time-based depreciation based on weighted average of formation-specific depreciation rates. "
            "Weights are assigned based on acreage distribution and commodity price trends. "
            "Depreciation rates are derived from industry-standard methodologies and applied to authoritative market reports. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Acreage distribution",
            "Commodity price trends",
            "Formation-specific depreciation rates",
            "Industry standards"
        ],
        primary_authority=[
            "Industry standards",
            "Market reports",
            "State lease auctions"
        ],
        burden_holder="Valuator",
        adversary_position="Counterparty disputes weighted average depreciation methodology",
        counter_arguments=[
            "Weighted average is industry-standard",
            "Commodity price trends support adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present weighted average depreciation analysis, validate with authoritative sources",
        entity_scope="Multi-formation properties",
        confidence=0.81,
        confidence_zone="Medium",
        controlling_precedent="Texas State Lease Auction Multi-Formation Depreciation Standard"
    ),
    DoctrineBlock(
        topic="Formation-Specific Valuation for Multi-Formation Properties: Wolfcamp",
        keywords=["formation-specific", "Wolfcamp", "multi-formation", "valuation", "market comparables"],
        conclusion_template="Wolfcamp formation values for multi-formation properties are determined by formation-specific comparables, weighted by acreage distribution and adjusted for operator activity.",
        reasoning_framework=(
            "Multi-formation properties require Wolfcamp formation valuation based on formation-specific comparables. "
            "Weights are assigned based on acreage distribution and operator activity. "
            "Adjustment factors are applied for commodity price environment and geological quality. "
            "Authoritative sources such as major operator reports and industry databases are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Acreage distribution",
            "Operator activity",
            "Commodity price environment",
            "Geological quality"
        ],
        primary_authority=[
            "Major operator reports",
            "Industry databases",
            "Public records"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes weighted average methodology",
        counter_arguments=[
            "Weighted average is industry-standard",
            "Formation-specific comparables support conclusion",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present weighted average analysis, validate with authoritative sources",
        entity_scope="Wolfcamp formation-specific",
        confidence=0.80,
        confidence_zone="Medium",
        controlling_precedent="Wolfcamp Formation Multi-Formation Valuation Standard"
    ),
    DoctrineBlock(
        topic="Formation-Specific Valuation for Multi-Formation Properties: Bone Spring",
        keywords=["formation-specific", "Bone Spring", "multi-formation", "valuation", "market comparables"],
        conclusion_template="Bone Spring formation values for multi-formation properties are determined by formation-specific comparables, weighted by acreage distribution and adjusted for geological quality.",
        reasoning_framework=(
            "Multi-formation properties require Bone Spring formation valuation based on formation-specific comparables. "
            "Weights are assigned based on acreage distribution and geological quality. "
            "Adjustment factors are applied for commodity price environment and operator activity. "
            "Authoritative sources such as major operator reports and industry databases are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Acreage distribution",
            "Geological quality",
            "Commodity price environment",
            "Operator activity"
        ],
        primary_authority=[
            "Major operator reports",
            "Industry databases",
            "Public records"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes weighted average methodology",
        counter_arguments=[
            "Weighted average is industry-standard",
            "Formation-specific comparables support conclusion",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present weighted average analysis, validate with authoritative sources",
        entity_scope="Bone Spring formation-specific",
        confidence=0.79,
        confidence_zone="Medium",
        controlling_precedent="Bone Spring Formation Multi-Formation Valuation Standard"
    ),
    DoctrineBlock(
        topic="Formation-Specific Valuation for Multi-Formation Properties: Spraberry",
        keywords=["formation-specific", "Spraberry", "multi-formation", "valuation", "market comparables"],
        conclusion_template="Spraberry formation values for multi-formation properties are determined by formation-specific comparables, weighted by acreage distribution and adjusted for operator activity.",
        reasoning_framework=(
            "Multi-formation properties require Spraberry formation valuation based on formation-specific comparables. "
            "Weights are assigned based on acreage distribution and operator activity. "
            "Adjustment factors are applied for commodity price environment and geological quality. "
            "Authoritative sources such as major operator reports and industry databases are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Acreage distribution",
            "Operator activity",
            "Commodity price environment",
            "Geological quality"
        ],
        primary_authority=[
            "Major operator reports",
            "Industry databases",
            "Public records"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes weighted average methodology",
        counter_arguments=[
            "Weighted average is industry-standard",
            "Formation-specific comparables support conclusion",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present weighted average analysis, validate with authoritative sources",
        entity_scope="Spraberry formation-specific",
        confidence=0.78,
        confidence_zone="Medium",
        controlling_precedent="Spraberry Formation Multi-Formation Valuation Standard"
    ),
    DoctrineBlock(
        topic="Lease Bonus Rate Analysis for Time-Based Depreciation",
        keywords=["lease bonus", "time-based depreciation", "analysis", "market comparables", "valuation"],
        conclusion_template="Lease bonus rates are depreciated based on elapsed time since comparable transaction, using industry-standard depreciation rates and market trend analysis.",
        reasoning_framework=(
            "Lease bonus rates require time-based depreciation analysis based on elapsed time since comparable transaction. "
            "Depreciation rates are derived from industry-standard methodologies and applied to recent market trends. "
            "Adjustment factors are applied for commodity price environment and regional demand. "
            "Authoritative sources such as state lease auctions and industry reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Elapsed time since transaction",
            "Depreciation rates",
            "Commodity price environment",
            "Regional demand"
        ],
        primary_authority=[
            "State lease auctions",
            "Industry reports",
            "Market trend databases"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator disputes depreciation rate methodology",
        counter_arguments=[
            "Depreciation rates are industry-standard",
            "Market trends support adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present depreciation analysis, validate with authoritative sources",
        entity_scope="County and formation-specific",
        confidence=0.77,
        confidence_zone="Medium",
        controlling_precedent="Texas State Lease Auction Depreciation Analysis Standard"
    ),
    DoctrineBlock(
        topic="Royalty Rate Negotiation for Time-Based Depreciation",
        keywords=["royalty rate", "time-based depreciation", "negotiation", "market comparables", "valuation"],
        conclusion_template="Royalty rates are depreciated based on elapsed time since comparable lease, using industry-standard depreciation rates and market trend analysis.",
        reasoning_framework=(
            "Royalty rates require time-based depreciation negotiation based on elapsed time since comparable lease. "
            "Depreciation rates are derived from industry-standard methodologies and applied to recent market trends. "
            "Adjustment factors are applied for lease term and operator competition. "
            "Authoritative sources such as state lease auctions and industry reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Elapsed time since lease",
            "Depreciation rates",
            "Lease term",
            "Operator competition"
        ],
        primary_authority=[
            "State lease auctions",
            "Industry reports",
            "Lease databases"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator disputes depreciation rate methodology",
        counter_arguments=[
            "Depreciation rates are industry-standard",
            "Lease term supports adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present depreciation analysis, validate with authoritative sources",
        entity_scope="County and formation-specific",
        confidence=0.76,
        confidence_zone="Medium",
        controlling_precedent="Texas State Lease Auction Royalty Depreciation Standard"
    ),
    DoctrineBlock(
        topic="Mineral Deed Valuation for Time-Based Depreciation",
        keywords=["mineral deed", "time-based depreciation", "valuation", "market comparables", "oil and gas"],
        conclusion_template="Mineral deed values are depreciated based on elapsed time since comparable sale, using industry-standard depreciation rates and market trend analysis.",
        reasoning_framework=(
            "Mineral deed values require time-based depreciation analysis based on elapsed time since comparable sale. "
            "Depreciation rates are derived from industry-standard methodologies and applied to recent market trends. "
            "Adjustment factors are applied for proximity to drilling activity and commodity price environment. "
            "Authoritative sources such as county records and industry reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Elapsed time since sale",
            "Depreciation rates",
            "Proximity to drilling activity",
            "Commodity price environment"
        ],
        primary_authority=[
            "County records",
            "Industry reports",
            "Market trend databases"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes depreciation rate methodology",
        counter_arguments=[
            "Depreciation rates are industry-standard",
            "Proximity to drilling supports adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present depreciation analysis, validate with authoritative sources",
        entity_scope="County and formation-specific",
        confidence=0.75,
        confidence_zone="Medium",
        controlling_precedent="Permian Basin Mineral Sale Depreciation Standard"
    ),
    DoctrineBlock(
        topic="Producing Property PV-10 Valuation for Time-Based Depreciation",
        keywords=["producing property", "PV-10", "time-based depreciation", "valuation", "discounted cash flow"],
        conclusion_template="PV-10 values for producing properties are depreciated based on elapsed time since comparable sale, using industry-standard depreciation rates and market trend analysis.",
        reasoning_framework=(
            "PV-10 values require time-based depreciation analysis based on elapsed time since comparable sale. "
            "Depreciation rates are derived from industry-standard methodologies and applied to recent market trends. "
            "Adjustment factors are applied for decline rates and commodity price environment. "
            "Authoritative sources such as operator disclosures and industry reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Elapsed time since sale",
            "Depreciation rates",
            "Decline rates",
            "Commodity price environment"
        ],
        primary_authority=[
            "Operator disclosures",
            "Industry reports",
            "Market trend databases"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes depreciation rate methodology",
        counter_arguments=[
            "Depreciation rates are industry-standard",
            "Decline rates support adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present depreciation analysis, validate with authoritative sources",
        entity_scope="Property-specific",
        confidence=0.74,
        confidence_zone="Medium",
        controlling_precedent="SEC PV-10 Depreciation Standard"
    ),
    DoctrineBlock(
        topic="Working Interest vs. ORRI Pricing for Time-Based Depreciation",
        keywords=["working interest", "ORRI", "time-based depreciation", "pricing", "market comparables"],
        conclusion_template="Pricing differential between working interest and ORRI is depreciated based on elapsed time since comparable transaction, using industry-standard depreciation rates and market trend analysis.",
        reasoning_framework=(
            "Working interest and ORRI pricing differentials require time-based depreciation analysis based on elapsed time since comparable transaction. "
            "Depreciation rates are derived from industry-standard methodologies and applied to recent market trends. "
            "Adjustment factors are applied for risk exposure and revenue share. "
            "Authoritative sources such as industry databases and broker reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Elapsed time since transaction",
            "Depreciation rates",
            "Risk exposure",
            "Revenue share"
        ],
        primary_authority=[
            "Industry databases",
            "Broker reports",
            "Market trend databases"
        ],
        burden_holder="Seller",
        adversary_position="Buyer disputes depreciation rate methodology",
        counter_arguments=[
            "Depreciation rates are industry-standard",
            "Risk exposure supports adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present depreciation analysis, validate with authoritative sources",
        entity_scope="Formation-specific",
        confidence=0.73,
        confidence_zone="Medium",
        controlling_precedent="Permian Basin Working Interest Depreciation Standard"
    ),
    DoctrineBlock(
        topic="Net Mineral Acre Calculation for Time-Based Depreciation",
        keywords=["net mineral acre", "time-based depreciation", "calculation", "ownership", "market comparables"],
        conclusion_template="Net mineral acre calculations are depreciated based on elapsed time since comparable transaction, using industry-standard depreciation rates and market trend analysis.",
        reasoning_framework=(
            "Net mineral acre calculations require time-based depreciation analysis based on elapsed time since comparable transaction. "
            "Depreciation rates are derived from industry-standard methodologies and applied to recent market trends. "
            "Adjustment factors are applied for undivided interests and legal encumbrances. "
            "Authoritative sources such as county records and industry reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Elapsed time since transaction",
            "Depreciation rates",
            "Undivided interests",
            "Legal encumbrances"
        ],
        primary_authority=[
            "County records",
            "Industry reports",
            "Market trend databases"
        ],
        burden_holder="Mineral owner",
        adversary_position="Operator disputes depreciation rate methodology",
        counter_arguments=[
            "Depreciation rates are industry-standard",
            "Undivided interests support adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present depreciation analysis, validate with authoritative sources",
        entity_scope="Property-specific",
        confidence=0.72,
        confidence_zone="Medium",
        controlling_precedent="Texas Mineral Ownership Depreciation Standard"
    ),
    DoctrineBlock(
        topic="Comparable Transaction Identification for Time-Based Depreciation",
        keywords=["comparable transaction", "time-based depreciation", "identification", "market comparables", "valuation"],
        conclusion_template="Comparable transactions are depreciated based on elapsed time since transaction, using industry-standard depreciation rates and market trend analysis.",
        reasoning_framework=(
            "Comparable transaction identification requires time-based depreciation analysis based on elapsed time since transaction. "
            "Depreciation rates are derived from industry-standard methodologies and applied to recent market trends. "
            "Adjustment factors are applied for deal structure and payment terms. "
            "Authoritative sources such as industry databases and broker reports are referenced. "
            "The conclusion is validated by cross-referencing multiple data sources and applying statistical normalization."
        ),
        key_factors=[
            "Elapsed time since transaction",
            "Depreciation rates",
            "Deal structure",
            "Payment terms"
        ],
        primary_authority=[
            "Industry databases",
            "Broker reports",
            "Market trend databases"
        ],
        burden_holder="Valuator",
        adversary_position="Counterparty disputes depreciation rate methodology",
        counter_arguments=[
            "Depreciation rates are industry-standard",
            "Deal structure supports adjustment",
            "Authoritative sources validate methodology"
        ],
        resolution_strategy="Present depreciation analysis, validate with authoritative sources",
        entity_scope="County and formation-specific",
        confidence=0.71,
        confidence_zone="Medium",
        controlling_precedent="Permian Basin Comparable Transaction Depreciation Standard"
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