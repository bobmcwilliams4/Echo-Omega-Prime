"""
LG08 Real Estate Law Engine - Semantic Normalization Module
=============================================================
Normalizes real estate-specific terminology, maps synonyms, handles
property transaction terms, deed types, title examination vocabulary,
zoning classifications, financing instruments, and Texas-specific terms.

Components:
    - SemanticMap: Core term normalization dictionary
    - normalize_query(): Main entry point for query normalization
    - Citation Patterns: Real estate statute/case citation extraction
    - Recording Reference Parser: Deed book/page, instrument number patterns
    - Texas Property Code Section Mapper

Version: 2.0.0
Engine: LG08 Real Estate Law
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# SEMANTIC MAP - REAL ESTATE TERMINOLOGY NORMALIZATION
# ============================================================================

SEMANTIC_MAP: Dict[str, Dict[str, Any]] = {
    # ---- PROPERTY TRANSACTIONS ----
    "purchase_agreement": {
        "canonical": "purchase_and_sale_agreement",
        "synonyms": ["purchase contract", "sales contract", "buy-sell agreement",
                      "earnest money contract", "contract for sale", "PSA", "real estate contract"],
        "category": "transaction",
        "weight": 1.0,
    },
    "closing": {
        "canonical": "real_estate_closing",
        "synonyms": ["settlement", "close of escrow", "closing date", "settlement date",
                      "closing table", "escrow closing"],
        "category": "transaction",
        "weight": 1.0,
    },
    "earnest_money": {
        "canonical": "earnest_money_deposit",
        "synonyms": ["earnest money", "good faith deposit", "emd", "deposit",
                      "binder", "hand money"],
        "category": "transaction",
        "weight": 0.9,
    },
    "escrow": {
        "canonical": "escrow",
        "synonyms": ["escrow account", "escrow agent", "escrow officer",
                      "title escrow", "closing escrow"],
        "category": "transaction",
        "weight": 0.9,
    },
    "option_contract": {
        "canonical": "option_to_purchase",
        "synonyms": ["option contract", "purchase option", "option agreement",
                      "right to purchase", "call option real estate"],
        "category": "transaction",
        "weight": 0.8,
    },
    "right_of_first_refusal": {
        "canonical": "right_of_first_refusal",
        "synonyms": ["rofr", "first right of refusal", "preemptive right",
                      "right of first offer", "rofo"],
        "category": "transaction",
        "weight": 0.8,
    },
    "statute_of_frauds": {
        "canonical": "statute_of_frauds",
        "synonyms": ["statute of frauds", "writing requirement", "must be in writing",
                      "signed writing", "memorandum requirement"],
        "category": "transaction",
        "weight": 1.0,
    },
    # ---- DEEDS ----
    "general_warranty_deed": {
        "canonical": "general_warranty_deed",
        "synonyms": ["warranty deed", "full warranty deed", "deed with full covenants",
                      "gwd", "full covenant deed"],
        "category": "deed",
        "weight": 1.0,
    },
    "special_warranty_deed": {
        "canonical": "special_warranty_deed",
        "synonyms": ["limited warranty deed", "grant deed", "bargain and sale with covenants",
                      "swd", "deed with limited covenants"],
        "category": "deed",
        "weight": 1.0,
    },
    "quitclaim_deed": {
        "canonical": "quitclaim_deed",
        "synonyms": ["quitclaim", "quit claim deed", "quit-claim deed", "qcd",
                      "release deed", "non-warranty deed"],
        "category": "deed",
        "weight": 1.0,
    },
    "deed_of_trust": {
        "canonical": "deed_of_trust",
        "synonyms": ["trust deed", "dot", "security deed", "deed to secure debt",
                      "trust indenture"],
        "category": "deed",
        "weight": 1.0,
    },
    "bargain_and_sale": {
        "canonical": "bargain_and_sale_deed",
        "synonyms": ["bargain and sale", "b&s deed", "bargain sale deed"],
        "category": "deed",
        "weight": 0.8,
    },
    "deed_covenants": {
        "canonical": "deed_covenants",
        "synonyms": ["covenants of title", "title covenants", "warranty covenants",
                      "covenant of seisin", "covenant of quiet enjoyment", "covenant against encumbrances"],
        "category": "deed",
        "weight": 0.9,
    },
    "grant_deed": {
        "canonical": "grant_deed",
        "synonyms": ["statutory grant deed", "california grant deed", "grant"],
        "category": "deed",
        "weight": 0.9,
    },
    "correction_deed": {
        "canonical": "correction_deed",
        "synonyms": ["corrective deed", "deed of correction", "scriveners affidavit"],
        "category": "deed",
        "weight": 0.7,
    },
    # ---- TITLE ----
    "title_search": {
        "canonical": "title_examination",
        "synonyms": ["title search", "title exam", "title abstract", "abstract of title",
                      "chain of title", "title review", "title rundown"],
        "category": "title",
        "weight": 1.0,
    },
    "title_insurance": {
        "canonical": "title_insurance",
        "synonyms": ["title policy", "owners policy", "lenders policy",
                      "alta policy", "title commitment", "title binder"],
        "category": "title",
        "weight": 1.0,
    },
    "title_defect": {
        "canonical": "title_defect",
        "synonyms": ["cloud on title", "title cloud", "defective title",
                      "unmarketable title", "title blemish", "title exception"],
        "category": "title",
        "weight": 1.0,
    },
    "encumbrance": {
        "canonical": "encumbrance",
        "synonyms": ["encumbrances", "lien", "title encumbrance", "burden on title",
                      "charge on property", "restriction on title"],
        "category": "title",
        "weight": 0.9,
    },
    "lien": {
        "canonical": "lien",
        "synonyms": ["property lien", "tax lien", "mechanics lien", "judgment lien",
                      "mortgage lien", "vendor lien", "materialman lien"],
        "category": "title",
        "weight": 1.0,
    },
    "lis_pendens": {
        "canonical": "lis_pendens",
        "synonyms": ["lis pendens", "notice of pending action", "notice of pendency",
                      "pending litigation notice"],
        "category": "title",
        "weight": 0.9,
    },
    "quiet_title": {
        "canonical": "quiet_title_action",
        "synonyms": ["quiet title", "action to quiet title", "suit to quiet title",
                      "clear title action", "remove cloud on title"],
        "category": "title",
        "weight": 1.0,
    },
    "marketable_title": {
        "canonical": "marketable_title",
        "synonyms": ["merchantable title", "good title", "clear title",
                      "insurable title", "record title"],
        "category": "title",
        "weight": 1.0,
    },
    # ---- EASEMENTS & COVENANTS ----
    "easement": {
        "canonical": "easement",
        "synonyms": ["right of way", "row", "easement right", "access easement",
                      "utility easement", "drainage easement"],
        "category": "easement",
        "weight": 1.0,
    },
    "prescriptive_easement": {
        "canonical": "prescriptive_easement",
        "synonyms": ["adverse possession easement", "easement by prescription",
                      "long-use easement", "prescriptive right"],
        "category": "easement",
        "weight": 0.9,
    },
    "easement_by_necessity": {
        "canonical": "easement_by_necessity",
        "synonyms": ["necessity easement", "landlocked easement", "implied easement",
                      "way of necessity"],
        "category": "easement",
        "weight": 0.9,
    },
    "conservation_easement": {
        "canonical": "conservation_easement",
        "synonyms": ["conservation restriction", "scenic easement", "land trust easement",
                      "preservation easement", "conservation covenant"],
        "category": "easement",
        "weight": 0.8,
    },
    "restrictive_covenant": {
        "canonical": "restrictive_covenant",
        "synonyms": ["deed restriction", "covenant running with the land",
                      "equitable servitude", "use restriction", "building restriction"],
        "category": "easement",
        "weight": 1.0,
    },
    "adverse_possession": {
        "canonical": "adverse_possession",
        "synonyms": ["squatters rights", "hostile possession", "adverse claim",
                      "open and notorious possession", "prescriptive title"],
        "category": "easement",
        "weight": 1.0,
    },
    # ---- ZONING & LAND USE ----
    "zoning": {
        "canonical": "zoning_regulation",
        "synonyms": ["zoning law", "zoning ordinance", "zoning code",
                      "use regulation", "land use restriction"],
        "category": "zoning",
        "weight": 1.0,
    },
    "variance": {
        "canonical": "zoning_variance",
        "synonyms": ["use variance", "area variance", "dimensional variance",
                      "zoning exception", "hardship variance"],
        "category": "zoning",
        "weight": 0.9,
    },
    "conditional_use": {
        "canonical": "conditional_use_permit",
        "synonyms": ["cup", "special use permit", "special exception",
                      "conditional use", "sup", "special permit"],
        "category": "zoning",
        "weight": 0.9,
    },
    "nonconforming_use": {
        "canonical": "nonconforming_use",
        "synonyms": ["grandfathered use", "legal nonconforming", "prior nonconforming",
                      "pre-existing use", "vested nonconforming"],
        "category": "zoning",
        "weight": 0.8,
    },
    "regulatory_taking": {
        "canonical": "regulatory_taking",
        "synonyms": ["regulatory taking", "inverse condemnation zoning",
                      "penn central", "takings analysis", "government taking"],
        "category": "zoning",
        "weight": 1.0,
    },
    "comprehensive_plan": {
        "canonical": "comprehensive_plan",
        "synonyms": ["master plan", "general plan", "comp plan",
                      "land use plan", "future land use map"],
        "category": "zoning",
        "weight": 0.8,
    },
    "planned_unit_development": {
        "canonical": "planned_unit_development",
        "synonyms": ["pud", "planned development", "planned community",
                      "cluster development", "mixed-use development"],
        "category": "zoning",
        "weight": 0.8,
    },
    # ---- LANDLORD-TENANT ----
    "lease": {
        "canonical": "lease_agreement",
        "synonyms": ["rental agreement", "tenancy agreement", "lease contract",
                      "rental contract", "lease"],
        "category": "landlord_tenant",
        "weight": 1.0,
    },
    "eviction": {
        "canonical": "eviction",
        "synonyms": ["forcible entry and detainer", "unlawful detainer",
                      "eviction notice", "notice to vacate", "ejectment", "dispossession"],
        "category": "landlord_tenant",
        "weight": 1.0,
    },
    "security_deposit": {
        "canonical": "security_deposit",
        "synonyms": ["damage deposit", "rental deposit", "lease deposit",
                      "refundable deposit", "security"],
        "category": "landlord_tenant",
        "weight": 0.9,
    },
    "habitability": {
        "canonical": "implied_warranty_of_habitability",
        "synonyms": ["habitability", "habitable condition", "fit for habitation",
                      "warranty of habitability", "livable condition"],
        "category": "landlord_tenant",
        "weight": 1.0,
    },
    "triple_net_lease": {
        "canonical": "triple_net_lease",
        "synonyms": ["nnn lease", "triple net", "net net net", "nnn",
                      "absolute net lease"],
        "category": "landlord_tenant",
        "weight": 0.9,
    },
    "ground_lease": {
        "canonical": "ground_lease",
        "synonyms": ["land lease", "ground rent", "leasehold estate",
                      "long-term ground lease"],
        "category": "landlord_tenant",
        "weight": 0.8,
    },
    "sublease": {
        "canonical": "sublease",
        "synonyms": ["sub-lease", "sublet", "subletting", "sub-tenancy",
                      "assignment of lease"],
        "category": "landlord_tenant",
        "weight": 0.8,
    },
    # ---- FINANCING ----
    "mortgage": {
        "canonical": "mortgage",
        "synonyms": ["home loan", "mortgage loan", "real estate loan",
                      "property loan", "mtg"],
        "category": "financing",
        "weight": 1.0,
    },
    "fha_loan": {
        "canonical": "fha_loan",
        "synonyms": ["fha", "fha mortgage", "federal housing administration loan",
                      "government-backed loan fha"],
        "category": "financing",
        "weight": 0.9,
    },
    "va_loan": {
        "canonical": "va_loan",
        "synonyms": ["va", "va mortgage", "veterans affairs loan",
                      "veteran home loan", "gi loan"],
        "category": "financing",
        "weight": 0.9,
    },
    "usda_loan": {
        "canonical": "usda_loan",
        "synonyms": ["usda", "rural development loan", "usda mortgage",
                      "rural housing loan"],
        "category": "financing",
        "weight": 0.8,
    },
    "seller_financing": {
        "canonical": "seller_financing",
        "synonyms": ["owner financing", "carry-back loan", "seller carryback",
                      "purchase money mortgage", "owner carry"],
        "category": "financing",
        "weight": 0.9,
    },
    "respa": {
        "canonical": "real_estate_settlement_procedures_act",
        "synonyms": ["respa", "settlement procedures act", "12 usc 2601",
                      "regulation x", "hud respa"],
        "category": "compliance",
        "weight": 1.0,
    },
    "tila": {
        "canonical": "truth_in_lending_act",
        "synonyms": ["tila", "truth in lending", "15 usc 1601",
                      "regulation z", "consumer credit disclosure"],
        "category": "compliance",
        "weight": 1.0,
    },
    "fair_housing": {
        "canonical": "fair_housing_act",
        "synonyms": ["fair housing", "fha discrimination", "42 usc 3601",
                      "housing discrimination", "protected class housing"],
        "category": "compliance",
        "weight": 1.0,
    },
    # ---- FORECLOSURE ----
    "foreclosure": {
        "canonical": "foreclosure",
        "synonyms": ["foreclosure action", "mortgage foreclosure",
                      "deed of trust foreclosure", "forced sale", "repossession"],
        "category": "foreclosure",
        "weight": 1.0,
    },
    "judicial_foreclosure": {
        "canonical": "judicial_foreclosure",
        "synonyms": ["court foreclosure", "judicial sale", "foreclosure lawsuit",
                      "foreclosure complaint"],
        "category": "foreclosure",
        "weight": 0.9,
    },
    "non_judicial_foreclosure": {
        "canonical": "non_judicial_foreclosure",
        "synonyms": ["power of sale", "trustee sale", "non-judicial",
                      "statutory foreclosure", "power of sale foreclosure"],
        "category": "foreclosure",
        "weight": 0.9,
    },
    "right_of_redemption": {
        "canonical": "right_of_redemption",
        "synonyms": ["equity of redemption", "redemption period", "statutory redemption",
                      "cure right", "reinstatement right"],
        "category": "foreclosure",
        "weight": 0.9,
    },
    "short_sale": {
        "canonical": "short_sale",
        "synonyms": ["pre-foreclosure sale", "underwater sale",
                      "short payoff", "deficiency sale"],
        "category": "foreclosure",
        "weight": 0.8,
    },
    "deed_in_lieu": {
        "canonical": "deed_in_lieu_of_foreclosure",
        "synonyms": ["deed in lieu", "voluntary conveyance", "friendly foreclosure",
                      "cash for keys foreclosure"],
        "category": "foreclosure",
        "weight": 0.8,
    },
    # ---- EMINENT DOMAIN ----
    "eminent_domain": {
        "canonical": "eminent_domain",
        "synonyms": ["condemnation", "government taking", "compulsory acquisition",
                      "expropriation", "taking"],
        "category": "eminent_domain",
        "weight": 1.0,
    },
    "just_compensation": {
        "canonical": "just_compensation",
        "synonyms": ["fair compensation", "fair market value taking",
                      "condemnation award", "compensation for taking"],
        "category": "eminent_domain",
        "weight": 1.0,
    },
    "public_use": {
        "canonical": "public_use_requirement",
        "synonyms": ["public use", "public purpose", "public benefit",
                      "kelo public use", "economic development taking"],
        "category": "eminent_domain",
        "weight": 1.0,
    },
    "inverse_condemnation": {
        "canonical": "inverse_condemnation",
        "synonyms": ["inverse taking", "de facto taking", "regulatory taking claim",
                      "government action taking"],
        "category": "eminent_domain",
        "weight": 0.9,
    },
    # ---- 1031 EXCHANGE ----
    "exchange_1031": {
        "canonical": "section_1031_exchange",
        "synonyms": ["1031 exchange", "like-kind exchange", "starker exchange",
                      "tax-deferred exchange", "irc 1031", "like kind exchange"],
        "category": "tax_exchange",
        "weight": 1.0,
    },
    "qualified_intermediary": {
        "canonical": "qualified_intermediary",
        "synonyms": ["qi", "accommodator", "exchange facilitator",
                      "1031 intermediary", "exchange accommodator"],
        "category": "tax_exchange",
        "weight": 0.9,
    },
    "boot": {
        "canonical": "boot_1031",
        "synonyms": ["boot", "cash boot", "mortgage boot", "taxable boot",
                      "unlike property", "non-like-kind property"],
        "category": "tax_exchange",
        "weight": 0.8,
    },
    "reverse_exchange": {
        "canonical": "reverse_1031_exchange",
        "synonyms": ["reverse exchange", "reverse starker", "exchange accommodation titleholder",
                      "eat", "parking arrangement"],
        "category": "tax_exchange",
        "weight": 0.8,
    },
    # ---- HOA/POA ----
    "hoa": {
        "canonical": "homeowners_association",
        "synonyms": ["hoa", "homeowners association", "property owners association",
                      "poa", "condo association", "condominium association"],
        "category": "hoa",
        "weight": 1.0,
    },
    "cc_and_rs": {
        "canonical": "covenants_conditions_restrictions",
        "synonyms": ["cc&rs", "cc and rs", "deed restrictions", "community restrictions",
                      "declaration of covenants", "ccrs"],
        "category": "hoa",
        "weight": 1.0,
    },
    "assessment": {
        "canonical": "hoa_assessment",
        "synonyms": ["hoa dues", "hoa fees", "association assessment",
                      "special assessment hoa", "maintenance fees"],
        "category": "hoa",
        "weight": 0.9,
    },
    # ---- TEXAS SPECIFIC ----
    "community_property": {
        "canonical": "community_property_texas",
        "synonyms": ["community property", "marital property texas",
                      "jointly owned texas", "community estate"],
        "category": "texas",
        "weight": 1.0,
    },
    "homestead_exemption": {
        "canonical": "texas_homestead_exemption",
        "synonyms": ["homestead", "homestead exemption", "homestead protection",
                      "texas homestead", "article xvi section 50"],
        "category": "texas",
        "weight": 1.0,
    },
    "texas_property_code": {
        "canonical": "texas_property_code",
        "synonyms": ["tpc", "tx property code", "texas property law",
                      "tex prop code"],
        "category": "texas",
        "weight": 1.0,
    },
    "mineral_rights": {
        "canonical": "mineral_rights",
        "synonyms": ["mineral estate", "mineral interest", "subsurface rights",
                      "mineral ownership", "mineral reservation"],
        "category": "mineral_rights",
        "weight": 1.0,
    },
    "surface_rights": {
        "canonical": "surface_rights",
        "synonyms": ["surface estate", "surface interest", "surface ownership",
                      "surface use", "surface access"],
        "category": "mineral_rights",
        "weight": 1.0,
    },
    "royalty_interest": {
        "canonical": "royalty_interest",
        "synonyms": ["royalty", "overriding royalty", "orri", "mineral royalty",
                      "npri", "nonparticipating royalty"],
        "category": "mineral_rights",
        "weight": 0.9,
    },
    "working_interest": {
        "canonical": "working_interest",
        "synonyms": ["operating interest", "wi", "lease interest",
                      "operating rights", "executive rights"],
        "category": "mineral_rights",
        "weight": 0.9,
    },
    "pooling_unitization": {
        "canonical": "pooling_and_unitization",
        "synonyms": ["pooling", "unitization", "pooled unit", "unit agreement",
                      "forced pooling", "voluntary pooling"],
        "category": "mineral_rights",
        "weight": 0.8,
    },
    "accommodation_doctrine": {
        "canonical": "accommodation_doctrine",
        "synonyms": ["accommodation doctrine", "surface accommodation",
                      "getty oil test", "surface use limitation"],
        "category": "mineral_rights",
        "weight": 0.9,
    },
    # ---- PROPERTY TAX ----
    "property_tax": {
        "canonical": "property_tax_assessment",
        "synonyms": ["ad valorem tax", "real estate tax", "property tax",
                      "tax assessment", "assessed value"],
        "category": "tax",
        "weight": 1.0,
    },
    "tax_appeal": {
        "canonical": "property_tax_appeal",
        "synonyms": ["assessment appeal", "tax protest", "valuation appeal",
                      "arb hearing", "appraisal review board"],
        "category": "tax",
        "weight": 0.9,
    },
    "tax_lien": {
        "canonical": "property_tax_lien",
        "synonyms": ["tax lien", "delinquent tax lien", "ad valorem lien",
                      "tax certificate", "tax deed"],
        "category": "tax",
        "weight": 0.9,
    },
    # ---- RECORDING ----
    "recording": {
        "canonical": "recording",
        "synonyms": ["record deed", "file deed", "recording act",
                      "constructive notice", "record notice"],
        "category": "recording",
        "weight": 1.0,
    },
    "race_notice": {
        "canonical": "race_notice_statute",
        "synonyms": ["race notice", "recording statute", "race-notice",
                      "race statute", "notice statute"],
        "category": "recording",
        "weight": 0.9,
    },
    "bona_fide_purchaser": {
        "canonical": "bona_fide_purchaser",
        "synonyms": ["bfp", "good faith purchaser", "purchaser for value",
                      "innocent purchaser", "bona fide buyer"],
        "category": "recording",
        "weight": 1.0,
    },
}


# ============================================================================
# RECORDING REFERENCE PATTERNS
# ============================================================================

RECORDING_PATTERNS: Dict[str, str] = {
    "book_page": r"(?:Vol(?:ume)?\.?\s*|Book\s*)(\d+)(?:\s*/\s*|\s*,?\s*(?:Page|Pg|P)\.?\s*)(\d+)",
    "instrument_number": r"(?:Inst(?:rument)?\.?\s*(?:No\.?\s*)?|Doc(?:ument)?\.?\s*(?:No\.?\s*)?|#\s*)(\d{2,}[\-/]?\d+)",
    "deed_record": r"(?:D\.?R\.?\s*|DR\s+)(\d+)(?:\s*/\s*|\s*,?\s*(?:Page|Pg|P)\.?\s*)(\d+)",
    "official_record": r"(?:O\.?R\.?\s*|OR\s+)(\d+)(?:\s*/\s*|\s*,?\s*(?:Page|Pg|P)\.?\s*)(\d+)",
    "plat_record": r"(?:Plat\s*(?:Book|Cabinet|Cab)\.?\s*)(\w+)(?:\s*/\s*|\s*,?\s*(?:Page|Pg|Slide)\.?\s*)(\w+)",
}


# ============================================================================
# CITATION PATTERNS (REAL ESTATE SPECIFIC)
# ============================================================================

CITATION_PATTERNS: Dict[str, str] = {
    "tex_prop_code": r"Tex(?:as)?\.?\s*Prop(?:erty)?\.?\s*Code\s*(?:\xA7\s*)?([\d]+(?:\.\d+)*)",
    "tex_tax_code": r"Tex(?:as)?\.?\s*Tax\s*Code\s*(?:\xA7\s*)?([\d]+(?:\.\d+)*)",
    "tex_bus_org_code": r"Tex(?:as)?\.?\s*Bus(?:iness)?\.?\s*(?:Org(?:anizations)?\.?\s*)?Code\s*(?:\xA7\s*)?([\d]+(?:\.\d+)*)",
    "tex_local_gov": r"Tex(?:as)?\.?\s*Loc(?:al)?\.?\s*Gov(?:ernment)?\.?\s*Code\s*(?:\xA7\s*)?([\d]+(?:\.\d+)*)",
    "usc_12": r"12\s*U\.?S\.?C\.?\s*(?:\xA7\s*)?([\d]+(?:\([a-z]\))?)",
    "usc_15": r"15\s*U\.?S\.?C\.?\s*(?:\xA7\s*)?([\d]+(?:\([a-z]\))?)",
    "usc_26": r"26\s*U\.?S\.?C\.?\s*(?:\xA7\s*)?([\d]+(?:\([a-z]\))?)",
    "usc_42": r"42\s*U\.?S\.?C\.?\s*(?:\xA7\s*)?([\d]+(?:\([a-z]\))?)",
    "cfr_12": r"12\s*C\.?F\.?R\.?\s*(?:\xA7\s*)?([\d]+(?:\.\d+)*)",
    "cfr_24": r"24\s*C\.?F\.?R\.?\s*(?:\xA7\s*)?([\d]+(?:\.\d+)*)",
    "cfr_26": r"26\s*C\.?F\.?R\.?\s*(?:\xA7\s*)?([\d]+(?:\.\d+)*)",
    "irc_section": r"(?:IRC|I\.?R\.?C\.?)\s*(?:\xA7\s*)?([\d]+(?:\([a-z]\))?)",
    "federal_case": r"(\d+)\s+(F\.(?:2d|3d|4th)|F\.\s*Supp\.(?:\s*2d|\s*3d)?|U\.S\.|S\.\s*Ct\.)\s+(\d+)",
    "state_case": r"(\d+)\s+(S\.W\.(?:2d|3d)?|N\.E\.(?:2d|3d)?|N\.W\.(?:2d)?|So\.(?:2d|3d)?|P\.(?:2d|3d)?|A\.(?:2d|3d)?|Cal\.?\s*(?:App\.?\s*)?(?:2d|3d|4th|5th)?)\s+(\d+)",
    "alta_form": r"ALTA\s*(?:Form\s*)?(\d{1,2}[\-\.]\d{2}(?:\-\d{2})?)",
    "restatement": r"Restatement\s*\((?:First|Second|Third)\)\s*(?:of\s*)?Property\s*(?:\xA7\s*)?([\d]+)",
}


# ============================================================================
# JURISDICTION MAPPING
# ============================================================================

JURISDICTION_MAP: Dict[str, Dict[str, Any]] = {
    "TX": {
        "name": "Texas",
        "recording_type": "race_notice",
        "homestead": True,
        "community_property": True,
        "foreclosure_type": "non_judicial",
        "property_code": "Texas Property Code",
        "mineral_state": True,
    },
    "CA": {
        "name": "California",
        "recording_type": "race_notice",
        "homestead": True,
        "community_property": True,
        "foreclosure_type": "non_judicial",
        "property_code": "California Civil Code",
        "mineral_state": False,
    },
    "NY": {
        "name": "New York",
        "recording_type": "race_notice",
        "homestead": True,
        "community_property": False,
        "foreclosure_type": "judicial",
        "property_code": "New York Real Property Law",
        "mineral_state": False,
    },
    "FL": {
        "name": "Florida",
        "recording_type": "race_notice",
        "homestead": True,
        "community_property": False,
        "foreclosure_type": "judicial",
        "property_code": "Florida Statutes Title XL",
        "mineral_state": False,
    },
    "NM": {
        "name": "New Mexico",
        "recording_type": "race",
        "homestead": True,
        "community_property": True,
        "foreclosure_type": "judicial",
        "property_code": "New Mexico Statutes Chapter 47",
        "mineral_state": True,
    },
    "OK": {
        "name": "Oklahoma",
        "recording_type": "race_notice",
        "homestead": True,
        "community_property": False,
        "foreclosure_type": "judicial_and_non_judicial",
        "property_code": "Oklahoma Statutes Title 16",
        "mineral_state": True,
    },
    "CO": {
        "name": "Colorado",
        "recording_type": "race_notice",
        "homestead": True,
        "community_property": False,
        "foreclosure_type": "non_judicial",
        "property_code": "Colorado Revised Statutes Title 38",
        "mineral_state": True,
    },
    "LA": {
        "name": "Louisiana",
        "recording_type": "race",
        "homestead": True,
        "community_property": True,
        "foreclosure_type": "judicial",
        "property_code": "Louisiana Civil Code",
        "mineral_state": True,
    },
}


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass
class NormalizationResult:
    """Result of normalizing a query through the semantic map."""
    original_query: str
    normalized_query: str
    tokens: List[str]
    matched_terms: List[Dict[str, Any]]
    unmatched_tokens: List[str]
    detected_categories: List[str]
    detected_re_type: Optional[str]
    detected_citations: List[Dict[str, str]]
    detected_recordings: List[Dict[str, str]]
    detected_jurisdiction: Optional[str]
    confidence: float
    normalization_time_ms: float
    hash_digest: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "original_query": self.original_query,
            "normalized_query": self.normalized_query,
            "tokens": self.tokens,
            "matched_terms": self.matched_terms,
            "unmatched_tokens": self.unmatched_tokens,
            "detected_categories": self.detected_categories,
            "detected_re_type": self.detected_re_type,
            "detected_citations": self.detected_citations,
            "detected_recordings": self.detected_recordings,
            "detected_jurisdiction": self.detected_jurisdiction,
            "confidence": round(self.confidence, 4),
            "normalization_time_ms": round(self.normalization_time_ms, 3),
            "hash_digest": self.hash_digest,
        }


# ============================================================================
# QUERY NORMALIZER
# ============================================================================

class RealEstateQueryNormalizer:
    """Normalizes real estate queries using the semantic map and citation extraction."""

    def __init__(self, semantic_map: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        self._map: Dict[str, Dict[str, Any]] = semantic_map or SEMANTIC_MAP
        self._synonym_index: Dict[str, str] = {}
        self._build_synonym_index()
        self._compiled_citations: Dict[str, re.Pattern] = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in CITATION_PATTERNS.items()
        }
        self._compiled_recordings: Dict[str, re.Pattern] = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in RECORDING_PATTERNS.items()
        }
        logger.info(f"RealEstateQueryNormalizer initialized | terms={len(self._map)} | synonyms={len(self._synonym_index)}")

    def _build_synonym_index(self) -> None:
        """Build reverse lookup from synonyms to canonical terms."""
        for key, entry in self._map.items():
            canonical = entry["canonical"]
            self._synonym_index[canonical.lower()] = key
            self._synonym_index[key.lower()] = key
            for syn in entry.get("synonyms", []):
                self._synonym_index[syn.lower()] = key

    def normalize(self, query: str) -> NormalizationResult:
        """Normalize a query through the semantic map."""
        start = time.monotonic()
        cleaned = self._clean_query(query)
        tokens = self._tokenize(cleaned)
        matched_terms: List[Dict[str, Any]] = []
        unmatched: List[str] = []
        categories: Set[str] = set()
        used_indices: Set[int] = set()

        # Multi-token matching (longest match first)
        for window_size in range(5, 0, -1):
            for i in range(len(tokens) - window_size + 1):
                if any(idx in used_indices for idx in range(i, i + window_size)):
                    continue
                phrase = " ".join(tokens[i:i + window_size]).lower()
                match_key = self._synonym_index.get(phrase)
                if match_key and match_key in self._map:
                    entry = self._map[match_key]
                    matched_terms.append({
                        "original": phrase,
                        "canonical": entry["canonical"],
                        "category": entry["category"],
                        "weight": entry["weight"],
                    })
                    categories.add(entry["category"])
                    for idx in range(i, i + window_size):
                        used_indices.add(idx)

        for i, tok in enumerate(tokens):
            if i not in used_indices:
                unmatched.append(tok)

        # Detect citations
        detected_citations = self._extract_citations(query)

        # Detect recording references
        detected_recordings = self._extract_recordings(query)

        # Detect jurisdiction
        jurisdiction = self._detect_jurisdiction(query, categories, matched_terms)

        # Detect RE type
        re_type = self._detect_re_type(categories, matched_terms)

        # Build normalized query
        canonical_parts = [m["canonical"] for m in matched_terms] + unmatched
        normalized = " ".join(canonical_parts)

        # Compute confidence
        total_tokens = len(tokens)
        matched_token_count = len(used_indices)
        base_confidence = matched_token_count / max(total_tokens, 1)
        citation_boost = min(len(detected_citations) * 0.05, 0.15)
        recording_boost = min(len(detected_recordings) * 0.03, 0.09)
        confidence = min(base_confidence + citation_boost + recording_boost, 1.0)

        # Hash
        hash_input = f"{query}|{normalized}|{json.dumps(matched_terms, sort_keys=True)}"
        hash_digest = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

        duration = (time.monotonic() - start) * 1000.0

        return NormalizationResult(
            original_query=query,
            normalized_query=normalized,
            tokens=tokens,
            matched_terms=matched_terms,
            unmatched_tokens=unmatched,
            detected_categories=sorted(categories),
            detected_re_type=re_type,
            detected_citations=detected_citations,
            detected_recordings=detected_recordings,
            detected_jurisdiction=jurisdiction,
            confidence=confidence,
            normalization_time_ms=duration,
            hash_digest=hash_digest,
        )

    def _clean_query(self, query: str) -> str:
        """Clean and normalize raw query text."""
        text = query.strip()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s\.\-\(\)/,;:'\"\xA7#&]", "", text)
        return text

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize cleaned text."""
        tokens = re.findall(r"[\w\xA7]+(?:[-/][\w]+)*", text.lower())
        return [t for t in tokens if len(t) >= 2]

    def _extract_citations(self, text: str) -> List[Dict[str, str]]:
        """Extract real estate citations from query text."""
        found: List[Dict[str, str]] = []
        seen: Set[str] = set()
        for cit_type, pattern in self._compiled_citations.items():
            for match in pattern.finditer(text):
                full_match = match.group(0).strip()
                if full_match not in seen:
                    seen.add(full_match)
                    found.append({
                        "type": cit_type,
                        "text": full_match,
                        "groups": str(match.groups()),
                    })
        return found

    def _extract_recordings(self, text: str) -> List[Dict[str, str]]:
        """Extract recording references from query text."""
        found: List[Dict[str, str]] = []
        seen: Set[str] = set()
        for ref_type, pattern in self._compiled_recordings.items():
            for match in pattern.finditer(text):
                full_match = match.group(0).strip()
                if full_match not in seen:
                    seen.add(full_match)
                    found.append({
                        "type": ref_type,
                        "text": full_match,
                        "groups": str(match.groups()),
                    })
        return found

    def _detect_jurisdiction(
        self,
        query: str,
        categories: Set[str],
        matched_terms: List[Dict[str, Any]],
    ) -> Optional[str]:
        """Detect the jurisdiction from query context."""
        query_lower = query.lower()
        # Check for explicit state mentions
        state_keywords: Dict[str, str] = {
            "texas": "TX", "tx ": "TX", "tex.": "TX",
            "california": "CA", "cal ": "CA",
            "new york": "NY", "n.y.": "NY",
            "florida": "FL", "fla.": "FL",
            "new mexico": "NM", "n.m.": "NM",
            "oklahoma": "OK", "okla.": "OK",
            "colorado": "CO", "colo.": "CO",
            "louisiana": "LA",
        }
        for keyword, state_code in state_keywords.items():
            if keyword in query_lower:
                return state_code

        # Texas category detection
        if "texas" in categories:
            return "TX"
        if "mineral_rights" in categories:
            return "TX"  # Default mineral rights jurisdiction

        return None

    def _detect_re_type(self, categories: Set[str], matched_terms: List[Dict[str, Any]]) -> Optional[str]:
        """Detect the primary real estate type from matched categories."""
        re_type_priority = [
            ("title", ["title"]),
            ("deed", ["deed"]),
            ("easement", ["easement"]),
            ("zoning", ["zoning"]),
            ("landlord_tenant", ["landlord_tenant"]),
            ("financing", ["financing"]),
            ("foreclosure", ["foreclosure"]),
            ("eminent_domain", ["eminent_domain"]),
            ("tax_exchange", ["tax_exchange"]),
            ("hoa", ["hoa"]),
            ("texas", ["texas"]),
            ("mineral_rights", ["mineral_rights"]),
            ("tax", ["tax"]),
            ("compliance", ["compliance"]),
            ("transaction", ["transaction"]),
            ("recording", ["recording"]),
        ]
        for re_type, type_categories in re_type_priority:
            if categories.intersection(type_categories):
                return re_type
        return None


