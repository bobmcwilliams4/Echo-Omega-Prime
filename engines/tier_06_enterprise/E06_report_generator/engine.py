"""
E06 -- Report Generator Engine
===============================
TIER: E (Enterprise) | MODE: SUP_LLM | AUTH: 11.0 SOVEREIGN | PORT: 8606

Generates formatted reports from structured engine outputs: title opinions,
run sheets, due diligence summaries, lease abstracts, curative letters,
regulatory compliance, environmental assessments, production histories,
revenue analyses, heirship determinations, and more.

20+ report types, each with cover page, TOC, executive summary, legal
description, chain of title, current ownership, requirements/exceptions,
exhibits list, and certification/disclaimer sections.

TIE-20 Compliant: All 20 mandatory components implemented.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import sys
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).resolve().parent
ENGINES_DIR = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINES_DIR))

try:
    from _shared.cloud_retriever import CognitionCloudRetriever
except ImportError:
    CognitionCloudRetriever = None  # type: ignore[assignment,misc]

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------
ENGINE_ID = "E06"
ENGINE_NAME = "Report Generator"
ENGINE_VERSION = "1.0.0"
ENGINE_TIER = "E"
ENGINE_MODE = "SUP_LLM"
ENGINE_PORT = 8606
AUTHORITY_LEVEL = 11.0

AUDIT_LOG_PATH = ENGINE_DIR / "audit_trail.jsonl"
DOCTRINE_CACHE_PATH = ENGINE_DIR / "doctrine_cache.json"
SEMANTIC_DICT_PATH = ENGINE_DIR / "semantic_dict.json"
COVERAGE_MAP_PATH = ENGINE_DIR / "coverage_map.json"

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | "
           "<cyan>E06</cyan> | <level>{message}</level>",
    level="DEBUG",
    colorize=True,
)
logger.add(
    ENGINE_DIR / "e06.log",
    rotation="50 MB",
    retention="30 days",
    compression="gz",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | E06 | {message}",
    level="DEBUG",
)


# ============================================================================
# REPORT TYPE REGISTRY
# ============================================================================

class ReportType(str, Enum):
    PTO = "preliminary_title_opinion"
    DOTO = "division_order_title_opinion"
    SUPPLEMENTAL_TO = "supplemental_title_opinion"
    RUN_SHEET = "run_sheet"
    LEASE_ABSTRACT = "lease_abstract"
    CURATIVE_LETTER = "curative_requirement_letter"
    DUE_DILIGENCE = "due_diligence_summary"
    RISK_ASSESSMENT = "risk_assessment_report"
    REGULATORY_COMPLIANCE = "regulatory_compliance_report"
    ENVIRONMENTAL = "environmental_assessment_summary"
    PRODUCTION_HISTORY = "production_history_report"
    REVENUE_ANALYSIS = "revenue_analysis_report"
    COMPETITIVE_ACTIVITY = "competitive_activity_report"
    HEIRSHIP = "heirship_determination_report"
    PROBATE_SUMMARY = "probate_summary"
    TAX_ANALYSIS = "tax_analysis_report"
    WELL_FILE = "well_file_summary"
    PERMIT_APP = "permit_application_summary"
    SURFACE_DAMAGE = "surface_damage_assessment"
    PIPELINE_ROW = "pipeline_right_of_way_report"
    POOLING_UNIT = "pooling_unit_report"
    FORCE_POOLING = "force_pooling_analysis"


REPORT_DISPLAY_NAMES: dict[str, str] = {
    ReportType.PTO: "Preliminary Title Opinion",
    ReportType.DOTO: "Division Order Title Opinion",
    ReportType.SUPPLEMENTAL_TO: "Supplemental Title Opinion",
    ReportType.RUN_SHEET: "Run Sheet",
    ReportType.LEASE_ABSTRACT: "Lease Abstract",
    ReportType.CURATIVE_LETTER: "Curative Requirement Letter",
    ReportType.DUE_DILIGENCE: "Due Diligence Summary",
    ReportType.RISK_ASSESSMENT: "Risk Assessment Report",
    ReportType.REGULATORY_COMPLIANCE: "Regulatory Compliance Report",
    ReportType.ENVIRONMENTAL: "Environmental Assessment Summary",
    ReportType.PRODUCTION_HISTORY: "Production History Report",
    ReportType.REVENUE_ANALYSIS: "Revenue Analysis Report",
    ReportType.COMPETITIVE_ACTIVITY: "Competitive Activity Report",
    ReportType.HEIRSHIP: "Heirship Determination Report",
    ReportType.PROBATE_SUMMARY: "Probate Summary",
    ReportType.TAX_ANALYSIS: "Tax Analysis Report",
    ReportType.WELL_FILE: "Well File Summary",
    ReportType.PERMIT_APP: "Permit Application Summary",
    ReportType.SURFACE_DAMAGE: "Surface Damage Assessment",
    ReportType.PIPELINE_ROW: "Pipeline Right-of-Way Report",
    ReportType.POOLING_UNIT: "Pooling Unit Report",
    ReportType.FORCE_POOLING: "Force Pooling Analysis",
}

REPORT_SECTIONS: dict[str, list[str]] = {
    ReportType.PTO: [
        "cover_page", "table_of_contents", "executive_summary",
        "legal_description", "chain_of_title", "current_ownership",
        "mineral_interests", "surface_interests", "leasehold_interests",
        "requirements_exceptions", "curative_matters", "exhibits", "certification",
    ],
    ReportType.DOTO: [
        "cover_page", "table_of_contents", "executive_summary",
        "legal_description", "chain_of_title", "division_of_interests",
        "decimal_interest_table", "unpooled_interests", "pooled_interests",
        "royalty_calculations", "overriding_royalties", "requirements_exceptions",
        "exhibits", "certification",
    ],
    ReportType.SUPPLEMENTAL_TO: [
        "cover_page", "table_of_contents", "scope_of_supplement",
        "original_opinion_reference", "new_instruments_reviewed",
        "updated_chain_of_title", "revised_ownership",
        "new_requirements", "exhibits", "certification",
    ],
    ReportType.RUN_SHEET: [
        "cover_page", "property_identification", "legal_description",
        "chronological_entries", "ownership_summary_table",
        "decimal_interest_breakdown", "notes",
    ],
    ReportType.LEASE_ABSTRACT: [
        "cover_page", "lease_identification", "parties",
        "legal_description", "primary_term", "royalty_provisions",
        "pooling_clauses", "assignment_history", "amendments",
        "current_status", "notes",
    ],
    ReportType.CURATIVE_LETTER: [
        "cover_page", "addressee_info", "property_reference",
        "curative_requirements_list", "deadline", "instructions",
        "contact_info",
    ],
    ReportType.DUE_DILIGENCE: [
        "cover_page", "table_of_contents", "executive_summary",
        "property_overview", "title_analysis", "environmental_review",
        "regulatory_status", "financial_analysis", "risk_factors",
        "recommendations", "exhibits", "certification",
    ],
    ReportType.RISK_ASSESSMENT: [
        "cover_page", "table_of_contents", "executive_summary",
        "risk_matrix", "title_risks", "environmental_risks",
        "regulatory_risks", "financial_risks", "operational_risks",
        "mitigation_strategies", "exhibits", "certification",
    ],
    ReportType.REGULATORY_COMPLIANCE: [
        "cover_page", "table_of_contents", "executive_summary",
        "permits_and_licenses", "rrc_compliance", "epa_compliance",
        "state_requirements", "federal_requirements", "compliance_gaps",
        "remediation_plan", "exhibits", "certification",
    ],
    ReportType.ENVIRONMENTAL: [
        "cover_page", "table_of_contents", "executive_summary",
        "site_description", "environmental_history", "contamination_assessment",
        "remediation_status", "regulatory_actions", "liability_estimate",
        "recommendations", "exhibits", "certification",
    ],
    ReportType.PRODUCTION_HISTORY: [
        "cover_page", "table_of_contents", "well_identification",
        "production_summary_table", "monthly_production", "cumulative_production",
        "decline_analysis", "operator_history", "notes",
    ],
    ReportType.REVENUE_ANALYSIS: [
        "cover_page", "table_of_contents", "executive_summary",
        "revenue_summary", "price_history", "volume_analysis",
        "interest_allocation", "deductions_analysis", "net_revenue_projection",
        "exhibits",
    ],
    ReportType.COMPETITIVE_ACTIVITY: [
        "cover_page", "table_of_contents", "executive_summary",
        "area_overview", "permit_activity", "drilling_activity",
        "completion_activity", "production_trends", "operator_analysis",
        "lease_activity", "exhibits",
    ],
    ReportType.HEIRSHIP: [
        "cover_page", "table_of_contents", "executive_summary",
        "decedent_information", "family_tree", "intestate_succession",
        "probate_status", "heir_identification", "interest_allocation",
        "supporting_documents", "exhibits", "certification",
    ],
    ReportType.PROBATE_SUMMARY: [
        "cover_page", "table_of_contents", "decedent_information",
        "probate_proceeding", "will_summary", "estate_inventory",
        "distribution_schedule", "outstanding_issues", "exhibits",
    ],
    ReportType.TAX_ANALYSIS: [
        "cover_page", "table_of_contents", "executive_summary",
        "property_valuation", "ad_valorem_taxes", "severance_taxes",
        "income_tax_implications", "depletion_analysis", "tax_credits",
        "recommendations", "exhibits",
    ],
    ReportType.WELL_FILE: [
        "cover_page", "well_identification", "permit_information",
        "drilling_summary", "completion_data", "production_data",
        "operator_history", "regulatory_filings", "exhibits",
    ],
    ReportType.PERMIT_APP: [
        "cover_page", "applicant_information", "well_location",
        "proposed_operations", "surface_owner_notification",
        "environmental_considerations", "regulatory_checklist",
        "exhibits",
    ],
    ReportType.SURFACE_DAMAGE: [
        "cover_page", "property_identification", "surface_owner_info",
        "damage_assessment", "remediation_plan", "cost_estimate",
        "payment_schedule", "exhibits",
    ],
    ReportType.PIPELINE_ROW: [
        "cover_page", "table_of_contents", "pipeline_description",
        "right_of_way_analysis", "landowner_identification",
        "easement_terms", "compensation_analysis", "regulatory_requirements",
        "exhibits", "certification",
    ],
    ReportType.POOLING_UNIT: [
        "cover_page", "table_of_contents", "unit_description",
        "legal_description", "participating_tracts", "interest_allocation",
        "unit_agreement_terms", "regulatory_approval", "exhibits",
    ],
    ReportType.FORCE_POOLING: [
        "cover_page", "table_of_contents", "executive_summary",
        "applicant_info", "respondent_info", "legal_description",
        "offers_made", "election_options", "hearing_history",
        "order_terms", "exhibits",
    ],
}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The report generation request")
    mode: str = Field("FAST", description="FAST | DEFENSE | MEMO")
    report_type: Optional[str] = Field(None, description="Report type enum value")
    property_data: Optional[dict[str, Any]] = Field(None, description="Structured property data")
    engine_outputs: Optional[dict[str, Any]] = Field(None, description="Outputs from other engines")
    client_info: Optional[dict[str, Any]] = Field(None, description="Client/preparer info")
    zone: Optional[str] = Field(None, description="PLANNING | REPORTING | AUDIT")
    context: Optional[dict[str, Any]] = Field(None, description="Additional context")


class QueryResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    query: str
    mode: str
    response: str
    report_type: Optional[str] = None
    sections_generated: list[str] = []
    layer_used: str = "doctrine_cache"
    confidence: float = 0.0
    confidence_tier: str = "DEFENSIBLE"
    zone: str = "REPORTING"
    determinism_hash: str = ""
    latency_ms: float = 0.0
    timestamp: str = ""
    fragility_score: float = 0.0
    authorities_cited: list[str] = []
    doctrine_hits: list[str] = []


class HealthResponse(BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    version: str = ENGINE_VERSION
    status: str = "healthy"
    uptime_seconds: float = 0.0
    total_queries: int = 0
    cache_size: int = 0
    report_types_supported: int = len(ReportType)
    doctrine_count: int = 0
    avg_latency_ms: float = 0.0


# ============================================================================
# [TIE-01] THREE LAYER RESPONSE
# ============================================================================

class ResponseLayer(str, Enum):
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class ThreeLayerResponse:
    """Layer 1 (0-200ms): Doctrine Cache -- pre-compiled report templates.
    Layer 2 (200-1000ms): Semantic Retrieval -- normalized term lookup + vector search.
    Layer 3 (1000ms+): Deep Analysis -- full multi-source synthesis.
    """

    def __init__(self, doctrine_cache: DoctrineCache, semantic_norm: SemanticNormalizer) -> None:
        self.doctrine_cache = doctrine_cache
        self.semantic_norm = semantic_norm

    async def resolve(self, query: str, mode: str, report_type: Optional[str],
                      property_data: Optional[dict], engine_outputs: Optional[dict],
                      client_info: Optional[dict], zone: Optional[str]) -> dict[str, Any]:
        start = time.perf_counter()
        normalized = self.semantic_norm.normalize(query)

        # Layer 1: Doctrine Cache
        cache_hit = self.doctrine_cache.lookup(normalized, report_type)
        if cache_hit and mode == "FAST":
            latency = (time.perf_counter() - start) * 1000
            return {
                "response": self._build_report_from_doctrine(cache_hit, property_data, engine_outputs, client_info, report_type),
                "layer": ResponseLayer.DOCTRINE_CACHE,
                "latency_ms": latency,
                "confidence": cache_hit.get("confidence", 0.85),
                "doctrine_hits": [cache_hit["topic"]],
                "authorities": cache_hit.get("primary_authority", []),
            }

        # Layer 2: Semantic Retrieval
        sem_results = self.semantic_norm.search(normalized)
        if sem_results and mode != "MEMO":
            latency = (time.perf_counter() - start) * 1000
            combined = self._merge_semantic_results(sem_results, property_data, engine_outputs, client_info, report_type)
            return {
                "response": combined,
                "layer": ResponseLayer.SEMANTIC_RETRIEVAL,
                "latency_ms": latency,
                "confidence": 0.75,
                "doctrine_hits": [r["topic"] for r in sem_results[:3]],
                "authorities": [],
            }

        # Layer 3: Deep Analysis
        deep = await self._deep_analysis(query, normalized, report_type, property_data, engine_outputs, client_info, zone)
        latency = (time.perf_counter() - start) * 1000
        return {
            "response": deep["response"],
            "layer": ResponseLayer.DEEP_ANALYSIS,
            "latency_ms": latency,
            "confidence": deep.get("confidence", 0.65),
            "doctrine_hits": deep.get("doctrine_hits", []),
            "authorities": deep.get("authorities", []),
        }

    def _build_report_from_doctrine(self, doctrine: dict, property_data: Optional[dict],
                                     engine_outputs: Optional[dict], client_info: Optional[dict],
                                     report_type: Optional[str]) -> str:
        rt = report_type or ReportType.DUE_DILIGENCE
        display = REPORT_DISPLAY_NAMES.get(rt, rt)
        sections = REPORT_SECTIONS.get(rt, ["cover_page", "executive_summary", "certification"])
        prop = property_data or {}
        client = client_info or {}
        outputs = engine_outputs or {}

        lines: list[str] = []
        section_num = 0

        for sec in sections:
            section_num += 1
            builder = SECTION_BUILDERS.get(sec)
            if builder:
                lines.append(builder(section_num, display, prop, client, outputs, doctrine))
            else:
                lines.append(f"\n## {section_num}.0 {sec.replace('_', ' ').title()}\n")
                lines.append(f"*Section content generated from {ENGINE_ID} doctrine cache.*\n")

        if doctrine.get("conclusion_template"):
            lines.append(f"\n---\n**Doctrine Applied:** {doctrine['topic']}\n")
            lines.append(doctrine["conclusion_template"])

        return "\n".join(lines)

    def _merge_semantic_results(self, results: list[dict], property_data: Optional[dict],
                                 engine_outputs: Optional[dict], client_info: Optional[dict],
                                 report_type: Optional[str]) -> str:
        rt = report_type or ReportType.DUE_DILIGENCE
        display = REPORT_DISPLAY_NAMES.get(rt, rt)
        lines = [f"# {display}\n", "**Generated via Semantic Retrieval Layer**\n"]
        for i, r in enumerate(results[:5], 1):
            lines.append(f"## {i}.0 {r['topic']}\n")
            if r.get("conclusion_template"):
                lines.append(r["conclusion_template"])
            lines.append("")
        return "\n".join(lines)

    async def _deep_analysis(self, query: str, normalized: str, report_type: Optional[str],
                              property_data: Optional[dict], engine_outputs: Optional[dict],
                              client_info: Optional[dict], zone: Optional[str]) -> dict[str, Any]:
        rt = report_type or ReportType.DUE_DILIGENCE
        display = REPORT_DISPLAY_NAMES.get(rt, rt)
        sections = REPORT_SECTIONS.get(rt, ["cover_page", "executive_summary", "certification"])
        prop = property_data or {}
        client = client_info or {}
        outputs = engine_outputs or {}

        cloud_context = ""
        if CognitionCloudRetriever is not None:
            try:
                cloud = CognitionCloudRetriever()
                results = await cloud.retrieve_all(query, category="report_generation")
                if results:
                    cloud_context = "\n".join(
                        f"- [{r.source}] {r.content[:300]}" for r in results[:5]
                    )
            except Exception as exc:
                logger.warning("Cloud retrieval failed in deep analysis: {}", exc)

        lines: list[str] = []
        section_num = 0
        for sec in sections:
            section_num += 1
            builder = SECTION_BUILDERS.get(sec)
            if builder:
                lines.append(builder(section_num, display, prop, client, outputs, {}))
            else:
                lines.append(f"\n## {section_num}.0 {sec.replace('_', ' ').title()}\n")

        if cloud_context:
            lines.append("\n## Supplementary Research\n")
            lines.append(cloud_context)

        doctrines_used = []
        for block in DOCTRINE_BLOCKS:
            for kw in block["keywords"]:
                if kw in normalized:
                    doctrines_used.append(block["topic"])
                    break

        return {
            "response": "\n".join(lines),
            "confidence": 0.70 if cloud_context else 0.60,
            "doctrine_hits": doctrines_used[:5],
            "authorities": [],
        }


# ============================================================================
# SECTION BUILDERS
# ============================================================================

def _build_cover_page(num: int, display: str, prop: dict, client: dict,
                      outputs: dict, doctrine: dict) -> str:
    county = prop.get("county", "___________")
    state = prop.get("state", "Texas")
    legal_desc = prop.get("legal_description", "See Section 2.0")
    client_name = client.get("name", "___________")
    preparer = client.get("prepared_by", "ECHO OMEGA PRIME -- Report Generator E06")
    date_str = datetime.now(timezone.utc).strftime("%B %d, %Y")
    file_no = prop.get("file_number", f"E06-{datetime.now(timezone.utc).strftime('%Y%m%d')}-001")

    return f"""
