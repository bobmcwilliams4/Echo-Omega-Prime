"""
LMIE Doctrine Extensions — Additional landman doctrine blocks.

These supplement the core doctrines embedded in engine.py with specialized
topics covering advanced landman practice areas.

Commander: Bobby Don McWilliams II | Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

from typing import Any, Dict, List

from loguru import logger
from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════
# EXTENDED DOCTRINE BLOCKS
# ═══════════════════════════════════════════════════════════════════

class ExtendedDoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    entity_scope: str = "general"
    confidence: str = "DEFENSIBLE"
    controlling_precedent: str = ""


EXTENDED_DOCTRINES: Dict[str, ExtendedDoctrineBlock] = {}


# ── TEXAS SPECIFIC: RELINQUISHMENT ACT ──

EXTENDED_DOCTRINES["texas_relinquishment_act"] = ExtendedDoctrineBlock(
    topic="texas_relinquishment_act",
    keywords=["relinquishment act", "state mineral", "free royalty", "vacancy", "school land"],
    conclusion_template="Under the Texas Relinquishment Act (TX Natural Resources Code §52.171 et seq.), the State of Texas retains a 1/16 free royalty interest in minerals under certain state school lands that were sold with mineral reservations. Surface owners of such lands may execute oil and gas leases on the State's behalf, with the State receiving its reserved royalty. Vacancy strips (unsurveyed land between patented surveys) belong to the State and require separate leasing from the GLO. Navigable waterway beds also contain State-owned minerals.",
    reasoning_framework="""1. Determine if tract originated from State school land patent with mineral reservation.
2. Check patent language for specific mineral reservation terms.
3. Verify if Relinquishment Act applies to the specific formation/depth.
4. Calculate State's free royalty interest (typically 1/16).
5. Determine surface owner's leasing authority under the Act.
6. Check for vacancy strip issues between surveys.
7. Evaluate navigable waterway implications for riverbed minerals.
8. Confirm GLO records for State mineral ownership.""",
    key_factors=[
        "State patent with mineral reservation verified",
        "Relinquishment Act applicability confirmed for formation",
        "State free royalty interest correctly calculated",
        "Surface owner leasing authority established",
        "Vacancy strips identified and addressed",
        "GLO records cross-referenced",
    ],
    primary_authority=[
        "TX Natural Resources Code §52.171 et seq. (Relinquishment Act)",
        "TX Natural Resources Code §51.001 et seq. (School land sales)",
        "State v. Magnolia Petroleum Co., 173 S.W.2d 186 (Tex. 1943)",
    ],
    entity_scope="state,surface_owner,lessee",
    confidence="DEFENSIBLE",
    controlling_precedent="TX Natural Resources Code §52.171",
)


# ── HORIZONTAL DRILLING AND FORCED POOLING ──

EXTENDED_DOCTRINES["horizontal_well_pooling"] = ExtendedDoctrineBlock(
    topic="horizontal_well_pooling",
    keywords=["horizontal well", "horizontal drilling", "lateral", "multi-section unit", "spacing", "proration unit"],
    conclusion_template="Horizontal well development in Texas requires pooling/unitization across multiple tracts and often multiple sections. The RRC grants spacing exceptions for horizontal wells under Statewide Rule 86, allowing multi-section proration units. Pooling authority must come from the lease pooling clause, and each tract's participation factor is calculated based on its proportionate acreage within the unit. Pugh clause implications are critical — depth-limited or horizontally-limited Pugh clauses may sever unpooled formations or acreage.",
    reasoning_framework="""1. Verify lease pooling clause authorizes multi-section units.
