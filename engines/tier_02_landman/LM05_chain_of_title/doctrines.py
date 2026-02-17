"""
LM05 Chain of Title Builder - Doctrine Cache
==============================================
ECHO OMEGA PRIME - Landman Intelligence Division

Comprehensive chain of title doctrines covering:
- Texas recording statutes (race-notice recording act)
- Constructive and actual notice frameworks
- Chain of title search methodology (grantor-grantee, tract index)
- Root of title selection and marketable title standards
- After-acquired title doctrine and estoppel by deed
- Wild deeds and stray instruments
- Mother Hubbard clauses
- Sovereign patent chain (Spanish, Mexican, Republic of Texas, State)
- Railroad land grants and school land (PSF)
- Abstract/survey system
- Gap analysis methodology and curative doctrines

Each doctrine block contains:
    topic: Canonical identifier
    category: Classification (RECORDING_ACT, CHAIN_SEARCH, SOVEREIGN, etc.)
    title: Human-readable title
    summary: Brief description
    legal_basis: Statutory or case law authority
    elements: Key elements or requirements
    texas_application: Texas-specific application notes
    chain_impact: How this doctrine affects chain construction
    related_topics: Cross-references

Authority: Bobby Don McWilliams II (11.0 SUPREME SOVEREIGN)
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class DoctrineBlock(BaseModel):
    """A single chain-of-title doctrine entry."""
    topic: str = Field(..., description="Canonical doctrine identifier")
    category: str = Field(..., description="Doctrine category")
    title: str = Field(..., description="Human-readable title")
    summary: str = Field(..., description="Brief description of the doctrine")
    legal_basis: List[str] = Field(default_factory=list, description="Statutory or case law authority")
    elements: List[str] = Field(default_factory=list, description="Key elements or requirements")
    texas_application: str = Field(default="", description="Texas-specific notes")
    chain_impact: str = Field(default="", description="Impact on chain construction")
    related_topics: List[str] = Field(default_factory=list, description="Cross-references")
    exceptions: List[str] = Field(default_factory=list, description="Known exceptions")
    curative_actions: List[str] = Field(default_factory=list, description="How to cure defects under this doctrine")
    risk_level: str = Field(default="MEDIUM", description="Risk if doctrine violated: LOW, MEDIUM, HIGH, CRITICAL")


class DoctrineCacheStats(BaseModel):
    """Statistics about the doctrine cache."""
    total_doctrines: int = 0
    categories: Dict[str, int] = Field(default_factory=dict)
    last_loaded: str = ""
    cache_hash: str = ""
    load_time_ms: float = 0.0


# ---------------------------------------------------------------------------
# Doctrine definitions
# ---------------------------------------------------------------------------

CHAIN_OF_TITLE_DOCTRINES: List[Dict[str, Any]] = [
    # ==================== RECORDING ACT DOCTRINES ====================
    {
        "topic": "texas_race_notice_recording_act",
        "category": "RECORDING_ACT",
        "title": "Texas Race-Notice Recording Act",
        "summary": "Texas follows a race-notice recording system. A subsequent purchaser for value who records first without notice of a prior unrecorded conveyance takes priority. The recording acts protect bona fide purchasers who record before the prior unrecorded instrument is recorded.",
        "legal_basis": [
            "Texas Property Code Section 13.001",
            "Texas Property Code Section 13.002",
            "Madison v. Gordon, 39 S.W.3d 604 (Tex. 2001)",
            "Lutton v. de los Santos, 896 S.W.2d 564 (Tex. 1995)"
        ],
        "elements": [
            "Subsequent purchaser must pay valuable consideration",
            "Purchaser must act in good faith (no actual notice)",
            "Purchaser must not have constructive notice from recorded instruments",
            "Purchaser must record before the prior unrecorded instrument is recorded",
            "Shelter rule: grantee of a BFP is also protected even with notice"
        ],
        "texas_application": "Texas Property Code Sec. 13.001 provides that a conveyance of real property is void as to a subsequent purchaser for a valuable consideration without notice unless the instrument has been acknowledged, sworn to, or proved and filed for record. This is the foundation of all chain-of-title analysis in Texas.",
        "chain_impact": "Recording date establishes priority. Unrecorded instruments are valid between the parties but void as to subsequent BFPs. Chain examiner must check for unrecorded interests by examining possession and other notice factors.",
        "related_topics": ["constructive_notice", "actual_notice", "bona_fide_purchaser", "shelter_rule"],
        "exceptions": [
            "Unrecorded deed valid between grantor and grantee",
            "Donee takes subject to prior unrecorded interests (no valuable consideration)",
            "Heir takes subject to prior unrecorded interests",
            "Purchaser with actual notice not protected even if records first"
        ],
        "curative_actions": [
            "Record the unrecorded instrument immediately",
            "Obtain quitclaim deed from all parties claiming through unrecorded chain",
            "File quiet title action if dispute exists"
        ],
        "risk_level": "CRITICAL"
    },
    {
        "topic": "constructive_notice",
        "category": "RECORDING_ACT",
        "title": "Constructive Notice Doctrine",
        "summary": "Recording an instrument in the proper county deed records provides constructive notice to all the world. A purchaser is charged with knowledge of all properly recorded instruments in the chain of title regardless of whether they actually examined the records.",
        "legal_basis": [
            "Texas Property Code Section 13.002",
            "Westland Oil Development Corp. v. Gulf Oil Corp., 637 S.W.2d 903 (Tex. 1982)",
            "Strong v. Strong, 128 Tex. 470 (1937)"
        ],
        "elements": [
            "Instrument must be properly acknowledged or proved",
            "Instrument must be filed in the correct county",
            "Recording must be in the proper index (grantor-grantee or tract)",
            "Defective recording may not provide constructive notice",
            "Constructive notice extends only to instruments in the chain of title"
        ],
        "texas_application": "In Texas, recording in the official deed records of the county where the property is located provides constructive notice. A mis-indexed instrument may not provide constructive notice. The chain examiner must search both grantor-grantee index and tract index where available.",
        "chain_impact": "All properly recorded instruments in the chain provide constructive notice. Examiner must identify every recorded instrument in the chain. A break in the recording chain creates a potential notice gap.",
        "related_topics": ["texas_race_notice_recording_act", "actual_notice", "chain_of_title_search", "wild_deed"],
        "exceptions": [
            "Instruments outside the chain of title (wild deeds) do not provide constructive notice",
            "Defectively acknowledged instruments may not provide notice",
            "Instruments recorded in wrong county do not provide notice in correct county"
        ],
        "curative_actions": [
            "Re-record with proper acknowledgment",
            "Obtain affidavit confirming recording details",
            "File in correct county if previously recorded in wrong county"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "actual_notice",
        "category": "RECORDING_ACT",
        "title": "Actual Notice Doctrine",
        "summary": "A purchaser who has actual knowledge of an unrecorded interest cannot claim bona fide purchaser status regardless of the recording status. Actual notice includes direct knowledge, inquiry notice from visible possession, and notice from circumstances that would prompt a reasonable investigation.",
        "legal_basis": [
            "Madison v. Gordon, 39 S.W.3d 604 (Tex. 2001)",
            "Nobles v. Marcus, 533 S.W.2d 923 (Tex. 1976)",
            "Strong v. Strong, 128 Tex. 470 (1937)"
        ],
        "elements": [
            "Direct knowledge of the unrecorded interest",
            "Inquiry notice: facts that would prompt investigation by a prudent person",
            "Possession notice: open and visible possession by someone other than grantor",
            "Knowledge of facts that would lead to discovery upon reasonable inquiry",
            "Imputed notice through agents (attorney, broker, surveyor)"
        ],
        "texas_application": "Texas courts hold that a purchaser is charged with notice of facts that a reasonable investigation would reveal. Open possession of the land by someone other than the seller creates inquiry notice. The chain examiner should note any visible possession inconsistencies.",
        "chain_impact": "Actual notice defeats BFP status. If the chain examiner discovers evidence of adverse possession, visible occupation, or known claims, these must be flagged as potential notice issues affecting chain priority.",
        "related_topics": ["constructive_notice", "bona_fide_purchaser", "adverse_possession"],
        "exceptions": [],
        "curative_actions": [
            "Obtain release or quitclaim from party providing notice",
            "File quiet title action",
            "Obtain title insurance commitment noting the known interest"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "bona_fide_purchaser",
        "category": "RECORDING_ACT",
        "title": "Bona Fide Purchaser (BFP) Doctrine",
        "summary": "A bona fide purchaser is one who acquires property for valuable consideration, in good faith, and without notice (actual or constructive) of outstanding claims or defects. BFP status is the shield that protects against prior unrecorded interests under the recording acts.",
        "legal_basis": [
            "Texas Property Code Section 13.001",
            "Madison v. Gordon, 39 S.W.3d 604 (Tex. 2001)",
            "Diversified Mortg. Inv'rs v. Lloyd D. Blaylock Gen. Contractor, 576 S.W.2d 794 (Tex. 1979)"
        ],
        "elements": [
            "Valuable consideration paid (nominal consideration may not suffice)",
            "Good faith at time of purchase",
            "No actual notice of prior claims",
            "No constructive notice from recorded instruments",
            "Must record to gain priority under race-notice system"
        ],
        "texas_application": "In Texas, heirs, devisees, and donees are NOT bona fide purchasers because they do not pay valuable consideration. A purchaser at a tax sale may qualify as a BFP. The chain examiner must assess each link for BFP status to determine priority.",
        "chain_impact": "BFP analysis determines which chain link takes priority when competing claims exist. Each conveyance in the chain should be assessed for whether the grantee qualifies as a BFP.",
        "related_topics": ["texas_race_notice_recording_act", "shelter_rule", "constructive_notice", "actual_notice"],
        "exceptions": [
            "Donee does not qualify as BFP",
            "Heir does not qualify as BFP",
            "Purchaser with knowledge of fraud does not qualify",
            "Inadequate consideration may negate BFP status"
        ],
        "curative_actions": [],
        "risk_level": "HIGH"
    },
    {
        "topic": "shelter_rule",
        "category": "RECORDING_ACT",
        "title": "Shelter Rule",
        "summary": "A person who acquires property from a bona fide purchaser is 'sheltered' by the BFP's protected status, even if the subsequent grantee had notice of the prior unrecorded interest. This prevents the need to trace BFP status through every link.",
        "legal_basis": [
            "Restatement (Third) of Property: Servitudes Section 7.15",
            "General recording act jurisprudence",
            "Lutton v. de los Santos, 896 S.W.2d 564 (Tex. 1995)"
        ],
        "elements": [
            "Must trace back to a bona fide purchaser in the chain",
            "Subsequent grantee sheltered even with actual notice",
            "Applies to all transferees after the BFP",
            "Does not apply if grantee was the original defrauding party"
        ],
        "texas_application": "The shelter rule is recognized in Texas. Once a BFP enters the chain, all subsequent grantees are protected. The chain examiner need only find one BFP in the chain to shelter all downstream links from prior unrecorded interests.",
        "chain_impact": "Simplifies chain analysis by allowing the examiner to stop tracing BFP status once a confirmed BFP is found in the chain. All subsequent grantees inherit the BFP protection.",
        "related_topics": ["bona_fide_purchaser", "texas_race_notice_recording_act"],
        "exceptions": [
            "The defrauding grantor cannot use shelter rule to regain clean title",
            "Does not shelter against interests that were recorded before the BFP"
        ],
        "curative_actions": [],
        "risk_level": "MEDIUM"
    },

    # ==================== CHAIN SEARCH METHODOLOGY ====================
    {
        "topic": "chain_of_title_search",
        "category": "CHAIN_SEARCH",
        "title": "Chain of Title Search Methodology",
        "summary": "The chain of title is the sequential history of title to a particular parcel of land, traced through recorded instruments from the sovereign patent to the present owner. A title search involves examining the grantor-grantee indexes and/or tract indexes to identify all instruments in the chain.",
        "legal_basis": [
            "Texas standard title examination practices",
            "AAPL Title Examination Standards",
            "Texas Title Examination Standards (State Bar)"
        ],
        "elements": [
            "Start with current owner (backward search) or sovereign (forward search)",
            "Search grantor index for each owner during period of ownership",
            "Search grantee index backward to find how each owner acquired title",
            "Verify each link connects (grantee of one instrument is grantor of next)",
            "Check for encumbrances, liens, and adverse claims during each ownership period",
            "Verify legal description consistency throughout chain",
            "Note any instruments that appear to be outside the chain (wild deeds)"
        ],
        "texas_application": "Texas counties use the grantor-grantee index system. Some counties have unofficial tract indexes. The abstract system (abstract/survey/block) is the primary parcel identification. The search should cover at least 60 years or back to the sovereign patent.",
        "chain_impact": "This is the core methodology for constructing the chain. Every instrument must be verified as properly linking to the next. Gaps or missing links indicate potential title defects.",
        "related_topics": ["grantor_grantee_index", "tract_index", "root_of_title", "abstract_survey_system"],
        "exceptions": [],
        "curative_actions": [],
        "risk_level": "CRITICAL"
    },
    {
        "topic": "grantor_grantee_index",
        "category": "CHAIN_SEARCH",
        "title": "Grantor-Grantee Index System",
        "summary": "The grantor-grantee index is the official system for indexing recorded instruments in most Texas counties. Instruments are indexed alphabetically by grantor name in the grantor (direct) index and by grantee name in the grantee (reverse) index. The examiner searches forward in the grantor index and backward in the grantee index.",
        "legal_basis": [
            "Texas Property Code Section 12.001 et seq.",
            "Texas Local Government Code Section 191 et seq."
        ],
        "elements": [
            "Grantor index: alphabetical by grantor, chronological within name",
            "Grantee index: alphabetical by grantee, chronological within name",
            "Each entry contains: names, instrument type, date, volume/page or doc number, legal description summary",
            "Search grantor index for each owner to find all conveyances OUT",
            "Search grantee index for each owner to find all conveyances IN",
            "Name variants, misspellings, and aliases must be searched"
        ],
        "texas_application": "In Texas, the county clerk maintains the official grantor-grantee index. The index is the only official method of providing constructive notice. A mis-indexed instrument may not provide constructive notice. The examiner must search under all known name variants including maiden names, married names, AKAs, and corporate name changes.",
        "chain_impact": "The grantor-grantee index is the primary tool for chain construction. Search accuracy depends on name normalization and variant matching. The chain builder must handle soundex, phonetic matching, and fuzzy name matching to avoid missing links.",
        "related_topics": ["chain_of_title_search", "tract_index", "name_variance", "constructive_notice"],
        "exceptions": [],
        "curative_actions": [
            "If instrument mis-indexed, file affidavit of correction with county clerk",
            "Re-record with corrected names if necessary"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "tract_index",
        "category": "CHAIN_SEARCH",
        "title": "Tract Index System",
        "summary": "A tract index organizes recorded instruments by the parcel of land affected rather than by party names. Some Texas counties maintain unofficial tract indexes, and title companies often maintain their own. The tract index is more efficient for searching but is not the official index in most Texas jurisdictions.",
        "legal_basis": [
            "No statutory requirement in Texas",
            "Title company internal practices",
            "Abstract company methodologies"
        ],
        "elements": [
            "Organized by legal description (abstract/survey/block or lot/block/subdivision)",
            "Contains all instruments affecting a particular tract",
            "More efficient than grantor-grantee for parcel-specific searches",
            "May catch instruments missed by name search",
            "Not officially maintained in most Texas counties"
        ],
        "texas_application": "While Texas does not require a tract index, many title companies and abstract companies maintain them. In oil and gas title examination, the tract index is invaluable because mineral interests are tied to specific legal descriptions. The Permian Basin counties (Reeves, Ector, Midland, Martin) have well-maintained abstract company tract indexes.",
        "chain_impact": "Tract index supplements grantor-grantee search. Instruments affecting the tract but with unusual or misspelled names are more likely to be found via tract index. The chain builder should cross-reference both indexes when available.",
        "related_topics": ["grantor_grantee_index", "chain_of_title_search", "abstract_survey_system"],
        "exceptions": [],
        "curative_actions": [],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "root_of_title",
        "category": "CHAIN_SEARCH",
        "title": "Root of Title Selection",
        "summary": "The root of title is the starting instrument from which the chain is built forward. For a standard title examination, the root should be at least 40-60 years old. The root must be a conveyance or other instrument that purported to transfer the fee simple title and was properly recorded. For oil and gas, the root typically goes back to the sovereign patent.",
        "legal_basis": [
            "AAPL Title Examination Standards",
            "Texas State Bar Title Examination Standards",
            "Marketable Title Act concepts (Texas has no MTA)"
        ],
        "elements": [
            "Root must be at least 40 years old (standard) or 60 years (extended)",
            "Root must be a recorded conveyance of fee simple or equivalent interest",
            "Root must contain a sufficient legal description",
            "Root should appear regular on its face (no obvious defects)",
            "For O&G title: root should be sovereign patent when possible",
            "Subsequent instruments build chain forward from root"
        ],
        "texas_application": "Texas does not have a Marketable Title Act, so there is no statutory root of title period. The examiner must use professional judgment. For oil and gas examinations, the standard practice is to trace to the sovereign patent because mineral interests may have been severed at any point in the chain. For surface-only transactions, a 60-year root is generally acceptable.",
        "chain_impact": "Root selection determines chain depth. An inadequate root may miss prior severances, reservations, or encumbrances. The chain builder must allow configurable root depth and default to sovereign patent for O&G examinations.",
        "related_topics": ["chain_of_title_search", "sovereign_patent_chain", "marketable_title"],
        "exceptions": [
            "Surface-only transactions may use shorter search period",
            "Title insurance may accept shorter search with appropriate exceptions"
        ],
        "curative_actions": [
            "Extend search period back to sovereign if root is questioned",
            "Obtain title insurance with full search coverage"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "marketable_title",
        "category": "CHAIN_SEARCH",
        "title": "Marketable Title Standards",
        "summary": "Marketable title is title that a reasonably prudent buyer would accept, free from reasonable doubt about its validity. It need not be perfect, but must be free from material defects, liens, and encumbrances that would affect the buyer's quiet enjoyment. In Texas, marketable title requires an unbroken chain from sovereign to present owner.",
        "legal_basis": [
            "Luker v. City of Breckenridge, 225 S.W.2d 570 (Tex. 1950)",
            "Pairett v. Gutierrez, 969 S.W.2d 512 (Tex. App. 1998)",
            "Texas Title Examination Standards"
        ],
        "elements": [
            "Unbroken chain of title from recognized root",
            "No material defects in any link",
            "No outstanding liens or encumbrances (or they are satisfied/released)",
            "No adverse claims or lis pendens",
            "No breaks in the chain requiring curative action",
            "Proper legal description throughout chain",
            "All probate and heirship matters properly documented"
        ],
        "texas_application": "Texas courts define marketable title as title that a reasonably prudent buyer, familiar with the facts and their legal significance, would accept. The standard is not perfection but absence of reasonable doubt. Oil and gas title examination typically requires a higher standard because of the fractional nature of mineral interests.",
        "chain_impact": "The chain builder must assess each link for marketability. Cumulative minor defects can render title unmarketable even if no single defect is fatal. The overall chain confidence score reflects marketability.",
        "related_topics": ["root_of_title", "chain_of_title_search", "gap_analysis"],
        "exceptions": [],
        "curative_actions": [
            "Cure specific defects identified in chain",
            "Obtain title insurance to insure over minor defects",
            "File quiet title action for disputed ownership"
        ],
        "risk_level": "HIGH"
    },

    # ==================== TITLE DOCTRINES ====================
    {
        "topic": "after_acquired_title",
        "category": "TITLE_DOCTRINE",
        "title": "After-Acquired Title Doctrine (Estoppel by Deed)",
        "summary": "When a grantor conveys property by warranty deed but does not actually own the property at the time of conveyance, and later acquires the title, the after-acquired title automatically passes to the grantee by operation of law. This doctrine prevents the grantor from claiming the after-acquired title against the grantee.",
        "legal_basis": [
            "Texas Property Code Section 5.023",
            "Caswell v. Llano Oil Co., 120 Tex. 153 (1931)",
            "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
            "Restatement (Third) of Property: Donative Transfers"
        ],
        "elements": [
            "Grantor executed a warranty deed (general or special)",
            "Grantor did not own the property at time of conveyance",
            "Grantor subsequently acquires the title",
            "Title passes automatically to grantee by operation of law",
            "Applies only to warranty deeds, not quitclaim deeds",
            "Subsequent BFP from grantor may be protected under recording acts"
        ],
        "texas_application": "In Texas, the after-acquired title doctrine is well-established and is codified in the Property Code. It applies to warranty deeds but NOT to quitclaim deeds. This has major implications for mineral title examination because early conveyances often exceeded the grantor's actual ownership. The Duhig rule extends this concept to mineral reservations.",
        "chain_impact": "The chain builder must track warranty deed conveyances and check whether the grantor actually owned the interest at the time. If not, the chain must flag this as a potential after-acquired title scenario and trace whether the grantor later acquired the interest.",
        "related_topics": ["estoppel_by_deed", "duhig_rule", "warranty_deed"],
        "exceptions": [
            "Does not apply to quitclaim deeds",
            "Subsequent BFP may defeat after-acquired title if records first",
            "Does not apply if grantor's later acquisition is by different type of interest"
        ],
        "curative_actions": [
            "Obtain confirmation deed from grantor after acquisition",
            "Record memorandum of after-acquired title",
            "File affidavit establishing the chain of after-acquired title"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "estoppel_by_deed",
        "category": "TITLE_DOCTRINE",
        "title": "Estoppel by Deed",
        "summary": "A grantor who conveys by warranty deed is estopped from later denying the validity of the conveyance or claiming an interest inconsistent with the deed. The grantor is bound by the covenants of title and cannot assert a subsequently acquired interest against the grantee.",
        "legal_basis": [
            "Caswell v. Llano Oil Co., 120 Tex. 153 (1931)",
            "Houston Oil Co. v. Niles, 255 S.W. 604 (Tex. Comm'n App. 1923)",
            "Texas Property Code Section 5.023"
        ],
        "elements": [
            "Deed must contain covenants of title (warranty deed)",
            "Grantor purported to convey an interest",
            "Grantor is now estopped from claiming otherwise",
            "Estoppel runs with the land and binds subsequent grantors",
            "Both legal and equitable estoppel apply"
        ],
        "texas_application": "In Texas, estoppel by deed prevents a grantor from claiming an after-acquired interest against the grantee of a warranty deed. This is particularly important in mineral title where grantors frequently conveyed more than they owned, especially in early Permian Basin conveyances.",
        "chain_impact": "Chain builder must identify warranty deeds and track estoppel implications. If a grantor conveyed 100% but only owned 50%, the chain must note that the remaining 50% is subject to estoppel if the grantor later acquires it.",
        "related_topics": ["after_acquired_title", "duhig_rule", "warranty_deed"],
        "exceptions": [
            "Quitclaim deed creates no estoppel",
            "Special warranty deed limits estoppel to acts of grantor only"
        ],
        "curative_actions": [],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "duhig_rule",
        "category": "TITLE_DOCTRINE",
        "title": "Duhig Rule (Texas Mineral Title)",
        "summary": "Under the Duhig rule, when a grantor conveys land by warranty deed with a mineral reservation, but a prior grantor has already reserved minerals, the warranty covenants estop the current grantor from claiming the reservation. The grantor's reservation fails because the warranty to the grantee takes precedence.",
        "legal_basis": [
            "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
            "Kokernot v. Caldwell, 231 S.W.2d 528 (Tex. 1950)",
            "Harris v. Currie, 176 S.W.2d 129 (Tex. 1943)"
        ],
        "elements": [
            "Grantor conveys by warranty deed",
            "Deed contains mineral reservation by grantor",
            "Prior grantor already reserved minerals in earlier conveyance",
            "Total minerals conveyed plus reserved would exceed 100%",
            "Warranty covenants protect grantee over grantor's reservation"
        ],
        "texas_application": "The Duhig rule is uniquely important in Texas mineral title. Many Permian Basin conveyances involve chains where multiple grantors attempted to reserve minerals. The Duhig rule resolves the overconveyance by giving priority to the grantee's warranty deed over the grantor's reservation. This is one of the most frequently encountered title issues in West Texas mineral examination.",
        "chain_impact": "Critical for mineral interest fraction calculation. The chain builder must track all mineral reservations and compare total reserved plus conveyed against 100%. When overage exists in a warranty deed, the Duhig rule reduces the grantor's reservation. This fundamentally changes the ownership calculation.",
        "related_topics": ["after_acquired_title", "estoppel_by_deed", "mineral_reservation", "fractional_interest_tracking"],
        "exceptions": [
            "Does not apply to quitclaim deeds",
            "Does not apply to special warranty deeds in some courts",
            "May not apply where intent is clear from four corners of deed"
        ],
        "curative_actions": [
            "Stipulation of interest from all affected parties",
            "Quiet title action to resolve Duhig overconveyance",
            "Agreed judgment establishing mineral ownership"
        ],
        "risk_level": "CRITICAL"
    },
    {
        "topic": "wild_deed",
        "category": "TITLE_DOCTRINE",
        "title": "Wild Deeds and Stray Instruments",
        "summary": "A wild deed is a recorded instrument that cannot be connected to the chain of title through the recording index. It typically occurs when a deed is recorded from a grantor who never appears in the chain as a grantee. A wild deed does not provide constructive notice because a reasonable search of the grantor-grantee index would not discover it.",
        "legal_basis": [
            "Lutton v. de los Santos, 896 S.W.2d 564 (Tex. 1995)",
            "Board of Regents v. S&G Constr. Co., 529 S.W.2d 90 (Tex. App. 1975)",
            "Restatement of Property: Servitudes"
        ],
        "elements": [
            "Instrument is recorded in county deed records",
            "Grantor of instrument never appears as grantee in the chain",
            "Cannot be found by searching grantor-grantee index in normal chain",
            "Does not provide constructive notice to subsequent purchasers",
            "May be discovered through tract index if available"
        ],
        "texas_application": "In Texas, wild deeds do not provide constructive notice under the grantor-grantee index system. However, they may provide actual notice if the person claiming under the wild deed is in possession. This is a significant issue in West Texas where early mineral conveyances sometimes were recorded outside the chain.",
        "chain_impact": "Wild deeds create a parallel chain that may or may not prevail depending on BFP status. The chain builder must identify potential wild deeds by detecting grantors who have no recorded source of title. These are flagged as stray instruments requiring investigation.",
        "related_topics": ["constructive_notice", "grantor_grantee_index", "chain_of_title_search"],
        "exceptions": [
            "May provide constructive notice through tract index in some jurisdictions",
            "May provide actual notice if party is in possession"
        ],
        "curative_actions": [
            "Connect the wild deed to the chain through a linking instrument",
            "Obtain quitclaim deed to bridge the gap",
            "File quiet title action"
        ],
        "risk_level": "CRITICAL"
    },
    {
        "topic": "mother_hubbard_clause",
        "category": "TITLE_DOCTRINE",
        "title": "Mother Hubbard Clause",
        "summary": "A Mother Hubbard clause (also called a cover-all or blanket clause) is a provision in a deed that purports to convey all property owned by the grantor in a particular county or area, in addition to specifically described tracts. Texas courts have held that such clauses are disfavored and may not convey property not specifically described.",
        "legal_basis": [
            "Sharp v. Fowler, 252 S.W.2d 153 (Tex. 1952)",
            "Geodyne Resources Ltd. v. Newton Corp., 923 S.W.2d 115 (Tex. App. 1996)",
            "Pich v. Lankford, 302 S.W.2d 645 (Tex. 1957)"
        ],
        "elements": [
            "Clause purports to convey all property in an area",
            "Typically says 'together with all other property owned by grantor in [county]'",
            "Disfavored by Texas courts",
            "May not convey property not specifically described in deed",
            "Intent of parties is examined but narrowly construed",
            "Does not provide constructive notice for non-described tracts"
        ],
        "texas_application": "Texas strongly disfavors Mother Hubbard clauses. They are generally held to convey only specifically described property. However, between the parties, they may convey the additional property if intent is clear. They do NOT provide constructive notice for undescribed tracts because a searcher would not find the instrument by legal description.",
        "chain_impact": "The chain builder must identify Mother Hubbard clauses and NOT treat them as valid conveyances of undescribed tracts for chain purposes. They should be flagged as potential claims requiring investigation but not used to build chain links for non-described property.",
        "related_topics": ["constructive_notice", "legal_description", "chain_of_title_search"],
        "exceptions": [
            "Valid between the parties to the deed",
            "May be effective if both tracts are specifically described elsewhere in deed"
        ],
        "curative_actions": [
            "Obtain specific deed for the additional tract",
            "File corrective deed with proper legal description",
            "Obtain ratification from grantor"
        ],
        "risk_level": "HIGH"
    },

    # ==================== SOVEREIGN CHAIN DOCTRINES ====================
    {
        "topic": "sovereign_patent_chain",
        "category": "SOVEREIGN",
        "title": "Sovereign Patent and the Root of All Title",
        "summary": "All title to land in Texas originates from the sovereign - either Spain, Mexico, the Republic of Texas, the State of Texas, or in some cases the United States. The sovereign patent is the first instrument in every chain of title and establishes the original grant of ownership from the government to a private party.",
        "legal_basis": [
            "Texas Constitution Art. XIV",
            "Treaty of Guadalupe Hidalgo (1848)",
            "Texas General Land Office records",
            "Republic of Texas land grant statutes"
        ],
        "elements": [
            "Every chain of title must trace to a sovereign origin",
            "Texas retained its public lands upon annexation to the US",
            "Texas General Land Office (GLO) maintains patent records",
            "Patent types: headright, bounty, donation, script, school land, university land",
            "Patent conveys fee simple from sovereign to patentee"
        ],
        "texas_application": "Texas is unique among states because it retained its public lands when it joined the Union in 1845. All Texas land patents come from the Republic of Texas or State of Texas, not the federal government (except for a small strip ceded to the US). The Texas General Land Office maintains all patent records and is the starting point for every chain.",
        "chain_impact": "The sovereign patent is the absolute root of every chain. The chain builder must verify that the chain traces back to a recognized patent. If the patent cannot be located, this is a critical chain defect.",
        "related_topics": ["spanish_mexican_grants", "republic_of_texas_grants", "school_land_psf", "railroad_land_grants", "abstract_survey_system"],
        "exceptions": [
            "Federal patents exist for small areas ceded by Texas",
            "Indian land grants in some East Texas areas"
        ],
        "curative_actions": [
            "Research GLO records for missing patent",
            "File certified copy of patent from GLO",
            "Obtain title insurance with sovereign chain coverage"
        ],
        "risk_level": "CRITICAL"
    },
    {
        "topic": "spanish_mexican_grants",
        "category": "SOVEREIGN",
        "title": "Spanish and Mexican Land Grants",
        "summary": "Before Texas independence in 1836, land was granted by the Spanish Crown (pre-1821) and the Republic of Mexico (1821-1836). These grants include royal grants, empresario grants, and colonization grants. Their validity was generally confirmed by the Republic and State of Texas.",
        "legal_basis": [
            "Treaty of Guadalupe Hidalgo (1848)",
            "Republic of Texas land laws",
            "Texas Supreme Court: State v. Balli, 144 Tex. 195 (1945)",
            "Bourland and Miller commission records"
        ],
        "elements": [
            "Spanish grants pre-date 1821 Mexican independence",
            "Mexican grants date from 1821-1836 Texas independence",
            "Empresario grants given to colonizers (Austin, DeWitt, etc.)",
            "Royal grants from Spanish Crown directly",
            "Validity confirmed by Republic of Texas, Bourland-Miller commission",
            "Some grants never confirmed and remain disputed"
        ],
        "texas_application": "In South Texas and the Rio Grande Valley, Spanish and Mexican land grants are the root of many chains. Some grants encompass enormous tracts (porciones). The validity of these grants was confirmed by various Texas commissions. Some remain disputed, particularly in the border region. The chain examiner must verify confirmation of the original grant.",
        "chain_impact": "Spanish/Mexican grants that were confirmed by the Republic or State are valid roots of title. Unconfirmed grants create a critical chain defect. The chain builder must check GLO records for confirmation status.",
        "related_topics": ["sovereign_patent_chain", "republic_of_texas_grants"],
        "exceptions": [
            "Unconfirmed grants may not be valid roots of title",
            "Grants that violate the Colonization Law of 1825 may be void"
        ],
        "curative_actions": [
            "Research GLO for confirmation records",
            "Obtain certified copies of confirmation proceedings"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "republic_of_texas_grants",
        "category": "SOVEREIGN",
        "title": "Republic of Texas Land Grants",
        "summary": "The Republic of Texas (1836-1846) issued its own land grants including headrights, bounty warrants, and donation grants. These are common roots of title in Central and West Texas. The Republic grants were continued and recognized by the State of Texas after annexation.",
        "legal_basis": [
            "Republic of Texas land laws (1836-1846)",
            "Texas Constitution of 1845",
            "Texas General Land Office Act",
            "Annexation Resolution (1845)"
        ],
        "elements": [
            "Headright grants: 640 acres to heads of household present before Mar 2, 1836",
            "Bounty grants: Military service in Texas Revolution",
            "Donation grants: Military service, lesser amounts",
            "Land scrip: Transferable certificates for land",
            "All grants required survey and patent from GLO"
        ],
        "texas_application": "Republic of Texas grants form the root of title for much of Central and West Texas. In the Permian Basin, many early patents trace to Republic-era headrights and bounty warrants that were located on surveys in the 1870s-1880s. The chain examiner must verify both the certificate and the patent.",
        "chain_impact": "Republic grants are valid sovereign roots. The chain must verify the patent was issued by GLO, the survey was properly conducted, and the certificate was valid. Missing patents require GLO research.",
        "related_topics": ["sovereign_patent_chain", "abstract_survey_system"],
        "exceptions": [
            "Fraudulent certificates were common in Republic era",
            "Some certificates were located on previously patented land"
        ],
        "curative_actions": [
            "Research GLO for patent and certificate records",
            "Obtain certified copy of patent from GLO"
        ],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "railroad_land_grants",
        "category": "SOVEREIGN",
        "title": "Railroad Land Grants",
        "summary": "Texas granted large tracts of public land to railroad companies as incentives for construction. These grants created a checkerboard pattern of railroad and public school land sections. Railroad companies then sold or conveyed their granted sections, creating unique chain of title patterns.",
        "legal_basis": [
            "Texas railroad land grant statutes (various, 1850s-1880s)",
            "Texas & Pacific Railway Co. land grants",
            "Houston & Texas Central Railway grants",
            "Texas General Land Office records"
        ],
        "elements": [
            "Alternate sections granted to railroads",
            "Remaining sections retained by state (school land/PSF)",
            "Railroad received odd-numbered sections, state retained even (or vice versa)",
            "Railroad companies conveyed by deed, creating standard chain",
            "Some railroads conveyed mineral rights separately",
            "Railroad bankruptcy may affect chain"
        ],
        "texas_application": "In the Permian Basin, the Texas & Pacific Railway received large grants. Sections are typically 640 acres (one square mile). The alternating section pattern means adjacent sections may have very different chain origins (railroad vs. school land). This is critical for proper chain identification - the chain builder must determine whether a section is railroad or school land.",
        "chain_impact": "Railroad grant sections have a corporate grantor at the top of the chain. The chain builder must identify the railroad company, verify the grant, and trace conveyances from the railroad forward. Mineral reservations by railroad companies are common and must be tracked.",
        "related_topics": ["sovereign_patent_chain", "school_land_psf", "abstract_survey_system"],
        "exceptions": [
            "Some grants were forfeited for non-construction",
            "Mineral reservations vary by railroad company and era"
        ],
        "curative_actions": [
            "Research railroad company succession and conveyance records",
            "Verify grant was not forfeited"
        ],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "school_land_psf",
        "category": "SOVEREIGN",
        "title": "School Land and Permanent School Fund (PSF)",
        "summary": "Texas dedicated alternate sections of public land to the Permanent School Fund (PSF). These sections were sold or leased by the State, creating unique chain patterns. School land minerals may be owned by the State even after surface sale. The PSF retains mineral interests in many West Texas sections.",
        "legal_basis": [
            "Texas Constitution Art. VII, Sections 2, 4, 5",
            "Texas Natural Resources Code Chapter 52",
            "Texas Education Code Chapter 43",
            "Relinquishment Act (1919)"
        ],
        "elements": [
            "Alternate sections retained by State for school fund",
            "Surface sold to settlers, minerals often retained by State",
            "Relinquishment Act allows surface owner to develop minerals with State royalty",
            "PSF retains 100% minerals in many sections",
            "State lease sales conducted by GLO",
            "Surface patents from GLO do not convey minerals in school land"
        ],
        "texas_application": "In the Permian Basin, school land sections are extremely common. The examiner must determine if a section is school land by checking the abstract/survey records. If it is school land, the State (PSF) likely owns the minerals. The Relinquishment Act allows the surface owner to lease the minerals and share royalty with the State. This creates a very different chain structure than private mineral ownership.",
        "chain_impact": "School land sections require fundamentally different chain analysis. The surface chain traces from State patent forward. The mineral chain may be entirely State-owned. The chain builder must flag school land sections and apply the correct analysis framework.",
        "related_topics": ["sovereign_patent_chain", "railroad_land_grants", "abstract_survey_system", "relinquishment_act"],
        "exceptions": [
            "Some school land minerals were sold before the reservation practice began",
            "Relinquishment Act gives surface owner leasing rights with State royalty"
        ],
        "curative_actions": [
            "Verify school land status through GLO records",
            "Determine if Relinquishment Act applies",
            "Research GLO lease sale records for mineral interests"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "abstract_survey_system",
        "category": "SOVEREIGN",
        "title": "Abstract/Survey System (Texas)",
        "summary": "Texas uses the abstract/survey system for land identification rather than the rectangular survey system used in most western states. Each parcel is identified by an abstract number, original grantee, survey number, and block designation. This system originated from the original land grants and surveys.",
        "legal_basis": [
            "Texas General Land Office survey records",
            "Texas Natural Resources Code",
            "County survey records"
        ],
        "elements": [
            "Abstract number: unique sequential number assigned by GLO",
            "Survey number: number within the block",
            "Block number: group of surveys, often tied to railroad grants",
            "Original grantee: person or entity to whom original certificate was issued",
            "Section: typically 640 acres (one square mile)",
            "Metes and bounds: original survey boundary description"
        ],
        "texas_application": "In the Permian Basin, parcels are identified as 'Abstract __, Survey __, Block __, [Township/Section], [Railroad Company]'. For example: 'Abstract 1234, Section 5, Block C-22, PSL Survey, Reeves County, Texas'. The abstract number is the primary identifier and links to all GLO records. The chain builder must normalize and match legal descriptions using this system.",
        "chain_impact": "Legal description matching is essential for chain construction. The abstract/survey system provides the key for connecting instruments to specific parcels. The chain builder must parse and normalize legal descriptions to correctly identify which instruments affect which parcels.",
        "related_topics": ["sovereign_patent_chain", "legal_description_matching", "chain_of_title_search"],
        "exceptions": [
            "Subdivisions in urban areas use lot/block/subdivision",
            "Some areas use metes and bounds without abstract numbers"
        ],
        "curative_actions": [
            "Verify abstract number through GLO records",
            "Obtain certified survey plat for boundary disputes"
        ],
        "risk_level": "MEDIUM"
    },

    # ==================== GAP ANALYSIS DOCTRINES ====================
    {
        "topic": "gap_analysis",
        "category": "GAP_ANALYSIS",
        "title": "Gap Analysis Methodology",
        "summary": "Gap analysis identifies missing links, temporal breaks, and unexplained transitions in the chain of title. Gaps may indicate lost instruments, unrecorded conveyances, probate matters not reflected in deed records, adverse possession, or clerical errors. Each gap must be classified and assessed for risk.",
        "legal_basis": [
            "AAPL Title Examination Standards",
            "Texas State Bar Title Standards",
            "Standard landman examination practices"
        ],
        "elements": [
            "Temporal gap: period where no conveyance activity appears",
            "Conveyance gap: grantee of one instrument does not match grantor of next",
            "Recording gap: significant delay between execution and recording",
            "Interest gap: conveyed interest does not equal received interest",
            "Name gap: grantor/grantee name does not match due to marriage, error, alias",
            "Legal description gap: description changes between instruments"
        ],
        "texas_application": "In Texas oil and gas title, gaps are common and must be carefully analyzed. Common causes include: heirship not established by affidavit, probate not recorded in deed records, name changes due to marriage, and corporate succession. The standard practice is to require curative for all material gaps.",
        "chain_impact": "Every gap in the chain is a potential title defect. The chain builder must identify, classify, and score all gaps. Critical gaps (conveyance breaks) require curative action. Minor gaps (name variances) may be acceptable with supporting evidence.",
        "related_topics": ["chain_of_title_search", "marketable_title", "curative_doctrine"],
        "exceptions": [],
        "curative_actions": [
            "Affidavit of heirship for death gaps",
            "Correction deed for name variances",
            "Quitclaim deed to bridge conveyance gaps",
            "Court order for complex disputes"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "temporal_gap_analysis",
        "category": "GAP_ANALYSIS",
        "title": "Temporal Gap Detection and Classification",
        "summary": "Temporal gaps are periods in the chain where no recorded activity appears for a particular owner. While some gaps are normal (an owner holding property for decades), extended gaps may indicate missing records, unrecorded transfers, or death/heirship issues. The length and context of the gap determine its significance.",
        "legal_basis": [
            "Title examination standard practices",
            "AAPL Title Standards"
        ],
        "elements": [
            "Short gap (<1 year): usually normal, recording delay",
            "Medium gap (1-5 years): investigate, may indicate unrecorded transfer",
            "Long gap (5-20 years): significant, requires explanation",
            "Extended gap (>20 years): critical, likely missing records or death/heirship",
            "Context matters: family ownership explains longer gaps",
            "Corporate ownership: shorter gaps expected due to entity changes"
        ],
        "texas_application": "In Texas, temporal gaps are common in rural and ranch properties where families held land for generations. The examiner must assess whether a gap is explained by continued family ownership or indicates missing links. For O&G title, any gap over 5 years should be investigated.",
        "chain_impact": "Temporal gaps affect chain confidence scoring. The chain builder assigns decreasing confidence as gap length increases and flags gaps requiring curative action.",
        "related_topics": ["gap_analysis", "heirship_gap", "probate_gap"],
        "exceptions": [
            "Family ownership explains multi-decade gaps",
            "Rural ranch land commonly has long ownership periods"
        ],
        "curative_actions": [
            "Research probate records for deaths during gap period",
            "Obtain affidavit of heirship",
            "Check tax records for ownership during gap"
        ],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "conveyance_gap",
        "category": "GAP_ANALYSIS",
        "title": "Conveyance Gap (Break in Chain)",
        "summary": "A conveyance gap exists when the grantee of one recorded instrument does not match the grantor of the next instrument in the chain. This is a fundamental break in the chain of title and is one of the most serious title defects. It means there is a missing link between two known instruments.",
        "legal_basis": [
            "Title examination standard practices",
            "Marketable title requirements"
        ],
        "elements": [
            "Grantee in prior instrument does not match grantor in subsequent instrument",
            "May be due to: unrecorded conveyance, heirship, name change, entity succession",
            "Must be bridged by a linking instrument or explanation",
            "Quitclaim deed is the standard curative instrument",
            "Affidavit of heirship bridges death-related gaps"
        ],
        "texas_application": "In Texas, conveyance gaps are common where property passed by inheritance without a recorded deed. The heirship affidavit or court-determined heirship proceeding is the standard cure. For corporate succession, documentation of merger, name change, or dissolution bridges the gap.",
        "chain_impact": "Conveyance gaps are critical chain defects. The chain builder must detect these by comparing grantee names with subsequent grantor names using fuzzy matching. Each conveyance gap breaks the chain and must be flagged for curative action.",
        "related_topics": ["gap_analysis", "heirship_gap", "name_variance", "wild_deed"],
        "exceptions": [],
        "curative_actions": [
            "Quitclaim deed from missing link party",
            "Affidavit of heirship for death/inheritance gaps",
            "Corporate succession documentation",
            "Court order establishing chain"
        ],
        "risk_level": "CRITICAL"
    },
    {
        "topic": "heirship_gap",
        "category": "GAP_ANALYSIS",
        "title": "Heirship Gap (Death Without Recorded Transfer)",
        "summary": "An heirship gap occurs when a title holder dies and the property passes to heirs by operation of law, but no recorded instrument reflects the transfer. This is one of the most common gaps in Texas title chains, especially in rural areas where families held property for generations.",
        "legal_basis": [
            "Texas Estates Code Section 201 et seq.",
            "Texas Property Code Section 52.001 et seq.",
            "Tex. Estates Code Section 203.001 (affidavit of heirship)"
        ],
        "elements": [
            "Title holder died (must verify death)",
            "No will probated in deed records (or no will at all)",
            "Property passes by intestate succession or under will",
            "Heirs not determined by court or affidavit",
            "Gap exists between decedent and heirs in deed records",
            "May span multiple generations if uncured"
        ],
        "texas_application": "Texas allows heirship to be established by: (1) Probate of will, (2) Court-determined heirship (Texas Estates Code), (3) Affidavit of heirship (filed in deed records and effective after 5 years). The affidavit of heirship is the most common cure in West Texas. For O&G title, the heirship affidavit must properly identify all heirs and their fractional interests.",
        "chain_impact": "Heirship gaps split the chain into multiple branches (one per heir). The chain builder must identify death events, determine heirs, calculate fractional interests, and create branch chains for each heir. This is the primary source of chain branching in most titles.",
        "related_topics": ["conveyance_gap", "gap_analysis", "fractional_interest_tracking", "intestate_succession"],
        "exceptions": [
            "Will may disinherit heirs (within legal limits)",
            "Community property rules affect surviving spouse's share",
            "Homestead rights may prevent partition"
        ],
        "curative_actions": [
            "File affidavit of heirship in deed records",
            "Probate the will (even late probate allowed in Texas)",
            "Court-determined heirship proceeding",
            "Small estate affidavit (if estate qualifies)"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "name_variance",
        "category": "GAP_ANALYSIS",
        "title": "Name Variance Between Instruments",
        "summary": "Name variances occur when the same person appears under different names in consecutive instruments (e.g., marriage name change, nickname, misspelling, middle name variation). While not a true break in chain, name variances must be resolved to confirm identity.",
        "legal_basis": [
            "Title examination standard practices",
            "Idem sonans doctrine (same sound)"
        ],
        "elements": [
            "Name differences between grantee and subsequent grantor",
            "Common causes: marriage, nickname, misspelling, middle initial, suffix",
            "Idem sonans: names that sound alike are treated as identical",
            "Affidavit of identity resolves substantial variances",
            "Corrections deed for significant errors"
        ],
        "texas_application": "Texas follows the idem sonans doctrine: names that sound the same are treated as identical (e.g., 'Thomson' and 'Thompson'). Minor variances (middle initial, suffix) are usually acceptable without curative. Substantial variances (married vs. maiden name) require affidavit of identity.",
        "chain_impact": "Name variances are the most common minor chain issue. The chain builder must use fuzzy matching, soundex, and metaphone to identify probable matches. Variances above the matching threshold should be flagged but not treated as breaks.",
        "related_topics": ["conveyance_gap", "grantor_grantee_index"],
        "exceptions": [
            "Truly different persons with similar names",
            "Fraudulent use of similar name"
        ],
        "curative_actions": [
            "Affidavit of identity establishing same person",
            "Correction deed with proper names",
            "Marriage certificate for married name changes"
        ],
        "risk_level": "LOW"
    },

    # ==================== CONVEYANCE DOCTRINES ====================
    {
        "topic": "warranty_deed",
        "category": "CONVEYANCE",
        "title": "General Warranty Deed Covenants",
        "summary": "A general warranty deed contains six traditional covenants of title: seisin, right to convey, against encumbrances, quiet enjoyment, warranty, and further assurances. These covenants warrant the entire chain of title, not just the grantor's own acts. This makes warranty deeds the strongest form of conveyance.",
        "legal_basis": [
            "Texas Property Code Section 5.022",
            "Common law covenants of title"
        ],
        "elements": [
            "Covenant of seisin: grantor owns the interest being conveyed",
            "Covenant of right to convey: grantor has authority to transfer",
            "Covenant against encumbrances: no undisclosed liens/encumbrances",
            "Covenant of quiet enjoyment: grantee will not be disturbed",
            "Covenant of warranty: grantor will defend title against all claims",
            "Covenant of further assurances: grantor will execute additional documents"
        ],
        "texas_application": "In Texas, the statutory warranty deed form (Property Code Sec. 5.022) includes all six covenants by use of the word 'grant'. A deed that uses 'grant, sell, and convey' with 'general warranty' language creates a full warranty deed. The after-acquired title doctrine and estoppel by deed apply to warranty deeds.",
        "chain_impact": "Warranty deeds are the strongest links in a chain. They trigger after-acquired title and estoppel by deed. The chain builder should note whether each link is a warranty deed, special warranty deed, or quitclaim deed, as this affects the strength of each link and the application of various doctrines.",
        "related_topics": ["after_acquired_title", "estoppel_by_deed", "duhig_rule", "special_warranty_deed"],
        "exceptions": [],
        "curative_actions": [],
        "risk_level": "LOW"
    },
    {
        "topic": "special_warranty_deed",
        "category": "CONVEYANCE",
        "title": "Special Warranty Deed",
        "summary": "A special warranty deed limits the grantor's warranty to claims arising from the grantor's own acts. The grantor does not warrant against defects or claims that arose before the grantor's ownership. This is a weaker form of conveyance than a general warranty deed.",
        "legal_basis": [
            "Texas Property Code Section 5.023",
            "Common law of deeds"
        ],
        "elements": [
            "Grantor warrants only against own acts",
            "Does not warrant against prior defects",
            "Common in corporate and institutional transactions",
            "After-acquired title may or may not apply (jurisdiction varies)",
            "Less protection for grantee than general warranty deed"
        ],
        "texas_application": "Special warranty deeds are common in Texas for corporate and bank transactions. The examiner must note that the chain protection is limited for links conveyed by special warranty deed. Prior defects are not warranted.",
        "chain_impact": "Special warranty deeds create weaker chain links. The chain builder should flag special warranty deeds and note the reduced protection. Estoppel by deed may be limited for these instruments.",
        "related_topics": ["warranty_deed", "quitclaim_deed"],
        "exceptions": [],
        "curative_actions": [],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "quitclaim_deed",
        "category": "CONVEYANCE",
        "title": "Quitclaim Deed",
        "summary": "A quitclaim deed conveys only whatever interest the grantor may have, without warranty that the grantor actually owns anything. It creates no estoppel and does not trigger after-acquired title. In Texas, quitclaim deeds do not make the grantee a bona fide purchaser.",
        "legal_basis": [
            "Texas Property Code Section 13.001",
            "Lutton v. de los Santos, 896 S.W.2d 564 (Tex. 1995)",
            "Houston First American Savings v. Musick, 650 S.W.2d 413 (Tex. 1983)"
        ],
        "elements": [
            "Conveys only grantor's interest, if any",
            "No warranties of title",
            "No estoppel by deed",
            "No after-acquired title",
            "Grantee may not qualify as BFP under Texas law",
            "Common for curative purposes"
        ],
        "texas_application": "In Texas, a quitclaim deed is sometimes called a 'release deed.' Texas courts have held that a grantee under a quitclaim deed is NOT a bona fide purchaser because the quitclaim language puts them on notice that the grantor's title may be defective. Quitclaim deeds are commonly used for curative purposes to release claims.",
        "chain_impact": "Quitclaim deeds are the weakest chain links. They do not create BFP protection and do not trigger after-acquired title. The chain builder should flag quitclaim deeds and reduce chain confidence accordingly. However, quitclaim deeds used for curative purposes (bridging gaps) serve an important chain function.",
        "related_topics": ["warranty_deed", "bona_fide_purchaser", "curative_doctrine"],
        "exceptions": [],
        "curative_actions": [],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "mineral_reservation",
        "category": "CONVEYANCE",
        "title": "Mineral Reservation and Exception",
        "summary": "A mineral reservation retains mineral rights in the grantor when the surface estate is conveyed. A mineral exception removes minerals from the conveyance, acknowledging they belong to a third party. The distinction between reservation and exception is critical for chain analysis and determining who owns the mineral estate.",
        "legal_basis": [
            "Texas case law on mineral estates",
            "French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995)",
            "Altman v. Blake, 712 S.W.2d 117 (Tex. 1986)"
        ],
        "elements": [
            "Reservation: grantor retains minerals for themselves",
            "Exception: grantor acknowledges minerals belong to third party",
            "Must specify what estate is reserved (minerals, royalty, executive right)",
            "Fractional reservation common (e.g., 'reserving 1/2 of minerals')",
            "Surface of minerals: rights to use surface for mineral development"
        ],
        "texas_application": "Texas recognizes the mineral estate as a separate, dominant estate. Mineral reservations must be carefully parsed to determine exactly what interest was retained. The 'minerals' definition in Texas includes oil, gas, and other substances if the intent was to reserve a mineral estate. Limestone, sand, and gravel may or may not be included depending on the deed language.",
        "chain_impact": "Every mineral reservation splits the chain into surface and mineral branches. The chain builder must track mineral reservations, calculate fractional interests, and maintain parallel chains for surface and mineral estates. This is the primary source of fractional interest complexity.",
        "related_topics": ["duhig_rule", "fractional_interest_tracking", "executive_right"],
        "exceptions": [
            "General warranty without reservation passes all minerals",
            "Exception vs reservation distinction affects chain construction"
        ],
        "curative_actions": [
            "Stipulation of interest to clarify ambiguous reservation language",
            "Correction deed to fix reservation errors"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "fractional_interest_tracking",
        "category": "CONVEYANCE",
        "title": "Fractional Interest Tracking",
        "summary": "Mineral and royalty interests are typically conveyed and reserved as fractions of the whole. Over generations, these fractions multiply and subdivide, creating complex ownership patterns. Accurate tracking of fractional interests through the chain is essential for determining net mineral acres (NMA) and royalty payments.",
        "legal_basis": [
            "Texas mineral interest law",
            "Standard landman calculation methods"
        ],
        "elements": [
            "Fractional interests expressed as decimal or fraction",
            "Must track: mineral interest, royalty interest, working interest, ORRI",
            "Fractions multiply when interest is subdivided (e.g., 1/2 of 1/2 = 1/4)",
            "Total of all interests must equal 1.0 (100%)",
            "Net mineral acres (NMA) = gross acres x mineral interest fraction",
            "Net revenue interest (NRI) = working interest x (1 - royalty burdens)"
        ],
        "texas_application": "In the Permian Basin, mineral interests have been subdivided for over 100 years. A single section may have dozens of mineral owners with fractional interests expressed as complex fractions (e.g., 'an undivided 1/16 of 1/2 of 1/4'). The chain builder must calculate these correctly and verify total does not exceed 1.0.",
        "chain_impact": "Fractional interest tracking is the mathematical core of chain analysis. The chain builder must maintain running totals for each owner, handle branching (heirship), merger (reconveyance), and verify that all interests sum correctly at every point in the chain.",
        "related_topics": ["mineral_reservation", "duhig_rule", "heirship_gap", "branch_handling"],
        "exceptions": [],
        "curative_actions": [
            "Stipulation of interest if fractions don't balance",
            "Division order title opinion to establish correct fractions"
        ],
        "risk_level": "HIGH"
    },

    # ==================== SPECIAL DOCTRINES ====================
    {
        "topic": "adverse_possession",
        "category": "SPECIAL_DOCTRINE",
        "title": "Adverse Possession and Limitations",
        "summary": "Adverse possession allows a person who openly, continuously, exclusively, and adversely possesses another's land for the statutory period to acquire title by operation of law. Texas has multiple limitation periods (3, 5, 10, and 25 years) depending on the circumstances.",
        "legal_basis": [
            "Texas Civil Practice and Remedies Code Sections 16.021-16.030",
            "Texas Property Code Section 22.001 et seq.",
            "Rhodes v. Cahill, 802 S.W.2d 643 (Tex. 1990)"
        ],
        "elements": [
            "Open and notorious possession",
            "Continuous and uninterrupted for statutory period",
            "Exclusive possession (not shared with owner)",
            "Adverse/hostile to true owner's interest",
            "Under claim of right or color of title",
            "Payment of taxes (for 5-year statute)",
            "3-year: with registered title or judgment",
            "5-year: with payment of taxes under deed/judgment",
            "10-year: general adverse possession",
            "25-year: peaceable possession without claim of right"
        ],
        "texas_application": "In Texas, adverse possession is significant in rural areas where fences may not follow true boundaries. For mineral interests, adverse possession is extremely rare because minerals cannot be 'possessed' in the traditional sense. The chain examiner should note any evidence of adverse possession claims.",
        "chain_impact": "Adverse possession can insert a new owner into the chain without a recorded conveyance. The chain builder must be aware of adverse possession claims flagged by the ENCORE scraper or ShadowGlass. These create potential competing chains.",
        "related_topics": ["gap_analysis", "actual_notice"],
        "exceptions": [
            "Cannot adversely possess minerals (generally)",
            "Cannot adversely possess government land",
            "Disability of owner may toll the limitations period"
        ],
        "curative_actions": [
            "Trespass to try title suit to establish adverse possession",
            "Affidavit of adverse possession (for 25-year statute)"
        ],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "lis_pendens",
        "category": "SPECIAL_DOCTRINE",
        "title": "Lis Pendens (Pending Litigation Notice)",
        "summary": "A lis pendens is a recorded notice that litigation is pending that affects title to real property. Recording a lis pendens provides constructive notice to all subsequent purchasers and encumbrancers. It creates a cloud on title until the litigation is resolved.",
        "legal_basis": [
            "Texas Property Code Section 12.007",
            "Texas Civil Practice and Remedies Code",
            "Land Title Abstract Co. v. Ameriquest Mortgage Co., 290 S.W.3d 43 (Tex. App. 2008)"
        ],
        "elements": [
            "Must describe the property with reasonable specificity",
            "Must identify the pending litigation (cause number, court, parties)",
            "Provides constructive notice from date of recording",
            "Subsequent purchasers take subject to outcome of litigation",
            "Must be released or expunged when litigation resolves"
        ],
        "texas_application": "In Texas, a lis pendens must be filed in the county where the property is located. It is effective from the date of recording. The chain examiner must check for unreleased lis pendens affecting the property.",
        "chain_impact": "Lis pendens is a critical encumbrance that affects chain marketability. The chain builder must flag any unreleased lis pendens as a major defect. The underlying lawsuit must be reviewed to assess risk to the chain.",
        "related_topics": ["constructive_notice", "encumbrance_tracking", "marketable_title"],
        "exceptions": [
            "Frivolous lis pendens may be expunged by court order"
        ],
        "curative_actions": [
            "Release of lis pendens after litigation resolves",
            "Court order expunging frivolous lis pendens",
            "Obtain dismissal of underlying lawsuit"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "tax_sale_title",
        "category": "SPECIAL_DOCTRINE",
        "title": "Tax Sale and Tax Deed",
        "summary": "When property taxes are delinquent, the taxing authority may sell the property at tax sale. Tax deeds create a new chain starting from the tax sale, but are subject to redemption rights. Tax sales in Texas are governed by the Tax Code and create specific title examination issues.",
        "legal_basis": [
            "Texas Tax Code Section 34.01 et seq.",
            "Texas Tax Code Section 34.21 (right of redemption)",
            "City of Houston v. Texan Land & Cattle Co., 138 Tex. 185 (1942)"
        ],
        "elements": [
            "Delinquent taxes must be properly assessed and noticed",
            "Tax sale must follow statutory procedures",
            "Tax deed conveys all interest of delinquent taxpayer",
            "Right of redemption: 2 years for non-homestead, 2 years for homestead",
            "After redemption period, tax sale becomes final",
            "Tax deed creates new root of title (but subject to prior liens in some cases)"
        ],
        "texas_application": "Texas tax sales are conducted by the county and the purchaser receives a sheriff's or constable's deed. The former owner has a right of redemption for 2 years (or 6 months for certain properties). After the redemption period, the tax deed buyer has clear title. Mineral interests generally survive tax sales.",
        "chain_impact": "Tax deeds can create a parallel chain competing with the original chain. The chain builder must identify tax sale events, determine if the redemption period has passed, and assess whether the tax deed chain supersedes the original chain. Mineral interests are typically NOT affected by tax sales.",
        "related_topics": ["gap_analysis", "sovereign_patent_chain", "mineral_reservation"],
        "exceptions": [
            "Mineral interests generally survive tax sales",
            "Federal tax liens may survive state tax sale",
            "Void tax sale (procedural defects) does not transfer title"
        ],
        "curative_actions": [
            "Quiet title action to confirm tax deed title",
            "Affidavit of non-redemption after redemption period expires"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "curative_doctrine",
        "category": "SPECIAL_DOCTRINE",
        "title": "Curative Instruments and Practices",
        "summary": "Curative instruments are documents filed to correct, clarify, or perfect defects in the chain of title. Common curative instruments include correction deeds, affidavits of identity, affidavits of heirship, ratifications, and stipulations of interest. Proper curative action can transform a defective chain into a marketable chain.",
        "legal_basis": [
            "Texas Property Code various sections",
            "Texas Estates Code Section 203.001",
            "Standard title company requirements"
        ],
        "elements": [
            "Correction deed: fixes errors in prior deed (legal description, names, interests)",
            "Affidavit of heirship: establishes heirs when probate not recorded",
            "Affidavit of identity: confirms that different names refer to same person",
            "Ratification: confirms or validates a prior conveyance",
            "Stipulation of interest: parties agree on ownership percentages",
            "Quitclaim deed: releases claims to cure chain breaks",
            "Court order: judicial determination of ownership or title"
        ],
        "texas_application": "In Texas oil and gas title, curative is a critical part of the title examination process. The landman identifies defects and the attorney prescribes curative requirements. The most common curatives are: affidavit of heirship (for death gaps), correction deed (for description errors), and quitclaim deed (for chain breaks). A curative list is a standard part of every title opinion.",
        "chain_impact": "Curative instruments bridge gaps, correct errors, and strengthen weak links. The chain builder must recognize curative instruments and apply their corrections to the chain. A gap with an appropriate curative instrument is no longer a defect.",
        "related_topics": ["gap_analysis", "heirship_gap", "name_variance", "marketable_title"],
        "exceptions": [],
        "curative_actions": [],
        "risk_level": "LOW"
    },
    {
        "topic": "relinquishment_act",
        "category": "SPECIAL_DOCTRINE",
        "title": "Texas Relinquishment Act",
        "summary": "The Relinquishment Act (1919) applies to school land sections where the State retained minerals but sold the surface. Under this act, the surface owner has the right to lease the minerals with the State receiving a royalty. This creates a unique ownership structure where neither the surface owner nor the State has full mineral ownership.",
        "legal_basis": [
            "Texas Natural Resources Code Sections 52.171-52.182",
            "Greene v. Robison, 117 Tex. 516 (1928)",
            "Lemar v. Garner, 121 Tex. 502 (1932)"
        ],
        "elements": [
            "Applies to PSF school land sections",
            "Surface owner has leasing rights (not mineral ownership)",
            "State retains mineral ownership",
            "State receives royalty (typically 1/16 to 1/8)",
            "Surface owner receives bonus and delay rentals",
            "Does not apply to university land or asylum land"
        ],
        "texas_application": "In the Permian Basin, many sections are school land subject to the Relinquishment Act. The chain examiner must identify school land sections and apply the Relinquishment Act framework. The mineral chain is fundamentally different - the State owns the minerals, and the surface owner has a statutory right to lease them.",
        "chain_impact": "Relinquishment Act sections require dual chain analysis: surface chain from State patent and mineral chain showing State ownership with surface owner leasing rights. The chain builder must identify these sections and apply the correct framework.",
        "related_topics": ["school_land_psf", "sovereign_patent_chain", "mineral_reservation"],
        "exceptions": [
            "Does not apply to university land",
            "Does not apply to asylum land or penitentiary land"
        ],
        "curative_actions": [
            "Verify school land status through GLO",
            "Confirm surface owner has proper chain to exercise leasing rights"
        ],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "intestate_succession",
        "category": "SPECIAL_DOCTRINE",
        "title": "Intestate Succession (Texas)",
        "summary": "When a person dies without a will (intestate), property passes to heirs according to the Texas Estates Code descent and distribution rules. Community property passes differently than separate property. The chain must trace through the statutory heirs at each death.",
        "legal_basis": [
            "Texas Estates Code Sections 201.001-201.101",
            "Texas Estates Code Section 201.003 (separate property)",
            "Texas Estates Code Section 201.002 (community property)"
        ],
        "elements": [
            "Community property: surviving spouse inherits all if all children are also children of surviving spouse",
            "Community property: otherwise, children inherit deceased spouse's share",
            "Separate personal property: surviving spouse gets 1/3, children get 2/3",
            "Separate real property: surviving spouse gets life estate in 1/3, children get remainder and 2/3 fee",
            "No surviving spouse: children inherit equally per stirpes",
            "No children: parents, siblings, etc. in statutory order"
        ],
        "texas_application": "Texas intestate succession rules determine the heirs at each death event in the chain. Community property rules are critical because Texas is a community property state. All property acquired during marriage is presumed community unless proven separate. The chain builder must determine whether each death involved community or separate property and apply the correct distribution rules.",
        "chain_impact": "Intestate succession is the primary mechanism for chain branching. Each death event potentially splits the chain into multiple branches (one per heir). The chain builder must correctly identify heirs and calculate their fractional interests based on the descent and distribution rules.",
        "related_topics": ["heirship_gap", "fractional_interest_tracking", "community_property"],
        "exceptions": [
            "Will overrides intestate succession (mostly)",
            "Homestead exemption may affect distribution",
            "Pre-1993 rules differ from post-1993 rules"
        ],
        "curative_actions": [
            "Affidavit of heirship identifying all heirs",
            "Court-determined heirship proceeding",
            "Probate of will if found"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "community_property",
        "category": "SPECIAL_DOCTRINE",
        "title": "Community Property Rules (Texas)",
        "summary": "Texas is a community property state. All property acquired during marriage is presumed to be community property, owned equally by both spouses. This affects chain of title because both spouses must join in conveyances of community property, and death of one spouse affects the other's interest.",
        "legal_basis": [
            "Texas Family Code Section 3.002",
            "Texas Family Code Section 3.003",
            "Texas Constitution Art. XVI, Section 15"
        ],
        "elements": [
            "Community property: property acquired during marriage",
            "Separate property: property owned before marriage or acquired by gift/inheritance",
            "Both spouses must join in community property conveyance",
            "Surviving spouse owns 1/2 of community property outright",
            "Deceased spouse's 1/2 passes to heirs or devisees",
            "Homestead requires joinder even if separate property"
        ],
        "texas_application": "In Texas, community property rules mean that both spouses must sign conveyances of community property. Missing spousal joinder is a common title defect. The chain examiner must identify all conveyances during marriage and verify joinder. For mineral interests acquired during marriage, both spouses have a community property interest.",
        "chain_impact": "Community property creates mandatory joinder requirements. The chain builder must identify married owners and verify spousal joinder in all conveyances during marriage. Missing joinder creates a defect that may or may not be cured by the passage of time.",
        "related_topics": ["intestate_succession", "heirship_gap", "link_validation"],
        "exceptions": [
            "Separate property does not require joinder (except homestead)",
            "Partition agreement can convert community to separate"
        ],
        "curative_actions": [
            "Obtain ratification from non-signing spouse",
            "Quitclaim deed from non-signing spouse or heirs",
            "Affidavit of separate property if applicable"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "executive_right",
        "category": "SPECIAL_DOCTRINE",
        "title": "Executive Right (Texas Mineral Law)",
        "summary": "The executive right is the power to lease the mineral estate for oil and gas development. In Texas, the executive right is severable from the mineral estate and can be conveyed separately. The holder of the executive right has a fiduciary duty to non-executive mineral owners.",
        "legal_basis": [
            "Lesley v. Veterans Land Board, 352 S.W.3d 479 (Tex. 2011)",
            "KCM Financial LLC v. Bradshaw, 457 S.W.3d 70 (Tex. 2015)",
            "Hlavinka v. Hancock, 116 S.W.3d 412 (Tex. App. 2003)"
        ],
        "elements": [
            "Executive right controls who can lease the minerals",
            "Severable from mineral ownership in Texas",
            "Executive owes fiduciary duty to non-executive mineral owners",
            "Must lease on commercially reasonable terms",
            "Cannot engage in self-dealing at expense of non-executive",
            "Non-executive mineral owner receives royalty but cannot lease"
        ],
        "texas_application": "In the Permian Basin, executive rights are frequently severed from mineral interests, especially in large family trusts and estate plans. The chain examiner must track executive rights separately from mineral ownership. A non-executive mineral owner cannot independently lease their minerals.",
        "chain_impact": "Executive right tracking adds another layer to the chain. The chain builder must maintain separate tracking for mineral ownership and executive right. Both must be traced through the chain to determine current ownership.",
        "related_topics": ["mineral_reservation", "fractional_interest_tracking"],
        "exceptions": [
            "Non-executive can sue executive for breach of fiduciary duty"
        ],
        "curative_actions": [
            "Stipulation of interest clarifying executive right ownership"
        ],
        "risk_level": "MEDIUM"
    },

    # ==================== RECORDING AND VALIDATION DOCTRINES ====================
    {
        "topic": "acknowledgment_requirements",
        "category": "RECORDING_VALIDATION",
        "title": "Acknowledgment and Notarization Requirements",
        "summary": "For an instrument to be eligible for recording in Texas, it must be acknowledged before a notary public or other authorized officer. Defective acknowledgment may prevent recording or may fail to provide constructive notice even if recorded.",
        "legal_basis": [
            "Texas Civil Practice and Remedies Code Section 121.001",
            "Texas Government Code Section 406",
            "Texas Property Code Section 12.001"
        ],
        "elements": [
            "Signer must personally appear before notary",
            "Notary must verify identity of signer",
            "Acknowledgment must be in substantially correct form",
            "Notary seal required in Texas",
            "Commission must be current at time of acknowledgment",
            "Venue (state and county) must be stated",
            "Date of acknowledgment must be stated"
        ],
        "texas_application": "In Texas, a defective acknowledgment may render an instrument unrecordable, or if recorded, may not provide constructive notice. The examiner must verify that each instrument in the chain has a proper acknowledgment. Foreign acknowledgments (out of state or country) have additional requirements.",
        "chain_impact": "Instruments with defective acknowledgments create weaker chain links. The chain builder should flag any instruments with missing or defective acknowledgments and assess the impact on constructive notice.",
        "related_topics": ["constructive_notice", "link_validation", "delivery_requirements"],
        "exceptions": [
            "Instruments valid between parties even without acknowledgment",
            "Old instruments may have different acknowledgment standards"
        ],
        "curative_actions": [
            "Re-execute with proper acknowledgment and re-record",
            "File affidavit confirming execution and acknowledgment",
            "Court order validating instrument"
        ],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "delivery_requirements",
        "category": "RECORDING_VALIDATION",
        "title": "Deed Delivery Requirements",
        "summary": "A deed is not effective until it is delivered to the grantee with intent to convey. Delivery is presumed if the deed is recorded or acknowledged, but this presumption can be rebutted. Death of the grantor before delivery renders the deed void.",
        "legal_basis": [
            "Steffian v. Milmo Nat'l Bank, 69 Tex. 513 (1888)",
            "Ragland v. Kelner, 148 Tex. 132 (1949)",
            "Common law of deed delivery"
        ],
        "elements": [
            "Physical transfer of deed to grantee or grantee's agent",
            "Intent to convey present interest (not future)",
            "Acceptance by grantee (presumed if beneficial)",
            "Recording creates rebuttable presumption of delivery",
            "Acknowledgment creates rebuttable presumption of delivery",
            "Conditional delivery to escrow agent is valid",
            "Death before delivery voids the deed"
        ],
        "texas_application": "In Texas, delivery is generally presumed when an instrument is recorded. The examiner need not investigate delivery unless there are facts suggesting non-delivery (e.g., deed found in grantor's safe deposit box, deed not recorded until after grantor's death).",
        "chain_impact": "Delivery issues are rare but when they occur, they can void an entire chain link. The chain builder should check for suspicious patterns such as recording dates significantly after the grantor's death.",
        "related_topics": ["acknowledgment_requirements", "link_validation"],
        "exceptions": [
            "Delivery in escrow is effective when conditions met",
            "Transfer on death deed (Texas Estates Code) is not delivered until death"
        ],
        "curative_actions": [
            "Affidavit of delivery by witnesses",
            "Court order establishing delivery"
        ],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "legal_description_matching",
        "category": "RECORDING_VALIDATION",
        "title": "Legal Description Matching and Validation",
        "summary": "Every instrument in the chain must contain a legal description sufficient to identify the property. Legal descriptions must be consistent throughout the chain. Variations, ambiguities, or errors in legal descriptions create title defects. The examiner must verify that each instrument describes the same parcel.",
        "legal_basis": [
            "Texas property description law",
            "Gates v. Asher, 154 Tex. 538 (1955)",
            "AIC Mgmt. v. Crews, 246 S.W.3d 640 (Tex. 2008)"
        ],
        "elements": [
            "Abstract/survey/block identification must match",
            "Section number must be consistent",
            "Acreage should be consistent (within survey error tolerance)",
            "Metes and bounds must describe same tract",
            "Lot/block/subdivision must match for platted land",
            "Scrivener's errors in description are correctable",
            "Ambiguous descriptions may require construction"
        ],
        "texas_application": "In Texas, legal descriptions in the Permian Basin follow the abstract/survey system. The examiner must normalize legal descriptions to match instruments across the chain. Common variations include: different abbreviations (Sec. vs Section), minor acreage differences, and different surveyor references.",
        "chain_impact": "Legal description matching is essential for chain construction. The chain builder must parse and normalize legal descriptions, match them across instruments, and flag any inconsistencies. A significant description change mid-chain may indicate the instruments describe different parcels.",
        "related_topics": ["abstract_survey_system", "chain_of_title_search"],
        "exceptions": [
            "Scrivener's errors correctable by correction deed",
            "Patent description controls over later variations"
        ],
        "curative_actions": [
            "Correction deed to fix description errors",
            "Survey to resolve ambiguous descriptions",
            "Court order to reform deed"
        ],
        "risk_level": "HIGH"
    },
    {
        "topic": "recording_delay_analysis",
        "category": "RECORDING_VALIDATION",
        "title": "Recording Delay Analysis",
        "summary": "The gap between execution date and recording date of an instrument can provide important clues about the chain. A significant delay may indicate intervening transactions, disputes, or escrow arrangements. Very old unrecorded instruments may surface and complicate the chain.",
        "legal_basis": [
            "Texas recording act principles",
            "Title examination practices"
        ],
        "elements": [
            "Normal delay: days to weeks (typical title company recording)",
            "Moderate delay: months (acceptable, may indicate escrow)",
            "Significant delay: years (investigate reason)",
            "Extreme delay: decades (highly suspicious, may be invalid)",
            "Intervening instruments during delay period affect priority",
            "Recording date controls constructive notice, not execution date"
        ],
        "texas_application": "In Texas, the recording date determines priority, not the execution date. An instrument executed first but recorded second loses to a subsequent BFP who records first. The chain builder must track both execution and recording dates to identify potential priority disputes.",
        "chain_impact": "Recording delays may create priority disputes between competing claims. The chain builder must flag significant recording delays and assess whether intervening instruments may have gained priority during the delay period.",
        "related_topics": ["texas_race_notice_recording_act", "bona_fide_purchaser", "gap_analysis"],
        "exceptions": [
            "Recording delay does not affect validity between the parties"
        ],
        "curative_actions": [
            "Title insurance may insure over recording delays",
            "Affidavit explaining the delay"
        ],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "branch_handling",
        "category": "CHAIN_CONSTRUCTION",
        "title": "Branch Handling in Chain Construction",
        "summary": "Chain branches occur when a single owner conveys to multiple grantees, when property passes to multiple heirs, or when interests are fractionally divided. Each branch represents a separate sub-chain that must be tracked independently. Branches may later merge when fractional interests are reconveyed to a single owner.",
        "legal_basis": [
            "Standard chain construction methodology",
            "Fractional conveyance principles"
        ],
        "elements": [
            "Split events: heirship, fractional conveyances, partitions",
            "Each branch tracks its own fraction of the whole",
            "Branches may further subdivide (sub-branches)",
            "Merger events: when fractional interests reconsolidate",
            "All branches must sum to 100% at every point",
            "Branch confidence inherits from parent link"
        ],
        "texas_application": "In the Permian Basin, chain branching is pervasive due to generations of mineral interest subdivisions through heirship. A single section may have 50+ mineral owners across dozens of branches. The chain builder must handle unlimited branching depth and maintain accurate fractional totals.",
        "chain_impact": "Branching is the primary complexity driver in chain construction. The chain builder must efficiently handle branch creation, tracking, and merger while maintaining fractional accuracy to the configured precision.",
        "related_topics": ["fractional_interest_tracking", "heirship_gap", "merger_detection"],
        "exceptions": [],
        "curative_actions": [],
        "risk_level": "MEDIUM"
    },
    {
        "topic": "merger_detection",
        "category": "CHAIN_CONSTRUCTION",
        "title": "Interest Merger Detection",
        "summary": "Merger occurs when fractional interests that were previously divided are reconveyed to a single owner. This simplifies the chain by reducing the number of active branches. Merger detection is important for accurate current ownership calculation and chain simplification.",
        "legal_basis": [
            "Common law merger doctrine",
            "Title calculation principles"
        ],
        "elements": [
            "Multiple fractional interests conveyed to same grantee",
            "Grantee's total interest increases (fractions add)",
            "Full merger: all fractions reconsolidate to 100%",
            "Partial merger: some fractions reconsolidate",
            "Merger simplifies forward chain (fewer branches)",
            "Must verify all fractions are properly summed"
        ],
        "texas_application": "In West Texas, oil companies frequently acquire fractional mineral interests from multiple owners to consolidate a working interest position. This creates merger events that simplify the chain. The chain builder must detect when a grantee already owns other fractions and add the new acquisition to the existing total.",
        "chain_impact": "Merger reduces chain complexity by consolidating branches. The chain builder must detect merger opportunities, combine fractional interests, and prune merged branches from the active chain.",
        "related_topics": ["branch_handling", "fractional_interest_tracking"],
        "exceptions": [
            "Interests of different types do not merge (mineral vs royalty)",
            "Trust interests may not merge with individual interests"
        ],
        "curative_actions": [],
        "risk_level": "LOW"
    },
]


# ---------------------------------------------------------------------------
# Doctrine cache manager
# ---------------------------------------------------------------------------

class ChainOfTitleDoctrineCache:
    """Manages the chain of title doctrine knowledge base.

    Provides fast lookup by topic and category, full-text search across
    doctrine content, and deterministic hashing for cache validation.
    """

    def __init__(self) -> None:
        self._doctrines: Dict[str, DoctrineBlock] = {}
        self._by_category: Dict[str, List[str]] = {}
        self._related_index: Dict[str, List[str]] = {}
        self._stats: DoctrineCacheStats = DoctrineCacheStats()
        self._loaded: bool = False
        logger.info("ChainOfTitleDoctrineCache initialized")

    # -- loading --

    def load(self) -> DoctrineCacheStats:
        """Load all chain of title doctrines into the cache."""
        import time
        start = time.perf_counter()

        self._doctrines.clear()
        self._by_category.clear()
        self._related_index.clear()

        for raw in CHAIN_OF_TITLE_DOCTRINES:
            block = DoctrineBlock(**raw)
            self._doctrines[block.topic] = block

            cat = block.category
            if cat not in self._by_category:
                self._by_category[cat] = []
            self._by_category[cat].append(block.topic)

            for related in block.related_topics:
                if related not in self._related_index:
                    self._related_index[related] = []
                self._related_index[related].append(block.topic)

        elapsed_ms = (time.perf_counter() - start) * 1000
        category_counts = {cat: len(topics) for cat, topics in self._by_category.items()}

        self._stats = DoctrineCacheStats(
            total_doctrines=len(self._doctrines),
            categories=category_counts,
            last_loaded=datetime.now(timezone.utc).isoformat(),
            cache_hash=self._compute_hash(),
            load_time_ms=round(elapsed_ms, 2),
        )
        self._loaded = True

        logger.info(
            f"Loaded {self._stats.total_doctrines} chain-of-title doctrines "
            f"across {len(category_counts)} categories in {elapsed_ms:.1f}ms"
        )
        return self._stats

    # -- queries --

    def get(self, topic: str) -> Optional[DoctrineBlock]:
        """Retrieve a doctrine by topic identifier."""
        self._ensure_loaded()
        return self._doctrines.get(topic)

    def get_by_category(self, category: str) -> List[DoctrineBlock]:
        """Retrieve all doctrines in a given category."""
        self._ensure_loaded()
        topics = self._by_category.get(category, [])
        return [self._doctrines[t] for t in topics if t in self._doctrines]

    def get_related(self, topic: str) -> List[DoctrineBlock]:
        """Retrieve doctrines related to the given topic."""
        self._ensure_loaded()
        block = self._doctrines.get(topic)
        if not block:
            return []

        related_topics: set[str] = set(block.related_topics)
        referencing = self._related_index.get(topic, [])
        related_topics.update(referencing)
        related_topics.discard(topic)

        return [self._doctrines[t] for t in related_topics if t in self._doctrines]

    def search(self, query: str, max_results: int = 20) -> List[DoctrineBlock]:
        """Full-text search across all doctrine content."""
        self._ensure_loaded()
        query_lower = query.lower()
        scored: List[tuple[float, str]] = []

        for topic, block in self._doctrines.items():
            score = 0.0
            searchable = (
                f"{block.title} {block.summary} {block.texas_application} "
                f"{block.chain_impact} {' '.join(block.elements)} "
                f"{' '.join(block.legal_basis)} {' '.join(block.exceptions)} "
                f"{' '.join(block.curative_actions)}"
            ).lower()

            terms = query_lower.split()
            for term in terms:
                count = searchable.count(term)
                if count > 0:
                    score += count * 1.0
                    if term in block.title.lower():
                        score += 5.0
                    if term in block.topic.lower():
                        score += 3.0

            if score > 0:
                scored.append((score, topic))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [self._doctrines[t] for _, t in scored[:max_results]]

    def get_by_risk_level(self, risk_level: str) -> List[DoctrineBlock]:
        """Retrieve all doctrines at a given risk level."""
        self._ensure_loaded()
        return [b for b in self._doctrines.values() if b.risk_level == risk_level.upper()]

    def get_curative_for_issue(self, issue_type: str) -> List[DoctrineBlock]:
        """Find doctrines with curative actions relevant to an issue type."""
        self._ensure_loaded()
        issue_lower = issue_type.lower().replace("_", " ")
        results: List[DoctrineBlock] = []

        for block in self._doctrines.values():
            if not block.curative_actions:
                continue
            searchable = (
                f"{block.topic} {block.title} {block.summary} "
                f"{' '.join(block.curative_actions)}"
            ).lower()
            if issue_lower in searchable or any(
                term in searchable for term in issue_lower.split()
            ):
                results.append(block)

        return results

    def list_categories(self) -> Dict[str, int]:
        """List all doctrine categories and their counts."""
        self._ensure_loaded()
        return {cat: len(topics) for cat, topics in self._by_category.items()}

    def list_topics(self) -> List[str]:
        """List all doctrine topic identifiers."""
        self._ensure_loaded()
        return list(self._doctrines.keys())

    def get_stats(self) -> DoctrineCacheStats:
        """Return cache statistics."""
        return self._stats

    def to_dict(self) -> Dict[str, Any]:
        """Export entire cache as a dictionary."""
        self._ensure_loaded()
        return {
            "stats": self._stats.model_dump(),
            "doctrines": {t: b.model_dump() for t, b in self._doctrines.items()},
            "categories": dict(self._by_category),
        }

    def export_json(self, path: Path) -> int:
        """Export doctrine cache to a JSON file. Returns bytes written."""
        data = self.to_dict()
        text = json.dumps(data, indent=2, default=str)
        path.write_text(text, encoding="utf-8")
        logger.info(f"Exported {len(self._doctrines)} doctrines to {path}")
        return len(text)

    # -- internals --

    def _ensure_loaded(self) -> None:
        """Load doctrines if not already loaded."""
        if not self._loaded:
            self.load()

    def _compute_hash(self) -> str:
        """Deterministic hash of all doctrine content."""
        hasher = hashlib.sha256()
        for topic in sorted(self._doctrines.keys()):
            block = self._doctrines[topic]
            hasher.update(block.model_dump_json().encode("utf-8"))
        return hasher.hexdigest()