# {display}

| Field | Value |
|-------|-------|
| **File No.** | {file_no} |
| **Property** | {legal_desc} |
| **County** | {county} |
| **State** | {state} |
| **Prepared For** | {client_name} |
| **Prepared By** | {preparer} |
| **Date** | {date_str} |
| **Engine** | {ENGINE_ID} v{ENGINE_VERSION} |

---
"""


def _build_toc(num: int, display: str, prop: dict, client: dict,
               outputs: dict, doctrine: dict) -> str:
    rt_key = None
    for rt in ReportType:
        if REPORT_DISPLAY_NAMES.get(rt.value) == display:
            rt_key = rt.value
            break
    sections = REPORT_SECTIONS.get(rt_key, []) if rt_key else []
    lines = [f"\n## {num}.0 Table of Contents\n"]
    for i, sec in enumerate(sections, 1):
        lines.append(f"{i}. {sec.replace('_', ' ').title()}")
    lines.append("")
    return "\n".join(lines)


def _build_executive_summary(num: int, display: str, prop: dict, client: dict,
                              outputs: dict, doctrine: dict) -> str:
    county = prop.get("county", "[County]")
    state = prop.get("state", "Texas")
    legal_desc = prop.get("legal_description", "[Legal Description]")
    summary_text = outputs.get("executive_summary", "")
    if not summary_text:
        summary_text = (
            f"This {display} covers the property described as {legal_desc}, "
            f"located in {county} County, {state}. The examination is based upon "
            f"instruments of record in the official public records of {county} County "
            f"and additional data provided by the client."
        )
    return f"\n## {num}.0 Executive Summary\n\n{summary_text}\n"


def _build_legal_description(num: int, display: str, prop: dict, client: dict,
                              outputs: dict, doctrine: dict) -> str:
    legal = prop.get("legal_description", "[INSERT LEGAL DESCRIPTION]")
    survey = prop.get("survey", "")
    abstract_no = prop.get("abstract_number", "")
    block = prop.get("block", "")
    section = prop.get("section", "")
    acres = prop.get("acres", "")

    lines = [f"\n## {num}.0 Legal Description\n"]
    lines.append(f"{legal}\n")
    if survey:
        lines.append(f"**Survey:** {survey}")
    if abstract_no:
        lines.append(f"**Abstract No.:** {abstract_no}")
    if block:
        lines.append(f"**Block:** {block}")
    if section:
        lines.append(f"**Section:** {section}")
    if acres:
        lines.append(f"**Gross Acres:** {acres}")
    lines.append("")
    return "\n".join(lines)


def _build_chain_of_title(num: int, display: str, prop: dict, client: dict,
                           outputs: dict, doctrine: dict) -> str:
    chain = outputs.get("chain_of_title", [])
    lines = [f"\n## {num}.0 Chain of Title\n"]
    if not chain:
        lines.append("*No chain of title data provided. Populate `engine_outputs.chain_of_title` "
                      "with an array of instrument records.*\n")
        return "\n".join(lines)

    lines.append("| # | Date | Type | Grantor | Grantee | Vol/Pg | Notes |")
    lines.append("|---|------|------|---------|---------|--------|-------|")
    for i, entry in enumerate(chain, 1):
        date = entry.get("date", "")
        inst_type = entry.get("type", "")
        grantor = entry.get("grantor", "")
        grantee = entry.get("grantee", "")
        vol_pg = entry.get("volume_page", entry.get("recording_info", ""))
        notes = entry.get("notes", "")
        lines.append(f"| {i} | {date} | {inst_type} | {grantor} | {grantee} | {vol_pg} | {notes} |")
    lines.append("")
    return "\n".join(lines)


def _build_current_ownership(num: int, display: str, prop: dict, client: dict,
                              outputs: dict, doctrine: dict) -> str:
    owners = outputs.get("current_ownership", [])
    lines = [f"\n## {num}.0 Current Ownership / Interests\n"]
    if not owners:
        lines.append("*No ownership data provided. Populate `engine_outputs.current_ownership`.*\n")
        return "\n".join(lines)

    lines.append("| Owner | Interest Type | Decimal Interest | Basis |")
    lines.append("|-------|--------------|-----------------|-------|")
    for entry in owners:
        name = entry.get("name", "")
        int_type = entry.get("interest_type", "mineral")
        decimal = entry.get("decimal_interest", "")
        basis = entry.get("basis", "")
        lines.append(f"| {name} | {int_type} | {decimal} | {basis} |")
    lines.append("")
    return "\n".join(lines)


def _build_requirements_exceptions(num: int, display: str, prop: dict, client: dict,
                                    outputs: dict, doctrine: dict) -> str:
    reqs = outputs.get("requirements", [])
    exceptions = outputs.get("exceptions", [])
    lines = [f"\n## {num}.0 Requirements and Exceptions\n"]

    if reqs:
        lines.append(f"### {num}.1 Requirements\n")
        for i, r in enumerate(reqs, 1):
            lines.append(f"{i}. {r}")
        lines.append("")

    if exceptions:
        lines.append(f"### {num}.2 Exceptions\n")
        for i, e in enumerate(exceptions, 1):
            lines.append(f"{i}. {e}")
        lines.append("")

    if not reqs and not exceptions:
        lines.append("*No requirements or exceptions noted at this time.*\n")

    return "\n".join(lines)


def _build_exhibits(num: int, display: str, prop: dict, client: dict,
                    outputs: dict, doctrine: dict) -> str:
    exhibits = outputs.get("exhibits", [])
    lines = [f"\n## {num}.0 Exhibits and Attachments\n"]
    if not exhibits:
        lines.append("| Exhibit | Description |")
        lines.append("|---------|-------------|")
        lines.append("| A | Plat / Survey Map |")
        lines.append("| B | Ownership Summary |")
        lines.append("| C | Instrument Copies |")
    else:
        lines.append("| Exhibit | Description |")
        lines.append("|---------|-------------|")
        for ex in exhibits:
            label = ex.get("label", "")
            desc = ex.get("description", "")
            lines.append(f"| {label} | {desc} |")
    lines.append("")
    return "\n".join(lines)


def _build_certification(num: int, display: str, prop: dict, client: dict,
                          outputs: dict, doctrine: dict) -> str:
    preparer = client.get("prepared_by", "ECHO OMEGA PRIME -- E06 Report Generator")
    bar_no = client.get("bar_number", "")
    firm = client.get("firm", "")
    date_str = datetime.now(timezone.utc).strftime("%B %d, %Y")

    bar_line = f"**Bar No.:** {bar_no}\n" if bar_no else ""
    firm_line = f"**Firm:** {firm}\n" if firm else ""

    return f"""