2. Check Pugh clause for depth/horizontal limitations.
3. Calculate participation factor: tract acreage / total unit acreage.
4. Verify RRC spacing permit and exceptions granted.
5. Evaluate allocation method: acreage-based vs production-based.
6. Check for anti-dilution provisions protecting small tracts.
7. Confirm all affected mineral owners' leases authorize pooling.
8. Document the pooling designation/declaration for recording.""",
    key_factors=[
        "Lease pooling clause authorizes size of proposed unit",
        "Pugh clause implications evaluated for all tracts",
        "Participation factors correctly calculated",
        "RRC spacing exception approved",
        "All mineral owners' lease authority verified",
    ],
    primary_authority=[
        "RRC Statewide Rule 86 (Horizontal well spacing)",
        "TX Natural Resources Code §102.011 (Force pooling)",
        "Pioneer Natural Resources v. Certain Mineral Interest Owners (horizontal pooling cases)",
    ],
    entity_scope="operator,mineral_owner,rrc",
    confidence="DEFENSIBLE",
    controlling_precedent="RRC Statewide Rule 86",
)


# ── DUHIG RULE ──

EXTENDED_DOCTRINES["duhig_rule_estoppel"] = ExtendedDoctrineBlock(
    topic="duhig_rule_estoppel",
    keywords=["duhig", "estoppel by deed", "after-acquired title", "warranty", "mineral reservation"],
    conclusion_template="The Duhig rule (Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503, 1940) provides that when a grantor conveys mineral interests by general warranty deed while simultaneously reserving a portion, but the grantor owns less than the full mineral estate, the reservation fails to the extent necessary to fulfill the warranty to the grantee. This is a form of estoppel by deed unique to mineral conveyances. The rule applies when: (1) the grantor conveys by warranty deed, (2) the grantor reserves minerals, (3) outstanding third-party interests make it impossible to honor both the grant and the reservation. Courts will honor the grant (to the warranted amount) and reduce the reservation.",
    reasoning_framework="""1. Identify the deed type — Duhig only applies to warranty deeds.
2. Determine what mineral interest the grantor actually owned at time of conveyance.
3. Parse the conveyance and reservation language.
4. Calculate whether outstanding third-party interests create a Duhig problem.
5. Apply Duhig: grantee gets warranted share first, reservation reduced.
6. Document the resulting ownership calculation.
7. Check for exceptions: special warranty, specific limitation language.
8. Evaluate after-acquired title implications.""",
    key_factors=[
        "General warranty deed used (required for Duhig)",
        "Grantor's actual mineral ownership at conveyance determined",
        "Outstanding third-party interests identified",
        "Duhig calculation shows reservation must be reduced",
        "No exceptions to Duhig applicability present",
    ],
    primary_authority=[
        "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
        "Benge v. Scharbauer, 259 S.W.2d 166 (Tex. 1953) (Duhig refinement)",
        "Harris v. Windsor, 294 S.W.2d 798 (Tex. 1956) (Duhig limitation)",
    ],
    entity_scope="grantor,grantee,third_party",
    confidence="DEFENSIBLE",
    controlling_precedent="Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
)


# ── EXECUTIVE RIGHTS ──

EXTENDED_DOCTRINES["executive_rights_minerals"] = ExtendedDoctrineBlock(
    topic="executive_rights_minerals",
    keywords=["executive rights", "right to lease", "non-participating", "npri", "npmi", "leasing authority"],
    conclusion_template="The executive right is the right to execute oil and gas leases on the mineral estate. It is one of the five sticks in the mineral estate bundle (executive, bonus, delay rental, royalty, right to develop). Executive rights may be severed from the mineral interest itself, creating a non-participating mineral interest (NPMI) or non-participating royalty interest (NPRI). The holder of executive rights owes a fiduciary-like duty of utmost good faith and fair dealing to the non-executive interest holders (Lesley v. Veterans Land Board, 352 S.W.3d 479). The executive right holder must consider the non-executive owner's interests when negotiating lease terms.",
    reasoning_framework="""1. Identify who holds executive rights in the mineral estate.
