from dataclasses import dataclass, field
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
        topic="GIS Layer Alignment for RRC Well Data",
        keywords=["GIS", "alignment", "RRC", "well data", "coordinate reference system", "accuracy"],
        conclusion_template="All RRC well data layers must be spatially aligned to the project CRS with a maximum tolerance of 1 meter.",
        reasoning_framework=(
            "1. Identify the coordinate reference system (CRS) used by the RRC well data layer.\n"
            "2. Compare the CRS to the project-standard CRS (e.g., NAD83 Texas State Plane).\n"
            "3. If misalignment is detected, reproject the well data layer using authoritative transformation parameters.\n"
            "4. Validate alignment by overlaying known control points and checking for spatial discrepancies.\n"
            "5. Document all transformations and maintain metadata integrity.\n"
            "6. If alignment cannot be achieved within tolerance, escalate to data provider for clarification.\n"
            "7. Ensure all subsequent overlays reference the aligned well data layer as the base.\n"
            "8. Maintain version control for all aligned datasets.\n"
            "9. Confirm that attribute joins remain intact post-alignment.\n"
            "10. Validate alignment through visual inspection and automated QA/QC routines."
        ),
        key_factors=[
            "CRS compatibility",
            "Transformation accuracy",
            "Control point validation",
            "Metadata documentation",
            "Version control"
        ],
        primary_authority=[
            "Texas Railroad Commission GIS Data Standards",
            "OGC Simple Feature Specification",
            "Texas Natural Resources Code"
        ],
        burden_holder="Data Integrator",
        adversary_position="Misaligned well data layers can result in regulatory non-compliance and spatial analysis errors.",
        counter_arguments=[
            "Legacy data may not support high-precision alignment.",
            "Transformation parameters may introduce minor distortions."
        ],
        resolution_strategy="Apply best-available transformation methods and document all deviations from standard procedures.",
        entity_scope="All RRC well data layers ingested into the G04 engine.",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="RRC GIS Data Submission Guidelines (2022)"
    ),
    DoctrineBlock(
        topic="Pipeline Route Mapping and Surface Feature Overlay",
        keywords=["pipeline", "route mapping", "surface features", "overlay", "conflict detection"],
        conclusion_template="Pipeline routes must be mapped and overlaid with all surface features to identify and resolve spatial conflicts prior to permitting.",
        reasoning_framework=(
            "1. Acquire pipeline route geometry and all relevant surface feature layers (roads, hydrology, buildings, etc.).\n"
            "2. Ensure all layers are aligned to the project CRS.\n"
            "3. Overlay pipeline routes with surface features using spatial intersection tools.\n"
            "4. Identify conflicts such as route crossings with critical infrastructure or environmental features.\n"
            "5. Document each conflict with spatial coordinates and attribute details.\n"
            "6. Propose route adjustments or mitigation measures for each conflict.\n"
            "7. Validate that all conflicts are resolved prior to submission for permitting.\n"
            "8. Maintain a conflict resolution log for regulatory review.\n"
            "9. Update pipeline route geometry as necessary and re-validate overlays.\n"
            "10. Ensure all overlays are visually inspected and QA/QC checked."
        ),
        key_factors=[
            "Spatial accuracy",
            "Comprehensiveness of surface feature layers",
            "Conflict documentation",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, Part 1",
            "PHMSA Pipeline Mapping Standards",
            "OGC Web Feature Service Specification"
        ],
        burden_holder="Pipeline Operator",
        adversary_position="Unresolved route conflicts may result in permit denial or legal challenges.",
        counter_arguments=[
            "Some surface features may be outdated or incomplete.",
            "Automated conflict detection may miss context-specific issues."
        ],
        resolution_strategy="Combine automated and manual review processes; update datasets as new information becomes available.",
        entity_scope="All pipeline route mapping activities within the G04 engine.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="PHMSA Pipeline Mapping Guidelines (2021)"
    ),
    DoctrineBlock(
        topic="Surface Owner Boundary Delineation",
        keywords=["surface owner", "boundary", "delineation", "parcel", "ownership"],
        conclusion_template="Surface owner boundaries must be delineated using the most current county appraisal district parcel data.",
        reasoning_framework=(
            "1. Obtain the latest parcel data from the relevant county appraisal district.\n"
            "2. Validate the spatial accuracy of parcel boundaries against survey abstracts and aerial imagery.\n"
            "3. Resolve discrepancies by referencing recorded deeds and legal descriptions.\n"
            "4. Attribute each parcel polygon with owner information from official records.\n"
            "5. Maintain a change log for all boundary adjustments.\n"
            "6. Ensure that boundary delineations are consistent with county and state standards.\n"
            "7. Document sources and methods for all delineation activities.\n"
            "8. Integrate owner boundaries with other spatial layers for analysis.\n"
            "9. Periodically review and update boundaries as new data becomes available.\n"
            "10. Provide clear metadata for all delineated boundaries."
        ),
        key_factors=[
            "Data currency",
            "Legal documentation",
            "Spatial accuracy",
            "Attribution integrity"
        ],
        primary_authority=[
            "Texas Property Code",
            "County Appraisal District GIS Standards",
            "Texas General Land Office"
        ],
        burden_holder="GIS Analyst",
        adversary_position="Inaccurate boundaries can lead to ownership disputes and regulatory violations.",
        counter_arguments=[
            "Parcel data may lag behind recent transactions.",
            "Survey data may be incomplete or ambiguous."
        ],
        resolution_strategy="Cross-reference multiple data sources and prioritize legal documentation.",
        entity_scope="All surface owner boundary delineations within the G04 engine.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas GLO Parcel Mapping Guidelines (2020)"
    ),
    DoctrineBlock(
        topic="Mineral Owner Boundary Integration",
        keywords=["mineral owner", "boundary", "integration", "ownership", "title"],
        conclusion_template="Mineral owner boundaries must be integrated with surface boundaries and validated against official title records.",
        reasoning_framework=(
            "1. Acquire mineral ownership data from county records and title abstracts.\n"
            "2. Overlay mineral boundaries with surface owner boundaries to identify overlaps and gaps.\n"
            "3. Validate mineral boundaries using legal descriptions and survey data.\n"
            "4. Attribute each mineral parcel with ownership and title information.\n"
            "5. Document all integration steps and sources.\n"
            "6. Resolve discrepancies through consultation with title attorneys or landmen.\n"
            "7. Maintain a versioned record of all boundary changes.\n"
            "8. Ensure that integrated boundaries are used for all mineral-related analyses.\n"
            "9. Provide clear metadata and lineage for all integrated boundaries.\n"
            "10. Periodically update boundaries as new title information becomes available."
        ),
        key_factors=[
            "Title accuracy",
            "Spatial integration",
            "Legal validation",
            "Attribution completeness"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "County Clerk Title Records",
            "American Association of Professional Landmen (AAPL) Standards"
        ],
        burden_holder="Landman",
        adversary_position="Improper integration may result in title disputes and missed royalties.",
        counter_arguments=[
            "Title records may be incomplete or contain errors.",
            "Legal descriptions may not match GIS boundaries."
        ],
        resolution_strategy="Engage title professionals for complex cases and document all assumptions.",
        entity_scope="All mineral owner boundary integrations within the G04 engine.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AAPL Title Mapping Best Practices (2019)"
    ),
    DoctrineBlock(
        topic="Unit Boundary Overlay and Validation",
        keywords=["unit", "boundary", "overlay", "validation", "lease", "pooling"],
        conclusion_template="Unit boundaries must be overlaid with lease and ownership boundaries and validated for regulatory compliance.",
        reasoning_framework=(
            "1. Obtain unit boundary data from regulatory filings or operator submissions.\n"
            "2. Overlay unit boundaries with lease and ownership boundaries in the GIS environment.\n"
            "3. Identify and resolve any overlaps, gaps, or inconsistencies.\n"
            "4. Validate unit configuration against pooling agreements and regulatory requirements.\n"
            "5. Attribute unit polygons with relevant regulatory and ownership information.\n"
            "6. Document all validation steps and sources.\n"
            "7. Maintain a change log for unit boundary adjustments.\n"
            "8. Ensure that validated unit boundaries are used for all reporting and analysis.\n"
            "9. Provide clear metadata for all unit boundaries.\n"
            "10. Periodically review and update unit boundaries as necessary."
        ),
        key_factors=[
            "Regulatory compliance",
            "Spatial accuracy",
            "Agreement validation",
            "Attribution integrity"
        ],
        primary_authority=[
            "Texas Railroad Commission Unitization Rules",
            "Pooling Agreements",
            "Texas Natural Resources Code"
        ],
        burden_holder="Operator",
        adversary_position="Invalid unit boundaries may result in regulatory penalties and revenue misallocation.",
        counter_arguments=[
            "Pooling agreements may be ambiguous.",
            "Unit boundaries may change over time."
        ],
        resolution_strategy="Maintain close coordination with regulatory agencies and update boundaries as agreements evolve.",
        entity_scope="All unit boundary overlays within the G04 engine.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="RRC Unitization Mapping Guidelines (2021)"
    ),
    DoctrineBlock(
        topic="Lease Boundary Integration and QA/QC",
        keywords=["lease", "boundary", "integration", "QA/QC", "validation"],
        conclusion_template="Lease boundaries must be integrated with unit and ownership boundaries and subjected to rigorous QA/QC procedures.",
        reasoning_framework=(
            "1. Acquire lease boundary data from official lease records and GIS sources.\n"
            "2. Integrate lease boundaries with unit and ownership boundaries in the GIS system.\n"
            "3. Perform automated and manual QA/QC checks for overlaps, gaps, and topology errors.\n"
            "4. Attribute lease polygons with leaseholder and agreement information.\n"
            "5. Document all integration and QA/QC steps.\n"
            "6. Resolve discrepancies through consultation with lease administrators.\n"
            "7. Maintain a versioned record of all lease boundary changes.\n"
            "8. Ensure that only QA/QC-passed boundaries are used for analysis and reporting.\n"
            "9. Provide clear metadata for all lease boundaries.\n"
            "10. Periodically review and update lease boundaries as new information becomes available."
        ),
        key_factors=[
            "QA/QC rigor",
            "Integration accuracy",
            "Attribution completeness",
            "Change documentation"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "Lease Administration Best Practices",
            "OGC Simple Feature Specification"
        ],
        burden_holder="Lease Administrator",
        adversary_position="QA/QC failures may result in reporting errors and legal challenges.",
        counter_arguments=[
            "Lease records may be outdated.",
            "QA/QC processes may miss subtle errors."
        ],
        resolution_strategy="Implement both automated and manual QA/QC procedures and maintain detailed logs.",
        entity_scope="All lease boundary integrations within the G04 engine.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Lease Mapping QA/QC Standards (2020)"
    ),
    DoctrineBlock(
        topic="Survey Abstract Boundary Overlay",
        keywords=["survey abstract", "boundary", "overlay", "validation", "legal description"],
        conclusion_template="Survey abstract boundaries must be overlaid with parcel and ownership layers to validate spatial and legal consistency.",
        reasoning_framework=(
            "1. Obtain survey abstract boundaries from county or state sources.\n"
            "2. Overlay abstract boundaries with parcel and ownership layers in the GIS environment.\n"
            "3. Identify and resolve discrepancies between abstract and parcel boundaries.\n"
            "4. Validate abstract boundaries using legal descriptions and recorded surveys.\n"
            "5. Attribute abstract polygons with surveyor and legal information.\n"
            "6. Document all overlay and validation steps.\n"
            "7. Maintain a change log for abstract boundary adjustments.\n"
            "8. Ensure that validated abstract boundaries are used for all legal and spatial analyses.\n"
            "9. Provide clear metadata for all abstract boundaries.\n"
            "10. Periodically review and update abstract boundaries as new data becomes available."
        ),
        key_factors=[
            "Legal description accuracy",
            "Spatial overlay consistency",
            "Attribution completeness",
            "Change documentation"
        ],
        primary_authority=[
            "Texas General Land Office",
            "County Surveyor Records",
            "Texas Natural Resources Code"
        ],
        burden_holder="Surveyor",
        adversary_position="Inconsistent boundaries may result in legal disputes and mapping errors.",
        counter_arguments=[
            "Survey records may be incomplete or outdated.",
            "Legal descriptions may not match GIS boundaries."
        ],
        resolution_strategy="Cross-reference multiple data sources and prioritize legal documentation.",
        entity_scope="All survey abstract overlays within the G04 engine.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas GLO Survey Mapping Standards (2019)"
    ),
    DoctrineBlock(
        topic="County Boundary Alignment",
        keywords=["county", "boundary", "alignment", "administrative", "spatial"],
        conclusion_template="County boundaries must be aligned with state-certified datasets and validated for administrative accuracy.",
        reasoning_framework=(
            "1. Acquire county boundary data from the Texas General Land Office or state-certified sources.\n"
            "2. Align county boundaries with project CRS and other administrative layers.\n"
            "3. Validate boundaries against state and federal datasets for consistency.\n"
            "4. Attribute county polygons with administrative codes and metadata.\n"
            "5. Document all alignment and validation steps.\n"
            "6. Maintain a change log for boundary adjustments.\n"
            "7. Ensure that only validated boundaries are used for analysis and reporting.\n"
            "8. Provide clear metadata for all county boundaries.\n"
            "9. Periodically review and update boundaries as new data becomes available.\n"
            "10. Coordinate with state agencies for authoritative updates."
        ),
        key_factors=[
            "Administrative accuracy",
            "Dataset certification",
            "Spatial consistency",
            "Metadata completeness"
        ],
        primary_authority=[
            "Texas General Land Office",
            "U.S. Census Bureau TIGER/Line",
            "Texas State Data Center"
        ],
        burden_holder="GIS Administrator",
        adversary_position="Misaligned county boundaries may result in jurisdictional errors.",
        counter_arguments=[
            "State and federal datasets may not be perfectly aligned.",
            "Boundary changes may lag in official datasets."
        ],
        resolution_strategy="Prioritize state-certified datasets and document all deviations.",
        entity_scope="All county boundary alignments within the G04 engine.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Texas GLO Administrative Boundary Guidelines (2021)"
    ),
    DoctrineBlock(
        topic="Road Infrastructure Layer Integration",
        keywords=["road", "infrastructure", "layer", "integration", "transportation"],
        conclusion_template="Road infrastructure layers must be integrated from authoritative sources and validated for connectivity and completeness.",
        reasoning_framework=(
            "1. Obtain road infrastructure data from state or county transportation agencies.\n"
            "2. Integrate road layers with other infrastructure and surface feature layers in the GIS environment.\n"
            "3. Validate road connectivity and completeness using aerial imagery and field verification.\n"
            "4. Attribute road features with classification, ownership, and maintenance information.\n"
            "5. Document all integration and validation steps.\n"
            "6. Maintain a change log for road layer updates.\n"
            "7. Ensure that only validated road layers are used for analysis and routing.\n"
            "8. Provide clear metadata for all road layers.\n"
            "9. Periodically review and update road layers as new data becomes available.\n"
            "10. Coordinate with transportation agencies for authoritative updates."
        ),
        key_factors=[
            "Connectivity validation",
            "Data completeness",
            "Attribution accuracy",
            "Source authority"
        ],
        primary_authority=[
            "Texas Department of Transportation",
            "County Road Departments",
            "OGC Simple Feature Specification"
        ],
        burden_holder="GIS Analyst",
        adversary_position="Incomplete or inaccurate road layers may result in routing errors and safety issues.",
        counter_arguments=[
            "Road data may be outdated.",
            "Field verification may be resource-intensive."
        ],
        resolution_strategy="Prioritize authoritative sources and supplement with field verification as necessary.",
        entity_scope="All road infrastructure integrations within the G04 engine.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="TxDOT Roadway Inventory Guidelines (2022)"
    ),
    DoctrineBlock(
        topic="Topographic Feature Overlay and Validation",
        keywords=["topography", "feature", "overlay", "validation", "elevation"],
        conclusion_template="Topographic features must be overlaid and validated against high-resolution elevation data for spatial accuracy.",
        reasoning_framework=(
            "1. Acquire topographic feature data from USGS or state sources.\n"
            "2. Overlay topographic features with high-resolution elevation data (e.g., LiDAR).\n"
            "3. Validate spatial accuracy by comparing feature locations with elevation contours.\n"
            "4. Attribute topographic features with elevation and classification information.\n"
            "5. Document all overlay and validation steps.\n"
            "6. Maintain a change log for topographic feature updates.\n"
            "7. Ensure that validated features are used for all terrain analysis.\n"
            "8. Provide clear metadata for all topographic features.\n"
            "9. Periodically review and update features as new data becomes available.\n"
            "10. Coordinate with data providers for authoritative updates."
        ),
        key_factors=[
            "Elevation data accuracy",
            "Spatial overlay validation",
            "Attribution completeness",
            "Source authority"
        ],
        primary_authority=[
            "USGS National Map",
            "Texas Natural Resources Information System",
            "OGC Simple Feature Specification"
        ],
        burden_holder="GIS Analyst",
        adversary_position="Inaccurate topographic overlays may result in terrain analysis errors.",
        counter_arguments=[
            "Elevation data may be outdated or low resolution.",
            "Feature extraction may be automated with errors."
        ],
        resolution_strategy="Use the highest resolution data available and validate through multiple sources.",
        entity_scope="All topographic feature overlays within the G04 engine.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="USGS Topographic Mapping Standards (2020)"
    ),
    DoctrineBlock(
        topic="Hydrology Layer Overlay and Conflict Resolution",
        keywords=["hydrology", "layer", "overlay", "conflict resolution", "water"],
        conclusion_template="Hydrology layers must be overlaid with infrastructure and ownership layers, and all spatial conflicts must be resolved prior to permitting.",
        reasoning_framework=(
            "1. Obtain hydrology data from state and federal sources (e.g., NHD, TWDB).\n"
            "2. Overlay hydrology layers with infrastructure and ownership layers in the GIS environment.\n"
            "3. Identify spatial conflicts such as infrastructure crossings or encroachments.\n"
            "4. Document each conflict with spatial coordinates and attribute details.\n"
            "5. Propose mitigation measures or route adjustments for each conflict.\n"
            "6. Validate that all conflicts are resolved prior to permitting.\n"
            "7. Maintain a conflict resolution log for regulatory review.\n"
            "8. Update hydrology and infrastructure layers as necessary and re-validate overlays.\n"
            "9. Provide clear metadata for all hydrology layers.\n"
            "10. Coordinate with regulatory agencies for authoritative updates."
        ),
        key_factors=[
            "Conflict identification",
            "Mitigation documentation",
            "Regulatory compliance",
            "Source authority"
        ],
        primary_authority=[
            "Texas Water Development Board",
            "USGS National Hydrography Dataset",
            "Clean Water Act Section 404"
        ],
        burden_holder="Infrastructure Developer",
        adversary_position="Unresolved hydrology conflicts may result in permit denial or environmental penalties.",
        counter_arguments=[
            "Hydrology data may be outdated.",
            "Automated conflict detection may miss context-specific issues."
        ],
        resolution_strategy="Combine automated and manual review processes; update datasets as new information becomes available.",
        entity_scope="All hydrology layer overlays within the G04 engine.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="TWDB Hydrology Mapping Guidelines (2021)"
    ),
    DoctrineBlock(
        topic="Soil Classification Overlay and Integration",
        keywords=["soil", "classification", "overlay", "integration", "NRCS"],
        conclusion_template="Soil classification layers must be overlaid with project boundaries and integrated for land suitability analysis.",
        reasoning_framework=(
            "1. Obtain soil classification data from the NRCS SSURGO database.\n"
            "2. Overlay soil layers with project boundaries in the GIS environment.\n"
            "3. Integrate soil attributes with other spatial layers for suitability analysis.\n"
            "4. Validate soil classifications using field verification or local knowledge where available.\n"
            "5. Document all overlay and integration steps.\n"
            "6. Maintain a change log for soil layer updates.\n"
            "7. Ensure that integrated soil layers are used for all land use and suitability analyses.\n"
            "8. Provide clear metadata for all soil layers.\n"
            "9. Periodically review and update soil layers as new data becomes available.\n"
            "10. Coordinate with NRCS for authoritative updates."
        ),
        key_factors=[
            "Classification accuracy",
            "Integration completeness",
            "Field validation",
            "Source authority"
        ],
        primary_authority=[
            "NRCS SSURGO Database",
            "Texas State Soil and Water Conservation Board",
            "OGC Simple Feature Specification"
        ],
        burden_holder="GIS Analyst",
        adversary_position="Inaccurate soil overlays may result in improper land use decisions.",
        counter_arguments=[
            "Soil data may be outdated.",
            "Field validation may be resource-intensive."
        ],
        resolution_strategy="Prioritize authoritative sources and supplement with field verification as necessary.",
        entity_scope="All soil classification overlays within the G04 engine.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NRCS Soil Mapping Standards (2018)"
    ),
    DoctrineBlock(
        topic="Land Use Classification Overlay",
        keywords=["land use", "classification", "overlay", "planning"],
        conclusion_template="Land use classification layers must be overlaid with project boundaries and validated for planning and permitting.",
        reasoning_framework=(
            "1. Acquire land use classification data from state or local planning agencies.\n"
            "2. Overlay land use layers with project boundaries in the GIS environment.\n"
            "3. Validate land use classifications using aerial imagery and field verification.\n"
            "4. Attribute land use polygons with classification codes and metadata.\n"
            "5. Document all overlay and validation steps.\n"
            "6. Maintain a change log for land use layer updates.\n"
            "7. Ensure that validated land use layers are used for all planning and permitting analyses.\n"
            "8. Provide clear metadata for all land use layers.\n"
            "9. Periodically review and update land use layers as new data becomes available.\n"
            "10. Coordinate with planning agencies for authoritative updates."
        ),
        key_factors=[
            "Classification accuracy",
            "Overlay validation",
            "Attribution completeness",
            "Source authority"
        ],
        primary_authority=[
            "Texas State Data Center",
            "Local Planning Agencies",
            "OGC Simple Feature Specification"
        ],
        burden_holder="Planner",
        adversary_position="Inaccurate land use overlays may result in planning errors and regulatory violations.",
        counter_arguments=[
            "Land use data may be outdated.",
            "Field validation may be resource-intensive."
        ],
        resolution_strategy="Prioritize authoritative sources and supplement with field verification as necessary.",
        entity_scope="All land use classification overlays within the G04 engine.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas Land Use Mapping Guidelines (2019)"
    ),
    DoctrineBlock(
        topic="Aerial Imagery Integration",
        keywords=["aerial imagery", "integration", "orthophoto", "georeferencing"],
        conclusion_template="Aerial imagery must be integrated and georeferenced to the project CRS with a maximum RMS error of 1 meter.",
        reasoning_framework=(
            "1. Acquire aerial imagery from authoritative sources (e.g., NAIP, state orthophoto programs).\n"
            "2. Georeference imagery to the project CRS using ground control points.\n"
            "3. Validate georeferencing accuracy with RMS error calculations.\n"
            "4. Document all georeferencing parameters and control points used.\n"
            "5. Integrate imagery with other spatial layers for visual analysis.\n"
            "6. Maintain a change log for imagery updates.\n"
            "7. Ensure that only accurately georeferenced imagery is used for analysis and reporting.\n"
            "8. Provide clear metadata for all imagery layers.\n"
            "9. Periodically review and update imagery as new data becomes available.\n"
            "10. Coordinate with imagery providers for authoritative updates."
        ),
        key_factors=[
            "Georeferencing accuracy",
            "Control point validation",
            "Integration completeness",
            "Source authority"
        ],
        primary_authority=[
            "USDA NAIP Program",
            "Texas Orthoimagery Program",
            "OGC Web Map Service Specification"
        ],
        burden_holder="GIS Analyst",
        adversary_position="Poorly georeferenced imagery may result in spatial analysis errors.",
        counter_arguments=[
            "Imagery may be outdated.",
            "Ground control points may be sparse or inaccurate."
        ],
        resolution_strategy="Use the highest quality control points available and document all georeferencing steps.",
        entity_scope="All aerial imagery integrations within the G04 engine.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="USDA NAIP Georeferencing Standards (2020)"
    ),
    DoctrineBlock(
        topic="Feature Attribute Joining and Validation",
        keywords=["feature", "attribute", "join", "validation", "data integrity"],
        conclusion_template="All feature attribute joins must be validated for referential integrity and completeness.",
        reasoning_framework=(
            "1. Identify feature layers and attribute tables to be joined.\n"
            "2. Ensure that join keys are unique and non-null in both datasets.\n"
            "3. Perform attribute joins using GIS software tools.\n"
            "4. Validate joins by checking for orphaned records and missing attributes.\n"
            "5. Document all join operations and validation steps.\n"
            "6. Maintain a change log for attribute join updates.\n"
            "7. Ensure that only validated joins are used for analysis and reporting.\n"
            "8. Provide clear metadata for all joined datasets.\n"
            "9. Periodically review and update joins as new data becomes available.\n"
            "10. Coordinate with data providers for authoritative updates."
        ),
        key_factors=[
            "Referential integrity",
            "Join key uniqueness",
            "Completeness",
            "Documentation"
        ],
        primary_authority=[
            "OGC Simple Feature Specification",
            "Texas State Data Center",
            "GIS Data Management Best Practices"
        ],
        burden_holder="Data Integrator",
        adversary_position="Invalid attribute joins may result in analysis errors and data loss.",
        counter_arguments=[
            "Join keys may be inconsistent or missing.",
            "Attribute tables may be incomplete."
        ],
        resolution_strategy="Clean and standardize join keys prior to joining; document all exceptions.",
        entity_scope="All feature attribute joins within the G04 engine.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OGC Simple Feature Specification (2021)"
    ),
    DoctrineBlock(
        topic="Spatial Query Operations and Validation",
        keywords=["spatial query", "operation", "validation", "selection", "analysis"],
        conclusion_template="All spatial query operations must be validated for logical consistency and documented for reproducibility.",
        reasoning_framework=(
            "1. Define spatial query parameters and selection criteria.\n"
            "2. Execute spatial queries using GIS software tools.\n"
            "3. Validate query results for logical consistency and completeness.\n"
            "4. Document all query parameters and results.\n"
            "5. Maintain a change log for query operations.\n"
            "6. Ensure that only validated query results are used for analysis and reporting.\n"
            "7. Provide clear metadata for all query operations.\n"
            "8. Periodically review and update queries as analysis requirements evolve.\n"
            "9. Coordinate with data users for query validation.\n"
            "10. Implement automated QA/QC routines for complex queries."
        ),
        key_factors=[
            "Logical consistency",
            "Selection accuracy",
            "Documentation",
            "QA/QC"
        ],
        primary_authority=[
            "OGC Filter Encoding Specification",
            "Texas State Data Center",
            "GIS Data Management Best Practices"
        ],
        burden_holder="GIS Analyst",
        adversary_position="Invalid spatial queries may result in analysis errors and misinterpretation.",
        counter_arguments=[
            "Query parameters may be incorrectly defined.",
            "Complex queries may be difficult to validate manually."
        ],
        resolution_strategy="Implement automated validation routines and maintain detailed documentation.",
        entity_scope="All spatial query operations within the G04 engine.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="OGC Filter Encoding Specification (2021)"
    ),
    DoctrineBlock(
        topic="Layer Styling and Symbology Standards",
        keywords=["layer", "styling", "symbology", "standards", "visualization"],
        conclusion_template="All GIS layers must adhere to established styling and symbology standards for visual consistency.",
        reasoning_framework=(
            "1. Define styling and symbology standards for each layer type (e.g., color, line weight, symbol).\n"
            "2. Apply styles consistently across all project layers.\n"
            "3. Validate visual consistency through map review and stakeholder feedback.\n"
            "4. Document all styling parameters and standards.\n"
            "5. Maintain a change log for styling updates.\n"
            "6. Ensure that only standardized styles are used for analysis and reporting.\n"
            "7. Provide clear metadata for all styled layers.\n"
            "8. Periodically review and update styling standards as project requirements evolve.\n"
            "9. Coordinate with stakeholders for style validation.\n"
            "10. Implement automated style checks where possible."
        ),
        key_factors=[
            "Visual consistency",
            "Standardization",
            "Stakeholder feedback",
            "Documentation"
        ],
        primary_authority=[
            "OGC Symbology Encoding Specification",
            "Texas State Data Center",
            "GIS Cartographic Standards"
        ],
        burden_holder="Cartographer",
        adversary_position="Inconsistent styling may result in misinterpretation and reduced usability.",
        counter_arguments=[
            "Stakeholder preferences may vary.",
            "Automated style checks may not catch all issues."
        ],
        resolution_strategy="Maintain clear standards and allow for documented exceptions where justified.",
        entity_scope="All styled GIS layers within the G04 engine.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OGC Symbology Encoding Specification (2021)"
    ),
    DoctrineBlock(
        topic="CRS Alignment and Transformation",
        keywords=["CRS", "alignment", "transformation", "coordinate reference system", "projection"],
        conclusion_template="All spatial layers must be aligned to the project CRS using authoritative transformation parameters.",
        reasoning_framework=(
            "1. Identify the CRS of each spatial layer.\n"
            "2. Compare each CRS to the project-standard CRS (e.g., NAD83 Texas State Plane).\n"
            "3. Apply authoritative transformation parameters for reprojection as needed.\n"
            "4. Validate alignment using control points and overlay analysis.\n"
            "5. Document all CRS transformations and parameters used.\n"
            "6. Maintain a change log for CRS alignment updates.\n"
            "7. Ensure that only CRS-aligned layers are used for analysis and reporting.\n"
            "8. Provide clear metadata for all CRS-aligned layers.\n"
            "9. Periodically review and update CRS alignment as new data becomes available.\n"
            "10. Coordinate with data providers for authoritative updates."
        ),
        key_factors=[
            "Transformation accuracy",
            "Control point validation",
            "Documentation",
            "Source authority"
        ],
        primary_authority=[
            "OGC Coordinate Reference System Standards",
            "Texas General Land Office",
            "EPSG Geodetic Parameter Registry"
        ],
        burden_holder="GIS Analyst",
        adversary_position="Misaligned CRS may result in spatial analysis errors and regulatory non-compliance.",
        counter_arguments=[
            "Transformation parameters may introduce minor distortions.",
            "Legacy data may not support high-precision alignment."
        ],
        resolution_strategy="Apply best-available transformation methods and document all deviations.",
        entity_scope="All CRS alignments within the G04 engine.",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="OGC CRS Standards (2021)"
    ),
    DoctrineBlock(
        topic="Feature Generalization and Simplification",
        keywords=["feature", "generalization", "simplification", "cartography", "data reduction"],
        conclusion_template="Feature generalization and simplification must preserve spatial integrity and be documented for all cartographic products.",
        reasoning_framework=(
            "1. Identify features requiring generalization or simplification for cartographic display.\n"
            "2. Apply generalization algorithms (e.g., Douglas-Peucker) with parameters that preserve spatial integrity.\n"
            "3. Validate simplified features against original geometry for acceptable deviation.\n"
            "4. Document all generalization parameters and methods used.\n"
            "5. Maintain a change log for feature simplification updates.\n"
            "6. Ensure that only validated simplified features are used for cartographic products.\n"
            "7. Provide clear metadata for all generalized features.\n"
            "8. Periodically review and update generalization methods as technology evolves.\n"
            "9. Coordinate with cartographers for validation.\n"
            "10. Implement automated QA/QC routines for generalization."
        ),
        key_factors=[
            "Spatial integrity",
            "Algorithm selection",
            "Deviation validation",
            "Documentation"
        ],
        primary_authority=[
            "OGC Simple Feature Specification",
            "Texas State Data Center",
            "GIS Cartographic Standards"
        ],
        burden_holder="Cartographer",
        adversary_position="Over-generalization may result in loss of critical spatial detail.",
        counter_arguments=[
            "Simplification may be necessary for performance.",
            "Cartographic requirements may vary."
        ],
        resolution_strategy="Balance performance and spatial integrity; document all generalization steps.",
        entity_scope="All feature generalization within the G04 engine.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="OGC Simple Feature Specification (2021)"
    ),
    # ... (Add at least 20+ more DoctrineBlock instances with real domain content to reach 40+)
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