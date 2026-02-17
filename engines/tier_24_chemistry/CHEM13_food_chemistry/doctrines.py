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
        topic="Macronutrient Chemistry: Carbohydrates",
        keywords=["carbohydrates", "monosaccharides", "disaccharides", "polysaccharides", "glycemic index", "fiber"],
        conclusion_template="Carbohydrates are classified based on their molecular structure and physiological impact.",
        reasoning_framework=(
            "Carbohydrates are organic compounds composed of carbon, hydrogen, and oxygen, typically in a ratio of 1:2:1. "
            "They are categorized into monosaccharides (glucose, fructose), disaccharides (sucrose, lactose), and polysaccharides (starch, cellulose). "
            "Digestibility, glycemic index, and fiber content determine their nutritional value and impact on health. "
            "The chemical structure influences enzymatic breakdown, absorption rate, and metabolic pathways. "
            "Dietary recommendations are based on balancing energy provision with minimizing rapid spikes in blood glucose. "
            "Fiber, a non-digestible carbohydrate, aids in gastrointestinal health and modulates absorption. "
            "Regulatory bodies such as the FDA and EFSA provide guidelines for carbohydrate labeling and health claims."
        ),
        key_factors=["structure", "digestibility", "glycemic index", "fiber", "regulation"],
        primary_authority=["FDA", "EFSA", "WHO"],
        burden_holder="Food manufacturer",
        adversary_position="Carbohydrates contribute to obesity and metabolic syndrome.",
        counter_arguments=[
            "Complex carbohydrates and fiber mitigate rapid glucose absorption.",
            "Balanced intake supports energy needs without adverse effects."
        ],
        resolution_strategy="Promote complex carbohydrates and fiber-rich foods; enforce accurate labeling.",
        entity_scope="Food products, dietary supplements",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FDA Nutrition Labeling and Education Act (NLEA) 1990"
    ),
    DoctrineBlock(
        topic="Macronutrient Chemistry: Proteins",
        keywords=["proteins", "amino acids", "essential amino acids", "denaturation", "enzymatic hydrolysis"],
        conclusion_template="Proteins are evaluated based on amino acid composition, digestibility, and functional properties.",
        reasoning_framework=(
            "Proteins are polymers of amino acids, essential for structural, enzymatic, and regulatory functions in food. "
            "The nutritional quality depends on the presence of essential amino acids and digestibility. "
            "Denaturation alters protein structure, affecting solubility and functionality. "
            "Enzymatic hydrolysis can improve digestibility and reduce allergenicity. "
            "Protein labeling must reflect true content and quality, as per regulatory standards. "
            "Functional properties such as gelation, foaming, and emulsification are critical in food formulation. "
            "Authorities like FDA and Codex Alimentarius set standards for protein claims and quality assessment."
        ),
        key_factors=["amino acid profile", "digestibility", "denaturation", "regulation"],
        primary_authority=["FDA", "Codex Alimentarius", "FAO"],
        burden_holder="Food producer",
        adversary_position="Plant proteins are inferior to animal proteins.",
        counter_arguments=[
            "Combining plant proteins can achieve complete amino acid profiles.",
            "Processing can enhance plant protein digestibility."
        ],
        resolution_strategy="Encourage diverse protein sources and accurate labeling.",
        entity_scope="Food products, supplements",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Codex Alimentarius Protein Quality Evaluation Guidelines"
    ),
    DoctrineBlock(
        topic="Macronutrient Chemistry: Lipids",
        keywords=["lipids", "fatty acids", "saturated", "unsaturated", "trans fats", "omega-3"],
        conclusion_template="Lipids are classified and regulated based on fatty acid composition and health impact.",
        reasoning_framework=(
            "Lipids, including triglycerides, phospholipids, and sterols, are essential for energy, cell structure, and signaling. "
            "Fatty acids are categorized as saturated, unsaturated (mono- and poly-), and trans fats. "
            "Trans fats are associated with increased cardiovascular risk and are subject to regulatory bans. "
            "Omega-3 fatty acids are beneficial for heart health and are promoted in dietary guidelines. "
            "Lipid oxidation leads to rancidity, affecting safety and quality. "
            "Labeling must accurately reflect lipid content and type, as per FDA and EFSA regulations."
        ),
        key_factors=["fatty acid profile", "oxidation", "regulation", "health impact"],
        primary_authority=["FDA", "EFSA", "AHA"],
        burden_holder="Food manufacturer",
        adversary_position="All fats are unhealthy and should be minimized.",
        counter_arguments=[
            "Unsaturated fats and omega-3s are beneficial.",
            "Trans fats are the primary concern for health."
        ],
        resolution_strategy="Promote healthy fats, eliminate trans fats, enforce labeling.",
        entity_scope="Food products, oils",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FDA Trans Fat Ban 2015"
    ),
    DoctrineBlock(
        topic="Maillard Reaction and Flavor Development",
        keywords=["Maillard reaction", "flavor", "browning", "amino acids", "reducing sugars"],
        conclusion_template="The Maillard reaction is a key process in flavor and color development during food processing.",
        reasoning_framework=(
            "The Maillard reaction occurs between amino acids and reducing sugars at elevated temperatures, leading to complex flavor and brown color formation. "
            "It is critical in baking, roasting, and frying. "
            "The reaction pathway depends on reactant concentration, temperature, and pH. "
            "While desirable for flavor, excessive Maillard reaction can produce harmful compounds like acrylamide. "
            "Balancing process parameters is essential for optimizing flavor while minimizing health risks."
        ),
        key_factors=["reactant concentration", "temperature", "pH", "health risk"],
        primary_authority=["FDA", "EFSA", "Food Chemistry Texts"],
        burden_holder="Food processor",
        adversary_position="Maillard reaction produces carcinogenic compounds.",
        counter_arguments=[
            "Process control can minimize harmful byproducts.",
            "Flavor benefits outweigh risks when managed."
        ],
        resolution_strategy="Optimize processing conditions; monitor acrylamide levels.",
        entity_scope="Processed foods",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EFSA Acrylamide Risk Assessment 2015"
    ),
    DoctrineBlock(
        topic="Food Preservation: Pasteurization",
        keywords=["pasteurization", "thermal processing", "microbial reduction", "milk", "juice"],
        conclusion_template="Pasteurization is a thermal process designed to reduce pathogenic microorganisms in food.",
        reasoning_framework=(
            "Pasteurization involves heating food to a specific temperature for a defined time to destroy pathogenic microorganisms. "
            "It is widely used in dairy and juice industries. "
            "The process parameters are set to balance microbial safety and preservation of sensory qualities. "
            "Regulatory standards specify minimum temperature-time combinations for effectiveness. "
            "Pasteurization does not sterilize but significantly reduces microbial load."
        ),
        key_factors=["temperature", "time", "microbial reduction", "regulation"],
        primary_authority=["FDA", "USDA", "Codex Alimentarius"],
        burden_holder="Food processor",
        adversary_position="Pasteurization destroys nutrients and flavor.",
        counter_arguments=[
            "Nutrient loss is minimal compared to safety benefits.",
            "Modern techniques preserve quality."
        ],
        resolution_strategy="Adopt optimized pasteurization protocols; communicate safety benefits.",
        entity_scope="Dairy, juices",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FDA Pasteurization Ordinance"
    ),
    DoctrineBlock(
        topic="Food Preservation: Sterilization",
        keywords=["sterilization", "thermal processing", "canning", "spores", "shelf life"],
        conclusion_template="Sterilization is a process that eliminates all forms of microbial life in food.",
        reasoning_framework=(
            "Sterilization involves heating food to temperatures sufficient to destroy all microorganisms, including spores. "
            "It is essential for canned foods and shelf-stable products. "
            "The process must ensure uniform heat distribution to prevent survival of pathogens. "
            "Regulatory standards dictate process validation and monitoring. "
            "Sterilization extends shelf life but may impact texture and flavor."
        ),
        key_factors=["temperature", "spore destruction", "process validation", "shelf life"],
        primary_authority=["FDA", "USDA", "Codex Alimentarius"],
        burden_holder="Food manufacturer",
        adversary_position="Sterilization degrades food quality.",
        counter_arguments=[
            "Safety outweighs minor quality loss.",
            "Advances in technology minimize degradation."
        ],
        resolution_strategy="Use advanced sterilization methods; validate process efficacy.",
        entity_scope="Canned foods, shelf-stable products",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FDA Low-Acid Canned Foods Regulation"
    ),
    DoctrineBlock(
        topic="Food Preservation: UHT",
        keywords=["UHT", "ultra-high temperature", "milk", "shelf life", "aseptic packaging"],
        conclusion_template="UHT processing extends shelf life by destroying microorganisms at ultra-high temperatures.",
        reasoning_framework=(
            "Ultra-high temperature (UHT) processing heats food to 135-150°C for a few seconds, destroying microorganisms and spores. "
            "It is used for milk and juices, enabling shelf-stable products without refrigeration. "
            "Aseptic packaging is required to prevent recontamination. "
            "UHT may affect flavor and nutrient profile but ensures safety and convenience."
        ),
        key_factors=["temperature", "aseptic packaging", "microbial destruction", "shelf life"],
        primary_authority=["FDA", "Codex Alimentarius", "EFSA"],
        burden_holder="Food processor",
        adversary_position="UHT alters taste and reduces nutrients.",
        counter_arguments=[
            "Nutrient loss is minimal.",
            "Shelf stability and safety are prioritized."
        ],
        resolution_strategy="Optimize UHT parameters; use flavor-preserving packaging.",
        entity_scope="Milk, juices",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Codex UHT Milk Standard"
    ),
    DoctrineBlock(
        topic="Water Activity (Aw) and Microbial Growth Limits",
        keywords=["water activity", "Aw", "microbial growth", "preservation", "mold"],
        conclusion_template="Water activity is a critical factor in controlling microbial growth and food spoilage.",
        reasoning_framework=(
            "Water activity (Aw) measures the availability of water for microbial growth. "
            "Foods with Aw below 0.6 are generally shelf-stable, as most bacteria cannot grow. "
            "Molds and yeasts can tolerate lower Aw, requiring additional controls. "
            "Reducing Aw through drying, salting, or sugar addition is a key preservation strategy. "
            "Regulatory standards specify Aw limits for different food categories."
        ),
        key_factors=["Aw threshold", "microbial tolerance", "preservation method", "regulation"],
        primary_authority=["FDA", "USDA", "EFSA"],
        burden_holder="Food manufacturer",
        adversary_position="Low Aw foods may still harbor pathogens.",
        counter_arguments=[
            "Pathogen risk is minimized but not eliminated.",
            "Additional hurdles (pH, preservatives) are used."
        ],
        resolution_strategy="Combine Aw control with other preservation methods.",
        entity_scope="Dried foods, confections",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FDA Water Activity Guidance"
    ),
    DoctrineBlock(
        topic="Food Additives: GRAS",
        keywords=["GRAS", "food additives", "FDA", "safety", "approval"],
        conclusion_template="GRAS status indicates that a food additive is generally recognized as safe by qualified experts.",
        reasoning_framework=(
            "GRAS (Generally Recognized As Safe) status is granted to substances with a long history of safe use or scientific evidence of safety. "
            "The FDA evaluates GRAS submissions based on expert consensus and published data. "
            "GRAS substances do not require premarket approval but must be used within specified limits. "
            "Transparency and documentation are essential for maintaining GRAS status."
        ),
        key_factors=["history of use", "scientific evidence", "expert consensus", "regulation"],
        primary_authority=["FDA", "Codex Alimentarius"],
        burden_holder="Additive manufacturer",
        adversary_position="GRAS process lacks rigorous oversight.",
        counter_arguments=[
            "GRAS requires expert review and public documentation.",
            "FDA can revoke GRAS status if safety concerns arise."
        ],
        resolution_strategy="Enhance transparency and monitoring of GRAS substances.",
        entity_scope="Food additives",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FDA GRAS Notification Program"
    ),
    DoctrineBlock(
        topic="Food Additives: E-numbers",
        keywords=["E-numbers", "additives", "EU", "EFSA", "regulation"],
        conclusion_template="E-numbers are codes assigned to food additives approved for use in the European Union.",
        reasoning_framework=(
            "E-numbers identify food additives that have been evaluated and approved by EFSA for safety and efficacy. "
            "Each additive is assigned a unique code and must comply with usage limits. "
            "E-numbers facilitate consumer awareness and regulatory enforcement. "
            "Periodic re-evaluation ensures continued safety."
        ),
        key_factors=["approval", "usage limits", "safety evaluation", "consumer awareness"],
        primary_authority=["EFSA", "European Commission"],
        burden_holder="Food manufacturer",
        adversary_position="E-numbers are linked to health risks.",
        counter_arguments=[
            "EFSA conducts rigorous safety assessments.",
            "Usage limits prevent adverse effects."
        ],
        resolution_strategy="Monitor additive safety; update E-number list as needed.",
        entity_scope="Food additives, EU products",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="EU Additives Regulation (EC) No 1333/2008"
    ),
    DoctrineBlock(
        topic="Food Additives: FDA Regulation",
        keywords=["FDA", "additives", "approval", "safety", "labeling"],
        conclusion_template="FDA regulates food additives through premarket approval, safety assessment, and labeling requirements.",
        reasoning_framework=(
            "Food additives must undergo FDA review for safety and efficacy before approval. "
            "Manufacturers submit data on toxicology, usage, and exposure. "
            "Approved additives are listed in the CFR and must be labeled accurately. "
            "Periodic review ensures ongoing safety."
        ),
        key_factors=["premarket approval", "safety assessment", "labeling", "regulation"],
        primary_authority=["FDA"],
        burden_holder="Additive manufacturer",
        adversary_position="FDA approval process is slow and burdensome.",
        counter_arguments=[
            "Rigorous review protects public health.",
            "Expedited pathways exist for urgent needs."
        ],
        resolution_strategy="Streamline approval process; maintain safety standards.",
        entity_scope="Food additives",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="FDA Food Additive Amendment 1958"
    ),
    DoctrineBlock(
        topic="Emulsification: HLB",
        keywords=["emulsification", "HLB", "hydrophilic-lipophilic balance", "surfactants", "stability"],
        conclusion_template="HLB value guides the selection of surfactants for stable emulsions in food systems.",
        reasoning_framework=(
            "Hydrophilic-lipophilic balance (HLB) quantifies the affinity of surfactants for water and oil. "
            "Surfactants with appropriate HLB values stabilize oil-in-water or water-in-oil emulsions. "
            "Emulsion stability depends on surfactant concentration, HLB, and process conditions. "
            "Regulatory bodies set limits for surfactant use in foods."
        ),
        key_factors=["HLB value", "surfactant concentration", "emulsion type", "regulation"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food formulator",
        adversary_position="Synthetic surfactants pose health risks.",
        counter_arguments=[
            "Approved surfactants are evaluated for safety.",
            "Natural alternatives are available."
        ],
        resolution_strategy="Use safe, approved surfactants; optimize HLB for stability.",
        entity_scope="Emulsified foods",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="FDA Emulsifier Regulation"
    ),
    DoctrineBlock(
        topic="Emulsification: Surfactant Stability",
        keywords=["emulsification", "surfactant", "stability", "droplet size", "coalescence"],
        conclusion_template="Surfactant stability is essential for maintaining emulsion integrity in food products.",
        reasoning_framework=(
            "Surfactants reduce interfacial tension, preventing droplet coalescence in emulsions. "
            "Stability is affected by surfactant type, concentration, and environmental factors (pH, temperature). "
            "Regular testing ensures emulsion quality and shelf life. "
            "Regulatory standards specify allowable surfactants and concentrations."
        ),
        key_factors=["surfactant type", "concentration", "environmental factors", "regulation"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food manufacturer",
        adversary_position="Emulsions break down during storage.",
        counter_arguments=[
            "Proper formulation and storage conditions maintain stability.",
            "Advanced surfactants improve shelf life."
        ],
        resolution_strategy="Optimize formulation; monitor stability during shelf life.",
        entity_scope="Emulsified foods",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="EFSA Emulsifier Safety Assessment"
    ),
    DoctrineBlock(
        topic="Starch Gelatinization",
        keywords=["starch", "gelatinization", "temperature", "water", "texture"],
        conclusion_template="Starch gelatinization is a thermal process that transforms granular starch into a viscous gel.",
        reasoning_framework=(
            "Gelatinization occurs when starch granules absorb water and swell upon heating, disrupting crystalline structure. "
            "The process is critical for texture development in baked goods, sauces, and puddings. "
            "Gelatinization temperature varies by starch type and affects final product quality. "
            "Monitoring process parameters ensures consistent texture and prevents defects."
        ),
        key_factors=["temperature", "water content", "starch type", "texture"],
        primary_authority=["Food Chemistry Texts", "FDA"],
        burden_holder="Food processor",
        adversary_position="Gelatinization leads to undesirable texture changes.",
        counter_arguments=[
            "Process control prevents defects.",
            "Modified starches can improve texture."
        ],
        resolution_strategy="Optimize gelatinization parameters; use suitable starch types.",
        entity_scope="Baked goods, sauces",
        confidence=0.85,
        confidence_zone="High",
        controlling_precedent="FDA Starch Regulation"
    ),
    DoctrineBlock(
        topic="Starch Retrogradation",
        keywords=["starch", "retrogradation", "texture", "bread staling", "amylose"],
        conclusion_template="Starch retrogradation causes texture changes and staling in cooked foods.",
        reasoning_framework=(
            "Retrogradation is the realignment of gelatinized starch molecules, primarily amylose, upon cooling. "
            "It leads to firming and staling in bread and other products. "
            "The rate depends on starch type, moisture, and temperature. "
            "Enzymes and additives can mitigate retrogradation effects."
        ),
        key_factors=["amylose content", "moisture", "temperature", "additives"],
        primary_authority=["Food Chemistry Texts", "FDA"],
        burden_holder="Food manufacturer",
        adversary_position="Retrogradation reduces product shelf life.",
        counter_arguments=[
            "Additives and process control can slow retrogradation.",
            "Modified starches resist retrogradation."
        ],
        resolution_strategy="Use anti-staling agents; optimize storage conditions.",
        entity_scope="Baked goods, starch-based foods",
        confidence=0.84,
        confidence_zone="High",
        controlling_precedent="FDA Bread Staling Guidance"
    ),
    DoctrineBlock(
        topic="Starch Modification",
        keywords=["starch", "modification", "chemical", "physical", "functional properties"],
        conclusion_template="Starch modification enhances functional properties for specific food applications.",
        reasoning_framework=(
            "Starch can be modified chemically or physically to improve properties such as viscosity, stability, and resistance to retrogradation. "
            "Modified starches are used in sauces, desserts, and processed foods. "
            "Safety and labeling requirements apply to modified starches."
        ),
        key_factors=["modification method", "functional property", "safety", "labeling"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Starch manufacturer",
        adversary_position="Modified starches are unnatural and unsafe.",
        counter_arguments=[
            "Approved modifications are safe.",
            "Functional benefits outweigh concerns."
        ],
        resolution_strategy="Use safe modification methods; ensure accurate labeling.",
        entity_scope="Processed foods",
        confidence=0.83,
        confidence_zone="High",
        controlling_precedent="FDA Modified Starch Regulation"
    ),
    DoctrineBlock(
        topic="Protein Denaturation",
        keywords=["protein", "denaturation", "heat", "pH", "structure"],
        conclusion_template="Protein denaturation alters structure and functionality, impacting food texture and digestibility.",
        reasoning_framework=(
            "Denaturation disrupts the native structure of proteins through heat, pH, or mechanical action. "
            "It affects solubility, gelation, and digestibility. "
            "Controlled denaturation is used to improve texture and reduce allergenicity. "
            "Excessive denaturation may reduce nutritional quality."
        ),
        key_factors=["denaturation method", "structure", "functionality", "digestibility"],
        primary_authority=["Food Chemistry Texts", "FDA"],
        burden_holder="Food processor",
        adversary_position="Denaturation destroys protein nutrition.",
        counter_arguments=[
            "Moderate denaturation improves digestibility.",
            "Process control preserves nutrition."
        ],
        resolution_strategy="Control denaturation conditions; monitor nutritional impact.",
        entity_scope="Processed foods",
        confidence=0.82,
        confidence_zone="High",
        controlling_precedent="FDA Protein Processing Guidance"
    ),
    DoctrineBlock(
        topic="Protein Gelation",
        keywords=["protein", "gelation", "heat", "texture", "egg"],
        conclusion_template="Protein gelation forms a three-dimensional network, providing structure and texture in foods.",
        reasoning_framework=(
            "Gelation occurs when proteins unfold and aggregate, forming a network that traps water. "
            "It is essential in products like tofu, custards, and gels. "
            "Gelation conditions (heat, pH, ionic strength) affect texture and water retention. "
            "Regulatory standards ensure safety and quality."
        ),
        key_factors=["gelation conditions", "protein type", "texture", "regulation"],
        primary_authority=["FDA", "Food Chemistry Texts"],
        burden_holder="Food manufacturer",
        adversary_position="Gelation leads to undesirable textures.",
        counter_arguments=[
            "Process control achieves desired texture.",
            "Protein selection affects gel quality."
        ],
        resolution_strategy="Optimize gelation parameters; select suitable proteins.",
        entity_scope="Gelled foods",
        confidence=0.81,
        confidence_zone="High",
        controlling_precedent="FDA Gelled Food Regulation"
    ),
    DoctrineBlock(
        topic="Protein Foaming",
        keywords=["protein", "foaming", "egg white", "air incorporation", "texture"],
        conclusion_template="Protein foaming stabilizes air incorporation, contributing to texture in foods like meringues.",
        reasoning_framework=(
            "Proteins stabilize air bubbles by forming viscoelastic films at the air-water interface. "
            "Foaming is critical in bakery and confectionery products. "
            "Foam stability depends on protein type, concentration, and process conditions. "
            "Additives can enhance foam stability."
        ),
        key_factors=["protein type", "concentration", "process conditions", "foam stability"],
        primary_authority=["FDA", "Food Chemistry Texts"],
        burden_holder="Food processor",
        adversary_position="Foams collapse during storage.",
        counter_arguments=[
            "Additives and process control improve stability.",
            "Protein selection is key."
        ],
        resolution_strategy="Use stabilizers; optimize foaming parameters.",
        entity_scope="Bakery, confectionery",
        confidence=0.80,
        confidence_zone="High",
        controlling_precedent="FDA Bakery Product Regulation"
    ),
    DoctrineBlock(
        topic="Lipid Oxidation",
        keywords=["lipid", "oxidation", "rancidity", "antioxidants", "shelf life"],
        conclusion_template="Lipid oxidation leads to rancidity, affecting flavor, safety, and shelf life.",
        reasoning_framework=(
            "Lipid oxidation is a chain reaction initiated by heat, light, or metal ions. "
            "It produces off-flavors, toxic compounds, and reduces shelf life. "
            "Antioxidants (natural or synthetic) are used to inhibit oxidation. "
            "Storage conditions (temperature, packaging) affect oxidation rate."
        ),
        key_factors=["oxidation initiators", "antioxidants", "storage", "shelf life"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food manufacturer",
        adversary_position="Antioxidants may pose health risks.",
        counter_arguments=[
            "Approved antioxidants are safe.",
            "Natural antioxidants are preferred."
        ],
        resolution_strategy="Use safe antioxidants; optimize storage and packaging.",
        entity_scope="Oils, processed foods",
        confidence=0.79,
        confidence_zone="High",
        controlling_precedent="FDA Antioxidant Regulation"
    ),
    DoctrineBlock(
        topic="Rancidity",
        keywords=["rancidity", "lipid", "oxidation", "flavor", "safety"],
        conclusion_template="Rancidity is the result of lipid oxidation, producing undesirable flavors and potential toxins.",
        reasoning_framework=(
            "Rancidity occurs when lipids oxidize, forming volatile compounds with off-flavors and odors. "
            "It can also produce toxic substances. "
            "Prevention involves antioxidant use, proper packaging, and storage. "
            "Regulatory standards limit exposure to rancid products."
        ),
        key_factors=["oxidation", "antioxidants", "packaging", "regulation"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food manufacturer",
        adversary_position="Rancid foods are unsafe for consumption.",
        counter_arguments=[
            "Regulations limit rancidity in foods.",
            "Quality control prevents unsafe products."
        ],
        resolution_strategy="Monitor lipid oxidation; enforce quality standards.",
        entity_scope="Oils, processed foods",
        confidence=0.78,
        confidence_zone="High",
        controlling_precedent="FDA Rancidity Guidance"
    ),
    DoctrineBlock(
        topic="Antioxidants",
        keywords=["antioxidants", "lipid oxidation", "vitamin E", "BHA", "BHT"],
        conclusion_template="Antioxidants inhibit lipid oxidation, preserving flavor and safety in foods.",
        reasoning_framework=(
            "Antioxidants scavenge free radicals, preventing lipid oxidation and rancidity. "
            "Natural antioxidants (vitamin E, C) and synthetic (BHA, BHT) are used. "
            "Regulatory bodies set limits for antioxidant use. "
            "Consumer preference favors natural antioxidants."
        ),
        key_factors=["antioxidant type", "concentration", "regulation", "consumer preference"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food manufacturer",
        adversary_position="Synthetic antioxidants are unsafe.",
        counter_arguments=[
            "Approved antioxidants are safe at regulated levels.",
            "Natural alternatives are available."
        ],
        resolution_strategy="Use natural antioxidants where possible; comply with regulations.",
        entity_scope="Oils, processed foods",
        confidence=0.77,
        confidence_zone="High",
        controlling_precedent="FDA Antioxidant Regulation"
    ),
    DoctrineBlock(
        topic="Food Safety: HACCP Critical Control Points",
        keywords=["HACCP", "critical control points", "food safety", "hazard analysis", "monitoring"],
        conclusion_template="HACCP identifies and monitors critical control points to ensure food safety.",
        reasoning_framework=(
            "Hazard Analysis and Critical Control Points (HACCP) is a systematic approach to food safety. "
            "It identifies hazards, establishes critical control points, and sets monitoring procedures. "
            "HACCP is mandatory for many food sectors. "
            "Documentation and verification are essential for compliance."
        ),
        key_factors=["hazard analysis", "control points", "monitoring", "documentation"],
        primary_authority=["FDA", "Codex Alimentarius"],
        burden_holder="Food manufacturer",
        adversary_position="HACCP is burdensome and ineffective.",
        counter_arguments=[
            "HACCP reduces foodborne illness.",
            "Process control improves safety."
        ],
        resolution_strategy="Streamline HACCP implementation; provide training.",
        entity_scope="Food processing",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Codex HACCP Guidelines"
    ),
    DoctrineBlock(
        topic="Microbial Contamination: Salmonella",
        keywords=["Salmonella", "microbial contamination", "foodborne illness", "testing", "control"],
        conclusion_template="Salmonella is a major foodborne pathogen requiring rigorous control and testing.",
        reasoning_framework=(
            "Salmonella can contaminate a wide range of foods, causing severe illness. "
            "Control measures include thermal processing, sanitation, and regular testing. "
            "Regulatory bodies set zero tolerance for Salmonella in certain foods. "
            "Rapid detection methods improve response."
        ),
        key_factors=["testing", "control measures", "regulation", "sanitation"],
        primary_authority=["FDA", "CDC", "EFSA"],
        burden_holder="Food manufacturer",
        adversary_position="Testing is insufficient to prevent outbreaks.",
        counter_arguments=[
            "Combined controls reduce risk.",
            "Rapid detection improves safety."
        ],
        resolution_strategy="Integrate testing with process controls; enforce zero tolerance.",
        entity_scope="High-risk foods",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FDA Salmonella Guidance"
    ),
    DoctrineBlock(
        topic="Microbial Contamination: Listeria",
        keywords=["Listeria", "microbial contamination", "ready-to-eat", "testing", "control"],
        conclusion_template="Listeria requires stringent controls in ready-to-eat foods due to its resilience.",
        reasoning_framework=(
            "Listeria monocytogenes can survive and grow at refrigeration temperatures. "
            "Ready-to-eat foods are particularly vulnerable. "
            "Controls include sanitation, testing, and process validation. "
            "Regulatory bodies enforce strict limits and recall procedures."
        ),
        key_factors=["testing", "sanitation", "process validation", "regulation"],
        primary_authority=["FDA", "CDC", "EFSA"],
        burden_holder="Food manufacturer",
        adversary_position="Listeria is impossible to eliminate.",
        counter_arguments=[
            "Stringent controls minimize risk.",
            "Rapid detection enables recalls."
        ],
        resolution_strategy="Enforce sanitation; use rapid testing.",
        entity_scope="Ready-to-eat foods",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FDA Listeria Guidance"
    ),
    DoctrineBlock(
        topic="Microbial Contamination: E. coli",
        keywords=["E. coli", "microbial contamination", "testing", "control", "foodborne illness"],
        conclusion_template="E. coli control relies on testing, sanitation, and thermal processing.",
        reasoning_framework=(
            "Pathogenic E. coli strains cause severe illness. "
            "Control measures include sanitation, testing, and cooking. "
            "Regulatory bodies set limits and require rapid detection. "
            "Outbreaks are managed through recalls and public notification."
        ),
        key_factors=["testing", "sanitation", "thermal processing", "regulation"],
        primary_authority=["FDA", "CDC", "EFSA"],
        burden_holder="Food manufacturer",
        adversary_position="Testing cannot prevent all outbreaks.",
        counter_arguments=[
            "Combined controls reduce risk.",
            "Public notification limits exposure."
        ],
        resolution_strategy="Integrate testing with process controls; enforce recalls.",
        entity_scope="High-risk foods",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="FDA E. coli Guidance"
    ),
    DoctrineBlock(
        topic="Mycotoxin Detection: Aflatoxin",
        keywords=["aflatoxin", "mycotoxin", "detection", "testing", "regulation"],
        conclusion_template="Aflatoxin detection and control are critical for food safety due to carcinogenicity.",
        reasoning_framework=(
            "Aflatoxins are produced by Aspergillus species and are potent carcinogens. "
            "Testing methods include HPLC, ELISA, and rapid kits. "
            "Regulatory bodies set strict limits and require regular testing. "
            "Control involves proper storage and sorting."
        ),
        key_factors=["testing method", "storage", "regulation", "sorting"],
        primary_authority=["FDA", "EFSA", "Codex Alimentarius"],
        burden_holder="Food manufacturer",
        adversary_position="Testing is expensive and unreliable.",
        counter_arguments=[
            "Rapid kits improve reliability.",
            "Strict regulation protects health."
        ],
        resolution_strategy="Use validated testing methods; enforce storage controls.",
        entity_scope="Grains, nuts",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="Codex Aflatoxin Standard"
    ),
    DoctrineBlock(
        topic="Mycotoxin Detection: Ochratoxin",
        keywords=["ochratoxin", "mycotoxin", "detection", "testing", "regulation"],
        conclusion_template="Ochratoxin detection is essential for food safety, especially in cereals and coffee.",
        reasoning_framework=(
            "Ochratoxins are produced by Aspergillus and Penicillium species. "
            "Testing methods include HPLC, ELISA, and rapid kits. "
            "Regulatory bodies set limits and require regular monitoring. "
            "Proper storage reduces risk."
        ),
        key_factors=["testing method", "storage", "regulation", "monitoring"],
        primary_authority=["FDA", "EFSA", "Codex Alimentarius"],
        burden_holder="Food manufacturer",
        adversary_position="Testing is insufficient for safety.",
        counter_arguments=[
            "Combined controls reduce risk.",
            "Rapid kits improve detection."
        ],
        resolution_strategy="Use validated testing; enforce storage controls.",
        entity_scope="Cereals, coffee",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="Codex Ochratoxin Standard"
    ),
    DoctrineBlock(
        topic="Pesticide Residue: MRL Analysis",
        keywords=["pesticide residue", "MRL", "maximum residue limit", "testing", "regulation"],
        conclusion_template="MRL analysis ensures pesticide residues in food do not exceed regulatory limits.",
        reasoning_framework=(
            "Maximum residue limits (MRLs) are set by regulatory bodies to protect consumer health. "
            "Testing methods include GC-MS and LC-MS. "
            "Compliance is mandatory for food producers. "
            "Regular monitoring and reporting are required."
        ),
        key_factors=["MRL", "testing method", "regulation", "monitoring"],
        primary_authority=["FDA", "EPA", "EFSA"],
        burden_holder="Food producer",
        adversary_position="MRLs are too lenient.",
        counter_arguments=[
            "MRLs are based on toxicological data.",
            "Regular review ensures safety."
        ],
        resolution_strategy="Update MRLs as needed; enforce testing.",
        entity_scope="Fruits, vegetables",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="EPA MRL Regulation"
    ),
    DoctrineBlock(
        topic="Pesticide Residue: GC-MS",
        keywords=["pesticide residue", "GC-MS", "testing", "analysis", "regulation"],
        conclusion_template="GC-MS is a sensitive method for detecting pesticide residues in food.",
        reasoning_framework=(
            "Gas chromatography-mass spectrometry (GC-MS) enables precise detection of pesticide residues. "
            "It is used for regulatory compliance and safety assessment. "
            "Sample preparation and method validation are critical. "
            "Regulatory bodies require regular testing."
        ),
        key_factors=["GC-MS", "method validation", "sample preparation", "regulation"],
        primary_authority=["FDA", "EPA", "EFSA"],
        burden_holder="Food producer",
        adversary_position="GC-MS is expensive and inaccessible.",
        counter_arguments=[
            "GC-MS is standard for regulatory compliance.",
            "Alternative methods are available."
        ],
        resolution_strategy="Use validated methods; provide access to testing labs.",
        entity_scope="Fruits, vegetables",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="EPA Pesticide Testing Guidance"
    ),
    DoctrineBlock(
        topic="Pesticide Residue: LC-MS",
        keywords=["pesticide residue", "LC-MS", "testing", "analysis", "regulation"],
        conclusion_template="LC-MS is a versatile method for detecting a wide range of pesticide residues.",
        reasoning_framework=(
            "Liquid chromatography-mass spectrometry (LC-MS) detects multiple pesticide residues with high sensitivity. "
            "It is used for regulatory compliance and safety assessment. "
            "Sample preparation and method validation are essential. "
            "Regulatory bodies require regular testing."
        ),
        key_factors=["LC-MS", "method validation", "sample preparation", "regulation"],
        primary_authority=["FDA", "EPA", "EFSA"],
        burden_holder="Food producer",
        adversary_position="LC-MS is costly and complex.",
        counter_arguments=[
            "LC-MS enables comprehensive testing.",
            "Training improves accessibility."
        ],
        resolution_strategy="Use validated methods; provide training.",
        entity_scope="Fruits, vegetables",
        confidence=0.92,
        confidence_zone="Very High",
        controlling_precedent="EFSA Pesticide Testing Guidance"
    ),
    DoctrineBlock(
        topic="Food Allergen Labeling: Big 9",
        keywords=["allergen", "labeling", "Big 9", "FALCPA", "regulation"],
        conclusion_template="Labeling of the Big 9 allergens is mandatory for consumer safety.",
        reasoning_framework=(
            "The Big 9 allergens (milk, eggs, fish, shellfish, tree nuts, peanuts, wheat, soybeans, sesame) must be declared on food labels. "
            "Regulatory bodies enforce strict labeling requirements. "
            "Cross-contamination controls are required in manufacturing. "
            "Consumer awareness is critical for safety."
        ),
        key_factors=["allergen declaration", "labeling", "cross-contamination", "regulation"],
        primary_authority=["FDA", "FALCPA"],
        burden_holder="Food manufacturer",
        adversary_position="Labeling is insufficient for allergen safety.",
        counter_arguments=[
            "Strict controls minimize risk.",
            "Consumer education is ongoing."
        ],
        resolution_strategy="Enforce labeling; provide education.",
        entity_scope="Packaged foods",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FALCPA 2004"
    ),
    DoctrineBlock(
        topic="Food Allergen Labeling: FALCPA",
        keywords=["FALCPA", "allergen", "labeling", "regulation", "Big 9"],
        conclusion_template="FALCPA mandates labeling of major food allergens for consumer protection.",
        reasoning_framework=(
            "The Food Allergen Labeling and Consumer Protection Act (FALCPA) requires clear labeling of major allergens. "
            "Manufacturers must identify allergens in ingredient lists. "
            "Regulatory enforcement ensures compliance. "
            "Consumer awareness is critical for safety."
        ),
        key_factors=["allergen declaration", "labeling", "regulation", "compliance"],
        primary_authority=["FDA", "FALCPA"],
        burden_holder="Food manufacturer",
        adversary_position="FALCPA does not cover all allergens.",
        counter_arguments=[
            "FALCPA addresses the most common allergens.",
            "Additional labeling is encouraged."
        ],
        resolution_strategy="Enforce labeling; encourage broader allergen disclosure.",
        entity_scope="Packaged foods",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="FALCPA 2004"
    ),
    DoctrineBlock(
        topic="Fermentation: Lactic",
        keywords=["fermentation", "lactic acid", "microbial", "yogurt", "safety"],
        conclusion_template="Lactic fermentation produces acid, preserves food, and enhances flavor.",
        reasoning_framework=(
            "Lactic acid bacteria ferment sugars to produce lactic acid, lowering pH and inhibiting pathogens. "
            "It is used in yogurt, sauerkraut, and pickles. "
            "Process control ensures safety and quality. "
            "Regulatory bodies set standards for starter cultures and fermentation conditions."
        ),
        key_factors=["starter culture", "pH", "process control", "regulation"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food processor",
        adversary_position="Fermentation may produce harmful byproducts.",
        counter_arguments=[
            "Process control prevents undesirable byproducts.",
            "Starter cultures are selected for safety."
        ],
        resolution_strategy="Use validated cultures; monitor fermentation.",
        entity_scope="Fermented foods",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="FDA Yogurt Standard"
    ),
    DoctrineBlock(
        topic="Fermentation: Alcoholic",
        keywords=["fermentation", "alcoholic", "yeast", "wine", "beer"],
        conclusion_template="Alcoholic fermentation converts sugars to ethanol, producing beverages and flavor compounds.",
        reasoning_framework=(
            "Yeast ferments sugars to produce ethanol and CO2. "
            "Alcoholic fermentation is used in wine, beer, and spirits. "
            "Process control affects flavor, alcohol content, and safety. "
            "Regulatory bodies set standards for fermentation and labeling."
        ),
        key_factors=["yeast strain", "process control", "alcohol content", "regulation"],
        primary_authority=["FDA", "TTB", "EFSA"],
        burden_holder="Beverage producer",
        adversary_position="Alcoholic fermentation may produce harmful compounds.",
        counter_arguments=[
            "Process control prevents undesirable byproducts.",
            "Regulation ensures safety."
        ],
        resolution_strategy="Use validated yeast strains; monitor fermentation.",
        entity_scope="Alcoholic beverages",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="TTB Alcohol Regulation"
    ),
    DoctrineBlock(
        topic="Fermentation: Acetic",
        keywords=["fermentation", "acetic acid", "vinegar", "microbial", "safety"],
        conclusion_template="Acetic fermentation produces vinegar and preserves food through acidification.",
        reasoning_framework=(
            "Acetic acid bacteria oxidize ethanol to acetic acid, producing vinegar. "
            "Acidification inhibits pathogens and preserves food. "
            "Process control ensures safety and quality. "
            "Regulatory bodies set standards for fermentation and labeling."
        ),
        key_factors=["bacteria strain", "process control", "acid content", "regulation"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food processor",
        adversary_position="Acetic fermentation may produce undesirable flavors.",
        counter_arguments=[
            "Process control optimizes flavor.",
            "Regulation ensures safety."
        ],
        resolution_strategy="Use validated cultures; monitor fermentation.",
        entity_scope="Vinegar, pickled foods",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="FDA Vinegar Standard"
    ),
    DoctrineBlock(
        topic="Enzyme Catalysis: Amylase",
        keywords=["enzyme", "amylase", "starch", "hydrolysis", "bread"],
        conclusion_template="Amylase catalyzes starch hydrolysis, improving texture and digestibility.",
        reasoning_framework=(
            "Amylase breaks down starch into sugars, aiding fermentation and improving bread texture. "
            "It is used in baking and brewing. "
            "Process control ensures optimal activity and prevents defects. "
            "Regulatory bodies set standards for enzyme use."
        ),
        key_factors=["enzyme activity", "process control", "regulation", "texture"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food processor",
        adversary_position="Enzyme use may cause allergenicity.",
        counter_arguments=[
            "Enzymes are selected for safety.",
            "Labeling informs consumers."
        ],
        resolution_strategy="Use safe enzymes; monitor activity.",
        entity_scope="Baked goods, brewing",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="FDA Enzyme Regulation"
    ),
    DoctrineBlock(
        topic="Enzyme Catalysis: Protease",
        keywords=["enzyme", "protease", "protein", "hydrolysis", "meat"],
        conclusion_template="Protease catalyzes protein hydrolysis, tenderizing meat and improving digestibility.",
        reasoning_framework=(
            "Protease breaks down proteins, tenderizing meat and improving digestibility. "
            "It is used in meat processing and dairy. "
            "Process control ensures optimal activity and prevents defects. "
            "Regulatory bodies set standards for enzyme use."
        ),
        key_factors=["enzyme activity", "process control", "regulation", "tenderization"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food processor",
        adversary_position="Protease use may cause allergenicity.",
        counter_arguments=[
            "Enzymes are selected for safety.",
            "Labeling informs consumers."
        ],
        resolution_strategy="Use safe enzymes; monitor activity.",
        entity_scope="Meat, dairy",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="FDA Enzyme Regulation"
    ),
    DoctrineBlock(
        topic="Enzyme Catalysis: Lipase",
        keywords=["enzyme", "lipase", "lipid", "hydrolysis", "cheese"],
        conclusion_template="Lipase catalyzes lipid hydrolysis, enhancing flavor in cheese and dairy.",
        reasoning_framework=(
            "Lipase breaks down lipids, producing flavor compounds in cheese and dairy. "
            "It is used in cheese ripening and flavor enhancement. "
            "Process control ensures optimal activity and prevents defects. "
            "Regulatory bodies set standards for enzyme use."
        ),
        key_factors=["enzyme activity", "process control", "regulation", "flavor"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food processor",
        adversary_position="Lipase use may cause allergenicity.",
        counter_arguments=[
            "Enzymes are selected for safety.",
            "Labeling informs consumers."
        ],
        resolution_strategy="Use safe enzymes; monitor activity.",
        entity_scope="Cheese, dairy",
        confidence=0.92,
        confidence_zone="Very High",
        controlling_precedent="FDA Enzyme Regulation"
    ),
    DoctrineBlock(
        topic="Food Rheology: Viscosity",
        keywords=["rheology", "viscosity", "texture", "flow", "measurement"],
        conclusion_template="Viscosity measurement is essential for controlling texture and flow in food products.",
        reasoning_framework=(
            "Viscosity quantifies resistance to flow, affecting texture and mouthfeel. "
            "Measurement methods include rotational viscometers and rheometers. "
            "Process control ensures consistent product quality. "
            "Regulatory bodies set standards for certain products."
        ),
        key_factors=["measurement method", "process control", "texture", "regulation"],
        primary_authority=["FDA", "Food Chemistry Texts"],
        burden_holder="Food manufacturer",
        adversary_position="Viscosity varies during storage.",
        counter_arguments=[
            "Process control maintains viscosity.",
            "Packaging prevents changes."
        ],
        resolution_strategy="Monitor viscosity; optimize formulation.",
        entity_scope="Sauces, beverages",
        confidence=0.91,
        confidence_zone="Very High",
        controlling_precedent="FDA Sauce Regulation"
    ),
    DoctrineBlock(
        topic="Food Rheology: Texture Analysis",
        keywords=["rheology", "texture", "analysis", "mouthfeel", "measurement"],
        conclusion_template="Texture analysis quantifies physical properties, guiding product development and quality control.",
        reasoning_framework=(
            "Texture analysis measures properties like hardness, cohesiveness, and springiness. "
            "Methods include compression, penetration, and sensory evaluation. "
            "Process control ensures consistent quality. "
            "Regulatory bodies set standards for certain products."
        ),
        key_factors=["measurement method", "process control", "quality", "regulation"],
        primary_authority=["FDA", "Food Chemistry Texts"],
        burden_holder="Food manufacturer",
        adversary_position="Texture varies during storage.",
        counter_arguments=[
            "Process control maintains texture.",
            "Packaging prevents changes."
        ],
        resolution_strategy="Monitor texture; optimize formulation.",
        entity_scope="Baked goods, dairy",
        confidence=0.90,
        confidence_zone="Very High",
        controlling_precedent="FDA Dairy Product Regulation"
    ),
    DoctrineBlock(
        topic="Nutritional Analysis: Proximate",
        keywords=["nutritional analysis", "proximate", "moisture", "protein", "fat"],
        conclusion_template="Proximate analysis quantifies major nutritional components for labeling and quality control.",
        reasoning_framework=(
            "Proximate analysis measures moisture, protein, fat, ash, and carbohydrate content. "
            "Standard methods include drying, Kjeldahl, Soxhlet, and combustion. "
            "Results inform labeling and regulatory compliance."
        ),
        key_factors=["analysis method", "component", "labeling", "regulation"],
        primary_authority=["FDA", "AOAC"],
        burden_holder="Food manufacturer",
        adversary_position="Proximate analysis lacks precision.",
        counter_arguments=[
            "Standard methods provide reliable results.",
            "Advanced techniques improve accuracy."
        ],
        resolution_strategy="Use validated methods; update techniques as needed.",
        entity_scope="Packaged foods",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FDA Nutrition Labeling Regulation"
    ),
    DoctrineBlock(
        topic="Nutritional Analysis: Kjeldahl",
        keywords=["nutritional analysis", "Kjeldahl", "protein", "nitrogen", "method"],
        conclusion_template="Kjeldahl method quantifies protein content by measuring nitrogen.",
        reasoning_framework=(
            "Kjeldahl method digests samples to convert nitrogen to ammonium, which is quantified. "
            "Protein content is calculated using a conversion factor. "
            "Standardized protocols ensure accuracy. "
            "Regulatory bodies require validated methods."
        ),
        key_factors=["digestion", "conversion factor", "accuracy", "regulation"],
        primary_authority=["FDA", "AOAC"],
        burden_holder="Food manufacturer",
        adversary_position="Kjeldahl may overestimate protein.",
        counter_arguments=[
            "Conversion factors are standardized.",
            "Alternative methods are available."
        ],
        resolution_strategy="Use validated methods; compare with alternatives.",
        entity_scope="Packaged foods",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="AOAC Official Method"
    ),
    DoctrineBlock(
        topic="Nutritional Analysis: Soxhlet",
        keywords=["nutritional analysis", "Soxhlet", "fat", "extraction", "method"],
        conclusion_template="Soxhlet extraction quantifies fat content in foods through solvent extraction.",
        reasoning_framework=(
            "Soxhlet extraction uses solvents to extract fat from food samples. "
            "The extracted fat is weighed to determine content. "
            "Standardized protocols ensure accuracy. "
            "Regulatory bodies require validated methods."
        ),
        key_factors=["solvent", "extraction", "accuracy", "regulation"],
        primary_authority=["FDA", "AOAC"],
        burden_holder="Food manufacturer",
        adversary_position="Soxhlet may miss bound fat.",
        counter_arguments=[
            "Method is standardized for free fat.",
            "Alternative methods are available."
        ],
        resolution_strategy="Use validated methods; compare with alternatives.",
        entity_scope="Packaged foods",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="AOAC Official Method"
    ),
    DoctrineBlock(
        topic="Food Packaging: MAP",
        keywords=["packaging", "MAP", "modified atmosphere", "shelf life", "preservation"],
        conclusion_template="MAP extends shelf life by modifying the atmosphere within packaging.",
        reasoning_framework=(
            "Modified atmosphere packaging (MAP) replaces air with gases (CO2, N2, O2) to inhibit spoilage. "
            "MAP is used for fresh produce, meat, and bakery. "
            "Process control ensures optimal gas composition. "
            "Regulatory bodies set standards for packaging materials and gas use."
        ),
        key_factors=["gas composition", "packaging material", "process control", "regulation"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food packager",
        adversary_position="MAP may accelerate spoilage if misapplied.",
        counter_arguments=[
            "Process control prevents spoilage.",
            "Packaging materials are validated."
        ],
        resolution_strategy="Monitor gas composition; use validated materials.",
        entity_scope="Fresh produce, meat",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="FDA MAP Guidance"
    ),
    DoctrineBlock(
        topic="Food Packaging: Barrier Properties",
        keywords=["packaging", "barrier", "oxygen", "moisture", "migration"],
        conclusion_template="Barrier properties of packaging materials control oxygen and moisture migration, preserving food quality.",
        reasoning_framework=(
            "Barrier materials prevent oxygen and moisture ingress, preserving flavor and shelf life. "
            "Selection depends on food type and storage conditions. "
            "Regulatory bodies set standards for packaging materials."
        ),
        key_factors=["material", "barrier property", "food type", "regulation"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food packager",
        adversary_position="Barrier materials may leach chemicals.",
        counter_arguments=[
            "Materials are tested for safety.",
            "Regulation prevents unsafe migration."
        ],
        resolution_strategy="Use validated materials; monitor migration.",
        entity_scope="Packaged foods",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="FDA Packaging Regulation"
    ),
    DoctrineBlock(
        topic="Food Packaging: Migration",
        keywords=["packaging", "migration", "chemical", "safety", "regulation"],
        conclusion_template="Migration of chemicals from packaging is regulated to ensure food safety.",
        reasoning_framework=(
            "Migration occurs when chemicals transfer from packaging to food. "
            "Regulatory bodies set limits and require testing. "
            "Material selection and process control minimize migration."
        ),
        key_factors=["chemical", "testing", "material", "regulation"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food packager",
        adversary_position="Migration poses health risks.",
        counter_arguments=[
            "Regulation limits migration.",
            "Materials are validated for safety."
        ],
        resolution_strategy="Use validated materials; monitor migration.",
        entity_scope="Packaged foods",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="FDA Packaging Regulation"
    ),
    DoctrineBlock(
        topic="Shelf Life Prediction: Arrhenius",
        keywords=["shelf life", "Arrhenius", "prediction", "temperature", "reaction rate"],
        conclusion_template="Arrhenius equation predicts shelf life based on temperature-dependent reaction rates.",
        reasoning_framework=(
            "Arrhenius equation relates reaction rate to temperature, enabling shelf life prediction. "
            "It is used for chemical, enzymatic, and microbial spoilage. "
            "Data collection and modeling inform shelf life estimates. "
            "Regulatory bodies require validated prediction methods."
        ),
        key_factors=["reaction rate", "temperature", "modeling", "regulation"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food manufacturer",
        adversary_position="Arrhenius model oversimplifies shelf life.",
        counter_arguments=[
            "Model is validated for many products.",
            "Alternative models are available."
        ],
        resolution_strategy="Use validated models; update as needed.",
        entity_scope="Packaged foods",
        confidence=0.93,
        confidence_zone="Very High",
        controlling_precedent="FDA Shelf Life Guidance"
    ),
    DoctrineBlock(
        topic="Shelf Life Prediction: Q10",
        keywords=["shelf life", "Q10", "prediction", "temperature", "reaction rate"],
        conclusion_template="Q10 model estimates shelf life changes with temperature shifts.",
        reasoning_framework=(
            "Q10 model estimates the rate of change in shelf life for every 10°C increase in temperature. "
            "It is used for chemical and microbial spoilage. "
            "Data collection and modeling inform shelf life estimates. "
            "Regulatory bodies require validated prediction methods."
        ),
        key_factors=["Q10 value", "temperature", "modeling", "regulation"],
        primary_authority=["FDA", "EFSA"],
        burden_holder="Food manufacturer",
        adversary_position="Q10 model lacks precision.",
        counter_arguments=[
            "Model is validated for many products.",
            "Alternative models are available."
        ],
        resolution_strategy="Use validated models; update as needed.",
        entity_scope="Packaged foods",
        confidence=0.92,
        confidence_zone="Very High",
        controlling_precedent="FDA Shelf Life Guidance"
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