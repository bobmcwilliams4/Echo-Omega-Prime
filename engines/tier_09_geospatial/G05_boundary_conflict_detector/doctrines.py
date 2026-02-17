from dataclasses import dataclass
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
        topic="Survey Overlap Resolution - Texas",
        keywords=["survey overlap", "boundary conflict", "Texas", "resolution", "tracts"],
        conclusion_template="Where two surveys overlap, the senior survey prevails unless evidence demonstrates the junior survey's boundaries were established first.",
        reasoning_framework=(
            "Resolution of survey overlaps in Texas requires a hierarchical analysis of survey dates, "
            "patent issuance, and physical evidence. The senior survey, defined by earlier patent or "
            "field notes, generally controls. If the junior survey was monumented or occupied prior to "
            "the senior survey's patent, courts may favor the junior survey. The doctrine considers "
            "intent of the original surveyor, presence of monuments, and reliance by landowners. "
            "Extrinsic evidence such as witness testimony, historical maps, and chain of title documents "
            "may be admitted to clarify ambiguous boundaries. The burden is on the party asserting the "
            "junior survey's priority to prove its establishment predates the senior survey. The doctrine "
            "also weighs public policy favoring certainty and stability in land titles. Where both surveys "
            "were conducted contemporaneously, the doctrine looks to physical occupation and acquiescence. "
            "Resolution may involve re-surveying, negotiation, or judicial determination. The controlling "
            "precedent is State v. Balli, 1951, which established the primacy of senior surveys unless "
            "contradicted by compelling evidence."
        ),
        key_factors=[
            "Date of survey",
            "Date of patent issuance",
            "Presence of monuments",
            "Physical occupation",
            "Chain of title",
            "Intent of surveyor",
            "Reliance by landowners"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "State v. Balli, 1951",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Junior survey claimant",
        adversary_position="Senior survey controls unless junior survey's boundaries were monumented or occupied first.",
        counter_arguments=[
            "Senior survey is ambiguous or defective.",
            "Junior survey was physically established and relied upon.",
            "Public policy favors junior survey due to longstanding occupation."
        ],
        resolution_strategy="Hierarchical analysis of survey dates, monuments, and occupation; judicial determination if unresolved.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Balli, 1951"
    ),
    DoctrineBlock(
        topic="Vacancy Strip Detection",
        keywords=["vacancy", "strip", "boundary", "detection", "survey gap"],
        conclusion_template="Vacancy strips are identified where survey boundaries fail to close, leaving unpatented land between tracts.",
        reasoning_framework=(
            "Vacancy strip detection involves analyzing survey field notes, plat maps, and patent records "
            "to identify unpatented gaps between surveyed tracts. The doctrine requires careful review of "
            "metes and bounds descriptions, closure calculations, and monument placement. Vacancies often "
            "arise from surveyor error, ambiguous calls, or intentional omission. The doctrine distinguishes "
            "between true vacancies and overlapping claims. The burden is on the claimant to demonstrate the "
            "existence of a vacancy by showing the absence of patent or title, and that the area was not "
            "included in any adjacent survey. Courts rely on expert testimony, historical records, and "
            "geospatial analysis to confirm the vacancy. The doctrine is guided by Texas General Land Office "
            "procedures and relevant case law. Resolution may involve patenting the vacancy, judicial "
            "determination, or administrative correction."
        ),
        key_factors=[
            "Survey closure calculations",
            "Metes and bounds descriptions",
            "Plat map analysis",
            "Patent records",
            "Monument placement",
            "Historical survey practices"
        ],
        primary_authority=[
            "Texas General Land Office rules",
            "Texas Natural Resources Code § 21.011",
            "State v. Balli, 1951"
        ],
        burden_holder="Vacancy claimant",
        adversary_position="No vacancy exists; area was included in adjacent survey.",
        counter_arguments=[
            "Survey closure was accurate.",
            "Area was patented under adjacent survey.",
            "Vacancy is result of surveyor error, not legal omission."
        ],
        resolution_strategy="Geospatial analysis, expert testimony, administrative correction.",
        entity_scope="Texas landowners, surveyors, GLO",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Balli, 1951"
    ),
    DoctrineBlock(
        topic="Junior vs Senior Survey Priority",
        keywords=["junior survey", "senior survey", "priority", "boundary conflict"],
        conclusion_template="The senior survey prevails unless the junior survey was monumented or occupied first, or the senior survey is defective.",
        reasoning_framework=(
            "Priority between junior and senior surveys is determined by date of survey, patent issuance, "
            "and physical evidence. The senior survey, typically the earliest in date, is presumed to control "
            "the boundaries. Exceptions arise where the junior survey was monumented, occupied, or relied upon "
            "prior to the senior survey's patent. The doctrine considers the intent of the surveyor, presence "
            "of monuments, and chain of title. Courts may admit extrinsic evidence to resolve ambiguities. "
            "The burden is on the junior survey claimant to prove priority by physical establishment or reliance. "
            "Resolution involves judicial determination based on evidence and controlling precedent."
        ),
        key_factors=[
            "Survey dates",
            "Patent issuance",
            "Monument placement",
            "Physical occupation",
            "Chain of title"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "State v. Balli, 1951"
        ],
        burden_holder="Junior survey claimant",
        adversary_position="Senior survey controls unless junior survey's boundaries were established first.",
        counter_arguments=[
            "Senior survey is ambiguous.",
            "Junior survey was physically established.",
            "Public policy favors junior survey."
        ],
        resolution_strategy="Judicial determination based on evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="State v. Balli, 1951"
    ),
    DoctrineBlock(
        topic="Excess and Deficit in Survey Area",
        keywords=["excess", "deficit", "survey area", "boundary", "tract size"],
        conclusion_template="Excess or deficit in survey area is resolved by adhering to original monuments and intent, not mathematical area.",
        reasoning_framework=(
            "When a survey's area exceeds or falls short of its stated acreage, resolution focuses on original "
            "monuments, field notes, and intent of the surveyor. Mathematical area is secondary to physical "
            "boundaries established by monuments. The doctrine recognizes that surveyor errors, terrain, and "
            "measurement limitations often result in excess or deficit. Courts prioritize physical evidence "
            "and historical occupation over stated acreage. The burden is on the party contesting the boundary "
            "to prove error or fraud. Resolution may involve re-surveying, judicial determination, or "
            "negotiation. Controlling precedent is Texas Supreme Court cases favoring monuments over area."
        ),
        key_factors=[
            "Original monuments",
            "Field notes",
            "Intent of surveyor",
            "Historical occupation",
            "Mathematical area"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party contesting boundary",
        adversary_position="Physical boundaries control over stated acreage.",
        counter_arguments=[
            "Monuments are missing or ambiguous.",
            "Mathematical area is critical for title.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to original monuments and intent.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Gap Detection Between Tracts",
        keywords=["gap", "boundary", "detection", "survey", "tracts"],
        conclusion_template="Gaps between tracts are identified by analyzing survey closure and field notes, and resolved by administrative correction or patenting.",
        reasoning_framework=(
            "Detection of gaps between surveyed tracts requires review of field notes, plat maps, and closure "
            "calculations. Gaps may arise from surveyor error, ambiguous calls, or intentional omission. The "
            "doctrine distinguishes between true gaps and overlapping claims. The burden is on the claimant to "
            "demonstrate the existence of a gap by showing the absence of patent or title. Courts rely on expert "
            "testimony, historical records, and geospatial analysis. Resolution may involve patenting the gap, "
            "administrative correction, or judicial determination."
        ),
        key_factors=[
            "Survey closure calculations",
            "Field notes",
            "Plat map analysis",
            "Patent records"
        ],
        primary_authority=[
            "Texas General Land Office rules",
            "Texas Natural Resources Code § 21.011"
        ],
        burden_holder="Gap claimant",
        adversary_position="No gap exists; area was included in adjacent survey.",
        counter_arguments=[
            "Survey closure was accurate.",
            "Area was patented under adjacent survey.",
            "Gap is result of surveyor error, not legal omission."
        ],
        resolution_strategy="Geospatial analysis, expert testimony, administrative correction.",
        entity_scope="Texas landowners, surveyors, GLO",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas General Land Office rules"
    ),
    DoctrineBlock(
        topic="Closure Error Analysis",
        keywords=["closure error", "survey", "boundary", "analysis", "mathematical error"],
        conclusion_template="Closure errors are analyzed mathematically and resolved by adhering to original monuments and intent.",
        reasoning_framework=(
            "Closure error analysis involves mathematical review of survey bearings and distances to determine "
            "if the survey closes properly. Errors may arise from measurement inaccuracies, terrain, or "
            "surveying equipment limitations. The doctrine prioritizes original monuments and field notes over "
            "mathematical closure. Courts recognize that minor closure errors do not invalidate boundaries if "
            "monuments and occupation are clear. The burden is on the party contesting the boundary to prove "
            "significant error or fraud. Resolution may involve re-surveying, judicial determination, or "
            "negotiation."
        ),
        key_factors=[
            "Mathematical closure calculations",
            "Original monuments",
            "Field notes",
            "Measurement accuracy"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party contesting boundary",
        adversary_position="Original monuments control over mathematical closure.",
        counter_arguments=[
            "Monuments are missing or ambiguous.",
            "Closure error is significant and affects title.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to original monuments and intent.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Metes and Bounds Traversal",
        keywords=["metes and bounds", "traversal", "survey", "boundary", "description"],
        conclusion_template="Metes and bounds descriptions are traversed in sequence, with monuments controlling over bearings and distances.",
        reasoning_framework=(
            "Metes and bounds traversal involves following the sequence of calls in the survey description, "
            "prioritizing monuments over bearings and distances. The doctrine recognizes that physical evidence "
            "and occupation may supersede mathematical calculations. Courts rely on field notes, historical maps, "
            "and witness testimony to resolve ambiguities. The burden is on the party contesting the boundary to "
            "prove error or fraud. Resolution may involve re-surveying, judicial determination, or negotiation."
        ),
        key_factors=[
            "Sequence of calls",
            "Monument placement",
            "Field notes",
            "Historical maps"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party contesting boundary",
        adversary_position="Monuments control over bearings and distances.",
        counter_arguments=[
            "Monuments are missing or ambiguous.",
            "Sequence of calls is defective.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to sequence of calls and monuments.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Bearing Tree and Monument Calls",
        keywords=["bearing tree", "monument", "calls", "survey", "boundary"],
        conclusion_template="Bearing trees and monuments control boundaries over mathematical calls and distances.",
        reasoning_framework=(
            "The doctrine of bearing tree and monument calls holds that physical evidence of bearing trees, "
            "stones, posts, or other monuments controls boundary location over mathematical calls and distances. "
            "Surveyors must prioritize monuments described in field notes and plat maps. Courts recognize that "
            "monuments provide certainty and stability in boundary determination. The burden is on the party "
            "contesting the boundary to prove the monument is missing, ambiguous, or fraudulent. Resolution may "
            "involve re-surveying, expert testimony, or judicial determination."
        ),
        key_factors=[
            "Presence of bearing trees",
            "Monument placement",
            "Field notes",
            "Plat maps"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party contesting boundary",
        adversary_position="Monuments control over mathematical calls.",
        counter_arguments=[
            "Monuments are missing or ambiguous.",
            "Mathematical calls are more reliable.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to monuments and physical evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Natural Boundary Interpretation",
        keywords=["natural boundary", "interpretation", "river", "creek", "survey"],
        conclusion_template="Natural boundaries such as rivers and creeks control over artificial monuments and mathematical calls.",
        reasoning_framework=(
            "Interpretation of natural boundaries requires analysis of field notes, historical maps, and physical "
            "evidence. Rivers, creeks, and other natural features control boundary location over artificial monuments "
            "and mathematical calls. The doctrine recognizes that natural boundaries may change over time due to "
            "accretion or avulsion. Courts rely on expert testimony, geospatial analysis, and historical records. "
            "The burden is on the party contesting the boundary to prove error or fraud. Resolution may involve "
            "re-surveying, judicial determination, or negotiation."
        ),
        key_factors=[
            "Presence of natural boundary",
            "Field notes",
            "Historical maps",
            "Physical evidence"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party contesting boundary",
        adversary_position="Natural boundaries control over artificial monuments.",
        counter_arguments=[
            "Natural boundary has changed due to accretion or avulsion.",
            "Artificial monuments are more reliable.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to natural boundaries and physical evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Accretion and Avulsion Rules",
        keywords=["accretion", "avulsion", "natural boundary", "river", "survey"],
        conclusion_template="Boundaries move with gradual accretion but remain fixed with sudden avulsion.",
        reasoning_framework=(
            "The doctrine distinguishes between accretion, the gradual and imperceptible addition of land by "
            "natural forces, and avulsion, the sudden and perceptible change. Boundaries move with accretion, "
            "reflecting the new course of the river or creek. In cases of avulsion, boundaries remain fixed at "
            "their pre-event location. Courts rely on expert testimony, historical records, and geospatial analysis "
            "to determine the nature of the change. The burden is on the party asserting boundary movement to prove "
            "accretion or avulsion. Resolution may involve judicial determination, negotiation, or administrative "
            "correction."
        ),
        key_factors=[
            "Nature of boundary change",
            "Expert testimony",
            "Historical records",
            "Geospatial analysis"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting boundary movement",
        adversary_position="Boundary remains fixed unless accretion is proven.",
        counter_arguments=[
            "Change was sudden and perceptible (avulsion).",
            "Boundary should remain fixed for stability.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Judicial determination based on evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Resurvey Procedures",
        keywords=["resurvey", "procedures", "boundary", "survey", "correction"],
        conclusion_template="Resurveys are conducted to correct errors, clarify boundaries, and must adhere to original monuments and field notes.",
        reasoning_framework=(
            "Resurvey procedures are governed by Texas General Land Office rules and relevant statutes. Resurveys "
            "are conducted to correct errors, clarify boundaries, or resolve disputes. Surveyors must adhere to "
            "original monuments, field notes, and intent of the original surveyor. Courts recognize that resurveys "
            "cannot alter boundaries established by original monuments unless fraud or error is proven. The burden "
            "is on the party seeking correction to prove error or ambiguity. Resolution may involve judicial "
            "determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Original monuments",
            "Field notes",
            "Intent of surveyor",
            "Surveyor error"
        ],
        primary_authority=[
            "Texas General Land Office rules",
            "Texas Natural Resources Code § 21.011"
        ],
        burden_holder="Party seeking correction",
        adversary_position="Original boundaries control unless error is proven.",
        counter_arguments=[
            "Monuments are missing or ambiguous.",
            "Resurvey alters established boundaries.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to original monuments and field notes.",
        entity_scope="Texas landowners, surveyors, GLO",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas General Land Office rules"
    ),
    DoctrineBlock(
        topic="Survey Call Hierarchy",
        keywords=["survey call", "hierarchy", "boundary", "monument", "description"],
        conclusion_template="Survey call hierarchy prioritizes natural boundaries, artificial monuments, and course and distance in that order.",
        reasoning_framework=(
            "The hierarchy of survey calls is established by Texas Supreme Court precedent and survey practice. "
            "Natural boundaries control over artificial monuments, which control over course and distance. The "
            "doctrine recognizes that physical evidence provides certainty and stability. Surveyors must prioritize "
            "calls in accordance with the hierarchy. Courts rely on field notes, historical maps, and expert testimony "
            "to resolve ambiguities. The burden is on the party contesting the boundary to prove error or fraud. "
            "Resolution may involve re-surveying, judicial determination, or negotiation."
        ),
        key_factors=[
            "Presence of natural boundary",
            "Artificial monuments",
            "Course and distance",
            "Field notes"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party contesting boundary",
        adversary_position="Hierarchy of calls must be followed.",
        counter_arguments=[
            "Monuments are missing or ambiguous.",
            "Natural boundary has changed.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to hierarchy of calls and physical evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Patent vs. Deed Conflict",
        keywords=["patent", "deed", "conflict", "boundary", "title"],
        conclusion_template="Patent boundaries control over deed descriptions unless fraud or error is proven.",
        reasoning_framework=(
            "Conflicts between patent and deed boundaries are resolved by prioritizing the boundaries described in "
            "the patent, which represents the original grant from the sovereign. Deed descriptions may clarify but "
            "cannot alter patent boundaries unless fraud or error is proven. Courts rely on field notes, historical "
            "records, and chain of title documents. The burden is on the party seeking to alter patent boundaries "
            "to prove fraud or error. Resolution may involve judicial determination, negotiation, or administrative "
            "correction."
        ),
        key_factors=[
            "Patent boundaries",
            "Deed descriptions",
            "Field notes",
            "Chain of title"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party seeking to alter patent boundaries",
        adversary_position="Patent boundaries control unless fraud or error is proven.",
        counter_arguments=[
            "Patent is ambiguous or defective.",
            "Deed clarifies boundary.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to patent boundaries and field notes.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Railroad Survey Strip Conflicts",
        keywords=["railroad", "survey", "strip", "conflict", "boundary"],
        conclusion_template="Railroad survey strips are resolved by adhering to original survey boundaries and intent, with priority to public use.",
        reasoning_framework=(
            "Conflicts involving railroad survey strips require analysis of original survey boundaries, field notes, "
            "and intent of the surveyor. The doctrine recognizes the public use and necessity of railroad corridors. "
            "Courts prioritize boundaries established by original monuments and occupation. The burden is on the party "
            "contesting the boundary to prove error or ambiguity. Resolution may involve re-surveying, judicial "
            "determination, or negotiation."
        ),
        key_factors=[
            "Original survey boundaries",
            "Field notes",
            "Intent of surveyor",
            "Public use"
        ],
        primary_authority=[
            "Texas General Land Office rules",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party contesting boundary",
        adversary_position="Original boundaries control unless error is proven.",
        counter_arguments=[
            "Monuments are missing or ambiguous.",
            "Public use justifies adjustment.",
            "Surveyor error justifies correction."
        ],
        resolution_strategy="Adherence to original boundaries and public use.",
        entity_scope="Texas landowners, surveyors, railroads",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Spanish and Mexican Land Grant Boundaries",
        keywords=["Spanish grant", "Mexican grant", "boundary", "survey", "historical"],
        conclusion_template="Spanish and Mexican land grant boundaries are interpreted according to original grant documents, field notes, and historical occupation.",
        reasoning_framework=(
            "Interpretation of Spanish and Mexican land grant boundaries requires review of original grant documents, "
            "field notes, and historical maps. The doctrine recognizes the unique legal framework of pre-statehood "
            "grants. Courts rely on expert testimony, historical records, and chain of title documents. The burden is "
            "on the party contesting the boundary to prove error or ambiguity. Resolution may involve judicial "
            "determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Original grant documents",
            "Field notes",
            "Historical maps",
            "Chain of title"
        ],
        primary_authority=[
            "Texas General Land Office rules",
            "Texas Supreme Court decisions",
            "Spanish and Mexican law"
        ],
        burden_holder="Party contesting boundary",
        adversary_position="Original grant boundaries control unless error is proven.",
        counter_arguments=[
            "Grant documents are ambiguous.",
            "Historical occupation clarifies boundary.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to original grant documents and historical evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Mineral Reservation Boundary Disputes",
        keywords=["mineral reservation", "boundary", "dispute", "surface", "subsurface"],
        conclusion_template="Mineral reservation boundaries are interpreted according to deed language, survey boundaries, and intent of parties.",
        reasoning_framework=(
            "Disputes over mineral reservation boundaries require analysis of deed language, survey boundaries, and "
            "intent of the parties. The doctrine distinguishes between surface and subsurface boundaries. Courts rely "
            "on field notes, chain of title documents, and expert testimony. The burden is on the party asserting "
            "mineral rights to prove reservation and boundary. Resolution may involve judicial determination, "
            "negotiation, or administrative correction."
        ),
        key_factors=[
            "Deed language",
            "Survey boundaries",
            "Intent of parties",
            "Chain of title"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting mineral rights",
        adversary_position="Surface boundaries control unless deed specifies otherwise.",
        counter_arguments=[
            "Deed is ambiguous.",
            "Survey boundaries are defective.",
            "Intent of parties clarifies boundary."
        ],
        resolution_strategy="Adherence to deed language and survey boundaries.",
        entity_scope="Texas landowners, surveyors, mineral owners",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Surface vs. Subsurface Boundary Divergence",
        keywords=["surface boundary", "subsurface boundary", "divergence", "survey", "mineral rights"],
        conclusion_template="Surface boundaries control unless deed or reservation specifies subsurface boundary divergence.",
        reasoning_framework=(
            "Divergence between surface and subsurface boundaries is resolved by analyzing deed language, survey "
            "boundaries, and intent of the parties. The doctrine recognizes that surface boundaries generally control "
            "unless the deed or reservation specifies otherwise. Courts rely on field notes, chain of title documents, "
            "and expert testimony. The burden is on the party asserting subsurface boundary divergence to prove "
            "reservation and boundary. Resolution may involve judicial determination, negotiation, or administrative "
            "correction."
        ),
        key_factors=[
            "Deed language",
            "Survey boundaries",
            "Intent of parties",
            "Chain of title"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting subsurface boundary divergence",
        adversary_position="Surface boundaries control unless deed specifies otherwise.",
        counter_arguments=[
            "Deed is ambiguous.",
            "Survey boundaries are defective.",
            "Intent of parties clarifies boundary."
        ],
        resolution_strategy="Adherence to deed language and survey boundaries.",
        entity_scope="Texas landowners, surveyors, mineral owners",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Boundary by Acquiescence",
        keywords=["boundary", "acquiescence", "agreement", "survey", "occupation"],
        conclusion_template="Boundaries established by acquiescence are recognized where parties have mutually accepted and occupied the boundary for a long period.",
        reasoning_framework=(
            "Boundary by acquiescence is established where adjoining landowners have mutually accepted and occupied a "
            "boundary for a long period, regardless of survey or title. The doctrine requires evidence of mutual "
            "acceptance, physical occupation, and absence of dispute. Courts rely on witness testimony, historical "
            "records, and physical evidence. The burden is on the party asserting acquiescence to prove mutual "
            "acceptance and occupation. Resolution may involve judicial determination, negotiation, or administrative "
            "correction."
        ),
        key_factors=[
            "Mutual acceptance",
            "Physical occupation",
            "Absence of dispute",
            "Historical records"
        ],
        primary_authority=[
            "Texas Supreme Court decisions",
            "Texas Property Code"
        ],
        burden_holder="Party asserting acquiescence",
        adversary_position="Survey boundaries control unless acquiescence is proven.",
        counter_arguments=[
            "No mutual acceptance.",
            "Physical occupation is ambiguous.",
            "Dispute existed during occupation."
        ],
        resolution_strategy="Judicial determination based on evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Agreed Boundary Doctrine",
        keywords=["agreed boundary", "doctrine", "survey", "boundary", "agreement"],
        conclusion_template="Agreed boundaries are recognized where parties have expressly agreed to a boundary and occupied it, regardless of survey or title.",
        reasoning_framework=(
            "The agreed boundary doctrine holds that boundaries expressly agreed to by adjoining landowners and "
            "occupied are recognized regardless of survey or title. The doctrine requires evidence of express "
            "agreement, physical occupation, and absence of dispute. Courts rely on witness testimony, historical "
            "records, and physical evidence. The burden is on the party asserting the agreed boundary to prove "
            "agreement and occupation. Resolution may involve judicial determination, negotiation, or administrative "
            "correction."
        ),
        key_factors=[
            "Express agreement",
            "Physical occupation",
            "Absence of dispute",
            "Historical records"
        ],
        primary_authority=[
            "Texas Supreme Court decisions",
            "Texas Property Code"
        ],
        burden_holder="Party asserting agreed boundary",
        adversary_position="Survey boundaries control unless agreement is proven.",
        counter_arguments=[
            "No express agreement.",
            "Physical occupation is ambiguous.",
            "Dispute existed during occupation."
        ],
        resolution_strategy="Judicial determination based on evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Adverse Possession and Boundary Disputes",
        keywords=["adverse possession", "boundary", "dispute", "survey", "occupation"],
        conclusion_template="Boundaries may be altered by adverse possession where statutory requirements are met.",
        reasoning_framework=(
            "Adverse possession may alter boundaries where statutory requirements are met, including open and notorious "
            "occupation, exclusive possession, and continuous use for the statutory period. The doctrine requires "
            "evidence of physical occupation, intent, and absence of dispute. Courts rely on witness testimony, "
            "historical records, and physical evidence. The burden is on the party asserting adverse possession to "
            "prove all elements. Resolution may involve judicial determination, negotiation, or administrative "
            "correction."
        ),
        key_factors=[
            "Open and notorious occupation",
            "Exclusive possession",
            "Continuous use",
            "Statutory period"
        ],
        primary_authority=[
            "Texas Civil Practice and Remedies Code § 16.021",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting adverse possession",
        adversary_position="Survey boundaries control unless adverse possession is proven.",
        counter_arguments=[
            "Occupation was not exclusive.",
            "Statutory period not met.",
            "Dispute existed during occupation."
        ],
        resolution_strategy="Judicial determination based on evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Boundary Line Agreement Recording",
        keywords=["boundary line agreement", "recording", "survey", "title", "dispute"],
        conclusion_template="Boundary line agreements must be recorded to be binding on successors in interest.",
        reasoning_framework=(
            "Boundary line agreements between adjoining landowners must be recorded in the county records to be binding "
            "on successors in interest. The doctrine recognizes the importance of public notice and title stability. "
            "Courts rely on deed records, witness testimony, and physical evidence. The burden is on the party asserting "
            "the agreement to prove recording and notice. Resolution may involve judicial determination, negotiation, or "
            "administrative correction."
        ),
        key_factors=[
            "Recording of agreement",
            "Public notice",
            "Deed records",
            "Physical evidence"
        ],
        primary_authority=[
            "Texas Property Code § 12.001",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting boundary line agreement",
        adversary_position="Agreement is not binding unless recorded.",
        counter_arguments=[
            "Agreement was not recorded.",
            "No public notice.",
            "Dispute existed during agreement."
        ],
        resolution_strategy="Recording in county records and judicial determination.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Riparian Boundary Determination",
        keywords=["riparian boundary", "river", "creek", "survey", "natural boundary"],
        conclusion_template="Riparian boundaries are determined by the thread of the stream, subject to accretion and avulsion rules.",
        reasoning_framework=(
            "Riparian boundary determination requires analysis of field notes, historical maps, and physical evidence. "
            "The doctrine recognizes the thread of the stream as the boundary, subject to accretion and avulsion rules. "
            "Courts rely on expert testimony, geospatial analysis, and historical records. The burden is on the party "
            "contesting the boundary to prove error or fraud. Resolution may involve re-surveying, judicial determination, "
            "or negotiation."
        ),
        key_factors=[
            "Thread of the stream",
            "Accretion and avulsion",
            "Field notes",
            "Historical maps"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party contesting boundary",
        adversary_position="Thread of the stream controls unless error is proven.",
        counter_arguments=[
            "Natural boundary has changed.",
            "Thread of stream is ambiguous.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to thread of stream and physical evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Boundary Conflicts",
        keywords=["subdivision", "plat", "boundary", "conflict", "survey"],
        conclusion_template="Subdivision plat boundaries control over individual lot surveys unless plat is ambiguous or defective.",
        reasoning_framework=(
            "Conflicts between subdivision plat boundaries and individual lot surveys are resolved by prioritizing the "
            "boundaries described in the recorded plat. The doctrine recognizes the importance of public notice and title "
            "stability. Courts rely on plat maps, deed records, and physical evidence. The burden is on the party seeking "
            "to alter plat boundaries to prove ambiguity or defect. Resolution may involve judicial determination, "
            "negotiation, or administrative correction."
        ),
        key_factors=[
            "Recorded plat boundaries",
            "Deed records",
            "Physical evidence",
            "Public notice"
        ],
        primary_authority=[
            "Texas Property Code § 12.002",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party seeking to alter plat boundaries",
        adversary_position="Plat boundaries control unless ambiguity or defect is proven.",
        counter_arguments=[
            "Plat is ambiguous or defective.",
            "Deed clarifies boundary.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to recorded plat boundaries and physical evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Fence Line as Boundary Evidence",
        keywords=["fence line", "boundary", "evidence", "survey", "occupation"],
        conclusion_template="Fence lines may be considered boundary evidence where physical occupation and acquiescence are proven.",
        reasoning_framework=(
            "Fence lines may be considered evidence of boundary where physical occupation and acquiescence are proven. "
            "The doctrine requires evidence of mutual acceptance, physical occupation, and absence of dispute. Courts "
            "rely on witness testimony, historical records, and physical evidence. The burden is on the party asserting "
            "the fence line as boundary to prove mutual acceptance and occupation. Resolution may involve judicial "
            "determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Mutual acceptance",
            "Physical occupation",
            "Absence of dispute",
            "Historical records"
        ],
        primary_authority=[
            "Texas Supreme Court decisions",
            "Texas Property Code"
        ],
        burden_holder="Party asserting fence line as boundary",
        adversary_position="Survey boundaries control unless fence line is proven as boundary.",
        counter_arguments=[
            "No mutual acceptance.",
            "Physical occupation is ambiguous.",
            "Dispute existed during occupation."
        ],
        resolution_strategy="Judicial determination based on evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Monument Relocation and Replacement",
        keywords=["monument", "relocation", "replacement", "survey", "boundary"],
        conclusion_template="Relocated or replaced monuments must be documented and adhere to original intent and field notes.",
        reasoning_framework=(
            "Relocation or replacement of monuments must be documented and adhere to original intent and field notes. "
            "The doctrine recognizes the importance of physical evidence and stability in boundary determination. Courts "
            "rely on survey records, field notes, and expert testimony. The burden is on the party relocating or replacing "
            "the monument to prove original intent and accuracy. Resolution may involve judicial determination, negotiation, "
            "or administrative correction."
        ),
        key_factors=[
            "Documentation of relocation",
            "Original intent",
            "Field notes",
            "Survey records"
        ],
        primary_authority=[
            "Texas General Land Office rules",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party relocating or replacing monument",
        adversary_position="Original monuments control unless relocation is documented.",
        counter_arguments=[
            "Relocation is undocumented.",
            "Original intent is ambiguous.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Documentation and adherence to original intent.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Ambiguous Survey Call Resolution",
        keywords=["ambiguous survey call", "resolution", "boundary", "survey", "field notes"],
        conclusion_template="Ambiguous survey calls are resolved by prioritizing physical evidence, monuments, and intent.",
        reasoning_framework=(
            "Resolution of ambiguous survey calls requires prioritizing physical evidence, monuments, and intent of the "
            "original surveyor. The doctrine recognizes the importance of certainty and stability in boundary determination. "
            "Courts rely on field notes, historical maps, and expert testimony. The burden is on the party contesting the "
            "boundary to prove ambiguity and error. Resolution may involve judicial determination, negotiation, or "
            "administrative correction."
        ),
        key_factors=[
            "Physical evidence",
            "Monuments",
            "Intent of surveyor",
            "Field notes"
        ],
        primary_authority=[
            "Texas Natural Resources Code § 21.011",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party contesting boundary",
        adversary_position="Physical evidence and monuments control.",
        counter_arguments=[
            "Monuments are missing or ambiguous.",
            "Intent is unclear.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Adherence to physical evidence and intent.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Mediation Procedures",
        keywords=["boundary conflict", "mediation", "procedures", "survey", "dispute"],
        conclusion_template="Boundary conflicts may be resolved through mediation, with agreements documented and recorded.",
        reasoning_framework=(
            "Boundary conflict mediation procedures provide an alternative to judicial determination. Mediation involves "
            "negotiation between parties, facilitated by a neutral mediator. Agreements must be documented and recorded "
            "to be binding. The doctrine recognizes the importance of public notice and title stability. Courts may enforce "
            "mediated agreements if statutory requirements are met. The burden is on the party asserting the agreement to "
            "prove documentation and recording. Resolution may involve judicial determination, negotiation, or "
            "administrative correction."
        ),
        key_factors=[
            "Mediation procedures",
            "Documentation of agreement",
            "Recording",
            "Public notice"
        ],
        primary_authority=[
            "Texas Property Code § 12.001",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting mediated agreement",
        adversary_position="Agreement is not binding unless documented and recorded.",
        counter_arguments=[
            "Agreement was not documented.",
            "No public notice.",
            "Dispute existed during mediation."
        ],
        resolution_strategy="Mediation, documentation, and recording.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Arbitration Procedures",
        keywords=["boundary conflict", "arbitration", "procedures", "survey", "dispute"],
        conclusion_template="Boundary conflicts may be resolved through arbitration, with awards enforceable by courts.",
        reasoning_framework=(
            "Boundary conflict arbitration procedures provide an alternative to judicial determination. Arbitration involves "
            "submission of the dispute to a neutral arbitrator, whose award is enforceable by courts. The doctrine recognizes "
            "the importance of public notice and title stability. Courts may enforce arbitration awards if statutory requirements "
            "are met. The burden is on the party asserting the award to prove arbitration and enforceability. Resolution may "
            "involve judicial determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Arbitration procedures",
            "Enforceability of award",
            "Public notice",
            "Documentation"
        ],
        primary_authority=[
            "Texas Civil Practice and Remedies Code § 171.001",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting arbitration award",
        adversary_position="Award is not enforceable unless statutory requirements are met.",
        counter_arguments=[
            "Arbitration was not conducted properly.",
            "Award is ambiguous.",
            "Dispute existed during arbitration."
        ],
        resolution_strategy="Arbitration and judicial enforcement.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Litigation Procedures",
        keywords=["boundary conflict", "litigation", "procedures", "survey", "dispute"],
        conclusion_template="Boundary conflicts may be resolved through litigation, with courts determining boundaries based on evidence and precedent.",
        reasoning_framework=(
            "Boundary conflict litigation procedures involve submission of the dispute to a court, which determines boundaries "
            "based on evidence and controlling precedent. The doctrine recognizes the importance of certainty and stability in "
            "title. Courts rely on field notes, historical maps, expert testimony, and chain of title documents. The burden is "
            "on the party asserting the boundary to prove evidence and legal authority. Resolution may involve judicial "
            "determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Litigation procedures",
            "Evidence",
            "Controlling precedent",
            "Chain of title"
        ],
        primary_authority=[
            "Texas Civil Practice and Remedies Code",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting boundary",
        adversary_position="Boundary is determined by court based on evidence.",
        counter_arguments=[
            "Evidence is ambiguous.",
            "Controlling precedent is unclear.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Litigation and judicial determination.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Administrative Procedures",
        keywords=["boundary conflict", "administrative", "procedures", "survey", "dispute"],
        conclusion_template="Boundary conflicts may be resolved through administrative procedures, with corrections made by relevant agencies.",
        reasoning_framework=(
            "Boundary conflict administrative procedures involve submission of the dispute to relevant agencies, such as the Texas "
            "General Land Office. Corrections may be made administratively based on evidence and statutory authority. The doctrine "
            "recognizes the importance of certainty and stability in title. Agencies rely on field notes, historical maps, expert "
            "testimony, and chain of title documents. The burden is on the party asserting the boundary to prove evidence and legal "
            "authority. Resolution may involve administrative correction, negotiation, or judicial determination."
        ),
        key_factors=[
            "Administrative procedures",
            "Evidence",
            "Statutory authority",
            "Chain of title"
        ],
        primary_authority=[
            "Texas General Land Office rules",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting boundary",
        adversary_position="Boundary is determined by agency based on evidence.",
        counter_arguments=[
            "Evidence is ambiguous.",
            "Statutory authority is unclear.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Administrative correction and agency determination.",
        entity_scope="Texas landowners, surveyors, GLO",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas General Land Office rules"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Title Insurance Procedures",
        keywords=["boundary conflict", "title insurance", "procedures", "survey", "dispute"],
        conclusion_template="Boundary conflicts may be addressed by title insurance claims, with insurers relying on survey and title evidence.",
        reasoning_framework=(
            "Boundary conflict title insurance procedures involve submission of claims to title insurers, who rely on survey and "
            "title evidence to determine coverage and liability. The doctrine recognizes the importance of certainty and stability "
            "in title. Insurers rely on field notes, deed records, expert testimony, and chain of title documents. The burden is on "
            "the insured to prove coverage and boundary conflict. Resolution may involve negotiation, litigation, or administrative "
            "correction."
        ),
        key_factors=[
            "Title insurance procedures",
            "Survey evidence",
            "Deed records",
            "Chain of title"
        ],
        primary_authority=[
            "Texas Insurance Code",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Insured party",
        adversary_position="Coverage is denied unless boundary conflict is proven.",
        counter_arguments=[
            "Survey evidence is ambiguous.",
            "Deed records are unclear.",
            "Chain of title is defective."
        ],
        resolution_strategy="Title insurance claim and negotiation.",
        entity_scope="Texas landowners, surveyors, insurers",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Insurance Code"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Surveyor Ethics",
        keywords=["boundary conflict", "surveyor ethics", "professional conduct", "survey", "dispute"],
        conclusion_template="Surveyors must adhere to ethical standards, prioritizing accuracy, impartiality, and public interest in boundary determination.",
        reasoning_framework=(
            "Surveyor ethics in boundary conflict resolution require adherence to professional standards, prioritizing accuracy, "
            "impartiality, and public interest. The doctrine recognizes the importance of certainty and stability in title. Surveyors "
            "must document evidence, disclose conflicts, and avoid bias. Courts and agencies rely on surveyor testimony, records, and "
            "professional conduct. The burden is on the surveyor to demonstrate ethical compliance. Resolution may involve disciplinary "
            "action, judicial determination, or administrative correction."
        ),
        key_factors=[
            "Professional standards",
            "Accuracy",
            "Impartiality",
            "Public interest"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying rules",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Surveyor",
        adversary_position="Surveyor failed to adhere to ethical standards.",
        counter_arguments=[
            "Surveyor was biased.",
            "Evidence was not documented.",
            "Public interest was not prioritized."
        ],
        resolution_strategy="Ethical compliance and disciplinary action.",
        entity_scope="Texas surveyors, landowners, courts",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Board of Professional Land Surveying rules"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Expert Testimony",
        keywords=["boundary conflict", "expert testimony", "survey", "dispute", "evidence"],
        conclusion_template="Expert testimony may be admitted to clarify boundary conflicts, subject to relevance and reliability standards.",
        reasoning_framework=(
            "Expert testimony in boundary conflict resolution may be admitted to clarify evidence, subject to relevance and reliability "
            "standards. The doctrine recognizes the importance of certainty and stability in title. Courts rely on expert testimony, "
            "field notes, historical maps, and chain of title documents. The burden is on the party offering expert testimony to prove "
            "relevance and reliability. Resolution may involve judicial determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Expert testimony",
            "Relevance",
            "Reliability",
            "Evidence"
        ],
        primary_authority=[
            "Texas Rules of Evidence",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party offering expert testimony",
        adversary_position="Testimony is inadmissible unless relevant and reliable.",
        counter_arguments=[
            "Testimony is irrelevant.",
            "Testimony is unreliable.",
            "Evidence is ambiguous."
        ],
        resolution_strategy="Judicial determination based on evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Rules of Evidence"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Chain of Title Analysis",
        keywords=["boundary conflict", "chain of title", "analysis", "survey", "dispute"],
        conclusion_template="Chain of title analysis clarifies boundary conflicts by tracing ownership and boundary descriptions.",
        reasoning_framework=(
            "Chain of title analysis clarifies boundary conflicts by tracing ownership and boundary descriptions through deed records, "
            "patent documents, and historical maps. The doctrine recognizes the importance of certainty and stability in title. Courts "
            "rely on chain of title documents, field notes, and expert testimony. The burden is on the party asserting chain of title "
            "to prove ownership and boundary description. Resolution may involve judicial determination, negotiation, or administrative "
            "correction."
        ),
        key_factors=[
            "Chain of title documents",
            "Ownership",
            "Boundary description",
            "Historical maps"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting chain of title",
        adversary_position="Chain of title is ambiguous or defective.",
        counter_arguments=[
            "Ownership is unclear.",
            "Boundary description is ambiguous.",
            "Historical maps are unreliable."
        ],
        resolution_strategy="Chain of title analysis and judicial determination.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Property Code"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Historical Map Analysis",
        keywords=["boundary conflict", "historical map", "analysis", "survey", "dispute"],
        conclusion_template="Historical map analysis clarifies boundary conflicts by providing evidence of original boundaries and occupation.",
        reasoning_framework=(
            "Historical map analysis clarifies boundary conflicts by providing evidence of original boundaries and occupation. The doctrine "
            "recognizes the importance of certainty and stability in title. Courts rely on historical maps, field notes, and expert testimony. "
            "The burden is on the party asserting historical map evidence to prove relevance and accuracy. Resolution may involve judicial "
            "determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Historical maps",
            "Original boundaries",
            "Occupation",
            "Field notes"
        ],
        primary_authority=[
            "Texas General Land Office map records",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting historical map evidence",
        adversary_position="Historical maps are ambiguous or inaccurate.",
        counter_arguments=[
            "Maps are ambiguous.",
            "Original boundaries are unclear.",
            "Occupation is not proven."
        ],
        resolution_strategy="Historical map analysis and judicial determination.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas General Land Office map records"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Surveyor Testimony",
        keywords=["boundary conflict", "surveyor testimony", "survey", "dispute", "evidence"],
        conclusion_template="Surveyor testimony may be admitted to clarify boundary conflicts, subject to relevance and reliability standards.",
        reasoning_framework=(
            "Surveyor testimony in boundary conflict resolution may be admitted to clarify evidence, subject to relevance and reliability "
            "standards. The doctrine recognizes the importance of certainty and stability in title. Courts rely on surveyor testimony, field "
            "notes, historical maps, and chain of title documents. The burden is on the party offering surveyor testimony to prove relevance "
            "and reliability. Resolution may involve judicial determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Surveyor testimony",
            "Relevance",
            "Reliability",
            "Evidence"
        ],
        primary_authority=[
            "Texas Rules of Evidence",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party offering surveyor testimony",
        adversary_position="Testimony is inadmissible unless relevant and reliable.",
        counter_arguments=[
            "Testimony is irrelevant.",
            "Testimony is unreliable.",
            "Evidence is ambiguous."
        ],
        resolution_strategy="Judicial determination based on evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Rules of Evidence"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Witness Testimony",
        keywords=["boundary conflict", "witness testimony", "survey", "dispute", "evidence"],
        conclusion_template="Witness testimony may be admitted to clarify boundary conflicts, subject to relevance and reliability standards.",
        reasoning_framework=(
            "Witness testimony in boundary conflict resolution may be admitted to clarify evidence, subject to relevance and reliability "
            "standards. The doctrine recognizes the importance of certainty and stability in title. Courts rely on witness testimony, field "
            "notes, historical maps, and chain of title documents. The burden is on the party offering witness testimony to prove relevance "
            "and reliability. Resolution may involve judicial determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Witness testimony",
            "Relevance",
            "Reliability",
            "Evidence"
        ],
        primary_authority=[
            "Texas Rules of Evidence",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party offering witness testimony",
        adversary_position="Testimony is inadmissible unless relevant and reliable.",
        counter_arguments=[
            "Testimony is irrelevant.",
            "Testimony is unreliable.",
            "Evidence is ambiguous."
        ],
        resolution_strategy="Judicial determination based on evidence.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Rules of Evidence"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Public Policy Considerations",
        keywords=["boundary conflict", "public policy", "considerations", "survey", "dispute"],
        conclusion_template="Public policy favors certainty, stability, and fairness in boundary conflict resolution.",
        reasoning_framework=(
            "Public policy considerations in boundary conflict resolution favor certainty, stability, and fairness in title. The doctrine "
            "recognizes the importance of public notice, reliance, and equitable principles. Courts and agencies rely on public policy to "
            "guide resolution of disputes. The burden is on the party asserting public policy to prove relevance and impact. Resolution may "
            "involve judicial determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Certainty",
            "Stability",
            "Fairness",
            "Public notice"
        ],
        primary_authority=[
            "Texas Supreme Court decisions",
            "Texas Property Code"
        ],
        burden_holder="Party asserting public policy",
        adversary_position="Public policy does not override controlling precedent.",
        counter_arguments=[
            "Certainty and stability are not served.",
            "Fairness is not achieved.",
            "Public notice is lacking."
        ],
        resolution_strategy="Judicial determination guided by public policy.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Equitable Principles",
        keywords=["boundary conflict", "equitable principles", "survey", "dispute", "fairness"],
        conclusion_template="Equitable principles may guide boundary conflict resolution where legal authority is ambiguous.",
        reasoning_framework=(
            "Equitable principles may guide boundary conflict resolution where legal authority is ambiguous. The doctrine recognizes the "
            "importance of fairness, reliance, and stability in title. Courts rely on equitable principles, field notes, historical maps, and "
            "chain of title documents. The burden is on the party asserting equitable principles to prove relevance and impact. Resolution may "
            "involve judicial determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Fairness",
            "Reliance",
            "Stability",
            "Legal authority"
        ],
        primary_authority=[
            "Texas Supreme Court decisions",
            "Texas Property Code"
        ],
        burden_holder="Party asserting equitable principles",
        adversary_position="Equitable principles do not override controlling precedent.",
        counter_arguments=[
            "Fairness is not achieved.",
            "Reliance is not proven.",
            "Legal authority is clear."
        ],
        resolution_strategy="Judicial determination guided by equitable principles.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court decisions"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Statutory Interpretation",
        keywords=["boundary conflict", "statutory interpretation", "survey", "dispute", "law"],
        conclusion_template="Statutory interpretation guides boundary conflict resolution where statutes govern boundaries.",
        reasoning_framework=(
            "Statutory interpretation guides boundary conflict resolution where statutes govern boundaries. The doctrine recognizes the "
            "importance of certainty, stability, and compliance with statutory authority. Courts and agencies rely on statutory interpretation, "
            "field notes, historical maps, and chain of title documents. The burden is on the party asserting statutory authority to prove "
            "relevance and impact. Resolution may involve judicial determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Statutory authority",
            "Certainty",
            "Stability",
            "Compliance"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting statutory authority",
        adversary_position="Statutory authority does not override controlling precedent.",
        counter_arguments=[
            "Statutory authority is ambiguous.",
            "Certainty and stability are not served.",
            "Compliance is lacking."
        ],
        resolution_strategy="Judicial determination guided by statutory interpretation.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Natural Resources Code"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Survey Correction Procedures",
        keywords=["boundary conflict", "survey correction", "procedures", "survey", "dispute"],
        conclusion_template="Survey corrections must be documented and adhere to original intent and field notes.",
        reasoning_framework=(
            "Survey correction procedures require documentation and adherence to original intent and field notes. The doctrine recognizes the "
            "importance of certainty and stability in boundary determination. Courts and agencies rely on survey records, field notes, and expert "
            "testimony. The burden is on the party seeking correction to prove error and original intent. Resolution may involve judicial "
            "determination, negotiation, or administrative correction."
        ),
        key_factors=[
            "Documentation of correction",
            "Original intent",
            "Field notes",
            "Survey records"
        ],
        primary_authority=[
            "Texas General Land Office rules",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party seeking correction",
        adversary_position="Original survey controls unless correction is documented.",
        counter_arguments=[
            "Correction is undocumented.",
            "Original intent is ambiguous.",
            "Surveyor error justifies adjustment."
        ],
        resolution_strategy="Documentation and adherence to original intent.",
        entity_scope="Texas landowners, surveyors, courts",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas General Land Office rules"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Surveyor Licensing Requirements",
        keywords=["boundary conflict", "surveyor licensing", "requirements", "survey", "dispute"],
        conclusion_template="Surveyors must be licensed and comply with statutory requirements to conduct boundary surveys.",
        reasoning_framework=(
            "Surveyor licensing requirements mandate that surveyors be licensed and comply with statutory requirements to conduct boundary "
            "surveys. The doctrine recognizes the importance of professional standards, accuracy, and public interest. Courts and agencies rely "
            "on surveyor licensing records, field notes, and expert testimony. The burden is on the surveyor to demonstrate compliance. "
            "Resolution may involve disciplinary action, judicial determination, or administrative correction."
        ),
        key_factors=[
            "Licensing records",
            "Professional standards",
            "Accuracy",
            "Public interest"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying rules",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Surveyor",
        adversary_position="Surveyor failed to comply with licensing requirements.",
        counter_arguments=[
            "Surveyor was unlicensed.",
            "Professional standards were not met.",
            "Public interest was not prioritized."
        ],
        resolution_strategy="Licensing compliance and disciplinary action.",
        entity_scope="Texas surveyors, landowners, courts",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Board of Professional Land Surveying rules"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Surveyor Recordkeeping Requirements",
        keywords=["boundary conflict", "surveyor recordkeeping", "requirements", "survey", "dispute"],
        conclusion_template="Surveyors must maintain accurate records of surveys, corrections, and boundary determinations.",
        reasoning_framework=(
            "Surveyor recordkeeping requirements mandate that surveyors maintain accurate records of surveys, corrections, and boundary "
            "determinations. The doctrine recognizes the importance of certainty, stability, and public interest. Courts and agencies rely on "
            "survey records, field notes, and expert testimony. The burden is on the surveyor to demonstrate compliance. Resolution may involve "
            "disciplinary action, judicial determination, or administrative correction."
        ),
        key_factors=[
            "Survey records",
            "Field notes",
            "Corrections",
            "Boundary determinations"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying rules",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Surveyor",
        adversary_position="Surveyor failed to maintain accurate records.",
        counter_arguments=[
            "Records are missing.",
            "Records are inaccurate.",
            "Corrections are undocumented."
        ],
        resolution_strategy="Recordkeeping compliance and disciplinary action.",
        entity_scope="Texas surveyors, landowners, courts",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Board of Professional Land Surveying rules"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Surveyor Disclosure Requirements",
        keywords=["boundary conflict", "surveyor disclosure", "requirements", "survey", "dispute"],
        conclusion_template="Surveyors must disclose conflicts, corrections, and boundary determinations to relevant parties.",
        reasoning_framework=(
            "Surveyor disclosure requirements mandate that surveyors disclose conflicts, corrections, and boundary determinations to relevant "
            "parties. The doctrine recognizes the importance of certainty, stability, and public interest. Courts and agencies rely on surveyor "
            "disclosure records, field notes, and expert testimony. The burden is on the surveyor to demonstrate compliance. Resolution may "
            "involve disciplinary action, judicial determination, or administrative correction."
        ),
        key_factors=[
            "Disclosure records",
            "Conflicts",
            "Corrections",
            "Boundary determinations"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying rules",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Surveyor",
        adversary_position="Surveyor failed to disclose conflicts.",
        counter_arguments=[
            "Conflicts were not disclosed.",
            "Corrections were not disclosed.",
            "Boundary determinations were not disclosed."
        ],
        resolution_strategy="Disclosure compliance and disciplinary action.",
        entity_scope="Texas surveyors, landowners, courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Board of Professional Land Surveying rules"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Surveyor Professional Liability",
        keywords=["boundary conflict", "surveyor professional liability", "survey", "dispute", "error"],
        conclusion_template="Surveyors may be liable for professional errors in boundary determination, subject to statutory and common law standards.",
        reasoning_framework=(
            "Surveyor professional liability arises from errors in boundary determination, subject to statutory and common law standards. The doctrine "
            "recognizes the importance of accuracy, impartiality, and public interest. Courts and agencies rely on survey records, field notes, and expert "
            "testimony. The burden is on the party asserting liability to prove error and impact. Resolution may involve disciplinary action, judicial "
            "determination, or administrative correction."
        ),
        key_factors=[
            "Professional standards",
            "Error",
            "Impact",
            "Statutory authority"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying rules",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting liability",
        adversary_position="Surveyor is not liable unless error is proven.",
        counter_arguments=[
            "Error is not proven.",
            "Impact is not proven.",
            "Statutory authority is lacking."
        ],
        resolution_strategy="Liability determination and disciplinary action.",
        entity_scope="Texas surveyors, landowners, courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Board of Professional Land Surveying rules"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Surveyor Standard of Care",
        keywords=["boundary conflict", "surveyor standard of care", "survey", "dispute", "professional standards"],
        conclusion_template="Surveyors must adhere to the standard of care established by professional standards and statutory authority.",
        reasoning_framework=(
            "Surveyor standard of care requires adherence to professional standards and statutory authority in boundary determination. The doctrine "
            "recognizes the importance of accuracy, impartiality, and public interest. Courts and agencies rely on survey records, field notes, and expert "
            "testimony. The burden is on the party asserting breach of standard of care to prove error and impact. Resolution may involve disciplinary action, "
            "judicial determination, or administrative correction."
        ),
        key_factors=[
            "Professional standards",
            "Statutory authority",
            "Error",
            "Impact"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying rules",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Party asserting breach of standard of care",
        adversary_position="Surveyor adhered to standard of care.",
        counter_arguments=[
            "Error is not proven.",
            "Impact is not proven.",
            "Statutory authority is lacking."
        ],
        resolution_strategy="Standard of care determination and disciplinary action.",
        entity_scope="Texas surveyors, landowners, courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Board of Professional Land Surveying rules"
    ),
    DoctrineBlock(
        topic="Boundary Conflict Surveyor Continuing Education Requirements",
        keywords=["boundary conflict", "surveyor continuing education", "requirements", "survey", "dispute"],
        conclusion_template="Surveyors must comply with continuing education requirements to maintain licensure and professional standards.",
        reasoning_framework=(
            "Surveyor continuing education requirements mandate compliance to maintain licensure and professional standards in boundary determination. The doctrine "
            "recognizes the importance of accuracy, impartiality, and public interest. Courts and agencies rely on continuing education records, survey records, and expert "
            "testimony. The burden is on the surveyor to demonstrate compliance. Resolution may involve disciplinary action, judicial determination, or administrative correction."
        ),
        key_factors=[
            "Continuing education records",
            "Licensure",
            "Professional standards",
            "Public interest"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying rules",
            "Texas Supreme Court decisions"
        ],
        burden_holder="Surveyor",
        adversary_position="Surveyor failed to comply with continuing education requirements.",
        counter_arguments=[
            "Continuing education was not completed.",
            "Licensure was not maintained.",
            "Professional standards were not met."
        ],
        resolution_strategy="Education compliance and disciplinary action.",
        entity_scope="Texas surveyors, landowners, courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Board of Professional Land Surveying rules"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(query: str) -> List[DoctrineBlock]:
    results = []
    query_lower = query.lower()
    for doctrine in DOCTRINE_CACHE:
        if query_lower in doctrine.topic.lower() or any(query_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]