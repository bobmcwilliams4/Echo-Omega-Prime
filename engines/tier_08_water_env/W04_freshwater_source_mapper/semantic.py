import hashlib
import re
from typing import Dict, List

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "W04 Engine Team"
SEMANTIC_MAP_ENGINE = "W04_freshwater_source_mapper"

SEMANTIC_MAP: Dict[str, str] = {
    # Ogallala Aquifer
    "ogallala": "ogallala_aquifer",
    "ogallala aquifer": "ogallala_aquifer",
    "ogallala formation": "ogallala_aquifer",
    "high plains aquifer": "ogallala_aquifer",
    "ogallala water": "ogallala_aquifer",
    "ogallala groundwater": "ogallala_aquifer",
    "ogallala region": "ogallala_aquifer",
    "ogallala source": "ogallala_aquifer",
    "ogallala basin": "ogallala_aquifer",
    "ogallala depletion": "ogallala_aquifer",
    "ogallala recharge": "ogallala_aquifer",
    "ogallala viability": "ogallala_source_viability",
    "ogallala frac": "ogallala_source_viability",
    "ogallala frac water": "ogallala_source_viability",
    "ogallala frac operations": "ogallala_source_viability",
    "ogallala frac suitability": "ogallala_source_viability",
    "ogallala frac source": "ogallala_source_viability",
    "ogallala frac use": "ogallala_source_viability",
    "ogallala frac suitability": "ogallala_source_viability",
    "ogallala frac viability": "ogallala_source_viability",
    "ogallala frac regulatory": "ogallala_regulatory",
    "ogallala frac legal": "ogallala_regulatory",
    "ogallala frac constraints": "ogallala_regulatory",
    "ogallala frac barriers": "ogallala_regulatory",
    "ogallala frac limits": "ogallala_regulatory",
    "ogallala frac enforcement": "ogallala_regulatory",
    "ogallala frac variance": "ogallala_regulatory",
    "ogallala frac permit": "ogallala_permitting",
    "ogallala frac permitting": "ogallala_permitting",
    "ogallala frac process": "ogallala_permitting",
    "ogallala frac pitfalls": "ogallala_permitting",
    "ogallala frac tds": "ogallala_water_quality",
    "ogallala frac hardness": "ogallala_water_quality",
    "ogallala frac quality": "ogallala_water_quality",
    "ogallala frac standards": "ogallala_water_quality",
    "ogallala frac requirements": "ogallala_water_quality",
    "ogallala frac operational": "ogallala_water_quality",
    "ogallala frac regulatory": "ogallala_water_quality",
    "ogallala frac seasonal": "ogallala_seasonal_availability",
    "ogallala frac drought": "ogallala_seasonal_availability",
    "ogallala frac response": "ogallala_seasonal_availability",
    "ogallala frac planning": "ogallala_seasonal_availability",
    "ogallala frac predictive": "ogallala_seasonal_availability",
    "ogallala frac index": "ogallala_drought_index_correlation",
    "ogallala frac correlation": "ogallala_drought_index_correlation",
    "ogallala frac predictive": "ogallala_drought_index_correlation",
    "ogallala frac planning": "ogallala_drought_index_correlation",
    # Pecos Valley Aquifer
    "pecos valley": "pecos_valley_aquifer",
    "pecos valley aquifer": "pecos_valley_aquifer",
    "pecos aquifer": "pecos_valley_aquifer",
    "pecos groundwater": "pecos_valley_aquifer",
    "pecos region": "pecos_valley_aquifer",
    "pecos source": "pecos_valley_aquifer",
    "pecos regulatory": "pecos_valley_regulatory_constraints",
    "pecos constraints": "pecos_valley_regulatory_constraints",
    "pecos hydrogeologic": "pecos_valley_hydrogeologic_constraints",
    "pecos hydrogeology": "pecos_valley_hydrogeologic_constraints",
    "pecos frac": "pecos_valley_frac_operations",
    "pecos frac operations": "pecos_valley_frac_operations",
    "pecos frac suitability": "pecos_valley_frac_operations",
    "pecos frac source": "pecos_valley_frac_operations",
    "pecos frac use": "pecos_valley_frac_operations",
    "pecos frac regulatory": "pecos_valley_regulatory_constraints",
    "pecos frac legal": "pecos_valley_regulatory_constraints",
    "pecos frac constraints": "pecos_valley_regulatory_constraints",
    "pecos frac barriers": "pecos_valley_regulatory_constraints",
    "pecos frac limits": "pecos_valley_regulatory_constraints",
    "pecos frac enforcement": "pecos_valley_regulatory_constraints",
    "pecos frac variance": "pecos_valley_regulatory_constraints",
    "pecos frac permit": "pecos_valley_permitting",
    "pecos frac permitting": "pecos_valley_permitting",
    "pecos frac process": "pecos_valley_permitting",
    "pecos frac pitfalls": "pecos_valley_permitting",
    "pecos frac tds": "pecos_valley_water_quality",
    "pecos frac hardness": "pecos_valley_water_quality",
    "pecos frac quality": "pecos_valley_water_quality",
    "pecos frac standards": "pecos_valley_water_quality",
    "pecos frac requirements": "pecos_valley_water_quality",
    "pecos frac operational": "pecos_valley_water_quality",
    "pecos frac regulatory": "pecos_valley_water_quality",
    "pecos frac seasonal": "pecos_valley_seasonal_availability",
    "pecos frac drought": "pecos_valley_seasonal_availability",
    "pecos frac response": "pecos_valley_seasonal_availability",
    "pecos frac planning": "pecos_valley_seasonal_availability",
    "pecos frac predictive": "pecos_valley_seasonal_availability",
    "pecos frac index": "pecos_valley_drought_index_correlation",
    "pecos frac correlation": "pecos_valley_drought_index_correlation",
    "pecos frac predictive": "pecos_valley_drought_index_correlation",
    "pecos frac planning": "pecos_valley_drought_index_correlation",
    # Edwards-Trinity Aquifer
    "edwards-trinity": "edwards_trinity_aquifer",
    "edwards trinity": "edwards_trinity_aquifer",
    "edwards-trinity aquifer": "edwards_trinity_aquifer",
    "edwards trinity aquifer": "edwards_trinity_aquifer",
    "edwards aquifer": "edwards_trinity_aquifer",
    "trinity aquifer": "edwards_trinity_aquifer",
    "edwards-trinity groundwater": "edwards_trinity_aquifer",
    "edwards-trinity region": "edwards_trinity_aquifer",
    "edwards-trinity source": "edwards_trinity_aquifer",
    "edwards-trinity legal": "edwards_trinity_legal_considerations",
    "edwards-trinity quality": "edwards_trinity_quality_considerations",
    "edwards-trinity frac": "edwards_trinity_frac_operations",
    "edwards-trinity frac operations": "edwards_trinity_frac_operations",
    "edwards-trinity frac suitability": "edwards_trinity_frac_operations",
    "edwards-trinity frac source": "edwards_trinity_frac_operations",
    "edwards-trinity frac use": "edwards_trinity_frac_operations",
    "edwards-trinity frac legal": "edwards_trinity_legal_considerations",
    "edwards-trinity frac quality": "edwards_trinity_quality_considerations",
    "edwards-trinity frac regulatory": "edwards_trinity_legal_considerations",
    "edwards-trinity frac constraints": "edwards_trinity_legal_considerations",
    "edwards-trinity frac barriers": "edwards_trinity_legal_considerations",
    "edwards-trinity frac limits": "edwards_trinity_legal_considerations",
    "edwards-trinity frac enforcement": "edwards_trinity_legal_considerations",
    "edwards-trinity frac variance": "edwards_trinity_legal_considerations",
    "edwards-trinity frac permit": "edwards_trinity_permitting",
    "edwards-trinity frac permitting": "edwards_trinity_permitting",
    "edwards-trinity frac process": "edwards_trinity_permitting",
    "edwards-trinity frac pitfalls": "edwards_trinity_permitting",
    "edwards-trinity frac tds": "edwards_trinity_water_quality",
    "edwards-trinity frac hardness": "edwards_trinity_water_quality",
    "edwards-trinity frac standards": "edwards_trinity_water_quality",
    "edwards-trinity frac requirements": "edwards_trinity_water_quality",
    "edwards-trinity frac operational": "edwards_trinity_water_quality",
    "edwards-trinity frac regulatory": "edwards_trinity_water_quality",
    "edwards-trinity frac seasonal": "edwards_trinity_seasonal_availability",
    "edwards-trinity frac drought": "edwards_trinity_seasonal_availability",
    "edwards-trinity frac response": "edwards_trinity_seasonal_availability",
    "edwards-trinity frac planning": "edwards_trinity_seasonal_availability",
    "edwards-trinity frac predictive": "edwards_trinity_seasonal_availability",
    "edwards-trinity frac index": "edwards_trinity_drought_index_correlation",
    "edwards-trinity frac correlation": "edwards_trinity_drought_index_correlation",
    "edwards-trinity frac predictive": "edwards_trinity_drought_index_correlation",
    "edwards-trinity frac planning": "edwards_trinity_drought_index_correlation",
    # Dockum Aquifer
    "dockum": "dockum_aquifer",
    "dockum aquifer": "dockum_aquifer",
    "dockum formation": "dockum_aquifer",
    "dockum groundwater": "dockum_aquifer",
    "dockum region": "dockum_aquifer",
    "dockum source": "dockum_aquifer",
    "dockum suitability": "dockum_suitability",
    "dockum regulatory": "dockum_regulatory_barriers",
    "dockum frac": "dockum_frac_operations",
    "dockum frac operations": "dockum_frac_operations",
    "dockum frac suitability": "dockum_suitability",
    "dockum frac source": "dockum_frac_operations",
    "dockum frac use": "dockum_frac_operations",
    "dockum frac regulatory": "dockum_regulatory_barriers",
    "dockum frac legal": "dockum_regulatory_barriers",
    "dockum frac constraints": "dockum_regulatory_barriers",
    "dockum frac barriers": "dockum_regulatory_barriers",
    "dockum frac limits": "dockum_regulatory_barriers",
    "dockum frac enforcement": "dockum_regulatory_barriers",
    "dockum frac variance": "dockum_regulatory_barriers",
    "dockum frac permit": "dockum_permitting",
    "dockum frac permitting": "dockum_permitting",
    "dockum frac process": "dockum_permitting",
    "dockum frac pitfalls": "dockum_permitting",
    "dockum frac tds": "dockum_water_quality",
    "dockum frac hardness": "dockum_water_quality",
    "dockum frac quality": "dockum_water_quality",
    "dockum frac standards": "dockum_water_quality",
    "dockum frac requirements": "dockum_water_quality",
    "dockum frac operational": "dockum_water_quality",
    "dockum frac regulatory": "dockum_water_quality",
    "dockum frac seasonal": "dockum_seasonal_availability",
    "dockum frac drought": "dockum_seasonal_availability",
    "dockum frac response": "dockum_seasonal_availability",
    "dockum frac planning": "dockum_seasonal_availability",
    "dockum frac predictive": "dockum_seasonal_availability",
    "dockum frac index": "dockum_drought_index_correlation",
    "dockum frac correlation": "dockum_drought_index_correlation",
    "dockum frac predictive": "dockum_drought_index_correlation",
    "dockum frac planning": "dockum_drought_index_correlation",
    # Santa Rosa Aquifer
    "santa rosa": "santa_rosa_aquifer",
    "santa rosa aquifer": "santa_rosa_aquifer",
    "santa rosa formation": "santa_rosa_aquifer",
    "santa rosa groundwater": "santa_rosa_aquifer",
    "santa rosa region": "santa_rosa_aquifer",
    "santa rosa source": "santa_rosa_aquifer",
    "santa rosa suitability": "santa_rosa_freshwater_sourcing",
    "santa rosa drought": "santa_rosa_drought_resilience",
    "santa rosa resilience": "santa_rosa_drought_resilience",
    "santa rosa frac": "santa_rosa_frac_operations",
    "santa rosa frac operations": "santa_rosa_frac_operations",
    "santa rosa frac suitability": "santa_rosa_freshwater_sourcing",
    "santa rosa frac source": "santa_rosa_frac_operations",
    "santa rosa frac use": "santa_rosa_frac_operations",
    "santa rosa frac regulatory": "santa_rosa_drought_resilience",
    "santa rosa frac legal": "santa_rosa_drought_resilience",
    "santa rosa frac constraints": "santa_rosa_drought_resilience",
    "santa rosa frac barriers": "santa_rosa_drought_resilience",
    "santa rosa frac limits": "santa_rosa_drought_resilience",
    "santa rosa frac enforcement": "santa_rosa_drought_resilience",
    "santa rosa frac variance": "santa_rosa_drought_resilience",
    "santa rosa frac permit": "santa_rosa_permitting",
    "santa rosa frac permitting": "santa_rosa_permitting",
    "santa rosa frac process": "santa_rosa_permitting",
    "santa rosa frac pitfalls": "santa_rosa_permitting",
    "santa rosa frac tds": "santa_rosa_water_quality",
    "santa rosa frac hardness": "santa_rosa_water_quality",
    "santa rosa frac quality": "santa_rosa_water_quality",
    "santa rosa frac standards": "santa_rosa_water_quality",
    "santa rosa frac requirements": "santa_rosa_water_quality",
    "santa rosa frac operational": "santa_rosa_water_quality",
    "santa rosa frac regulatory": "santa_rosa_water_quality",
    "santa rosa frac seasonal": "santa_rosa_seasonal_availability",
    "santa rosa frac drought": "santa_rosa_seasonal_availability",
    "santa rosa frac response": "santa_rosa_seasonal_availability",
    "santa rosa frac planning": "santa_rosa_seasonal_availability",
    "santa rosa frac predictive": "santa_rosa_seasonal_availability",
    "santa rosa frac index": "santa_rosa_drought_index_correlation",
    "santa rosa frac correlation": "santa_rosa_drought_index_correlation",
    "santa rosa frac predictive": "santa_rosa_drought_index_correlation",
    "santa rosa frac planning": "santa_rosa_drought_index_correlation",
    # TWDB Freshwater Well Permitting
    "twdb": "twdb",
    "twdb freshwater": "twdb_freshwater",
    "twdb freshwater well": "twdb_freshwater_well",
    "twdb freshwater well permitting": "twdb_freshwater_well_permitting",
    "twdb well permitting": "twdb_freshwater_well_permitting",
    "twdb well permit": "twdb_freshwater_well_permitting",
    "twdb well process": "twdb_freshwater_well_permitting",
    "twdb well pitfalls": "twdb_freshwater_well_permitting",
    "twdb freshwater permitting": "twdb_freshwater_well_permitting",
    "twdb freshwater permit": "twdb_freshwater_well_permitting",
    "twdb freshwater process": "twdb_freshwater_well_permitting",
    "twdb freshwater pitfalls": "twdb_freshwater_well_permitting",
    "twdb well regulatory": "twdb_freshwater_well_permitting",
    "twdb well legal": "twdb_freshwater_well_permitting",
    "twdb well requirements": "twdb_freshwater_well_permitting",
    "twdb well standards": "twdb_freshwater_well_permitting",
    "twdb well operational": "twdb_freshwater_well_permitting",
    "twdb well quality": "twdb_freshwater_well_permitting",
    # GCD Production Limits
    "gcd": "gcd",
    "gcd production": "gcd_production_limits",
    "gcd production limits": "gcd_production_limits",
    "gcd limits": "gcd_production_limits",
    "gcd enforcement": "gcd_production_enforcement",
    "gcd variance": "gcd_production_variance",
    "gcd regulatory": "gcd_production_limits",
    "gcd legal": "gcd_production_limits",
    "gcd permit": "gcd_production_limits",
    "gcd permitting": "gcd_production_limits",
    "gcd process": "gcd_production_limits",
    "gcd pitfalls": "gcd_production_limits",
    "gcd standards": "gcd_production_limits",
    "gcd requirements": "gcd_production_limits",
    "gcd operational": "gcd_production_limits",
    "gcd quality": "gcd_production_limits",
    "gcd enforcement variance": "gcd_production_enforcement",
    "gcd enforcement process": "gcd_production_enforcement",
    "gcd enforcement pitfalls": "gcd_production_enforcement",
    # Water Quality Parameters
    "tds": "water_quality_tds",
    "total dissolved solids": "water_quality_tds",
    "hardness": "water_quality_hardness",
    "water hardness": "water_quality_hardness",
    "frac water tds": "water_quality_tds",
    "frac water hardness": "water_quality_hardness",
    "frac tds": "water_quality_tds",
    "frac hardness": "water_quality_hardness",
    "frac water quality": "frac_water_quality_requirements",
    "frac water standards": "frac_water_quality_requirements",
    "frac water requirements": "frac_water_quality_requirements",
    "frac water regulatory": "frac_water_quality_requirements",
    "frac water operational": "frac_water_quality_requirements",
    "frac water use": "frac_water_quality_requirements",
    "frac water suitability": "frac_water_quality_requirements",
    "frac water legal": "frac_water_quality_requirements",
    "frac water permit": "frac_water_quality_requirements",
    "frac water permitting": "frac_water_quality_requirements",
    "frac water process": "frac_water_quality_requirements",
    "frac water pitfalls": "frac_water_quality_requirements",
    # Seasonal Availability
    "seasonal availability": "seasonal_availability",
    "aquifer response": "seasonal_availability",
    "aquifer response to drought": "seasonal_availability",
    "drought response": "seasonal_availability",
    "seasonal drought": "seasonal_availability",
    "seasonal planning": "seasonal_availability",
    "seasonal predictive": "seasonal_availability",
    "seasonal index": "seasonal_availability",
    "seasonal correlation": "seasonal_availability",
    "seasonal suitability": "seasonal_availability",
    # Drought Index Correlation
    "drought index": "drought_index_correlation",
    "drought index correlation": "drought_index_correlation",
    "drought predictive": "drought_index_correlation",
    "drought planning": "drought_index_correlation",
    "drought suitability": "drought_index_correlation",
    "drought correlation": "drought_index_correlation",
    "drought index planning": "drought_index_correlation",
    "drought index suitability": "drought_index_correlation",
    # Frac Water Quality Requirements
    "frac water": "frac_water_quality_requirements",
    "frac water requirements": "frac_water_quality_requirements",
    "frac water standards": "frac_water_quality_requirements",
    "frac water regulatory": "frac_water_quality_requirements",
    "frac water operational": "frac_water_quality_requirements",
    "frac water legal": "frac_water_quality_requirements",
    "frac water permit": "frac_water_quality_requirements",
    "frac water permitting": "frac_water_quality_requirements",
    "frac water process": "frac_water_quality_requirements",
    "frac water pitfalls": "frac_water_quality_requirements",
    # General synonyms, abbreviations, misspellings, related terms
    "ogalala": "ogallala_aquifer",
    "ogalala aquifer": "ogallala_aquifer",
    "pecos vally": "pecos_valley_aquifer",
    "edwards trinty": "edwards_trinity_aquifer",
    "edwards-trinty": "edwards_trinity_aquifer",
    "dockhum": "dockum_aquifer",
    "santarosa": "santa_rosa_aquifer",
    "santa rosa aquifer": "santa_rosa_aquifer",
    "twdb permit": "twdb_freshwater_well_permitting",
    "twdb pitfall": "twdb_freshwater_well_permitting",
    "gcd limit": "gcd_production_limits",
    "gcd enforcement": "gcd_production_enforcement",
    "gcd varience": "gcd_production_variance",
    "tds value": "water_quality_tds",
    "hardness value": "water_quality_hardness",
    "total dissolved solid": "water_quality_tds",
    "water quality": "frac_water_quality_requirements",
    "frac quality": "frac_water_quality_requirements",
    "frac standards": "frac_water_quality_requirements",
    "frac requirements": "frac_water_quality_requirements",
    "frac regulatory": "frac_water_quality_requirements",
    "frac operational": "frac_water_quality_requirements",
    "frac legal": "frac_water_quality_requirements",
    "frac permit": "frac_water_quality_requirements",
    "frac permitting": "frac_water_quality_requirements",
    "frac process": "frac_water_quality_requirements",
    "frac pitfalls": "frac_water_quality_requirements",
    "frac suitability": "frac_water_quality_requirements",
    "frac planning": "drought_index_correlation",
    "frac predictive": "drought_index_correlation",
    "frac index": "drought_index_correlation",
    "frac correlation": "drought_index_correlation",
    "frac drought": "seasonal_availability",
    "frac response": "seasonal_availability",
    "frac seasonal": "seasonal_availability",
    "frac use": "frac_water_quality_requirements",
    "frac source": "frac_water_quality_requirements",
    "frac operations": "frac_water_quality_requirements",
    "frac operation": "frac_water_quality_requirements",
    "frac enforcement": "gcd_production_enforcement",
    "frac variance": "gcd_production_variance",
    "frac process": "frac_water_quality_requirements",
    "frac pitfall": "frac_water_quality_requirements",
    "frac pitfalls": "frac_water_quality_requirements",
    "frac limits": "gcd_production_limits",
    "frac barriers": "gcd_production_limits",
    "frac constraints": "gcd_production_limits",
    "frac legal": "frac_water_quality_requirements",
    "frac regulatory": "frac_water_quality_requirements",
    "frac legal": "frac_water_quality_requirements",
    "frac standards": "frac_water_quality_requirements",
    "frac requirements": "frac_water_quality_requirements",
    "frac operational": "frac_water_quality_requirements",
    "frac suitability": "frac_water_quality_requirements",
    "frac planning": "drought_index_correlation",
    "frac predictive": "drought_index_correlation",
    "frac index": "drought_index_correlation",
    "frac correlation": "drought_index_correlation",
    "frac drought": "seasonal_availability",
    "frac response": "seasonal_availability",
    "frac seasonal": "seasonal_availability",
    # More general misspellings and variants
    "ogallalla": "ogallala_aquifer",
    "ogallala aquifer": "ogallala_aquifer",
    "pecos valey": "pecos_valley_aquifer",
    "edwards trinity aquifer": "edwards_trinity_aquifer",
    "dockum aquifer": "dockum_aquifer",
    "santa rosa aquifer": "santa_rosa_aquifer",
    "twdb freshwater well": "twdb_freshwater_well_permitting",
    "gcd production limit": "gcd_production_limits",
    "gcd enforcement": "gcd_production_enforcement",
    "gcd variance": "gcd_production_variance",
    "tds": "water_quality_tds",
    "hardness": "water_quality_hardness",
    # Abbreviations
    "gcd": "gcd",
    "twdb": "twdb",
    "t.d.s.": "water_quality_tds",
    "harness": "water_quality_hardness",
    # Related terms
    "freshwater source": "freshwater_source",
    "freshwater sourcing": "freshwater_source",
    "freshwater suitability": "freshwater_source",
    "freshwater viability": "freshwater_source",
    "freshwater regulatory": "freshwater_source",
    "freshwater legal": "freshwater_source",
    "freshwater constraints": "freshwater_source",
    "freshwater barriers": "freshwater_source",
    "freshwater limits": "freshwater_source",
    "freshwater enforcement": "freshwater_source",
    "freshwater variance": "freshwater_source",
    "freshwater permit": "freshwater_source",
    "freshwater permitting": "freshwater_source",
    "freshwater process": "freshwater_source",
    "freshwater pitfalls": "freshwater_source",
    "freshwater tds": "water_quality_tds",
    "freshwater hardness": "water_quality_hardness",
    "freshwater quality": "frac_water_quality_requirements",
    "freshwater standards": "frac_water_quality_requirements",
    "freshwater requirements": "frac_water_quality_requirements",
    "freshwater operational": "frac_water_quality_requirements",
    "freshwater planning": "drought_index_correlation",
    "freshwater predictive": "drought_index_correlation",
    "freshwater index": "drought_index_correlation",
    "freshwater correlation": "drought_index_correlation",
    "freshwater drought": "seasonal_availability",
    "freshwater response": "seasonal_availability",
    "freshwater seasonal": "seasonal_availability",
    # Misspellings and common typos
    "ogallala aquifer": "ogallala_aquifer",
    "pecos valley aquifer": "pecos_valley_aquifer",
    "edwards trinity aquifer": "edwards_trinity_aquifer",
    "dockum aquifer": "dockum_aquifer",
    "santa rosa aquifer": "santa_rosa_aquifer",
    "twdb freshwater well permitting": "twdb_freshwater_well_permitting",
    "gcd production limits": "gcd_production_limits",
    "gcd production enforcement": "gcd_production_enforcement",
    "gcd production variance": "gcd_production_variance",
    "water quality tds": "water_quality_tds",
    "water quality hardness": "water_quality_hardness",
    "frac water quality requirements": "frac_water_quality_requirements",
    "seasonal availability": "seasonal_availability",
    "drought index correlation": "drought_index_correlation",
    # Additional synonyms and variants
    "ogallala viability": "ogallala_source_viability",
    "pecos regulatory": "pecos_valley_regulatory_constraints",
    "edwards-trinity legal": "edwards_trinity_legal_considerations",
    "dockum suitability": "dockum_suitability",
    "santa rosa drought": "santa_rosa_drought_resilience",
    "twdb well permit": "twdb_freshwater_well_permitting",
    "gcd production": "gcd_production_limits",
    "tds": "water_quality_tds",
    "hardness": "water_quality_hardness",
    "frac water quality": "frac_water_quality_requirements",
    "frac water requirements": "frac_water_quality_requirements",
    "frac water standards": "frac_water_quality_requirements",
    "frac water regulatory": "frac_water_quality_requirements",
    "frac water operational": "frac_water_quality_requirements",
    "frac water legal": "frac_water_quality_requirements",
    "frac water permit": "frac_water_quality_requirements",
    "frac water permitting": "frac_water_quality_requirements",
    "frac water process": "frac_water_quality_requirements",
    "frac water pitfalls": "frac_water_quality_requirements",
    # Acronyms and abbreviations
    "pv": "pecos_valley_aquifer",
    "et": "edwards_trinity_aquifer",
    "dk": "dockum_aquifer",
    "sr": "santa_rosa_aquifer",
    "ow": "ogallala_aquifer",
    "pv aquifer": "pecos_valley_aquifer",
    "et aquifer": "edwards_trinity_aquifer",
    "dk aquifer": "dockum_aquifer",
    "sr aquifer": "santa_rosa_aquifer",
    "ow aquifer": "ogallala_aquifer",
    # Misspellings
    "ogallalla aquifer": "ogallala_aquifer",
    "pecos valey aquifer": "pecos_valley_aquifer",
    "edwards trinty aquifer": "edwards_trinity_aquifer",
    "dockhum aquifer": "dockum_aquifer",
    "santarosa aquifer": "santa_rosa_aquifer",
    # More related terms
    "well permitting": "twdb_freshwater_well_permitting",
    "well permit": "twdb_freshwater_well_permitting",
    "well process": "twdb_freshwater_well_permitting",
    "well pitfalls": "twdb_freshwater_well_permitting",
    "production limits": "gcd_production_limits",
    "production enforcement": "gcd_production_enforcement",
    "production variance": "gcd_production_variance",
    "production regulatory": "gcd_production_limits",
    "production legal": "gcd_production_limits",
    "production permit": "gcd_production_limits",
    "production permitting": "gcd_production_limits",
    "production process": "gcd_production_limits",
    "production pitfalls": "gcd_production_limits",
    "production standards": "gcd_production_limits",
    "production requirements": "gcd_production_limits",
    "production operational": "gcd_production_limits",
    "production quality": "gcd_production_limits",
    "enforcement variance": "gcd_production_enforcement",
    "enforcement process": "gcd_production_enforcement",
    "enforcement pitfalls": "gcd_production_enforcement",
    "water tds": "water_quality_tds",
    "water hardness": "water_quality_hardness",
    "frac tds": "water_quality_tds",
    "frac hardness": "water_quality_hardness",
    # Lowercase normalization
    "ogallala_aquifer": "ogallala_aquifer",
    "pecos_valley_aquifer": "pecos_valley_aquifer",
    "edwards_trinity_aquifer": "edwards_trinity_aquifer",
    "dockum_aquifer": "dockum_aquifer",
    "santa_rosa_aquifer": "santa_rosa_aquifer",
    "twdb_freshwater_well_permitting": "twdb_freshwater_well_permitting",
    "gcd_production_limits": "gcd_production_limits",
    "gcd_production_enforcement": "gcd_production_enforcement",
    "gcd_production_variance": "gcd_production_variance",
    "water_quality_tds": "water_quality_tds",
    "water_quality_hardness": "water_quality_hardness",
    "frac_water_quality_requirements": "frac_water_quality_requirements",
    "seasonal_availability": "seasonal_availability",
    "drought_index_correlation": "drought_index_correlation",
    "ogallala_source_viability": "ogallala_source_viability",
    "pecos_valley_regulatory_constraints": "pecos_valley_regulatory_constraints",
    "pecos_valley_hydrogeologic_constraints": "pecos_valley_hydrogeologic_constraints",
    "pecos_valley_frac_operations": "pecos_valley_frac_operations",
    "edwards_trinity_legal_considerations": "edwards_trinity_legal_considerations",
    "edwards_trinity_quality_considerations": "edwards_trinity_quality_considerations",
    "edwards_trinity_frac_operations": "edwards_trinity_frac_operations",
    "dockum_suitability": "dockum_suitability",
    "dockum_regulatory_barriers": "dockum_regulatory_barriers",
    "dockum_frac_operations": "dockum_frac_operations",
    "santa_rosa_freshwater_sourcing": "santa_rosa_freshwater_sourcing",
    "santa_rosa_drought_resilience": "santa_rosa_drought_resilience",
    "santa_rosa_frac_operations": "santa_rosa_frac_operations",
    "twdb_freshwater": "twdb_freshwater",
    "twdb_freshwater_well": "twdb_freshwater_well",
    "gcd": "gcd",
    "twdb": "twdb",
    "freshwater_source": "freshwater_source",
}