2. Determine if executive rights were severed from other mineral interests.
3. Classify non-executive interests: NPMI vs NPRI.
4. Evaluate the duty owed by executive to non-executive under Lesley standard.
5. Review lease terms for fairness to non-executive interests.
6. Check if bonus and delay rental payment obligations exist for non-executive.
7. Calculate royalty entitlement for non-participating interest holders.
8. Evaluate whether executive right holder has breached duty (self-dealing, unfair terms).""",
    key_factors=[
        "Executive right holder identified",
        "Non-executive interests classified (NPMI/NPRI)",
        "Duty of utmost good faith compliance evaluated",
        "Lease terms fair to non-executive interests",
        "Bonus/rental allocation properly handled",
        "Royalty entitlement correctly calculated for all parties",
    ],
    primary_authority=[
        "Lesley v. Veterans Land Board, 352 S.W.3d 479 (Tex. 2011)",
        "KCM Financial v. Bradshaw, 457 S.W.3d 70 (Tex. 2015) (executive duty refined)",
        "Day & Co. v. Texland Petroleum, 786 S.W.2d 667 (Tex. 1990)",
    ],
    entity_scope="executive_holder,non_participating_owner",
    confidence="DEFENSIBLE",
    controlling_precedent="Lesley v. Veterans Land Board, 352 S.W.3d 479 (Tex. 2011)",
)


# ── ADVERSE POSSESSION OF MINERAL INTERESTS ──

EXTENDED_DOCTRINES["adverse_possession_minerals"] = ExtendedDoctrineBlock(
    topic="adverse_possession_minerals",
    keywords=["adverse possession", "limitation title", "prescriptive rights", "hostile possession", "mineral adverse"],
    conclusion_template="Adverse possession of mineral interests in Texas is more restrictive than surface adverse possession. Under TX Civil Practice & Remedies Code §16.021-16.030, adverse possession of a severed mineral estate requires actual physical use of the minerals (drilling, production) for the statutory period — mere surface possession does not establish adverse possession of a severed mineral estate. The 3-year, 5-year, 10-year, and 25-year limitation periods each have specific requirements. Color of title enhances adverse possession claims. After mineral/surface severance, surface possession alone cannot ripen into mineral title.",
    reasoning_framework="""1. Determine if mineral estate is severed from surface.
2. If severed: surface possession alone cannot adversely possess minerals.
3. Identify the specific limitation statute claimed (3/5/10/25 year).
4. Evaluate elements: actual possession, hostile, open, notorious, continuous.
5. For minerals: must show actual use of minerals (production, drilling).
6. Check for color of title (recorded instrument purporting to convey).
7. Evaluate tax payment history (some statutes require tax payment).
8. Calculate statutory period from commencement of adverse use.""",
    key_factors=[
        "Mineral estate severance status determined",
        "Actual mineral use (not just surface possession) established",
        "All statutory elements met for claimed limitation period",
        "Color of title enhances claim",
        "Tax payments made during limitation period",
        "Continuous and uninterrupted possession for full statutory period",
    ],
    primary_authority=[
        "TX Civil Practice & Remedies Code §16.021-16.030",
        "Kinder Morgan North Texas Pipeline v. Justiss, 202 S.W.3d 427 (Tex. App. 2006)",
        "Natural Gas Pipeline Co. v. Pool, 124 S.W.3d 188 (Tex. 2003)",
    ],
    entity_scope="adverse_possessor,record_owner",
    confidence="DEFENSIBLE",
    controlling_precedent="TX Civil Practice & Remedies Code §16.021 et seq.",
)


# ── TRESPASS TO TRY TITLE ──

EXTENDED_DOCTRINES["trespass_try_title"] = ExtendedDoctrineBlock(
    topic="trespass_try_title",
    keywords=["trespass to try title", "quiet title", "cloud removal", "title litigation", "declaratory judgment"],
    conclusion_template="Trespass to try title (TX Property Code §22.001) is the statutory remedy for resolving disputed title to real property in Texas. The plaintiff must recover on the strength of their own title, not the weakness of the defendant's. The action is used to remove clouds on title, establish ownership, and quiet title against adverse claims. A declaratory judgment action under TX Civil Practice & Remedies Code Ch. 37 may also be used for title disputes. Lis pendens may be filed to provide notice of pending title litigation.",
    reasoning_framework="""1. Determine the specific title dispute (competing claims, cloud removal, boundary).