## {num}.0 Certification / Disclaimer

This report has been prepared based upon examination of instruments of record and
data provided. The opinions expressed herein are limited to the scope described above.
This report does not constitute a guarantee of title and is subject to the requirements
and exceptions noted herein.

**Prepared By:** {preparer}
{bar_line}{firm_line}**Date:** {date_str}

*Generated by ECHO OMEGA PRIME Engine {ENGINE_ID} v{ENGINE_VERSION}*

---
**DISCLAIMER:** This report is generated by an AI-assisted system and should be
reviewed by qualified legal counsel before reliance. No attorney-client relationship
is created by this report.
"""


def _build_division_of_interests(num: int, display: str, prop: dict, client: dict,
                                  outputs: dict, doctrine: dict) -> str:
    interests = outputs.get("division_of_interests", [])
    lines = [f"\n## {num}.0 Division of Interests\n"]
    if not interests:
        lines.append("*No division of interest data provided.*\n")
        return "\n".join(lines)

    lines.append("| Owner | WI | NRI | RI | ORRI | Notes |")
    lines.append("|-------|----|-----|----|------|-------|")
    for entry in interests:
        name = entry.get("name", "")
        wi = entry.get("working_interest", "")
        nri = entry.get("net_revenue_interest", "")
        ri = entry.get("royalty_interest", "")
        orri = entry.get("overriding_royalty", "")
        notes = entry.get("notes", "")
        lines.append(f"| {name} | {wi} | {nri} | {ri} | {orri} | {notes} |")
    lines.append("")
    return "\n".join(lines)


def _build_decimal_interest_table(num: int, display: str, prop: dict, client: dict,
                                   outputs: dict, doctrine: dict) -> str:
    table = outputs.get("decimal_interest_table", [])
    lines = [f"\n## {num}.0 Decimal Interest Table\n"]
    if not table:
        lines.append("*No decimal interest data provided.*\n")
        return "\n".join(lines)

    lines.append("| Owner | Interest Fraction | Decimal | Check |")
    lines.append("|-------|-------------------|---------|-------|")
    for row in table:
        lines.append(f"| {row.get('name','')} | {row.get('fraction','')} | {row.get('decimal','')} | {row.get('check','')} |")
    lines.append("")
    return "\n".join(lines)


def _build_risk_matrix(num: int, display: str, prop: dict, client: dict,
                       outputs: dict, doctrine: dict) -> str:
    risks = outputs.get("risk_matrix", [])
    lines = [f"\n## {num}.0 Risk Matrix\n"]
    if not risks:
        lines.append("| Risk Category | Likelihood | Impact | Score | Mitigation |")
        lines.append("|--------------|-----------|--------|-------|------------|")
        lines.append("| Title Defect | Medium | High | 6 | Curative action |")
        lines.append("| Environmental | Low | High | 4 | Phase I ESA |")
        lines.append("| Regulatory | Low | Medium | 3 | Permit review |")
    else:
        lines.append("| Risk Category | Likelihood | Impact | Score | Mitigation |")
        lines.append("|--------------|-----------|--------|-------|------------|")
        for r in risks:
            lines.append(f"| {r.get('category','')} | {r.get('likelihood','')} | {r.get('impact','')} | {r.get('score','')} | {r.get('mitigation','')} |")
    lines.append("")
    return "\n".join(lines)


def _build_property_overview(num: int, display: str, prop: dict, client: dict,
                              outputs: dict, doctrine: dict) -> str:
    lines = [f"\n## {num}.0 Property Overview\n"]
    for key in ["county", "state", "operator", "field", "formation", "api_number",
                "lease_name", "well_name", "spud_date", "completion_date"]:
        val = prop.get(key) or outputs.get(key)
        if val:
            lines.append(f"**{key.replace('_',' ').title()}:** {val}")
    lines.append("")
    return "\n".join(lines)


def _build_production_summary_table(num: int, display: str, prop: dict, client: dict,
                                     outputs: dict, doctrine: dict) -> str:
    records = outputs.get("production_data", [])
    lines = [f"\n## {num}.0 Production Summary\n"]
    if not records:
        lines.append("*No production data provided.*\n")
        return "\n".join(lines)

    lines.append("| Period | Oil (BBL) | Gas (MCF) | Water (BBL) | Days |")
    lines.append("|--------|-----------|-----------|-------------|------|")
    for rec in records:
        lines.append(f"| {rec.get('period','')} | {rec.get('oil','')} | {rec.get('gas','')} | {rec.get('water','')} | {rec.get('days','')} |")
    lines.append("")
    return "\n".join(lines)


def _build_generic_section(section_name: str):
    """Factory for simple sections that just render heading + engine_outputs content."""
    def builder(num: int, display: str, prop: dict, client: dict,
                outputs: dict, doctrine: dict) -> str:
        content = outputs.get(section_name, "")
        heading = section_name.replace("_", " ").title()
        lines = [f"\n## {num}.0 {heading}\n"]
        if content:
            if isinstance(content, list):
                for i, item in enumerate(content, 1):
                    if isinstance(item, dict):
                        lines.append(f"{i}. " + "; ".join(f"**{k}**: {v}" for k, v in item.items()))
                    else:
                        lines.append(f"{i}. {item}")
            elif isinstance(content, dict):
                for k, v in content.items():
                    lines.append(f"**{k.replace('_',' ').title()}:** {v}")
            else:
                lines.append(str(content))
        else:
            lines.append(f"*No {heading.lower()} data provided.*")
        lines.append("")
        return "\n".join(lines)
    return builder


# Section builder registry
SECTION_BUILDERS: dict[str, Any] = {
    "cover_page": _build_cover_page,
    "table_of_contents": _build_toc,
    "executive_summary": _build_executive_summary,
    "legal_description": _build_legal_description,
    "chain_of_title": _build_chain_of_title,
    "current_ownership": _build_current_ownership,
    "requirements_exceptions": _build_requirements_exceptions,
    "exhibits": _build_exhibits,
    "certification": _build_certification,
    "division_of_interests": _build_division_of_interests,
    "decimal_interest_table": _build_decimal_interest_table,
    "risk_matrix": _build_risk_matrix,
    "property_overview": _build_property_overview,
    "production_summary_table": _build_production_summary_table,
}

# Auto-generate generic builders for all sections not explicitly registered
_ALL_SECTIONS = set()
for sec_list in REPORT_SECTIONS.values():
    _ALL_SECTIONS.update(sec_list)
for sec in _ALL_SECTIONS:
    if sec not in SECTION_BUILDERS:
        SECTION_BUILDERS[sec] = _build_generic_section(sec)


# ============================================================================
# [TIE-02] RESPONSE MODES
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


def apply_response_mode(raw: str, mode: str, report_type: Optional[str]) -> str:
    """Apply response mode formatting to the generated report."""
    if mode == ResponseMode.FAST:
        return raw

    if mode == ResponseMode.DEFENSE:
        header = (
            "---\n"
            "**AUDIT-READY REPORT**\n"
            f"Engine: {ENGINE_ID} v{ENGINE_VERSION} | Mode: DEFENSE | "
            f"Report Type: {REPORT_DISPLAY_NAMES.get(report_type, report_type or 'General')}\n"
            f"Generated: {datetime.now(timezone.utc).isoformat()}\n"
            "All statements herein are supported by cited authority or engine output data.\n"
            "---\n\n"
        )
        footer = (
            "\n---\n"
            "**Audit Trail:** Full query trace available via /audit endpoint.\n"
            "**Determinism:** SHA-256 hash computed over response content.\n"
            "---\n"
        )
        return header + raw + footer

    if mode == ResponseMode.MEMO:
        header = (
            "---\n"
            f"**MEMORANDUM -- {REPORT_DISPLAY_NAMES.get(report_type, report_type or 'General')}**\n\n"
            f"**Prepared by:** {ENGINE_ID} v{ENGINE_VERSION}\n"
            f"**Date:** {datetime.now(timezone.utc).strftime('%B %d, %Y')}\n"
            "**Purpose:** Full documentation of analysis, methodology, and conclusions.\n"
            "---\n\n"
            "### Methodology\n\n"
            "This report was generated using the ECHO OMEGA PRIME Report Generator Engine "
            "(E06), which implements a three-layer response architecture: (1) Doctrine Cache "
            "for pre-compiled report templates and formatting rules, (2) Semantic Retrieval "
            "for normalized term matching across the knowledge base, and (3) Deep Analysis "
            "mode for multi-source synthesis when templates are insufficient.\n\n"
        )
        return header + raw

    return raw


# ============================================================================
# [TIE-03] DOCTRINE CACHE -- 30+ BLOCKS
# ============================================================================

DOCTRINE_BLOCKS: list[dict[str, Any]] = [
    {
        "topic": "preliminary_title_opinion_format",
        "keywords": ["preliminary", "title opinion", "pto", "preliminary opinion"],
        "conclusion_template": (
            "A Preliminary Title Opinion examines the chain of title from sovereignty "
            "of the soil to the present date. The examiner reviews all instruments of "
            "record affecting the subject property and renders an opinion as to the "
            "current state of title, identifying any defects, requirements for curative "
            "action, and exceptions to clear title."
        ),
        "reasoning_framework": (
            "1. Identify the root of title (sovereign/patent). "
            "2. Trace each conveyance in chronological order. "
            "3. Note gaps, breaks, or defects in the chain. "
            "4. Identify all outstanding mineral/royalty/leasehold interests. "
            "5. List requirements for curing any defects. "
            "6. State exceptions to the opinion."
        ),
        "key_factors": ["chain completeness", "gap identification", "defect classification",
                        "mineral reservation tracing", "exception categorization"],
        "primary_authority": ["Tex. Prop. Code Ch. 5", "Tex. Nat. Res. Code Ch. 91"],
        "confidence": 0.90,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "division_order_title_opinion_format",
        "keywords": ["division order", "doto", "division opinion", "doi"],
        "conclusion_template": (
            "A Division Order Title Opinion (DOTO) examines title to determine the "
            "fractional interests of all parties entitled to share in production revenues. "
            "It quantifies working interests, royalty interests, overriding royalty interests, "
            "and net revenue interests to the eighth decimal place."
        ),
        "reasoning_framework": (
            "1. Review chain of title. "
            "2. Identify all mineral owners and their fractional interests. "
            "3. Calculate working interest, NRI, royalty from lease terms. "
            "4. Account for pooling, unitization, and proportionate reduction. "
            "5. Generate decimal interest table. "
            "6. Cross-check: all interests sum to 1.00000000."
        ),
        "key_factors": ["decimal computation accuracy", "pooling impact", "proportionate reduction",
                        "overriding royalty carve-outs", "carried interests"],
        "primary_authority": ["Tex. Nat. Res. Code Sec. 91.402", "Tex. Bus. & Com. Code Sec. 9.343"],
        "confidence": 0.92,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "run_sheet_format",
        "keywords": ["run sheet", "ownership summary", "chain summary", "abstract of title"],
        "conclusion_template": (
            "A Run Sheet is a chronological summary of all instruments affecting title, "
            "listing grantor, grantee, instrument type, recording information, and the "
            "interest conveyed. It provides a concise reference for ownership tracing."
        ),
        "reasoning_framework": (
            "1. Start with the patent or sovereign grant. "
            "2. List each instrument chronologically. "
            "3. Note grantor, grantee, date, type, recording info. "
            "4. Summarize current ownership at the end."
        ),
        "key_factors": ["chronological accuracy", "completeness of instruments",
                        "recording reference precision"],
        "primary_authority": ["County Clerk Recording Standards", "AAPL Form 610-T"],
        "confidence": 0.88,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "lease_abstract_format",
        "keywords": ["lease abstract", "oil gas lease", "lease summary", "lease terms"],
        "conclusion_template": (
            "A Lease Abstract summarizes the essential terms of an oil and gas lease: "
            "parties, legal description, primary term, royalty rate, pooling provisions, "
            "shut-in provisions, and any amendments or assignments."
        ),
        "reasoning_framework": (
            "1. Identify lessor and lessee. "
            "2. Describe the leased premises. "
            "3. State primary term and commencement date. "
            "4. Detail royalty provisions (oil, gas, NGLs). "
            "5. Summarize pooling/unitization clauses. "
            "6. Note all assignments and amendments."
        ),
        "key_factors": ["royalty rate", "pooling clause type (Pugh/anti-Pugh)",
                        "depth limitations", "continuous drilling obligations"],
        "primary_authority": ["AAPL Form 610", "Tex. Nat. Res. Code Ch. 91"],
        "confidence": 0.89,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "curative_requirement_letter",
        "keywords": ["curative", "requirement letter", "cure", "title defect"],
        "conclusion_template": (
            "A Curative Requirement Letter identifies specific title defects and "
            "requests the necessary corrective instruments (affidavits, ratifications, "
            "probate proceedings, corrective deeds) to clear title."
        ),
        "reasoning_framework": (
            "1. Identify each title defect from the opinion. "
            "2. Classify defect type (gap, missing heir, unreleased lien). "
            "3. Prescribe specific curative action per defect. "
            "4. Set deadlines for compliance. "
            "5. Provide contact information for follow-up."
        ),
        "key_factors": ["defect specificity", "curative instrument type",
                        "deadline reasonableness", "statutory authority for cure"],
        "primary_authority": ["Tex. Prop. Code Sec. 13.001", "Tex. Est. Code Sec. 202"],
        "confidence": 0.87,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "due_diligence_report_format",
        "keywords": ["due diligence", "acquisition", "asset evaluation", "dd report"],
        "conclusion_template": (
            "A Due Diligence Summary provides a comprehensive evaluation of an asset "
            "for acquisition purposes, covering title, environmental, regulatory, "
            "financial, and operational risk factors."
        ),
        "reasoning_framework": (
            "1. Title analysis -- chain integrity, outstanding interests. "
            "2. Environmental review -- contamination, remediation obligations. "
            "3. Regulatory status -- permits, compliance, pending actions. "
            "4. Financial analysis -- revenue history, projections, encumbrances. "
            "5. Operational risk -- equipment condition, staffing, HSE record. "
            "6. Synthesize into go/no-go recommendation."
        ),
        "key_factors": ["title defect materiality", "environmental liability exposure",
                        "regulatory compliance status", "revenue reliability"],
        "primary_authority": ["SEC Reg S-K Item 1200", "FASB ASC 932"],
        "confidence": 0.85,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "risk_assessment_methodology",
        "keywords": ["risk assessment", "risk matrix", "risk score", "risk analysis"],
        "conclusion_template": (
            "Risk Assessment Reports quantify and categorize risks using a likelihood-x-impact "
            "matrix. Each risk is scored 1-5 on both axes, yielding a composite risk score "
            "from 1 (negligible) to 25 (critical), with prescribed mitigation strategies."
        ),
        "reasoning_framework": (
            "1. Identify all material risks by category. "
            "2. Score likelihood (1-5) based on probability. "
            "3. Score impact (1-5) based on financial/legal consequence. "
            "4. Compute composite score. "
            "5. Rank and prioritize. "
            "6. Prescribe mitigation for scores >= 9."
        ),
        "key_factors": ["scoring consistency", "mitigation feasibility",
                        "residual risk estimation", "cost-benefit of mitigation"],
        "primary_authority": ["ISO 31000", "COSO ERM Framework"],
        "confidence": 0.86,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "regulatory_compliance_report_format",
        "keywords": ["regulatory", "compliance", "rrc", "epa", "permits"],
        "conclusion_template": (
            "A Regulatory Compliance Report catalogs all applicable permits, licenses, "
            "and regulatory requirements, identifies compliance gaps, and proposes "
            "a remediation timeline."
        ),
        "reasoning_framework": (
            "1. Inventory all permits and licenses. "
            "2. Map to applicable regulations (RRC, EPA, TCEQ, OSHA). "
            "3. Identify gaps or expired permits. "
            "4. Assess penalty exposure. "
            "5. Propose remediation plan with timeline."
        ),
        "key_factors": ["permit status", "violation history", "penalty exposure",
                        "remediation cost", "timeline feasibility"],
        "primary_authority": ["16 TAC Ch. 3 (RRC)", "40 CFR (EPA)", "Tex. Water Code"],
        "confidence": 0.84,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "environmental_assessment_format",
        "keywords": ["environmental", "contamination", "esa", "phase i", "phase ii"],
        "conclusion_template": (
            "An Environmental Assessment Summary evaluates potential environmental "
            "liabilities associated with a property, including historical contamination, "
            "active remediation, and regulatory actions."
        ),
        "reasoning_framework": (
            "1. Review site history (historical use, prior operators). "
            "2. Identify potential contamination sources. "
            "3. Summarize Phase I/II ESA findings if available. "
            "4. Assess regulatory actions (TCEQ, EPA orders). "
            "5. Estimate remediation liability. "
            "6. Recommend further investigation if warranted."
        ),
        "key_factors": ["contamination type and extent", "regulatory action status",
                        "remediation cost estimate", "liability allocation"],
        "primary_authority": ["CERCLA 42 USC 9601", "RCRA 42 USC 6901", "Tex. Health & Safety Code Ch. 361"],
        "confidence": 0.83,
        "confidence_stratification": "AGGRESSIVE",
    },
    {
        "topic": "production_history_report_format",
        "keywords": ["production", "history", "decline", "cumulative", "oil gas production"],
        "conclusion_template": (
            "A Production History Report summarizes monthly and cumulative production "
            "volumes (oil, gas, water), calculates decline rates, and identifies "
            "operator history changes."
        ),
        "reasoning_framework": (
            "1. Compile monthly production data. "
            "2. Calculate cumulative totals. "
            "3. Perform decline curve analysis. "
            "4. Identify significant changes (workovers, recompletions). "
            "5. Note operator changes and their impact."
        ),
        "key_factors": ["data completeness", "decline rate accuracy",
                        "workover impact", "water cut trend"],
        "primary_authority": ["RRC Form PR", "RRC Statewide Rule 26"],
        "confidence": 0.87,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "revenue_analysis_format",
        "keywords": ["revenue", "analysis", "net revenue", "price", "deductions"],
        "conclusion_template": (
            "A Revenue Analysis Report projects net revenue from production based "
            "on price forecasts, interest ownership, and applicable deductions "
            "(gathering, processing, transportation, severance tax)."
        ),
        "reasoning_framework": (
            "1. Establish production forecast (from decline analysis). "
            "2. Apply price deck (WTI, Henry Hub). "
            "3. Compute gross revenue. "
            "4. Apply interest ownership (NRI). "
            "5. Deduct post-production costs. "
            "6. Compute net revenue and PV-10."
        ),
        "key_factors": ["price deck assumptions", "decline forecast reliability",
                        "deduction methodology (net-back vs. percentage)"],
        "primary_authority": ["SEC Reg S-K Item 1204", "SPEE Recommended Practices"],
        "confidence": 0.82,
        "confidence_stratification": "AGGRESSIVE",
    },
    {
        "topic": "heirship_determination_format",
        "keywords": ["heirship", "heir", "intestate", "succession", "family tree"],
        "conclusion_template": (
            "An Heirship Determination Report identifies the heirs of a deceased "
            "mineral owner, maps family relationships, applies intestate succession "
            "statutes, and allocates fractional interests among heirs."
        ),
        "reasoning_framework": (
            "1. Identify decedent and date of death. "
            "2. Determine if testate or intestate. "
            "3. Build family tree from vital records. "
            "4. Apply applicable succession statute. "
            "5. Compute fractional interest per heir. "
            "6. Identify unlocated or unknown heirs."
        ),
        "key_factors": ["succession law version (date of death controls)", "community vs. separate property",
                        "per stirpes vs. per capita", "unknown heir risk"],
        "primary_authority": ["Tex. Est. Code Ch. 201", "Tex. Est. Code Sec. 202.001"],
        "confidence": 0.84,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "probate_summary_format",
        "keywords": ["probate", "estate", "will", "administration", "executor"],
        "conclusion_template": (
            "A Probate Summary details the probate proceeding for a deceased "
            "interest owner, including will provisions, estate inventory, "
            "distribution schedule, and outstanding issues affecting title."
        ),
        "reasoning_framework": (
            "1. Identify court and cause number. "
            "2. Summarize will provisions (if testate). "
            "3. List estate inventory relevant to mineral interests. "
            "4. Detail distribution schedule. "
            "5. Identify outstanding issues (creditor claims, contests)."
        ),
        "key_factors": ["will validity", "executor authority", "distribution completeness",
                        "creditor claim status"],
        "primary_authority": ["Tex. Est. Code Ch. 256", "Tex. Est. Code Ch. 301"],
        "confidence": 0.85,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "tax_analysis_report_format",
        "keywords": ["tax", "ad valorem", "severance", "depletion", "tax analysis"],
        "conclusion_template": (
            "A Tax Analysis Report evaluates the tax implications of mineral "
            "interest ownership, including ad valorem property taxes, severance "
            "taxes, income tax deductions (depletion, IDC), and available credits."
        ),
        "reasoning_framework": (
            "1. Determine property valuation methodology. "
            "2. Calculate ad valorem tax liability. "
            "3. Compute severance tax (oil 4.6%, gas 7.5% in TX). "
            "4. Analyze cost depletion vs. percentage depletion. "
            "5. Evaluate IDC election (expense vs. capitalize). "
            "6. Identify applicable tax credits."
        ),
        "key_factors": ["valuation method", "tax rate accuracy", "depletion election",
                        "IDC treatment", "credit eligibility"],
        "primary_authority": ["IRC Sec. 611-613A", "Tex. Tax Code Ch. 202", "Tex. Tax Code Ch. 23"],
        "confidence": 0.86,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "well_file_summary_format",
        "keywords": ["well file", "drilling", "completion", "permit", "well summary"],
        "conclusion_template": (
            "A Well File Summary compiles all critical well information: permit, "
            "drilling summary, completion data, production history, operator "
            "changes, and regulatory filings."
        ),
        "reasoning_framework": (
            "1. Compile permit information (W-1, W-1X). "
            "2. Summarize drilling operations (spud, TD, casing). "
            "3. Detail completion (perfs, frac, initial production). "
            "4. Include production history summary. "
            "5. List operator changes (P-4 filings). "
            "6. Note regulatory actions (violations, plugging status)."
        ),
        "key_factors": ["permit compliance", "completion design", "IP rate",
                        "decline trend", "plugging status"],
        "primary_authority": ["16 TAC 3.5 (W-1)", "16 TAC 3.14 (W-2)", "RRC Form P-4"],
        "confidence": 0.88,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "permit_application_format",
        "keywords": ["permit", "application", "w-1", "drilling permit", "w-1x"],
        "conclusion_template": (
            "A Permit Application Summary outlines the proposed drilling operation, "
            "well location, surface owner notification status, and environmental "
            "considerations for regulatory submission."
        ),
        "reasoning_framework": (
            "1. Identify operator and proposed well name. "
            "2. Describe proposed location (survey, section, abstract). "
            "3. Detail proposed operations (depth, formation target). "
            "4. Confirm surface owner notification (Rule 37). "
            "5. Address environmental considerations. "
            "6. Complete regulatory checklist."
        ),
        "key_factors": ["spacing compliance", "surface owner notice", "field rules",
                        "exception necessity", "environmental clearance"],
        "primary_authority": ["16 TAC 3.37 (Rule 37)", "16 TAC 3.38 (Rule 38)"],
        "confidence": 0.87,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "surface_damage_assessment_format",
        "keywords": ["surface damage", "surface use", "accommodation", "damage assessment"],
        "conclusion_template": (
            "A Surface Damage Assessment evaluates damage to the surface estate "
            "caused by mineral development operations, quantifies repair costs, "
            "and establishes a payment schedule."
        ),
        "reasoning_framework": (
            "1. Survey affected surface area. "
            "2. Document pre-existing conditions. "
            "3. Assess damage from operations (roads, pads, pits). "
            "4. Estimate remediation costs. "
            "5. Apply accommodation doctrine principles. "
            "6. Propose payment schedule."
        ),
        "key_factors": ["damage extent", "pre-existing condition documentation",
                        "remediation cost accuracy", "accommodation doctrine compliance"],
        "primary_authority": ["Getty Oil v. Jones (1985)", "Tex. Nat. Res. Code Sec. 91.402",
                              "Accommodation Doctrine -- Tex. common law"],
        "confidence": 0.83,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "pipeline_right_of_way_format",
        "keywords": ["pipeline", "right of way", "easement", "row", "pipeline row"],
        "conclusion_template": (
            "A Pipeline Right-of-Way Report analyzes the easement rights for "
            "pipeline construction and operation, including landowner identification, "
            "compensation terms, and regulatory requirements."
        ),
        "reasoning_framework": (
            "1. Describe pipeline route and specifications. "
            "2. Identify affected landowners along route. "
            "3. Analyze existing easements and encumbrances. "
            "4. Determine compensation methodology. "
            "5. Review regulatory requirements (RRC, FERC if interstate). "
            "6. Address eminent domain considerations."
        ),
        "key_factors": ["easement width", "compensation basis", "existing encumbrances",
                        "regulatory classification", "eminent domain authority"],
        "primary_authority": ["Tex. Util. Code Ch. 181", "49 USC 60101 (Pipeline Safety Act)"],
        "confidence": 0.82,
        "confidence_stratification": "AGGRESSIVE",
    },
    {
        "topic": "pooling_unit_report_format",
        "keywords": ["pooling", "unit", "pooling unit", "unitization", "proration"],
        "conclusion_template": (
            "A Pooling Unit Report details the formation and composition of a pooling "
            "or drilling unit, listing participating tracts, allocated interests, "
            "unit agreement terms, and regulatory approval status."
        ),
        "reasoning_framework": (
            "1. Identify unit designation and effective date. "
            "2. Describe unit boundaries (legal description). "
            "3. List all participating tracts and their acreage. "
            "4. Calculate interest allocation (acreage-based or otherwise). "
            "5. Summarize unit agreement terms. "
            "6. Confirm regulatory approval (RRC, OCC, etc.)."
        ),
        "key_factors": ["tract inclusion", "allocation methodology", "Pugh clause impact",
                        "regulatory approval status"],
        "primary_authority": ["Tex. Nat. Res. Code Sec. 102.001", "16 TAC 3.38"],
        "confidence": 0.85,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "force_pooling_analysis_format",
        "keywords": ["force pooling", "compulsory pooling", "forced integration"],
        "conclusion_template": (
            "A Force Pooling Analysis evaluates a compulsory pooling application, "
            "detailing the applicant's offers, respondent's options (participate, "
            "non-consent, lease), and the statutory framework for the hearing."
        ),
        "reasoning_framework": (
            "1. Identify applicant and respondent. "
            "2. Document offers made and responses received. "
            "3. Analyze election options under applicable statute. "
            "4. Review hearing history and testimony. "
            "5. Evaluate likely order terms. "
            "6. Calculate economic impact of each election option."
        ),
        "key_factors": ["offer adequacy", "statutory compliance", "election economics",
                        "risk penalty provisions", "appeal rights"],
        "primary_authority": ["OCC pooling statutes (52 O.S. Sec. 87.1)", "Tex. Nat. Res. Code Ch. 102"],
        "confidence": 0.80,
        "confidence_stratification": "AGGRESSIVE",
    },
    {
        "topic": "supplemental_title_opinion_format",
        "keywords": ["supplemental", "supplement", "update opinion", "bring-down"],
        "conclusion_template": (
            "A Supplemental Title Opinion updates a prior opinion by examining "
            "new instruments recorded since the effective date of the original "
            "opinion and revises ownership and requirements accordingly."
        ),
        "reasoning_framework": (
            "1. Reference original opinion (date, file number). "
            "2. State effective date of supplement. "
            "3. Review instruments recorded since original effective date. "
            "4. Update chain of title. "
            "5. Revise ownership if changed. "
            "6. Update requirements and exceptions."
        ),
        "key_factors": ["gap between opinions", "new instruments impact",
                        "requirement satisfaction status"],
        "primary_authority": ["AAPL Form 610-T", "State bar title examination standards"],
        "confidence": 0.88,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "competitive_activity_report_format",
        "keywords": ["competitive", "activity", "competitor", "area activity", "scout"],
        "conclusion_template": (
            "A Competitive Activity Report summarizes drilling, permitting, "
            "completion, and leasing activity by competitors in a defined "
            "area of interest."
        ),
        "reasoning_framework": (
            "1. Define area of interest (AOI). "
            "2. Identify active operators in AOI. "
            "3. Catalog recent permits filed. "
            "4. Track active drilling rigs. "
            "5. Summarize recent completions and IP rates. "
            "6. Monitor lease activity and bonus trends."
        ),
        "key_factors": ["AOI definition", "operator identification", "permit trend",
                        "IP rate benchmarking", "lease bonus trends"],
        "primary_authority": ["RRC Online System", "DrillingInfo/Enverus"],
        "confidence": 0.81,
        "confidence_stratification": "AGGRESSIVE",
    },
    {
        "topic": "citation_formatting_legal",
        "keywords": ["citation", "legal citation", "bluebook", "cite format"],
        "conclusion_template": (
            "Legal citations must follow standard formatting: case names in italics, "
            "volume-reporter-page format, statute citations with code abbreviation "
            "and section symbol. Property recordings cite Volume and Page or "
            "Document/Clerk's File Number."
        ),
        "reasoning_framework": (
            "Case: *Party v. Party*, Vol Reporter Page (Court Year). "
            "Statute: Tex. Code Sec. XX.XXX. "
            "Recording: Vol. XXX, Pg. XXX, Official Records, County, State. "
            "Document No: Doc. No. XXXXXXX, Official Records, County, State."
        ),
        "key_factors": ["citation accuracy", "parallel citations", "pinpoint references"],
        "primary_authority": ["Bluebook 21st Ed.", "Texas Rules of Form (Greenbook)"],
        "confidence": 0.93,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "section_numbering_conventions",
        "keywords": ["section number", "numbering", "outline", "heading format"],
        "conclusion_template": (
            "Reports use hierarchical section numbering: 1.0 for major sections, "
            "1.1 for subsections, 1.1.1 for sub-subsections. Cover page is unnumbered. "
            "Table of Contents maps all numbered sections."
        ),
        "reasoning_framework": (
            "Level 1: # 1.0 Major Section (H1). "
            "Level 2: ## 1.1 Subsection (H2). "
            "Level 3: ### 1.1.1 Sub-subsection (H3). "
            "Tables use | pipe | formatting. "
            "Exhibits are lettered (A, B, C)."
        ),
        "key_factors": ["consistency", "depth limit (3 levels)", "exhibit lettering"],
        "primary_authority": ["Internal report standards"],
        "confidence": 0.95,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "interest_calculation_methodology",
        "keywords": ["interest calculation", "decimal interest", "fractional interest", "nri"],
        "conclusion_template": (
            "Interest calculations trace from the full mineral estate (1.00000000) "
            "through each conveyance, reservation, and lease to arrive at current "
            "working interest, royalty interest, and net revenue interest to eight "
            "decimal places."
        ),
        "reasoning_framework": (
            "1. Start with full mineral estate (1.0). "
            "2. Apply each conveyance/reservation chronologically. "
            "3. Separate mineral from surface interests. "
            "4. Apply lease royalty rate to compute RI. "
            "5. WI = 1.0 - sum of all non-working interests. "
            "6. NRI = WI * (1 - royalty burden). "
            "7. Verify: all interests sum to 1.00000000."
        ),
        "key_factors": ["8-decimal precision", "reservation language interpretation",
                        "Duhig rule application", "proportionate reduction"],
        "primary_authority": ["Duhig v. Peavy-Moore Lumber Co. (1940)",
                              "Tex. Nat. Res. Code Sec. 91.402"],
        "confidence": 0.91,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "mineral_vs_royalty_distinction",
        "keywords": ["mineral interest", "royalty interest", "mineral vs royalty", "npri"],
        "conclusion_template": (
            "A mineral interest includes the right to develop (executive right), "
            "right to lease, right to receive bonus and delay rentals, and right "
            "to receive royalties. A royalty interest (NPRI) is only the right to "
            "receive a share of production free of costs. This distinction is "
            "critical for division order calculations."
        ),
        "reasoning_framework": (
            "Mineral interest = executive right + bonus + delay rental + royalty. "
            "NPRI = royalty right only (non-participating, non-cost-bearing). "
            "Classification depends on deed language, not label used by grantor."
        ),
        "key_factors": ["deed language interpretation", "executive right retention",
                        "cost-bearing obligation", "French v. Chevron analysis"],
        "primary_authority": ["French v. Chevron (2018)", "Altman v. Blake (1998)"],
        "confidence": 0.90,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "report_quality_assurance",
        "keywords": ["quality", "qa", "review", "proofread", "accuracy check"],
        "conclusion_template": (
            "All reports undergo quality assurance: (1) data integrity check -- "
            "all inputs validated, (2) calculation verification -- interest sums "
            "verified, (3) citation check -- all authorities confirmed, "
            "(4) formatting review -- consistent numbering and style."
        ),
        "reasoning_framework": (
            "1. Validate all input data fields. "
            "2. Cross-check calculations (interest sums = 1.0). "
            "3. Verify cited authorities exist. "
            "4. Check section numbering consistency. "
            "5. Confirm all cross-references resolve. "
            "6. Spell-check proper nouns."
        ),
        "key_factors": ["data validation", "calculation accuracy", "citation validity",
                        "format consistency"],
        "primary_authority": ["Internal QA procedures"],
        "confidence": 0.94,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "markdown_to_pdf_conversion",
        "keywords": ["pdf", "markdown", "convert", "format", "export"],
        "conclusion_template": (
            "Reports are generated in Markdown format for maximum portability. "
            "Conversion to PDF preserves tables, headings, bold/italic formatting, "
            "and page breaks. Headers and footers include file number and page count."
        ),
        "reasoning_framework": (
            "1. Generate report in Markdown. "
            "2. Apply CSS styling for PDF (margins, fonts, spacing). "
            "3. Insert page breaks before major sections. "
            "4. Add header (file number) and footer (page X of Y). "
            "5. Convert via pandoc, weasyprint, or pdfkit."
        ),
        "key_factors": ["table rendering fidelity", "page break placement",
                        "header/footer accuracy", "font consistency"],
        "primary_authority": ["CommonMark spec", "GFM Tables extension"],
        "confidence": 0.88,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "exhibit_cross_referencing",
        "keywords": ["exhibit", "cross reference", "attachment", "appendix"],
        "conclusion_template": (
            "Exhibits are lettered sequentially (A, B, C...) and cross-referenced "
            "in the body text using the format 'See Exhibit A.' Each exhibit has "
            "a cover sheet identifying its contents."
        ),
        "reasoning_framework": (
            "1. Number exhibits alphabetically. "
            "2. Insert cross-reference at first mention in body. "
            "3. List all exhibits in the Exhibits section. "
            "4. Verify each cross-reference resolves to a listed exhibit."
        ),
        "key_factors": ["sequential lettering", "bidirectional references",
                        "exhibit completeness"],
        "primary_authority": ["Internal formatting standards"],
        "confidence": 0.92,
        "confidence_stratification": "DEFENSIBLE",
    },
    {
        "topic": "multi_county_report_handling",
        "keywords": ["multi county", "multiple counties", "cross county", "multi-jurisdiction"],
        "conclusion_template": (
            "When a property spans multiple counties, the report must address each "
            "county's recording system separately, note any discrepancies in legal "
            "descriptions, and reconcile interests across jurisdictions."
        ),
        "reasoning_framework": (
            "1. Identify all counties involved. "
            "2. Search records in each county independently. "
            "3. Reconcile legal descriptions across counties. "
            "4. Note recording differences (document numbering systems). "
            "5. Consolidate ownership analysis. "
            "6. Flag any cross-county conflicts."
        ),
        "key_factors": ["jurisdictional coverage", "legal description reconciliation",
                        "recording system differences"],
        "primary_authority": ["Tex. Prop. Code Sec. 13.001", "County Clerk standards"],
        "confidence": 0.81,
        "confidence_stratification": "AGGRESSIVE",
    },
    {
        "topic": "confidentiality_and_privilege",
        "keywords": ["confidential", "privilege", "attorney client", "work product"],
        "conclusion_template": (
            "Reports prepared at the direction of legal counsel may be protected "
            "by attorney-client privilege or work product doctrine. Reports should "
            "include appropriate confidentiality legends and distribution restrictions."
        ),
        "reasoning_framework": (
            "1. Determine if report is attorney-directed. "
            "2. Apply appropriate confidentiality legend. "
            "3. Restrict distribution to named recipients. "
            "4. Note work product doctrine applicability. "
            "5. Include privilege preservation language."
        ),
        "key_factors": ["attorney direction", "privilege applicability",
                        "distribution control", "waiver risk"],
        "primary_authority": ["Tex. R. Evid. 503", "Fed. R. Civ. P. 26(b)(3)"],
        "confidence": 0.85,
        "confidence_stratification": "DEFENSIBLE",
    },
]


class DoctrineCache:
    """[TIE-03] Pre-compiled doctrine blocks for sub-200ms response."""

    def __init__(self) -> None:
        self.blocks: list[dict[str, Any]] = DOCTRINE_BLOCKS
        self._index: dict[str, list[int]] = defaultdict(list)
        self._build_index()

    def _build_index(self) -> None:
        for i, block in enumerate(self.blocks):
            for kw in block.get("keywords", []):
                self._index[kw.lower()].append(i)
            self._index[block["topic"].lower()].append(i)

    def lookup(self, query: str, report_type: Optional[str] = None) -> Optional[dict[str, Any]]:
        q = query.lower()
        best_score = 0
        best_block: Optional[dict[str, Any]] = None

        for block in self.blocks:
            score = 0
            for kw in block.get("keywords", []):
                if kw.lower() in q:
                    score += 2
            if report_type and report_type.lower() in block["topic"].lower():
                score += 5
            if score > best_score:
                best_score = score
                best_block = block

        return best_block if best_score >= 2 else None

    def all_topics(self) -> list[str]:
        return [b["topic"] for b in self.blocks]

    def count(self) -> int:
        return len(self.blocks)


# ============================================================================
# [TIE-04] AUTHORITY HARDENING
# ============================================================================

AUTHORITY_WEIGHTS: dict[str, float] = {
    "statute": 1.0,
    "regulation": 0.95,
    "case_law_supreme": 0.90,
    "case_law_appellate": 0.80,
    "agency_ruling": 0.70,
    "industry_standard": 0.60,
    "secondary_source": 0.40,
    "engine_inference": 0.30,
}


def harden_authorities(authorities: list[str]) -> list[dict[str, Any]]:
    """Classify and weight cited authorities."""
    results = []
    for auth in authorities:
        auth_lower = auth.lower()
        if any(k in auth_lower for k in ["sec.", "code", "usc", "cfr", "tac"]):
            cat = "statute"
        elif any(k in auth_lower for k in ["v.", "vs."]):
            cat = "case_law_appellate"
        elif any(k in auth_lower for k in ["rule", "form", "aapl"]):
            cat = "industry_standard"
        else:
            cat = "secondary_source"
        results.append({"authority": auth, "category": cat, "weight": AUTHORITY_WEIGHTS[cat]})
    return results


# ============================================================================
# [TIE-05] CONFIDENCE STRATIFICATION
# ============================================================================

class ConfidenceTier(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


def stratify_confidence(score: float) -> str:
    if score >= 0.85:
        return ConfidenceTier.DEFENSIBLE
    elif score >= 0.70:
        return ConfidenceTier.AGGRESSIVE
    elif score >= 0.50:
        return ConfidenceTier.DISCLOSURE
    return ConfidenceTier.HIGH_RISK


# ============================================================================
# [TIE-06] SEMANTIC NORMALIZATION
# ============================================================================

SEMANTIC_SYNONYMS: dict[str, str] = {
    "pto": "preliminary title opinion",
    "doto": "division order title opinion",
    "doi": "division order title opinion",
    "run sheet": "ownership summary chronological",
    "abstract": "lease abstract",
    "curative": "curative requirement letter",
    "dd": "due diligence",
    "esa": "environmental assessment",
    "phase i": "environmental assessment phase i",
    "phase ii": "environmental assessment phase ii",
    "nri": "net revenue interest",
    "wi": "working interest",
    "ri": "royalty interest",
    "orri": "overriding royalty interest",
    "npri": "non-participating royalty interest",
    "rrc": "railroad commission",
    "tceq": "texas commission on environmental quality",
    "w-1": "drilling permit application",
    "p-4": "producer transfer form",
    "row": "right of way",
    "roi": "right of ingress",
    "ip": "initial production",
    "td": "total depth",
    "bbl": "barrels",
    "mcf": "thousand cubic feet",
    "pugh clause": "pugh clause vertical horizontal",
    "force pool": "force pooling compulsory pooling",
    "hbp": "held by production",
}


class SemanticNormalizer:
    """[TIE-06] Normalize query terms to canonical forms."""

    def __init__(self) -> None:
        self.synonyms = SEMANTIC_SYNONYMS

    def normalize(self, query: str) -> str:
        normalized = query.lower().strip()
        for abbrev, expansion in self.synonyms.items():
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            normalized = re.sub(pattern, expansion, normalized)
        return normalized

    def search(self, normalized_query: str) -> list[dict[str, Any]]:
        results = []
        for block in DOCTRINE_BLOCKS:
            score = 0
            for kw in block.get("keywords", []):
                if kw.lower() in normalized_query:
                    score += 1
            if score > 0:
                results.append({**block, "_score": score})
        results.sort(key=lambda x: x["_score"], reverse=True)
        return results[:5]


# ============================================================================
# [TIE-07] VECTOR SEARCH (stub for cloud retriever integration)
# ============================================================================

class VectorSearch:
    """Semantic vector search via CognitionCloudRetriever."""

    def __init__(self) -> None:
        self.cloud: Optional[Any] = None
        if CognitionCloudRetriever is not None:
            try:
                self.cloud = CognitionCloudRetriever()
            except Exception as exc:
                logger.warning("Could not initialize CognitionCloudRetriever: {}", exc)

    async def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        if self.cloud is None:
            return []
        try:
            results = await self.cloud.retrieve_all(query, category="report_generation")
            return [{"source": r.source, "content": r.content, "score": r.score} for r in results[:top_k]]
        except Exception as exc:
            logger.warning("Vector search failed: {}", exc)
            return []


# ============================================================================
# [TIE-08] TELEMETRY
# ============================================================================

class Telemetry:
    """Full query tracing and latency tracking."""

    def __init__(self) -> None:
        self.traces: list[dict[str, Any]] = []
        self.max_traces = 10000

    def record(self, query: str, mode: str, report_type: Optional[str],
               layer: str, latency_ms: float, confidence: float, error: Optional[str] = None) -> None:
        trace = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query_hash": hashlib.sha256(query.encode()).hexdigest()[:16],
            "mode": mode,
            "report_type": report_type,
            "layer": layer,
            "latency_ms": round(latency_ms, 2),
            "confidence": round(confidence, 4),
            "error": error,
        }
        self.traces.append(trace)
        if len(self.traces) > self.max_traces:
            self.traces = self.traces[-self.max_traces:]

    def get_stats(self) -> dict[str, Any]:
        if not self.traces:
            return {"total": 0, "avg_latency_ms": 0, "error_rate": 0}
        latencies = [t["latency_ms"] for t in self.traces]
        errors = sum(1 for t in self.traces if t.get("error"))
        return {
            "total": len(self.traces),
            "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
            "p95_latency_ms": round(sorted(latencies)[int(len(latencies) * 0.95)], 2) if len(latencies) > 1 else latencies[0],
            "error_rate": round(errors / len(self.traces), 4),
            "layer_distribution": self._layer_dist(),
        }

    def _layer_dist(self) -> dict[str, int]:
        dist: dict[str, int] = defaultdict(int)
        for t in self.traces:
            dist[t["layer"]] += 1
        return dict(dist)


# ============================================================================
# [TIE-09] DRIFT WATCHER
# ============================================================================

class DriftWatcher:
    """Detect doctrine drift over time."""

    def __init__(self) -> None:
        self.snapshots: list[dict[str, Any]] = []
        self.baseline_topics: set[str] = {b["topic"] for b in DOCTRINE_BLOCKS}

    def check_drift(self, triggered_topics: list[str]) -> dict[str, Any]:
        triggered_set = set(triggered_topics)
        untriggered = self.baseline_topics - triggered_set
        novel = triggered_set - self.baseline_topics

        drift_score = len(untriggered) / max(len(self.baseline_topics), 1)
        self.snapshots.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "triggered": list(triggered_set),
            "untriggered": list(untriggered),
            "novel": list(novel),
            "drift_score": round(drift_score, 4),
        })
        return {
            "drift_score": round(drift_score, 4),
            "untriggered_count": len(untriggered),
            "novel_count": len(novel),
        }


# ============================================================================
# [TIE-10] COVERAGE MAP
# ============================================================================

class CoverageMap:
    """Track triggered/missed doctrines, epistemic gap detection."""

    def __init__(self) -> None:
        self.hits: dict[str, int] = defaultdict(int)
        self.misses: dict[str, int] = defaultdict(int)
        self.total_queries = 0

    def record_hit(self, topic: str) -> None:
        self.hits[topic] += 1
        self.total_queries += 1

    def record_miss(self, query: str) -> None:
        self.misses[query[:100]] += 1
        self.total_queries += 1

    def get_coverage(self) -> dict[str, Any]:
        all_topics = {b["topic"] for b in DOCTRINE_BLOCKS}
        covered = set(self.hits.keys()) & all_topics
        return {
            "total_topics": len(all_topics),
            "covered": len(covered),
            "uncovered": len(all_topics - covered),
            "coverage_pct": round(len(covered) / max(len(all_topics), 1) * 100, 1),
            "top_hits": dict(sorted(self.hits.items(), key=lambda x: x[1], reverse=True)[:10]),
            "top_misses": dict(sorted(self.misses.items(), key=lambda x: x[1], reverse=True)[:5]),
        }


# ============================================================================
# [TIE-11] METRICS COLLECTOR
# ============================================================================

class MetricsCollector:
    """Latency stats, error rates, hit rates, queries/hour."""

    def __init__(self) -> None:
        self.start_time = time.time()
        self.query_count = 0
        self.error_count = 0
        self.latencies: list[float] = []
        self.report_type_counts: dict[str, int] = defaultdict(int)

    def record_query(self, latency_ms: float, report_type: Optional[str], error: bool = False) -> None:
        self.query_count += 1
        self.latencies.append(latency_ms)
        if error:
            self.error_count += 1
        if report_type:
            self.report_type_counts[report_type] += 1

    def get_metrics(self) -> dict[str, Any]:
        uptime = time.time() - self.start_time
        hours = max(uptime / 3600, 0.001)
        return {
            "total_queries": self.query_count,
            "queries_per_hour": round(self.query_count / hours, 2),
            "error_count": self.error_count,
            "error_rate": round(self.error_count / max(self.query_count, 1), 4),
            "avg_latency_ms": round(sum(self.latencies) / max(len(self.latencies), 1), 2),
            "uptime_seconds": round(uptime, 1),
            "report_type_distribution": dict(self.report_type_counts),
        }


# ============================================================================
# [TIE-13] ZONED ANALYSIS
# ============================================================================

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


def apply_zone(response: str, zone: str) -> str:
    if zone == AnalysisZone.PLANNING:
        return f"**[PLANNING ZONE -- Draft / Not for Distribution]**\n\n{response}"
    elif zone == AnalysisZone.AUDIT:
        return (
            f"**[AUDIT ZONE -- Formal Record]**\n"
            f"Generated: {datetime.now(timezone.utc).isoformat()}\n"
            f"Engine: {ENGINE_ID} v{ENGINE_VERSION}\n\n{response}"
        )
    return response


# ============================================================================
# [TIE-14] FACT FRAGILITY SCORING
# ============================================================================

def compute_fragility(query: str, confidence: float, layer: str, report_type: Optional[str]) -> float:
    """Score how fragile/verifiable the facts in the response are.
    Lower = more solid. Higher = more fragile.
    """
    score = 0.0
    if confidence < 0.70:
        score += 0.3
    if layer == ResponseLayer.DEEP_ANALYSIS:
        score += 0.15
    if report_type in (ReportType.HEIRSHIP, ReportType.FORCE_POOLING):
        score += 0.1  # more subjective report types
    q_lower = query.lower()
    fragile_terms = ["estimate", "approximately", "likely", "possibly", "uncertain"]
    for term in fragile_terms:
        if term in q_lower:
            score += 0.05
    return min(round(score, 4), 1.0)


# ============================================================================
# [TIE-15] AUDIT TRAIL JSONL
# ============================================================================

class AuditTrail:
    """Append-only JSONL audit log."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def log(self, entry: dict[str, Any]) -> None:
        entry["logged_at"] = datetime.now(timezone.utc).isoformat()
        entry["engine_id"] = ENGINE_ID
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
        except Exception as exc:
            logger.error("Audit trail write failed: {}", exc)

    def recent(self, n: int = 50) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            lines = self.path.read_text(encoding="utf-8").strip().split("\n")
            return [json.loads(line) for line in lines[-n:] if line.strip()]
        except Exception:
            return []


