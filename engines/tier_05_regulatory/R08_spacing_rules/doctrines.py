"""R08 SPACING RULES DOCTRINE CACHE
Well spacing and density rules for oil & gas operations.
Topics: Rule 37, Rule 38, density, pooling, special field rules, horizontal spacing
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class ConfidenceStratification(str, Enum):
    MANDATORY = "mandatory"
    CLEARLY_REQUIRED = "clearly_required"

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
    entity_scope: List[str]
    confidence: float
    confidence_stratification: ConfidenceStratification
    controlling_precedent: Optional[str] = None

RULE_37_SPACING = DoctrineBlock(
    topic="Rule 37 Well Spacing",
    keywords=["rule 37", "spacing", "property line", "lease line", "minimum distance", "spacing exception"],
    conclusion_template="Texas statewide Rule 37 requires oil wells to be at least 467 feet from lease lines and 1,200 feet from other wells on same lease (330-foot lease line, 660-foot between-well spacing for gas wells). Exceptions available through Railroad Commission application.",
    reasoning_framework="16 TAC §3.37 establishes minimum well spacing for oil and gas wells in Texas. Oil wells: 467 feet from lease/property lines, 1,200 feet from other oil wells on same lease. Gas wells: 330 feet from lease lines, 660 feet between wells. Purpose: prevent drainage of adjoining properties, ensure orderly field development, protect correlative rights. Exceptions: operators may apply for Rule 37 exception to drill closer to lease lines or other wells, must show: (1) undue hardship if exception denied, (2) no adverse impact on adjoining operators, (3) field development efficiency. Common exception scenarios: small leases (<40 acres for oil, <160 acres for gas), irregular lease shapes, existing drainage from offset wells, urban drilling. Exception process: file application with RRC, notify offset operators, may require hearing if protests filed. Denial: RRC can deny exception if drainage concerns or offset operator opposition. Horizontal wells: different spacing rules apply (see special provisions).",
    key_factors=["Oil wells: 467 ft from lease lines, 1,200 ft between wells", "Gas wells: 330 ft from lease lines, 660 ft between wells", "Exceptions available through RRC application", "Must show undue hardship and no drainage impact", "Offset operators have right to protest exception", "Horizontal wells have different spacing rules"],
    primary_authority=["16 TAC §3.37 (Spacing)", "Texas Natural Resources Code §85 (Correlative Rights)"],
    burden_holder="Operator seeking exception",
    adversary_position="Offset operators, Railroad Commission",
    counter_arguments=["Offset operators can protest exceptions", "RRC can deny if drainage concerns"],
    resolution_strategy="File Rule 37 exception application, notify offsets, demonstrate no drainage impact, negotiate with offset operators",
    entity_scope=["operator"],
    confidence=0.96,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="16 TAC §3.37"
)

RULE_38_DENSITY = DoctrineBlock(
    topic="Rule 38 Density and Proration Units",
    keywords=["rule 38", "density", "proration unit", "allocation", "allowable", "density exception"],
    conclusion_template="Texas statewide Rule 38 establishes proration units (40 acres for oil, 640 acres for gas) for allocation of production allowables. Density exceptions allow additional wells on proration units under specified conditions.",
    reasoning_framework="16 TAC §3.38 establishes proration units for allocation of production. Oil proration unit: 40 acres (660 ft x 2,640 ft). Gas proration unit: 640 acres (sections). One well per proration unit assigned allowable production. Purpose: prevent physical and economic waste, ensure fair allocation of production rights. Density exception: allows drilling additional wells on proration unit beyond one well. Criteria: show additional well will (1) prevent waste, (2) prevent drainage, (3) increase ultimate recovery, (4) be commercially productive. Common density scenarios: multiple pay zones (vertical density), horizontal wells (lateral density), enhanced recovery projects. Process: file Form W-1 with density request, technical data showing need, may require hearing. Allocation: production from multiple wells on same unit allocated among wells (each gets portion of allowable). Special field rules: many fields have field-specific density rules superseding Rule 38.",
    key_factors=["Oil proration unit: 40 acres", "Gas proration unit: 640 acres", "One well per unit gets full allowable", "Density exception allows additional wells on unit", "Must show prevention of waste/drainage or increased recovery", "Multiple wells on unit share allowable production", "Special field rules may supersede Rule 38"],
    primary_authority=["16 TAC §3.38 (Density)", "Field-Specific Rules"],
    burden_holder="Operator seeking density exception",
    adversary_position="Railroad Commission",
    counter_arguments=["Density exceptions require strong technical justification", "Special field rules may prohibit additional wells"],
    resolution_strategy="File density exception with technical data, demonstrate waste prevention or drainage, consider voluntary pooling to optimize spacing",
    entity_scope=["operator"],
    confidence=0.93,
    confidence_stratification=ConfidenceStratification.MANDATORY,
    controlling_precedent="16 TAC §3.38"
)

POOLING = DoctrineBlock(
    topic="Pooling (Voluntary and Forced)",
    keywords=["pooling", "voluntary pooling", "forced pooling", "mineral interest pooling", "pooling agreement", "unleased minerals"],
    conclusion_template="Texas allows voluntary pooling by agreement and forced pooling of mineral interests under certain conditions. Voluntary pooling: mineral owners agree to pool interests for development. Forced pooling: available under Mineral Interest Pooling Act for unleased interests in spacing units.",
    reasoning_framework="Pooling combines multiple mineral interests into single spacing unit for development. Voluntary pooling: mineral owners and operator agree to pool interests, typically through lease provisions or separate pooling agreement, each interest shares production pro-rata based on acreage. Forced pooling: Texas Mineral Interest Pooling Act (Natural Resources Code Chapter 102) allows operator to pool unleased mineral interests in spacing unit if: (1) operator has leases covering majority of unit, (2) unable to reach agreement with unleased owners, (3) RRC approves forced pooling application. Forced pooling process: file application with RRC, hearing required, unleased owners can participate (receive lease bonus and royalty) or not participate (receive cost-free royalty after operator recoups 200-300% of costs). Purpose: prevent waste from inability to develop spacing unit, protect correlative rights of all mineral owners. Controversy: forced pooling viewed as taking of property rights by some mineral owners. Urban drilling: forced pooling common for assembling urban drilling units.",
    key_factors=["Voluntary pooling by agreement among mineral owners", "Forced pooling for unleased interests under TX Natural Resources Code Ch. 102", "Operator must hold majority of unit acreage to force pool", "RRC hearing required for forced pooling", "Unleased owners can participate or take cost-free royalty", "Urban drilling commonly uses forced pooling"],
    primary_authority=["Texas Natural Resources Code Chapter 102 (Forced Pooling)", "16 TAC §3 (Pooling Rules)"],
    burden_holder="Operator seeking forced pooling",
    adversary_position="Unleased mineral owners, Railroad Commission",
    counter_arguments=["Forced pooling viewed as property rights taking", "RRC approval required and not guaranteed"],
    resolution_strategy="Negotiate voluntary pooling first, file forced pooling application if negotiations fail, demonstrate unit majority ownership",
    entity_scope=["operator", "mineral_owner"],
    confidence=0.88,
    confidence_stratification=ConfidenceStratification.CLEARLY_REQUIRED,
    controlling_precedent="Texas Natural Resources Code Chapter 102"
)

HORIZONTAL_SPACING = DoctrineBlock(
    topic="Horizontal Well Spacing",
    keywords=["horizontal well", "horizontal spacing", "lateral spacing", "multi-lateral", "stacked laterals", "horizontal rule 37"],
    conclusion_template="Horizontal wells in Texas have modified Rule 37 spacing requirements, typically requiring greater setbacks from lease lines and between laterals. Many fields have special horizontal spacing rules. Diagonal rule often applies for property line setbacks.",
    reasoning_framework="Horizontal wells drill laterally through reservoir, requiring different spacing than vertical wells. Modified Rule 37 for horizontals: lateral portion of wellbore (typically measured from first perforation to end of lateral) must comply with setback requirements, but specific distances vary by field. Common horizontal spacing: 330-660 feet from lease lines (measured perpendicular to lateral), 660-1,320 feet between laterals in same zone. Diagonal rule: setback measured from any point on lateral to nearest lease line. Multi-lateral spacing: multiple laterals from same vertical wellbore, each lateral separately spaced. Stacked laterals: multiple horizontal wells in different zones from same surface location, vertical spacing between zones (typically 200+ feet). Special field rules: major horizontal fields (Permian, Eagle Ford) have field-specific spacing rules, often 660 ft from lease lines, 1,320 ft between laterals. Exception process: horizontal Rule 37 exceptions common, must show no drainage impact on offsets. Urban drilling: horizontal wells allow development from small surface locations (pads).",
    key_factors=["Horizontal wells have modified Rule 37 spacing", "Typical: 330-660 ft from lease lines, 660-1,320 ft between laterals", "Diagonal rule: setback from any point on lateral", "Multi-laterals from same wellbore separately spaced", "Stacked laterals: vertical separation between zones", "Special field rules in major horizontal plays", "Rule 37 exceptions common for horizontal wells"],
    primary_authority=["16 TAC §3.37 (Horizontal Spacing)", "Field-Specific Horizontal Rules"],
    burden_holder="Operator",
    adversary_position="Offset operators, Railroad Commission",
    counter_arguments=["Field-specific rules vary widely", "Diagonal rule can be complex to apply"],
    resolution_strategy="Review field-specific horizontal spacing rules, apply for Rule 37 exception if needed, coordinate with offset operators on lateral spacing",
    entity_scope=["operator"],
    confidence=0.90,
    confidence_stratification=ConfidenceStratification.CLEARLY_REQUIRED,
    controlling_precedent="16 TAC §3.37 (Horizontal Provisions)"
)

URBAN_DRILLING = DoctrineBlock(
    topic="Urban Drilling Spacing",
    keywords=["urban drilling", "city ordinance", "municipal", "populated place", "protected use", "urban setback"],
    conclusion_template="Urban drilling in Texas cities must comply with both Railroad Commission spacing rules AND city ordinances, which often impose additional setbacks from protected uses (homes, schools, hospitals). City ordinances can be more restrictive than RRC rules.",
    reasoning_framework="Texas cities have authority to regulate surface location and operations of oil/gas wells within city limits. Urban drilling requirements: (1) RRC spacing rules (Rule 37/38) still apply, (2) city ordinances add additional restrictions (setbacks from homes/schools/churches/hospitals, noise limits, traffic management, visual screening, operating hours). Common urban setbacks: 600-1,500 feet from protected uses (varies by city). Fort Worth ordinance (leading example): 600 ft from protected uses, 1,200 ft from residential, noise limits, visual screening, traffic routes. Dallas: banned most urban drilling. Austin: very restrictive ordinances. Legal framework: Texas Local Government Code §81.0523 prohibits cities from banning drilling but allows 'reasonable' regulation of surface operations. Controversy: conflicts between cities and operators over what constitutes 'reasonable' regulation. Compliance: operators must obtain both RRC permits AND city permits/variances. Horizontal drilling: allows development of urban leases from pads outside city or in industrial areas.",
    key_factors=["Urban drilling subject to RRC rules AND city ordinances", "City ordinances often more restrictive (600-1,500 ft setbacks)", "Cities can regulate surface operations but not ban drilling", "Common restrictions: setbacks, noise, traffic, visual screening", "Fort Worth ordinance is leading model (600 ft from protected uses)", "Operators need RRC permits AND city permits", "Horizontal drilling can avoid urban surface locations"],
    primary_authority=["Texas Local Government Code §81.0523", "City Ordinances (Fort Worth, Dallas, Austin, etc.)", "16 TAC §3.37"],
    burden_holder="Operator",
    adversary_position="Cities, neighborhood groups, Railroad Commission",
    counter_arguments=["City ordinances can effectively prohibit drilling in many areas", "Legal disputes over 'reasonable' regulation are common"],
    resolution_strategy="Review city ordinances early, consider horizontal drilling from pads outside city, work with city staff on compliance, obtain necessary city permits",
    entity_scope=["operator"],
    confidence=0.87,
    confidence_stratification=ConfidenceStratification.CLEARLY_REQUIRED,
    controlling_precedent="Texas Local Government Code §81.0523"
)

DOCTRINE_CACHE = [RULE_37_SPACING, RULE_38_DENSITY, POOLING, HORIZONTAL_SPACING, URBAN_DRILLING]

def match_doctrines(query_text: str, keywords: List[str]) -> List[DoctrineBlock]:
    query_lower = query_text.lower()
    keyword_set = set(k.lower() for k in keywords)
    matches = []
    for doctrine in DOCTRINE_CACHE:
        doctrine_keywords = set(k.lower() for k in doctrine.keywords)
        overlap = len(keyword_set & doctrine_keywords)
        text_matches = sum(1 for dk in doctrine.keywords if dk.lower() in query_lower)
        total_score = overlap + text_matches
        if total_score > 0: matches.append((total_score, doctrine))
    matches.sort(key=lambda x: x[0], reverse=True)
    return [doctrine for score, doctrine in matches]