2. Evaluate plaintiff's chain of title — must establish superior title from common source.
3. Identify all necessary parties (all persons claiming interest in the property).
4. Consider declaratory judgment as alternative or supplement to trespass to try title.
5. Evaluate whether lis pendens notice should be filed.
6. Analyze statute of limitations for the underlying claim.
7. Consider whether mediation or settlement is appropriate.
8. Prepare title evidence (abstracts, deed records, surveys).""",
    key_factors=[
        "Plaintiff establishes superior title from common source",
        "All necessary parties joined in the action",
        "Statute of limitations not expired",
        "Title evidence properly compiled and authenticated",
        "Lis pendens filed if appropriate",
    ],
    primary_authority=[
        "TX Property Code §22.001 (Trespass to try title)",
        "TX Civil Practice & Remedies Code Ch. 37 (Declaratory judgment)",
        "Martin v. Amerman, 133 S.W.3d 262 (Tex. 2004) (common source doctrine)",
    ],
    entity_scope="plaintiff,defendant",
    confidence="DEFENSIBLE",
    controlling_precedent="TX Property Code §22.001",
)


# ═══════════════════════════════════════════════════════════════════
# DOCTRINE INTERACTION EDGES — Cross-doctrine dependencies
# ═══════════════════════════════════════════════════════════════════

INTERACTION_EDGES: List[Dict[str, str]] = [
    {"from": "chain_of_title_sovereignty_trace", "to": "mineral_surface_severance", "relationship": "Chain reveals severance points"},
    {"from": "mineral_surface_severance", "to": "oil_gas_lease_habendum", "relationship": "Severed mineral estate is leased"},
    {"from": "oil_gas_lease_habendum", "to": "division_order_interest_calculation", "relationship": "Lease terms define royalty split"},
    {"from": "oil_gas_lease_habendum", "to": "pooling_unitization_texas", "relationship": "Pooling clause in lease controls"},
    {"from": "division_order_interest_calculation", "to": "duhig_rule_estoppel", "relationship": "Duhig affects interest calculations"},
    {"from": "chain_of_title_sovereignty_trace", "to": "title_curative_instruments", "relationship": "Chain gaps require curative"},
    {"from": "title_curative_instruments", "to": "probate_heirship_mineral_interests", "relationship": "Probate gaps common curative need"},
    {"from": "mineral_surface_severance", "to": "easement_scope_abandonment", "relationship": "Severed estates affect easement analysis"},
    {"from": "mineral_surface_severance", "to": "right_of_way_eminent_domain", "relationship": "ROW impacts both estates"},
    {"from": "mineral_surface_severance", "to": "executive_rights_minerals", "relationship": "Executive rights part of mineral bundle"},
    {"from": "chain_of_title_sovereignty_trace", "to": "adverse_possession_minerals", "relationship": "Chain gaps may trigger AP claims"},
    {"from": "adverse_possession_minerals", "to": "trespass_try_title", "relationship": "AP disputed via trespass action"},
    {"from": "oil_gas_lease_habendum", "to": "lease_negotiation_terms", "relationship": "Habendum is key negotiation term"},
    {"from": "pooling_unitization_texas", "to": "horizontal_well_pooling", "relationship": "Horizontal wells require large pools"},
    {"from": "federal_blm_leasing", "to": "indian_land_oil_gas", "relationship": "Some tribal land under federal jurisdiction"},
    {"from": "right_of_way_eminent_domain", "to": "renewable_energy_surface_use", "relationship": "Transmission ROW for renewables"},
    {"from": "chain_of_title_sovereignty_trace", "to": "texas_relinquishment_act", "relationship": "State patent origin triggers RA"},
    {"from": "water_rights_texas", "to": "due_diligence_og_acquisition", "relationship": "Water rights part of acquisition DD"},
    {"from": "title_curative_instruments", "to": "trespass_try_title", "relationship": "Litigation as last-resort curative"},
]


def get_all_doctrines() -> Dict[str, Any]:
    """Return all extended doctrines for the engine."""
    return {topic: block.model_dump() for topic, block in EXTENDED_DOCTRINES.items()}


def get_interaction_graph() -> Dict[str, Any]:
    """Return the doctrine interaction graph."""
    return {
        "nodes": list(EXTENDED_DOCTRINES.keys()),
        "edges": INTERACTION_EDGES,
        "edge_count": len(INTERACTION_EDGES),
    }


logger.info("LMIE extended doctrines loaded: {} topics, {} interaction edges", len(EXTENDED_DOCTRINES), len(INTERACTION_EDGES))