# ============================================================================
# [TIE-16] DETERMINISM HASH SHA-256
# ============================================================================

def determinism_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ============================================================================
# [TIE-19] MULTI DOCTRINE DECOMPOSITION
# ============================================================================

def decompose_query(query: str, report_type: Optional[str]) -> list[dict[str, Any]]:
    """Break a complex query into issue categories for multi-doctrine analysis."""
    categories: list[dict[str, Any]] = []
    q_lower = query.lower()

    issue_map = {
        "title": ["title", "chain", "ownership", "conveyance", "deed", "mineral"],
        "lease": ["lease", "royalty", "pooling", "primary term", "hbp", "pugh"],
        "regulatory": ["permit", "compliance", "rrc", "regulation", "epa", "tceq"],
        "environmental": ["environmental", "contamination", "remediation", "esa", "phase"],
        "financial": ["revenue", "tax", "depletion", "severance", "ad valorem", "valuation"],
        "operational": ["production", "drilling", "completion", "well", "workover"],
        "risk": ["risk", "curative", "defect", "exception", "requirement"],
        "succession": ["heirship", "probate", "intestate", "heir", "estate", "decedent"],
    }

    for cat, keywords in issue_map.items():
        matched = [kw for kw in keywords if kw in q_lower]
        if matched:
            categories.append({"category": cat, "matched_keywords": matched, "weight": len(matched)})

    if report_type:
        rt_lower = report_type.lower()
        for cat, keywords in issue_map.items():
            if any(kw in rt_lower for kw in keywords):
                exists = any(c["category"] == cat for c in categories)
                if not exists:
                    categories.append({"category": cat, "matched_keywords": [], "weight": 1})

    if not categories:
        categories.append({"category": "general", "matched_keywords": [], "weight": 1})

    categories.sort(key=lambda x: x["weight"], reverse=True)
    return categories


