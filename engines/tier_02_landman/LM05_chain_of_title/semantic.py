"""
LM05 Chain of Title Builder - Semantic Dictionary
====================================================
ECHO OMEGA PRIME - Landman Intelligence Division

Comprehensive chain of title terminology covering:
- Root of title, patent, sovereign grant terminology
- Chain links, breaks, gaps, and wild deeds
- Grantor/grantee index and tract index terminology
- Recording system terms (book/page, document number, recording date)
- Execution, acknowledgment, and delivery terms
- Mineral estate and conveyance terminology
- Texas-specific abstract/survey system terms
- Interest types and fractional ownership terms
- Curative and title examination terms

Each semantic entry contains:
    term: Canonical normalized term
    category: Classification
    aliases: Alternative names, abbreviations
    definition: Clear definition
    context: Usage context in chain of title work
    related_terms: Cross-references
    texas_notes: Texas-specific usage notes

Authority: Bobby Don McWilliams II (11.0 SUPREME SOVEREIGN)
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class SemanticEntry(BaseModel):
    """A single semantic dictionary entry."""
    term: str = Field(..., description="Canonical normalized term")
    category: str = Field(..., description="Semantic category")
    aliases: List[str] = Field(default_factory=list, description="Alternative names")
    abbreviations: List[str] = Field(default_factory=list, description="Common abbreviations")
    definition: str = Field(..., description="Clear definition")
    context: str = Field(default="", description="Usage context")
    related_terms: List[str] = Field(default_factory=list, description="Cross-references")
    texas_notes: str = Field(default="", description="Texas-specific notes")
    examples: List[str] = Field(default_factory=list, description="Usage examples")
    is_instrument_type: bool = Field(default=False, description="Whether this is a recordable instrument type")
    is_interest_type: bool = Field(default=False, description="Whether this is a type of property interest")


class SemanticDictionaryStats(BaseModel):
    """Statistics about the semantic dictionary."""
    total_entries: int = 0
    categories: Dict[str, int] = Field(default_factory=dict)
    total_aliases: int = 0
    total_abbreviations: int = 0
    last_loaded: str = ""
    dictionary_hash: str = ""


# ---------------------------------------------------------------------------
# Semantic dictionary entries
# ---------------------------------------------------------------------------

CHAIN_OF_TITLE_SEMANTICS: List[Dict[str, Any]] = [
    # ==================== CHAIN STRUCTURE TERMS ====================
    {
        "term": "chain_of_title",
        "category": "CHAIN_STRUCTURE",
        "aliases": ["chain", "title chain", "title history", "ownership chain", "conveyance chain"],
        "abbreviations": ["COT"],
        "definition": "The sequential history of title to a particular parcel of land, traced through recorded instruments from the sovereign patent to the present owner. Each link in the chain represents a conveyance or other transfer of ownership.",
        "context": "The chain of title is the fundamental output of a title search. It must show an unbroken sequence of conveyances from the sovereign to the current owner.",
        "related_terms": ["link_in_chain", "break_in_chain", "root_of_title", "run_sheet"],
        "texas_notes": "In Texas, the chain traces back to the sovereign patent from the Republic or State of Texas.",
        "examples": ["The chain of title shows 12 conveyances from the 1903 patent to the current owner."]
    },
    {
        "term": "link_in_chain",
        "category": "CHAIN_STRUCTURE",
        "aliases": ["chain link", "title link", "conveyance link"],
        "abbreviations": [],
        "definition": "A single instrument in the chain of title that transfers or affects ownership. Each link connects a grantor to a grantee and represents one step in the chain. A valid link requires proper execution, acknowledgment, delivery, and recording.",
        "context": "Each link in the chain must be verified for proper execution and legal sufficiency. A defective link weakens the entire chain.",
        "related_terms": ["chain_of_title", "break_in_chain", "gap_in_chain"],
        "texas_notes": "Texas requires acknowledgment before a notary for a link to provide constructive notice.",
        "examples": ["The 1945 warranty deed from Smith to Jones is the seventh link in the chain."]
    },
    {
        "term": "break_in_chain",
        "category": "CHAIN_STRUCTURE",
        "aliases": ["chain break", "title break", "broken chain", "chain defect", "chain interruption"],
        "abbreviations": [],
        "definition": "A discontinuity in the chain of title where the grantee of one instrument does not match the grantor of the next. This indicates a missing instrument, unrecorded transfer, or other defect that must be cured.",
        "context": "A break in the chain is a critical title defect that must be resolved before title can be considered marketable.",
        "related_terms": ["gap_in_chain", "wild_deed", "curative_instrument"],
        "texas_notes": "Breaks are commonly caused by heirship not established by affidavit, divorce not reflected in deed records, or entity succession not documented.",
        "examples": ["There is a break in the chain between 1952 and 1967 where no recorded instrument connects the Smith heirs to the Jones purchase."]
    },
    {
        "term": "gap_in_chain",
        "category": "CHAIN_STRUCTURE",
        "aliases": ["title gap", "chain gap", "temporal gap", "recording gap"],
        "abbreviations": [],
        "definition": "A period in the chain where no recorded activity appears, or where the instruments do not fully account for the transfer of ownership. Gaps may be temporal (time periods with no activity) or substantive (missing conveyance linking two known parties).",
        "context": "Gaps must be classified by type and severity. Short temporal gaps may be normal; substantive gaps require curative action.",
        "related_terms": ["break_in_chain", "temporal_gap", "conveyance_gap"],
        "texas_notes": "In Texas O&G title, any gap over 5 years should be investigated. Gaps are commonly caused by deaths without recorded heirship.",
        "examples": ["A 15-year gap exists between 1938 and 1953 during which no instruments were recorded affecting the Smith mineral interest."]
    },
    {
        "term": "root_of_title",
        "category": "CHAIN_STRUCTURE",
        "aliases": ["title root", "starting point", "chain origin", "search root"],
        "abbreviations": [],
        "definition": "The instrument selected as the starting point for the chain of title search. For standard title examination, the root should be at least 40-60 years old. For oil and gas title, the root is typically the sovereign patent.",
        "context": "Root selection determines the depth and completeness of the chain examination. An inadequate root may miss early severances and reservations.",
        "related_terms": ["chain_of_title", "sovereign_patent", "marketable_title"],
        "texas_notes": "Texas has no Marketable Title Act, so the root is selected by professional judgment. O&G practice traces to sovereign patent.",
        "examples": ["The root of title is the 1903 State of Texas patent to H.G. Chandler, Abstract 234."]
    },
    {
        "term": "run_sheet",
        "category": "CHAIN_STRUCTURE",
        "aliases": ["title abstract", "abstract of title", "title rundown", "ownership rundown"],
        "abbreviations": [],
        "definition": "A chronological listing of all recorded instruments affecting a particular tract of land. The run sheet is the working document from which the chain of title is constructed. It includes all conveyances, encumbrances, releases, and other instruments.",
        "context": "The run sheet is the landman's primary work product during title examination. It lists every instrument in the chain with key details.",
        "related_terms": ["chain_of_title", "abstract_of_title", "title_opinion"],
        "texas_notes": "Standard landman run sheet format includes: entry number, instrument type, recording date, volume/page, doc number, grantor, grantee, legal description, interest conveyed, reservations, exceptions, consideration, and remarks.",
        "examples": ["The run sheet for Section 270, Block 13, H&GN RR Co. Survey contains 47 entries spanning 1903-2024."]
    },
    {
        "term": "wild_deed",
        "category": "CHAIN_STRUCTURE",
        "aliases": ["stray instrument", "wild instrument", "unconnected deed", "orphan deed"],
        "abbreviations": [],
        "definition": "A recorded instrument that cannot be connected to the chain of title through the grantor-grantee index. The grantor of a wild deed never appears as a grantee in the chain. Wild deeds do not provide constructive notice under the grantor-grantee index system.",
        "context": "Wild deeds are recorded but invisible to a standard chain search. They represent potential competing claims that may or may not be valid.",
        "related_terms": ["break_in_chain", "constructive_notice", "grantor_grantee_index"],
        "texas_notes": "In Texas, wild deeds do not provide constructive notice. They may be found through a tract index search but not through standard grantor-grantee search.",
        "examples": ["A deed from Brown to Green recorded in 1965 appears to be a wild deed because Brown never appears as a grantee in the chain."]
    },
    {
        "term": "stray_instrument",
        "category": "CHAIN_STRUCTURE",
        "aliases": ["stray", "unlinked instrument", "floating instrument"],
        "abbreviations": [],
        "definition": "An instrument that appears to affect the subject tract but cannot be definitively connected to the chain. Unlike a wild deed, a stray instrument may involve known parties but the connection is unclear or the legal description is ambiguous.",
        "context": "Stray instruments must be investigated to determine if they affect the chain. They may be Mother Hubbard clause pickups or misdescribed tracts.",
        "related_terms": ["wild_deed", "mother_hubbard_clause", "legal_description"],
        "texas_notes": "In the Permian Basin, stray instruments are common due to the large number of mineral conveyances and variations in legal descriptions.",
        "examples": ["An assignment of OGL references Block 13 but does not specify a section number, making it a stray instrument."]
    },

    # ==================== SOVEREIGN AND PATENT TERMS ====================
    {
        "term": "sovereign_patent",
        "category": "SOVEREIGN",
        "aliases": ["land patent", "patent", "original patent", "sovereign grant", "government patent"],
        "abbreviations": ["PAT"],
        "definition": "The original conveyance of land from the sovereign (government) to a private party. In Texas, patents were issued by the Republic of Texas or State of Texas through the General Land Office. The patent is the first link in every chain of title.",
        "context": "The sovereign patent is the ultimate root of title. All private ownership derives from the sovereign grant.",
        "related_terms": ["root_of_title", "general_land_office", "headright", "bounty_warrant"],
        "texas_notes": "Texas patents come from the Republic or State of Texas (not the federal government). The GLO maintains all patent records.",
        "examples": ["Patent from the State of Texas to H.G. Chandler, dated March 14, 1903, for Abstract 234, Section 270, Block 13."],
        "is_instrument_type": True
    },
    {
        "term": "headright",
        "category": "SOVEREIGN",
        "aliases": ["headright grant", "headright certificate", "first class headright"],
        "abbreviations": [],
        "definition": "A land grant issued by the Republic of Texas to settlers who were present in Texas at the time of independence (1836) or shortly thereafter. First class headrights were 4,605 acres for heads of families; second and third class were smaller grants for later arrivals.",
        "context": "Headrights are the root of many West Texas chains. The certificate was issued first, then located on a specific survey, then patented.",
        "related_terms": ["sovereign_patent", "bounty_warrant", "general_land_office"],
        "texas_notes": "Republic of Texas headright certificates were freely transferable and were often sold, creating a secondary market.",
        "examples": ["First class headright certificate No. 789, located on Survey 270, Block 13, patented in 1903."],
        "is_instrument_type": True
    },
    {
        "term": "bounty_warrant",
        "category": "SOVEREIGN",
        "aliases": ["bounty land warrant", "military warrant", "bounty grant"],
        "abbreviations": [],
        "definition": "A land grant issued to soldiers for military service, particularly during the Texas Revolution. Bounty warrants could be located on any available public land and were freely transferable.",
        "context": "Bounty warrants appear as root instruments in chains for lands surveyed under military certificates.",
        "related_terms": ["sovereign_patent", "headright", "general_land_office"],
        "texas_notes": "Texas bounty warrants were authorized by the Republic of Texas for service in the Texas Revolution and related campaigns.",
        "examples": ["Bounty warrant for 640 acres issued to J. Smith for service in the Texas Revolution, located on Survey 15."]
    },
    {
        "term": "general_land_office",
        "category": "SOVEREIGN",
        "aliases": ["GLO", "Texas Land Office", "Land Office"],
        "abbreviations": ["GLO"],
        "definition": "The Texas General Land Office is the state agency responsible for managing state lands, including issuing patents, maintaining survey records, and managing the Permanent School Fund lands. The GLO holds all original patent records and survey field notes.",
        "context": "The GLO is the primary source for sovereign patent information. Chain examiners must reference GLO records to verify the patent at the top of every chain.",
        "related_terms": ["sovereign_patent", "school_land", "abstract_number"],
        "texas_notes": "The GLO archives are available online at glo.texas.gov. All patent files, field notes, and land grant certificates are archived.",
        "examples": ["GLO File No. 12345, Patent to H.G. Chandler for Abstract 234, Reeves County."]
    },
    {
        "term": "empresario_grant",
        "category": "SOVEREIGN",
        "aliases": ["empresario", "colonization grant", "Austin colony grant"],
        "abbreviations": [],
        "definition": "Land grants made to empresarios (colonization agents) by the Spanish and Mexican governments to encourage settlement of Texas. Stephen F. Austin was the most well-known empresario. Empresario grants typically included large tracts distributed to colonists.",
        "context": "Empresario grants are the root of title in many Central and South Texas areas. Their validity was confirmed by the Republic of Texas.",
        "related_terms": ["sovereign_patent", "spanish_grant", "mexican_grant"],
        "texas_notes": "Austin's Colony grants are the root of title for much of Central Texas. The Bourland-Miller Commission confirmed many Mexican-era grants.",
        "examples": ["Empresario grant from Mexico to Stephen F. Austin for colonization of Gonzales area."]
    },

    # ==================== INDEX AND RECORDING TERMS ====================
    {
        "term": "grantor_grantee_index",
        "category": "RECORDING_SYSTEM",
        "aliases": ["grantor index", "grantee index", "direct index", "reverse index", "official index"],
        "abbreviations": ["G-G Index", "GGI"],
        "definition": "The official system for indexing recorded instruments by party names. The grantor (direct) index is alphabetical by grantor name; the grantee (reverse) index is alphabetical by grantee name. This is the primary search tool for constructing the chain of title.",
        "context": "The grantor-grantee index is how instruments are found during a title search. Searching the grantor index reveals what a person conveyed; searching the grantee index reveals what they received.",
        "related_terms": ["tract_index", "recording_date", "volume_page", "document_number"],
        "texas_notes": "Texas county clerks maintain the official grantor-grantee index. It is the only index that provides constructive notice.",
        "examples": ["Search the grantor index under 'Smith, John' from 1950 to 1975 to find all conveyances by Smith during his ownership."]
    },
    {
        "term": "tract_index",
        "category": "RECORDING_SYSTEM",
        "aliases": ["parcel index", "property index", "land index", "geographic index"],
        "abbreviations": [],
        "definition": "An index of recorded instruments organized by the parcel of land affected rather than by party names. Not officially maintained in most Texas counties, but title companies and abstract companies often maintain their own tract indexes.",
        "context": "The tract index is a supplemental search tool that catches instruments missed by grantor-grantee name searches.",
        "related_terms": ["grantor_grantee_index", "abstract_number", "legal_description"],
        "texas_notes": "Texas does not require a tract index, but Permian Basin title companies maintain excellent tract indexes. The tract index is organized by abstract/survey/block.",
        "examples": ["The tract index for Abstract 234 shows 52 recorded instruments from 1903 to present."]
    },
    {
        "term": "volume_page",
        "category": "RECORDING_SYSTEM",
        "aliases": ["book and page", "vol/pg", "book/page", "liber/page", "volume and page"],
        "abbreviations": ["Vol.", "Pg.", "Bk.", "V/P", "B/P"],
        "definition": "The traditional method of identifying the location of a recorded instrument in the county deed records. Each instrument is recorded in a numbered volume at a specific page. This is the primary citation method for older instruments.",
        "context": "Volume/page references are used to locate instruments in the physical deed records. Newer instruments may also have document numbers.",
        "related_terms": ["document_number", "recording_date", "official_records"],
        "texas_notes": "Texas counties transitioned from volume/page to document number systems at different times. Many counties use both. Volume references may be abbreviated as 'Vol.', 'V.', or 'Bk.'",
        "examples": ["Warranty deed recorded in Volume 831, Page 393 of the Official Records of Reeves County, Texas."]
    },
    {
        "term": "document_number",
        "category": "RECORDING_SYSTEM",
        "aliases": ["doc number", "instrument number", "filing number", "reception number", "clerk's file number"],
        "abbreviations": ["Doc#", "Doc. No.", "Inst. No."],
        "definition": "A unique sequential number assigned to each instrument when it is filed for recording. This is the modern method of identifying recorded instruments, supplementing or replacing the volume/page system.",
        "context": "Document numbers provide a unique identifier for each instrument. Modern county systems use document numbers as the primary reference.",
        "related_terms": ["volume_page", "recording_date", "official_records"],
        "texas_notes": "In Reeves County, document numbers typically follow the format YY-NNNNN (e.g., 18-17007). Some counties use longer or different formats.",
        "examples": ["Mineral Deed filed as Document No. 18-17007 in the Official Records of Reeves County, Texas."]
    },
    {
        "term": "recording_date",
        "category": "RECORDING_SYSTEM",
        "aliases": ["filed date", "date of recording", "file date", "date filed", "date of filing"],
        "abbreviations": [],
        "definition": "The date an instrument was actually filed with and recorded by the county clerk. This date controls priority under the recording acts. Not to be confused with the execution date (when the instrument was signed) or the acknowledgment date (when it was notarized).",
        "context": "Recording date is the critical date for priority analysis. Under race-notice recording, the first to record gains priority.",
        "related_terms": ["execution_date", "acknowledgment_date", "volume_page", "document_number"],
        "texas_notes": "In Texas, the recording date is stamped on the instrument by the county clerk's office. The date and time of filing determine priority.",
        "examples": ["The deed was executed on March 1, 2020, but not recorded until June 15, 2020."]
    },
    {
        "term": "execution_date",
        "category": "RECORDING_SYSTEM",
        "aliases": ["date of execution", "signing date", "date signed", "deed date"],
        "abbreviations": [],
        "definition": "The date the instrument was signed by the grantor(s). This is the date the grantor expressed intent to convey. It may differ significantly from the recording date.",
        "context": "Execution date establishes when the grantor intended to convey. Large gaps between execution and recording dates should be investigated.",
        "related_terms": ["recording_date", "acknowledgment_date", "delivery_date"],
        "texas_notes": "In Texas, the execution date does not control priority. Only the recording date matters for constructive notice.",
        "examples": ["Executed January 15, 1998; Acknowledged January 15, 1998; Recorded March 10, 1998."]
    },
    {
        "term": "acknowledgment_date",
        "category": "RECORDING_SYSTEM",
        "aliases": ["date of acknowledgment", "notary date", "notarization date"],
        "abbreviations": [],
        "definition": "The date the grantor appeared before a notary public or other authorized officer to acknowledge execution of the instrument. Must occur on or after the execution date and before the recording date.",
        "context": "Acknowledgment is required for recording in Texas. The acknowledgment date should logically fall between execution and recording dates.",
        "related_terms": ["execution_date", "recording_date", "notary_public"],
        "texas_notes": "Texas requires a notary seal and venue (state and county) on the acknowledgment certificate.",
        "examples": ["Acknowledged before Jane Doe, Notary Public, State of Texas, on January 15, 1998."]
    },
    {
        "term": "official_records",
        "category": "RECORDING_SYSTEM",
        "aliases": ["deed records", "official public records", "county records", "real property records", "OR"],
        "abbreviations": ["OR", "OPR", "DR"],
        "definition": "The official public records maintained by the county clerk where instruments affecting real property are recorded. Includes deeds, mortgages, liens, leases, and other recordable instruments.",
        "context": "The official records are the source of constructive notice. All chain of title instruments should be found in the official records.",
        "related_terms": ["grantor_grantee_index", "volume_page", "document_number", "county_clerk"],
        "texas_notes": "In Texas, the county clerk is the custodian of the official records. Records are organized chronologically within volumes.",
        "examples": ["Recorded in the Official Records of Reeves County, Texas, Volume 831, Page 393."]
    },

    # ==================== CONVEYANCE AND INTEREST TERMS ====================
    {
        "term": "grantor",
        "category": "CONVEYANCE",
        "aliases": ["seller", "transferor", "conveyor", "assignor", "lessor"],
        "abbreviations": ["G/R", "GR"],
        "definition": "The party who conveys or transfers an interest in real property. In a deed, the grantor is the seller. In a lease, the grantor is the lessor. In an assignment, the grantor is the assignor.",
        "context": "The grantor appears in the grantor index. The chain examiner searches the grantor index to find all conveyances BY an owner.",
        "related_terms": ["grantee", "grantor_grantee_index"],
        "texas_notes": "In Texas community property, both spouses must be grantors for community property conveyances.",
        "examples": ["John Smith, Grantor, hereby grants and conveys to Mary Jones, Grantee..."]
    },
    {
        "term": "grantee",
        "category": "CONVEYANCE",
        "aliases": ["buyer", "transferee", "purchaser", "assignee", "lessee"],
        "abbreviations": ["G/E", "GE"],
        "definition": "The party who receives an interest in real property. In a deed, the grantee is the buyer. In a lease, the grantee is the lessee. In an assignment, the grantee is the assignee.",
        "context": "The grantee appears in the grantee index. The chain examiner searches the grantee index to find how a party acquired title.",
        "related_terms": ["grantor", "grantor_grantee_index"],
        "texas_notes": "The grantee of a quitclaim deed may not qualify as a bona fide purchaser in Texas.",
        "examples": ["...to Mary Jones, Grantee, and to her heirs and assigns forever."]
    },
    {
        "term": "mineral_interest",
        "category": "INTEREST_TYPE",
        "aliases": ["mineral estate", "mineral rights", "mineral ownership", "subsurface rights"],
        "abbreviations": ["MI"],
        "definition": "Ownership of the minerals beneath the surface of the land, including the right to explore for, develop, and produce oil, gas, and other minerals. In Texas, the mineral estate is a separate, dominant estate that can be severed from the surface.",
        "context": "Mineral interest tracking is the core of oil and gas title examination. Mineral interests are expressed as fractions of the whole.",
        "related_terms": ["royalty_interest", "working_interest", "executive_right", "surface_estate"],
        "texas_notes": "In Texas, the mineral estate is dominant over the surface estate. The mineral owner has an implied right to use as much of the surface as reasonably necessary for mineral development.",
        "examples": ["Smith owns an undivided 1/4 mineral interest in Section 270, or 160 net mineral acres."],
        "is_interest_type": True
    },
    {
        "term": "royalty_interest",
        "category": "INTEREST_TYPE",
        "aliases": ["royalty", "landowner royalty", "royalty estate", "royalty share"],
        "abbreviations": ["RI"],
        "definition": "The right to receive a share of production (or its value) from a mineral lease, free of the costs of production. The standard royalty in Texas is 1/8 (12.5%) but modern leases often provide 1/4 (25%) or higher.",
        "context": "Royalty interests are paid from production revenue. They are a burden on the working interest. Royalty interests can be severed and conveyed separately from the mineral estate.",
        "related_terms": ["mineral_interest", "overriding_royalty", "working_interest"],
        "texas_notes": "Texas recognizes royalty as a severable interest. A royalty deed conveys only the right to receive royalty, not the right to lease (executive right) or bonus/rentals.",
        "examples": ["Jones owns a 1/16 royalty interest in Section 270 under the 2019 lease providing 1/4 royalty."],
        "is_interest_type": True
    },
    {
        "term": "overriding_royalty",
        "category": "INTEREST_TYPE",
        "aliases": ["ORRI", "override", "overriding royalty interest"],
        "abbreviations": ["ORRI"],
        "definition": "A royalty interest carved out of the working interest in a mineral lease. The ORRI is a burden on the lessee's working interest, not on the mineral estate itself. It expires when the underlying lease terminates.",
        "context": "ORRIs are commonly created when a lessee assigns a lease and retains a royalty interest. They must be tracked separately from mineral royalties.",
        "related_terms": ["royalty_interest", "working_interest", "assignment"],
        "texas_notes": "ORRIs are common in Permian Basin farmout transactions. They expire with the lease and do not burden subsequent leases.",
        "examples": ["Smith retained a 3% overriding royalty interest in the assignment of the 2019 OGL."],
        "is_interest_type": True
    },
    {
        "term": "working_interest",
        "category": "INTEREST_TYPE",
        "aliases": ["operating interest", "WI", "lessee's interest", "leasehold interest"],
        "abbreviations": ["WI"],
        "definition": "The operating interest in a mineral lease that bears the cost of exploration, development, and production. The working interest owner pays all costs and receives production revenue net of royalty burdens.",
        "context": "Working interest is the operator's interest. It is burdened by royalty, overriding royalty, and other non-operating interests.",
        "related_terms": ["mineral_interest", "royalty_interest", "overriding_royalty", "net_revenue_interest"],
        "texas_notes": "Working interest in Texas is created by the oil and gas lease. The lessee receives the working interest, subject to the lessor's royalty.",
        "examples": ["The operator holds a 75% working interest (100% WI less 25% royalty burden = 75% NRI)."],
        "is_interest_type": True
    },
    {
        "term": "net_mineral_acres",
        "category": "INTEREST_TYPE",
        "aliases": ["NMA", "net minerals", "mineral acres"],
        "abbreviations": ["NMA"],
        "definition": "The product of gross acres multiplied by the mineral interest fraction. Represents the actual acreage equivalent of the fractional mineral interest. Used as the standard unit for mineral ownership quantification.",
        "context": "NMA is the standard measure of mineral ownership. Division orders, lease negotiations, and title opinions all use NMA.",
        "related_terms": ["mineral_interest", "net_revenue_interest", "gross_acres"],
        "texas_notes": "In the Permian Basin, a standard section is 640 gross acres. If you own 1/4 minerals, that is 160 NMA.",
        "examples": ["Smith owns 1/16 of 640 acres = 40 net mineral acres in Section 270."],
        "is_interest_type": True
    },
    {
        "term": "net_revenue_interest",
        "category": "INTEREST_TYPE",
        "aliases": ["NRI", "net revenue", "revenue interest"],
        "abbreviations": ["NRI"],
        "definition": "The percentage of production revenue actually received by an interest owner after deducting all royalty and overriding royalty burdens. NRI = Working Interest x (1 - total royalty burdens).",
        "context": "NRI determines the actual revenue share. It is used in division orders and revenue distribution.",
        "related_terms": ["working_interest", "royalty_interest", "net_mineral_acres"],
        "texas_notes": "For a typical Texas lease with 1/4 royalty and no ORRIs: NRI = 100% WI x (1 - 0.25) = 75% NRI.",
        "examples": ["The 87.5% WI with a 1/8 royalty burden has an NRI of 87.5% x (1 - 0.125) = 76.5625%."],
        "is_interest_type": True
    },
    {
        "term": "executive_right",
        "category": "INTEREST_TYPE",
        "aliases": ["executive rights", "leasing right", "right to lease"],
        "abbreviations": [],
        "definition": "The power to execute oil and gas leases on the mineral estate. In Texas, the executive right is severable from the mineral interest. The holder of the executive right has a fiduciary duty to non-executive mineral owners.",
        "context": "Executive right determines who can sign leases. Non-executive mineral owners receive royalty but cannot control leasing.",
        "related_terms": ["mineral_interest", "royalty_interest", "fiduciary_duty"],
        "texas_notes": "Texas uniquely allows severance of the executive right from the mineral estate. This is common in family estate planning.",
        "examples": ["The trust holds the executive right while the beneficiaries hold the non-executive mineral interests."],
        "is_interest_type": True
    },
    {
        "term": "surface_estate",
        "category": "INTEREST_TYPE",
        "aliases": ["surface rights", "surface interest", "surface ownership"],
        "abbreviations": [],
        "definition": "Ownership of the surface of the land, as distinct from the mineral estate below. After mineral severance, the surface owner has no rights to the minerals but retains all surface use rights subject to the mineral owner's dominant estate.",
        "context": "Surface estate tracking is separate from mineral chain analysis. After severance, the surface and mineral chains diverge.",
        "related_terms": ["mineral_interest", "accommodation_doctrine", "dominant_estate"],
        "texas_notes": "Texas mineral estate is dominant. The accommodation doctrine (Getty Oil v. Jones) limits surface damage but the mineral owner has broad implied rights.",
        "examples": ["The 1950 deed conveyed the surface only, having previously severed the minerals in 1935."],
        "is_interest_type": True
    },

    # ==================== ABSTRACT/SURVEY TERMS ====================
    {
        "term": "abstract_number",
        "category": "LAND_DESCRIPTION",
        "aliases": ["abstract", "abstract no.", "abst.", "abs."],
        "abbreviations": ["Abst.", "Abs.", "A-"],
        "definition": "A unique sequential number assigned by the Texas General Land Office to each original survey in a county. The abstract number is the primary parcel identifier in the Texas abstract/survey system and links to all GLO records for that survey.",
        "context": "Abstract numbers are the primary means of identifying tracts in the Texas system. All chain searches should reference the abstract number.",
        "related_terms": ["survey_number", "block_number", "section_number", "general_land_office"],
        "texas_notes": "Abstract numbers are unique within each county. The same survey may have different abstract numbers in different counties if it crosses county lines.",
        "examples": ["Abstract 234, Section 270, Block 13, H&GN RR Co. Survey, Reeves County, Texas."]
    },
    {
        "term": "survey_number",
        "category": "LAND_DESCRIPTION",
        "aliases": ["survey", "section", "section number", "surv."],
        "abbreviations": ["Surv.", "Sec.", "S."],
        "definition": "The number assigned to a specific survey within a block. In the Permian Basin, surveys are typically 640 acres (one section or one square mile). The survey number combined with the block identifies the specific parcel.",
        "context": "Survey/section numbers are used with block numbers to identify tracts. In the Permian Basin, the typical description is Section X, Block Y.",
        "related_terms": ["abstract_number", "block_number", "section"],
        "texas_notes": "In West Texas, 'section' and 'survey' are used interchangeably. A standard section is 640 acres.",
        "examples": ["Section 270, Block 13, H&GN RR Co. Survey, Reeves County, Texas."]
    },
    {
        "term": "block_number",
        "category": "LAND_DESCRIPTION",
        "aliases": ["block", "blk.", "survey block"],
        "abbreviations": ["Blk.", "Bk."],
        "definition": "A grouping of adjacent surveys, typically associated with a railroad grant or surveying company. Blocks are identified by numbers, letters, or combinations and are part of the standard legal description in the Texas abstract/survey system.",
        "context": "Block numbers group surveys together and are essential for legal description identification. Common Permian Basin blocks include C-22, 13, 34, etc.",
        "related_terms": ["abstract_number", "survey_number", "railroad_grant"],
        "texas_notes": "Permian Basin block designations often reference the original railroad company survey. Block 13 = H&GN RR Co., Block C-22 = PSL Survey.",
        "examples": ["Block 13, H&GN RR Co. Survey (common designation for Reeves County surveys)."]
    },
    {
        "term": "legal_description",
        "category": "LAND_DESCRIPTION",
        "aliases": ["property description", "land description", "description of premises", "legal desc."],
        "abbreviations": ["Leg. Desc."],
        "definition": "The formal description of real property sufficient to identify it uniquely. In Texas, this typically includes the abstract number, survey/section number, block number, original grantee, and county. For subdivisions, lot/block/subdivision name is used.",
        "context": "Legal descriptions must be consistent throughout the chain. Variations may indicate different parcels or scrivener's errors.",
        "related_terms": ["abstract_number", "metes_and_bounds", "survey_number", "block_number"],
        "texas_notes": "Standard Permian Basin format: 'Abstract ____, Section ____, Block ____, ______ Survey, ______ County, Texas, containing ____ acres, more or less.'",
        "examples": ["Abstract 234, Section 270, Block 13, H&GN RR Co. Survey, Reeves County, Texas, containing 640 acres, more or less."]
    },
    {
        "term": "metes_and_bounds",
        "category": "LAND_DESCRIPTION",
        "aliases": ["metes & bounds", "boundary description", "survey description", "field notes"],
        "abbreviations": ["M&B"],
        "definition": "A method of describing land by specifying the boundary lines using compass directions, distances, and reference points (monuments). Metes and bounds descriptions start at a point of beginning and trace the boundary back to the starting point.",
        "context": "Metes and bounds descriptions are found in original survey field notes and some deeds. They are more precise but harder to verify than abstract/survey descriptions.",
        "related_terms": ["legal_description", "field_notes", "survey_number"],
        "texas_notes": "Original Texas surveys were described by metes and bounds in the field notes. Modern conveyances typically use the abstract/survey reference.",
        "examples": ["Beginning at the NE corner of Section 270; thence S 0 degrees W 5280 feet to the SE corner..."]
    },

    # ==================== INSTRUMENT TYPES ====================
    {
        "term": "warranty_deed",
        "category": "INSTRUMENT_TYPE",
        "aliases": ["general warranty deed", "GWD", "deed with full warranties"],
        "abbreviations": ["WD", "GWD"],
        "definition": "A deed in which the grantor warrants and defends the title against all claims, not just those arising from the grantor's own actions. Contains all six covenants of title: seisin, right to convey, against encumbrances, quiet enjoyment, warranty, and further assurances.",
        "context": "Warranty deeds are the strongest form of conveyance and the preferred instrument in chain of title. They trigger after-acquired title and estoppel by deed.",
        "related_terms": ["special_warranty_deed", "quitclaim_deed", "covenant_of_warranty"],
        "texas_notes": "In Texas, the statutory form deed using 'grant, sell, and convey' with 'general warranty' language is a general warranty deed per Property Code Section 5.022.",
        "examples": ["Smith and wife Jane Smith hereby grant, sell, and convey unto Jones with general warranty..."],
        "is_instrument_type": True
    },
    {
        "term": "mineral_deed",
        "category": "INSTRUMENT_TYPE",
        "aliases": ["mineral conveyance", "mineral interest deed", "deed of mineral interest"],
        "abbreviations": ["MD"],
        "definition": "A deed that conveys mineral interests (subsurface rights) separately from the surface estate. May convey all or a fractional interest in minerals. Creates the mineral severance that separates the mineral and surface chains.",
        "context": "Mineral deeds are the primary mechanism for severing the mineral estate from the surface. Every mineral deed creates a branch point in the chain.",
        "related_terms": ["mineral_interest", "royalty_deed", "mineral_reservation"],
        "texas_notes": "In Texas, a mineral deed is a conveyance of real property. The mineral estate is a separate fee simple estate.",
        "examples": ["Smith conveys an undivided 1/2 mineral interest in Section 270 to Jones."],
        "is_instrument_type": True
    },
    {
        "term": "royalty_deed",
        "category": "INSTRUMENT_TYPE",
        "aliases": ["royalty conveyance", "royalty interest deed", "deed of royalty interest"],
        "abbreviations": ["RD"],
        "definition": "A deed that conveys a royalty interest (right to share in production) without conveying the underlying mineral estate. The grantee receives royalty payments but has no right to lease, develop, or produce minerals.",
        "context": "Royalty deeds create a separate royalty interest that must be tracked in the chain. The royalty owner has no executive right.",
        "related_terms": ["royalty_interest", "mineral_deed", "mineral_interest"],
        "texas_notes": "In Texas, the distinction between a mineral deed and royalty deed has been extensively litigated. The key issue is whether the 'minerals' or 'royalty' language creates a mineral or royalty estate.",
        "examples": ["Smith conveys a 1/16 royalty interest in all oil, gas, and other minerals produced from Section 270."],
        "is_instrument_type": True
    },
    {
        "term": "oil_gas_lease",
        "category": "INSTRUMENT_TYPE",
        "aliases": ["OGL", "mineral lease", "petroleum lease", "O&G lease"],
        "abbreviations": ["OGL", "O&G Lease"],
        "definition": "A lease granting the right to explore for, develop, and produce oil, gas, and other minerals from a tract of land. The lessor retains a royalty interest and the lessee receives the working interest. Modern Texas leases typically have 3-5 year primary terms.",
        "context": "Oil and gas leases are the primary instrument creating the operating interest. They do not transfer ownership but create a leasehold estate.",
        "related_terms": ["working_interest", "royalty_interest", "primary_term", "habendum_clause"],
        "texas_notes": "Texas OGLs create a determinable fee (estate that ends when production ceases). The 'held by production' clause extends the lease beyond the primary term.",
        "examples": ["Paid-Up Oil and Gas Lease from Smith to Energy Co., covering Section 270, 3-year primary term, 1/4 royalty."],
        "is_instrument_type": True
    },
    {
        "term": "assignment",
        "category": "INSTRUMENT_TYPE",
        "aliases": ["assignment of lease", "assignment of interest", "ASN"],
        "abbreviations": ["ASN", "ASGN"],
        "definition": "A transfer of an interest in an existing lease or other agreement from one party to another. The assignor transfers their interest (or a portion of it) to the assignee. Assignments may be of the entire working interest or a partial interest.",
        "context": "Assignments transfer leasehold interests and must be tracked in the chain. Each assignment creates a new link in the leasehold chain.",
        "related_terms": ["oil_gas_lease", "working_interest", "overriding_royalty"],
        "texas_notes": "In Texas, assignments of OGLs are recorded in the deed records and must be tracked in the chain examination.",
        "examples": ["Assignment of Oil and Gas Lease from Energy Co. to Production Co., retaining 3% ORRI."],
        "is_instrument_type": True
    },
    {
        "term": "deed_of_trust",
        "category": "INSTRUMENT_TYPE",
        "aliases": ["DOT", "trust deed", "mortgage equivalent"],
        "abbreviations": ["DOT", "D/T"],
        "definition": "A security instrument used in Texas instead of a mortgage. The borrower (trustor) conveys title to a trustee who holds it as security for a loan from the lender (beneficiary). If the loan defaults, the trustee can sell the property at foreclosure.",
        "context": "Deeds of trust are encumbrances that must be tracked in the chain. They create a lien but not a break in the ownership chain.",
        "related_terms": ["release_of_lien", "foreclosure", "encumbrance"],
        "texas_notes": "Texas uses deeds of trust rather than mortgages. Non-judicial foreclosure is available under the Texas Property Code.",
        "examples": ["Deed of Trust from Smith to First Bank, securing $500,000 note, encumbering Section 270."],
        "is_instrument_type": True
    },
    {
        "term": "affidavit_of_heirship",
        "category": "INSTRUMENT_TYPE",
        "aliases": ["heirship affidavit", "affidavit of heirs", "heirship"],
        "abbreviations": ["AOH"],
        "definition": "An affidavit filed in the deed records to establish the heirs of a deceased property owner when no probate was conducted. After being of record for 5 years, it becomes prima facie evidence of the facts stated. It bridges heirship gaps in the chain.",
        "context": "Affidavits of heirship are the most common curative instrument for death gaps in the chain. They establish who the heirs are and their fractional interests.",
        "related_terms": ["heirship_gap", "curative_instrument", "probate"],
        "texas_notes": "Under Texas Estates Code Section 203.001, an affidavit of heirship filed for 5+ years is prima facie evidence of heirship. It must be made by a disinterested party who knew the decedent.",
        "examples": ["Affidavit of Heirship for John Smith, deceased, establishing his four children as equal heirs."],
        "is_instrument_type": True
    },

    # ==================== CURATIVE AND TITLE EXAMINATION TERMS ====================
    {
        "term": "curative_instrument",
        "category": "CURATIVE",
        "aliases": ["curative", "curative document", "corrective instrument", "healing instrument"],
        "abbreviations": [],
        "definition": "Any instrument filed to correct, clarify, or perfect a defect in the chain of title. Includes correction deeds, affidavits of identity, affidavits of heirship, ratifications, quitclaim deeds, and stipulations of interest.",
        "context": "Curative instruments bridge gaps, fix errors, and strengthen the chain. They are prescribed by the examining attorney in the title opinion curative requirements.",
        "related_terms": ["gap_in_chain", "break_in_chain", "title_opinion", "correction_deed"],
        "texas_notes": "In Texas O&G title, curative is a major component of the examination process. Standard curatives include: AOH, correction deed, QCD, ratification, and stipulation of interest.",
        "examples": ["The title opinion requires the following curative: (1) Affidavit of Heirship for Mary Smith, (2) Correction Deed to fix legal description."]
    },
    {
        "term": "title_opinion",
        "category": "CURATIVE",
        "aliases": ["opinion of title", "title letter", "attorney's title opinion"],
        "abbreviations": ["T/O"],
        "definition": "A formal written opinion by an attorney examining the chain of title, identifying defects, and listing curative requirements. The opinion expresses the attorney's professional judgment on whether title is marketable and what steps are needed to cure any defects.",
        "context": "The title opinion is the final work product of a title examination. It relies on the run sheet and chain of title constructed by the landman.",
        "related_terms": ["run_sheet", "chain_of_title", "curative_instrument", "marketable_title"],
        "texas_notes": "Texas title opinions follow AAPL standards and typically include: overview, chain analysis, defects found, curative requirements, and ownership schedule.",
        "examples": ["Based on my examination of the chain of title, it is my opinion that title is vested in Jones, subject to the following requirements..."]
    },
    {
        "term": "stipulation_of_interest",
        "category": "CURATIVE",
        "aliases": ["stip", "SOI", "interest stipulation", "stipulation"],
        "abbreviations": ["SOI", "Stip."],
        "definition": "An agreement among parties establishing and confirming their respective ownership interests. Commonly used to resolve fractional interest disputes, Duhig issues, and overconveyance problems. When recorded, it creates a clean link in the chain.",
        "context": "Stipulations resolve disputed ownership without litigation. They require agreement of all affected parties and are recorded in the deed records.",
        "related_terms": ["curative_instrument", "fractional_interest", "duhig_rule"],
        "texas_notes": "Stipulations of interest are very common in Permian Basin mineral title to resolve fractional discrepancies caused by Duhig problems and overconveyances.",
        "examples": ["Stipulation of Interest among Smith heirs and Jones, establishing Smith heirs own 1/4 MI and Jones owns 3/4 MI."],
        "is_instrument_type": True
    },
    {
        "term": "quiet_title_action",
        "category": "CURATIVE",
        "aliases": ["quiet title", "trespass to try title", "declaratory judgment"],
        "abbreviations": ["QTA"],
        "definition": "A lawsuit filed to establish ownership of real property and eliminate competing claims. In Texas, the primary form is 'trespass to try title' under Texas Property Code Chapter 22. A successful quiet title judgment creates a definitive chain link.",
        "context": "Quiet title is the last resort for resolving chain disputes. It is used when voluntary curative is not possible.",
        "related_terms": ["curative_instrument", "break_in_chain", "adverse_possession"],
        "texas_notes": "In Texas, trespass to try title is the primary action for adjudicating competing title claims. Tex. Prop. Code Chapter 22.",
        "examples": ["Plaintiff filed trespass to try title to establish ownership against all unknown heirs of Smith."]
    },
    {
        "term": "constructive_notice",
        "category": "LEGAL_CONCEPT",
        "aliases": ["record notice", "notice from recording", "imputed notice"],
        "abbreviations": [],
        "definition": "The legal presumption that a person has knowledge of facts that could be discovered by examining the public records. Recording an instrument provides constructive notice to all subsequent purchasers. A person is charged with knowledge of all instruments properly recorded in the chain of title.",
        "context": "Constructive notice is the foundation of the recording system. It makes chain of title examination essential and meaningful.",
        "related_terms": ["actual_notice", "recording_date", "bona_fide_purchaser", "grantor_grantee_index"],
        "texas_notes": "In Texas, recording in the official deed records provides constructive notice per Property Code Section 13.002.",
        "examples": ["The 1965 mineral deed provides constructive notice to all subsequent purchasers because it was properly recorded."]
    },
    {
        "term": "bona_fide_purchaser",
        "category": "LEGAL_CONCEPT",
        "aliases": ["BFP", "good faith purchaser", "innocent purchaser", "purchaser for value"],
        "abbreviations": ["BFP"],
        "definition": "A person who purchases real property for valuable consideration, in good faith, and without notice (actual or constructive) of any defects or prior claims. BFP status is the key defense against prior unrecorded interests under the recording acts.",
        "context": "BFP analysis is essential for determining priority between competing claims in the chain. Each buyer should be assessed for BFP status.",
        "related_terms": ["constructive_notice", "actual_notice", "recording_date", "shelter_rule"],
        "texas_notes": "In Texas, grantees under quitclaim deeds and donees/heirs are NOT BFPs because they lack valuable consideration or are on notice of title defects.",
        "examples": ["Jones qualifies as a BFP because she paid full value, had no notice of Smith's unrecorded deed, and recorded promptly."]
    },
]


# ---------------------------------------------------------------------------
# Semantic dictionary manager
# ---------------------------------------------------------------------------

class ChainOfTitleSemanticDictionary:
    """Manages the chain of title semantic dictionary.

    Provides lookup by term, alias, abbreviation, and category.
    Supports fuzzy matching and normalization for chain construction.
    """

    def __init__(self) -> None:
        self._entries: Dict[str, SemanticEntry] = {}
        self._alias_index: Dict[str, str] = {}
        self._abbreviation_index: Dict[str, str] = {}
        self._by_category: Dict[str, List[str]] = {}
        self._instrument_types: Set[str] = set()
        self._interest_types: Set[str] = set()
        self._stats: SemanticDictionaryStats = SemanticDictionaryStats()
        self._loaded: bool = False
        logger.info("ChainOfTitleSemanticDictionary initialized")

    def load(self) -> SemanticDictionaryStats:
        """Load all semantic entries into the dictionary."""
        import time
        start = time.perf_counter()

        self._entries.clear()
        self._alias_index.clear()
        self._abbreviation_index.clear()
        self._by_category.clear()
        self._instrument_types.clear()
        self._interest_types.clear()

        total_aliases = 0
        total_abbrevs = 0

        for raw in CHAIN_OF_TITLE_SEMANTICS:
            entry = SemanticEntry(**raw)
            self._entries[entry.term] = entry

            for alias in entry.aliases:
                normalized_alias = self._normalize_term(alias)
                self._alias_index[normalized_alias] = entry.term
                total_aliases += 1

            for abbr in entry.abbreviations:
                normalized_abbr = abbr.upper().strip()
                self._abbreviation_index[normalized_abbr] = entry.term
                total_abbrevs += 1

            cat = entry.category
            if cat not in self._by_category:
                self._by_category[cat] = []
            self._by_category[cat].append(entry.term)

            if entry.is_instrument_type:
                self._instrument_types.add(entry.term)
            if entry.is_interest_type:
                self._interest_types.add(entry.term)

        elapsed_ms = (time.perf_counter() - start) * 1000
        category_counts = {cat: len(terms) for cat, terms in self._by_category.items()}

        self._stats = SemanticDictionaryStats(
            total_entries=len(self._entries),
            categories=category_counts,
            total_aliases=total_aliases,
            total_abbreviations=total_abbrevs,
            last_loaded=datetime.now(timezone.utc).isoformat(),
            dictionary_hash=self._compute_hash(),
        )
        self._loaded = True

        logger.info(
            f"Loaded {self._stats.total_entries} semantic entries "
            f"({total_aliases} aliases, {total_abbrevs} abbreviations) "
            f"in {elapsed_ms:.1f}ms"
        )
        return self._stats

    def lookup(self, query: str) -> Optional[SemanticEntry]:
        """Look up a term by exact match, alias, or abbreviation."""
        self._ensure_loaded()
        normalized = self._normalize_term(query)

        if normalized in self._entries:
            return self._entries[normalized]

        if normalized in self._alias_index:
            return self._entries.get(self._alias_index[normalized])

        upper = query.upper().strip()
        if upper in self._abbreviation_index:
            return self._entries.get(self._abbreviation_index[upper])

        return None

    def search(self, query: str, max_results: int = 20) -> List[SemanticEntry]:
        """Search across all semantic entries by relevance."""
        self._ensure_loaded()
        query_lower = query.lower().strip()
        scored: List[Tuple[float, str]] = []

        for term, entry in self._entries.items():
            score = 0.0
            if query_lower in term:
                score += 10.0
            for alias in entry.aliases:
                if query_lower in alias.lower():
                    score += 7.0
            for abbr in entry.abbreviations:
                if query_lower == abbr.lower():
                    score += 8.0
            if query_lower in entry.definition.lower():
                score += 3.0
            if query_lower in entry.context.lower():
                score += 2.0
            if query_lower in entry.texas_notes.lower():
                score += 1.0

            if score > 0:
                scored.append((score, term))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [self._entries[t] for _, t in scored[:max_results]]

    def get_by_category(self, category: str) -> List[SemanticEntry]:
        """Retrieve all entries in a given category."""
        self._ensure_loaded()
        terms = self._by_category.get(category, [])
        return [self._entries[t] for t in terms if t in self._entries]

    def get_instrument_types(self) -> List[SemanticEntry]:
        """Retrieve all instrument type entries."""
        self._ensure_loaded()
        return [self._entries[t] for t in self._instrument_types if t in self._entries]

    def get_interest_types(self) -> List[SemanticEntry]:
        """Retrieve all interest type entries."""
        self._ensure_loaded()
        return [self._entries[t] for t in self._interest_types if t in self._entries]

    def list_categories(self) -> Dict[str, int]:
        """List all categories with entry counts."""
        self._ensure_loaded()
        return {cat: len(terms) for cat, terms in self._by_category.items()}

    def list_terms(self) -> List[str]:
        """List all canonical terms."""
        self._ensure_loaded()
        return list(self._entries.keys())

    def get_definition(self, term: str) -> Optional[str]:
        """Quick lookup for just the definition of a term."""
        entry = self.lookup(term)
        return entry.definition if entry else None

    def normalize_instrument_type(self, raw_type: str) -> Optional[str]:
        """Normalize a raw instrument type string to canonical form."""
        self._ensure_loaded()
        entry = self.lookup(raw_type)
        if entry and entry.is_instrument_type:
            return entry.term

        normalized = self._normalize_term(raw_type)
        type_mapping: Dict[str, str] = {
            "wd": "warranty_deed",
            "gwd": "warranty_deed",
            "swd": "special_warranty_deed",
            "qcd": "quitclaim_deed",
            "md": "mineral_deed",
            "rd": "royalty_deed",
            "ogl": "oil_gas_lease",
            "asn": "assignment",
            "asgn": "assignment",
            "dot": "deed_of_trust",
            "aoh": "affidavit_of_heirship",
            "soi": "stipulation_of_interest",
            "deed": "warranty_deed",
            "mineral deed": "mineral_deed",
            "royalty deed": "royalty_deed",
            "oil and gas lease": "oil_gas_lease",
            "oil & gas lease": "oil_gas_lease",
            "deed of trust": "deed_of_trust",
            "affidavit of heirship": "affidavit_of_heirship",
            "heirship affidavit": "affidavit_of_heirship",
            "quit claim deed": "quitclaim_deed",
            "quit claim": "quitclaim_deed",
            "quitclaim": "quitclaim_deed",
            "warranty": "warranty_deed",
            "general warranty": "warranty_deed",
            "special warranty": "special_warranty_deed",
            "patent": "sovereign_patent",
            "land patent": "sovereign_patent",
            "correction deed": "correction_deed",
            "ratification": "ratification",
            "stipulation": "stipulation_of_interest",
        }

        return type_mapping.get(normalized) or type_mapping.get(raw_type.upper().strip())

    def normalize_interest_type(self, raw_type: str) -> Optional[str]:
        """Normalize a raw interest type string to canonical form."""
        self._ensure_loaded()
        entry = self.lookup(raw_type)
        if entry and entry.is_interest_type:
            return entry.term

        normalized = self._normalize_term(raw_type)
        interest_mapping: Dict[str, str] = {
            "mi": "mineral_interest",
            "ri": "royalty_interest",
            "orri": "overriding_royalty",
            "wi": "working_interest",
            "nma": "net_mineral_acres",
            "nri": "net_revenue_interest",
            "minerals": "mineral_interest",
            "mineral": "mineral_interest",
            "royalty": "royalty_interest",
            "overriding royalty": "overriding_royalty",
            "override": "overriding_royalty",
            "working interest": "working_interest",
            "operating interest": "working_interest",
            "surface": "surface_estate",
            "surface estate": "surface_estate",
            "executive right": "executive_right",
            "executive": "executive_right",
            "net mineral acres": "net_mineral_acres",
            "net revenue interest": "net_revenue_interest",
        }

        return interest_mapping.get(normalized) or interest_mapping.get(raw_type.upper().strip())

    def get_stats(self) -> SemanticDictionaryStats:
        """Return dictionary statistics."""
        return self._stats

    def _normalize_term(self, term: str) -> str:
        """Normalize a term for lookup."""
        normalized = term.lower().strip()
        normalized = re.sub(r"[_\-/]", " ", normalized)
        normalized = re.sub(r"\s+", " ", normalized)
        normalized = re.sub(r"[^\w\s]", "", normalized)
        normalized = normalized.strip()
        return normalized

    def _ensure_loaded(self) -> None:
        """Load dictionary if not already loaded."""
        if not self._loaded:
            self.load()

    def _compute_hash(self) -> str:
        """Deterministic hash of all dictionary content."""
        hasher = hashlib.sha256()
        for term in sorted(self._entries.keys()):
            entry = self._entries[term]
            hasher.update(entry.model_dump_json().encode("utf-8"))
        return hasher.hexdigest()
