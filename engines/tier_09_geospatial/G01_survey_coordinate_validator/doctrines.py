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
        topic="Texas State Plane Coordinate System - North Central Zone Definition",
        keywords=[
            "Texas State Plane", "North Central Zone", "coordinate system", "projection", "SPCS83", "NAD83"
        ],
        conclusion_template="The Texas State Plane Coordinate System (SPCS) North Central Zone is defined by NAD83 datum using the Lambert Conformal Conic projection with specific parameters as established by the Texas General Land Office and the National Geodetic Survey.",
        reasoning_framework=(
            "The Texas State Plane Coordinate System (SPCS) divides Texas into multiple zones for high-accuracy mapping. "
            "The North Central Zone is defined by the National Geodetic Survey (NGS) and the Texas General Land Office (GLO) "
            "using the NAD83 datum and the Lambert Conformal Conic projection. The parameters for this zone are specified in "
            "the Code of Federal Regulations (CFR) and the Texas Administrative Code (TAC). The zone provides a standard "
            "reference for surveyors and GIS professionals, ensuring spatial data consistency across agencies. "
            "The coordinate system is used for legal land descriptions, engineering, and mapping. The system's parameters are "
            "subject to updates as datums and projections evolve, but the current standard is NAD83 with Lambert Conformal Conic, "
            "as outlined in the EPSG registry (EPSG:32138)."
        ),
        key_factors=[
            "Datum: NAD83", "Projection: Lambert Conformal Conic", "Zone parameters", "Legal and regulatory standards",
            "EPSG code: 32138", "State and federal guidance"
        ],
        primary_authority=[
            "Texas Administrative Code, Title 1, Part 4, Chapter 3", "National Geodetic Survey", "EPSG Registry"
        ],
        burden_holder="Surveyor submitting coordinate data",
        adversary_position="Alternate coordinate system or datum used",
        counter_arguments=[
            "Alternate datums (e.g., NAD27, WGS84) may be used for legacy data",
            "Local coordinate systems may be justified for specific projects"
        ],
        resolution_strategy="Require documentation of coordinate system and transformation parameters; default to SPCS83 North Central Zone for regulatory submissions.",
        entity_scope="Surveyors, GIS professionals, state agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Texas Administrative Code, Title 1, Part 4, Chapter 3"
    ),
    DoctrineBlock(
        topic="NAD83 to NAD27 Transformation in Texas",
        keywords=[
            "NAD83", "NAD27", "datum transformation", "coordinate conversion", "Texas", "survey"
        ],
        conclusion_template="Transformation from NAD83 to NAD27 in Texas must use the NGS-published transformation grids (NADCON) and document all parameters and residuals.",
        reasoning_framework=(
            "NAD83 and NAD27 are distinct geodetic datums with different reference ellipsoids and origins. "
            "Transforming coordinates between these datums in Texas requires the use of the NADCON transformation grids, "
            "as published by the National Geodetic Survey. The transformation is not a simple mathematical shift but involves "
            "interpolation from grid files that account for local distortions. Surveyors must document the transformation method, "
            "software used, and any residuals or errors. The Texas Board of Professional Land Surveying requires such documentation "
            "for legal land descriptions. Failure to use the correct transformation can result in significant positional errors, "
            "potentially invalidating survey results."
        ),
        key_factors=[
            "Use of NADCON grids", "Documentation of transformation", "Residuals/errors", "Legal requirements"
        ],
        primary_authority=[
            "National Geodetic Survey (NGS)", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor performing transformation",
        adversary_position="Use of simplified or undocumented transformation methods",
        counter_arguments=[
            "Small projects may claim negligible error",
            "Legacy data may lack transformation documentation"
        ],
        resolution_strategy="Require use of NGS-published NADCON grids and full documentation for all transformations.",
        entity_scope="Surveyors, engineers, GIS professionals",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="NGS NADCON documentation"
    ),
    DoctrineBlock(
        topic="WGS84 Datum Usage in Texas Surveying",
        keywords=[
            "WGS84", "datum", "surveying", "GPS", "Texas", "coordinate system"
        ],
        conclusion_template="WGS84 is permitted for GPS data collection in Texas, but must be transformed to NAD83 or SPCS for regulatory submissions.",
        reasoning_framework=(
            "WGS84 is the global geodetic datum used by GPS systems. In Texas, surveyors may collect data in WGS84, "
            "but for regulatory, legal, or mapping purposes, coordinates must be transformed to the official state plane "
            "coordinate system (NAD83/SPCS). The transformation between WGS84 and NAD83 is minor but non-negligible, "
            "especially for high-precision applications. The NGS provides transformation parameters and tools. "
            "Surveyors must document the transformation process and software used. Failure to transform WGS84 data "
            "can result in misalignment with state datasets and legal disputes."
        ),
        key_factors=[
            "WGS84 GPS data collection", "Transformation to NAD83/SPCS", "Documentation", "Precision requirements"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor submitting data",
        adversary_position="Submission of WGS84 coordinates without transformation",
        counter_arguments=[
            "WGS84 and NAD83 are nearly identical for small-scale mapping",
            "Some agencies may accept WGS84 for non-legal purposes"
        ],
        resolution_strategy="Require transformation and documentation for all regulatory submissions.",
        entity_scope="Surveyors, GIS professionals, state agencies",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NGS Transformation Guidelines"
    ),
    DoctrineBlock(
        topic="EPSG Codes for Texas State Plane Zones",
        keywords=[
            "EPSG", "Texas State Plane", "zone codes", "coordinate reference system", "SPCS83", "SPCS27"
        ],
        conclusion_template="Each Texas State Plane zone has a unique EPSG code; for North Central NAD83, use EPSG:32138.",
        reasoning_framework=(
            "The European Petroleum Survey Group (EPSG) maintains a registry of coordinate reference systems, "
            "assigning unique codes to each. Texas State Plane zones are included, with separate codes for NAD27 and NAD83 datums. "
            "For the North Central Zone under NAD83, the EPSG code is 32138. Surveyors and GIS professionals must use the correct "
            "EPSG code when specifying coordinate systems in software, metadata, and regulatory submissions. "
            "Incorrect EPSG codes can lead to misinterpretation of spatial data and legal challenges."
        ),
        key_factors=[
            "Correct EPSG code usage", "Datum and projection identification", "Software interoperability"
        ],
        primary_authority=[
            "EPSG Registry", "Texas General Land Office"
        ],
        burden_holder="Data submitter",
        adversary_position="Use of incorrect or unspecified EPSG codes",
        counter_arguments=[
            "Some legacy systems do not support EPSG codes",
            "Local codes may be used internally"
        ],
        resolution_strategy="Require EPSG code specification in all metadata and submissions.",
        entity_scope="Surveyors, GIS professionals, state agencies",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="EPSG Registry"
    ),
    DoctrineBlock(
        topic="Lambert Conformal Conic Projection Parameters for Texas",
        keywords=[
            "Lambert Conformal Conic", "projection parameters", "Texas", "State Plane", "standard parallels", "central meridian"
        ],
        conclusion_template="The Lambert Conformal Conic projection for Texas State Plane zones uses zone-specific standard parallels, central meridian, and false easting/northing as defined by the NGS.",
        reasoning_framework=(
            "The Lambert Conformal Conic projection is used for Texas State Plane zones due to its suitability for east-west "
            "extending regions. Each zone has unique parameters: two standard parallels, a central meridian, latitude of origin, "
            "false easting, and false northing. These parameters are defined by the National Geodetic Survey and codified in the "
            "Texas Administrative Code. Surveyors must use the correct parameters for their zone to ensure spatial data accuracy. "
            "Incorrect projection parameters can result in significant coordinate errors and legal disputes."
        ),
        key_factors=[
            "Zone-specific projection parameters", "NGS definitions", "Legal and regulatory requirements"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Administrative Code"
        ],
        burden_holder="Surveyor or GIS professional",
        adversary_position="Use of incorrect or generic projection parameters",
        counter_arguments=[
            "Some software defaults may not match official parameters",
            "Legacy data may use outdated parameters"
        ],
        resolution_strategy="Require documentation of projection parameters and verification against NGS definitions.",
        entity_scope="Surveyors, GIS professionals, engineers",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NGS State Plane Coordinate System Specifications"
    ),
    DoctrineBlock(
        topic="Legal Status of State Plane Coordinates in Texas Land Surveys",
        keywords=[
            "legal status", "state plane coordinates", "Texas", "land survey", "property boundary", "statute"
        ],
        conclusion_template="State Plane Coordinates are legally recognized for land surveys in Texas when referenced to the appropriate zone and datum.",
        reasoning_framework=(
            "Texas statutes and administrative codes recognize State Plane Coordinates as a legal means of describing property boundaries, "
            "provided the correct zone and datum are specified. The Texas Board of Professional Land Surveying requires that all coordinate "
            "references in legal documents include the datum, zone, and projection parameters. This ensures clarity and prevents disputes "
            "arising from ambiguous or incorrect coordinate references. Surveyors must maintain documentation and metadata for all submissions."
        ),
        key_factors=[
            "Statutory recognition", "Datum and zone specification", "Documentation requirements"
        ],
        primary_authority=[
            "Texas Administrative Code", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor preparing legal descriptions",
        adversary_position="Use of local or ambiguous coordinate systems",
        counter_arguments=[
            "Some counties may have local requirements",
            "Older surveys may lack full coordinate documentation"
        ],
        resolution_strategy="Require full coordinate system specification and reference to legal authority.",
        entity_scope="Surveyors, title companies, attorneys",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Administrative Code, Title 1, Part 4, Chapter 3"
    ),
    DoctrineBlock(
        topic="Datum Tagging in Texas Survey Deliverables",
        keywords=[
            "datum tagging", "survey deliverables", "metadata", "NAD83", "NAD27", "WGS84", "Texas"
        ],
        conclusion_template="All survey deliverables in Texas must include explicit datum tagging in metadata and documentation.",
        reasoning_framework=(
            "Datum tagging is the explicit identification of the geodetic datum used for coordinate data. In Texas, all survey deliverables "
            "must include datum information in both metadata and documentation. This requirement is enforced by the Texas Board of Professional "
            "Land Surveying and is critical for data interoperability and legal defensibility. Omission of datum tagging can lead to "
            "misinterpretation of coordinates and legal disputes. Surveyors must ensure that all digital and paper deliverables clearly state "
            "the datum (e.g., NAD83, NAD27, WGS84) and, if applicable, the transformation method used."
        ),
        key_factors=[
            "Datum identification", "Metadata standards", "Legal requirements"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "National Geodetic Survey"
        ],
        burden_holder="Surveyor or data provider",
        adversary_position="Omission of datum information",
        counter_arguments=[
            "Legacy data may lack datum tagging",
            "Some software does not enforce metadata standards"
        ],
        resolution_strategy="Reject deliverables lacking explicit datum tagging.",
        entity_scope="Surveyors, GIS professionals, regulatory agencies",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Use of Grid vs. Ground Coordinates in Texas",
        keywords=[
            "grid coordinates", "ground coordinates", "scale factor", "Texas", "survey", "state plane"
        ],
        conclusion_template="Surveyors must specify whether coordinates are grid or ground, and provide scale factors if ground coordinates are used.",
        reasoning_framework=(
            "Grid coordinates are projected values on the State Plane system, while ground coordinates are adjusted for local scale. "
            "In Texas, surveyors must specify which type is used and provide the scale factor if ground coordinates are reported. "
            "This distinction is critical for construction, engineering, and legal purposes. The Texas Board of Professional Land Surveying "
            "requires documentation of scale factors and methods used for conversion. Ambiguity can lead to construction errors and legal disputes."
        ),
        key_factors=[
            "Grid vs. ground distinction", "Scale factor documentation", "Legal and engineering standards"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "Texas Administrative Code"
        ],
        burden_holder="Surveyor reporting coordinates",
        adversary_position="Omission of scale factor or coordinate type",
        counter_arguments=[
            "Some projects may not require ground coordinates",
            "Legacy data may lack this information"
        ],
        resolution_strategy="Require explicit specification and documentation in all deliverables.",
        entity_scope="Surveyors, engineers, contractors",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Official Transformation Tools for Texas Coordinate Systems",
        keywords=[
            "transformation tools", "NGS", "NADCON", "VERTCON", "Texas", "coordinate system"
        ],
        conclusion_template="Surveyors in Texas must use NGS-published tools (NADCON, VERTCON) for all official datum and vertical transformations.",
        reasoning_framework=(
            "The National Geodetic Survey publishes official tools for horizontal (NADCON) and vertical (VERTCON) datum transformations. "
            "Texas surveyors are required to use these tools for all legal and regulatory submissions involving coordinate transformations. "
            "Third-party or proprietary methods are not acceptable unless validated against NGS results. Documentation of the tool version, "
            "parameters, and residuals is required. This ensures consistency and legal defensibility of transformed data."
        ),
        key_factors=[
            "Use of official tools", "Documentation of transformation", "Legal requirements"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor performing transformation",
        adversary_position="Use of unvalidated or proprietary transformation methods",
        counter_arguments=[
            "Some software may implement NGS algorithms",
            "Legacy data may lack transformation documentation"
        ],
        resolution_strategy="Require use of NGS tools and full documentation for all transformations.",
        entity_scope="Surveyors, GIS professionals, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NGS Transformation Guidelines"
    ),
    DoctrineBlock(
        topic="Vertical Datum Standards in Texas",
        keywords=[
            "vertical datum", "NAVD88", "NGVD29", "elevation", "Texas", "survey"
        ],
        conclusion_template="NAVD88 is the official vertical datum for Texas; NGVD29 is accepted only for legacy data with documented transformation.",
        reasoning_framework=(
            "The North American Vertical Datum of 1988 (NAVD88) is the official vertical datum for Texas. Surveyors must use NAVD88 for all new "
            "elevation data and document the datum in all deliverables. The National Geodetic Vertical Datum of 1929 (NGVD29) is accepted only "
            "for legacy data, and any transformation to or from NAVD88 must use NGS-published VERTCON grids. Documentation of transformation "
            "parameters and residuals is required. Use of outdated or undocumented vertical datums can lead to significant elevation errors."
        ),
        key_factors=[
            "Official vertical datum", "Transformation documentation", "Legacy data handling"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor reporting elevations",
        adversary_position="Use of NGVD29 without transformation or documentation",
        counter_arguments=[
            "Some agencies may still require NGVD29",
            "Legacy projects may lack transformation data"
        ],
        resolution_strategy="Require NAVD88 for all new data and documentation for any transformations.",
        entity_scope="Surveyors, engineers, regulatory agencies",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="NGS Vertical Datum Guidelines"
    ),
    DoctrineBlock(
        topic="Authority of the Texas General Land Office in Coordinate Standards",
        keywords=[
            "Texas General Land Office", "GLO", "coordinate standards", "state plane", "survey"
        ],
        conclusion_template="The Texas General Land Office is the primary state authority for coordinate system standards and specifications.",
        reasoning_framework=(
            "The Texas General Land Office (GLO) is empowered by state statute to establish and maintain coordinate system standards for Texas. "
            "The GLO works with the National Geodetic Survey and the Texas Board of Professional Land Surveying to publish official parameters, "
            "zone definitions, and datum specifications. Surveyors and agencies must adhere to GLO standards for all legal and regulatory submissions. "
            "The GLO also maintains archives of historical coordinate system definitions and provides guidance on updates."
        ),
        key_factors=[
            "Statutory authority", "Coordination with NGS", "Publication of standards"
        ],
        primary_authority=[
            "Texas General Land Office", "Texas Administrative Code"
        ],
        burden_holder="Surveyor or agency submitting data",
        adversary_position="Use of non-GLO standards",
        counter_arguments=[
            "Federal projects may use alternate standards",
            "Local agencies may have supplemental requirements"
        ],
        resolution_strategy="Default to GLO standards for all state-regulated activities.",
        entity_scope="Surveyors, state agencies, engineers",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Texas Natural Resources Code"
    ),
    DoctrineBlock(
        topic="EPSG:32138 - Texas North Central Zone NAD83",
        keywords=[
            "EPSG:32138", "Texas North Central", "NAD83", "coordinate system", "projection"
        ],
        conclusion_template="EPSG:32138 defines the Texas North Central State Plane Zone using NAD83 and Lambert Conformal Conic projection.",
        reasoning_framework=(
            "EPSG:32138 is the official code for the Texas North Central State Plane Zone under NAD83, using the Lambert Conformal Conic projection. "
            "This code is recognized internationally and ensures interoperability between GIS and CAD software. Surveyors must use this code when "
            "specifying the coordinate system for data submissions in this zone. Failure to use the correct code can result in misalignment and "
            "legal disputes."
        ),
        key_factors=[
            "EPSG code specification", "Datum and projection", "Software interoperability"
        ],
        primary_authority=[
            "EPSG Registry", "National Geodetic Survey"
        ],
        burden_holder="Surveyor or data provider",
        adversary_position="Omission or use of incorrect EPSG code",
        counter_arguments=[
            "Some legacy systems may not support EPSG codes",
            "Local codes may be used for internal purposes"
        ],
        resolution_strategy="Require EPSG:32138 for all North Central Zone NAD83 submissions.",
        entity_scope="Surveyors, GIS professionals, engineers",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="EPSG Registry"
    ),
    DoctrineBlock(
        topic="EPSG:2276 - Texas North Central Zone NAD27",
        keywords=[
            "EPSG:2276", "Texas North Central", "NAD27", "coordinate system", "projection"
        ],
        conclusion_template="EPSG:2276 defines the Texas North Central State Plane Zone using NAD27 and Lambert Conformal Conic projection.",
        reasoning_framework=(
            "EPSG:2276 is the official code for the Texas North Central State Plane Zone under NAD27, using the Lambert Conformal Conic projection. "
            "This code is used for legacy data and must be specified in all metadata and documentation for NAD27-based coordinates. "
            "Surveyors must ensure that any transformation to or from NAD83 is documented and performed using NGS tools."
        ),
        key_factors=[
            "EPSG code specification", "Datum and projection", "Legacy data handling"
        ],
        primary_authority=[
            "EPSG Registry", "National Geodetic Survey"
        ],
        burden_holder="Surveyor or data provider",
        adversary_position="Omission or use of incorrect EPSG code",
        counter_arguments=[
            "Some legacy systems may not support EPSG codes",
            "Local codes may be used for internal purposes"
        ],
        resolution_strategy="Require EPSG:2276 for all North Central Zone NAD27 submissions.",
        entity_scope="Surveyors, GIS professionals, engineers",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="EPSG Registry"
    ),
    DoctrineBlock(
        topic="Metadata Requirements for Texas Coordinate Data",
        keywords=[
            "metadata", "coordinate data", "Texas", "survey", "datum", "projection", "EPSG"
        ],
        conclusion_template="All Texas coordinate data must include complete metadata specifying datum, projection, zone, and EPSG code.",
        reasoning_framework=(
            "Metadata is essential for the correct interpretation and use of coordinate data. In Texas, all survey and GIS data must include "
            "metadata specifying the datum, projection, zone, and EPSG code. This requirement is enforced by the Texas Board of Professional "
            "Land Surveying and the Texas General Land Office. Metadata ensures interoperability, legal defensibility, and prevents errors "
            "arising from ambiguous coordinate references."
        ),
        key_factors=[
            "Complete metadata", "Datum and projection specification", "Legal and regulatory requirements"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "Texas General Land Office"
        ],
        burden_holder="Data provider",
        adversary_position="Omission or incomplete metadata",
        counter_arguments=[
            "Legacy data may lack full metadata",
            "Some software does not enforce metadata standards"
        ],
        resolution_strategy="Reject data lacking complete metadata.",
        entity_scope="Surveyors, GIS professionals, regulatory agencies",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Transformation Documentation Requirements",
        keywords=[
            "transformation documentation", "datum conversion", "Texas", "survey", "metadata"
        ],
        conclusion_template="All coordinate transformations in Texas must be documented, including methods, parameters, and residuals.",
        reasoning_framework=(
            "Documentation of coordinate transformations is required to ensure traceability and legal defensibility. Surveyors must record "
            "the transformation method (e.g., NADCON), parameters, software version, and any residuals or errors. This documentation must "
            "be included in metadata and deliverables. Failure to document transformations can invalidate survey results and lead to legal disputes."
        ),
        key_factors=[
            "Transformation method", "Parameter documentation", "Legal requirements"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "National Geodetic Survey"
        ],
        burden_holder="Surveyor performing transformation",
        adversary_position="Omission of transformation documentation",
        counter_arguments=[
            "Legacy data may lack documentation",
            "Some transformations may be considered trivial"
        ],
        resolution_strategy="Require full documentation for all transformations.",
        entity_scope="Surveyors, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Survey Control Points and Coordinate System Consistency",
        keywords=[
            "control points", "coordinate system", "consistency", "Texas", "survey", "datum"
        ],
        conclusion_template="All control points must be referenced to the same coordinate system and datum as the project deliverables.",
        reasoning_framework=(
            "Survey control points provide the foundation for all coordinate measurements. In Texas, all control points used in a project "
            "must be referenced to the same coordinate system and datum as the project deliverables. This ensures internal consistency and "
            "prevents errors in mapping, construction, and legal descriptions. Surveyors must document the coordinate system for all control points."
        ),
        key_factors=[
            "Control point consistency", "Datum and projection specification", "Documentation"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "National Geodetic Survey"
        ],
        burden_holder="Surveyor establishing control",
        adversary_position="Use of mixed datums or projections",
        counter_arguments=[
            "Legacy control points may use different datums",
            "Some projects may require multiple systems"
        ],
        resolution_strategy="Require documentation and, if necessary, transformation to a common system.",
        entity_scope="Surveyors, engineers, contractors",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Use of Geoid Models in Texas Elevation Surveys",
        keywords=[
            "geoid model", "elevation", "survey", "Texas", "GEOID18", "NAVD88"
        ],
        conclusion_template="GEOID18 is the official geoid model for converting GPS ellipsoid heights to NAVD88 orthometric heights in Texas.",
        reasoning_framework=(
            "The National Geodetic Survey's GEOID18 model is the official standard for converting GPS-derived ellipsoid heights to NAVD88 "
            "orthometric heights in Texas. Surveyors must use GEOID18 for all new elevation surveys and document the model version in metadata. "
            "Use of outdated geoid models can result in significant elevation errors. GEOID18 supersedes previous models such as GEOID12B."
        ),
        key_factors=[
            "Official geoid model", "Elevation accuracy", "Documentation"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor performing elevation survey",
        adversary_position="Use of outdated or undocumented geoid models",
        counter_arguments=[
            "Legacy data may use older models",
            "Some projects may not require high-precision elevations"
        ],
        resolution_strategy="Require GEOID18 for all new elevation surveys.",
        entity_scope="Surveyors, engineers, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NGS GEOID18 Documentation"
    ),
    DoctrineBlock(
        topic="Handling Legacy Coordinate Data in Texas",
        keywords=[
            "legacy data", "coordinate system", "datum", "Texas", "NAD27", "NGVD29"
        ],
        conclusion_template="Legacy coordinate data in NAD27 or NGVD29 must be clearly identified and, if used, transformed and documented.",
        reasoning_framework=(
            "Legacy data in NAD27 or NGVD29 is common in Texas. Surveyors must clearly identify the datum and coordinate system for all legacy data. "
            "If legacy data is used in new projects, it must be transformed to current standards (NAD83, NAVD88) using NGS tools and fully documented. "
            "Failure to do so can result in significant positional or elevation errors."
        ),
        key_factors=[
            "Legacy data identification", "Transformation to current standards", "Documentation"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "National Geodetic Survey"
        ],
        burden_holder="Surveyor using legacy data",
        adversary_position="Use of legacy data without transformation or documentation",
        counter_arguments=[
            "Some projects may not require transformation",
            "Legacy data may be used for reference only"
        ],
        resolution_strategy="Require identification, transformation, and documentation for all legacy data used.",
        entity_scope="Surveyors, engineers, regulatory agencies",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Datum Realization Updates (NAD83 HARN, NAD83(2011))",
        keywords=[
            "datum realization", "NAD83 HARN", "NAD83(2011)", "Texas", "survey"
        ],
        conclusion_template="Surveyors must specify the NAD83 realization (e.g., HARN, CORS96, 2011) used for all coordinate data in Texas.",
        reasoning_framework=(
            "NAD83 has multiple realizations (HARN, CORS96, NSRS2007, 2011) reflecting updates in the reference frame. In Texas, surveyors must "
            "specify the realization used for all coordinate data. This is critical for high-precision work and data interoperability. "
            "Omission of the realization can result in errors of several centimeters or more."
        ),
        key_factors=[
            "Datum realization specification", "High-precision requirements", "Documentation"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor or data provider",
        adversary_position="Omission of realization information",
        counter_arguments=[
            "Some projects may not require high precision",
            "Legacy data may lack realization information"
        ],
        resolution_strategy="Require realization specification in all metadata and documentation.",
        entity_scope="Surveyors, GIS professionals, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NGS NAD83 Realization Guidelines"
    ),
    DoctrineBlock(
        topic="Use of Local Coordinate Systems in Texas Projects",
        keywords=[
            "local coordinate system", "Texas", "project-specific", "engineering", "survey"
        ],
        conclusion_template="Local coordinate systems may be used for project-specific purposes but must be documented and not used for legal submissions.",
        reasoning_framework=(
            "Local coordinate systems are sometimes used for engineering or construction projects for convenience. In Texas, such systems must be "
            "fully documented, including the origin, orientation, and any transformation parameters. Local systems are not acceptable for legal "
            "land descriptions or regulatory submissions, which must use official state plane or UTM systems."
        ),
        key_factors=[
            "Documentation of local system", "Legal submission requirements", "Project-specific use"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "Texas General Land Office"
        ],
        burden_holder="Engineer or surveyor using local system",
        adversary_position="Use of local system for legal submissions",
        counter_arguments=[
            "Local systems may be more convenient for some projects",
            "Some agencies may accept local systems for internal use"
        ],
        resolution_strategy="Restrict local systems to project use and require full documentation.",
        entity_scope="Engineers, surveyors, contractors",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="UTM Zones in Texas",
        keywords=[
            "UTM", "Universal Transverse Mercator", "Texas", "zones", "coordinate system"
        ],
        conclusion_template="UTM Zones 13, 14, and 15 cover Texas; surveyors must specify the correct zone and datum for all UTM coordinates.",
        reasoning_framework=(
            "Texas is covered by UTM Zones 13, 14, and 15. Surveyors using UTM coordinates must specify the correct zone and datum (e.g., NAD83, WGS84). "
            "UTM is not the official legal coordinate system for Texas land descriptions but may be used for mapping and engineering. "
            "Omission of the zone or datum can result in significant positional errors."
        ),
        key_factors=[
            "UTM zone specification", "Datum identification", "Legal vs. mapping use"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor or engineer using UTM",
        adversary_position="Omission of zone or datum information",
        counter_arguments=[
            "UTM is widely used for mapping",
            "Some projects may not require legal descriptions"
        ],
        resolution_strategy="Require full specification of zone and datum for all UTM data.",
        entity_scope="Surveyors, engineers, GIS professionals",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="NGS UTM Guidelines"
    ),
    DoctrineBlock(
        topic="Accuracy Standards for Texas State Plane Coordinates",
        keywords=[
            "accuracy standards", "state plane coordinates", "Texas", "survey", "tolerance"
        ],
        conclusion_template="Texas surveyors must meet minimum accuracy standards for State Plane Coordinates as defined by the Texas Board of Professional Land Surveying.",
        reasoning_framework=(
            "The Texas Board of Professional Land Surveying sets minimum accuracy standards for State Plane Coordinates used in legal and regulatory "
            "submissions. These standards vary by project type but generally require sub-centimeter to decimeter accuracy for control surveys. "
            "Surveyors must document methods and equipment used to achieve required accuracy. Failure to meet standards can result in rejection of deliverables."
        ),
        key_factors=[
            "Minimum accuracy requirements", "Documentation of methods", "Project type"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor submitting coordinates",
        adversary_position="Submission of data not meeting accuracy standards",
        counter_arguments=[
            "Some projects may not require high accuracy",
            "Legacy data may not meet current standards"
        ],
        resolution_strategy="Enforce accuracy standards for all legal and regulatory submissions.",
        entity_scope="Surveyors, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Reporting Units for Texas Coordinate Data",
        keywords=[
            "reporting units", "coordinate data", "feet", "meters", "Texas", "survey"
        ],
        conclusion_template="Texas State Plane Coordinates are reported in U.S. Survey Feet; metric units may be used if specified.",
        reasoning_framework=(
            "The Texas State Plane Coordinate System uses U.S. Survey Feet as the default reporting unit. Metric units (meters) may be used if "
            "specified in the project documentation and agreed upon by all parties. Surveyors must clearly state the units in all deliverables. "
            "Omission or confusion regarding units can result in significant errors."
        ),
        key_factors=[
            "Default reporting units", "Unit specification", "Legal requirements"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "Texas General Land Office"
        ],
        burden_holder="Surveyor reporting coordinates",
        adversary_position="Omission or confusion of units",
        counter_arguments=[
            "Some software defaults to meters",
            "Federal projects may require metric units"
        ],
        resolution_strategy="Require explicit unit specification in all deliverables.",
        entity_scope="Surveyors, engineers, regulatory agencies",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Datum Epoch Specification for High-Precision Surveys",
        keywords=[
            "datum epoch", "high-precision survey", "Texas", "NAD83(2011)", "epoch date"
        ],
        conclusion_template="High-precision surveys in Texas must specify the datum epoch date for all coordinate data.",
        reasoning_framework=(
            "The datum epoch date reflects the reference time for a set of coordinates, accounting for tectonic motion and realization updates. "
            "For high-precision surveys in Texas, the epoch date (e.g., 2010.00 for NAD83(2011)) must be specified in all deliverables. "
            "Omission of the epoch can result in centimeter-level errors, especially in dynamic regions."
        ),
        key_factors=[
            "Epoch date specification", "High-precision requirements", "Documentation"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor performing high-precision survey",
        adversary_position="Omission of epoch date",
        counter_arguments=[
            "Some projects may not require epoch specification",
            "Legacy data may lack epoch information"
        ],
        resolution_strategy="Require epoch specification for all high-precision surveys.",
        entity_scope="Surveyors, engineers, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NGS NAD83(2011) Guidelines"
    ),
    DoctrineBlock(
        topic="Coordinate System Specification in Texas Engineering Plans",
        keywords=[
            "coordinate system", "engineering plans", "Texas", "state plane", "documentation"
        ],
        conclusion_template="All engineering plans in Texas must specify the coordinate system, zone, datum, and units used.",
        reasoning_framework=(
            "Engineering plans in Texas must include explicit specification of the coordinate system, zone, datum, and units used for all spatial data. "
            "This requirement ensures consistency and prevents errors during construction and regulatory review. Omission of this information can "
            "result in costly mistakes and legal disputes."
        ),
        key_factors=[
            "Coordinate system specification", "Documentation", "Legal and engineering standards"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "Texas General Land Office"
        ],
        burden_holder="Engineer or surveyor preparing plans",
        adversary_position="Omission of coordinate system information",
        counter_arguments=[
            "Some projects may use local systems for convenience",
            "Legacy plans may lack this information"
        ],
        resolution_strategy="Require full specification in all engineering plans.",
        entity_scope="Engineers, surveyors, contractors",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Acceptance of WGS84 Coordinates for Mapping in Texas",
        keywords=[
            "WGS84", "mapping", "Texas", "coordinate system", "survey"
        ],
        conclusion_template="WGS84 coordinates may be used for mapping and visualization in Texas, but not for legal or regulatory submissions.",
        reasoning_framework=(
            "WGS84 is the global standard for GPS and mapping. In Texas, WGS84 coordinates are acceptable for mapping, visualization, and non-legal "
            "applications. For legal or regulatory submissions, coordinates must be transformed to the official state plane or UTM system and datum. "
            "This ensures consistency with state standards and legal defensibility."
        ),
        key_factors=[
            "Mapping vs. legal use", "Transformation requirements", "Documentation"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "National Geodetic Survey"
        ],
        burden_holder="Surveyor or GIS professional submitting data",
        adversary_position="Submission of WGS84 for legal purposes",
        counter_arguments=[
            "Some agencies may accept WGS84 for internal use",
            "Transformation may introduce small errors"
        ],
        resolution_strategy="Restrict WGS84 to mapping; require transformation for legal submissions.",
        entity_scope="Surveyors, GIS professionals, regulatory agencies",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Use of CORS Stations in Texas Surveying",
        keywords=[
            "CORS", "Continuously Operating Reference Stations", "Texas", "survey", "NAD83(2011)"
        ],
        conclusion_template="CORS stations are the preferred reference for high-precision GPS surveys in Texas; surveyors must document station IDs and coordinates.",
        reasoning_framework=(
            "Continuously Operating Reference Stations (CORS) provide high-precision, real-time reference data for GPS surveys. In Texas, "
            "surveyors are encouraged to use CORS stations for establishing control and must document the station IDs, coordinates, and datum realization. "
            "This ensures traceability and consistency with the National Spatial Reference System."
        ),
        key_factors=[
            "Use of CORS", "Documentation of reference stations", "High-precision requirements"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor performing GPS survey",
        adversary_position="Use of unverified or undocumented reference stations",
        counter_arguments=[
            "Some areas may lack nearby CORS stations",
            "Legacy surveys may use local control"
        ],
        resolution_strategy="Require documentation and, where possible, use of CORS stations.",
        entity_scope="Surveyors, engineers, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NGS CORS Guidelines"
    ),
    DoctrineBlock(
        topic="Datum Shifts and Legal Implications in Texas",
        keywords=[
            "datum shift", "legal implications", "Texas", "survey", "NAD83", "NAD27"
        ],
        conclusion_template="Surveyors must account for datum shifts and document all transformations to avoid legal disputes in Texas.",
        reasoning_framework=(
            "Datum shifts between NAD27, NAD83, and other datums can result in coordinate differences of tens to hundreds of meters. "
            "In Texas, surveyors must document all datum transformations and account for shifts in legal descriptions. Failure to do so "
            "can result in property boundary disputes and legal liability."
        ),
        key_factors=[
            "Datum shift magnitude", "Transformation documentation", "Legal defensibility"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "National Geodetic Survey"
        ],
        burden_holder="Surveyor preparing legal descriptions",
        adversary_position="Omission of datum shift information",
        counter_arguments=[
            "Some projects may not require high precision",
            "Legacy data may lack transformation documentation"
        ],
        resolution_strategy="Require full documentation of all datum shifts and transformations.",
        entity_scope="Surveyors, attorneys, regulatory agencies",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Transformation of Heights between Ellipsoid and Orthometric in Texas",
        keywords=[
            "height transformation", "ellipsoid", "orthometric", "geoid", "Texas", "survey"
        ],
        conclusion_template="Surveyors must use the official NGS geoid model (GEOID18) for all height transformations between ellipsoid and orthometric heights in Texas.",
        reasoning_framework=(
            "Transformation between GPS-derived ellipsoid heights and orthometric heights (NAVD88) requires the use of the official NGS geoid model. "
            "In Texas, GEOID18 is the current standard. Surveyors must document the model version and transformation method in all deliverables. "
            "Use of outdated or undocumented models can result in significant elevation errors."
        ),
        key_factors=[
            "Use of official geoid model", "Documentation", "Elevation accuracy"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor performing height transformation",
        adversary_position="Use of outdated or undocumented geoid models",
        counter_arguments=[
            "Legacy data may use older models",
            "Some projects may not require high-precision elevations"
        ],
        resolution_strategy="Require GEOID18 for all new height transformations.",
        entity_scope="Surveyors, engineers, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NGS GEOID18 Documentation"
    ),
    DoctrineBlock(
        topic="Projection Distortion Awareness in Texas State Plane Zones",
        keywords=[
            "projection distortion", "state plane", "Texas", "Lambert Conformal Conic", "scale factor"
        ],
        conclusion_template="Surveyors must account for projection distortion and document scale factors in Texas State Plane zones.",
        reasoning_framework=(
            "Lambert Conformal Conic projection introduces scale distortion that varies with distance from the central meridian and standard parallels. "
            "Surveyors in Texas must account for this distortion, especially for large projects, and document the scale factors used. "
            "Failure to do so can result in construction errors and legal disputes."
        ),
        key_factors=[
            "Projection distortion", "Scale factor documentation", "Project size"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "National Geodetic Survey"
        ],
        burden_holder="Surveyor performing mapping or construction layout",
        adversary_position="Omission of distortion or scale factor information",
        counter_arguments=[
            "Small projects may have negligible distortion",
            "Some software applies scale factors automatically"
        ],
        resolution_strategy="Require documentation of all scale factors and distortion corrections.",
        entity_scope="Surveyors, engineers, contractors",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Use of State Plane Coordinates in Texas GIS Applications",
        keywords=[
            "state plane coordinates", "GIS", "Texas", "mapping", "projection"
        ],
        conclusion_template="State Plane Coordinates are the preferred system for Texas GIS applications requiring high accuracy and legal defensibility.",
        reasoning_framework=(
            "For GIS applications in Texas requiring high accuracy and legal defensibility, the State Plane Coordinate System is preferred. "
            "This system aligns with state standards and ensures interoperability with regulatory and engineering data. "
            "Other systems (e.g., UTM, WGS84) may be used for mapping, but State Plane is required for legal and regulatory purposes."
        ),
        key_factors=[
            "Accuracy requirements", "Legal defensibility", "System interoperability"
        ],
        primary_authority=[
            "Texas General Land Office", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="GIS professional or agency",
        adversary_position="Use of alternate systems for high-accuracy or legal applications",
        counter_arguments=[
            "UTM and WGS84 are widely used for mapping",
            "Some projects may not require legal defensibility"
        ],
        resolution_strategy="Require State Plane for all high-accuracy and legal GIS applications.",
        entity_scope="GIS professionals, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Texas General Land Office Standards"
    ),
    DoctrineBlock(
        topic="Coordinate System Change Notification in Texas Projects",
        keywords=[
            "coordinate system change", "notification", "Texas", "survey", "engineering"
        ],
        conclusion_template="Any change in coordinate system during a Texas project must be documented and communicated to all stakeholders.",
        reasoning_framework=(
            "Changing the coordinate system during the course of a project can introduce significant errors and confusion. In Texas, any such change "
            "must be documented, including the reason for the change, transformation methods, and affected data. All stakeholders must be notified. "
            "Failure to do so can result in project delays, errors, and legal disputes."
        ),
        key_factors=[
            "Change documentation", "Stakeholder notification", "Transformation methods"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "Texas General Land Office"
        ],
        burden_holder="Project manager or lead surveyor",
        adversary_position="Unannounced or undocumented system changes",
        counter_arguments=[
            "Some changes may be minor or internal",
            "Legacy projects may lack documentation"
        ],
        resolution_strategy="Require full documentation and notification for all system changes.",
        entity_scope="Surveyors, engineers, project managers",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Use of National Spatial Reference System (NSRS) in Texas",
        keywords=[
            "NSRS", "National Spatial Reference System", "Texas", "survey", "datum"
        ],
        conclusion_template="All official surveys in Texas must reference the National Spatial Reference System (NSRS) as maintained by the NGS.",
        reasoning_framework=(
            "The National Spatial Reference System (NSRS) is the official geodetic reference for the United States, maintained by the National Geodetic Survey. "
            "In Texas, all official surveys must reference the NSRS, specifying the datum, realization, and epoch used. This ensures consistency and legal defensibility."
        ),
        key_factors=[
            "Reference to NSRS", "Datum and realization specification", "Legal requirements"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor performing official survey",
        adversary_position="Use of non-NSRS references",
        counter_arguments=[
            "Some projects may use local references for convenience",
            "Legacy data may not reference NSRS"
        ],
        resolution_strategy="Require NSRS reference for all official surveys.",
        entity_scope="Surveyors, regulatory agencies",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="NGS NSRS Guidelines"
    ),
    DoctrineBlock(
        topic="EPSG Code Updates and Deprecation in Texas",
        keywords=[
            "EPSG code", "update", "deprecation", "Texas", "coordinate system"
        ],
        conclusion_template="Surveyors must monitor EPSG code updates and use current codes for all new Texas coordinate data submissions.",
        reasoning_framework=(
            "EPSG codes are periodically updated and deprecated as coordinate systems evolve. Surveyors in Texas must monitor the EPSG registry "
            "and use current codes for all new data submissions. Use of deprecated codes may result in data rejection or misinterpretation."
        ),
        key_factors=[
            "EPSG code currency", "Registry monitoring", "Data interoperability"
        ],
        primary_authority=[
            "EPSG Registry", "Texas General Land Office"
        ],
        burden_holder="Surveyor or data provider",
        adversary_position="Use of deprecated EPSG codes",
        counter_arguments=[
            "Legacy data may use older codes",
            "Some software may not support new codes"
        ],
        resolution_strategy="Require current EPSG codes for all new submissions.",
        entity_scope="Surveyors, GIS professionals, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="EPSG Registry"
    ),
    DoctrineBlock(
        topic="Datum Transformation Residuals and Reporting in Texas",
        keywords=[
            "datum transformation", "residuals", "reporting", "Texas", "survey"
        ],
        conclusion_template="All datum transformations in Texas must include reporting of residuals and estimated positional accuracy.",
        reasoning_framework=(
            "Datum transformations introduce residual errors due to interpolation and model limitations. In Texas, surveyors must report the residuals "
            "and estimated positional accuracy for all transformations. This information must be included in metadata and deliverables. "
            "Failure to report residuals can result in data rejection or legal disputes."
        ),
        key_factors=[
            "Residual reporting", "Estimated accuracy", "Documentation"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "National Geodetic Survey"
        ],
        burden_holder="Surveyor performing transformation",
        adversary_position="Omission of residuals or accuracy estimates",
        counter_arguments=[
            "Some transformations may have negligible residuals",
            "Legacy data may lack this information"
        ],
        resolution_strategy="Require residual and accuracy reporting for all transformations.",
        entity_scope="Surveyors, regulatory agencies",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Coordinate System Adoption for New Texas Projects",
        keywords=[
            "coordinate system", "adoption", "new projects", "Texas", "state plane"
        ],
        conclusion_template="All new projects in Texas must adopt the current official State Plane Coordinate System and datum.",
        reasoning_framework=(
            "For consistency and interoperability, all new projects in Texas must adopt the current official State Plane Coordinate System and datum "
            "(e.g., NAD83(2011)). This ensures alignment with state standards and facilitates data sharing. Use of outdated or alternate systems "
            "is discouraged except for legacy data integration."
        ),
        key_factors=[
            "Adoption of current standards", "Data interoperability", "Project initiation"
        ],
        primary_authority=[
            "Texas General Land Office", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Project manager or lead surveyor",
        adversary_position="Use of outdated or alternate systems",
        counter_arguments=[
            "Some projects may require alternate systems for compatibility",
            "Legacy data integration may require exceptions"
        ],
        resolution_strategy="Require adoption of current standards for all new projects.",
        entity_scope="Surveyors, engineers, project managers",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Texas General Land Office Standards"
    ),
    DoctrineBlock(
        topic="Legal Precedence of Coordinate Descriptions in Texas",
        keywords=[
            "legal precedence", "coordinate description", "Texas", "survey", "property boundary"
        ],
        conclusion_template="Coordinate-based property descriptions have legal precedence in Texas if referenced to the official system and properly documented.",
        reasoning_framework=(
            "Texas law recognizes coordinate-based property descriptions as legally binding if they reference the official State Plane Coordinate System, "
            "specify the datum, and are properly documented. Such descriptions take precedence over ambiguous or conflicting metes and bounds descriptions. "
            "Surveyors must ensure all coordinate-based descriptions meet statutory requirements."
        ),
        key_factors=[
            "Legal recognition", "Official system reference", "Documentation"
        ],
        primary_authority=[
            "Texas Administrative Code", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor preparing legal description",
        adversary_position="Use of ambiguous or unofficial coordinate systems",
        counter_arguments=[
            "Some counties may have local requirements",
            "Legacy descriptions may lack full documentation"
        ],
        resolution_strategy="Require reference to official system and full documentation.",
        entity_scope="Surveyors, attorneys, title companies",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Texas Administrative Code, Title 1, Part 4, Chapter 3"
    ),
    DoctrineBlock(
        topic="Datum and Projection Specification in Texas Land Title Surveys",
        keywords=[
            "datum", "projection", "land title survey", "Texas", "state plane"
        ],
        conclusion_template="All Texas land title surveys must specify the datum and projection used for coordinate data.",
        reasoning_framework=(
            "Land title surveys in Texas must include explicit specification of the datum and projection used for all coordinate data. "
            "This requirement ensures clarity in property descriptions and prevents legal disputes. Omission of this information can result in "
            "rejection of the survey by title companies or regulatory agencies."
        ),
        key_factors=[
            "Datum and projection specification", "Legal requirements", "Survey acceptance"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "Texas Administrative Code"
        ],
        burden_holder="Surveyor preparing land title survey",
        adversary_position="Omission of datum or projection information",
        counter_arguments=[
            "Some legacy surveys may lack this information",
            "Local practices may differ"
        ],
        resolution_strategy="Require full specification in all land title surveys.",
        entity_scope="Surveyors, title companies, attorneys",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Use of Survey-Grade GNSS Equipment in Texas",
        keywords=[
            "GNSS", "survey-grade", "equipment", "Texas", "accuracy"
        ],
        conclusion_template="Survey-grade GNSS equipment is required for high-precision surveys in Texas; equipment specifications must be documented.",
        reasoning_framework=(
            "High-precision surveys in Texas require the use of survey-grade GNSS equipment meeting or exceeding accuracy standards set by the Texas Board "
            "of Professional Land Surveying. Surveyors must document equipment make, model, and specifications in all deliverables. Use of consumer-grade "
            "equipment is not acceptable for legal or regulatory submissions."
        ),
        key_factors=[
            "Equipment specifications", "Accuracy standards", "Documentation"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor performing high-precision survey",
        adversary_position="Use of consumer-grade or undocumented equipment",
        counter_arguments=[
            "Some projects may not require high precision",
            "Legacy surveys may lack equipment documentation"
        ],
        resolution_strategy="Require survey-grade equipment and documentation for all high-precision surveys.",
        entity_scope="Surveyors, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Coordinate System Consistency in Multi-Agency Texas Projects",
        keywords=[
            "coordinate system", "consistency", "multi-agency", "Texas", "interoperability"
        ],
        conclusion_template="All agencies participating in Texas projects must agree on and document the coordinate system, datum, and projection used.",
        reasoning_framework=(
            "Multi-agency projects in Texas require agreement and documentation of the coordinate system, datum, and projection used. "
            "This ensures data interoperability and prevents errors arising from inconsistent references. The lead agency is responsible for "
            "coordinating and documenting this agreement."
        ),
        key_factors=[
            "Inter-agency agreement", "Documentation", "Data interoperability"
        ],
        primary_authority=[
            "Texas General Land Office", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Lead agency or project manager",
        adversary_position="Use of inconsistent or undocumented systems",
        counter_arguments=[
            "Some agencies may have legacy requirements",
            "Projects may span multiple coordinate systems"
        ],
        resolution_strategy="Require agreement and documentation for all multi-agency projects.",
        entity_scope="Agencies, surveyors, engineers",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas General Land Office Standards"
    ),
    DoctrineBlock(
        topic="Use of State Plane vs. UTM for Texas Regulatory Submissions",
        keywords=[
            "state plane", "UTM", "regulatory submission", "Texas", "coordinate system"
        ],
        conclusion_template="State Plane Coordinates are required for all Texas regulatory submissions; UTM may be used for mapping only.",
        reasoning_framework=(
            "Texas regulatory agencies require the use of State Plane Coordinates for all official submissions. UTM may be used for mapping and visualization, "
            "but not for legal or regulatory purposes. This ensures consistency with state standards and legal defensibility."
        ),
        key_factors=[
            "Regulatory requirements", "Legal defensibility", "System interoperability"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "Texas General Land Office"
        ],
        burden_holder="Surveyor or engineer submitting data",
        adversary_position="Submission of UTM coordinates for regulatory purposes",
        counter_arguments=[
            "UTM is widely used for mapping",
            "Some federal projects may require UTM"
        ],
        resolution_strategy="Restrict UTM to mapping; require State Plane for regulatory submissions.",
        entity_scope="Surveyors, engineers, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Transformation of Legacy Texas Data for Modern Use",
        keywords=[
            "legacy data", "transformation", "modern use", "Texas", "NAD27", "NAD83"
        ],
        conclusion_template="Legacy Texas data must be transformed to current standards (NAD83, NAVD88) for integration with modern datasets.",
        reasoning_framework=(
            "Integration of legacy data (NAD27, NGVD29) with modern datasets requires transformation to current standards (NAD83, NAVD88) using NGS tools. "
            "Surveyors must document all transformation parameters, methods, and residuals. This ensures data consistency and legal defensibility."
        ),
        key_factors=[
            "Transformation to current standards", "Documentation", "Data integration"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "National Geodetic Survey"
        ],
        burden_holder="Surveyor or data integrator",
        adversary_position="Use of legacy data without transformation",
        counter_arguments=[
            "Some legacy data may be used for reference only",
            "Transformation may introduce small errors"
        ],
        resolution_strategy="Require transformation and documentation for all legacy data used in modern projects.",
        entity_scope="Surveyors, engineers, GIS professionals",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Documentation of Coordinate System Parameters in Texas",
        keywords=[
            "documentation", "coordinate system parameters", "Texas", "projection", "datum"
        ],
        conclusion_template="All Texas survey and GIS deliverables must include documentation of coordinate system parameters, including datum, projection, zone, and units.",
        reasoning_framework=(
            "Documentation of coordinate system parameters is required for all survey and GIS deliverables in Texas. This includes datum, projection, zone, "
            "units, and any transformation methods used. Complete documentation ensures data interoperability, legal defensibility, and prevents errors."
        ),
        key_factors=[
            "Parameter documentation", "Legal requirements", "Data interoperability"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "Texas General Land Office"
        ],
        burden_holder="Surveyor or GIS professional submitting data",
        adversary_position="Omission of parameter documentation",
        counter_arguments=[
            "Some legacy data may lack full documentation",
            "Projects may use default parameters"
        ],
        resolution_strategy="Require full parameter documentation for all deliverables.",
        entity_scope="Surveyors, GIS professionals, regulatory agencies",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Use of Official State Plane Zone Boundaries in Texas",
        keywords=[
            "state plane zone", "official boundaries", "Texas", "coordinate system", "mapping"
        ],
        conclusion_template="Surveyors must use official State Plane zone boundaries as defined by the Texas General Land Office.",
        reasoning_framework=(
            "The Texas General Land Office defines official boundaries for State Plane zones. Surveyors must use these boundaries when specifying coordinate "
            "systems for projects. Use of unofficial or approximate boundaries can result in errors and regulatory rejection."
        ),
        key_factors=[
            "Official zone boundaries", "Legal requirements", "Project location"
        ],
        primary_authority=[
            "Texas General Land Office", "Texas Administrative Code"
        ],
        burden_holder="Surveyor or engineer specifying coordinate system",
        adversary_position="Use of unofficial or approximate boundaries",
        counter_arguments=[
            "Some projects may span multiple zones",
            "Legacy data may use approximate boundaries"
        ],
        resolution_strategy="Require use of official boundaries for all projects.",
        entity_scope="Surveyors, engineers, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Texas General Land Office Standards"
    ),
    DoctrineBlock(
        topic="Datum and Projection Specification in Texas GIS Metadata",
        keywords=[
            "datum", "projection", "GIS metadata", "Texas", "coordinate system"
        ],
        conclusion_template="All Texas GIS metadata must specify the datum and projection used for spatial data.",
        reasoning_framework=(
            "GIS metadata in Texas must include explicit specification of the datum and projection used for all spatial data. This ensures correct "
            "interpretation, interoperability, and legal defensibility. Omission of this information can result in data rejection."
        ),
        key_factors=[
            "Datum and projection specification", "Metadata standards", "Legal requirements"
        ],
        primary_authority=[
            "Texas General Land Office", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="GIS professional preparing metadata",
        adversary_position="Omission of datum or projection information",
        counter_arguments=[
            "Some legacy data may lack this information",
            "Projects may use default parameters"
        ],
        resolution_strategy="Require full specification in all GIS metadata.",
        entity_scope="GIS professionals, regulatory agencies",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Texas General Land Office Standards"
    ),
    DoctrineBlock(
        topic="Use of Official NGS Datasheets for Texas Control Points",
        keywords=[
            "NGS datasheet", "control point", "Texas", "survey", "coordinate system"
        ],
        conclusion_template="Surveyors must reference official NGS datasheets for all control points used in Texas projects.",
        reasoning_framework=(
            "Official NGS datasheets provide authoritative information on control point coordinates, datum, and projection. Surveyors in Texas must "
            "reference these datasheets for all control points used in projects. This ensures accuracy, traceability, and legal defensibility."
        ),
        key_factors=[
            "Use of official datasheets", "Control point accuracy", "Documentation"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor establishing control",
        adversary_position="Use of unofficial or undocumented control points",
        counter_arguments=[
            "Some projects may use local control for convenience",
            "Legacy surveys may lack datasheet references"
        ],
        resolution_strategy="Require reference to NGS datasheets for all control points.",
        entity_scope="Surveyors, engineers, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="NGS Datasheet Guidelines"
    ),
    DoctrineBlock(
        topic="Datum Transformation Software Validation in Texas",
        keywords=[
            "datum transformation", "software validation", "Texas", "survey", "NGS"
        ],
        conclusion_template="All datum transformation software used in Texas must be validated against NGS-published results.",
        reasoning_framework=(
            "Datum transformation software must be validated against official NGS-published results to ensure accuracy and legal defensibility. "
            "Surveyors in Texas must document the software used, version, and validation results. Use of unvalidated software can result in data rejection."
        ),
        key_factors=[
            "Software validation", "Documentation", "Legal requirements"
        ],
        primary_authority=[
            "National Geodetic Survey", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor performing transformation",
        adversary_position="Use of unvalidated or undocumented software",
        counter_arguments=[
            "Some software may claim NGS compliance",
            "Legacy data may lack validation documentation"
        ],
        resolution_strategy="Require validation and documentation for all transformation software.",
        entity_scope="Surveyors, regulatory agencies",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="NGS Transformation Guidelines"
    ),
    DoctrineBlock(
        topic="Use of State Plane Coordinates for Texas Transportation Projects",
        keywords=[
            "state plane coordinates", "transportation projects", "Texas", "TxDOT", "survey"
        ],
        conclusion_template="State Plane Coordinates are required for all Texas Department of Transportation (TxDOT) projects.",
        reasoning_framework=(
            "The Texas Department of Transportation (TxDOT) requires the use of State Plane Coordinates for all survey, design, and construction projects. "
            "This ensures consistency, interoperability, and legal defensibility. Surveyors must specify the zone, datum, and units used."
        ),
        key_factors=[
            "TxDOT requirements", "System specification", "Project consistency"
        ],
        primary_authority=[
            "Texas Department of Transportation", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor or engineer working on TxDOT projects",
        adversary_position="Use of alternate coordinate systems",
        counter_arguments=[
            "Some federal projects may require UTM",
            "Legacy projects may use local systems"
        ],
        resolution_strategy="Require State Plane Coordinates for all TxDOT projects.",
        entity_scope="Surveyors, engineers, TxDOT",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="TxDOT Survey Manual"
    ),
    DoctrineBlock(
        topic="Datum and Projection Specification for Texas Utility Mapping",
        keywords=[
            "datum", "projection", "utility mapping", "Texas", "state plane"
        ],
        conclusion_template="All utility mapping in Texas must specify the datum and projection used for spatial data.",
        reasoning_framework=(
            "Utility mapping in Texas requires explicit specification of the datum and projection used for all spatial data. This ensures accurate "
            "location of utilities and prevents errors during construction or maintenance. Omission of this information can result in costly mistakes."
        ),
        key_factors=[
            "Datum and projection specification", "Utility location accuracy", "Documentation"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying", "Texas General Land Office"
        ],
        burden_holder="Utility engineer or surveyor",
        adversary_position="Omission of datum or projection information",
        counter_arguments=[
            "Some legacy maps may lack this information",
            "Projects may use default parameters"
        ],
        resolution_strategy="Require full specification in all utility mapping deliverables.",
        entity_scope="Utility engineers, surveyors, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Texas Board of Professional Land Surveying Rules"
    ),
    DoctrineBlock(
        topic="Use of Official State Plane Parameters in Texas Survey Software",
        keywords=[
            "state plane parameters", "survey software", "Texas", "projection", "datum"
        ],
        conclusion_template="Survey software used in Texas must implement official State Plane parameters as published by the Texas General Land Office.",
        reasoning_framework=(
            "Survey software used in Texas must implement the official State Plane parameters (datum, projection, zone, units) as published by the Texas General Land Office. "
            "Surveyors must verify software compliance and document the parameters used in all deliverables. Use of unofficial or default parameters can result in errors."
        ),
        key_factors=[
            "Software compliance", "Parameter verification", "Documentation"
        ],
        primary_authority=[
            "Texas General Land Office", "Texas Board of Professional Land Surveying"
        ],
        burden_holder="Surveyor using survey software",
        adversary_position="Use of unofficial or default parameters",
        counter_arguments=[
            "Some software may not be updated with latest parameters",
            "Legacy projects may use older parameters"
        ],
        resolution_strategy="Require verification and documentation of software parameters.",
        entity_scope="Surveyors, engineers, regulatory agencies",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="Texas General Land Office Standards"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]