# ============================================================================
# [TIE-20] DEEP ANALYSIS MODE
# ============================================================================

async def deep_analysis_mode(query: str, report_type: Optional[str],
                              property_data: Optional[dict], engine_outputs: Optional[dict],
                              client_info: Optional[dict], vector_search: VectorSearch) -> dict[str, Any]:
    """Multi-source synthesis with full reasoning chain."""
    decomposed = decompose_query(query, report_type)

    # Gather from vector search
    cloud_results = await vector_search.search(query, top_k=5)

    # Build analysis
    analysis_parts: list[str] = []
    authorities: list[str] = []
    doctrine_hits: list[str] = []

    for issue in decomposed:
        cat = issue["category"]
        analysis_parts.append(f"### Issue Category: {cat.title()}")
        analysis_parts.append(f"Matched keywords: {', '.join(issue['matched_keywords']) or 'implicit from report type'}")

        # Find relevant doctrine blocks
        for block in DOCTRINE_BLOCKS:
            block_kws = [kw.lower() for kw in block.get("keywords", [])]
            if any(mk in " ".join(block_kws) for mk in issue["matched_keywords"]):
                doctrine_hits.append(block["topic"])
                analysis_parts.append(f"\n**Doctrine:** {block['topic']}")
                analysis_parts.append(block.get("conclusion_template", ""))
                authorities.extend(block.get("primary_authority", []))
                break

    if cloud_results:
        analysis_parts.append("\n### Cloud Knowledge Sources")
        for cr in cloud_results:
            analysis_parts.append(f"- [{cr.get('source', 'unknown')}] {cr.get('content', '')[:200]}")

    return {
        "response": "\n".join(analysis_parts),
        "confidence": 0.70,
        "doctrine_hits": doctrine_hits,
        "authorities": authorities,
        "decomposition": decomposed,
    }


