"""
LM21 Federal/State Lands Engine - Doctrine Cache Module
=========================================================
Pre-compiled expert reasoning blocks for federal and state land
oil & gas leasing, permitting, royalty compliance, environmental
review, and surface management.

Each DoctrineBlock contains real domain expertise distilled into
structured reasoning frameworks with authorities, counter-arguments,
and resolution strategies.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel, Field


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class EntityScope(str, Enum):
    FEDERAL = "FEDERAL"
    STATE_TX = "STATE_TX"
    STATE_NM = "STATE_NM"
    STATE_GENERAL = "STATE_GENERAL"
    SPLIT_ESTATE = "SPLIT_ESTATE"
    TRIBAL = "TRIBAL"
    MULTI_JURISDICTION = "MULTI_JURISDICTION"


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str] = Field(min_length=5)
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str] = Field(min_length=5)
    primary_authority: List[str] = Field(min_length=3)
    burden_holder: str = ""
    adversary_position: str = ""
    counter_arguments: List[str] = Field(min_length=3)
    resolution_strategy: str = ""
    entity_scope: EntityScope = EntityScope.FEDERAL
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    controlling_precedent: str = ""
    category: str = ""


def build_doctrine_cache() -> Dict[str, DoctrineBlock]:
    cache: Dict[str, DoctrineBlock] = {}
    blocks = _all_blocks()
    for b in blocks:
        cache[b.topic] = b
    logger.info(f"Doctrine cache built | blocks={len(cache)}")
    return cache


def _all_blocks() -> List[DoctrineBlock]:
    return [
        _blm_competitive_leasing(),
        _blm_noncompetitive_leasing(),
        _federal_lease_primary_term(),
        _federal_royalty_rate(),
        _federal_rental_obligations(),
        _ira_2022_fee_changes(),
        _federal_unit_agreements(),
        _participating_area_designation(),
        _communitization_agreements(),
        _federal_lease_assignment(),
        _operating_rights_transfer(),
        _suspension_of_operations(),
        _apd_process(),
        _surface_use_plan(),
        _nepa_environmental_assessment(),
        _nepa_eis_process(),
        _categorical_exclusion(),
        _esa_section7_consultation(),
        _section106_nhpa(),
        _split_estate_surface_rights(),
        _national_forest_consent(),
        _onrr_royalty_reporting(),
        _onrr_product_valuation(),
        _federal_bonding_requirements(),
        _idle_well_regulations(),
        _texas_glo_leasing(),
        _texas_relinquishment_act(),
        _texas_university_lands(),
        _texas_school_lands(),
        _nm_state_land_leasing(),
        _federal_lease_reinstatement(),
        _federal_lease_renewal(),
        _blm_protest_and_appeal(),
        _ibla_appeals_process(),
        _federal_right_of_way(),
        _resource_management_plan(),
        _methane_waste_prevention(),
        _federal_inspection_enforcement(),
        _tribal_mineral_leasing(),
        _allotted_tribal_lands(),
        _state_mineral_classification(),
        _orphan_well_program(),
    ]


def _blm_competitive_leasing() -> DoctrineBlock:
    return DoctrineBlock(
        topic="blm_competitive_leasing",
        keywords=["competitive", "lease sale", "BLM", "nomination", "sealed bid", "oral auction", "expression of interest"],
        conclusion_template=(
            "BLM competitive lease sales under 43 CFR 3120 require parcels to be nominated through Expressions of Interest (EOI), "
            "reviewed under NEPA, and offered at oral or internet-based auction with a minimum bid. Post-IRA 2022, the minimum "
            "bid is $10/acre, the minimum rental is $3/acre for years 1-2 and $5/acre thereafter, and the royalty floor is 16.67%."
        ),
        reasoning_framework=(
            "Step 1: Determine if lands are available for leasing under the current RMP. "
            "Step 2: Confirm EOI was filed and BLM accepted the nomination. "
            "Step 3: Verify NEPA review is complete (EA/EIS/CX) for the sale parcel. "
            "Step 4: Check if any protests were filed and resolved before sale. "
            "Step 5: Confirm sale was conducted per 43 CFR 3120 procedures. "
            "Step 6: Apply IRA 2022 minimum bid ($10/acre), rental ($3/$5), and royalty (16.67%) floors. "
            "Step 7: Verify the high bidder paid the first year rental + bonus bid within required timeframe. "
            "Step 8: Lease issued for 10-year primary term."
        ),
        key_factors=[
            "EOI filing and BLM acceptance",
            "NEPA compliance for sale parcel",
            "Protest resolution before sale",
            "Minimum bid per acre (post-IRA: $10)",
            "Rental rates (post-IRA: $3/yr 1-2, $5/yr 3+)",
            "Royalty rate floor (post-IRA: 16.67%)",
            "Payment of bonus bid and first year rental",
            "10-year primary term",
        ],
        primary_authority=[
            "30 USC 226 (MLA Sec 17 - Competitive Leasing)",
            "43 CFR 3120 (Competitive Lease Sales)",
            "Inflation Reduction Act of 2022, Sec 50265",
            "BLM Instruction Memorandum 2023-007",
        ],
        burden_holder="BLM (compliance with sale procedures); Lessee (payment obligations)",
        adversary_position="Environmental groups may protest lease sales arguing inadequate NEPA review or RMP inconsistency.",
        counter_arguments=[
            "BLM has discretion to defer or withdraw parcels even after nomination",
            "Pre-sale NEPA does not immunize APD-stage review requirements",
            "IRA 2022 fiscal terms cannot be negotiated below statutory floors",
            "Protests must be filed within 30 days of sale notice per 43 CFR 3120.1-3",
            "IBLA may stay lease issuance pending appeal resolution",
        ],
        resolution_strategy=(
            "Confirm procedural compliance at each step. If protest filed, evaluate grounds under 43 CFR 3120.1-3. "
            "Ensure IRA fiscal terms applied. Document NEPA record of decision or FONSI."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Center for Biological Diversity v. BLM, IBLA 2019-0054 (NEPA adequacy for lease sales)",
        category="leasing",
    )


def _blm_noncompetitive_leasing() -> DoctrineBlock:
    return DoctrineBlock(
        topic="blm_noncompetitive_leasing",
        keywords=["noncompetitive", "over the counter", "post-sale", "OTC", "filing", "offer to lease", "noncomp"],
        conclusion_template=(
            "Under pre-IRA law, parcels that received no bids at competitive sale could be leased noncompetitively for 2 years "
            "after the sale. The IRA 2022 eliminated noncompetitive leasing for new offers filed after August 16, 2022. "
            "Existing noncompetitive leases remain valid through their primary terms."
        ),
        reasoning_framework=(
            "Step 1: Determine if the offer was filed before or after August 16, 2022. "
            "Step 2: If pre-IRA, verify parcel was offered at competitive sale and received no bids. "
            "Step 3: Confirm offer was filed within 2-year window per former 43 CFR 3110. "
            "Step 4: If post-IRA, noncompetitive leasing is no longer available. "
            "Step 5: Existing noncompetitive leases continue under original terms. "
            "Step 6: For post-IRA, the parcel must be re-nominated and offered competitively."
        ),
        key_factors=[
            "Date of noncompetitive offer filing",
            "IRA 2022 effective date (August 16, 2022)",
            "Whether parcel received no bids at prior sale",
            "2-year filing window from original sale date",
            "Grandfathering of existing noncompetitive leases",
            "No new noncompetitive offers accepted post-IRA",
        ],
        primary_authority=[
            "Former 43 CFR 3110 (Noncompetitive Leasing, pre-IRA)",
            "Inflation Reduction Act of 2022, Sec 50264",
            "30 USC 226(c) as amended by IRA",
            "BLM Instruction Memorandum 2022-054",
        ],
        burden_holder="Applicant (timely filing); BLM (processing existing applications)",
        adversary_position="Industry may argue existing applications in pipeline should be honored despite IRA changes.",
        counter_arguments=[
            "IRA statutory language is unambiguous: no new noncompetitive leasing",
            "Applications pending as of IRA enactment may have transitional treatment",
            "BLM retains discretion on processing timeline for grandfathered applications",
        ],
        resolution_strategy=(
            "Check filing date against IRA effective date. Pre-IRA filings in pipeline may proceed. "
            "Post-IRA, redirect to competitive nomination process."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="BLM IM 2022-054 (implementation of IRA leasing provisions)",
        category="leasing",
    )


def _federal_lease_primary_term() -> DoctrineBlock:
    return DoctrineBlock(
        topic="federal_lease_primary_term",
        keywords=["primary term", "ten year", "10 year", "lease term", "lease duration", "expiration", "extension"],
        conclusion_template=(
            "Federal onshore oil and gas leases carry a 10-year primary term under 30 USC 226(e). The lease extends beyond "
            "the primary term as long as oil or gas is produced in paying quantities, or upon approved suspension, or where "
            "a well capable of production exists. The IRA 2022 did not change the 10-year primary term."
        ),
        reasoning_framework=(
            "Step 1: Confirm lease issue date and calculate 10-year primary term expiration. "
            "Step 2: Determine if production in paying quantities exists before expiration. "
            "Step 3: If no production, check for well capable of production in paying quantities. "
            "Step 4: Check for approved SOP extending the lease. "
            "Step 5: Check for unit commitment extending the lease. "
            "Step 6: If none apply, lease terminates by operation of law at end of primary term. "
            "Step 7: Untimely rental payments can cause automatic termination under 30 USC 188."
        ),
        key_factors=[
            "Lease issue date and 10-year calculation",
            "Production in paying quantities at expiration",
            "Well capable of production",
            "Approved suspension of operations or production",
            "Unit commitment and participating area status",
            "Timely rental payments throughout primary term",
            "No partial extensions - entire lease or nothing",
        ],
        primary_authority=[
            "30 USC 226(e) (Lease term and extension)",
            "30 USC 226(i) (Production requirement)",
            "43 CFR 3107 (Continuation and Extension of Leases)",
            "43 CFR 3107.2 (Production in paying quantities)",
        ],
        burden_holder="Lessee (demonstrating production or extension basis)",
        adversary_position="BLM may contend that marginal production does not constitute 'paying quantities' sufficient to extend the lease.",
        counter_arguments=[
            "Paying quantities test is whether a prudent operator would continue to operate",
            "Temporary cessation doctrine allows brief production interruptions",
            "Unit operations on committed lands satisfy the production requirement",
            "SOP must be applied for before lease expiration to preserve rights",
            "BLM cannot retroactively revoke lease extension based on later production decline",
        ],
        resolution_strategy=(
            "Calculate expiration date precisely. Verify production records or approved SOP. "
            "If marginal, apply prudent operator standard from Continental Resources v. BLM."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Continental Resources v. BLM, IBLA 2012-238 (paying quantities standard)",
        category="lease_terms",
    )


def _federal_royalty_rate() -> DoctrineBlock:
    return DoctrineBlock(
        topic="federal_royalty_rate",
        keywords=["royalty rate", "royalty", "12.5%", "16.67%", "one-sixth", "one-eighth", "IRA royalty"],
        conclusion_template=(
            "Pre-IRA leases carry a 12.5% (1/8) royalty rate. Post-IRA leases issued after August 16, 2022 carry a "
            "minimum 16.67% (1/6) royalty rate that cannot be reduced below that floor. BLM may set higher rates. "
            "The royalty is owed on all production removed or sold from the lease."
        ),
        reasoning_framework=(
            "Step 1: Determine lease issue date to identify applicable royalty rate. "
            "Step 2: Pre-IRA leases: 12.5% unless lease terms specify higher. "
            "Step 3: Post-IRA leases: minimum 16.67%, BLM may set higher at sale. "
            "Step 4: Royalty computed on gross proceeds or index-based value per 30 CFR 1206. "
            "Step 5: Transportation and processing allowances may reduce royalty value. "
            "Step 6: ONRR administers royalty collection and audit. "
            "Step 7: Royalty relief programs (reduced rates) may apply under 43 CFR 3103.4."
        ),
        key_factors=[
            "Lease issue date (pre or post IRA 2022)",
            "Lease-specific royalty rate terms",
            "Gross proceeds vs index-based valuation",
            "Transportation allowance deductions",
            "Processing allowance deductions",
            "Royalty relief eligibility",
            "ONRR reporting obligations (OGOR-A, OGOR-B)",
        ],
        primary_authority=[
            "30 USC 226(b)(1)(A) (royalty rate)",
            "IRA 2022 Sec 50265 (minimum royalty rate increase)",
            "30 CFR 1206 (Product Valuation)",
            "43 CFR 3103.3 (Royalties)",
        ],
        burden_holder="Lessee/Operator (accurate reporting and payment); ONRR (audit and enforcement)",
        adversary_position="ONRR may argue higher valuation methodology increases royalty obligation; lessee may seek maximum allowances.",
        counter_arguments=[
            "Transportation allowances capped and must be arms-length or ONRR-approved",
            "Processing allowances must reflect actual costs, not transfer pricing",
            "Royalty relief requires affirmative BLM approval per 43 CFR 3103.4",
            "IRA floor cannot be waived by administrative action",
        ],
        resolution_strategy=(
            "Verify lease date for applicable rate. Confirm valuation method (gross proceeds vs index). "
            "Audit allowance deductions against 30 CFR 1206 limits."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Burlington Resources v. ONRR (royalty valuation methodology)",
        category="royalty",
    )


def _federal_rental_obligations() -> DoctrineBlock:
    return DoctrineBlock(
        topic="federal_rental_obligations",
        keywords=["rental", "annual rental", "rental payment", "lease rental", "$1.50", "$2", "$3", "$5"],
        conclusion_template=(
            "Federal lease rentals are due annually on the anniversary of the lease. Pre-IRA rates were $1.50/acre (years 1-5) "
            "and $2/acre (years 6-10). Post-IRA rates are $3/acre (years 1-2) and $5/acre (years 3+). Failure to pay rental "
            "timely results in automatic lease termination under 30 USC 188(b)."
        ),
        reasoning_framework=(
            "Step 1: Determine lease issue date and applicable rental schedule. "
            "Step 2: Calculate acreage for rental computation. "
            "Step 3: Verify payment was received by BLM on or before anniversary date. "
            "Step 4: If payment late, lease terminates automatically by statute. "
            "Step 5: Reinstatement possible under 30 USC 188(d) or (e) if good faith shown. "
            "Step 6: Once production established, royalty replaces rental (no double payment)."
        ),
        key_factors=[
            "Lease anniversary date for rental due date",
            "Pre-IRA vs post-IRA rental rate schedule",
            "Lease acreage for computation",
            "Automatic termination for late payment",
            "Reinstatement eligibility under 30 USC 188",
            "Production substitutes for rental obligation",
        ],
        primary_authority=[
            "30 USC 226(d) (Rental rate)",
            "30 USC 188(b) (Automatic termination for nonpayment)",
            "30 USC 188(d)-(e) (Reinstatement)",
            "IRA 2022 Sec 50265 (rental rate increase)",
        ],
        burden_holder="Lessee (timely payment); BLM (processing reinstatement petitions)",
        adversary_position="BLM may deny reinstatement if lessee cannot demonstrate good faith or justifiable excuse.",
        counter_arguments=[
            "Automatic termination is harsh but statutory - courts uphold strictly",
            "Reinstatement requires showing nonpayment was justified or not due to lack of reasonable diligence",
            "USPS delays may support good faith argument if postmarked timely",
        ],
        resolution_strategy=(
            "Calendar all rental due dates. Pay early. If missed, file reinstatement petition immediately "
            "with documentation of good faith."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Copper Valley Machine Works v. Andrus, 653 F.2d 595 (D.C. Cir. 1981) (automatic termination strict)",
        category="lease_terms",
    )


def _ira_2022_fee_changes() -> DoctrineBlock:
    return DoctrineBlock(
        topic="ira_2022_fee_changes",
        keywords=["IRA", "Inflation Reduction Act", "2022", "reform", "minimum bid", "rental increase", "royalty increase", "methane fee"],
        conclusion_template=(
            "The IRA 2022 fundamentally changed federal onshore leasing economics: minimum bid from $2 to $10/acre, "
            "rental from $1.50/$2 to $3/$5 per acre, royalty floor from 12.5% to 16.67%, new $5/acre EOI fee, "
            "elimination of noncompetitive leasing, and a methane emissions charge. These changes apply to leases "
            "issued after August 16, 2022."
        ),
        reasoning_framework=(
            "Step 1: Identify which IRA provisions apply based on lease issue date. "
            "Step 2: Apply new minimum bid ($10/acre) to competitive sales. "
            "Step 3: Apply new rental schedule ($3 years 1-2, $5 years 3+). "
            "Step 4: Apply 16.67% minimum royalty rate. "
            "Step 5: Note $5/acre EOI nomination fee (nonrefundable). "
            "Step 6: Confirm noncompetitive leasing eliminated. "
            "Step 7: Assess methane emissions charge applicability. "
            "Step 8: Note IRA ties onshore leasing to renewable energy leasing."
        ),
        key_factors=[
            "Effective date: August 16, 2022",
            "Minimum bid: $2 -> $10/acre",
            "Rental: $1.50/$2 -> $3/$5 per acre",
            "Royalty floor: 12.5% -> 16.67%",
            "EOI fee: $5/acre (new)",
            "Noncompetitive leasing: eliminated",
            "Methane emissions charge: phased in",
            "Onshore-renewable leasing linkage",
        ],
        primary_authority=[
            "Inflation Reduction Act of 2022 (PL 117-169), Sec 50261-50265",
            "30 USC 226 as amended",
            "BLM IM 2022-054 (IRA implementation)",
            "BLM IM 2023-007 (lease sale procedures post-IRA)",
        ],
        burden_holder="BLM (implementing new provisions); Lessees (complying with new fiscal terms)",
        adversary_position="Industry argues IRA fiscal terms make marginal federal lands uneconomic; environmental groups argue changes insufficient.",
        counter_arguments=[
            "Statutory floors are mandatory; BLM cannot waive below minimums",
            "Pre-IRA leases are grandfathered at original terms",
            "Methane charge phases in: $900/ton in 2024, $1,200 in 2025, $1,500 in 2026+",
            "Onshore-renewable linkage means no onshore lease sales without prior renewable energy offering",
        ],
        resolution_strategy=(
            "Categorize each lease by issue date. Apply correct fiscal terms. "
            "Model economics under new rates. Track methane charge phase-in."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="IRA statutory text (no case law yet; too recent for appellate review)",
        category="reform",
    )


def _federal_unit_agreements() -> DoctrineBlock:
    return DoctrineBlock(
        topic="federal_unit_agreements",
        keywords=["unit", "unitization", "unit agreement", "exploratory unit", "committed lands", "unit operator"],
        conclusion_template=(
            "Federal unit agreements under 43 CFR 3180 allow consolidation of multiple leases for joint exploration and "
            "development. The unit operator must drill initial obligation wells within contract periods. Uncommitted acreage "
            "contracts automatically at the end of each period. Participating areas are designated around proved productive lands."
        ),
        reasoning_framework=(
            "Step 1: Determine if unitization is required (multiple federal leases, mixed ownership). "
            "Step 2: Prepare unit agreement using BLM Model Unit Agreement. "
            "Step 3: Obtain commitment from working interest and royalty owners (federal + private). "
            "Step 4: Submit unit application to BLM with supporting geological data. "
            "Step 5: BLM approves unit and sets initial drilling obligation and contract periods. "
            "Step 6: Drill obligation wells within contract period or lose uncommitted acreage. "
            "Step 7: Designate participating areas around proved productive acreage. "
            "Step 8: Lease terms extended by unit commitment for committed lands."
        ),
        key_factors=[
            "BLM Model Unit Agreement terms",
            "Commitment percentages by tract",
            "Initial and subsequent obligation wells",
            "Contract period deadlines",
            "Automatic contraction of uncommitted lands",
            "Participating area designation criteria",
            "Production allocation among tracts",
            "Unit operator duties and liabilities",
        ],
        primary_authority=[
            "43 CFR 3180 (Exploratory Unitization Agreements)",
            "30 USC 226(m) (Unitization authorization)",
            "BLM Manual 3180 (Unit Agreements)",
            "Onshore Oil and Gas Order No. 3",
        ],
        burden_holder="Unit operator (drilling obligations, reporting); BLM (approval, PA designation)",
        adversary_position="BLM may terminate unit if operator fails to meet drilling obligations; non-consenting owners may challenge allocation.",
        counter_arguments=[
            "Contraction is automatic unless BLM grants extension for good cause",
            "PA designation requires proof of productivity, not just drilling",
            "Non-federal owners can refuse commitment but lose lease extension benefit",
            "Force majeure may excuse drilling delay but requires BLM approval",
        ],
        resolution_strategy=(
            "Calendar all contract period deadlines. Ensure obligation wells drilled timely. "
            "File PA applications promptly upon establishing production. Monitor contraction dates."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Pan American Petroleum Corp. v. Udall, 352 F.2d 32 (10th Cir. 1965) (unit drilling obligations)",
        category="development",
    )


def _participating_area_designation() -> DoctrineBlock:
    return DoctrineBlock(
        topic="participating_area_designation",
        keywords=["participating area", "PA", "productive acreage", "allocation", "PA revision", "PA expansion"],
        conclusion_template=(
            "A participating area (PA) is the acreage within a federal unit that has been proved productive and is entitled "
            "to share in unit production. PA designation determines royalty allocation among tracts. PAs must be applied for "
            "within 60 days of establishing production and are subject to BLM approval and periodic revision."
        ),
        reasoning_framework=(
            "Step 1: Well completes as productive within unit boundary. "
            "Step 2: Operator files PA application within 60 days per unit agreement. "
            "Step 3: PA boundaries drawn based on geological/engineering data (drainage, reservoir limits). "
            "Step 4: BLM reviews and approves PA with effective date. "
            "Step 5: Production allocated to tracts within PA based on surface acreage or other agreed formula. "
            "Step 6: PA revision required when new wells extend productive area or production declines. "
            "Step 7: Tracts outside PA do not share in production and must meet separate lease obligations."
        ),
        key_factors=[
            "60-day filing deadline from production",
            "Geological basis for PA boundaries",
            "Production allocation formula",
            "PA effective date (relates back to first production)",
            "Revision triggers (new wells, depletion)",
            "Impact on lease rental and royalty obligations",
        ],
        primary_authority=[
            "43 CFR 3186 (Participating Areas)",
            "BLM Model Unit Agreement, Article 11",
            "Onshore Oil and Gas Order No. 3",
        ],
        burden_holder="Operator (timely filing, geological support); BLM (review and approval)",
        adversary_position="Royalty owners outside PA may argue boundaries are drawn too narrowly to exclude their tracts.",
        counter_arguments=[
            "PA must be based on geological evidence, not operator preference",
            "BLM can expand PA if evidence supports larger productive area",
            "Late PA application does not forfeit rights but delays allocation",
        ],
        resolution_strategy=(
            "File PA within 60 days. Support boundaries with well logs, production data, and reservoir analysis. "
            "Anticipate BLM questions on boundary justification."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="BLM Manual 3186 (PA designation criteria and procedures)",
        category="development",
    )


def _communitization_agreements() -> DoctrineBlock:
    return DoctrineBlock(
        topic="communitization_agreements",
        keywords=["communitization", "CA", "spacing", "communitized", "pooling", "drilling unit"],
        conclusion_template=(
            "Communitization agreements (CAs) under 43 CFR 3105.2 pool federal and non-federal lands to form a drilling "
            "and spacing unit where state spacing orders require a larger unit than a single federal lease provides. "
            "Production from the CA is allocated by surface acreage, and operations anywhere on the CA satisfy the "
            "federal lease's production obligation."
        ),
        reasoning_framework=(
            "Step 1: Determine state spacing requirements for the formation. "
            "Step 2: Identify federal and non-federal tracts within the proposed spacing unit. "
            "Step 3: Prepare CA using BLM model form or approved variation. "
            "Step 4: Obtain consent from all working interest and royalty owners. "
            "Step 5: Submit CA to BLM for approval (must be filed before lease expiration). "
            "Step 6: BLM approves CA; production allocated by surface acreage ratio. "
            "Step 7: Operations anywhere on CA satisfy federal lease obligations. "
            "Step 8: CA remains in effect as long as capable of production in paying quantities."
        ),
        key_factors=[
            "State spacing order requirements",
            "Acreage ratio for production allocation",
            "Consent of all interest owners",
            "Filing before federal lease expiration",
            "BLM approval requirement",
            "Effect on lease term extension",
        ],
        primary_authority=[
            "43 CFR 3105.2 (Communitization Agreements)",
            "30 USC 226(m) (Communitization authority)",
            "BLM Form 3105-3 (Application for CA)",
        ],
        burden_holder="Operator (obtaining consents, timely filing); BLM (approval)",
        adversary_position="BLM may reject CA if spacing unit does not conform to state order or if filed after lease expiration.",
        counter_arguments=[
            "CA must be filed before federal lease expiration to preserve lease",
            "State forced pooling does not automatically create federal CA",
            "BLM requires separate CA approval even if state pooling order exists",
        ],
        resolution_strategy=(
            "Verify state spacing requirements. File CA well before lease expiration. "
            "Obtain all necessary consents. Ensure acreage allocation matches plat survey."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texaco Inc., 123 IBLA 379 (1992) (CA filing timing requirements)",
        category="development",
    )


def _federal_lease_assignment() -> DoctrineBlock:
    return DoctrineBlock(
        topic="federal_lease_assignment",
        keywords=["assignment", "transfer", "record title", "sublease", "43 CFR 3106", "lease transfer"],
        conclusion_template=(
            "Federal lease assignments under 43 CFR 3106 require BLM approval and must be filed within 90 days of execution. "
            "Record title transfers convey the full leasehold; operating rights transfers (subleases) convey working interest "
            "only. All transferees must qualify as lessees and post required bonds."
        ),
        reasoning_framework=(
            "Step 1: Determine assignment type (record title vs operating rights). "
            "Step 2: Prepare assignment instrument meeting BLM requirements. "
            "Step 3: File with BLM within 90 days of execution plus $10 filing fee per lease. "
            "Step 4: Transferee must be qualified to hold federal lease (US citizen, corporation). "
            "Step 5: Transferee must have adequate bonding in place. "
            "Step 6: BLM reviews and approves; effective date relates back to execution date. "
            "Step 7: Assignor remains liable for obligations arising before effective date. "
            "Step 8: Partial assignments (aliquot parts) permitted if resulting tracts meet minimum acreage."
        ),
        key_factors=[
            "90-day filing deadline from execution",
            "Record title vs operating rights distinction",
            "Transferee qualification requirements",
            "Bonding requirements for transferee",
            "Partial assignment minimum acreage",
            "Assignor ongoing liability for pre-transfer obligations",
            "Filing fee ($10/lease affected)",
        ],
        primary_authority=[
            "43 CFR 3106 (Assignment and Transfer of Leases)",
            "BLM Form 3106-1 (Transfer of Record Title Interest)",
            "BLM Form 3106-2 (Transfer of Operating Rights)",
            "43 CFR 3106.1 (Filing requirements)",
        ],
        burden_holder="Assignor/Assignee (timely filing, qualification); BLM (approval)",
        adversary_position="BLM may reject assignment if transferee lacks bonding or qualification, or if filed outside 90-day window.",
        counter_arguments=[
            "Late-filed assignments may be accepted with justification but are not guaranteed",
            "Operating rights transferees assume full operator obligations",
            "BLM can refuse partial assignments creating subeconomic tracts",
        ],
        resolution_strategy=(
            "File promptly within 90 days. Ensure transferee bonds in place before filing. "
            "Verify transferee qualification. Include all required forms and fees."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="43 CFR 3106.4 (BLM authority to reject untimely filings)",
        category="leasing",
    )


def _operating_rights_transfer() -> DoctrineBlock:
    return DoctrineBlock(
        topic="operating_rights_transfer",
        keywords=["operating rights", "sublease", "working interest", "operator transfer", "OR transfer"],
        conclusion_template=(
            "Operating rights (working interest) transfers are distinct from record title transfers. The operating rights "
            "owner assumes the obligation to comply with all lease terms, drill, produce, and pay royalties. The record "
            "title owner retains the lease but the operating rights owner is the entity BLM holds responsible for operations."
        ),
        reasoning_framework=(
            "Step 1: Distinguish operating rights transfer from record title transfer. "
            "Step 2: Operating rights owner assumes all operational obligations. "
            "Step 3: Record title owner retains lease but is secondarily liable. "
            "Step 4: Operating rights transferee must qualify and bond separately. "
            "Step 5: BLM correspondence goes to operating rights owner for operational matters. "
            "Step 6: Multiple operating rights owners possible on a single lease (by formation or area). "
            "Step 7: File using BLM Form 3106-2 within 90 days."
        ),
        key_factors=[
            "Operational liability shifts to OR owner",
            "Record title owner retains secondary liability",
            "Separate bonding required for OR owner",
            "Formation or area-specific OR transfers",
            "BLM correspondence routing",
            "Compliance and enforcement directed at OR owner",
        ],
        primary_authority=[
            "43 CFR 3106.1(b) (Operating rights transfer)",
            "BLM Form 3106-2",
            "43 CFR 3162.1 (Operator obligations)",
        ],
        burden_holder="Operating rights transferee (all operational obligations)",
        adversary_position="BLM may pursue both record title and operating rights owners for violations; record title owner cannot fully insulate through OR transfer.",
        counter_arguments=[
            "Record title owner remains secondarily liable for lease obligations",
            "OR transfer does not relieve prior obligations of the assignor",
            "BLM can require additional bonding from OR transferee",
        ],
        resolution_strategy=(
            "Clearly define scope of OR transfer (formation, depth, area). Ensure OR transferee bonds cover full obligations. "
            "Record title owner should monitor compliance to protect lease."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="43 CFR 3162.1 (obligations of operating rights owners)",
        category="leasing",
    )


def _suspension_of_operations() -> DoctrineBlock:
    return DoctrineBlock(
        topic="suspension_of_operations_production",
        keywords=["suspension", "SOP", "SOO", "shut in", "force majeure", "lease suspension", "43 CFR 3103.4"],
        conclusion_template=(
            "Suspensions of operations (SOO) and/or production (SOP) under 43 CFR 3103.4-2 toll the lease term and "
            "relieve rental/royalty obligations during the suspension period. BLM may grant SOP/SOO for conservation, "
            "force majeure, or other justified reasons. Application must be filed before lease expiration."
        ),
        reasoning_framework=(
            "Step 1: Determine grounds for suspension (conservation, force majeure, market conditions). "
            "Step 2: File application with BLM before lease expires. "
            "Step 3: Include geological/engineering justification. "
            "Step 4: BLM evaluates whether suspension serves conservation of resources. "
            "Step 5: If approved, lease term tolled during suspension. "
            "Step 6: Rental and minimum royalty obligations suspended. "
            "Step 7: BLM may impose conditions or time limits on suspension. "
            "Step 8: Operator must resume operations when suspension lifted or lease terminates."
        ),
        key_factors=[
            "Application must precede lease expiration",
            "Conservation or force majeure justification",
            "Lease term tolling during suspension",
            "Relief from rental and royalty during suspension",
            "BLM conditions and time limits",
            "Obligation to resume when suspension ends",
        ],
        primary_authority=[
            "43 CFR 3103.4-2 (Suspension of operations and/or production)",
            "30 USC 209 (Suspension authority)",
            "43 CFR 3165.1 (Relief from operating requirements)",
        ],
        burden_holder="Lessee (demonstrating justification for suspension)",
        adversary_position="BLM may deny suspension if lessee cannot show conservation purpose or genuine force majeure.",
        counter_arguments=[
            "Market conditions alone may not justify SOP without conservation nexus",
            "BLM has discretion to deny - no automatic right to suspension",
            "Expired leases cannot be retroactively suspended",
        ],
        resolution_strategy=(
            "File SOP application well before lease expiration. Document conservation rationale. "
            "Maintain well in safe condition during suspension period."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Harvey E. Yates Co. v. DOI, 819 F.2d 963 (10th Cir. 1987) (suspension discretion)",
        category="lease_terms",
    )


def _apd_process() -> DoctrineBlock:
    return DoctrineBlock(
        topic="apd_process",
        keywords=["APD", "application for permit to drill", "drilling permit", "sundry notice", "BLM permit", "NOS"],
        conclusion_template=(
            "The APD process under 43 CFR 3162.3-1 requires operators to submit a complete application including surface "
            "use plan, drilling plan, and environmental information. BLM must complete NEPA review before approval. "
            "Post-IRA 2022, a $10,000 APD application fee applies. Average processing time is 30-180 days."
        ),
        reasoning_framework=(
            "Step 1: Prepare APD package (Form 3160-3, drilling plan, SUPO, geologic prognosis). "
            "Step 2: Pay $10,000 APD fee (post-IRA). "
            "Step 3: BLM reviews for completeness within 10 business days. "
            "Step 4: If complete, BLM initiates NEPA review (EA/CX). "
            "Step 5: Section 7 ESA consultation if listed species present. "
            "Step 6: Section 106 NHPA review for cultural resources. "
            "Step 7: BLM issues Conditions of Approval (COA) with stipulations. "
            "Step 8: APD approved; operator must commence drilling within 12 months or permit expires. "
            "Step 9: Sundry notices required for any changes to approved plan."
        ),
        key_factors=[
            "$10,000 APD fee (post-IRA 2022)",
            "Completeness review within 10 business days",
            "NEPA compliance required before approval",
            "ESA Section 7 and NHPA Section 106 clearances",
            "Conditions of Approval with stipulations",
            "12-month permit validity",
            "Sundry notice for plan modifications",
        ],
        primary_authority=[
            "43 CFR 3162.3-1 (Drilling plans and operations)",
            "BLM Form 3160-3 (APD Application)",
            "Onshore Oil and Gas Order No. 1 (APD requirements)",
            "IRA 2022 Sec 50262 (APD fee)",
        ],
        burden_holder="Operator (complete application, COA compliance); BLM (timely processing)",
        adversary_position="Environmental groups may challenge APD approval arguing inadequate NEPA review at site-specific level.",
        counter_arguments=[
            "Site-specific NEPA may tier from existing RMP EIS",
            "Categorical exclusions available for certain infill wells",
            "BLM has 30-day target for CX completions",
            "APD fee is nonrefundable even if application denied",
        ],
        resolution_strategy=(
            "Submit complete APD package to avoid rejection. Coordinate with BLM before filing on ESA/NHPA concerns. "
            "Budget $10,000 fee per APD. Track 12-month drilling deadline."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Onshore Oil and Gas Order No. 1 (comprehensive APD requirements)",
        category="permitting",
    )


def _surface_use_plan() -> DoctrineBlock:
    return DoctrineBlock(
        topic="surface_use_plan",
        keywords=["surface use", "SUPO", "reclamation", "surface disturbance", "access road", "well pad"],
        conclusion_template=(
            "The Surface Use Plan of Operations (SUPO) is a mandatory component of the APD that details the operator's "
            "proposed surface disturbance, access roads, well pad construction, water sources, waste disposal, and "
            "interim and final reclamation. BLM reviews SUPO for compliance with RMP stipulations and surface protection."
        ),
        reasoning_framework=(
            "Step 1: Map proposed surface disturbance (well pad, roads, pipelines, facilities). "
            "Step 2: Identify sensitive resources (wetlands, streams, cultural sites, habitat). "
            "Step 3: Apply lease stipulations (timing, no surface occupancy, controlled surface use). "
            "Step 4: Design mitigation measures for identified impacts. "
            "Step 5: Include interim reclamation plan (during operations) and final reclamation plan. "
            "Step 6: BLM reviews SUPO as part of APD NEPA process. "
            "Step 7: Conditions of Approval may modify SUPO requirements."
        ),
        key_factors=[
            "Surface disturbance acreage and footprint",
            "Lease stipulation compliance",
            "NSO (no surface occupancy) zones",
            "Timing limitation stipulations",
            "Interim and final reclamation plans",
            "Water source identification and permitting",
            "Waste disposal methods",
        ],
        primary_authority=[
            "43 CFR 3162.3-1(f) (Surface use plan requirements)",
            "Onshore Oil and Gas Order No. 1, Sec III.D",
            "BLM Gold Book (Surface Operating Standards for Oil and Gas)",
        ],
        burden_holder="Operator (designing adequate SUPO and performing reclamation)",
        adversary_position="BLM or surface management agency may require additional mitigation increasing costs and timeline.",
        counter_arguments=[
            "NSO stipulations can be waived or modified by BLM with adequate justification",
            "Reclamation bond amount must be adequate to cover actual reclamation costs",
            "Surface owner on split estate has separate negotiation rights",
        ],
        resolution_strategy=(
            "Reference Gold Book standards. Address all stipulations explicitly. "
            "Include detailed reclamation cost estimate to support bond amount."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="BLM Gold Book (Surface Operating Standards, 4th Ed. 2007)",
        category="permitting",
    )


def _nepa_environmental_assessment() -> DoctrineBlock:
    return DoctrineBlock(
        topic="nepa_environmental_assessment",
        keywords=["NEPA", "EA", "environmental assessment", "FONSI", "environmental review", "40 CFR 1501"],
        conclusion_template=(
            "An Environmental Assessment (EA) under NEPA is the standard review level for most federal oil and gas actions. "
            "The EA analyzes environmental impacts, alternatives, and mitigation. If no significant impact is found, BLM "
            "issues a Finding of No Significant Impact (FONSI). If significant impacts exist, a full EIS is required."
        ),
        reasoning_framework=(
            "Step 1: BLM determines NEPA level needed (CX, EA, or EIS). "
            "Step 2: EA scope defined (proposed action, alternatives, affected environment). "
            "Step 3: Analyze direct, indirect, and cumulative impacts. "
            "Step 4: Consider reasonable alternatives including no-action. "
            "Step 5: Identify mitigation measures to reduce impacts. "
            "Step 6: Issue FONSI if impacts not significant. "
            "Step 7: If significant impacts cannot be mitigated, prepare EIS. "
            "Step 8: Decision documented in Decision Record."
        ),
        key_factors=[
            "Significance determination (context and intensity)",
            "Direct, indirect, and cumulative impacts",
            "Reasonable range of alternatives",
            "Mitigation measures effectiveness",
            "Public involvement opportunities",
            "Tiering from RMP-level EIS",
        ],
        primary_authority=[
            "42 USC 4332 (NEPA Sec 102)",
            "40 CFR 1501.3 (Determine level of NEPA review)",
            "40 CFR 1501.5 (Environmental Assessments)",
            "43 CFR 46 (BLM NEPA procedures)",
        ],
        burden_holder="BLM (adequate analysis); Operator (providing accurate project description)",
        adversary_position="Challengers argue EA scope too narrow, cumulative impacts ignored, or alternatives improperly dismissed.",
        counter_arguments=[
            "EA can tier from existing RMP EIS for cumulative analysis",
            "Range of alternatives must be reasonable, not exhaustive",
            "Mitigation measures can reduce impacts below significance threshold",
        ],
        resolution_strategy=(
            "Ensure project description is accurate and complete. Provide environmental data proactively. "
            "Support BLM in addressing cumulative impacts to avoid EIS trigger."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Robertson v. Methow Valley Citizens Council, 490 U.S. 332 (1989) (NEPA analysis requirements)",
        category="environmental",
    )


def _nepa_eis_process() -> DoctrineBlock:
    return DoctrineBlock(
        topic="nepa_eis_process",
        keywords=["EIS", "environmental impact statement", "scoping", "ROD", "record of decision", "draft EIS"],
        conclusion_template=(
            "A full Environmental Impact Statement (EIS) is required for major federal actions significantly affecting the "
            "environment. The EIS process includes scoping, draft EIS with public comment, final EIS, and Record of Decision. "
            "Typical timeline is 1-3 years. Lease sales and large development projects may require EIS-level review."
        ),
        reasoning_framework=(
            "Step 1: BLM publishes Notice of Intent to prepare EIS. "
            "Step 2: Public scoping to identify issues and alternatives. "
            "Step 3: Draft EIS prepared analyzing alternatives and impacts. "
            "Step 4: 45-day minimum public comment period on draft. "
            "Step 5: Final EIS incorporating comments and responses. "
            "Step 6: 30-day wait period after final EIS. "
            "Step 7: Record of Decision (ROD) issued selecting preferred alternative. "
            "Step 8: Implementation of selected alternative with monitoring."
        ),
        key_factors=[
            "Notice of Intent publication",
            "Public scoping process",
            "Range of alternatives analysis",
            "Draft and final EIS content requirements",
            "Public comment periods (45+ days for draft)",
            "30-day wait after final EIS",
            "Record of Decision content and timing",
        ],
        primary_authority=[
            "42 USC 4332(C) (EIS requirement)",
            "40 CFR 1502 (Environmental Impact Statement)",
            "40 CFR 1503 (Commenting on EIS)",
            "40 CFR 1505 (NEPA and agency decision making)",
        ],
        burden_holder="BLM (adequate analysis and public process)",
        adversary_position="Litigants argue inadequate alternatives analysis, flawed cumulative impact assessment, or premature ROD.",
        counter_arguments=[
            "BLM need not analyze every conceivable alternative, only reasonable ones",
            "Supplemental EIS required only for substantial new information",
            "Programmatic EIS can tier to site-specific decisions",
        ],
        resolution_strategy=(
            "Engage early in scoping. Provide technical data to support preferred alternative. "
            "Review draft EIS for accuracy of project description. Comment constructively."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Calvert Cliffs' Coordinating Comm. v. AEC, 449 F.2d 1109 (D.C. Cir. 1971) (EIS rigor)",
        category="environmental",
    )


def _categorical_exclusion() -> DoctrineBlock:
    return DoctrineBlock(
        topic="categorical_exclusion",
        keywords=["categorical exclusion", "CX", "CatEx", "NEPA exemption", "categorical", "exclusion"],
        conclusion_template=(
            "Categorical exclusions (CXs) allow certain federal oil and gas actions to proceed without EA or EIS if the "
            "action falls within a pre-approved category and no extraordinary circumstances exist. Energy Policy Act of 2005 "
            "CXs cover certain infill drilling and routine well operations. BLM has additional CX categories in 516 DM 11."
        ),
        reasoning_framework=(
            "Step 1: Determine if proposed action fits a CX category. "
            "Step 2: Check for extraordinary circumstances that would preclude CX use. "
            "Step 3: Document CX determination in project file. "
            "Step 4: If extraordinary circumstances exist, escalate to EA or EIS. "
            "Step 5: CX does not eliminate other compliance (ESA, NHPA). "
            "Step 6: BLM tracks CX usage for reporting purposes."
        ),
        key_factors=[
            "Action must fit established CX category",
            "No extraordinary circumstances present",
            "EPAct 2005 Sec 390 CX categories for O&G",
            "Does not eliminate ESA/NHPA compliance",
            "Documentation still required",
            "BLM Departmental Manual 516 DM 11 categories",
        ],
        primary_authority=[
            "40 CFR 1501.4 (Categorical exclusions)",
            "Energy Policy Act of 2005 Sec 390",
            "516 DM 11 (BLM CX categories)",
            "43 CFR 46.210 (Extraordinary circumstances)",
        ],
        burden_holder="BLM (verifying CX applicability and no extraordinary circumstances)",
        adversary_position="Environmental groups challenge CX use arguing extraordinary circumstances exist (endangered species, cultural sites).",
        counter_arguments=[
            "CX is valid only when extraordinary circumstances are absent",
            "EPAct 2005 CXs have specific qualifying criteria that must be met",
            "BLM must document extraordinary circumstance analysis even for CX",
        ],
        resolution_strategy=(
            "Confirm proposed action fits CX category precisely. Document absence of extraordinary circumstances. "
            "Obtain ESA/NHPA clearances independently of CX determination."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Sierra Club v. Bosworth, 510 F.3d 1016 (9th Cir. 2007) (CX extraordinary circumstances)",
        category="environmental",
    )


def _esa_section7_consultation() -> DoctrineBlock:
    return DoctrineBlock(
        topic="esa_section7_consultation",
        keywords=["ESA", "section 7", "endangered species", "biological opinion", "incidental take", "critical habitat", "jeopardy"],
        conclusion_template=(
            "ESA Section 7 requires BLM to consult with USFWS when a proposed federal oil and gas action may affect listed "
            "species or critical habitat. Informal consultation may result in a 'not likely to adversely affect' concurrence. "
            "Formal consultation produces a Biological Opinion with an Incidental Take Statement and reasonable alternatives."
        ),
        reasoning_framework=(
            "Step 1: BLM identifies listed species and critical habitat in project area. "
            "Step 2: Prepare Biological Assessment (BA) analyzing effects. "
            "Step 3: If 'no effect' determination, no consultation needed. "
            "Step 4: If 'not likely to adversely affect,' initiate informal consultation. "
            "Step 5: USFWS concurs or requests formal consultation. "
            "Step 6: Formal consultation: USFWS issues Biological Opinion (BO). "
            "Step 7: BO includes Incidental Take Statement (ITS) with terms and conditions. "
            "Step 8: If jeopardy found, USFWS provides reasonable and prudent alternatives."
        ),
        key_factors=[
            "Listed species presence in project area",
            "Critical habitat designation",
            "Effect determination (no effect, NLAA, LAA)",
            "Formal vs informal consultation",
            "Biological Opinion content",
            "Incidental Take Statement terms",
            "Reasonable and prudent alternatives if jeopardy",
        ],
        primary_authority=[
            "16 USC 1536 (ESA Sec 7)",
            "50 CFR 402 (Section 7 Consultation)",
            "50 CFR 402.14 (Formal consultation)",
            "50 CFR 402.13 (Informal consultation)",
        ],
        burden_holder="BLM (initiating consultation); USFWS (completing review); Operator (complying with ITS terms)",
        adversary_position="Environmental groups argue BLM failed to consult or that BO is flawed; industry argues consultation delays unreasonable.",
        counter_arguments=[
            "BLM must reinitiate consultation if project scope changes or new species listed",
            "ITS terms and conditions are mandatory, not optional",
            "Failure to consult can result in injunction halting operations",
        ],
        resolution_strategy=(
            "Conduct early species surveys. Prepare thorough BA to streamline consultation. "
            "Design project to minimize species impacts. Comply strictly with ITS terms."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Tennessee Valley Authority v. Hill, 437 U.S. 153 (1978) (ESA supremacy)",
        category="environmental",
    )


def _section106_nhpa() -> DoctrineBlock:
    return DoctrineBlock(
        topic="section106_nhpa_compliance",
        keywords=["section 106", "NHPA", "cultural resources", "archaeological", "historic preservation", "tribal consultation"],
        conclusion_template=(
            "Section 106 of NHPA requires BLM to identify historic properties in the area of potential effect, assess "
            "adverse effects, and consult with SHPO/THPO and tribes to resolve adverse effects before approving the APD. "
            "Class III archaeological surveys are typically required for previously unsurveyed areas."
        ),
        reasoning_framework=(
            "Step 1: Define Area of Potential Effects (APE) for the project. "
            "Step 2: Review existing cultural resource records and surveys. "
            "Step 3: Conduct Class III intensive survey if area not previously surveyed. "
            "Step 4: Identify historic properties eligible for National Register. "
            "Step 5: Assess effects (no effect, no adverse effect, adverse effect). "
            "Step 6: Consult with SHPO/THPO and interested tribes. "
            "Step 7: If adverse effect, negotiate Memorandum of Agreement for mitigation. "
            "Step 8: BLM incorporates 106 findings into APD decision."
        ),
        key_factors=[
            "Area of Potential Effects definition",
            "Class III survey requirement",
            "National Register eligibility criteria",
            "SHPO/THPO consultation",
            "Tribal consultation on traditional cultural properties",
            "Adverse effect assessment",
            "Memorandum of Agreement for mitigation",
        ],
        primary_authority=[
            "54 USC 306108 (NHPA Sec 106)",
            "36 CFR 800 (Section 106 regulations)",
            "36 CFR 800.4 (Identification of historic properties)",
            "36 CFR 800.5 (Assessment of adverse effects)",
        ],
        burden_holder="BLM (completing 106 process); Operator (paying for surveys)",
        adversary_position="Tribes may argue traditional cultural properties not adequately identified; SHPO may disagree on eligibility.",
        counter_arguments=[
            "Operator typically bears cost of Class III survey",
            "BLM cannot approve APD before 106 process complete",
            "Programmatic agreements can streamline repetitive 106 reviews",
        ],
        resolution_strategy=(
            "Commission Class III survey early. Engage tribes proactively. "
            "If sites found, design project to avoid rather than mitigate."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Muckleshoot Indian Tribe v. USFS, 177 F.3d 800 (9th Cir. 1999) (Section 106 adequacy)",
        category="environmental",
    )


def _split_estate_surface_rights() -> DoctrineBlock:
    return DoctrineBlock(
        topic="split_estate_surface_rights",
        keywords=["split estate", "surface owner", "federal minerals", "private surface", "surface notification", "accommodation"],
        conclusion_template=(
            "Split estate occurs when federal minerals underlie private surface. The mineral estate is dominant, but the "
            "operator must provide advance notice to the surface owner and attempt good faith negotiation for surface use. "
            "BLM regulations require surface owner notification before APD approval and encourage surface use agreements."
        ),
        reasoning_framework=(
            "Step 1: Determine if lease involves split estate (federal minerals, private surface). "
            "Step 2: Operator must notify surface owner of proposed operations (43 CFR 3101.1-2). "
            "Step 3: Good faith effort to negotiate surface use agreement. "
            "Step 4: If no agreement, operator may still proceed under federal mineral right dominance. "
            "Step 5: BLM includes surface owner concerns in NEPA analysis. "
            "Step 6: Conditions of Approval may address surface owner issues. "
            "Step 7: State law accommodation doctrines may apply in parallel. "
            "Step 8: Surface owner has no veto over federal mineral development."
        ),
        key_factors=[
            "Federal mineral dominance doctrine",
            "Surface owner notification requirements",
            "Good faith negotiation obligation",
            "Surface use agreement (voluntary)",
            "No surface owner veto over development",
            "State accommodation doctrine applicability",
            "BLM NEPA consideration of surface impacts",
        ],
        primary_authority=[
            "43 CFR 3101.1-2 (Surface owner notification)",
            "30 USC 226(g) (Surface owner protection)",
            "BLM IM 2007-097 (Split estate guidance)",
        ],
        burden_holder="Operator (notification and good faith negotiation); BLM (NEPA consideration of surface impacts)",
        adversary_position="Surface owners argue mineral development destroys agricultural value without adequate compensation.",
        counter_arguments=[
            "Mineral estate is dominant under federal common law",
            "Surface owner cannot prevent access but can negotiate terms",
            "Some states require separate surface damage payments",
        ],
        resolution_strategy=(
            "Notify surface owner early. Negotiate in good faith. Document all communications. "
            "Include surface use agreement terms in APD if reached."
        ),
        entity_scope=EntityScope.SPLIT_ESTATE,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Kinney-Coastal Oil Co. v. Kieffer, 277 U.S. 488 (1928) (mineral estate dominance)",
        category="surface_rights",
    )


def _national_forest_consent() -> DoctrineBlock:
    return DoctrineBlock(
        topic="national_forest_consent",
        keywords=["national forest", "Forest Service", "USFS", "NFS", "forest consent", "forest stipulation"],
        conclusion_template=(
            "For federal mineral leases on National Forest System lands, the Forest Service must consent to leasing under "
            "the Mineral Leasing Act. Forest Service consent may include stipulations for surface protection. The Forest "
            "Service is the surface management agency and conducts its own NEPA review for APDs on NFS lands."
        ),
        reasoning_framework=(
            "Step 1: Determine if proposed lease or APD is on NFS lands. "
            "Step 2: Forest Service must consent to lease issuance with stipulations. "
            "Step 3: Forest Plan (NFMA) compatibility analysis required. "
            "Step 4: Forest Service NEPA review separate from BLM for surface impacts. "
            "Step 5: Forest Service may apply NSO, timing, or controlled surface use stipulations. "
            "Step 6: APD requires Forest Service approval of surface use plan on NFS lands. "
            "Step 7: BLM issues lease but Forest Service controls surface."
        ),
        key_factors=[
            "Forest Service consent to lease issuance",
            "Forest Plan compatibility",
            "Forest Service NEPA review for surface impacts",
            "NSO and timing stipulations by Forest Service",
            "Dual jurisdiction: BLM (subsurface), USFS (surface)",
            "Forest Service approval of surface use plan for APD",
        ],
        primary_authority=[
            "30 USC 226(h) (Forest Service consent requirement)",
            "36 CFR 228 Subpart E (Oil and Gas on NFS lands)",
            "National Forest Management Act (16 USC 1600 et seq.)",
        ],
        burden_holder="Forest Service (consent and surface protection); BLM (lease issuance); Operator (compliance with both agencies)",
        adversary_position="Forest Service may impose restrictive stipulations that make development uneconomic.",
        counter_arguments=[
            "Forest Service consent authority is broad and discretionary",
            "Stipulation waivers require Forest Service approval, not just BLM",
            "Operator must comply with both BLM and USFS requirements",
        ],
        resolution_strategy=(
            "Coordinate with both BLM and Forest Service early. Understand Forest Plan provisions. "
            "Design operations to minimize surface disturbance on NFS lands."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="California v. Bergland, 483 F. Supp. 465 (E.D. Cal. 1980) (Forest Service consent authority)",
        category="permitting",
    )


def _onrr_royalty_reporting() -> DoctrineBlock:
    return DoctrineBlock(
        topic="onrr_royalty_reporting",
        keywords=["ONRR", "royalty reporting", "OGOR", "production reporting", "payor report", "Form 2014", "Form 4054"],
        conclusion_template=(
            "ONRR requires monthly production and royalty reporting from federal and Indian lease operators. The OGOR-A "
            "(production) and OGOR-B (sales/disposition) are due by the end of the month following production. Royalty "
            "payments are due on the same schedule. Late payments accrue interest at the Federal Register rate."
        ),
        reasoning_framework=(
            "Step 1: Operator reports production volumes on OGOR-A by end of month following production. "
            "Step 2: Payor reports royalty value on OGOR-B with royalty payment. "
            "Step 3: Oil valued at gross proceeds or NYMEX-based; gas at index-based price. "
            "Step 4: Transportation and processing allowances deducted per 30 CFR 1206. "
            "Step 5: ONRR audits reported values and may issue orders to pay. "
            "Step 6: Interest accrues on late payments from due date. "
            "Step 7: Civil penalties for knowing or willful misreporting."
        ),
        key_factors=[
            "Monthly reporting deadlines",
            "OGOR-A (production volumes) and OGOR-B (royalty values)",
            "Valuation methodology (gross proceeds vs index)",
            "Transportation and processing allowance limits",
            "Interest on late payments",
            "Civil penalties for misreporting",
            "7-year statute of limitations for royalty demands",
        ],
        primary_authority=[
            "30 CFR 1210 (Reporting and Paying Royalties)",
            "30 CFR 1206 (Product Valuation)",
            "30 CFR 1218 (Collection of Payments)",
            "30 USC 1720a (Civil penalties)",
        ],
        burden_holder="Operator/Payor (accurate and timely reporting); ONRR (audit and enforcement)",
        adversary_position="ONRR may apply higher valuation methodology or disallow claimed allowances; lessee may contest audit findings.",
        counter_arguments=[
            "ONRR demand letters must be issued within 7 years of production month",
            "Lessees may appeal ONRR orders through administrative process",
            "Allowances must be arm's length or ONRR-approved",
        ],
        resolution_strategy=(
            "Maintain accurate production and sales records. File timely. "
            "Document all transportation and processing costs for allowance claims."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="BP Amoco v. ONRR (royalty valuation methodology disputes)",
        category="royalty",
    )


def _onrr_product_valuation() -> DoctrineBlock:
    return DoctrineBlock(
        topic="onrr_product_valuation",
        keywords=["valuation", "gross proceeds", "index price", "arm length", "allowance", "30 CFR 1206"],
        conclusion_template=(
            "Federal royalty valuation under 30 CFR 1206 depends on whether the sale is arm's length or non-arm's length. "
            "Arm's length sales use gross proceeds less allowances. Non-arm's length oil uses NYMEX-based benchmarks; "
            "non-arm's length gas uses published index prices. Allowances for transportation and processing are capped."
        ),
        reasoning_framework=(
            "Step 1: Determine if first sale is arm's length or non-arm's length. "
            "Step 2: Arm's length: value = gross proceeds (actual sales price). "
            "Step 3: Non-arm's length oil: NYMEX settlement price adjusted for quality and location. "
            "Step 4: Non-arm's length gas: index-based value from published price sources. "
            "Step 5: Deduct transportation allowance (actual cost or ONRR rate, whichever lower). "
            "Step 6: Deduct processing allowance for gas (actual cost or percentage cap). "
            "Step 7: Apply royalty rate to net value. "
            "Step 8: Report on OGOR-B with supporting documentation."
        ),
        key_factors=[
            "Arm's length vs non-arm's length sale determination",
            "Gross proceeds definition and inclusions",
            "NYMEX-based valuation for non-arm's length oil",
            "Index-based valuation for non-arm's length gas",
            "Transportation allowance caps and documentation",
            "Processing allowance caps (66.67% or actual cost)",
            "Quality and location adjustments",
        ],
        primary_authority=[
            "30 CFR 1206.100-1206.109 (Oil valuation)",
            "30 CFR 1206.140-1206.157 (Gas valuation)",
            "30 CFR 1206.110-1206.115 (Transportation allowances)",
            "30 CFR 1206.156-1206.159 (Processing allowances)",
        ],
        burden_holder="Payor (demonstrating proper valuation and allowances); ONRR (audit verification)",
        adversary_position="ONRR may reclassify transactions as non-arm's length or disallow excessive allowances.",
        counter_arguments=[
            "Arm's length status requires genuine independence between buyer and seller",
            "Affiliate transactions are presumptively non-arm's length",
            "ONRR can require actual cost documentation for claimed allowances",
        ],
        resolution_strategy=(
            "Document arm's length status with independent market evidence. "
            "Maintain detailed transportation and processing cost records. "
            "Use published index prices consistently for non-arm's length valuations."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Devon Energy v. Kempthorne, 551 F.3d 1030 (D.C. Cir. 2008) (gas valuation methodology)",
        category="royalty",
    )


def _federal_bonding_requirements() -> DoctrineBlock:
    return DoctrineBlock(
        topic="federal_bonding_requirements",
        keywords=["bond", "bonding", "performance bond", "reclamation bond", "nationwide bond", "statewide bond", "idle well bond"],
        conclusion_template=(
            "Federal lease operators must maintain adequate bonds per 43 CFR 3104. Individual lease bonds start at $10,000. "
            "Statewide bonds are $25,000; nationwide bonds are $150,000. The IRA 2022 increased minimum bond amounts and "
            "requires supplemental bonding for operators with idle wells. BLM may require additional bonding if warranted."
        ),
        reasoning_framework=(
            "Step 1: Determine bond type needed (individual, statewide, nationwide). "
            "Step 2: Apply IRA 2022 minimum amounts ($150K nationwide, $25K statewide, $10K individual). "
            "Step 3: BLM assesses whether minimum bond covers plugging and reclamation liability. "
            "Step 4: If minimum insufficient, BLM requires supplemental bond. "
            "Step 5: Operators with idle wells face additional bonding requirements. "
            "Step 6: Bond must remain in effect until all obligations satisfied. "
            "Step 7: BLM can demand increased bond at any time based on liability assessment."
        ),
        key_factors=[
            "Individual lease bond minimum ($10,000)",
            "Statewide bond minimum ($25,000)",
            "Nationwide bond minimum ($150,000)",
            "IRA 2022 bond amount increases",
            "Supplemental bonding for idle wells",
            "BLM discretion to increase bond amounts",
            "Bond release only after all obligations met",
        ],
        primary_authority=[
            "43 CFR 3104 (Bonds)",
            "IRA 2022 Sec 50263 (Bonding requirements)",
            "30 USC 226(g) (Bond requirements)",
        ],
        burden_holder="Operator (maintaining adequate bond); BLM (assessing bond adequacy)",
        adversary_position="Environmental groups argue bond amounts still inadequate to cover actual plugging and reclamation costs.",
        counter_arguments=[
            "IRA substantially increased minimums from pre-existing $10K/$25K/$150K levels",
            "BLM has discretion to require additional bonding above minimums",
            "Idle well bonding specifically addresses orphan well liability",
        ],
        resolution_strategy=(
            "Maintain nationwide bond for portfolio operators. Assess idle well liability proactively. "
            "Budget for potential supplemental bonding requirements."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="43 CFR 3104 as amended by IRA 2022 implementing regulations",
        category="compliance",
    )


def _idle_well_regulations() -> DoctrineBlock:
    return DoctrineBlock(
        topic="idle_well_regulations",
        keywords=["idle well", "orphan well", "plugging", "abandonment", "decommissioning", "idle iron", "nonproducing"],
        conclusion_template=(
            "Federal regulations require operators to plug and abandon wells no longer capable of production. The IRA 2022 "
            "established new idle well fees and bonding requirements. BLM can order plugging of wells idle for 7+ years. "
            "The Orphaned Well Program provides $4.7 billion for plugging documented orphan wells on federal land."
        ),
        reasoning_framework=(
            "Step 1: Identify wells idle for extended period (no production, no approved SOP). "
            "Step 2: Determine if well meets BLM idle well definition. "
            "Step 3: Assess plugging and reclamation liability. "
            "Step 4: Pay applicable idle well fee or submit plan to return to production. "
            "Step 5: BLM may order plugging if operator fails to act. "
            "Step 6: If operator cannot be found, well enters orphan well program. "
            "Step 7: Bond forfeiture if operator defaults on plugging obligation."
        ),
        key_factors=[
            "Definition of idle well (no production, no approved SOP)",
            "7-year idle well threshold for BLM ordered plugging",
            "Idle well fees under IRA 2022",
            "Plugging and reclamation cost estimates",
            "Bond forfeiture for defaulting operators",
            "$4.7 billion Orphaned Well Program",
            "State coordination for orphan well plugging",
        ],
        primary_authority=[
            "IRA 2022 Sec 50263 (Idle well provisions)",
            "Bipartisan Infrastructure Law Sec 40601 (Orphaned Well Program)",
            "43 CFR 3162.3-4 (Well abandonment requirements)",
        ],
        burden_holder="Operator (plugging idle wells); BLM (enforcement); Federal/State governments (orphan well program)",
        adversary_position="Environmental groups push for faster plugging timelines; industry argues some idle wells have future potential.",
        counter_arguments=[
            "Operators must demonstrate legitimate plan to return idle well to production",
            "BLM can deny SOP if well is truly uneconomic",
            "Bond amounts may be insufficient for actual plugging costs",
        ],
        resolution_strategy=(
            "Inventory all idle wells. Develop plan to produce, plug, or obtain SOP for each. "
            "Budget for plugging liability and supplemental bonding."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="IRA 2022 and BIL implementing regulations (emerging regulatory framework)",
        category="compliance",
    )


def _texas_glo_leasing() -> DoctrineBlock:
    return DoctrineBlock(
        topic="texas_glo_leasing",
        keywords=["Texas", "GLO", "General Land Office", "state lease", "Texas state mineral", "uplands", "submerged"],
        conclusion_template=(
            "The Texas General Land Office manages mineral leasing on state-owned lands including Permanent School Fund (PSF) "
            "lands, submerged lands, and other state tracts. GLO leases are offered at competitive auction with minimum "
            "bonus bids. Primary terms are typically 3-5 years. Royalty rates range from 20-25%. GLO uses electronic bidding."
        ),
        reasoning_framework=(
            "Step 1: Determine land classification (PSF, submerged, other state land). "
            "Step 2: Check GLO lease sale schedule for tract availability. "
            "Step 3: Submit bid at or above minimum bonus bid. "
            "Step 4: Winning bidder executes GLO lease form with state-mandated terms. "
            "Step 5: Primary term is 3-5 years; lease held by production thereafter. "
            "Step 6: Royalty rate set by GLO (typically 20-25%, higher than federal). "
            "Step 7: GLO conducts its own surface and environmental review. "
            "Step 8: Annual delay rentals due until production established."
        ),
        key_factors=[
            "PSF and other state land classifications",
            "Competitive auction process",
            "Minimum bonus bid requirements",
            "3-5 year primary terms",
            "20-25% royalty rates (higher than federal)",
            "GLO lease form terms (non-negotiable)",
            "Surface and environmental review by GLO",
        ],
        primary_authority=[
            "Texas Natural Resources Code Ch 32 (Oil and Gas Leasing on State Lands)",
            "Texas Natural Resources Code Ch 51 (General Land Office Authority)",
            "16 TAC Part 1 (GLO Administrative Rules)",
        ],
        burden_holder="Lessee (compliance with GLO lease terms); GLO (administration and enforcement)",
        adversary_position="GLO may terminate lease for failure to develop or pay rentals; lessee may challenge lease terms as unreasonable.",
        counter_arguments=[
            "GLO lease terms are prescribed by statute and regulation, non-negotiable",
            "Higher royalty rates reflect state's ownership interest",
            "GLO has broad discretion in lease administration",
        ],
        resolution_strategy=(
            "Review GLO lease form terms before bidding. Budget for higher royalty rates. "
            "Calendar all rental and reporting deadlines. Coordinate with GLO on surface use."
        ),
        entity_scope=EntityScope.STATE_TX,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas NRC Ch 32 and Ch 51 (statutory framework for GLO leasing)",
        category="state_leasing",
    )


def _texas_relinquishment_act() -> DoctrineBlock:
    return DoctrineBlock(
        topic="texas_relinquishment_act",
        keywords=["Relinquishment Act", "RA lands", "surface owner lease", "Texas RA", "1919", "surface owner minerals"],
        conclusion_template=(
            "Under the Texas Relinquishment Act (1919), the state relinquished its interest in minerals under certain "
            "public school lands to the surface owner for leasing purposes. The surface owner has the exclusive right to "
            "execute mineral leases on RA lands but the state retains a royalty interest (typically 1/16 to 1/8). "
            "GLO consent is not required for leasing but GLO collects the state's royalty."
        ),
        reasoning_framework=(
            "Step 1: Determine if land is classified as Relinquishment Act land in GLO records. "
            "Step 2: Surface owner has exclusive leasing authority - no GLO lease sale needed. "
            "Step 3: Surface owner negotiates lease terms with operator. "
            "Step 4: State retains royalty interest (1/16 to 1/8 depending on classification). "
            "Step 5: Operator reports and pays state's royalty share to GLO. "
            "Step 6: Surface owner's royalty is separate from state's royalty. "
            "Step 7: Title verification requires GLO land classification records."
        ),
        key_factors=[
            "Land classification in GLO records",
            "Surface owner exclusive leasing authority",
            "State retained royalty (1/16 to 1/8)",
            "No GLO consent required for leasing",
            "Operator pays state royalty to GLO",
            "Surface owner's separate royalty interest",
            "Title examination must verify RA classification",
        ],
        primary_authority=[
            "Texas Natural Resources Code Ch 52 (Relinquishment Act)",
            "Texas Education Code Sec 32 (School land provisions)",
            "GLO records and land classification files",
        ],
        burden_holder="Surface owner (leasing); Operator (paying state royalty to GLO); GLO (collecting state royalty)",
        adversary_position="GLO may dispute land classification; surface owner may claim higher retained interest than warranted.",
        counter_arguments=[
            "RA classification is a matter of GLO record, not negotiation",
            "Surface owner cannot waive or reduce state's royalty interest",
            "Title examiners must verify RA status before acquisition",
        ],
        resolution_strategy=(
            "Verify RA classification with GLO before acquiring lease. Confirm state royalty rate applicable. "
            "Establish payment mechanism to GLO for state royalty share."
        ),
        entity_scope=EntityScope.STATE_TX,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Greene v. Robison, 117 Tex. 516 (1928) (Relinquishment Act interpretation)",
        category="state_leasing",
    )


def _texas_university_lands() -> DoctrineBlock:
    return DoctrineBlock(
        topic="texas_university_lands",
        keywords=["University Lands", "UT System", "PUF", "Permanent University Fund", "University of Texas", "UTLA"],
        conclusion_template=(
            "University Lands in West Texas (2.1 million acres) are managed by University Lands/Texas A&M System for the "
            "benefit of the Permanent University Fund (PUF). Mineral leases are offered at competitive auction with "
            "non-negotiable lease forms. Royalty rates are 25% and primary terms are 5 years. These lands represent the "
            "largest single block of oil and gas mineral rights in Texas."
        ),
        reasoning_framework=(
            "Step 1: Identify if tract is University Lands (primarily in Andrews, Crane, Ector, Reagan, Upton counties). "
            "Step 2: University Lands administers competitive lease sales. "
            "Step 3: Lease form is non-negotiable with 25% royalty. "
            "Step 4: 5-year primary term with production extension. "
            "Step 5: Revenue goes to PUF, invested by UTIMCO. "
            "Step 6: University Lands has own surface permitting process. "
            "Step 7: Environmental compliance through University Lands staff."
        ),
        key_factors=[
            "2.1 million acres in West Texas",
            "25% royalty rate (non-negotiable)",
            "5-year primary term",
            "Competitive auction process",
            "Revenue to Permanent University Fund",
            "University Lands surface permitting",
            "Non-negotiable lease form",
        ],
        primary_authority=[
            "Texas Constitution Art VII Sec 11 (PUF)",
            "Texas Education Code Ch 66 (University Lands)",
            "University Lands rules and lease forms",
        ],
        burden_holder="Lessee (compliance with University Lands terms); University Lands (administration)",
        adversary_position="Operators argue 25% royalty rate makes marginal acreage uneconomic; University Lands maintains rate to maximize PUF revenue.",
        counter_arguments=[
            "University Lands terms are take-it-or-leave-it",
            "High royalty rate offset by proven Permian Basin geology",
            "Surface use permitting can be more streamlined than BLM/GLO",
        ],
        resolution_strategy=(
            "Model economics at 25% royalty before bidding. Coordinate with University Lands on surface use early. "
            "Understand that lease terms are not subject to negotiation."
        ),
        entity_scope=EntityScope.STATE_TX,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Constitution Art VII Sec 11 (PUF establishment and purpose)",
        category="state_leasing",
    )


def _texas_school_lands() -> DoctrineBlock:
    return DoctrineBlock(
        topic="texas_school_lands",
        keywords=["school land", "PSF", "Permanent School Fund", "public school", "Texas school", "school mineral"],
        conclusion_template=(
            "Texas Permanent School Fund lands are managed by the GLO for the benefit of public education. Mineral leases "
            "are offered competitively through GLO lease sales. Revenue from PSF mineral leases goes to the Permanent School "
            "Fund, one of the largest education endowments in the US. GLO sets royalty rates (typically 20-25%)."
        ),
        reasoning_framework=(
            "Step 1: Verify land is PSF classified in GLO records. "
            "Step 2: GLO offers tracts at periodic competitive sales. "
            "Step 3: GLO sets minimum bid and royalty rate per tract. "
            "Step 4: Winning bidder executes GLO standard lease form. "
            "Step 5: Revenue allocated to PSF for investment. "
            "Step 6: GLO enforces lease terms and collects royalties. "
            "Step 7: Distinguish from Relinquishment Act lands (different regime)."
        ),
        key_factors=[
            "PSF land classification by GLO",
            "GLO competitive sale process",
            "Revenue to Permanent School Fund",
            "Royalty rates 20-25%",
            "GLO standard lease form",
            "Distinction from RA lands",
        ],
        primary_authority=[
            "Texas Constitution Art VII Sec 2-5 (Permanent School Fund)",
            "Texas Natural Resources Code Ch 32 and 51",
            "GLO administrative rules for PSF mineral leasing",
        ],
        burden_holder="GLO (administration, revenue collection); Lessee (compliance)",
        adversary_position="Operators may challenge GLO royalty rates; GLO must balance revenue maximization with development encouragement.",
        counter_arguments=[
            "GLO has fiduciary duty to maximize PSF revenue",
            "GLO lease terms are standardized by regulation",
            "Operators have no right to negotiate below-market terms",
        ],
        resolution_strategy=(
            "Verify PSF classification. Review current GLO lease sale terms. "
            "Budget for higher-than-federal royalty rates."
        ),
        entity_scope=EntityScope.STATE_TX,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texas Natural Resources Code Ch 32 (PSF mineral leasing authority)",
        category="state_leasing",
    )


def _nm_state_land_leasing() -> DoctrineBlock:
    return DoctrineBlock(
        topic="new_mexico_state_land_leasing",
        keywords=["New Mexico", "SLO", "State Land Office", "NM state", "trust land", "New Mexico lease"],
        conclusion_template=(
            "The New Mexico State Land Office manages 9 million surface acres and 13 million mineral acres held in trust "
            "for public schools and other beneficiaries. Oil and gas leases are offered at competitive auction with state-"
            "mandated terms. Primary terms are 5 years with royalty rates typically 18.75% (3/16) to 20%. NMSLO conducts "
            "its own environmental review."
        ),
        reasoning_framework=(
            "Step 1: Verify tract status with NMSLO records. "
            "Step 2: NMSLO holds periodic competitive lease sales. "
            "Step 3: Minimum bonus bid and rental rates set by NMSLO. "
            "Step 4: 5-year primary term with production extension. "
            "Step 5: Royalty rate typically 18.75-20%. "
            "Step 6: NMSLO conducts environmental and surface review. "
            "Step 7: Revenue allocated to designated trust beneficiaries. "
            "Step 8: NM Oil Conservation Division (OCD) regulates operations."
        ),
        key_factors=[
            "13 million mineral acres under NMSLO management",
            "Competitive auction for lease sales",
            "5-year primary terms",
            "18.75-20% royalty rates",
            "Trust beneficiary fiduciary obligation",
            "NMSLO environmental review",
            "NM OCD operational regulation",
        ],
        primary_authority=[
            "NMSA 1978 Sec 19-1 through 19-10 (State Lands)",
            "NM Constitution Art XII (Trust lands)",
            "NMSLO administrative rules and lease forms",
        ],
        burden_holder="NMSLO (trust administration); Lessee (compliance with lease and OCD rules)",
        adversary_position="NMSLO has fiduciary duty to beneficiaries; may increase terms to maximize revenue.",
        counter_arguments=[
            "NMSLO terms are set by regulation and statute",
            "NM OCD permitting is separate from NMSLO leasing",
            "Federal lands in NM subject to different (BLM) regime",
        ],
        resolution_strategy=(
            "Verify state vs federal jurisdiction for each tract. Review current NMSLO sale terms. "
            "Coordinate with both NMSLO (lease) and OCD (operations)."
        ),
        entity_scope=EntityScope.STATE_NM,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="NMSA 1978 Sec 19-1 et seq. (State Lands statutory framework)",
        category="state_leasing",
    )


def _federal_lease_reinstatement() -> DoctrineBlock:
    return DoctrineBlock(
        topic="federal_lease_reinstatement",
        keywords=["reinstatement", "30 USC 188", "terminated lease", "late payment", "good faith", "reinstate"],
        conclusion_template=(
            "A federal lease terminated for nonpayment of rental may be reinstated under 30 USC 188(d) (Class I - within "
            "one year if filed timely and good faith shown) or 30 USC 188(e) (Class II - over one year with additional "
            "justification). Reinstatement requires back rental, $10/acre reinstatement fee, and showing of justifiable excuse."
        ),
        reasoning_framework=(
            "Step 1: Determine when lease terminated (date of missed rental payment). "
            "Step 2: Class I reinstatement: filed within 15 months, $10/acre penalty, back rentals. "
            "Step 3: Class II reinstatement: filed within 2 years, $20/acre penalty, additional justification. "
            "Step 4: Petitioner must show nonpayment was justified or not due to lack of reasonable diligence. "
            "Step 5: BLM reviews and may approve or deny. "
            "Step 6: If approved, lease reinstated with continuous primary term. "
            "Step 7: IBLA appeals available if denied."
        ),
        key_factors=[
            "Class I vs Class II reinstatement timelines",
            "Good faith / justifiable excuse showing",
            "Back rental payment requirement",
            "Reinstatement penalty fees ($10 or $20/acre)",
            "BLM discretion in approval",
            "IBLA appeal rights",
        ],
        primary_authority=[
            "30 USC 188(d) (Class I reinstatement)",
            "30 USC 188(e) (Class II reinstatement)",
            "43 CFR 3108.2 (Reinstatement procedures)",
        ],
        burden_holder="Former lessee (demonstrating good faith and paying required amounts)",
        adversary_position="BLM may deny reinstatement if lessee's excuse is insufficient or filing is untimely.",
        counter_arguments=[
            "Courts strictly construe reinstatement deadlines",
            "Clerical errors may support good faith but must be documented",
            "BLM cannot reinstate outside statutory deadlines regardless of equities",
        ],
        resolution_strategy=(
            "File reinstatement petition immediately upon discovering termination. "
            "Document all circumstances of missed payment. Pay all required amounts with petition."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Copper Valley Machine Works v. Andrus, 653 F.2d 595 (D.C. Cir. 1981)",
        category="lease_terms",
    )


def _federal_lease_renewal() -> DoctrineBlock:
    return DoctrineBlock(
        topic="federal_lease_renewal",
        keywords=["renewal", "lease renewal", "20 year", "extension", "secondary term", "continued operations"],
        conclusion_template=(
            "Federal leases do not have a formal renewal process. Instead, leases continue beyond the primary term through "
            "production in paying quantities under 43 CFR 3107. The lease remains in effect so long as oil or gas is produced "
            "in paying quantities. There is no separate renewal application - continuation is automatic with production."
        ),
        reasoning_framework=(
            "Step 1: Federal leases have a 10-year primary term. "
            "Step 2: No 'renewal' - lease extends automatically with production. "
            "Step 3: Production in paying quantities must exist at expiration. "
            "Step 4: Paying quantities = revenue exceeding direct operating costs. "
            "Step 5: Temporary cessation allowed under prudent operator standard. "
            "Step 6: If production ceases permanently, lease terminates. "
            "Step 7: Distinguish from state leases that may have formal renewal provisions."
        ),
        key_factors=[
            "Automatic continuation with production",
            "No formal renewal application needed",
            "Paying quantities standard (prudent operator test)",
            "Temporary cessation doctrine",
            "Permanent cessation terminates lease",
            "Unit commitment can substitute for production on committed tracts",
        ],
        primary_authority=[
            "30 USC 226(e) and (i) (Lease extension by production)",
            "43 CFR 3107.2 (Production in paying quantities)",
            "43 CFR 3107.4 (Cessation of production)",
        ],
        burden_holder="Lessee (maintaining production to continue lease)",
        adversary_position="BLM may challenge whether marginal production constitutes paying quantities.",
        counter_arguments=[
            "Prudent operator test considers totality of circumstances",
            "Brief production interruptions do not terminate if operations continuing",
            "Marketing difficulties may support temporary cessation argument",
        ],
        resolution_strategy=(
            "Monitor production economics continuously. If well becomes marginal, document prudent operator analysis. "
            "Consider SOP application before production permanently ceases."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Texaco Inc., 123 IBLA 379 (1992) (paying quantities and lease continuation)",
        category="lease_terms",
    )


def _blm_protest_and_appeal() -> DoctrineBlock:
    return DoctrineBlock(
        topic="blm_protest_and_appeal",
        keywords=["protest", "appeal", "IBLA", "lease sale protest", "BLM decision", "administrative appeal"],
        conclusion_template=(
            "BLM lease sale decisions and APD approvals may be protested administratively and appealed to the Interior Board "
            "of Land Appeals (IBLA). Lease sale protests must be filed before the sale. Post-decision appeals go to IBLA "
            "within 30 days. IBLA may grant stays pending appeal. Federal court review follows exhaustion of administrative remedies."
        ),
        reasoning_framework=(
            "Step 1: Identify the BLM decision being challenged. "
            "Step 2: For lease sales, file protest before sale date. "
            "Step 3: For other decisions, file appeal with IBLA within 30 days. "
            "Step 4: Request stay if immediate relief needed. "
            "Step 5: IBLA reviews on administrative record. "
            "Step 6: IBLA decision is final DOI action. "
            "Step 7: Federal court review available after IBLA decision."
        ),
        key_factors=[
            "Pre-sale protest filing deadline",
            "30-day appeal deadline to IBLA",
            "Stay request for immediate relief",
            "Administrative record basis for review",
            "IBLA as final DOI decision",
            "Exhaustion of administrative remedies before court",
        ],
        primary_authority=[
            "43 CFR 4.410-4.480 (IBLA procedures)",
            "43 CFR 3120.1-3 (Lease sale protest procedures)",
            "Administrative Procedure Act, 5 USC 706",
        ],
        burden_holder="Appellant (filing timely, demonstrating error); BLM (defending decision on administrative record)",
        adversary_position="Environmental groups are frequent appellants; industry may also appeal unfavorable BLM decisions.",
        counter_arguments=[
            "IBLA stays are discretionary, not automatic",
            "Lease already issued may not be reversed absent clear error",
            "Court applies deferential review to IBLA decisions",
        ],
        resolution_strategy=(
            "File timely. Build strong administrative record during BLM process. "
            "Intervene if third party appeal threatens your lease interests."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="43 CFR Part 4 (DOI administrative appeal procedures)",
        category="compliance",
    )


def _ibla_appeals_process() -> DoctrineBlock:
    return DoctrineBlock(
        topic="ibla_appeals_process",
        keywords=["IBLA", "Interior Board", "land appeals", "DOI appeal", "administrative judge", "stay of decision"],
        conclusion_template=(
            "The Interior Board of Land Appeals (IBLA) hears appeals from BLM and other DOI bureau decisions on public land "
            "and mineral matters. Appeals must be filed within 30 days of the decision. The 4-part stay test considers "
            "likelihood of success, irreparable harm, harm to other parties, and public interest."
        ),
        reasoning_framework=(
            "Step 1: File Notice of Appeal with BLM State Director within 30 days. "
            "Step 2: File Statement of Reasons within 30 days after Notice of Appeal. "
            "Step 3: If stay needed, file petition for stay with 4-part test analysis. "
            "Step 4: BLM files answer within 30 days. "
            "Step 5: IBLA reviews on written record (no oral argument typically). "
            "Step 6: IBLA issues written decision. "
            "Step 7: Reconsideration petition available within 60 days."
        ),
        key_factors=[
            "30-day appeal deadline",
            "Statement of Reasons required",
            "4-part stay test",
            "Written record review (no oral argument usually)",
            "IBLA written decision",
            "60-day reconsideration window",
            "Federal court review after IBLA exhaustion",
        ],
        primary_authority=[
            "43 CFR 4.410 (Who may appeal)",
            "43 CFR 4.411 (Appeal deadlines)",
            "43 CFR 4.413 (Stays)",
            "43 CFR 4.480 (IBLA decisions)",
        ],
        burden_holder="Appellant (demonstrating BLM error); BLM (defending decision)",
        adversary_position="IBLA may be slow to decide; stays are difficult to obtain absent clear irreparable harm.",
        counter_arguments=[
            "IBLA defers to BLM factual findings supported by substantial evidence",
            "Legal questions reviewed de novo",
            "Late-filed appeals are jurisdictionally barred",
        ],
        resolution_strategy=(
            "File within 30 days, no exceptions. Prepare thorough Statement of Reasons. "
            "If stay needed, address all 4 factors explicitly."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="43 CFR Part 4 Subpart E (IBLA procedures)",
        category="compliance",
    )


def _federal_right_of_way() -> DoctrineBlock:
    return DoctrineBlock(
        topic="federal_right_of_way",
        keywords=["right of way", "ROW", "pipeline ROW", "access road", "FLPMA ROW", "Title V", "right-of-way grant"],
        conclusion_template=(
            "Rights-of-way across federal land for oil and gas pipelines and access roads are granted under FLPMA Title V "
            "(43 CFR 2800). Applications are processed by BLM with NEPA review. ROW grants include rental payments, bond "
            "requirements, and terms and conditions for construction and reclamation."
        ),
        reasoning_framework=(
            "Step 1: Determine if access or pipeline crosses federal land. "
            "Step 2: File ROW application (SF-299) with BLM. "
            "Step 3: BLM processes with NEPA review. "
            "Step 4: If approved, ROW grant issued with terms, conditions, and rental schedule. "
            "Step 5: Grantee must post bond and pay annual rental. "
            "Step 6: ROW terms typically 30 years with renewal option. "
            "Step 7: Grantee must reclaim on expiration or abandonment."
        ),
        key_factors=[
            "FLPMA Title V ROW authority",
            "SF-299 application form",
            "NEPA review required",
            "Annual rental payments",
            "Bond requirements",
            "30-year typical term with renewal",
            "Reclamation obligations on expiration",
        ],
        primary_authority=[
            "43 USC 1761-1771 (FLPMA Title V)",
            "43 CFR 2800 (ROW regulations)",
            "BLM Manual 2800 (ROW processing)",
        ],
        burden_holder="Applicant (complete application, NEPA data); BLM (processing and oversight)",
        adversary_position="BLM may impose restrictive terms or deny ROW if inconsistent with RMP.",
        counter_arguments=[
            "ROW is not automatic - BLM has discretion to deny",
            "Temporary use permits available for short-term access",
            "ROW for oil and gas access may be included in APD surface use plan",
        ],
        resolution_strategy=(
            "File ROW application early in project planning. Coordinate with APD filing. "
            "Ensure NEPA analysis covers ROW footprint."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="43 CFR 2800 (comprehensive ROW regulatory framework)",
        category="permitting",
    )


def _resource_management_plan() -> DoctrineBlock:
    return DoctrineBlock(
        topic="resource_management_plan",
        keywords=["RMP", "resource management plan", "land use plan", "FLPMA planning", "RMP amendment", "management decision"],
        conclusion_template=(
            "Resource Management Plans (RMPs) under FLPMA govern all BLM land management decisions including which areas "
            "are open, closed, or subject to special restrictions for oil and gas leasing. RMPs require EIS-level NEPA "
            "review. All BLM oil and gas decisions must be consistent with the applicable RMP."
        ),
        reasoning_framework=(
            "Step 1: Identify the applicable RMP for the geographic area. "
            "Step 2: Review RMP decisions on fluid mineral management (open/closed/restrictions). "
            "Step 3: Verify proposed action is consistent with RMP. "
            "Step 4: If inconsistent, RMP amendment required before action can proceed. "
            "Step 5: RMP amendments require their own NEPA process. "
            "Step 6: RMPs are revised approximately every 15-20 years."
        ),
        key_factors=[
            "RMP governs all land management decisions",
            "Open/closed/restricted designations for O&G",
            "Consistency requirement for all BLM actions",
            "RMP amendment process for changes",
            "EIS-level NEPA for RMP/amendments",
            "Public participation in RMP process",
        ],
        primary_authority=[
            "43 USC 1712 (FLPMA land use planning)",
            "43 CFR 1600 (BLM planning regulations)",
            "BLM Land Use Planning Handbook H-1601-1",
        ],
        burden_holder="BLM (maintaining current RMPs); Industry (operating consistent with RMP)",
        adversary_position="Environmental groups may challenge RMP mineral decisions as too permissive; industry may challenge as too restrictive.",
        counter_arguments=[
            "RMP decisions are programmatic - site-specific review still required",
            "RMP consistency is mandatory, not discretionary",
            "Outdated RMPs may not reflect current policy or conditions",
        ],
        resolution_strategy=(
            "Review applicable RMP before any federal land investment. Participate in RMP revision processes. "
            "If RMP restricts desired development, assess amendment feasibility."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Norton v. Southern Utah Wilderness Alliance, 542 U.S. 55 (2004) (RMP management decisions)",
        category="planning",
    )


def _methane_waste_prevention() -> DoctrineBlock:
    return DoctrineBlock(
        topic="methane_waste_prevention",
        keywords=["methane", "venting", "flaring", "waste prevention", "NTL-4A", "methane rule", "gas capture"],
        conclusion_template=(
            "BLM's methane waste prevention rules regulate venting, flaring, and leaks from federal and tribal oil and gas "
            "operations. The current rule requires gas capture plans, limits on routine flaring, leak detection and repair "
            "(LDAR), and reporting. The IRA 2022 methane emissions charge adds a financial penalty on excessive emissions."
        ),
        reasoning_framework=(
            "Step 1: Determine applicable methane rule version (NTL-4A, 2016 rule, or current rule). "
            "Step 2: Operator must submit gas capture plan. "
            "Step 3: Routine venting prohibited; flaring limited to approved volumes. "
            "Step 4: LDAR inspections required at specified intervals. "
            "Step 5: Royalty owed on avoidably lost gas (vented/flared beyond allowance). "
            "Step 6: IRA methane charge applies to reported emissions above threshold. "
            "Step 7: State regulations may also apply (NM, CO have separate methane rules)."
        ),
        key_factors=[
            "Gas capture plan requirement",
            "Routine venting prohibition",
            "Flaring volume limits and approval",
            "LDAR inspection intervals",
            "Royalty on avoidably lost gas",
            "IRA methane emissions charge",
            "State methane rules (concurrent jurisdiction)",
        ],
        primary_authority=[
            "43 CFR 3179 (Waste Prevention)",
            "NTL-4A (legacy waste prevention notice)",
            "IRA 2022 Sec 60113 (Methane Emissions Charge)",
            "EPA 40 CFR Part 60 Subpart OOOOb",
        ],
        burden_holder="Operator (compliance with capture and reporting); BLM (enforcement); EPA (methane charge)",
        adversary_position="Environmental groups push for stricter limits; industry argues existing requirements adequate.",
        counter_arguments=[
            "Royalty obligation on wasted gas creates dual penalty with methane charge",
            "State rules may be more stringent than federal (NM Methane Rule)",
            "Gas capture infrastructure investment offsets compliance costs",
        ],
        resolution_strategy=(
            "Implement comprehensive gas capture infrastructure. Maintain LDAR program. "
            "Report accurately to avoid methane charge penalties."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="43 CFR 3179 (current waste prevention regulatory framework)",
        category="compliance",
    )


def _federal_inspection_enforcement() -> DoctrineBlock:
    return DoctrineBlock(
        topic="federal_inspection_enforcement",
        keywords=["inspection", "enforcement", "INC", "incident of noncompliance", "civil penalty", "BLM inspection"],
        conclusion_template=(
            "BLM inspects federal oil and gas operations for compliance with regulations, lease terms, and approved permits. "
            "Incidents of noncompliance (INCs) may result in orders to remedy, civil penalties, or lease cancellation for "
            "serious violations. BSEE handles offshore enforcement; BLM handles onshore federal and Indian lands."
        ),
        reasoning_framework=(
            "Step 1: BLM conducts routine and triggered inspections. "
            "Step 2: INCs documented with specific regulatory violation cited. "
            "Step 3: Minor INCs: corrective action required within specified timeframe. "
            "Step 4: Major INCs: immediate shut-in may be ordered. "
            "Step 5: Civil penalties assessed per 43 CFR 3163. "
            "Step 6: Penalty amounts based on severity, history, and good faith. "
            "Step 7: Repeat violations may lead to lease cancellation. "
            "Step 8: Operator may appeal INCs and penalties through IBLA."
        ),
        key_factors=[
            "Routine and triggered inspection authority",
            "INC documentation and citation",
            "Corrective action deadlines",
            "Shut-in authority for serious violations",
            "Civil penalty calculation factors",
            "Repeat violation escalation",
            "IBLA appeal rights",
        ],
        primary_authority=[
            "43 CFR 3163 (Noncompliance, Assessments, and Penalties)",
            "43 CFR 3162 (Requirements for Operating Rights Owners)",
            "30 USC 1719 (Civil penalties)",
        ],
        burden_holder="BLM (conducting inspections); Operator (compliance and corrective action)",
        adversary_position="BLM may assess penalties aggressively; operator may challenge INC basis or penalty amount.",
        counter_arguments=[
            "Self-reporting of violations may mitigate penalty amounts",
            "Good faith compliance efforts considered in penalty calculation",
            "IBLA reviews penalty assessments for reasonableness",
        ],
        resolution_strategy=(
            "Maintain compliance program with self-inspection. Respond to INCs promptly. "
            "Self-report violations where appropriate to mitigate penalties."
        ),
        entity_scope=EntityScope.FEDERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="43 CFR 3163 (comprehensive enforcement framework)",
        category="compliance",
    )


def _tribal_mineral_leasing() -> DoctrineBlock:
    return DoctrineBlock(
        topic="tribal_mineral_leasing",
        keywords=["tribal", "Indian", "BIA", "tribal lease", "Indian mineral", "IMLA", "tribal trust"],
        conclusion_template=(
            "Mineral leasing on tribal trust lands is governed by the Indian Mineral Leasing Act (IMLA) of 1938 and "
            "the Indian Mineral Development Act (IMDA) of 1982. BIA must approve all tribal mineral agreements. ONRR "
            "collects royalties for tribal leases. Tribal sovereignty adds unique consultation and approval requirements."
        ),
        reasoning_framework=(
            "Step 1: Determine if minerals are tribal trust or allotted. "
            "Step 2: Tribal council must approve mineral agreement. "
            "Step 3: BIA reviews and approves on behalf of trustee (Secretary of Interior). "
            "Step 4: IMLA lease: standard lease form; IMDA agreement: flexible terms. "
            "Step 5: NEPA review required for federal approval action. "
            "Step 6: ONRR handles royalty collection and distribution. "
            "Step 7: Tribal employment preferences and environmental conditions apply."
        ),
        key_factors=[
            "Tribal trust vs allotted distinction",
            "Tribal council approval required",
            "BIA approval as federal trustee action",
            "IMLA (standard) vs IMDA (flexible) agreements",
            "NEPA triggered by federal approval",
            "ONRR royalty collection for tribes",
            "Tribal sovereignty and consultation",
        ],
        primary_authority=[
            "25 USC 396a-396g (Indian Mineral Leasing Act)",
            "25 USC 2101-2108 (Indian Mineral Development Act)",
            "25 CFR 211-212 (Tribal mineral leasing regulations)",
            "25 CFR 225 (IMDA regulations)",
        ],
        burden_holder="Tribe (negotiation and approval); BIA (trustee review); Operator (compliance with tribal requirements)",
        adversary_position="Tribes may seek more favorable terms than standard IMLA; BIA may require additional protections.",
        counter_arguments=[
            "IMDA allows tribes to negotiate any terms they choose",
            "BIA trustee duty requires protecting tribal interests",
            "Federal trust responsibility overrides standard lease provisions",
        ],
        resolution_strategy=(
            "Engage tribal government directly and respectfully. Understand BIA approval timeline. "
            "Consider IMDA agreement for flexibility. Comply with all tribal requirements."
        ),
        entity_scope=EntityScope.TRIBAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Jicarilla Apache Tribe v. Supron Energy Corp., 728 F.2d 1555 (10th Cir. 1984)",
        category="leasing",
    )


def _allotted_tribal_lands() -> DoctrineBlock:
    return DoctrineBlock(
        topic="allotted_tribal_lands",
        keywords=["allotted", "allottee", "individual Indian", "fractionated", "AIPRA", "allotted minerals"],
        conclusion_template=(
            "Allotted Indian lands have individual Indian owners rather than tribal ownership. Mineral leasing requires "
            "consent of allottees owning a majority interest (under AIPRA). BIA administers leasing for allotted tracts. "
            "Fractionated ownership (many small interests from inheritance) complicates the consent process."
        ),
        reasoning_framework=(
            "Step 1: Determine allotted status and current ownership fractions. "
            "Step 2: Obtain consent from allottees owning majority interest (AIPRA threshold). "
            "Step 3: BIA may consent on behalf of missing or non-responsive allottees. "
            "Step 4: BIA reviews and approves lease. "
            "Step 5: Royalties distributed to individual allottees by BIA. "
            "Step 6: ONRR collects and BIA distributes royalty proceeds. "
            "Step 7: Highly fractionated tracts may use AIPRA streamlined consent."
        ),
        key_factors=[
            "Individual Indian ownership (not tribal)",
            "Fractionated interests from inheritance",
            "AIPRA majority consent threshold",
            "BIA consent for unresponsive allottees",
            "BIA lease approval required",
            "Individual royalty distribution",
            "ONRR collection, BIA distribution",
        ],
        primary_authority=[
            "25 USC 2201-2221 (AIPRA)",
            "25 CFR 212 (Leasing of allotted lands)",
            "25 USC 396 (Original allotted leasing authority)",
        ],
        burden_holder="Operator (obtaining consents); BIA (processing and approval); ONRR/BIA (royalty distribution)",
        adversary_position="Individual allottees may withhold consent; fractionation makes unanimous consent impossible.",
        counter_arguments=[
            "AIPRA streamlined consent reduces threshold for fractionated tracts",
            "BIA can consent for non-responsive owners under certain conditions",
            "Cotenancy law principles apply to allotted mineral interests",
        ],
        resolution_strategy=(
            "Research ownership fractions in BIA title records. Identify majority interest holders. "
            "Work with BIA to obtain necessary consents. Use AIPRA streamlined process where eligible."
        ),
        entity_scope=EntityScope.TRIBAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="AIPRA (25 USC 2201 et seq.) (streamlined consent for fractionated interests)",
        category="leasing",
    )


def _state_mineral_classification() -> DoctrineBlock:
    return DoctrineBlock(
        topic="state_mineral_classification",
        keywords=["mineral classification", "reclassification", "state minerals", "GLO classification", "mineral survey"],
        conclusion_template=(
            "State land offices classify lands as mineral or non-mineral, which determines leasing authority and revenue "
            "allocation. Reclassification may occur when mineral potential is discovered on lands previously classified as "
            "non-mineral. Texas GLO and New Mexico SLO maintain mineral classification records that are critical for title."
        ),
        reasoning_framework=(
            "Step 1: Review state land office classification records. "
            "Step 2: Determine if land was patented with mineral reservation. "
            "Step 3: If classified non-mineral but minerals discovered, reclassification possible. "
            "Step 4: Reclassification changes leasing authority and revenue allocation. "
            "Step 5: Title examination must verify mineral classification status. "
            "Step 6: Impact on surface owner rights depends on classification and state law."
        ),
        key_factors=[
            "Original land classification (mineral vs non-mineral)",
            "State patent terms and mineral reservations",
            "Reclassification triggers and process",
            "Impact on leasing authority",
            "Revenue allocation changes",
            "Title examination requirements",
        ],
        primary_authority=[
            "Texas Natural Resources Code Ch 51-52",
            "NMSA 1978 Sec 19-1 (NM land classification)",
            "State land office classification records",
        ],
        burden_holder="State land office (maintaining accurate classifications); Title examiner (verifying classification)",
        adversary_position="Surface owners may challenge reclassification that reduces their mineral rights.",
        counter_arguments=[
            "Classification records are conclusive unless challenged through proper process",
            "Reclassification is prospective, not retroactive",
            "Mineral reservation in patent is determinative regardless of classification",
        ],
        resolution_strategy=(
            "Always verify mineral classification in state land office records during title examination. "
            "If classification questionable, obtain certified copy of original patent."
        ),
        entity_scope=EntityScope.STATE_GENERAL,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="State land office administrative records and state statutory frameworks",
        category="state_leasing",
    )


def _orphan_well_program() -> DoctrineBlock:
    return DoctrineBlock(
        topic="orphan_well_program",
        keywords=["orphan well", "orphaned", "plugging program", "BIL", "infrastructure", "abandoned well", "federal program"],
        conclusion_template=(
            "The Bipartisan Infrastructure Law (2021) appropriated $4.7 billion for orphaned well plugging and site "
            "remediation. States receive formula and performance grants. Federal land orphan wells are plugged by DOI. "
            "The program prioritizes wells posing greatest environmental and safety risks."
        ),
        reasoning_framework=(
            "Step 1: Identify orphaned wells (no responsible operator, bonds insufficient). "
            "Step 2: Determine if well is on federal, state, private, or tribal land. "
            "Step 3: Federal wells: DOI manages plugging through BLM. "
            "Step 4: State wells: States apply for BIL grants. "
            "Step 5: Prioritize by environmental risk, safety, and community impact. "
            "Step 6: Plugging performed to state and federal standards. "
            "Step 7: Site remediation and reclamation included."
        ),
        key_factors=[
            "$4.7 billion BIL appropriation",
            "State formula and performance grants",
            "DOI direct plugging on federal lands",
            "Risk-based prioritization",
            "Plugging standards compliance",
            "Site remediation and reclamation",
            "Methane emission reduction benefits",
        ],
        primary_authority=[
            "Bipartisan Infrastructure Law Sec 40601 (Orphaned Well Program)",
            "30 USC 1751 (Federal orphan well authority)",
            "DOI Orphaned Wells Program Office guidance",
        ],
        burden_holder="DOI (federal wells); States (state grant programs); EPA (environmental standards)",
        adversary_position="Current operators may be compelled to plug wells they acquired through cheap acquisitions of distressed assets.",
        counter_arguments=[
            "Program focused on truly orphaned wells (no responsible party)",
            "Current operators of acquired wells remain responsible",
            "Bond forfeiture proceeds applied before federal/state funds",
        ],
        resolution_strategy=(
            "Inventory potential orphan well liability before acquisitions. "
            "Apply for state grant funding where eligible. "
            "Cooperate with DOI/state programs for legacy liability resolution."
        ),
        entity_scope=EntityScope.MULTI_JURISDICTION,
        confidence=ConfidenceLevel.DEFENSIBLE,
        controlling_precedent="Bipartisan Infrastructure Law Sec 40601 (statutory framework)",
        category="compliance",
    )