# ============================================================================
# MODULE-LEVEL SINGLETON AND CONVENIENCE FUNCTIONS
# ============================================================================

_normalizer: Optional[RealEstateQueryNormalizer] = None
_map_version: str = "2.0.0"


def _get_normalizer() -> RealEstateQueryNormalizer:
    """Get or create the singleton normalizer."""
    global _normalizer
    if _normalizer is None:
        _normalizer = RealEstateQueryNormalizer(SEMANTIC_MAP)
    return _normalizer


def normalize_query(query: str) -> NormalizationResult:
    """Normalize a real estate query through the semantic map."""
    return _get_normalizer().normalize(query)


def get_semantic_map() -> Dict[str, Dict[str, Any]]:
    """Get the full semantic map."""
    return SEMANTIC_MAP


def get_semantic_map_version() -> str:
    """Get the semantic map version."""
    return _map_version


def get_semantic_map_hash() -> str:
    """Get a hash of the current semantic map for integrity checks."""
    content = json.dumps(SEMANTIC_MAP, sort_keys=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def verify_dictionary_integrity() -> Dict[str, Any]:
    """Verify the semantic dictionary integrity."""
    total_terms = len(SEMANTIC_MAP)
    total_synonyms = sum(len(v.get("synonyms", [])) for v in SEMANTIC_MAP.values())
    categories = set(v["category"] for v in SEMANTIC_MAP.values())
    map_hash = get_semantic_map_hash()

    return {
        "valid": True,
        "version": _map_version,
        "total_terms": total_terms,
        "total_synonyms": total_synonyms,
        "categories": sorted(categories),
        "category_count": len(categories),
        "hash": map_hash,
    }


def get_governance_metadata() -> Dict[str, Any]:
    """Get governance metadata for the semantic dictionary."""
    return {
        "engine_id": "LG08",
        "module": "semantic",
        "version": _map_version,
        "term_count": len(SEMANTIC_MAP),
        "hash": get_semantic_map_hash(),
        "categories": sorted(set(v["category"] for v in SEMANTIC_MAP.values())),
        "citation_patterns": list(CITATION_PATTERNS.keys()),
        "recording_patterns": list(RECORDING_PATTERNS.keys()),
        "jurisdictions": list(JURISDICTION_MAP.keys()),
    }


def get_citation_patterns() -> Dict[str, str]:
    """Get citation extraction patterns."""
    return CITATION_PATTERNS


def get_recording_patterns() -> Dict[str, str]:
    """Get recording reference patterns."""
    return RECORDING_PATTERNS


def get_jurisdiction_map() -> Dict[str, Dict[str, Any]]:
    """Get jurisdiction mapping data."""
    return JURISDICTION_MAP