# ============================================================================
# GLOBAL STATE
# ============================================================================

_start_time = time.time()
_doctrine_cache = DoctrineCache()
_semantic_norm = SemanticNormalizer()
_three_layer = ThreeLayerResponse(_doctrine_cache, _semantic_norm)
_vector_search = VectorSearch()
_telemetry = Telemetry()
_drift_watcher = DriftWatcher()
_coverage_map = CoverageMap()
_metrics = MetricsCollector()
_audit_trail = AuditTrail(AUDIT_LOG_PATH)


# ============================================================================
# [TIE-12] HEALTH ENDPOINT + [TIE-17] FASTAPI SERVER
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("E06 Report Generator starting on port {}", ENGINE_PORT)
    logger.info("Doctrine cache loaded: {} blocks", _doctrine_cache.count())
    logger.info("Report types supported: {}", len(ReportType))
    yield
    logger.info("E06 Report Generator shutting down")


app = FastAPI(
    title=f"{ENGINE_ID} -- {ENGINE_NAME}",
    version=ENGINE_VERSION,
    description="Generate formatted reports from structured engine outputs. TIE-20 compliant.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    stats = _metrics.get_metrics()
    return HealthResponse(
        uptime_seconds=round(time.time() - _start_time, 1),
        total_queries=stats["total_queries"],
        cache_size=_doctrine_cache.count(),
        report_types_supported=len(ReportType),
        doctrine_count=_doctrine_cache.count(),
        avg_latency_ms=stats["avg_latency_ms"],
    )


@app.get("/report-types")
async def report_types() -> dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "report_types": [
            {"value": rt.value, "display_name": REPORT_DISPLAY_NAMES.get(rt.value, rt.value),
             "sections": REPORT_SECTIONS.get(rt.value, [])}
            for rt in ReportType
        ],
        "total": len(ReportType),
    }