_EXPECTED_ENTRY_COUNT = 244

def _compute_map_hash() -> str:
    items = sorted((k, v) for k, v in SEMANTIC_MAP.items())
    concat = ''.join(f"{k}:{v};" for k, v in items)
    return hashlib.sha256(concat.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity() -> dict:
    actual_hash = _compute_map_hash()
    is_valid = (actual_hash == _MAP_INTEGRITY_HASH) and (len(SEMANTIC_MAP) == _EXPECTED_ENTRY_COUNT)
    return {
        "status": "ok" if is_valid else "error",
        "entries": len(SEMANTIC_MAP),
        "hash": actual_hash,
        "is_valid": is_valid,
    }

def normalize_term(term: str) -> str:
    if not term:
        return ""
    norm = term.strip().lower()
    norm = re.sub(r"[\s_]+", " ", norm)
    norm = norm.replace("-", " ")
    norm = norm.strip()
    norm = re.sub(r"\s+", " ", norm)
    norm = norm.replace("'", "")
    norm = norm.replace(".", "")
    norm = norm.replace(":", "")
    norm = norm.replace(",", "")
    norm = norm.replace("/", " ")
    norm = norm.strip()
    # Try direct match
    if norm in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm]
    # Try underscore variant
    norm_ = norm.replace(" ", "_")
    if norm_ in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm_]
    # Try space variant
    norm_space = norm.replace("_", " ")
    if norm_space in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm_space]
    # Try removing "aquifer" suffix
    if norm.endswith(" aquifer"):
        base = norm[:-8].strip()
        if base in SEMANTIC_MAP:
            return SEMANTIC_MAP[base]
        base_ = base.replace(" ", "_")
        if base_ in SEMANTIC_MAP:
            return SEMANTIC_MAP[base_]
    # Try removing "frac" prefix
    if norm.startswith("frac "):
        base = norm[5:]
        if base in SEMANTIC_MAP:
            return SEMANTIC_MAP[base]
        base_ = base.replace(" ", "_")
        if base_ in SEMANTIC_MAP:
            return SEMANTIC_MAP[base_]
    # Try removing "well" prefix
    if norm.startswith("well "):
        base = norm[5:]
        if base in SEMANTIC_MAP:
            return SEMANTIC_MAP[base]
        base_ = base.replace(" ", "_")
        if base_ in SEMANTIC_MAP:
            return SEMANTIC_MAP[base_]
    # Try removing "production" prefix
    if norm.startswith("production "):
        base = norm[11:]
        if base in SEMANTIC_MAP:
            return SEMANTIC_MAP[base]
        base_ = base.replace(" ", "_")
        if base_ in SEMANTIC_MAP:
            return SEMANTIC_MAP[base_]
    # Try removing "enforcement" prefix
    if norm.startswith("enforcement "):
        base = norm[12:]
        if base in SEMANTIC_MAP:
            return SEMANTIC_MAP[base]
        base_ = base.replace(" ", "_")
        if base_ in SEMANTIC_MAP:
            return SEMANTIC_MAP[base_]
    # Try removing "freshwater" prefix
    if norm.startswith("freshwater "):
        base = norm[11:]
        if base in SEMANTIC_MAP:
            return SEMANTIC_MAP[base]
        base_ = base.replace(" ", "_")
        if base_ in SEMANTIC_MAP:
            return SEMANTIC_MAP[base_]
    # Try removing "twdb" prefix
    if norm.startswith("twdb "):
        base = norm[5:]
        if base in SEMANTIC_MAP:
            return SEMANTIC_MAP[base]
        base_ = base.replace(" ", "_")
        if base_ in SEMANTIC_MAP:
            return SEMANTIC_MAP[base_]
    # Try removing "gcd" prefix
    if norm.startswith("gcd "):
        base = norm[4:]
        if base in SEMANTIC_MAP:
            return SEMANTIC_MAP[base]
        base_ = base.replace(" ", "_")
        if base_ in SEMANTIC_MAP:
            return SEMANTIC_MAP[base_]
    # Try removing "tds" or "hardness" suffix
    if norm.endswith(" tds"):
        base = norm[:-4].strip()
        if base in SEMANTIC_MAP:
            return SEMANTIC_MAP[base]
    if norm.endswith(" hardness"):
        base = norm[:-9].strip()
        if base in SEMANTIC_MAP:
            return SEMANTIC_MAP[base]
    # Return normalized input if nothing matches
    return norm.replace(" ", "_")

def get_related_terms(term: str) -> List[str]:
    normalized = normalize_term(term)
    related = []
    for k, v in SEMANTIC_MAP.items():
        if v == normalized and k != term:
            related.append(k)
    return related

def get_all_mappings() -> Dict[str, str]:
    return dict(SEMANTIC_MAP)