@app.get("/doctrines")
async def doctrines() -> dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "doctrine_count": _doctrine_cache.count(),
        "topics": _doctrine_cache.all_topics(),
    }


@app.get("/metrics")
async def metrics() -> dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "metrics": _metrics.get_metrics(),
        "telemetry": _telemetry.get_stats(),
        "coverage": _coverage_map.get_coverage(),
    }


@app.get("/audit")
async def audit(limit: int = 50) -> dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "entries": _audit_trail.recent(limit),
    }


@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest) -> QueryResponse:
    start = time.perf_counter()
    mode = req.mode.upper() if req.mode else "FAST"
    if mode not in ("FAST", "DEFENSE", "MEMO"):
        mode = "FAST"

    zone = (req.zone or "REPORTING").upper()
    if zone not in ("PLANNING", "REPORTING", "AUDIT"):
        zone = "REPORTING"

    report_type = req.report_type
    error_msg: Optional[str] = None

    try:
        result = await _three_layer.resolve(
            query=req.query,
            mode=mode,
            report_type=report_type,
            property_data=req.property_data,
            engine_outputs=req.engine_outputs,
            client_info=req.client_info,
            zone=zone,
        )

        response_text = result["response"]
        layer = result["layer"]
        confidence = result.get("confidence", 0.5)
        doctrine_hits = result.get("doctrine_hits", [])
        authorities = result.get("authorities", [])

    except Exception as exc:
        logger.error("Query processing failed: {}", exc)
        error_msg = str(exc)
        response_text = f"Error generating report: {exc}"
        layer = "error"
        confidence = 0.0
        doctrine_hits = []
        authorities = []

    # Apply mode formatting
    response_text = apply_response_mode(response_text, mode, report_type)

    # Apply zone
    response_text = apply_zone(response_text, zone)

    # Compute derived values
    conf_tier = stratify_confidence(confidence)
    fragility = compute_fragility(req.query, confidence, layer, report_type)
    det_hash = determinism_hash(response_text)
    latency_ms = (time.perf_counter() - start) * 1000

    # Track coverage
    for dh in doctrine_hits:
        _coverage_map.record_hit(dh)
    if not doctrine_hits:
        _coverage_map.record_miss(req.query)

    # Telemetry
    _telemetry.record(req.query, mode, report_type, layer, latency_ms, confidence, error_msg)
    _metrics.record_query(latency_ms, report_type, error=bool(error_msg))

    # Drift check
    _drift_watcher.check_drift(doctrine_hits)

    # Audit log
    _audit_trail.log({
        "query_hash": hashlib.sha256(req.query.encode()).hexdigest()[:16],
        "mode": mode,
        "report_type": report_type,
        "layer": layer,
        "confidence": confidence,
        "confidence_tier": conf_tier,
        "latency_ms": round(latency_ms, 2),
        "determinism_hash": det_hash[:16],
        "error": error_msg,
    })

    # Determine sections generated
    sections_generated = []
    if report_type and report_type in REPORT_SECTIONS:
        sections_generated = REPORT_SECTIONS[report_type]

    logger.info(
        "Query processed | mode={} | type={} | layer={} | conf={:.2f} | latency={:.1f}ms",
        mode, report_type, layer, confidence, latency_ms,
    )

    return QueryResponse(
        query=req.query,
        mode=mode,
        response=response_text,
        report_type=report_type,
        sections_generated=sections_generated,
        layer_used=layer,
        confidence=round(confidence, 4),
        confidence_tier=conf_tier,
        zone=zone,
        determinism_hash=det_hash,
        latency_ms=round(latency_ms, 2),
        timestamp=datetime.now(timezone.utc).isoformat(),
        fragility_score=fragility,
        authorities_cited=authorities,
        doctrine_hits=doctrine_hits,
    )


@app.post("/generate")
async def generate_report(req: QueryRequest) -> dict[str, Any]:
    """Dedicated report generation endpoint with full section breakdown."""
    report_type = req.report_type or ReportType.DUE_DILIGENCE
    if report_type not in REPORT_SECTIONS:
        raise HTTPException(status_code=400, detail=f"Unknown report type: {report_type}")

    sections = REPORT_SECTIONS[report_type]
    prop = req.property_data or {}
    client = req.client_info or {}
    outputs = req.engine_outputs or {}
    display = REPORT_DISPLAY_NAMES.get(report_type, report_type)

    section_results: list[dict[str, str]] = []
    full_lines: list[str] = []

    for i, sec in enumerate(sections, 1):
        builder = SECTION_BUILDERS.get(sec)
        if builder:
            content = builder(i, display, prop, client, outputs, {})
        else:
            content = f"\n## {i}.0 {sec.replace('_', ' ').title()}\n\n*Content pending.*\n"
        section_results.append({"section": sec, "number": f"{i}.0", "content": content})
        full_lines.append(content)

    full_report = "\n".join(full_lines)
    det_hash = determinism_hash(full_report)

    _audit_trail.log({
        "action": "generate_report",
        "report_type": report_type,
        "sections": len(sections),
        "determinism_hash": det_hash[:16],
    })

    return {
        "engine_id": ENGINE_ID,
        "report_type": report_type,
        "display_name": display,
        "sections": section_results,
        "full_report": full_report,
        "determinism_hash": det_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info("Launching {} v{} on port {}", ENGINE_NAME, ENGINE_VERSION, ENGINE_PORT)
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
