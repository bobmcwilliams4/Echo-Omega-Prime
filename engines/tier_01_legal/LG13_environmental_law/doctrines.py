"""
LG13 Environmental Law Engine - Doctrine Cache
=================================================
Pre-compiled environmental law doctrine blocks for sub-200ms response.

Each block contains:
    - topic: Canonical identifier
    - category: Domain classification
    - summary: Expert-level explanation
    - analysis: Detailed legal analysis
    - authority: Statutory/regulatory citations
    - keywords: Search optimization terms
    - jurisdiction: Applicable jurisdiction
    - confidence: Pre-assigned confidence score
    - last_updated: ISO timestamp
    - block_hash: SHA-256 integrity hash

66+ doctrine blocks covering:
    NEPA, CAA, CWA, RCRA, CERCLA, TSCA, ESA, FIFRA, SDWA, OPA, EPCRA,
    TCEQ, RRC, Permian Basin environmental, carbon/climate, environmental
    justice, citizen suits, Phase I/II ESA, brownfield, toxic tort, permits.

Port: 8403
Engine: LG13 Environmental Law
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from typing import Any, ClassVar, Dict, FrozenSet, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# DOCTRINE BLOCK MODEL
# ============================================================================

@dataclass
class DoctrineCacheBlock:
    """A single pre-compiled doctrine block."""
    topic: str
    category: str
    summary: str
    analysis: str
    authority: str
    keywords: List[str] = dc_field(default_factory=list)
    statute: str = ""
    cfr_reference: str = ""
    jurisdiction: str = "FEDERAL"
    confidence: float = 0.90
    last_updated: str = dc_field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    block_hash: str = ""
    cross_references: List[str] = dc_field(default_factory=list)
    practice_tips: List[str] = dc_field(default_factory=list)
    penalties: str = ""
    texas_notes: str = ""

    def __post_init__(self) -> None:
        if not self.block_hash:
            content = f"{self.topic}|{self.summary}|{self.analysis}|{self.authority}"
            self.block_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "topic": self.topic,
            "category": self.category,
            "summary": self.summary,
            "analysis": self.analysis,
            "authority": self.authority,
            "keywords": self.keywords,
            "statute": self.statute,
            "cfr_reference": self.cfr_reference,
            "jurisdiction": self.jurisdiction,
            "confidence": self.confidence,
            "last_updated": self.last_updated,
            "block_hash": self.block_hash,
            "cross_references": self.cross_references,
            "practice_tips": self.practice_tips,
            "penalties": self.penalties,
            "texas_notes": self.texas_notes,
        }


# ============================================================================
# DOCTRINE CACHE INDEX
# ============================================================================

class DoctrineCacheIndex:
    """Index over doctrine blocks for O(1) lookup by topic and keyword search."""

    def __init__(self) -> None:
        self._by_topic: Dict[str, DoctrineCacheBlock] = {}
        self._by_category: Dict[str, List[str]] = {}
        self._keyword_index: Dict[str, Set[str]] = {}
        self._all_topics: List[str] = []

    def add(self, block: DoctrineCacheBlock) -> None:
        """Add a block to the index."""
        self._by_topic[block.topic] = block
        self._all_topics.append(block.topic)
        if block.category not in self._by_category:
            self._by_category[block.category] = []
        self._by_category[block.category].append(block.topic)
        for kw in block.keywords:
            kw_lower = kw.lower()
            if kw_lower not in self._keyword_index:
                self._keyword_index[kw_lower] = set()
            self._keyword_index[kw_lower].add(block.topic)

    def get(self, topic: str) -> Optional[DoctrineCacheBlock]:
        """Get a block by topic."""
        return self._by_topic.get(topic)

    def search(self, query: str, max_results: int = 10) -> List[DoctrineCacheBlock]:
        """Search blocks by keyword matching."""
        tokens = query.lower().split()
        scores: Dict[str, int] = {}
        for token in tokens:
            for kw, topics in self._keyword_index.items():
                if token in kw or kw in token:
                    for topic in topics:
                        scores[topic] = scores.get(topic, 0) + 1
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results: List[DoctrineCacheBlock] = []
        for topic, _ in ranked[:max_results]:
            block = self._by_topic.get(topic)
            if block:
                results.append(block)
        return results

    def get_by_category(self, category: str) -> List[DoctrineCacheBlock]:
        """Get all blocks in a category."""
        topics = self._by_category.get(category, [])
        return [self._by_topic[t] for t in topics if t in self._by_topic]

    @property
    def total_blocks(self) -> int:
        """Return total blocks in cache."""
        return len(self._by_topic)

    @property
    def categories(self) -> List[str]:
        """Return all categories."""
        return list(self._by_category.keys())

    @property
    def topics(self) -> List[str]:
        """Return all topics."""
        return list(self._all_topics)

    def get_stats(self) -> Dict[str, Any]:
        """Return cache statistics."""
        return {
            "total_blocks": self.total_blocks,
            "categories": len(self._by_category),
            "category_distribution": {k: len(v) for k, v in self._by_category.items()},
            "total_keywords": len(self._keyword_index),
        }


# ============================================================================
# DOCTRINE BLOCKS — 66+ blocks
# ============================================================================

DOCTRINE_BLOCKS: List[DoctrineCacheBlock] = [
    # ---- NEPA ----
    DoctrineCacheBlock(
        topic="nepa_eis",
        category="nepa",
        summary="Environmental Impact Statement (EIS) required under NEPA for major federal actions significantly affecting the human environment. The EIS must analyze the proposed action, reasonable alternatives, and their environmental consequences.",
        analysis="NEPA Section 102(2)(C) requires all federal agencies to prepare an EIS for major federal actions significantly affecting the quality of the human environment. The CEQ regulations (40 CFR 1500-1508, revised 2020/2022) govern EIS preparation. Key steps: (1) Notice of Intent (NOI) published in Federal Register, (2) public scoping to identify issues, (3) Draft EIS with alternatives analysis, (4) public comment period (minimum 45 days), (5) Final EIS addressing comments, (6) Record of Decision (ROD) after 30-day waiting period. The 'hard look' standard requires thorough investigation but NEPA is procedural — it does not mandate a particular outcome. The range of alternatives must include a no-action alternative and must rigorously explore and objectively evaluate all reasonable alternatives. Cumulative impacts analysis is required. Under NEPA Phase 1 regulations (2020), page limits of 150/300 pages and 2-year time limits were imposed. The 2022 Phase 2 rule partially restored pre-2020 provisions including cumulative effects analysis.",
        authority="42 USC 4332(C); 40 CFR 1500-1508; Robertson v. Methow Valley Citizens Council, 490 U.S. 332 (1989); Kleppe v. Sierra Club, 427 U.S. 390 (1976)",
        keywords=["nepa", "eis", "environmental impact statement", "major federal action", "alternatives", "ceq", "scoping", "record of decision", "rod", "hard look", "cumulative impact"],
        statute="42 USC 4332(C)",
        cfr_reference="40 CFR 1500-1508",
        confidence=0.95,
        cross_references=["nepa_ea", "nepa_fonsi", "nepa_catex"],
        practice_tips=[
            "Always identify the 'major federal action' trigger — federal funding, permitting, or land use is sufficient",
            "Cumulative impacts must consider past, present, and reasonably foreseeable future actions",
            "The alternatives analysis is the 'heart of the EIS' (40 CFR 1502.14)",
            "Mitigation measures can reduce impacts below significance thresholds",
        ],
        penalties="No direct penalties under NEPA; remedy is injunction to halt action pending adequate NEPA review",
    ),
    DoctrineCacheBlock(
        topic="nepa_ea",
        category="nepa",
        summary="Environmental Assessment (EA) is a concise NEPA document used to determine whether an EIS is required. If the EA finds no significant impact, the agency issues a FONSI.",
        analysis="An EA under 40 CFR 1501.5 is prepared when a federal agency action does not clearly require an EIS or qualify for a categorical exclusion. The EA provides sufficient evidence and analysis to determine significance. It must briefly discuss the need for the proposed action, alternatives, environmental impacts, and list agencies and persons consulted. If the EA demonstrates no significant impact, the agency issues a Finding of No Significant Impact (FONSI). If significant impacts are identified, the agency must prepare an EIS. The 'significance' determination considers both context (affected region, interests, locality) and intensity factors including unique characteristics, controversy, uncertainty, precedent, cumulative significance, endangered species effects, and violations of environmental laws. Mitigated FONSIs are permissible where mitigation measures reduce impacts below the significance threshold, but the mitigation must be binding and enforceable.",
        authority="40 CFR 1501.5; 40 CFR 1501.3 (significance); Grand Canyon Trust v. FAA, 290 F.3d 339 (D.C. Cir. 2002)",
        keywords=["nepa", "ea", "environmental assessment", "fonsi", "significance", "mitigated fonsi", "categorical exclusion"],
        statute="42 USC 4332",
        cfr_reference="40 CFR 1501.5",
        confidence=0.93,
        cross_references=["nepa_eis", "nepa_fonsi"],
        practice_tips=[
            "Review the 10 intensity factors in 40 CFR 1501.3(b) carefully when assessing significance",
            "Mitigated FONSIs require enforceable mitigation commitments, not aspirational measures",
            "EAs are increasingly scrutinized; ensure the analysis is proportionate to the action's impacts",
        ],
    ),
    DoctrineCacheBlock(
        topic="nepa_fonsi",
        category="nepa",
        summary="Finding of No Significant Impact (FONSI) issued after an EA determines the proposed federal action will not have significant environmental effects.",
        analysis="A FONSI under 40 CFR 1501.6 documents the agency's determination that a proposed action will not have significant environmental effects, based on the EA analysis. The FONSI must include the EA or a summary of it, note any related NEPA documents, and be made available to the public. A FONSI may not be issued if the proposed action would significantly affect the environment — in that case, an EIS must be prepared. Mitigated FONSIs are permitted where enforceable mitigation reduces impacts below significance. Agencies must monitor and enforce mitigation commitments in mitigated FONSIs. Judicial review applies the 'arbitrary and capricious' standard: courts ask whether the agency took a 'hard look' at the potential impacts.",
        authority="40 CFR 1501.6; Sierra Club v. U.S. DOT, 753 F.2d 120 (D.C. Cir. 1985)",
        keywords=["fonsi", "finding of no significant impact", "mitigated fonsi", "nepa", "significance determination"],
        statute="42 USC 4332",
        cfr_reference="40 CFR 1501.6",
        confidence=0.92,
        cross_references=["nepa_ea", "nepa_eis"],
    ),
    DoctrineCacheBlock(
        topic="nepa_catex",
        category="nepa",
        summary="Categorical Exclusions (CatEx/CATEX) are categories of actions that normally do not individually or cumulatively have significant environmental effects and are excluded from NEPA EIS/EA requirements.",
        analysis="Under 40 CFR 1501.4, agencies identify categorical exclusions in their NEPA procedures. A CATEX applies unless extraordinary circumstances exist (e.g., impacts to endangered species, wetlands, historic properties, or hazardous waste sites). Each federal agency publishes its own list of CATEXs. The FAST Act (2015) and IIJA (2021) expanded CATEXs for transportation and infrastructure projects. No environmental document is prepared, but the agency must verify no extraordinary circumstances apply. Documentation requirements vary by agency — some require a brief checklist, others require no documentation. CATEXs are vulnerable to challenge if the agency fails to consider extraordinary circumstances or applies a CATEX to an action outside its scope.",
        authority="40 CFR 1501.4; 42 USC 4336e (IIJA CATEXs)",
        keywords=["catex", "categorical exclusion", "extraordinary circumstances", "nepa", "ceq", "fast act", "iija"],
        statute="42 USC 4332",
        cfr_reference="40 CFR 1501.4",
        confidence=0.90,
        cross_references=["nepa_ea", "nepa_eis"],
    ),

    # ---- CLEAN AIR ACT ----
    DoctrineCacheBlock(
        topic="caa_naaqs",
        category="air_quality",
        summary="National Ambient Air Quality Standards (NAAQS) set by EPA under CAA Section 109 for six criteria pollutants to protect public health (primary) and welfare (secondary).",
        analysis="EPA must establish NAAQS for criteria pollutants under CAA Section 109: (1) ozone, (2) particulate matter (PM2.5/PM10), (3) carbon monoxide, (4) sulfur dioxide, (5) nitrogen dioxide, (6) lead. Primary standards protect public health with an adequate margin of safety. Secondary standards protect public welfare (crops, vegetation, buildings, visibility). States must adopt State Implementation Plans (SIPs) to attain NAAQS. Areas failing to meet NAAQS are designated 'nonattainment' and subject to stricter requirements including Lowest Achievable Emission Rate (LAER) for new sources and reasonable further progress demonstrations. Attainment areas are subject to Prevention of Significant Deterioration (PSD). The current ozone NAAQS is 0.070 ppm (8-hour); PM2.5 annual is 12.0 ug/m3. NAAQS review is required every 5 years. The Permian Basin region has ozone concerns due to oil/gas activity VOC and NOx emissions.",
        authority="42 USC 7409; Whitman v. American Trucking Assns., 531 U.S. 457 (2001); 40 CFR Part 50",
        keywords=["naaqs", "criteria pollutant", "ozone", "particulate matter", "pm2.5", "attainment", "nonattainment", "sip", "air quality"],
        statute="42 USC 7409",
        cfr_reference="40 CFR Part 50",
        confidence=0.95,
        cross_references=["caa_title_v", "caa_nsr_psd", "caa_nsps"],
        texas_notes="Permian Basin counties monitored for ozone; TCEQ maintains Texas SIP; Ector/Midland counties near marginal nonattainment for ozone",
        penalties="Up to $109,024/day/violation (2024 adjusted); criminal penalties for knowing violations",
    ),
    DoctrineCacheBlock(
        topic="caa_title_v",
        category="air_quality",
        summary="Title V operating permits required for major stationary sources under CAA, consolidating all air quality requirements into a single, enforceable permit renewed every 5 years.",
        analysis="CAA Title V (42 USC 7661-7661f) requires major sources to obtain an operating permit that consolidates all applicable air quality requirements. Major source thresholds: 100 tpy of any criteria pollutant, 10 tpy of a single HAP, or 25 tpy of combined HAPs (lower thresholds in nonattainment areas). The permit must include emission limits, monitoring requirements, recordkeeping, reporting, and compliance certification obligations. Applications must include a compliance plan and compliance schedule. Permits are effective for up to 5 years. EPA and the public have review opportunities. The 'permit shield' provides that compliance with permit conditions is deemed compliance with applicable requirements (if specifically identified in the permit). States administer Title V programs with EPA oversight. In Texas, TCEQ administers the Title V program under 30 TAC Chapter 122.",
        authority="42 USC 7661-7661f; 40 CFR Part 70 (state programs); 40 CFR Part 71 (EPA-administered)",
        keywords=["title v", "operating permit", "major source", "caa", "air permit", "compliance certification", "permit shield"],
        statute="42 USC 7661",
        cfr_reference="40 CFR Part 70",
        confidence=0.94,
        cross_references=["caa_naaqs", "caa_nsr_psd", "caa_nsps", "caa_neshap"],
        texas_notes="TCEQ administers Title V under 30 TAC Chapter 122; Texas-specific exemptions include standard permits and permits by rule for smaller sources",
        penalties="Up to $109,024/day for operating without or violating a Title V permit",
    ),
    DoctrineCacheBlock(
        topic="caa_nsr_psd",
        category="air_quality",
        summary="New Source Review (NSR) and Prevention of Significant Deterioration (PSD) programs require preconstruction permits for new or modified major stationary sources of air pollution.",
        analysis="NSR encompasses two programs: PSD for attainment areas (40 CFR 52.21) and Nonattainment NSR for nonattainment areas (CAA Part D). PSD requires new major sources or major modifications to install Best Available Control Technology (BACT) and demonstrate compliance with NAAQS increments and ambient standards. The PSD applicant must conduct air quality monitoring, analyze impacts, and consider alternatives. In nonattainment areas, new sources must achieve Lowest Achievable Emission Rate (LAER) and obtain emission offsets. Major modification triggers are complicated: the project must result in both an emissions increase from the project (Step 1) and a net emissions increase at the source (Step 2, netting). The 2002 NSR Reform Rule introduced plant-wide applicability limits (PALs) and other flexibility mechanisms. Texas implements NSR through the TCEQ air permitting program (30 TAC Chapter 116). The definition of 'modification' under NSR vs. NSPS vs. Title V can differ, creating compliance traps.",
        authority="42 USC 7470-7479 (PSD); 42 USC 7501-7515 (NA-NSR); 40 CFR 52.21; EPA v. EME Homer City, 572 U.S. 489 (2014)",
        keywords=["nsr", "psd", "new source review", "prevention of significant deterioration", "bact", "laer", "offset", "modification", "major source"],
        statute="42 USC 7470-7515",
        cfr_reference="40 CFR 52.21",
        confidence=0.93,
        cross_references=["caa_naaqs", "caa_title_v"],
        texas_notes="TCEQ NSR permitting under 30 TAC Chapter 116; Texas has unique 'standard permit' and 'permit by rule' pathways for smaller sources",
    ),
    DoctrineCacheBlock(
        topic="caa_nsps",
        category="air_quality",
        summary="New Source Performance Standards (NSPS) under CAA Section 111 set emission standards for categories of new stationary sources reflecting the best demonstrated technology.",
        analysis="CAA Section 111 directs EPA to establish NSPS for categories of stationary sources that cause or contribute significantly to air pollution. NSPS apply to new sources (constructed or modified after the standard is proposed). Standards reflect the best system of emission reduction (BSER) considering cost, energy, and environmental impacts. Important NSPS categories for oil and gas include Subpart OOOO (2012) and Subpart OOOOa (2016) covering VOC and methane emissions from oil and gas production, processing, transmission, and storage. The 2024 OOOOb/OOOOc rules significantly expanded methane regulation across the oil and gas sector, including existing sources. NSPS apply independently of Title V and NSR — a source can trigger NSPS without being a major source. In the Permian Basin, NSPS OOOO/OOOOa/OOOOb are critical for well completion, pneumatic controller, compressor, and storage vessel emissions.",
        authority="42 USC 7411; 40 CFR Part 60 Subparts OOOO, OOOOa, OOOOb, OOOOc",
        keywords=["nsps", "new source performance standards", "section 111", "oooo", "ooooa", "methane", "oil and gas", "bser"],
        statute="42 USC 7411",
        cfr_reference="40 CFR Part 60",
        confidence=0.93,
        cross_references=["caa_naaqs", "caa_title_v", "permian_methane"],
        texas_notes="OOOOb/OOOOc methane rules significantly impact Permian Basin operators; TCEQ enforcement complements EPA oversight",
    ),

    # ---- CLEAN WATER ACT ----
    DoctrineCacheBlock(
        topic="cwa_npdes",
        category="water_quality",
        summary="NPDES permits under CWA Section 402 regulate the discharge of pollutants from point sources into waters of the United States.",
        analysis="CWA Section 402 (33 USC 1342) establishes the National Pollutant Discharge Elimination System. Any discharge of a pollutant from a point source to waters of the US requires an NPDES permit. Permits contain technology-based effluent limitations (BPT, BAT, BCT) and may include water quality-based limitations where technology-based limits are insufficient to meet water quality standards. Permits require self-monitoring, Discharge Monitoring Reports (DMRs), and compliance with narrative and numeric limits. Violation of an NPDES permit is a violation of the CWA. Most states have delegated NPDES authority (Texas administers TPDES). Key issues: (1) definition of 'point source' is broad, (2) 'discharge of a pollutant' requires an addition from an outside source, (3) 'waters of the United States' (WOTUS) definition is contested, (4) permit shield protects permittees complying with permit terms. Sackett v. EPA (2023) narrowed WOTUS to waters with a continuous surface connection to traditionally navigable waters.",
        authority="33 USC 1342; 40 CFR Parts 122-125; Sackett v. EPA, 598 U.S. 651 (2023); County of Maui v. Hawaii Wildlife Fund, 590 U.S. 165 (2020)",
        keywords=["npdes", "discharge permit", "point source", "effluent", "water quality", "cwa", "wotus", "dmr", "bat", "bpt"],
        statute="33 USC 1342",
        cfr_reference="40 CFR Parts 122-125",
        confidence=0.95,
        cross_references=["cwa_404", "cwa_tmdl", "cwa_wetlands"],
        texas_notes="Texas administers TPDES under delegation from EPA; TCEQ is the permitting authority (30 TAC Chapter 305)",
        penalties="Civil: up to $64,618/day/violation; Criminal: negligent violations up to $50,000/day; knowing violations up to $100,000/day and/or imprisonment",
    ),
    DoctrineCacheBlock(
        topic="cwa_404",
        category="water_quality",
        summary="CWA Section 404 regulates the discharge of dredged or fill material into waters of the United States, including wetlands, administered jointly by USACE and EPA.",
        analysis="Section 404 (33 USC 1344) requires a permit from the Army Corps of Engineers for any discharge of dredged or fill material into waters of the US, including wetlands. EPA provides oversight and can veto USACE permits under Section 404(c). The 404(b)(1) Guidelines (40 CFR 230) require the permit applicant to demonstrate: (1) no practicable alternative exists that would have less adverse impact (the LEDPA requirement), (2) the activity will not cause significant degradation, (3) appropriate mitigation is provided. Nationwide Permits (NWPs) authorize activities with minimal impacts (currently NWP 1-57). Individual permits require full environmental review. Compensatory mitigation follows the 2008 Mitigation Rule (33 CFR 332) with preference order: mitigation banking > in-lieu fee > permittee-responsible. Post-Sackett, the scope of Section 404 jurisdiction is significantly narrowed — wetlands must have a continuous surface connection to traditionally navigable waters.",
        authority="33 USC 1344; 40 CFR Part 230; 33 CFR Parts 320-332; Rapanos v. United States, 547 U.S. 715 (2006); Sackett v. EPA, 598 U.S. 651 (2023)",
        keywords=["section 404", "dredge and fill", "wetlands", "usace", "corps of engineers", "nationwide permit", "mitigation banking", "ledpa"],
        statute="33 USC 1344",
        cfr_reference="40 CFR Part 230; 33 CFR 320-332",
        confidence=0.94,
        cross_references=["cwa_npdes", "cwa_wetlands", "esa_section_7"],
        penalties="Civil: up to $64,618/day; Criminal: knowing violations; USACE can issue restoration orders",
    ),
    DoctrineCacheBlock(
        topic="cwa_tmdl",
        category="water_quality",
        summary="Total Maximum Daily Loads (TMDLs) establish the maximum amount of a pollutant that a water body can receive while meeting water quality standards, allocated among point and nonpoint sources.",
        analysis="CWA Section 303(d) requires states to identify impaired waters that do not meet water quality standards and develop TMDLs for those waters. A TMDL establishes: waste load allocations (WLA) for point sources, load allocations (LA) for nonpoint sources, and a margin of safety (MOS). TMDLs must account for seasonal variation and a margin of safety. EPA must approve or disapprove state-submitted TMDLs and may establish TMDLs if the state fails. TMDLs are translated into NPDES permit limits for point sources. The relationship between TMDLs and NPDES permits is a key compliance nexus. Courts have held that TMDLs are not self-executing — they must be implemented through permitting, land use controls, and voluntary BMPs for nonpoint sources.",
        authority="33 USC 1313(d); 40 CFR 130.7; Pronsolino v. Nastri, 291 F.3d 1123 (9th Cir. 2002)",
        keywords=["tmdl", "total maximum daily load", "impaired waters", "303d", "water quality standards", "waste load allocation"],
        statute="33 USC 1313(d)",
        cfr_reference="40 CFR 130.7",
        confidence=0.92,
        cross_references=["cwa_npdes", "cwa_wetlands"],
    ),

    # ---- RCRA ----
    DoctrineCacheBlock(
        topic="rcra_subtitle_c",
        category="hazardous_waste",
        summary="RCRA Subtitle C (42 USC 6921-6939g) establishes the 'cradle-to-grave' regulatory framework for hazardous waste generation, transportation, treatment, storage, and disposal.",
        analysis="RCRA Subtitle C creates a comprehensive hazardous waste management system. Key elements: (1) Waste Identification: waste must be 'solid waste' and then either 'listed' (F, K, U, P lists) or 'characteristic' (ignitability, corrosivity, reactivity, toxicity via TCLP). (2) Generator Requirements: generators classified as LQG (>1,000 kg/month), SQG (100-1,000 kg/month), or VSQG (<100 kg/month) with corresponding requirements for accumulation time, container management, manifesting, emergency planning, and biennial reporting. (3) Transporter Requirements: EPA ID number, manifest compliance, spill response. (4) TSDF Requirements: Part B permit, groundwater monitoring, closure/post-closure plans, financial assurance, corrective action. Key rules: mixture rule (hazardous waste mixed with solid waste = hazardous), derived-from rule (residue from treating hazardous waste = hazardous), contained-in policy. Land Disposal Restrictions (LDR) prohibit land disposal of untreated hazardous waste. Exclusions include oil/gas exploration and production wastes (E&P exemption), household hazardous waste, and conditionally exempt materials.",
        authority="42 USC 6921-6939g; 40 CFR Parts 260-268; American Chemistry Council v. EPA (D.C. Cir. 2021)",
        keywords=["rcra", "hazardous waste", "subtitle c", "generator", "tsdf", "manifest", "listed waste", "characteristic waste", "ldr", "cradle to grave"],
        statute="42 USC 6921-6939g",
        cfr_reference="40 CFR Parts 260-268",
        confidence=0.95,
        cross_references=["rcra_corrective_action", "rcra_ust", "cercla_prp"],
        texas_notes="TCEQ administers authorized RCRA program in Texas (30 TAC Chapters 335-336); E&P waste exemption critical for Permian Basin operators",
        penalties="Civil: up to $70,117/day/violation; Criminal: knowing violations up to $50,000/day and/or 2 years; knowing endangerment up to $250,000 and/or 15 years",
    ),
    DoctrineCacheBlock(
        topic="rcra_ust",
        category="hazardous_waste",
        summary="RCRA Subtitle I regulates underground storage tanks (USTs) containing petroleum or hazardous substances, requiring leak detection, release reporting, corrective action, and financial responsibility.",
        analysis="RCRA Subtitle I (42 USC 6991-6991m) and EPA regulations (40 CFR Part 280) establish comprehensive UST management requirements. Key requirements: (1) Registration with designated state agency, (2) Leak detection (automatic tank gauging, interstitial monitoring, or SIR), (3) Corrosion protection (cathodic protection, fiberglass, or composite), (4) Spill/overfill prevention (catchment basins, auto shutoff), (5) Release reporting within 24 hours, (6) Corrective action for confirmed releases (initial response, site assessment, cleanup), (7) Financial responsibility ($1M per occurrence, $2M aggregate for petroleum). The 2015 UST rule strengthened requirements including operator training, periodic testing, and secondary containment for new installations. LUST (Leaking UST) cleanups are a major environmental program — EPA's LUST Trust Fund assists with cleanup of petroleum releases. In Texas, TCEQ's Petroleum Storage Tank (PST) program administers the UST program with the Leaking Petroleum Storage Tank (LPST) remediation fund providing reimbursement for eligible cleanups.",
        authority="42 USC 6991-6991m; 40 CFR Part 280; 30 TAC Chapter 334 (Texas)",
        keywords=["ust", "underground storage tank", "leak detection", "lust", "petroleum", "corrective action", "financial responsibility", "subtitle i"],
        statute="42 USC 6991",
        cfr_reference="40 CFR Part 280",
        confidence=0.93,
        cross_references=["rcra_subtitle_c", "tceq_vcp"],
        texas_notes="TCEQ PST program under 30 TAC Chapter 334; LPST remediation fund available for eligible petroleum cleanup costs",
        penalties="Civil: up to $70,117/day/violation; failure to report releases carries enhanced penalties",
    ),

    # ---- CERCLA / SUPERFUND ----
    DoctrineCacheBlock(
        topic="cercla_prp_liability",
        category="superfund",
        summary="CERCLA imposes strict, joint and several, retroactive liability on four categories of PRPs for cleanup costs at contaminated sites: current owners/operators, past owners/operators at time of disposal, arrangers, and transporters.",
        analysis="CERCLA Section 107(a) (42 USC 9607) establishes liability for response costs and natural resource damages against four PRP categories: (1) current owners/operators of a facility, (2) owners/operators at the time of disposal, (3) persons who arranged for disposal/treatment (arrangers), (4) transporters who selected the disposal site. Liability is strict (no fault required), joint and several (each PRP potentially liable for 100% of costs), and retroactive (pre-CERCLA conduct creates liability). In Burlington Northern (2009), SCOTUS held that joint and several liability is not mandatory — if there is a reasonable basis for apportionment, divisible liability may apply. The 'arranger' liability requires an intent to dispose (not merely selling a useful product). Defenses under Section 107(b) are narrow: act of God, act of war, third party (no contractual relationship), or combinations. The 2002 Brownfields Amendments added innocent landowner, bona fide prospective purchaser (BFPP), and contiguous property owner defenses. De minimis settlements available under Section 122(g). Contribution claims under Section 113(f) allow PRPs who settle to seek contribution from non-settling PRPs.",
        authority="42 USC 9607; Burlington Northern & Santa Fe Ry. v. United States, 556 U.S. 599 (2009); United States v. Bestfoods, 524 U.S. 51 (1998); United States v. Atlantic Research Corp., 551 U.S. 128 (2007)",
        keywords=["cercla", "superfund", "prp", "strict liability", "joint and several", "retroactive", "arranger", "transporter", "cost recovery", "contribution", "107", "113"],
        statute="42 USC 9607",
        cfr_reference="40 CFR Part 300",
        confidence=0.96,
        cross_references=["cercla_ncp", "cercla_brownfield", "cercla_defenses"],
        practice_tips=[
            "Always assess BFPP defense early — it requires AAI before acquisition",
            "Burlington Northern divisibility argument can dramatically reduce exposure",
            "Contribution protection under 113(f)(2) is a major incentive for early settlement",
            "Insurance archaeology — check historical CGL policies for coverage",
        ],
        penalties="Cleanup costs can range from $1M to $500M+; treble damages for failure to comply with EPA order under 106(b)",
    ),
    DoctrineCacheBlock(
        topic="cercla_ncp",
        category="superfund",
        summary="The National Contingency Plan (NCP) at 40 CFR Part 300 establishes the framework for hazardous substance response, including the Superfund cleanup process from discovery through deletion from the NPL.",
        analysis="The NCP (40 CFR Part 300) is the operational blueprint for CERCLA response. Key phases: (1) Preliminary Assessment (PA) — initial evaluation using available information, (2) Site Inspection (SI) — targeted sampling to confirm contamination, (3) Hazard Ranking System (HRS) scoring — if score ≥28.5, site proposed for NPL, (4) NPL listing — makes site eligible for Superfund-financed remedial action, (5) Remedial Investigation/Feasibility Study (RI/FS) — characterize contamination and evaluate alternatives, (6) Proposed Plan — preferred remedy with public comment, (7) Record of Decision (ROD) — final remedy selection with nine criteria (threshold: protectiveness, compliance with ARARs; balancing: long-term effectiveness, reduction of toxicity/mobility/volume, short-term effectiveness, implementability, cost; modifying: state acceptance, community acceptance), (8) Remedial Design/Remedial Action (RD/RA), (9) Operation & Maintenance, (10) Five-Year Reviews, (11) Site deletion from NPL. Private parties conducting cleanups must be 'consistent with' the NCP to recover costs under Section 107.",
        authority="40 CFR Part 300; 42 USC 9604-9605; Ohio v. EPA, 997 F.2d 1520 (D.C. Cir. 1993)",
        keywords=["ncp", "national contingency plan", "npl", "hrs", "ri/fs", "rod", "remedial action", "superfund", "remedy selection", "nine criteria"],
        statute="42 USC 9604-9605",
        cfr_reference="40 CFR Part 300",
        confidence=0.94,
        cross_references=["cercla_prp_liability", "cercla_arar", "cercla_brownfield"],
    ),
    DoctrineCacheBlock(
        topic="cercla_brownfield",
        category="superfund",
        summary="The 2002 Brownfields Amendments to CERCLA created liability protections for prospective purchasers and facilitated redevelopment of contaminated properties through grants, tax incentives, and defense provisions.",
        analysis="The Small Business Liability Relief and Brownfields Revitalization Act (2002) amended CERCLA to encourage brownfield redevelopment by: (1) creating the BFPP defense (Section 101(40)) for purchasers who know of contamination but conduct AAI and do not impede cleanup, (2) establishing contiguous property owner protections, (3) strengthening innocent landowner defense, (4) providing EPA brownfield grants for assessment ($200K), cleanup ($500K per site), and revolving loan funds, (5) requiring AAI per 40 CFR Part 312 (codified ASTM E1527 as the standard), (6) limiting EPA enforcement at sites addressed under state voluntary cleanup programs (VCPs), (7) providing liability protections for state and local governments acquiring contaminated property involuntarily. The BFPP must: conduct AAI prior to acquisition, exercise appropriate care post-acquisition, comply with institutional controls, provide cooperation to EPA, and not be affiliated with a PRP. State VCPs like Texas TCEQ's Voluntary Cleanup Program (VCP) provide 'comfort letters' and certificates of completion that, combined with BFPP protections, significantly reduce liability risk for developers.",
        authority="42 USC 9601(40), 9607(r); 40 CFR Part 312; ASTM E1527-21",
        keywords=["brownfield", "bfpp", "bona fide prospective purchaser", "all appropriate inquiries", "aai", "voluntary cleanup", "redevelopment", "innocent landowner"],
        statute="42 USC 9601(40), 9607(r)",
        cfr_reference="40 CFR Part 312",
        confidence=0.93,
        cross_references=["cercla_prp_liability", "phase_i_esa", "tceq_vcp"],
        texas_notes="TCEQ VCP under Texas Health & Safety Code Chapter 361, Subchapter S; certificates of completion provide state-level liability release",
    ),

    # ---- TSCA ----
    DoctrineCacheBlock(
        topic="tsca_chemical_review",
        category="toxic_substances",
        summary="TSCA as amended by the Lautenberg Act (2016) requires EPA to evaluate existing chemicals for risk and regulate those posing unreasonable risk, while also reviewing new chemicals before manufacture.",
        analysis="The Frank R. Lautenberg Chemical Safety for the 21st Century Act (2016) significantly reformed TSCA. Key provisions: (1) EPA must prioritize chemicals as high or low priority for risk evaluation, (2) risk evaluations assess whether a chemical presents unreasonable risk under conditions of use (without considering costs), (3) if unreasonable risk found, EPA must promulgate risk management rules within prescribed deadlines, (4) new chemicals require premanufacture notice (PMN) 90 days before manufacture — EPA must affirmatively find the chemical is not likely to present unreasonable risk, (5) TSCA preempts some state chemical regulations but preserves state authority in many areas. EPA has completed risk evaluations for 10 initial chemicals including asbestos, methylene chloride, TCE, and PCE. The TSCA inventory lists approximately 86,000 chemicals. Chemical Data Reporting (CDR) requires manufacturers/importers to report production volumes and use information every 4 years.",
        authority="15 USC 2601-2697; Lautenberg Act (P.L. 114-182, 2016); 40 CFR Parts 700-799",
        keywords=["tsca", "toxic substances", "lautenberg", "chemical review", "pmn", "premanufacture", "risk evaluation", "unreasonable risk", "chemical regulation"],
        statute="15 USC 2601-2697",
        cfr_reference="40 CFR Parts 700-799",
        confidence=0.92,
        cross_references=["tsca_pcb", "tsca_asbestos", "tsca_pfas"],
    ),
    DoctrineCacheBlock(
        topic="tsca_pfas",
        category="toxic_substances",
        summary="PFAS (per- and polyfluoroalkyl substances) are an emerging regulatory priority under TSCA, SDWA, CERCLA, and state laws, with EPA establishing MCLs, CERCLA hazardous substance designations, and TSCA risk evaluations.",
        analysis="PFAS regulation is rapidly evolving across multiple federal statutes: (1) SDWA: EPA finalized MCLs for PFOA (4 ppt) and PFOS (4 ppt) in April 2024, plus limits for PFHxS, PFNA, HFPO-DA, and PFAS mixtures — compliance by 2029. (2) CERCLA: EPA designated PFOA and PFOS as hazardous substances in April 2024, enabling Superfund enforcement and cost recovery. (3) TSCA: EPA using Section 8(a)(7) reporting rule requiring manufacturers to report PFAS production and use data. (4) CWA: EPA developing effluent guidelines for PFAS discharges. (5) RCRA: EPA considering listing PFAS wastes. State regulation varies widely — many states have adopted PFAS standards more stringent than federal. Key sources include AFFF firefighting foam, industrial processes, and consumer products. Treatment technologies include granular activated carbon (GAC), ion exchange, high-pressure membranes, and destruction technologies. Liability exposure is enormous — the American Chemistry Council estimates $400B+ in potential cleanup costs nationwide.",
        authority="15 USC 2607(a)(7) (TSCA 8(a)(7)); 42 USC 300f (SDWA MCLs); 42 USC 9601 (CERCLA designation); 89 FR 22390 (2024 PFAS MCL rule)",
        keywords=["pfas", "pfoa", "pfos", "forever chemicals", "mcl", "drinking water", "cercla designation", "firefighting foam", "afff"],
        statute="Multiple (TSCA, SDWA, CERCLA, CWA)",
        cfr_reference="40 CFR 141 (SDWA); 40 CFR 302 (CERCLA)",
        confidence=0.91,
        cross_references=["sdwa_mcl", "cercla_prp_liability", "tsca_chemical_review"],
        texas_notes="TCEQ monitoring PFAS in public water systems; no state-specific PFAS standards yet but compliance with federal MCLs required by 2029",
    ),

    # ---- ESA ----
    DoctrineCacheBlock(
        topic="esa_section_7",
        category="endangered_species",
        summary="ESA Section 7 requires federal agencies to consult with USFWS/NMFS to ensure their actions are not likely to jeopardize listed species or adversely modify critical habitat.",
        analysis="Section 7 consultation is triggered when a federal agency action 'may affect' a listed species or critical habitat. Informal consultation occurs when the action is 'not likely to adversely affect' — USFWS/NMFS concurrence letter concludes consultation. Formal consultation occurs when the action is 'likely to adversely affect' — results in a Biological Opinion (BiOp). The BiOp determines: (1) jeopardy/no jeopardy to the species, (2) adverse modification of critical habitat, (3) if no jeopardy, an Incidental Take Statement (ITS) with take limits, reasonable and prudent measures, and terms and conditions. If jeopardy is found, USFWS/NMFS must suggest reasonable and prudent alternatives (RPAs) that avoid jeopardy. The 'action area' encompasses all areas that may be directly or indirectly affected. Section 7 applies to federal permits (including NPDES, Section 404, FERC licenses), federal funding, and federal lands management. Failure to consult can result in injunctive relief. The 2019 ESA regulatory revisions modified the definition of 'destruction or adverse modification' of critical habitat; the 2024 rules further refined these provisions.",
        authority="16 USC 1536; 50 CFR Part 402; Tennessee Valley Authority v. Hill, 437 U.S. 153 (1978); Nat'l Ass'n of Home Builders v. Defenders of Wildlife, 551 U.S. 644 (2007)",
        keywords=["esa", "section 7", "consultation", "biological opinion", "jeopardy", "incidental take", "critical habitat", "usfws", "nmfs"],
        statute="16 USC 1536",
        cfr_reference="50 CFR Part 402",
        confidence=0.94,
        cross_references=["esa_section_9", "esa_section_10", "esa_critical_habitat"],
        texas_notes="Key Texas listed species for Permian Basin: dunes sagebrush lizard (Sceloporus arenicolus), Texas hornshell mussel, various bat species",
    ),

    # ---- FIFRA ----
    DoctrineCacheBlock(
        topic="fifra_registration",
        category="pesticides",
        summary="FIFRA requires all pesticides sold or distributed in the US to be registered by EPA, with the label constituting a legally binding document governing use, application rates, and restrictions.",
        analysis="FIFRA (7 USC 136-136y) establishes a registration system where manufacturers must demonstrate their pesticide will not cause 'unreasonable adverse effects on the environment' considering economic, social, and environmental costs and benefits. Key provisions: (1) Registration requires extensive data on toxicology, ecological effects, environmental fate, residue chemistry, and product performance. (2) The label is the law — use inconsistent with labeling is a federal violation. (3) Reregistration and Registration Review ensure periodic reassessment (15-year cycle). (4) FQPA (1996) added a 10x safety factor for children, aggregate exposure assessment, and cumulative risk assessment for common mechanism pesticides. (5) Classification as general use or restricted use (RUP) — RUPs require certified applicator. (6) Emergency exemptions (Section 18) allow unregistered uses in emergencies. (7) FIFRA preempts local pesticide regulation but states can impose stricter labeling requirements. (8) Worker Protection Standard (40 CFR 170) protects agricultural workers.",
        authority="7 USC 136-136y; 40 CFR Parts 150-189; Ruckelshaus v. Monsanto Co., 467 U.S. 986 (1984)",
        keywords=["fifra", "pesticide", "registration", "label", "restricted use", "fqpa", "tolerance", "applicator", "worker protection"],
        statute="7 USC 136",
        cfr_reference="40 CFR Parts 150-189",
        confidence=0.92,
        cross_references=["esa_section_7"],
    ),

    # ---- SDWA ----
    DoctrineCacheBlock(
        topic="sdwa_mcl",
        category="drinking_water",
        summary="SDWA requires EPA to set enforceable Maximum Contaminant Levels (MCLs) for public water systems to protect human health, with states responsible for implementation and enforcement.",
        analysis="SDWA (42 USC 300f-300j) establishes the framework for drinking water protection. EPA sets National Primary Drinking Water Regulations (NPDWRs) including MCLs and treatment techniques. MCLs are set as close as feasible to Maximum Contaminant Level Goals (MCLGs) — MCLGs are health-based and non-enforceable, while MCLs consider feasibility and cost. The 1996 amendments added cost-benefit analysis requirements. Key regulations include the Lead and Copper Rule (revised 2024), Surface Water Treatment Rules, Disinfection Byproducts Rules, and the landmark 2024 PFAS rule (PFOA/PFOS MCL of 4 ppt). Public water systems (PWS) must monitor, treat, and report compliance. States with primacy administer the SDWA program. The Unregulated Contaminant Monitoring Rule (UCMR) identifies contaminants for potential future regulation. State-specific standards may be more stringent than federal MCLs. Texas TCEQ administers the SDWA program through 30 TAC Chapter 290.",
        authority="42 USC 300f-300j; 40 CFR Parts 141-149; 89 FR 22390 (2024 PFAS rule)",
        keywords=["sdwa", "mcl", "drinking water", "maximum contaminant level", "public water system", "mclg", "lead copper rule", "pfas"],
        statute="42 USC 300f-300j",
        cfr_reference="40 CFR Parts 141-149",
        confidence=0.93,
        cross_references=["sdwa_uic", "tsca_pfas"],
        texas_notes="TCEQ has SDWA primacy; 30 TAC Chapter 290; some Texas MCLs may differ from federal",
    ),
    DoctrineCacheBlock(
        topic="sdwa_uic",
        category="drinking_water",
        summary="SDWA's Underground Injection Control (UIC) program regulates injection wells to protect underground sources of drinking water, with six well classes and state/federal administration.",
        analysis="The UIC program (42 USC 300h; 40 CFR Parts 144-148) regulates underground injection to prevent contamination of USDWs (underground sources of drinking water). Six well classes: Class I (industrial/municipal waste — deep wells below USDW), Class II (oil/gas related — brine disposal, enhanced recovery, hydrocarbon storage), Class III (mineral extraction), Class IV (banned — hazardous/radioactive into/above USDW), Class V (all others not in I-IV — stormwater, geothermal, aquifer recharge), Class VI (carbon sequestration). Texas is unique: RRC administers Class II wells under state primacy, while TCEQ/EPA share jurisdiction over Classes I, III, V, and VI. Class II permits require area of review (1/4 mile minimum), well construction standards, mechanical integrity testing, monitoring, and financial responsibility. Induced seismicity from Class II disposal wells has become a major issue in Texas, Oklahoma, and other oil/gas states — RRC now requires seismicity review before approving or modifying disposal permits in areas with seismic activity.",
        authority="42 USC 300h; 40 CFR Parts 144-148; 16 TAC Chapter 3 (RRC Class II)",
        keywords=["uic", "underground injection", "disposal well", "class ii", "class vi", "carbon sequestration", "usdw", "injection well"],
        statute="42 USC 300h",
        cfr_reference="40 CFR Parts 144-148",
        confidence=0.93,
        cross_references=["sdwa_mcl", "permian_produced_water", "permian_seismicity"],
        texas_notes="RRC administers Class II wells; TCEQ administers other classes; seismicity review required for Permian Basin disposal wells",
    ),

    # ---- OPA ----
    DoctrineCacheBlock(
        topic="opa_spcc",
        category="oil_spill",
        summary="OPA and CWA Section 311 require facilities storing oil to prepare SPCC plans to prevent oil spills into navigable waters, with Facility Response Plans for worst-case discharge scenarios.",
        analysis="The SPCC rule (40 CFR Part 112) applies to non-transportation-related facilities that store oil and could reasonably be expected to discharge to navigable waters. Applicability thresholds: >1,320 gallons total aboveground storage or >42,000 gallons total underground storage. SPCC plans must be prepared by a Professional Engineer and include: facility description, spill history, potential discharge predictions, secondary containment, countermeasures, inspection procedures, and employee training. Tier I/II qualified facility plans available for smaller facilities. Amendments must be made within 6 months of changes. Facility Response Plans (FRP) required under OPA Section 311(j) for facilities that could cause 'substantial harm' — must address worst-case discharge, response resources, communication plans, and exercises. OPA also establishes strict liability for cleanup costs and damages from oil spills, with limited defenses (act of God, act of war, act/omission of third party). The Oil Spill Liability Trust Fund finances federal responses. In the Permian Basin, SPCC requirements apply to tank batteries, oil storage facilities, and produced water handling operations.",
        authority="33 USC 2701-2762 (OPA); 33 USC 1321 (CWA 311); 40 CFR Part 112",
        keywords=["spcc", "oil spill", "facility response plan", "opa", "secondary containment", "cwa 311", "oil storage", "worst case discharge"],
        statute="33 USC 2701-2762; 33 USC 1321",
        cfr_reference="40 CFR Part 112",
        confidence=0.93,
        cross_references=["cwa_npdes", "permian_pipeline_spill"],
        texas_notes="RRC has oil spill response authority for oil/gas facilities; TCEQ/EPA for non-oil/gas; GRP (formerly OSRO) requirements for Coastal Zone",
        penalties="OPA civil: up to $64,618/day or $2,582,462 per spill event; CWA 311: similar per-barrel and per-day penalties",
    ),

    # ---- EPCRA ----
    DoctrineCacheBlock(
        topic="epcra_tri",
        category="epcra_reporting",
        summary="EPCRA Section 313 requires facilities in specified sectors to annually report releases of listed toxic chemicals through the Toxic Release Inventory (TRI) program.",
        analysis="TRI reporting under EPCRA Section 313 (42 USC 11023) applies to facilities with 10+ employees in covered SIC/NAICS codes that manufacture (>25,000 lbs), process (>25,000 lbs), or otherwise use (>10,000 lbs) a listed TRI chemical. Currently ~770 chemicals and 33 chemical categories. Reports due July 1 annually for the prior calendar year. Form R (full report) or Form A (abbreviated for small quantities). Data includes: facility identification, chemical identity, maximum amounts on-site, releases to air/water/land, transfers for disposal/recycling, source reduction activities, and pollution prevention data. TRI data is publicly available on EPA's TRI Explorer. EPCRA also requires: Section 302-303 emergency planning notification, Section 304 emergency release notification, and Sections 311-312 Tier I/II chemical inventory reporting. Oil and gas extraction (SIC 13/NAICS 211) has been added to TRI reporting requirements as of 2022. This affects Permian Basin operators storing or using large quantities of listed chemicals.",
        authority="42 USC 11023; 40 CFR Part 372; Executive Order 12856",
        keywords=["tri", "toxic release inventory", "epcra", "section 313", "chemical reporting", "tier ii", "emergency planning", "right to know"],
        statute="42 USC 11023",
        cfr_reference="40 CFR Part 372",
        confidence=0.92,
        cross_references=["rcra_subtitle_c", "caa_title_v"],
        texas_notes="TCEQ Tier II reporting; LEPCs active in Permian Basin counties; oil/gas sector TRI reporting now required",
        penalties="Up to $64,618/day per violation for failure to report; criminal penalties for false reporting",
    ),

    # ---- TCEQ ----
    DoctrineCacheBlock(
        topic="tceq_vcp",
        category="tceq",
        summary="TCEQ's Voluntary Cleanup Program (VCP) provides a framework for property owners to investigate and remediate contaminated sites with TCEQ oversight, resulting in a certificate of completion that limits future liability.",
        analysis="The Texas VCP under Texas Health & Safety Code Chapter 361, Subchapter S allows voluntary participants to characterize and clean up contaminated sites. Key features: (1) Applicant submits application with site information and $1,000 fee, (2) TCEQ assigns project manager and reviews Affected Property Assessment Report (APAR) and Response Action Plan (RAP), (3) Risk-based corrective action (RBCA) approach — Texas Risk Reduction Standards (30 TAC 350) apply, (4) Upon completion, TCEQ issues a Certificate of Completion and Voluntary Cleanup Program (VCPCC) — this provides innocent purchaser defense under state law and supports BFPP defense under federal CERCLA, (5) Municipal Settings Designations (MSD) can eliminate groundwater ingestion pathway. Benefits: liability protection, faster timeline than enforcement-driven cleanup, risk-based standards, and marketability of property. VCP is widely used for brownfield redevelopment, real estate transactions, and resolving environmental legacy issues. The program processes approximately 800-1,000 sites and completes 150-200 per year.",
        authority="Texas Health & Safety Code Chapter 361 Subchapter S; 30 TAC Chapter 350",
        keywords=["vcp", "voluntary cleanup", "tceq", "certificate of completion", "rbca", "risk reduction", "brownfield", "texas", "msd"],
        statute="Texas Health & Safety Code 361.601-613",
        cfr_reference="30 TAC Chapter 350",
        jurisdiction="TX",
        confidence=0.93,
        cross_references=["cercla_brownfield", "phase_i_esa", "environmental_due_diligence"],
        texas_notes="VCP is the primary pathway for brownfield transactions in Texas; MSD eliminates groundwater ingestion pathway for urban sites",
    ),

    # ---- RRC ENVIRONMENTAL ----
    DoctrineCacheBlock(
        topic="rrc_environmental",
        category="rrc",
        summary="The Railroad Commission of Texas (RRC) has exclusive jurisdiction over environmental regulation of oil and gas activities, including waste management, well plugging, surface restoration, produced water disposal, and air emissions from oil and gas sources.",
        analysis="RRC environmental authority derives from the Texas Natural Resources Code and Texas Water Code. Key Statewide Rules: SWR 8 (water protection — no pollution of surface/ground water), SWR 9 (disposal wells), SWR 13 (casing and cementing), SWR 14 (plugging), SWR 36 (oil and gas waste). RRC regulates: (1) drilling and completions environmental requirements, (2) produced water management and disposal, (3) oilfield waste management (pits, tanks, disposal), (4) well plugging when wells are abandoned, (5) surface restoration post-plugging, (6) H2S operations plans, (7) pipeline safety and leak prevention, (8) flaring/venting authorizations. RRC's Oil and Gas Division handles permits; the Environmental and Safety Division handles compliance and enforcement. RRC maintains the Oil and Gas Well Plugging Fund for orphan well cleanups. In the Permian Basin, key issues include: produced water disposal and induced seismicity, methane emissions and flaring reduction, orphan well inventory, and contamination from legacy operations. RRC authority is distinct from TCEQ — operators must deal with the correct agency for the type of environmental issue.",
        authority="Texas Natural Resources Code; Texas Water Code; 16 TAC Chapter 3",
        keywords=["rrc", "railroad commission", "oil gas environmental", "statewide rule", "produced water", "plugging", "flaring", "waste", "swr 8", "swr 9"],
        statute="Texas Natural Resources Code; Texas Water Code",
        cfr_reference="16 TAC Chapter 3",
        jurisdiction="TX",
        confidence=0.94,
        cross_references=["permian_produced_water", "permian_flaring", "rrc_produced_water"],
        texas_notes="RRC has exclusive jurisdiction over oil/gas environmental; do NOT file environmental complaints with TCEQ for oil/gas operations",
    ),

    # ---- PERMIAN BASIN ----
    DoctrineCacheBlock(
        topic="permian_produced_water",
        category="permian_basin",
        summary="Produced water management is the single largest environmental challenge in the Permian Basin, with billions of barrels annually requiring disposal, recycling, or beneficial reuse.",
        analysis="The Permian Basin generates approximately 3-5 billion barrels of produced water annually, with water-to-oil ratios of 3:1 to 10:1 depending on formation. Disposal options: (1) Saltwater disposal wells (SWD) — Class II UIC wells, the dominant disposal method, regulated by RRC under SWR 9 and 16 TAC 3.46. (2) Recycling/reuse — treatment for hydraulic fracturing reuse, reducing freshwater demand. (3) Beneficial reuse — agriculture, dust suppression, road maintenance (limited due to salinity/contaminants). (4) Evaporation ponds — less common, surface water/air quality concerns. Key issues: (a) Induced seismicity — correlation between injection volumes and seismic events, particularly in Delaware Basin; RRC seismicity review required for new/modified permits in seismic response areas. (b) NORM (Naturally Occurring Radioactive Material) — produced water often contains elevated radium; disposal of NORM scale is regulated. (c) Surface spills — pipeline leaks and tank overflows can contaminate soil/groundwater; must report to RRC within 24 hours. (d) TDS concentrations — Permian produced water TDS ranges 40,000-300,000+ mg/L, making treatment expensive. The 2023 Texas legislature authorized expanded produced water beneficial reuse research.",
        authority="16 TAC Chapter 3 Rules 9, 46; Texas Water Code Chapter 122 (produced water); RRC Statewide Rules",
        keywords=["produced water", "saltwater disposal", "swd", "permian basin", "induced seismicity", "recycling", "beneficial reuse", "norm", "rrc"],
        statute="Texas Natural Resources Code; Texas Water Code Chapter 122",
        jurisdiction="TX",
        confidence=0.93,
        cross_references=["permian_seismicity", "sdwa_uic", "rrc_environmental"],
        texas_notes="RRC Seismic Response Areas in Delaware Basin; produced water beneficial reuse legislation (HB 2771, 2023)",
    ),
    DoctrineCacheBlock(
        topic="permian_flaring",
        category="permian_basin",
        summary="Gas flaring in the Permian Basin is under increasing regulatory and investor pressure, with RRC requiring flaring permits and EPA imposing methane emission limits under NSPS OOOOb/OOOOc.",
        analysis="Flaring in the Permian Basin results from insufficient gas gathering/processing infrastructure relative to oil production growth. Key regulatory framework: (1) RRC flaring permits — operators must obtain a permit to flare or vent gas; SWR 32 prohibits waste of gas. Routine flaring extensions have been increasingly scrutinized. (2) EPA NSPS OOOOb (new sources) and OOOOOc (existing sources) — 2024 rules require methane monitoring (LDAR), limit flaring during completions, and mandate Super-Emitter Response Program. (3) IRA Methane Fee — the Inflation Reduction Act imposes a methane fee starting at $900/ton in 2024, escalating to $1,500/ton in 2026, for facilities exceeding methane waste thresholds. (4) World Bank Zero Routine Flaring Initiative — major operators have committed. (5) ESG pressure — investors and lenders increasingly requiring flaring reduction targets. (6) Permian Basin flaring intensity has decreased from ~4.2% to ~1.5% (2019-2024) but absolute volumes remain high. Solutions include: gas gathering infrastructure buildout, on-site gas processing, CNG/LNG transport, gas-to-power, and carbon capture. RRC has authority to shut in wells where gas is being wasted.",
        authority="16 TAC 3.32 (SWR 32); 40 CFR Part 60 Subpart OOOOb/OOOOc; IRA Section 60113 (Methane Fee)",
        keywords=["flaring", "venting", "methane", "permian basin", "nsps", "oooo", "rrc", "gas waste", "ira methane fee", "esg"],
        statute="Texas Natural Resources Code (SWR 32); 42 USC 7411 (CAA 111)",
        cfr_reference="40 CFR Part 60 Subparts OOOOb, OOOOc",
        jurisdiction="TX",
        confidence=0.92,
        cross_references=["caa_nsps", "permian_methane", "rrc_environmental"],
        texas_notes="RRC flaring permit requirements; increasing denials of routine flaring extensions; SWR 32 waste prohibition",
    ),
    DoctrineCacheBlock(
        topic="permian_seismicity",
        category="permian_basin",
        summary="Induced seismicity from saltwater disposal well injection in the Permian Basin has prompted RRC to establish Seismic Response Areas with mandatory monitoring, volume reduction, and permit conditions.",
        analysis="Induced seismicity in the Permian Basin, particularly the Delaware Basin, has increased significantly since 2020. The scientific consensus links deep well injection of produced water to fault reactivation. RRC responses: (1) Seismic Response Areas (SRAs) designated where injection is linked to seismic activity. (2) Operators in SRAs must reduce injection volumes, install seismic monitoring, and comply with additional permit conditions. (3) New disposal well permits in seismic areas require seismicity review including fault proximity analysis. (4) RRC can suspend or modify permits where injection is causing seismic events. (5) 2021-2024: RRC issued multiple orders reducing injection volumes in Culberson-Reeves, Stanton, and other areas. Key legal issues: (a) operator liability for induced seismicity damage (nuisance, trespass, negligence), (b) insurance coverage for induced seismicity, (c) regulatory takings if injection curtailed, (d) produced water disposal alternatives. The Texas Supreme Court has not yet directly addressed liability for injection-induced earthquakes, though analogous cases exist. FracFocus and RRC databases provide injection volume data for analysis.",
        authority="16 TAC Chapter 3; RRC Seismicity Orders (2021-2024); Texas Natural Resources Code",
        keywords=["induced seismicity", "earthquake", "saltwater disposal", "swd", "permian basin", "seismic response area", "fault", "injection"],
        statute="Texas Natural Resources Code",
        jurisdiction="TX",
        confidence=0.91,
        cross_references=["permian_produced_water", "sdwa_uic", "rrc_environmental"],
        texas_notes="RRC Seismic Response Areas actively managed; operators subject to volume curtailment orders",
    ),

    # ---- ENVIRONMENTAL JUSTICE ----
    DoctrineCacheBlock(
        topic="environmental_justice",
        category="environmental_justice",
        summary="Environmental justice requires fair treatment and meaningful involvement of all people regardless of race, color, income, or national origin in environmental decision-making, rooted in Executive Order 12898 and increasingly codified in statute.",
        analysis="Environmental justice (EJ) addresses the disproportionate environmental and health impacts on minority and low-income communities. Key framework: (1) EO 12898 (1994) directs federal agencies to identify and address disproportionate effects on minority/low-income populations. (2) EO 14096 (2023) strengthened EJ requirements including cumulative impacts analysis. (3) Title VI of the Civil Rights Act prohibits recipients of federal funding from discriminating based on race. (4) EPA's EJScreen tool identifies communities with EJ concerns. (5) The IRA and IIJA include Justice40 Initiative — directing 40% of clean energy/climate benefits to disadvantaged communities. (6) NEPA EIS must analyze EJ impacts. (7) EPA's disparate impact regulations under Title VI allow administrative complaints. Challenges: no standalone federal EJ statute; EJ is implemented through existing authorities. Permit applicants increasingly must address EJ in applications. State EJ laws emerging (NJ, NY, CA). In Texas, EJ considerations arise in permit proceedings before TCEQ, particularly for facilities sited near minority/low-income communities. Cumulative impact analysis is the frontier of EJ — assessing not just the proposed action but the total pollution burden on a community.",
        authority="EO 12898 (1994); EO 14096 (2023); Title VI Civil Rights Act (42 USC 2000d); EPA EJ Policy (2022)",
        keywords=["environmental justice", "ej", "disproportionate impact", "cumulative impact", "ejscreen", "justice40", "title vi", "eo 12898"],
        statute="EO 12898; 42 USC 2000d (Title VI)",
        confidence=0.90,
        cross_references=["nepa_eis", "caa_title_v", "rcra_subtitle_c"],
    ),

    # ---- CITIZEN SUITS ----
    DoctrineCacheBlock(
        topic="citizen_suits",
        category="compliance_enforcement",
        summary="Most federal environmental statutes contain citizen suit provisions allowing private parties to enforce environmental laws against violators and against EPA for failure to perform mandatory duties.",
        analysis="Citizen suit provisions exist in CAA 304, CWA 505, RCRA 7002, CERCLA 310, TSCA 20, ESA 11(g), SDWA 1449, and EPCRA 326. Key requirements: (1) 60-day notice to alleged violator, EPA, and state (90 days for RCRA). (2) No suit if EPA or state is 'diligently prosecuting.' (3) Standing requires injury in fact, causation, and redressability. (4) Violation must be ongoing or reasonably likely to recur (Gwaltney v. Chesapeake Bay Foundation, 484 U.S. 49 (1987) — wholly past violations generally insufficient under CWA). (5) Available remedies: injunctive relief, civil penalties payable to U.S. Treasury, and attorney's fees. RCRA 7002(a)(1)(B) 'imminent and substantial endangerment' claims are uniquely powerful — they apply to past and present conduct, cover solid waste (not just hazardous), and can compel cleanup. Supplemental environmental projects (SEPs) may be included in consent decrees to benefit the affected community. Strategy: citizen suit notice letters are powerful negotiation tools even if suit is never filed — the 60-day period often triggers voluntary compliance or consent negotiations.",
        authority="CAA 304 (42 USC 7604); CWA 505 (33 USC 1365); RCRA 7002 (42 USC 6972); Gwaltney v. Chesapeake Bay Foundation, 484 U.S. 49 (1987); Friends of the Earth v. Laidlaw, 528 U.S. 167 (2000)",
        keywords=["citizen suit", "private enforcement", "notice", "standing", "injunction", "attorney fees", "diligent prosecution", "gwaltney"],
        statute="Multiple (CAA 304, CWA 505, RCRA 7002, etc.)",
        confidence=0.93,
        cross_references=["cwa_npdes", "rcra_subtitle_c", "caa_title_v"],
        practice_tips=[
            "60-day notice letter is often more powerful than the suit itself",
            "Research enforcement history — if EPA/state is 'diligently prosecuting,' citizen suit is barred",
            "RCRA 7002(a)(1)(B) imminent endangerment claims can reach past violations",
            "Fee-shifting makes environmental citizen suits economically viable for plaintiffs",
        ],
    ),

    # ---- CARBON / CLIMATE ----
    DoctrineCacheBlock(
        topic="carbon_credits",
        category="carbon_climate",
        summary="Carbon credits represent verified greenhouse gas emission reductions or removals, tradeable in voluntary and compliance markets, subject to evolving verification standards and regulatory frameworks.",
        analysis="Carbon markets operate in two categories: (1) Compliance markets — mandatory cap-and-trade programs (California Cap-and-Trade under AB 32, RGGI in northeastern states, EU ETS). Allowances are allocated or auctioned; entities must surrender allowances equal to emissions. California allowances trade at $25-40/ton. (2) Voluntary markets — companies/individuals purchase offsets to meet voluntary sustainability commitments. Offset types include renewable energy, forestry/land use (REDD+), methane capture, direct air capture, and agricultural soil carbon. Verification standards: Verra (VCS), Gold Standard, American Carbon Registry (ACR), Climate Action Reserve (CAR). Key issues: additionality (would the reduction have happened anyway?), permanence (will the carbon stay sequestered?), leakage (does reduction in one area increase emissions elsewhere?), double counting. The SEC climate disclosure rule (2024, partially stayed) would require public companies to report Scope 1, 2, and material Scope 3 emissions. The IRA provides 45Q tax credits for carbon capture ($85/ton for geological storage, $180/ton for direct air capture). Carbon credit integrity concerns have led to tighter verification standards and push toward 'high quality' credits.",
        authority="California AB 32/SB 32; RGGI; IRA Section 45Q; SEC Climate Disclosure Rule (2024)",
        keywords=["carbon credit", "carbon offset", "cap and trade", "voluntary market", "compliance market", "45q", "carbon capture", "verification"],
        statute="IRA Section 45Q; California AB 32",
        confidence=0.88,
        cross_references=["climate_regulation", "caa_ghg"],
    ),

    # ---- PHASE I ESA ----
    DoctrineCacheBlock(
        topic="phase_i_esa",
        category="site_assessment",
        summary="Phase I Environmental Site Assessment per ASTM E1527-21 satisfies the 'all appropriate inquiries' requirement under CERCLA, identifying recognized environmental conditions through records review, site reconnaissance, and interviews.",
        analysis="ASTM E1527-21 (Standard Practice for Environmental Site Assessments: Phase I Process) defines the scope and methodology for Phase I ESAs. The Phase I satisfies the 'all appropriate inquiries' (AAI) requirement of CERCLA 101(35)(B) and 40 CFR Part 312 needed to claim innocent landowner, BFPP, or contiguous property owner defenses. Key components: (1) Records Review — federal/state/local environmental databases (EDR, NETR), historical sources (Sanborn maps, aerial photos, city directories, building permits), (2) Site Reconnaissance — visual inspection of subject property and adjoining properties, (3) Interviews — owner, occupants, local government officials, (4) Report — professional opinion on RECs, CRECs, HRECs, and de minimis conditions. ASTM E1527-21 updates include: mandatory vapor intrusion screening, expanded definition of 'migrate,' refined REC/CREC/HREC definitions. A REC is 'the presence or likely presence of any hazardous substances or petroleum products in, on, or at a property due to release or likely release to the environment.' Phase I shelf life: 180 days, with update possible within 1 year. Must be conducted by an Environmental Professional (EP) as defined by 40 CFR 312.10. Phase I does NOT include sampling; if RECs are identified, Phase II ESA with sampling is recommended.",
        authority="ASTM E1527-21; 40 CFR Part 312; 42 USC 9601(35)(B)",
        keywords=["phase i", "esa", "environmental site assessment", "astm e1527", "rec", "crec", "hrec", "all appropriate inquiries", "aai"],
        statute="42 USC 9601(35)(B)",
        cfr_reference="40 CFR Part 312",
        confidence=0.95,
        cross_references=["cercla_brownfield", "phase_ii_esa", "environmental_due_diligence"],
        practice_tips=[
            "Phase I is critical for any commercial real estate transaction to preserve CERCLA defenses",
            "Ensure the EP meets 40 CFR 312.10 qualifications",
            "Vapor intrusion screening is now mandatory under E1527-21",
            "Data gaps should be clearly identified and assessed for their impact on REC identification",
            "The Phase I must be 'reliance' specific — ensure your entity is listed as an authorized user",
        ],
    ),

    # ---- TOXIC TORT ----
    DoctrineCacheBlock(
        topic="toxic_tort",
        category="toxic_tort",
        summary="Toxic tort litigation involves claims for personal injury or property damage from exposure to hazardous substances, requiring proof of exposure, causation (general and specific), and damages.",
        analysis="Toxic tort claims arise under state common law theories: negligence, strict liability, trespass, nuisance, and battery. Key elements: (1) Exposure — plaintiff must prove actual exposure to the substance at issue. (2) General causation — the substance is capable of causing the type of harm alleged (typically proven through epidemiological studies). (3) Specific causation — the plaintiff's particular injury was caused by the exposure (typically requires expert medical testimony using differential diagnosis). (4) Dose-response — courts and experts apply dose-response principles to assess whether exposure was sufficient. (5) Daubert/Robinson — expert testimony must satisfy reliability standards. (6) Latency — many environmental diseases have long latency periods (asbestos mesothelioma: 20-50 years). Statutes of limitation may be tolled by discovery rule. Common environmental toxic tort scenarios: contaminated drinking water, air pollution, soil contamination, occupational exposure, consumer product exposure (PFAS, Roundup, AFFF). Class actions and multidistrict litigation (MDL) are common vehicles. Texas toxic tort law follows proportionate responsibility (Chapter 33, CPRC) for negligence claims; strict liability under Restatement (Second) for abnormally dangerous activities; nuisance claims for pollution affecting property use.",
        authority="Restatement (Second) of Torts; Daubert v. Merrell Dow, 509 U.S. 579 (1993); E.I. du Pont de Nemours v. Robinson, 923 S.W.2d 549 (Tex. 1995)",
        keywords=["toxic tort", "causation", "exposure", "personal injury", "contamination", "daubert", "epidemiology", "class action", "nuisance", "strict liability"],
        statute="State common law; Texas CPRC Chapter 33",
        jurisdiction="TX",
        confidence=0.91,
        cross_references=["cercla_prp_liability", "cwa_npdes", "tsca_pfas"],
        texas_notes="Texas proportionate responsibility (CPRC Ch. 33); Robinson standard for scientific expert testimony; 2-year statute of limitations for personal injury (discovery rule)",
    ),

    # ---- ENVIRONMENTAL AUDIT PRIVILEGE ----
    DoctrineCacheBlock(
        topic="environmental_audit_privilege",
        category="compliance_enforcement",
        summary="Texas Environmental Audit Privilege Act (Texas Health & Safety Code Chapter 1101) provides a qualified privilege for voluntary environmental self-audits, protecting audit reports from discovery and use in enforcement.",
        analysis="Texas is one of approximately 25 states with an environmental audit privilege law. Key provisions: (1) Voluntary environmental audits conducted in good faith to assess compliance with environmental laws are privileged. (2) The privilege protects the audit report from discovery in civil, criminal, or administrative proceedings. (3) The privilege does not apply if: the audit was conducted to avoid detection of a criminal offense, the information shows a clear, present, and impending danger to public health/safety/environment, or the person asserting privilege committed environmental fraud. (4) Self-disclosure immunity: entities that voluntarily disclose violations discovered through audits may receive penalty mitigation. (5) EPA's Audit Policy (Incentives for Self-Policing) provides up to 100% gravity penalty reduction for voluntarily discovered and promptly disclosed violations. Requirements for EPA Audit Policy: systematic discovery (not monitoring/inspection), voluntary disclosure within 21 days, prompt correction, prevent recurrence, no repeat violations, not criminal. The privilege encourages compliance auditing without creating litigation exposure, balancing environmental improvement with enforcement fairness.",
        authority="Texas Health & Safety Code Chapter 1101; EPA Audit Policy (65 FR 19618, 2000)",
        keywords=["environmental audit", "privilege", "self-disclosure", "immunity", "penalty mitigation", "epa audit policy", "compliance audit", "voluntary disclosure"],
        statute="Texas Health & Safety Code Chapter 1101",
        jurisdiction="TX",
        confidence=0.91,
        cross_references=["citizen_suits", "caa_title_v", "rcra_subtitle_c"],
        texas_notes="Texas Environmental Audit Privilege Act is one of the strongest state audit privilege laws; complements EPA federal Audit Policy",
    ),

    # ---- ENVIRONMENTAL INSURANCE ----
    DoctrineCacheBlock(
        topic="environmental_insurance",
        category="environmental_insurance",
        summary="Environmental insurance products (PLL, CPL, EIL) provide coverage for pollution conditions, cleanup costs, third-party claims, and regulatory defense costs not covered by standard CGL policies.",
        analysis="Standard CGL policies contain absolute pollution exclusions (post-1986). Environmental insurance fills this gap: (1) Pollution Legal Liability (PLL) — covers third-party bodily injury/property damage claims and cleanup costs from pollution conditions on, under, or migrating from the insured's property. (2) Contractor's Pollution Liability (CPL) — covers contractors for pollution events arising from their operations. (3) Environmental Impairment Liability (EIL) — broader coverage including gradual pollution. (4) Secured Creditor/Lender Protection — covers lender liability for contaminated collateral. (5) Cleanup Cost Cap — covers cost overruns on remediation projects. Key considerations: retroactive date (pre-existing conditions), claims-made vs. occurrence, definition of 'pollution condition,' regulatory defense costs, natural resource damage coverage. Environmental insurance is increasingly required in real estate transactions involving contaminated property, M&A deals with environmental exposure, and as CERCLA liability protection for lenders and property owners. Premiums range from $10,000 to $500,000+ annually depending on risk profile. Policy limits typically $1M-$50M. Historical CGL policies (pre-pollution exclusion, pre-1986) may provide coverage — insurance archaeology can be valuable for legacy contamination.",
        authority="Insurance contract law; state insurance regulations; CERCLA 107/101 (liability context)",
        keywords=["environmental insurance", "pll", "cpl", "eil", "pollution liability", "cleanup cost cap", "cgl exclusion", "insurance archaeology"],
        statute="State insurance code; CERCLA (liability context)",
        confidence=0.89,
        cross_references=["cercla_prp_liability", "phase_i_esa", "environmental_due_diligence"],
    ),

    # ---- SUPPLEMENTAL ENVIRONMENTAL PROJECT ----
    DoctrineCacheBlock(
        topic="sep",
        category="compliance_enforcement",
        summary="Supplemental Environmental Projects (SEPs) are environmentally beneficial projects that a violator agrees to undertake as part of an enforcement settlement, reducing the penalty amount while providing community benefit.",
        analysis="SEPs are projects that go beyond what is required by law and provide tangible environmental or public health benefits. EPA's SEP Policy (2015, updated 2022) establishes categories: (1) pollution prevention, (2) pollution reduction, (3) environmental restoration, (4) environmental compliance promotion, (5) emergency planning/preparedness, (6) environmental audits, (7) public health. A SEP must have a 'nexus' to the violation — must be related to the violation's type or geographic area. SEP value can offset up to 80% of the gravity component of the penalty (not the economic benefit component). The violator must spend at least $1.25 on the SEP for every $1 of penalty mitigation. SEPs cannot be projects the violator is already legally required to perform. EPA approval is required. Texas TCEQ also accepts SEPs in enforcement settlements under 30 TAC Chapter 70. SEPs are attractive for companies seeking to demonstrate community responsibility and for communities seeking environmental improvement beyond simple penalty payment.",
        authority="EPA SEP Policy (2015, updated 2022); 30 TAC Chapter 70 (Texas)",
        keywords=["sep", "supplemental environmental project", "penalty mitigation", "enforcement", "settlement", "community benefit", "nexus"],
        statute="EPA enforcement discretion; 30 TAC Chapter 70 (Texas)",
        confidence=0.90,
        cross_references=["citizen_suits", "environmental_justice"],
    ),

    # ---- ENVIRONMENTAL DISCLOSURE ----
    DoctrineCacheBlock(
        topic="environmental_disclosure",
        category="compliance_enforcement",
        summary="Environmental disclosure requirements apply in real estate transactions, securities offerings, lending, and corporate reporting, with failure to disclose creating liability under CERCLA, state law, and securities regulations.",
        analysis="Environmental disclosure obligations arise from multiple sources: (1) CERCLA — AAI requirements effectively mandate Phase I ESA disclosure in property transactions. (2) Real estate disclosure — many states require sellers to disclose known environmental conditions; Texas Property Code 5.008 requires residential seller disclosure but commercial transactions rely on contractual representations. (3) Securities law — SEC requires disclosure of material environmental liabilities in 10-K/10-Q filings; the 2024 climate disclosure rule adds Scope 1/2 emissions reporting for large filers. (4) ASTM E2600 (vapor encroachment screening) and E1528 (limited ESA) provide transaction screening tools. (5) Lending — banks require Phase I ESA for commercial loans (Fannie Mae, SBA, CMBS requirements). (6) Environmental liens — CERCLA Section 107(l) creates a federal lien on contaminated property; state environmental liens also exist. (7) M&A — environmental representations and warranties, indemnifications, and escrow provisions are standard. Failure to disclose known contamination can result in: fraud claims, rescission, CERCLA cost recovery, regulatory enforcement, and loss of CERCLA defenses (innocent purchaser, BFPP). Environmental insurance (PLL) and contractual risk allocation are key transaction tools.",
        authority="42 USC 9607(l) (CERCLA lien); SEC Regulation S-K Item 101/103; Texas Property Code 5.008",
        keywords=["environmental disclosure", "transaction", "phase i", "securities", "material liability", "environmental lien", "due diligence", "representations warranties"],
        statute="42 USC 9607(l); SEC Regulation S-K; Texas Property Code 5.008",
        confidence=0.90,
        cross_references=["phase_i_esa", "cercla_brownfield", "environmental_insurance"],
    ),

    # ---- RCRA CORRECTIVE ACTION ----
    DoctrineCacheBlock(
        topic="rcra_corrective_action",
        category="hazardous_waste",
        summary="RCRA Corrective Action under Section 3004(u) and 3008(h) requires investigation and cleanup of releases of hazardous waste or constituents at RCRA-permitted facilities, paralleling but distinct from CERCLA remediation.",
        analysis="RCRA Corrective Action applies to all solid waste management units (SWMUs) at facilities seeking or holding a RCRA permit. Key authority: Section 3004(u) (permit condition requiring corrective action for all SWMUs), Section 3008(h) (interim status corrective action orders). The process involves: (1) RCRA Facility Assessment (RFA) to identify SWMUs and areas of concern, (2) RCRA Facility Investigation (RFI) to characterize contamination, (3) Corrective Measures Study (CMS) to evaluate remedy alternatives, (4) Corrective Measures Implementation (CMI). EPA's 2015 Corrective Action Strategy emphasizes human exposure controls, groundwater migration controls, and final remedy construction. Unlike CERCLA, RCRA corrective action is typically implemented through permit conditions or administrative orders rather than unilateral action. Financial assurance is required. The corrective action process can apply to facilities even after closure. EPA's Environmental Indicators track progress: (1) Current Human Exposures Under Control, (2) Migration of Contaminated Groundwater Under Control. Over 3,700 facilities subject to RCRA corrective action nationally. Risk-based cleanup standards (state RBCA programs) often apply.",
        authority="42 USC 6924(u), 6928(h); 40 CFR 264.101; EPA RCRA Corrective Action Strategy (2015)",
        keywords=["rcra corrective action", "3004u", "3008h", "swmu", "rfa", "rfi", "cms", "cmi", "cleanup", "hazardous waste"],
        statute="42 USC 6924(u), 6928(h)",
        cfr_reference="40 CFR 264.101",
        confidence=0.93,
        cross_references=["rcra_subtitle_c", "cercla_ncp", "tceq_vcp"],
        texas_notes="TCEQ administers RCRA corrective action in Texas under authorized program; 30 TAC Chapter 335 Subchapter S",
    ),

    # ---- CWA WETLANDS ----
    DoctrineCacheBlock(
        topic="cwa_wetlands",
        category="water_quality",
        summary="Wetlands are protected under CWA Section 404 and Section 401, with the definition of jurisdictional wetlands significantly narrowed by Sackett v. EPA (2023) requiring a continuous surface connection to navigable waters.",
        analysis="Wetlands are 'areas that are inundated or saturated by surface or ground water at a frequency and duration sufficient to support, and that under normal circumstances do support, a prevalence of vegetation typically adapted for life in saturated soil conditions' (33 CFR 328.3). Post-Sackett v. EPA (2023), only wetlands with a 'continuous surface connection' to waters of the United States such that they are indistinguishable from those waters are jurisdictional. This overturned the significant nexus test from Justice Kennedy's Rapanos concurrence. Impact: many isolated wetlands, non-adjacent wetlands, and wetlands connected only through subsurface flow lose federal CWA protection. State wetland programs may still protect non-jurisdictional wetlands. Wetland delineation follows the 1987 Corps of Engineers Wetland Delineation Manual and regional supplements. Compensatory mitigation for unavoidable wetland losses follows the 2008 Mitigation Rule: mitigation banking (preferred) > in-lieu fee > permittee-responsible. Nationwide permits authorize minor impacts. In Texas, there is no comprehensive state wetland program — federal CWA Section 404 is the primary protection.",
        authority="33 USC 1344; 33 CFR 328.3; Sackett v. EPA, 598 U.S. 651 (2023); Rapanos v. United States, 547 U.S. 715 (2006); 33 CFR 332",
        keywords=["wetlands", "section 404", "sackett", "jurisdictional", "delineation", "mitigation", "wotus", "continuous surface connection"],
        statute="33 USC 1344",
        cfr_reference="33 CFR 328.3; 33 CFR 332",
        confidence=0.94,
        cross_references=["cwa_404", "cwa_npdes", "esa_section_7"],
        texas_notes="Texas has no state wetland program; CWA Section 404 is primary federal protection; post-Sackett, many Texas wetlands may lose federal jurisdiction",
    ),

    # ---- CAA NESHAP ----
    DoctrineCacheBlock(
        topic="caa_neshap",
        category="air_quality",
        summary="National Emission Standards for Hazardous Air Pollutants (NESHAPs) under CAA Section 112 regulate HAP emissions from major and area sources, initially technology-based (MACT) with residual risk review after 8 years.",
        analysis="CAA Section 112 lists 187 hazardous air pollutants (HAPs) and requires EPA to establish emission standards for source categories. Major sources (10+ tpy single HAP or 25+ tpy combined HAPs) must comply with MACT (Maximum Achievable Control Technology) standards. Area sources (below major thresholds) may be subject to GACT (Generally Available Control Technology). The 1990 CAA Amendments required EPA to promulgate MACT standards for all listed source categories within 10 years. Standards reflect the best-performing 12% of existing sources (MACT floor). After 8 years, EPA must conduct residual risk review to ensure standards provide an 'ample margin of safety.' NESHAPs relevant to oil and gas include Subpart HH (oil and natural gas production), Subpart HHH (natural gas transmission/storage), and the 2024 methane/HAP rules. NESHAPs for other industries include Subpart M (asbestos), Subpart DDDDD (boilers), and Subpart ZZZZ (reciprocating internal combustion engines). Compliance typically requires emissions testing, monitoring, recordkeeping, and reporting. Case-by-case MACT determinations (Section 112(g)) apply when MACT standards have not yet been promulgated for a category.",
        authority="42 USC 7412; 40 CFR Part 63; National Emission Standards for Hazardous Air Pollutants",
        keywords=["neshap", "hap", "hazardous air pollutant", "mact", "section 112", "area source", "major source", "residual risk"],
        statute="42 USC 7412",
        cfr_reference="40 CFR Part 63",
        confidence=0.93,
        cross_references=["caa_title_v", "caa_naaqs", "caa_nsps"],
        texas_notes="TCEQ implements NESHAP requirements through air quality permits; MACT applicability must be assessed in all air permit applications",
    ),

    # ---- ESA CRITICAL HABITAT ----
    DoctrineCacheBlock(
        topic="esa_critical_habitat",
        category="endangered_species",
        summary="Critical habitat designation under ESA Section 4 identifies specific areas essential for the conservation of a listed species, requiring federal agencies to avoid destruction or adverse modification through Section 7 consultation.",
        analysis="ESA Section 4(a)(3) requires USFWS to designate critical habitat 'to the maximum extent prudent and determinable' concurrent with species listing. Critical habitat includes: (1) occupied habitat — areas occupied by the species at the time of listing containing physical or biological features essential to conservation, (2) unoccupied habitat — areas not occupied but essential for conservation. Designation requires economic impact analysis (ESA Section 4(b)(2)) and may exclude areas where economic costs outweigh benefits, unless exclusion would result in extinction. Effects of designation: federal agencies must consult under Section 7 to ensure actions do not 'destroy or adversely modify' critical habitat. This is a separate prohibition from the jeopardy standard. Critical habitat does not create a reserve or refuge — it applies only to federal actions, not private activities (unless there is a federal nexus). In the Permian Basin, critical habitat designations for the dunes sagebrush lizard and lesser prairie-chicken have significant implications for oil and gas development on federal lands.",
        authority="16 USC 1533(a)(3); 50 CFR 424; Weyerhaeuser Co. v. USFWS, 586 U.S. 9 (2018)",
        keywords=["critical habitat", "esa", "section 4", "designation", "conservation", "occupied", "unoccupied", "economic analysis"],
        statute="16 USC 1533(a)(3)",
        cfr_reference="50 CFR 424",
        confidence=0.92,
        cross_references=["esa_section_7", "esa_section_9"],
        texas_notes="Dunes sagebrush lizard critical habitat proposal affects Permian Basin counties; lesser prairie-chicken listing impacts oil/gas operations",
    ),

    # ---- ESA SECTION 9 ----
    DoctrineCacheBlock(
        topic="esa_section_9",
        category="endangered_species",
        summary="ESA Section 9 prohibits the 'take' of endangered species by any person, including private parties, where 'take' includes harass, harm, pursue, hunt, shoot, wound, kill, trap, capture, or collect.",
        analysis="Section 9 (16 USC 1538) creates a broad prohibition on 'take' of endangered species. 'Harm' includes significant habitat modification or degradation that actually kills or injures wildlife by significantly impairing essential behavioral patterns such as breeding, feeding, or sheltering (50 CFR 17.3; Babbitt v. Sweet Home, 515 U.S. 687 (1995)). For threatened species, the take prohibition applies through species-specific 4(d) rules. Section 9 applies to all persons subject to US jurisdiction — no federal nexus required. Violations can result in civil penalties up to $57,527 per violation and criminal penalties up to $50,000 and/or one year imprisonment. Incidental take permits (Section 10) are available for non-federal activities that may incidentally take listed species, requiring a Habitat Conservation Plan (HCP). In the Permian Basin, Section 9 is particularly relevant for oil and gas operators on private lands where listed species (dunes sagebrush lizard, Texas hornshell mussel) may be present. Candidate Conservation Agreements with Assurances (CCAAs) provide regulatory certainty for landowners who voluntarily conserve candidate species.",
        authority="16 USC 1538; 50 CFR 17.3; Babbitt v. Sweet Home Chapter of Communities for a Great Oregon, 515 U.S. 687 (1995)",
        keywords=["section 9", "take", "harm", "endangered species", "incidental take", "hcp", "habitat conservation plan", "sweet home"],
        statute="16 USC 1538",
        cfr_reference="50 CFR 17",
        confidence=0.93,
        cross_references=["esa_section_7", "esa_section_10", "esa_critical_habitat"],
        texas_notes="Private land operators in Permian Basin must assess Section 9 take risk for listed species; CCAAs provide regulatory assurance",
    ),

    # ---- PHASE II ESA ----
    DoctrineCacheBlock(
        topic="phase_ii_esa",
        category="site_assessment",
        summary="Phase II Environmental Site Assessment involves soil, groundwater, and soil gas sampling to evaluate Recognized Environmental Conditions (RECs) identified in a Phase I ESA, following ASTM E1903-19 standards.",
        analysis="Phase II ESA per ASTM E1903-19 is conducted when Phase I identifies RECs requiring further investigation. Key components: (1) Scope of work design based on Phase I findings — target specific areas of concern. (2) Soil sampling — typically borings to investigate potential soil contamination, analyze for contaminants of concern (petroleum hydrocarbons, VOCs, SVOCs, metals, pesticides as applicable). (3) Groundwater sampling — install monitoring wells or use direct-push technology to assess groundwater quality. (4) Soil gas sampling — evaluate vapor intrusion potential (increasingly required post-E1527-21). (5) Laboratory analysis — EPA methods (8260 for VOCs, 8270 for SVOCs, 6010/6020 for metals, 8015 for TPH). (6) Results compared to applicable screening levels — EPA RSLs, state RBCA standards (30 TAC 350 in Texas), or other applicable criteria. (7) Phase II report with conclusions on nature and extent of contamination, risk assessment, and recommendations (no further action, additional investigation, or remediation). Phase II results determine CERCLA defense viability, transaction risk, remediation need, and regulatory reporting obligations. Cost typically $10,000-$100,000+ depending on scope.",
        authority="ASTM E1903-19; EPA Regional Screening Levels; 30 TAC Chapter 350 (Texas RBCA)",
        keywords=["phase ii", "esa", "sampling", "soil", "groundwater", "soil gas", "vapor intrusion", "astm e1903", "investigation"],
        statute="ASTM E1903-19",
        confidence=0.92,
        cross_references=["phase_i_esa", "tceq_vcp", "cercla_brownfield"],
        texas_notes="Texas Risk Reduction Standards (30 TAC 350) apply to Phase II results; TCEQ VCP accepts Phase II as part of APAR",
    ),

    # ---- PERMIT SHIELD ----
    DoctrineCacheBlock(
        topic="permit_shield",
        category="compliance_enforcement",
        summary="The permit shield doctrine provides that compliance with an environmental permit constitutes compliance with the underlying statute, protecting permittees from enforcement for pollutants or conditions specifically addressed in the permit.",
        analysis="The permit shield exists under both CWA (Section 402(k)) and CAA (Title V). Under CWA 402(k), compliance with an NPDES permit is deemed compliance with Sections 301, 302, 306, 307, and 403 for any pollutant specifically identified in the permit. The shield does not protect against: (1) pollutants not listed in the permit, (2) violations of permit conditions, (3) permit conditions based on incorrect information. Under Title V, the permit shield (40 CFR 70.6(f)) provides that compliance with permit conditions is deemed compliance with all applicable requirements, provided the applicable requirement is specifically identified in the permit. Jurisdictions vary on the scope of the permit shield. Some circuits apply it broadly; others limit it to pollutants the permitting authority specifically considered. The permit shield does not protect against CERCLA liability, which operates independently of permit compliance. Strategy: ensure all potential pollutants and applicable requirements are specifically identified in the permit to maximize shield protection.",
        authority="33 USC 1342(k); 40 CFR 70.6(f); Piney Run Preservation Ass'n v. County Commissioners, 268 F.3d 255 (4th Cir. 2001)",
        keywords=["permit shield", "compliance", "npdes", "title v", "enforcement defense", "402k", "applicable requirements"],
        statute="33 USC 1342(k); 42 USC 7661c(f)",
        confidence=0.91,
        cross_references=["cwa_npdes", "caa_title_v", "citizen_suits"],
    ),

    # ---- CLIMATE REGULATION ----
    DoctrineCacheBlock(
        topic="climate_regulation",
        category="carbon_climate",
        summary="Climate regulation in the US is primarily implemented through CAA GHG regulations, SEC disclosure rules, state programs (California cap-and-trade, RGGI), and IRA incentives, with no comprehensive federal climate statute.",
        analysis="Federal climate regulation has evolved through regulatory, not legislative, pathways: (1) Massachusetts v. EPA (2007) held GHGs are air pollutants under the CAA, enabling EPA regulation. (2) EPA Endangerment Finding (2009) determined GHGs endanger public health. (3) Tailpipe rule (2010+) regulates vehicle GHG emissions. (4) Clean Power Plan (2015)/ACE Rule (2019)/Good Neighbor Rule — power sector regulation has been subject to repeated litigation (West Virginia v. EPA, 2022 major questions doctrine). (5) NSPS OOOOb/OOOOc methane rules for oil/gas. (6) SEC Climate Disclosure Rule (2024, partially stayed) — Scope 1, 2 reporting for large filers. (7) IRA (2022) — massive climate incentives: $369B in clean energy tax credits, 45Q carbon capture ($85/ton geo-storage), methane fee, clean vehicle credits. (8) State programs: California AB 32/SB 32 cap-and-trade, RGGI (northeastern states), state renewable portfolio standards. (9) Paris Agreement (rejoined 2021) — US NDC targets 50-52% reduction by 2030 from 2005 levels. Key legal uncertainty: major questions doctrine (West Virginia v. EPA) constrains EPA authority for 'transformative' regulatory actions without clear congressional authorization.",
        authority="Massachusetts v. EPA, 549 U.S. 497 (2007); West Virginia v. EPA, 597 U.S. 697 (2022); IRA (P.L. 117-169); CAA Section 111",
        keywords=["climate regulation", "ghg", "greenhouse gas", "cap and trade", "paris agreement", "ira", "clean energy", "endangerment finding", "major questions"],
        statute="42 USC 7401+ (CAA); IRA P.L. 117-169",
        confidence=0.89,
        cross_references=["carbon_credits", "caa_nsps", "permian_flaring"],
    ),

    # ---- ENVIRONMENTAL DUE DILIGENCE ----
    DoctrineCacheBlock(
        topic="environmental_due_diligence",
        category="site_assessment",
        summary="Environmental due diligence in real estate and M&A transactions involves Phase I/II ESAs, compliance audits, regulatory database reviews, and liability allocation through contractual mechanisms to manage environmental risk.",
        analysis="Environmental due diligence is a critical component of commercial transactions. Components: (1) Phase I ESA (ASTM E1527-21) — records review, site reconnaissance, interviews to identify RECs. (2) Phase II ESA (ASTM E1903-19) — sampling to confirm or rule out RECs. (3) Compliance audit — review of facility permits, reporting history, enforcement actions, and compliance status. (4) Regulatory database search — CERCLIS/SEMS, NPL, state lists, RCRA generators, LUST, ECHO, state VCP databases. (5) Insurance review — historical CGL policies, current environmental insurance. (6) Environmental liability assessment — quantify known and potential liabilities. (7) Contractual mechanisms: representations and warranties, indemnification (survival period, caps, baskets), escrow holdbacks, purchase price adjustment, insurance requirements, and environmental reserves. (8) CERCLA defense qualification — AAI compliance, BFPP election, innocent purchaser defense. For M&A: evaluate target's entire environmental portfolio including permits, pending enforcement, potential CERCLA sites, compliance history. For real estate: focus on property condition, neighboring site impacts, and vapor intrusion. Lender requirements: Fannie Mae, SBA, CMBS all require Phase I ESA. Cost: Phase I $2,000-$8,000, Phase II $10,000-$100,000+, full environmental audit $25,000-$250,000+.",
        authority="ASTM E1527-21; ASTM E1903-19; 40 CFR 312; CERCLA 101(35)(B)",
        keywords=["environmental due diligence", "transaction", "m&a", "real estate", "phase i", "phase ii", "compliance audit", "indemnification", "reps warranties"],
        statute="42 USC 9601(35)(B)",
        confidence=0.92,
        cross_references=["phase_i_esa", "phase_ii_esa", "cercla_brownfield", "environmental_insurance"],
    ),

    # ---- CERCLA ARAR ----
    DoctrineCacheBlock(
        topic="cercla_arar",
        category="superfund",
        summary="Applicable or Relevant and Appropriate Requirements (ARARs) are federal/state environmental standards that must be met by CERCLA remedial actions, ensuring cleanups achieve at least the level of protection required by other environmental laws.",
        analysis="ARARs are a cornerstone of CERCLA remedy selection. Three categories: (1) Applicable requirements — legally enforceable standards that specifically address a hazardous substance, pollutant, action, or location at the site (e.g., RCRA land disposal restrictions, CWA water quality standards, CAA emission standards). (2) Relevant and appropriate requirements — standards that, while not directly applicable, address problems or situations sufficiently similar that their use is well-suited (e.g., MCLs for groundwater where the aquifer is or could be a drinking water source). (3) To be considered (TBCs) — non-enforceable criteria, advisories, or guidance that are not ARARs but may be useful (e.g., EPA health advisories, ATSDR toxicological profiles). State ARARs must be met if they are more stringent than federal standards and have been timely identified. ARAR waivers are available for: interim measures, equivalent standard of performance, greater risk, technical impracticability, inconsistency with other ARARs, and fund-balancing (Superfund-financed only). ARARs are identified in the ROD and become enforceable cleanup standards. Common ARARs: MCLs (drinking water), effluent standards (discharge), RCRA closure requirements, state RBCA standards.",
        authority="42 USC 9621(d); 40 CFR 300.400(g); 40 CFR 300.430(e)(9)(iii)",
        keywords=["arar", "applicable relevant appropriate", "cleanup standard", "cercla", "remedy selection", "mcl", "waiver", "state standards"],
        statute="42 USC 9621(d)",
        cfr_reference="40 CFR 300.400(g)",
        confidence=0.93,
        cross_references=["cercla_ncp", "cercla_prp_liability", "sdwa_mcl"],
    ),

    # ---- PERMIAN METHANE ----
    DoctrineCacheBlock(
        topic="permian_methane",
        category="permian_basin",
        summary="Methane emissions from Permian Basin oil and gas operations are regulated under EPA NSPS OOOOb/OOOOc, RRC flaring rules, and the IRA methane fee, with significant economic and environmental implications for operators.",
        analysis="The Permian Basin is one of the largest sources of methane emissions in the US. Regulatory framework: (1) EPA NSPS Subpart OOOOb (new sources, 2024) requires LDAR surveys, pneumatic controller standards, well completion controls, compressor seal requirements, storage vessel controls, and the Super-Emitter Response Program enabling third-party reporting of large methane releases detected via satellite or aircraft. (2) Subpart OOOOc (existing sources, 2024) extends many OOOOb requirements to existing operations. (3) IRA Methane Fee (Section 60113) — applies to facilities reporting >25,000 MT CO2e to EPA GHGRP; waste emissions charge starts at $900/ton (2024), $1,200 (2025), $1,500/ton (2026+) for emissions exceeding threshold based on facility type. (4) RRC SWR 32 — prohibits waste of gas; flaring/venting requires permit. (5) Texas SB 1210 (2023) — allows RRC to consider emissions reduction proposals. Measurement: satellite monitoring (TROPOMI, MethaneSAT), aerial surveys (Carbon Mapper), continuous emission monitoring. Major sources: well completions, pneumatic devices, storage tanks, gathering and processing fugitives, produced water tanks. Impact: methane fee could cost large Permian operators millions annually; LDAR programs require significant labor investment; retrofit requirements for existing equipment are substantial.",
        authority="40 CFR Part 60 Subparts OOOOb, OOOOc; IRA Section 60113; 16 TAC 3.32",
        keywords=["methane", "permian basin", "oooo", "ldar", "super emitter", "methane fee", "ira", "flaring", "fugitive emissions"],
        statute="42 USC 7411; IRA P.L. 117-169 Section 60113",
        cfr_reference="40 CFR Part 60 Subparts OOOOb, OOOOc",
        jurisdiction="TX",
        confidence=0.91,
        cross_references=["permian_flaring", "caa_nsps", "rrc_environmental"],
        texas_notes="RRC flaring permits increasingly scrutinized; IRA methane fee creates new financial exposure for Permian operators",
    ),

    # ---- RRC PRODUCED WATER REGULATIONS ----
    DoctrineCacheBlock(
        topic="rrc_produced_water",
        category="rrc",
        summary="RRC regulates produced water disposal and management in Texas through Statewide Rule 9 (disposal wells), Rule 8 (water protection), and evolving rules for beneficial reuse, recycling, and seismicity management.",
        analysis="Produced water management is governed by: (1) SWR 9 (16 TAC 3.9) — authorizes disposal of oil/gas waste into formations not productive of oil/gas or into depleted formations through Class II injection wells. Permits require geological evaluation, area of review, casing/cementing specifications, mechanical integrity testing, and (since 2014) seismicity review. (2) SWR 8 (16 TAC 3.8) — prohibits pollution of surface and subsurface water; requires prevention, monitoring, and cleanup of releases. (3) SWR 36 (16 TAC 3.36) — oil/gas waste management, including pit construction, waste classification, and disposal methods. (4) Texas Water Code Chapter 122 (2023) — authorizes produced water beneficial reuse research and pilot projects, creating a pathway for non-injection disposal. (5) Seismicity: RRC has designated Seismic Response Areas (SRAs) where injection volumes are curtailed; new permits in seismic areas require operator-funded seismic monitoring networks. (6) H-10 permits for surface land application; limited use due to salinity. (7) Water recycling — increasingly adopted by operators; reduces freshwater demand and disposal costs. Currently no comprehensive state permitting program for recycled produced water reuse outside of oilfield operations. TCEQ involvement triggers when produced water leaves oil/gas jurisdiction.",
        authority="16 TAC Chapter 3 (Rules 8, 9, 36, 46); Texas Water Code Chapter 122; RRC Seismicity Orders",
        keywords=["produced water", "rrc", "statewide rule 9", "disposal well", "recycling", "beneficial reuse", "seismicity", "class ii"],
        statute="Texas Natural Resources Code; Texas Water Code Chapter 122",
        cfr_reference="16 TAC Chapter 3",
        jurisdiction="TX",
        confidence=0.93,
        cross_references=["permian_produced_water", "permian_seismicity", "sdwa_uic"],
        texas_notes="RRC seismicity review required for all new/modified disposal permits in SRAs; HB 2771 (2023) enables produced water beneficial reuse research",
    ),

    # ---- TCEQ AIR PERMITS ----
    DoctrineCacheBlock(
        topic="tceq_air_permits",
        category="tceq",
        summary="TCEQ administers air quality permitting in Texas under 30 TAC Chapter 116 (new construction) and Chapter 122 (Title V), offering multiple authorization pathways including standard permits, permits by rule, and case-by-case permits.",
        analysis="Texas air quality permitting under TCEQ provides multiple authorization pathways: (1) New Source Review permits (30 TAC Chapter 116) — required for new construction or modification of facilities. Applications require emission rate calculations, BACT/LAER demonstrations (as applicable), air dispersion modeling, and health effects review. (2) Standard permits (30 TAC 116.611) — pre-approved permits for common facility types with emission caps (e.g., oil and gas production, concrete batch plants, paint/body shops). No case-by-case review required if facility qualifies. (3) Permits by rule (PBR, 30 TAC Chapter 106) — de minimis authorizations for small sources meeting prescribed conditions. Widely used for oil and gas operations (PBR 106.352 for oil and gas facilities). (4) Title V operating permits (30 TAC Chapter 122) — for major sources, consolidating all air requirements. (5) Flexible permits — allow facility-wide emission caps with operational flexibility. TCEQ unique features: no MACT 'gap filling' state program; Texas Standard Exemption 106 is very commonly used for oil/gas sources; compliance history score affects permit proceedings and enforcement. Contested case hearings are available for affected persons. TCEQ processes approximately 6,000 air authorization actions per year.",
        authority="30 TAC Chapters 106, 116, 122; Texas Health & Safety Code Chapter 382",
        keywords=["tceq", "air permit", "standard permit", "permit by rule", "pbr", "title v", "new source review", "texas", "106.352"],
        statute="Texas Health & Safety Code Chapter 382",
        cfr_reference="30 TAC Chapters 106, 116, 122",
        jurisdiction="TX",
        confidence=0.93,
        cross_references=["caa_title_v", "caa_nsr_psd", "caa_neshap"],
        texas_notes="PBR 106.352 is the most commonly used authorization for Permian Basin oil/gas surface facilities; standard permits available for production sites",
    ),

    # ---- CERCLA COST RECOVERY ----
    DoctrineCacheBlock(
        topic="cercla_cost_recovery",
        category="superfund",
        summary="CERCLA Section 107(a) provides the basis for cost recovery actions by EPA, states, and private parties to recover response costs incurred cleaning up hazardous substance releases from responsible parties.",
        analysis="Section 107(a) cost recovery is the primary CERCLA enforcement mechanism. Elements: (1) defendant falls within one of the four PRP categories, (2) there was a release or threatened release of a hazardous substance, (3) from a 'facility,' (4) causing the plaintiff to incur response costs. Response costs must be 'consistent with the NCP' for private party recovery (not required for EPA/state). Strict, joint and several liability applies (subject to Burlington Northern divisibility defense). Statute of limitations: 6 years for remedial action, 3 years for removal action, from completion of the action. Attorney fees are not recoverable under Section 107. Prejudgment interest is available. EPA has a right of subrogation for costs paid from the Superfund. Contribution under Section 113(f) is available to PRPs who have resolved liability with EPA through settlement or judicial determination — contribution claims allow equitable allocation among PRPs. Key distinction: Section 107 = cost recovery (innocent party vs. PRP); Section 113(f) = contribution (PRP vs. PRP). Post-Atlantic Research Corp. (2007), a party that voluntarily cleans up may bring a 107(a) action without first settling with EPA.",
        authority="42 USC 9607(a); United States v. Atlantic Research Corp., 551 U.S. 128 (2007); Cooper Industries v. Aviall Services, 543 U.S. 157 (2004)",
        keywords=["cost recovery", "107", "cercla", "response costs", "ncp consistent", "contribution", "113", "prp", "strict liability"],
        statute="42 USC 9607(a)",
        confidence=0.94,
        cross_references=["cercla_prp_liability", "cercla_ncp", "cercla_brownfield"],
    ),

    # ---- ENVIRONMENTAL LIEN ----
    DoctrineCacheBlock(
        topic="environmental_lien",
        category="compliance_enforcement",
        summary="CERCLA Section 107(l) creates a federal environmental lien on contaminated property where EPA has incurred response costs, subordinate to prior recorded liens but potentially devastating for property values and transactions.",
        analysis="Section 107(l) provides that all response costs for which a person is liable under 107(a) constitute a lien upon all real property belonging to that person that is subject to or affected by a removal or remedial action. The lien: (1) arises at the time costs are first incurred, (2) continues until the liability is satisfied or becomes unenforceable through statute of limitations, (3) is subject to the rights of prior bona fide purchasers (subordinate to prior recorded interests), (4) is not valid against any mortgagee, pledgee, purchaser, or judgment lien creditor until notice is filed in the appropriate office. EPA must provide notice to the property owner before filing the lien. State environmental liens also exist — many states have 'superlien' statutes that give environmental cleanup liens priority over prior recorded liens including mortgages (e.g., Connecticut, Massachusetts, New Jersey). Texas does not have a state environmental superlien. Environmental liens create title defects that must be addressed in transactions. Title insurance companies typically exclude environmental liens. Phase I ESA should identify any recorded environmental liens. CERCLA lien search is part of standard environmental due diligence.",
        authority="42 USC 9607(l); 42 USC 9607(r) (BFPP exemption from lien)",
        keywords=["environmental lien", "cercla lien", "superlien", "107l", "property", "title", "cleanup costs", "response costs"],
        statute="42 USC 9607(l)",
        confidence=0.91,
        cross_references=["cercla_prp_liability", "environmental_disclosure", "phase_i_esa"],
        texas_notes="Texas does not have a state environmental superlien; federal CERCLA lien subordinate to prior recorded interests",
    ),

    # ---- CONSENT DECREES ----
    DoctrineCacheBlock(
        topic="consent_decree",
        category="compliance_enforcement",
        summary="Consent decrees are court-approved settlement agreements between EPA/state and the violator, embodying injunctive relief, compliance schedules, penalties, and supplemental environmental projects enforceable through contempt of court.",
        analysis="Consent decrees are the primary mechanism for resolving federal environmental enforcement actions. Key features: (1) Entered as judicial orders — enforceable through contempt, not just breach of contract. (2) Typically include: injunctive relief (specific actions required), compliance schedule with interim milestones, civil penalty payment, stipulated penalties for future violations, reporting and certification requirements, and dispute resolution procedures. (3) Public comment period required (28 days for DOJ lodged decrees under 28 CFR 50.7). (4) Court must find the decree fair, reasonable, adequate, and consistent with public interest. (5) Modification requires showing of changed circumstances (Rufo v. Inmates of Suffolk County Jail, 502 U.S. 367 (1992)). (6) CERCLA consent decrees often include contribution protection under Section 113(f)(2) — major incentive for settlement. (7) Supplemental Environmental Projects (SEPs) may offset up to 80% of the gravity penalty. (8) EPA tracks all consent decrees in the ECHO database. In CERCLA context, consent decrees may be de minimis (Section 122(g)), cost recovery (Section 107), or remedial action (Section 106/122). Texas TCEQ uses Agreed Orders (administrative equivalent) more frequently than judicial consent decrees.",
        authority="28 CFR 50.7; CERCLA 122 (42 USC 9622); Rufo v. Inmates of Suffolk County Jail, 502 U.S. 367 (1992)",
        keywords=["consent decree", "settlement", "enforcement", "injunctive relief", "stipulated penalty", "contribution protection", "agreed order"],
        statute="42 USC 9622 (CERCLA); various statutes",
        confidence=0.92,
        cross_references=["citizen_suits", "sep", "cercla_prp_liability"],
        texas_notes="TCEQ uses Agreed Orders (30 TAC Chapter 70) as administrative settlement mechanism; judicial consent decrees less common at state level",
    ),

    # ---- NATURAL RESOURCE DAMAGES ----
    DoctrineCacheBlock(
        topic="nrd",
        category="superfund",
        summary="Natural Resource Damage (NRD) claims under CERCLA, OPA, and CWA allow designated natural resource trustees to recover damages for injury, destruction, or loss of natural resources caused by hazardous substance releases or oil spills.",
        analysis="NRD provides compensation beyond cleanup costs for injuries to natural resources held in trust for the public. Legal framework: (1) CERCLA Section 107(a)(4)(C) — damages for injury/destruction/loss of natural resources from hazardous substance releases, assessed using DOI regulations (43 CFR Part 11). (2) OPA Section 1002(b)(2)(A) — damages for injury to natural resources from oil discharges, assessed using NOAA regulations (15 CFR Part 990). (3) CWA Section 311(f) — limited NRD for oil spills predating OPA. Trustees: federal agencies (DOI, NOAA, DOD), state agencies (TCEQ, TPWD in Texas), and tribal governments. Assessment process: (1) preassessment screening, (2) injury determination (documentation that resources were exposed and injured), (3) injury quantification, (4) damage determination (restoration-based under OPA; lesser of restoration cost or diminution in value under CERCLA). Restoration is the preferred remedy. NRD claims have grown significantly — Deepwater Horizon NRD settlement was $8.8 billion. In the Permian Basin, NRD exposure exists for groundwater contamination, habitat destruction, and wildlife impacts from oil/gas operations. Statute of limitations: 3 years from discovery of injury or assessment completion.",
        authority="42 USC 9607(a)(4)(C); 33 USC 2706; 43 CFR Part 11; 15 CFR Part 990; Ohio v. DOI, 880 F.2d 432 (D.C. Cir. 1989)",
        keywords=["natural resource damages", "nrd", "trustee", "restoration", "injury assessment", "doi", "noaa", "cercla", "opa"],
        statute="42 USC 9607(a)(4)(C); 33 USC 2706",
        cfr_reference="43 CFR Part 11; 15 CFR Part 990",
        confidence=0.91,
        cross_references=["cercla_prp_liability", "opa_spcc", "esa_section_7"],
        texas_notes="TCEQ and TPWD are state natural resource trustees in Texas; NRD exposure significant for Permian Basin groundwater contamination",
    ),

    # ---- UNDERGROUND INJECTION CONTROL (expanded from SDWA) ----
    DoctrineCacheBlock(
        topic="uic_class_vi",
        category="drinking_water",
        summary="UIC Class VI wells are specifically designed for geologic sequestration of carbon dioxide (CO2), subject to rigorous SDWA requirements to protect USDWs from injected CO2 and displaced brine.",
        analysis="Class VI wells were established by EPA in 2010 specifically for CO2 geologic sequestration (GS). Key requirements: (1) extensive site characterization including geological, geochemical, and geomechanical modeling, (2) area of review must evaluate the entire plume extent and pressure front, (3) well construction with CO2-resistant materials (corrosion-resistant cement and casing), (4) comprehensive monitoring: operational (pressure, injection rate, annulus), groundwater quality, CO2 plume tracking (seismic, logging), and surface air monitoring, (5) emergency and remedial response plan, (6) post-injection site care (PISC) and site closure — minimum 50-year PISC period (reducible on demonstration), (7) financial responsibility for entire project lifecycle including PISC, (8) pre-operational testing including MIT and injectivity testing. EPA Class VI primacy: only North Dakota and Wyoming have primacy; other states (including Texas) must obtain permits from EPA Region 6 (or other applicable region). The IRA Section 45Q tax credit ($85/ton for geological storage) has driven enormous interest in Class VI permits — EPA backlog of applications is significant. In Texas, RRC has applied for Class VI primacy; until approved, EPA retains authority. Key challenge: distinguishing Class II enhanced oil recovery with incidental CO2 storage from Class VI dedicated storage.",
        authority="42 USC 300h; 40 CFR 146 Subpart H; 75 FR 77230 (2010 final rule); IRA Section 45Q",
        keywords=["class vi", "carbon sequestration", "co2", "geologic storage", "uic", "45q", "post injection site care", "pisc"],
        statute="42 USC 300h",
        cfr_reference="40 CFR 146 Subpart H",
        confidence=0.90,
        cross_references=["sdwa_uic", "carbon_credits", "climate_regulation"],
        texas_notes="RRC applied for Class VI primacy (pending); EPA Region 6 currently issues Texas Class VI permits; major 45Q-driven activity in Permian Basin",
    ),

    # ---- ENVIRONMENTAL STANDING ----
    DoctrineCacheBlock(
        topic="environmental_standing",
        category="compliance_enforcement",
        summary="Standing in environmental cases requires injury in fact, causation, and redressability, with key precedents establishing that procedural injuries (NEPA violations) and aesthetic/recreational injuries qualify if sufficiently particularized.",
        analysis="Environmental standing under Article III requires: (1) Injury in fact — concrete, particularized, and actual/imminent. In environmental cases: aesthetic injury (Sierra Club v. Morton, 405 U.S. 727 (1972)), recreational use injury, health concerns from pollution exposure, and property value diminution all qualify. Organizational standing requires showing members would have standing individually, interests at stake are germane to the organization's purpose, and neither the claim nor relief requires individual member participation. (2) Causation — fairly traceable to the challenged action. In Massachusetts v. EPA, state standing benefited from 'special solicitude.' (3) Redressability — favorable decision must likely remedy the injury. Procedural injury (e.g., agency failed to prepare EIS): plaintiff need not show the EIS would have changed the outcome, only that the procedure was legally required and the procedural violation increased the risk of harm. Lujan v. Defenders of Wildlife (504 U.S. 555 (1992)) established strict standing requirements. Friends of the Earth v. Laidlaw (528 U.S. 167 (2000)) held standing exists where pollution deterred recreational use, even without proof of actual environmental harm. Recent cases: TransUnion (2021) tightened standing for statutory violations without concrete harm. In practice: environmental plaintiffs must submit detailed declarations demonstrating personal use of and connection to the affected area.",
        authority="Sierra Club v. Morton, 405 U.S. 727 (1972); Lujan v. Defenders of Wildlife, 504 U.S. 555 (1992); Friends of the Earth v. Laidlaw, 528 U.S. 167 (2000); Massachusetts v. EPA, 549 U.S. 497 (2007)",
        keywords=["standing", "article iii", "injury in fact", "causation", "redressability", "environmental plaintiff", "organizational standing", "procedural injury"],
        statute="Article III; Administrative Procedure Act",
        confidence=0.93,
        cross_references=["citizen_suits", "nepa_eis"],
        practice_tips=[
            "Standing declarations must be specific — identify the individual, their personal use of the affected area, and how the challenged action injures them",
            "Procedural injury standing (NEPA, ESA consultation) is more forgiving than substantive injury standing",
            "Organizational standing requires at least one member with individual standing",
        ],
    ),

    # ---- ENFORCEMENT PRIORITIES ----
    DoctrineCacheBlock(
        topic="epa_enforcement_priorities",
        category="compliance_enforcement",
        summary="EPA's National Enforcement and Compliance Initiatives (NECIs) identify priority areas for enforcement focus, currently including PFAS, climate/methane, environmental justice, coal combustion residuals, and hazardous air pollutants.",
        analysis="EPA establishes National Enforcement and Compliance Initiatives (NECIs) for 3-year cycles. Current FY2024-2027 priorities: (1) Mitigating Climate Change — reducing GHG emissions from largest sources including oil/gas methane, power sector, and industrial sources. (2) Addressing Exposure to PFAS — enforcement against PFAS manufacturers, dischargers, and facilities. (3) Protecting Communities from Coal Ash Contamination — CCR Rule implementation and groundwater monitoring. (4) Reducing Air Toxics — NESHAP compliance for facilities in overburdened communities. (5) Increasing Compliance with Drinking Water Standards — SDWA compliance including lead and copper. (6) Reducing Hazardous Air Emissions and Ensuring Compliance at Facilities in Communities with Environmental Justice Concerns. EPA enforcement tools: administrative compliance orders (Section 309/CWA, Section 113/CAA, Section 3008/RCRA), administrative penalty orders, civil judicial actions (DOJ referral), and criminal prosecution. Supplemental enforcement tools: ECHO database (public compliance data), Next Generation Compliance (electronic reporting, transparency), and third-party audits. EPA Region 6 (Texas, Louisiana, Oklahoma, Arkansas, New Mexico) focuses on oil/gas, refining, petrochemical, and environmental justice communities. TCEQ has its own enforcement priorities and compliance history program (30 TAC Chapter 60) that assigns compliance scores to regulated entities.",
        authority="EPA NECIs FY2024-2027; CAA 113, CWA 309, RCRA 3008, CERCLA 106",
        keywords=["enforcement", "neci", "compliance initiative", "epa priority", "pfas", "methane", "environmental justice", "echo", "region 6"],
        statute="Multiple enforcement authorities",
        confidence=0.90,
        cross_references=["citizen_suits", "consent_decree", "sep"],
        texas_notes="EPA Region 6 in Dallas covers Texas; TCEQ compliance history program (30 TAC Chapter 60) assigns compliance scores affecting permitting and enforcement",
    ),

    # ---- WASTE CLASSIFICATION ----
    DoctrineCacheBlock(
        topic="waste_classification",
        category="hazardous_waste",
        summary="RCRA waste classification determines whether a solid waste is hazardous through a systematic process: listed waste identification (F, K, U, P lists), characteristic testing (ignitability, corrosivity, reactivity, toxicity), and application of exclusions and exemptions.",
        analysis="The waste classification process under 40 CFR 261 determines regulatory obligations: (1) Is it a solid waste? — must be a discarded material (abandoned, recycled, or inherently waste-like). (2) Is it excluded? — key exclusions include domestic sewage, CWA point source discharge, irrigation return flow, nuclear material, and the oil and gas exploration and production (E&P) waste exemption (40 CFR 261.4(b)(5)). The E&P exemption is critically important in the Permian Basin — it exempts drilling fluids, produced water, and other wastes intrinsically derived from primary field operations. (3) Is it listed? — F list (non-specific sources, e.g., F001-F005 spent solvents), K list (specific sources, e.g., K048-K052 petroleum refining), U list (discarded commercial chemical products), P list (acutely hazardous commercial chemical products). (4) Is it characteristic? — ignitability (D001, flash point <140F), corrosivity (D002, pH <2 or >12.5), reactivity (D003), toxicity (D004-D043, TCLP testing). (5) Mixture rule: mixing listed waste with non-hazardous = all hazardous (with exceptions for wastewater). (6) Derived-from rule: residue from treating listed waste = listed waste. (7) Contained-in policy: media contaminated with listed waste must be managed as hazardous until delisted. (8) Generator knowledge vs. testing: generators may use knowledge of processes to classify waste, but must be able to demonstrate the basis.",
        authority="40 CFR Part 261; 45 FR 33084 (1980); Chemical Waste Management v. EPA, 976 F.2d 2 (D.C. Cir. 1992)",
        keywords=["waste classification", "rcra", "listed waste", "characteristic waste", "f list", "k list", "u list", "p list", "tclp", "e&p exemption", "mixture rule"],
        statute="42 USC 6921",
        cfr_reference="40 CFR Part 261",
        confidence=0.94,
        cross_references=["rcra_subtitle_c", "rcra_corrective_action"],
        texas_notes="E&P waste exemption (40 CFR 261.4(b)(5)) is critical for Permian Basin operators — exempts most exploration and production wastes from RCRA Subtitle C",
    ),

    # ---- VAPOR INTRUSION ----
    DoctrineCacheBlock(
        topic="vapor_intrusion",
        category="remediation",
        summary="Vapor intrusion occurs when volatile contaminants in soil or groundwater migrate as vapors through the subsurface and into overlying buildings, posing indoor air health risks and requiring evaluation under CERCLA, RCRA, and state cleanup programs.",
        analysis="Vapor intrusion (VI) has become a major environmental concern and regulatory focus. EPA's 2015 Technical Guide for Assessing and Mitigating the Vapor Intrusion Pathway establishes the framework: (1) Screening — use EPA VISS (Vapor Intrusion Screening Levels) to compare subsurface data to screening criteria. If groundwater or soil gas concentrations exceed screening levels, further assessment needed. (2) Investigation — subsurface soil gas sampling (probes), sub-slab soil gas sampling, indoor air sampling, outdoor air sampling. Multiple sampling events recommended to account for temporal variability. (3) Attenuation factors — EPA default: 0.03 (soil gas to indoor air) for residential; site-specific factors preferred. (4) Risk assessment — compare indoor air concentrations to EPA RSLs or state-specific standards. (5) Mitigation — sub-slab depressurization systems (SSD/SSDS) are the most common mitigation approach (similar to radon mitigation), passive barriers, vapor recovery systems, building pressurization, or institutional controls. ASTM E1527-21 now mandates vapor intrusion screening as part of Phase I ESA — this is a significant change from the 2013 standard. ASTM E2600-15 provides the vapor encroachment screening standard. Petroleum VI guidance (EPA 2015) recognizes that petroleum compounds biodegrade in the vadose zone, potentially reducing VI risk (PVI screen). State programs vary widely — Texas TCEQ addresses VI under 30 TAC 350 (TRRP) and the LPST program.",
        authority="EPA OSWER 9200.2-154 (2015 VI Technical Guide); ASTM E1527-21 Section 8.2.1; ASTM E2600-15; 30 TAC 350 (Texas TRRP)",
        keywords=["vapor intrusion", "indoor air", "sub-slab", "soil gas", "volatile", "screening", "viss", "mitigation", "ssds", "phase i"],
        statute="CERCLA/RCRA (cleanup authority); ASTM E1527-21",
        confidence=0.91,
        cross_references=["phase_i_esa", "phase_ii_esa", "rcra_corrective_action", "tceq_vcp"],
        texas_notes="TCEQ evaluates VI under TRRP (30 TAC 350); petroleum VI guidance accounts for biodegradation; LPST program addresses UST-related VI",
    ),

    # ---- STORMWATER MANAGEMENT ----
    DoctrineCacheBlock(
        topic="stormwater_management",
        category="water_quality",
        summary="CWA stormwater regulation requires NPDES/TPDES permits for construction activities disturbing 1+ acres, industrial facilities with SIC codes exposed to stormwater, and MS4s, implemented through SWPPPs and BMPs.",
        analysis="Stormwater permitting under CWA Section 402(p) covers three categories: (1) Construction General Permit (CGP) — required for construction activities disturbing 1+ acres (or smaller sites part of a larger common plan). Requires SWPPP with erosion and sediment controls, post-construction stormwater management, and inspection schedule. In Texas, TCEQ issues the CGP (TPDES TXR150000). (2) Multi-Sector General Permit (MSGP) — covers industrial stormwater discharges from 29 industrial sectors (based on SIC codes). Requires SWPPP, monitoring/sampling, and sector-specific requirements. Texas equivalent: TPDES TXR050000. (3) MS4 permits — Municipal Separate Storm Sewer Systems serving populations >100,000 (Phase I) or smaller (Phase II, >1,000 in urbanized areas). Requires six minimum control measures: public education, public participation, illicit discharge detection, construction stormwater management, post-construction management, and good housekeeping. Key compliance issues: (a) turbidity exceedances during construction, (b) failure to maintain BMPs, (c) inadequate SWPPP documentation, (d) failure to conduct required inspections (within 24 hours of 0.5+ inch rainfall event). No-exposure certification available for industrial facilities where all materials/activities are covered. Penalties for stormwater violations: up to $64,618/day (federal) or $25,000/day (Texas).",
        authority="33 USC 1342(p); 40 CFR 122.26; TPDES TXR150000, TXR050000; 30 TAC Chapter 305",
        keywords=["stormwater", "swppp", "construction general permit", "ms4", "bmp", "erosion control", "sediment", "multi sector", "cgp", "msgp"],
        statute="33 USC 1342(p)",
        cfr_reference="40 CFR 122.26",
        confidence=0.92,
        cross_references=["cwa_npdes", "cwa_tmdl"],
        texas_notes="TCEQ issues construction (TXR150000) and industrial (TXR050000) stormwater general permits; MS4 permits for Texas urbanized areas",
    ),

    # ---- TSCA ASBESTOS ----
    DoctrineCacheBlock(
        topic="tsca_asbestos",
        category="toxic_substances",
        summary="Asbestos is regulated under TSCA, CAA NESHAP, and OSHA standards, with requirements for building inspection, management, abatement, disposal, and worker protection, plus EPA's 2024 comprehensive ban on chrysotile asbestos.",
        analysis="Asbestos regulation spans multiple statutes: (1) TSCA — EPA issued a comprehensive ban on chrysotile asbestos in March 2024 (final rule under amended TSCA Section 6), phasing out remaining uses over 2-12 years. Previous ban (1989) was overturned by Corrosion Proof Fittings (5th Cir. 1991). (2) CAA NESHAP (40 CFR 61 Subpart M) — requires notification before demolition/renovation of facilities with regulated asbestos-containing materials (RACM), wet removal, no visible emissions, proper disposal at licensed landfills. Applies to commercial and public buildings. (3) OSHA standards (29 CFR 1926.1101) — construction industry standard for asbestos exposure; PEL of 0.1 f/cc TWA. Classes I-IV of asbestos work with decreasing exposure potential. (4) AHERA (Asbestos Hazard Emergency Response Act) — requires inspection and management plans for K-12 schools. (5) State requirements — Texas DSHS licenses asbestos abatement contractors, consultants, and workers; 25 TAC Chapter 295 Subchapter C. Building surveys must identify all ACM before renovation/demolition. ACM disposal at specially licensed landfills with recordkeeping. Liability: building owners liable for worker/tenant exposure; asbestos litigation is the longest-running mass tort in US history.",
        authority="15 USC 2605 (TSCA Section 6); 40 CFR 61 Subpart M; 29 CFR 1926.1101; 15 USC 2641-2656 (AHERA); 25 TAC 295 Subchapter C (Texas)",
        keywords=["asbestos", "tsca", "neshap", "abatement", "acm", "ahera", "chrysotile", "demolition", "renovation", "building survey"],
        statute="15 USC 2605; 42 USC 7412 (CAA); 15 USC 2641 (AHERA)",
        cfr_reference="40 CFR 61 Subpart M; 29 CFR 1926.1101",
        confidence=0.93,
        cross_references=["tsca_chemical_review", "caa_neshap", "toxic_tort"],
        texas_notes="Texas DSHS licenses asbestos professionals; 25 TAC Chapter 295; notification required 10 days before demolition/renovation with ACM",
    ),
    # ========================================================================
    # ADDITIONAL DOCTRINE BLOCKS — EXPANDED COVERAGE
    # ========================================================================
    DoctrineCacheBlock(
        topic="mprsa_ocean_dumping",
        category="water_quality",
        summary="The Marine Protection, Research, and Sanctuaries Act (MPRSA/Ocean Dumping Act) prohibits unpermitted dumping of material into ocean waters, with EPA regulating most materials and USACE regulating dredged material under Section 103 permits.",
        analysis="The MPRSA (33 USC 1401-1445) prohibits transportation of material from the US for ocean dumping without an EPA permit. Key provisions: (1) EPA designates ocean disposal sites and sets site management/monitoring plans. (2) USACE issues Section 103 permits for dredged material disposal at EPA-designated sites, subject to EPA concurrence on environmental criteria (40 CFR 227). (3) Prohibited materials include radiological/chemical/biological warfare agents, high-level radioactive waste, and medical waste. (4) Permit criteria under 40 CFR 227 require need for dumping, no practicable alternative, no unreasonable degradation. (5) EPA can designate sites or withdraw designation. (6) Criminal penalties for unpermitted ocean dumping up to $50,000 per violation and/or imprisonment. (7) The 1988 amendments phased out ocean dumping of sewage sludge and industrial waste. (8) Title III establishes the National Marine Sanctuary Program (now under NOAA). (9) Dredged material must meet bioassay testing requirements (Green Book/Ocean Testing Manual). (10) International obligations under London Convention and London Protocol.",
        authority="33 USC 1401-1445; 40 CFR Parts 220-229; 33 CFR 324-325 (USACE permits)",
        keywords=["ocean dumping", "mprsa", "dredged material", "marine protection", "ocean disposal", "marine sanctuary"],
        statute="33 USC 1401-1445",
        cfr_reference="40 CFR 220-229; 33 CFR 324-325",
        confidence=0.89,
        cross_references=["cwa_section_404", "cwa_npdes"],
        texas_notes="Texas Gulf Coast dredging projects require USACE Section 103 permits for ocean disposal of dredged material; TCEQ may also require CWA Section 401 certification",
    ),
    DoctrineCacheBlock(
        topic="tceq_air_permits",
        category="tceq",
        summary="TCEQ administers air quality permits in Texas under delegated Clean Air Act authority, including New Source Review (NSR), Title V federal operating permits, Permits by Rule (PBR), and Standard Permits for various facility types.",
        analysis="Texas air permitting is administered by TCEQ under 30 TAC Chapters 106 (PBR), 116 (NSR), and 122 (Title V). Key framework: (1) New Source Review — required for new or modified sources of air contaminants; major sources must go through Prevention of Significant Deterioration (PSD) in attainment areas or Nonattainment NSR in nonattainment areas. Minor NSR for sources below major thresholds. (2) Permit by Rule (30 TAC 106) — pre-authorized permits for specific activities with defined emission limits; no individual application required if conditions met. Commonly used PBRs: 106.261 (facilities installations), 106.352 (oil and gas), 106.511 (rock crushers). (3) Standard Permits (30 TAC 116 Subchapter F) — pre-authorized for specific source categories; more flexibility than PBR but less review than NSR. (4) Title V Operating Permits — federally enforceable consolidation of all applicable requirements for major sources. 5-year renewal cycle. (5) Flexible Permits — Texas-specific; cap emissions at facility level rather than unit-by-unit. (6) BACT/LAER requirements for major new sources. (7) Public participation required for NSR permits; contested case hearings at SOAH. (8) Emissions Events — required reporting under 30 TAC 101.201/101.211 for unauthorized emissions. (9) Emissions inventory reporting under 30 TAC 101.10. (10) Shutdown/startup exemptions have been narrowed; EPA 2015 SSM SIP Call requirements.",
        authority="30 TAC Chapters 106, 116, 122; 42 USC 7401 et seq.; 40 CFR Parts 51, 52, 70, 71; EPA-approved Texas SIP",
        keywords=["tceq", "air permit", "nsr", "title v", "pbr", "permit by rule", "standard permit", "emissions", "texas air quality", "bact"],
        statute="42 USC 7401 (CAA); Texas Health & Safety Code Chapter 382",
        cfr_reference="30 TAC 106, 116, 122; 40 CFR 52.2270 (Texas SIP)",
        confidence=0.94,
        cross_references=["caa_nsps", "caa_naaqs", "permian_flaring"],
        practice_tips=[
            "Check PBR applicability first — avoids months of NSR review",
            "Track emissions events carefully — failure to report triggers enforcement",
            "Flexible permits offer operational flexibility but limit transferability",
        ],
        texas_notes="TCEQ Region 7 (Midland) handles Permian Basin air permits; standard processing time 6-12 months for NSR; PBR registration is immediate if conditions met",
    ),
    DoctrineCacheBlock(
        topic="tceq_water_permits",
        category="tceq",
        summary="TCEQ administers water quality permits in Texas including TPDES (Texas Pollutant Discharge Elimination System), water rights, stormwater, and pretreatment program authorization under delegated CWA and state water code authority.",
        analysis="Texas water permitting framework: (1) TPDES permits — Texas received CWA delegation from EPA in 1998; TCEQ issues individual TPDES permits for point source discharges (industrial, municipal). General permits available for specific discharge categories (TXG permits). (2) Water Rights — under Texas Water Code, surface water belongs to the state; appropriative rights system administered by TCEQ. Requires permit for any diversion, impoundment, or use of state surface water. Exempt domestic/livestock use up to 200 acre-feet. (3) Stormwater — construction general permit (TXR150000), multi-sector general permit (TXR050000), and MS4 permits for municipalities. Construction sites >1 acre need SWPPP and NOT. (4) Pretreatment — TCEQ oversees approved pretreatment programs for POTWs accepting industrial discharges. (5) Aquifer protection — 30 TAC Chapter 331 for injection wells (coordinated with EPA UIC program). (6) Water quality standards — Texas Surface Water Quality Standards (30 TAC 307) define designated uses, criteria, and antidegradation policy. (7) Edwards Aquifer protection — 30 TAC 213 for activities over contributing/recharge zones. (8) Groundwater — rule of capture in Texas, but groundwater conservation districts have regulatory authority. (9) Reclaimed water — 30 TAC 210 governs reuse of treated effluent. (10) 401 certification — TCEQ issues CWA Section 401 water quality certifications for federal permits/licenses.",
        authority="Texas Water Code Chapters 11, 26; 30 TAC Chapters 210, 213, 307, 309, 311, 319, 321; 33 USC 1251 (CWA)",
        keywords=["tceq", "tpdes", "water permit", "water rights", "stormwater", "pretreatment", "edwards aquifer", "water quality"],
        statute="33 USC 1251 (CWA); Texas Water Code",
        cfr_reference="30 TAC 307, 309, 311, 319, 321; 40 CFR 122 (NPDES delegation)",
        confidence=0.93,
        cross_references=["cwa_npdes", "cwa_section_404", "sdwa_underground_injection"],
        practice_tips=[
            "Construction stormwater permits (TXR150000) must be obtained BEFORE ground disturbance",
            "Edwards Aquifer protection plans required for development over recharge/contributing zones",
            "Water rights applications can take 1-3 years; consider temporary permits for interim needs",
        ],
        texas_notes="TCEQ is the delegated NPDES authority in Texas; EPA retains oversight and can object to individual permits within 90 days of public notice",
    ),
    DoctrineCacheBlock(
        topic="rrc_well_plugging",
        category="rrc",
        summary="The Railroad Commission of Texas requires proper plugging of oil and gas wells upon cessation of operations, with specific procedures, bonding requirements, and the Orphan Well Program for wells with no solvent operator.",
        analysis="RRC well plugging requirements under Statewide Rules and 16 TAC Chapter 3: (1) Plugging obligation — operator must plug well within one year of cessation of operations or obtain an extension. Rule 14 (16 TAC 3.14) sets plugging procedures. (2) Plugging methods — cement must isolate all productive zones, freshwater zones, and surface. Bottom plug, intermediate plugs, and surface plug required. Cement must set before testing. (3) Financial security — operators must maintain organizational report (P-5), financial assurance (bonds, letters of credit), and comply with well compliance requirements. Base bond amounts range from $25,000 (single well) to $250,000 (blanket bond for 100+ wells). (4) Orphan wells — when operator is insolvent/unknown, RRC's Oil Field Cleanup Fund pays for plugging and remediation. Fund financed by operator fees and legislative appropriations. (5) Well transfer — Rule 79 requires financial capability review before well transfers; prevents transfer to operators unable to plug. (6) Violations — failure to plug subjects operator to penalties of up to $10,000/day, certificate revocation, and personal liability of corporate officers. (7) Plugging exceptions — wells may be designated as inactive if maintained and tested (Rule 14(b)(2)). (8) State-managed plugging projects — RRC may use contractors for orphan/abandoned well plugging. (9) Federal infrastructure funding — Bipartisan Infrastructure Law (2021) allocated $4.7B for orphaned well plugging, including allocation to Texas. (10) H2S wells — special plugging requirements for sour wells under Rule 36.",
        authority="16 TAC 3.14 (Rule 14); 16 TAC 3.78 (Rule 78); 16 TAC 3.79 (Rule 79); Texas Natural Resources Code Chapter 89",
        keywords=["rrc", "well plugging", "orphan well", "p5", "bond", "abandonment", "inactive well", "oil field cleanup"],
        statute="Texas Natural Resources Code Chapters 85, 89, 91",
        cfr_reference="16 TAC Chapter 3",
        confidence=0.94,
        cross_references=["rrc_environmental", "permian_produced_water", "permian_seismicity"],
        practice_tips=[
            "Track well status carefully — inactive wells require annual compliance testing",
            "Before acquiring wells, verify plugging liability exposure and bond adequacy",
            "Federal orphan well funding may be available through state allocation programs",
        ],
        texas_notes="RRC administers approximately 8,000 orphan well sites statewide; Permian Basin has highest concentration of orphan wells requiring plugging",
    ),
    DoctrineCacheBlock(
        topic="nepa_categorical_exclusion",
        category="nepa",
        summary="Categorical Exclusions (CatExs/CEs) are categories of federal actions that normally do not individually or cumulatively have a significant environmental effect, exempting them from EA or EIS requirements under NEPA unless extraordinary circumstances exist.",
        analysis="NEPA Categorical Exclusions (40 CFR 1508.1(d), CEQ regulations 2020/2024): (1) Definition — actions that the agency has determined, through experience, normally do not individually or cumulatively have significant environmental effects. Each federal agency establishes its own list of CEs in agency NEPA procedures. (2) Establishment — agencies must substantiate CEs with documentation, often through programmatic reviews. New CEs require public comment. (3) Extraordinary circumstances — even if an action fits a CE, the agency must check for extraordinary circumstances that might trigger significant impacts: endangered species habitat, historic properties, wetlands, floodplains, hazardous waste, environmental justice, etc. (4) Documentation — some CEs require no documentation; others require a brief record documenting the CE applicability and extraordinary circumstances check. (5) FAST-41 and Fiscal Responsibility Act of 2023 — expanded use of CEs; allows agencies to adopt other agencies' CEs for similar actions. (6) Common federal agency CEs: DOI — routine maintenance, minor renovation; DOE — administrative actions, categorical exclusions in Appendix A/B; USACE — nationwide permits (CWA Section 404); EPA — administrative grants, minor facility modifications. (7) Judicial review — courts may invalidate CE use where agency failed to consider extraordinary circumstances or where action does not fit CE description (Wilderness Society v. Wisely, Center for Biological Diversity v. Salazar). (8) CEQ 2024 Phase 2 regulations revised CE requirements. (9) Environmental justice must be considered even for CEs under EO 12898 and recent guidance. (10) Cumulative effects of multiple CEs in same area may trigger need for EA/EIS.",
        authority="42 USC 4332 (NEPA Section 102); 40 CFR 1501.4, 1508.1(d); CEQ NEPA regulations (2020, 2024 Phase 2)",
        keywords=["nepa", "categorical exclusion", "catex", "ce", "extraordinary circumstances", "environmental review", "federal action"],
        statute="42 USC 4321-4347",
        cfr_reference="40 CFR 1501.4, 1508.1(d)",
        confidence=0.91,
        cross_references=["nepa_eis", "nepa_ea", "esa_section_7"],
        texas_notes="Federal actions in Texas (USACE permits, BLM leases, DOE loans) may qualify for CEs; state-only actions not subject to NEPA unless federal nexus exists",
    ),
    DoctrineCacheBlock(
        topic="esa_critical_habitat",
        category="endangered_species",
        summary="Critical habitat designation under ESA Section 4 identifies specific geographic areas essential for the conservation of listed species, triggering Section 7 consultation requirements for federal actions that may adversely modify designated critical habitat.",
        analysis="ESA Critical Habitat (16 USC 1533(a)(3), (b)(2)): (1) Designation — USFWS/NMFS must designate critical habitat concurrently with listing, to the maximum extent prudent and determinable. Based on best available science and after considering economic impacts. (2) Components — physical or biological features (PBFs) essential for conservation: space, food/water, cover, breeding sites, and features required for each life stage. (3) Occupied vs. unoccupied habitat — occupied areas require PBFs; unoccupied areas can be designated only if essential for conservation and must contain PBFs or have potential to develop them. (4) Exclusion authority — Secretary may exclude areas if benefits of exclusion outweigh inclusion, unless exclusion would result in species extinction. Economic analysis required (Executive Order, court rulings). (5) Section 7 adverse modification standard — federal agencies must ensure actions are not likely to result in destruction or adverse modification of critical habitat. Separate from jeopardy standard. 2016 definition: action that appreciably diminishes the value of critical habitat as a whole. (6) No direct regulation of private land — critical habitat imposes no restrictions on private actions without a federal nexus. But presence of critical habitat often delays or modifies federal permits. (7) Texas species with critical habitat: golden-cheeked warbler, black-capped vireo, whooping crane, Texas hornshell mussel, numerous aquatic species in Edwards Aquifer system. (8) Permian Basin — several candidate species and proposed critical habitat designations may affect oil and gas operations on federal/state lands. (9) Judicial review — designation challenges common on both scientific and economic grounds. (10) Recovery plans may inform but are not equivalent to critical habitat designation.",
        authority="16 USC 1533(a)(3), (b)(2); 50 CFR 424; ESA Section 4(b)(2) economic exclusion; Weyerhaeuser Co. v. USFWS (2018)",
        keywords=["esa", "critical habitat", "endangered species", "section 7", "adverse modification", "designation", "conservation"],
        statute="16 USC 1531-1544",
        cfr_reference="50 CFR 424",
        confidence=0.92,
        cross_references=["esa_section_7", "esa_incidental_take", "nepa_eis"],
        texas_notes="Golden-cheeked warbler critical habitat covers 33 Texas counties; dunes sagebrush lizard habitat discussions directly affect Permian Basin operations in Andrews, Crane, Gaines, Ward, and Winkler counties",
    ),
    DoctrineCacheBlock(
        topic="sdwa_underground_injection",
        category="drinking_water",
        summary="The Underground Injection Control (UIC) program under SDWA regulates injection wells in six classes to protect underground sources of drinking water (USDWs), with EPA or delegated state programs issuing permits and setting construction, operation, and closure standards.",
        analysis="UIC program under SDWA Part C (42 USC 300h): (1) Six well classes — Class I: industrial/municipal hazardous and non-hazardous waste; Class II: oil/gas production-related (disposal, enhanced recovery, hydrocarbon storage); Class III: solution mining; Class IV: hazardous waste into/above USDWs (banned with limited exceptions); Class V: all other injection wells not in Classes I-IV; Class VI: geologic sequestration of CO2. (2) Primacy — states may obtain primacy for UIC enforcement; Texas has primacy for Class I (TCEQ) and Class II (RRC). EPA directly administers in non-primacy states. (3) Class II wells (oil and gas) — most numerous class; Texas RRC regulates approximately 53,000 active Class II wells. Permits require demonstration of mechanical integrity (MIT) testing, area of review, casing/cementing standards, and USDW protection. (4) Class VI wells (CO2 sequestration) — established by 2010 EPA rule; most stringent requirements including comprehensive site characterization, AoR/corrective action, financial responsibility, post-injection site care (50 years default), and emergency/remedial response plan. Texas applied for and received Class VI primacy (2023). (5) Mechanical integrity testing — required initially and periodically (every 5 years for Class II); annular pressure testing and cementing evaluation. (6) Area of review — radius around well where USDWs could be affected; varies by class (1/4 mile default for Class II, computed zone for Class VI). (7) Aquifer exemption — EPA or state may exempt aquifers that are mineral-producing, too deep/saline for beneficial use, or contaminated beyond remediation. (8) Penalties — up to $25,000/day civil; criminal penalties for knowing violations. (9) Emergency powers — EPA can take action if contamination may present imminent/substantial endangerment to health. (10) Relationship to RCRA — Class I hazardous waste wells must also meet RCRA Subtitle C requirements (40 CFR 148 land disposal restrictions).",
        authority="42 USC 300h (SDWA Part C); 40 CFR 144-148; 16 TAC Chapter 3 (RRC Class II); 30 TAC Chapter 331 (TCEQ Class I/III/V)",
        keywords=["uic", "underground injection", "sdwa", "class ii", "class vi", "disposal well", "injection well", "usdw", "aquifer"],
        statute="42 USC 300h-300h-8",
        cfr_reference="40 CFR 144-148; 16 TAC 3.9, 3.46; 30 TAC 331",
        confidence=0.94,
        cross_references=["sdwa_mcl", "rrc_environmental", "permian_produced_water", "uic_class_vi"],
        practice_tips=[
            "Class II permits require Area of Review analysis — check for unplugged wellbores within 1/4 mile",
            "MIT testing failures can result in well shut-in; maintain regular testing schedule",
            "Class VI primacy in Texas (effective 2023) means RRC handles CO2 sequestration well permits",
        ],
        texas_notes="RRC has Class II primacy; TCEQ has Class I/III/V primacy; Texas received Class VI primacy in 2023; approximately 53,000 active Class II wells statewide, heavily concentrated in Permian Basin",
    ),
    DoctrineCacheBlock(
        topic="rcra_corrective_action",
        category="hazardous_waste",
        summary="RCRA corrective action (Section 3004(u)/(v), Section 3008(h)) requires investigation and cleanup of releases of hazardous waste and constituents at facilities seeking or holding RCRA permits, covering all solid waste management units (SWMUs) at the facility.",
        analysis="RCRA Corrective Action: (1) Trigger — Section 3004(u) requires corrective action for all releases from any SWMU at a facility seeking a RCRA permit, regardless of when waste was placed in the unit. Section 3004(v) extends to releases beyond facility boundary. Section 3008(h) authorizes EPA to issue corrective action orders at interim status facilities. (2) Process — RFI (RCRA Facility Investigation) identifies nature/extent of contamination; CMS (Corrective Measures Study) evaluates remedy alternatives; CMI (Corrective Measures Implementation) implements selected remedy. (3) Environmental Indicators (EIs) — EPA tracks two key indicators: human exposures under control (CA725) and migration of contaminated groundwater under control (CA750). (4) Scope — covers all SWMUs (not just hazardous waste units); includes areas of concern (AOCs) identified during investigations. Broader scope than CERCLA in that it applies to all releases from any waste management unit. (5) Financial assurance — required for corrective action under RCRA permit conditions (40 CFR 264.101). (6) Remedy selection — must protect human health and environment, attain media cleanup standards, control sources, comply with waste management standards. Flexibility in setting site-specific cleanup levels based on risk assessment. (7) Relationship to CERCLA — dual-track facilities may have both RCRA corrective action and CERCLA obligations; EPA/state coordination determines lead authority. (8) State authorization — 46 states authorized for corrective action base program. Texas TCEQ has authorization and runs RCRA corrective action program under 30 TAC 335. (9) Brownfields — RCRA corrective action completion facilitates brownfield redevelopment; Ready for Reuse determinations available. (10) Interim measures — immediate actions to address imminent threats before full remedy selected.",
        authority="42 USC 6924(u),(v) (RCRA 3004); 42 USC 6928(h) (RCRA 3008(h)); 40 CFR 264.100-101; EPA RCRA Corrective Action ANPR (1996); 30 TAC 335 (Texas)",
        keywords=["rcra", "corrective action", "swmu", "rfi", "cms", "cmi", "hazardous waste", "cleanup", "facility investigation"],
        statute="42 USC 6924(u), 6924(v), 6928(h)",
        cfr_reference="40 CFR 264.100-101; 40 CFR 264 Subpart F; 30 TAC 335",
        confidence=0.93,
        cross_references=["rcra_subtitle_c", "cercla_ncp", "tceq_remediation", "brownfield_redevelopment"],
        texas_notes="TCEQ administers RCRA corrective action in Texas under 30 TAC 335; coordinates with EPA Region 6 on dual-track sites; TCEQ's Voluntary Cleanup Program (VCP) may provide alternative cleanup pathway",
    ),
    DoctrineCacheBlock(
        topic="fifra_worker_protection",
        category="pesticides",
        summary="FIFRA's Worker Protection Standard (40 CFR Part 170) protects agricultural workers and pesticide handlers from occupational exposure to pesticides through training, notification, PPE, restricted entry intervals, and decontamination requirements.",
        analysis="FIFRA Worker Protection Standard (WPS), revised 2015 (effective 2018): (1) Scope — applies to agricultural establishments (farms, forests, nurseries, greenhouses) and commercial pesticide handling establishments. Does not apply to residential, structural, or public health pest control. (2) Workers — those performing hand-labor tasks in treated areas (planting, harvesting, pruning); must receive annual WPS training, access to Safety Data Sheets, notification of pesticide applications. (3) Handlers — those mixing, loading, applying, or otherwise directly handling pesticides; require specific training, PPE as specified on label, medical monitoring for cholinesterase-inhibiting pesticides. (4) Restricted Entry Intervals (REIs) — period after application when entry to treated area is restricted; set on pesticide label (4-72 hours typically; longer for certain products). Early entry permitted only with specific PPE and for limited activities. (5) Application exclusion zones (AEZ) — revised in 2015; 25-foot or 100-foot AEZ around application equipment during application; must suspend application if persons within AEZ. (6) Decontamination supplies — water, soap, towels must be available within 1/4 mile of work area; eyewash for handlers using products requiring eye protection. (7) Emergency assistance — employer must promptly provide emergency transportation and information to medical facility. (8) Designated representative — workers can designate a representative to access pesticide application records. (9) Recordkeeping — 2 years for applications in areas where workers/handlers present. (10) Penalties — FIFRA Section 14; up to $21,952 per violation (2024 adjusted) for commercial applicators; lower for private applicators.",
        authority="7 USC 136-136y (FIFRA); 40 CFR Part 170 (WPS); FIFRA Section 14 (penalties); EPA WPS How to Comply Manual",
        keywords=["fifra", "wps", "worker protection", "pesticide", "rei", "handler", "agricultural worker", "application exclusion zone"],
        statute="7 USC 136-136y",
        cfr_reference="40 CFR Part 170",
        confidence=0.91,
        cross_references=["fifra_registration", "esa_pesticide_consultation", "toxic_tort"],
        texas_notes="Texas Department of Agriculture (TDA) administers FIFRA in Texas; TDA licenses commercial/noncommercial applicators and regulates restricted-use pesticides; 4 TAC Chapter 7",
    ),
    DoctrineCacheBlock(
        topic="epcra_tier_ii",
        category="epcra_reporting",
        summary="EPCRA Section 312 Tier II reporting requires facilities storing hazardous chemicals at or above threshold quantities to annually report chemical inventories to state/local emergency planning authorities and fire departments, enabling emergency response preparedness.",
        analysis="EPCRA Tier II Reporting (42 USC 11022): (1) Who reports — facilities that must maintain Safety Data Sheets (SDS) under OSHA HazCom Standard and store hazardous chemicals at or above threshold quantities. General threshold: 10,000 lbs for most chemicals; 500 lbs or threshold planning quantity (whichever lower) for Extremely Hazardous Substances (EHS, EPCRA Section 302 list). (2) What is reported — chemical identity, physical/health hazards, maximum/average daily amounts, storage locations, days on site. Tier I is aggregate by category (no longer commonly used); Tier II is chemical-specific (standard practice). (3) Where filed — State Emergency Response Commission (SERC), Local Emergency Planning Committee (LEPC), and local fire department. Due annually by March 1 for previous calendar year. (4) Public access — Tier II reports are publicly available; trade secret claims may protect specific chemical identity but not hazard information. (5) EHS requirements — facilities with EHS above threshold must also file Section 302 notification (LEPC/SERC) and designate emergency coordinator. (6) Release reporting — EPCRA Section 304 requires immediate notification of releases of EHS or CERCLA hazardous substances above reportable quantities. (7) TRI reporting — Section 313 requires separate Toxic Release Inventory reporting for manufacturing/processing facilities with 10+ employees using listed toxic chemicals above thresholds. (8) Penalties — up to $64,618 per day per violation (2024 adjusted) for failure to comply; criminal penalties for knowing/willful violations. (9) Citizen suits — EPCRA Section 326 authorizes citizen suits for failure to file reports. (10) State implementation — Texas Commission on Environmental Quality administers EPCRA in coordination with Texas Division of Emergency Management.",
        authority="42 USC 11001-11050 (EPCRA); 40 CFR Parts 355, 370, 372; OSHA 29 CFR 1910.1200 (HazCom)",
        keywords=["epcra", "tier ii", "emergency planning", "hazardous chemical", "ehs", "lepc", "serc", "tri", "release reporting"],
        statute="42 USC 11001-11050",
        cfr_reference="40 CFR 355, 370, 372",
        confidence=0.92,
        cross_references=["cercla_reporting", "rcra_subtitle_c", "tceq_remediation"],
        practice_tips=[
            "March 1 deadline is firm — set calendar reminders for January to begin inventory compilation",
            "Track all EHS chemicals monthly — threshold is based on maximum amount present at any one time",
            "Oil and gas well sites storing chemicals may trigger Tier II reporting — don't overlook field locations",
        ],
        texas_notes="Texas files Tier II reports through Tier2 Submit online system; TCEQ provides SERC function; local LEPCs vary in activity level; 90-day extension possible with written request",
    ),
    DoctrineCacheBlock(
        topic="opa_spcc",
        category="oil_spill",
        summary="The Spill Prevention, Control, and Countermeasure (SPCC) rule under the Clean Water Act (40 CFR Part 112) requires facilities storing oil above threshold quantities to prepare and implement plans to prevent oil discharges to navigable waters and adjoining shorelines.",
        analysis="SPCC Rule (40 CFR Part 112, implementing CWA Section 311(j)): (1) Applicability — non-transportation-related onshore facilities and offshore facilities that store oil in aggregate aboveground storage capacity >1,320 gallons, or completely buried underground storage capacity >42,000 gallons, and could reasonably be expected to discharge oil to navigable waters or adjoining shorelines. (2) SPCC Plan requirements — prepared by a licensed Professional Engineer (PE); describes facility, oil storage, secondary containment, inspections, security, personnel training, and discharge notification procedures. (3) Qualified facility provision — facilities with aggregate capacity ≤10,000 gallons and no single discharge >1,000 gallons in past 3 years may self-certify plan without PE certification. (4) Secondary containment — required for all bulk containers (tanks, containers >55 gallons); must hold 110% of largest container or 100% of largest plus rainfall. Sized for precipitation in 25-year, 24-hour storm event. (5) Oil production facilities — Subpart C of Part 112 applies; specific provisions for flowlines, produced water containers, drilling/workover facilities. (6) Inspections — monthly visual inspections; integrity testing of containers per industry standards (API 653, STI SP001). (7) Facility Response Plan (FRP) — required for substantial harm facilities (storage >1M gallons, proximity to waters); must demonstrate response capability and equipment deployment within specified timeframes. (8) Amendments — plan must be amended within 6 months of any material change; reviewed every 5 years. (9) Penalties — CWA Section 311 penalties for discharges; SPCC violations enforceable under CWA Section 309. (10) Relationship to OPA 90 — SPCC addresses prevention; OPA 90 Facility Response Plans address response planning for larger facilities.",
        authority="33 USC 1321 (CWA Section 311); 40 CFR Part 112; OPA 90 (33 USC 2701); EPA SPCC Guidance",
        keywords=["spcc", "oil spill", "spill prevention", "secondary containment", "oil storage", "facility response plan", "frp"],
        statute="33 USC 1321 (CWA Section 311); 33 USC 2701 (OPA 90)",
        cfr_reference="40 CFR Part 112",
        confidence=0.93,
        cross_references=["opa_liability", "cwa_section_311", "rrc_environmental"],
        practice_tips=[
            "Oil production facilities in Permian Basin commonly trigger SPCC requirements — verify aggregate capacity",
            "PE certification required unless facility qualifies as 'qualified facility' under Subpart C",
            "Keep SPCC plan on-site and available for EPA inspection; training records must be maintained",
        ],
        texas_notes="RRC has MOU with EPA on SPCC inspections at oil/gas production facilities; TCEQ handles SPCC at non-E&P facilities; dual jurisdiction common at midstream facilities",
    ),
    DoctrineCacheBlock(
        topic="brownfield_liability_protection",
        category="site_assessment",
        summary="Federal brownfield liability protections under CERCLA Sections 107(r) and 128 provide bona fide prospective purchaser, contiguous property owner, and innocent landowner defenses to CERCLA liability, enabling redevelopment of contaminated properties.",
        analysis="Brownfield Liability Protections (Brownfields Amendments, 2002): (1) Bona Fide Prospective Purchaser (BFPP) defense (42 USC 9607(r)) — purchaser who acquires property after January 11, 2002, after all contamination occurred, with knowledge of contamination (AAI/Phase I ESA), and meets continuing obligations: no further releases, compliance with institutional controls, cooperation with authorized response actions, reasonable steps to stop ongoing releases. (2) Contiguous Property Owner defense (42 USC 9607(q)) — owner of property contaminated solely by migration from adjoining properties; must not cause or contribute, exercise appropriate care, cooperate with response actions. (3) Innocent Landowner defense (42 USC 9601(35)) — pre-Brownfields defense; must demonstrate all appropriate inquiries at time of acquisition and no reason to know of contamination. (4) All Appropriate Inquiries (AAI) (40 CFR 312) — standardized Phase I ESA process; ASTM E1527-21 complies with AAI rule. Must be conducted or updated within 180 days before acquisition; certain components (search distance, government records) valid for 1 year. (5) State brownfield programs — EPA Section 128(a) cooperative agreements with states; state voluntary cleanup programs (VCPs) provide alternative cleanup pathway with liability protection. Texas VCP under TCEQ (30 TAC 333) issues comfort letters and certificates of completion. (6) Federal brownsfields grants — EPA awards assessment, cleanup, revolving loan fund, and job training grants to communities and nonprofits. (7) Windfall lien — EPA may assert a lien equal to increase in property value from federal cleanup (42 USC 9607(r)(4)). (8) All continuing obligations must be maintained perpetually; loss of defense if obligations violated. (9) Federal conformity — state VCP cleanups that meet EPA standards can provide CERCLA liability protection. (10) Tax incentives — Section 198 brownfield expensing (expired, periodically reauthorized).",
        authority="42 USC 9601(35), 9607(q), 9607(r), 9628; 40 CFR 312 (AAI); ASTM E1527-21; 30 TAC 333 (Texas VCP)",
        keywords=["brownfield", "bfpp", "innocent landowner", "contiguous property", "voluntary cleanup", "vcp", "liability protection", "phase i", "aai"],
        statute="42 USC 9601(35), 9607(q), 9607(r), 9628",
        cfr_reference="40 CFR 312; 30 TAC 333",
        confidence=0.93,
        cross_references=["cercla_prp_liability", "phase_i_esa", "environmental_insurance", "brownfield_redevelopment"],
        practice_tips=[
            "Always update Phase I ESA within 180 days of closing — stale assessments lose AAI compliance",
            "BFPP defense has continuing obligations — failure to comply at any point forfeits the defense",
            "Texas VCP certificates of completion provide strongest state-level liability protection",
        ],
        texas_notes="TCEQ Voluntary Cleanup Program (30 TAC 333) issues certificate of completion upon successful cleanup; protects future owners/lenders; TCEQ innocent owner/operator program available under THSC Chapter 361",
    ),
    DoctrineCacheBlock(
        topic="caa_neshap",
        category="air_quality",
        summary="National Emission Standards for Hazardous Air Pollutants (NESHAPs) under CAA Section 112 regulate emissions of 188 hazardous air pollutants (HAPs) from major and area sources through technology-based standards (MACT/GACT) and residual risk standards.",
        analysis="CAA Section 112 NESHAPs: (1) Listed HAPs — 188 hazardous air pollutants listed in Section 112(b), including metals (arsenic, beryllium, cadmium, chromium, lead, manganese, mercury, nickel), organics (benzene, toluene, formaldehyde, vinyl chloride, 1,3-butadiene), and compound groups (glycol ethers, polycyclic organic matter). (2) Source categories — EPA identifies and lists source categories that emit HAPs; promulgates MACT standards for each category. Over 100 source categories regulated. (3) MACT standards — Maximum Achievable Control Technology for major sources (emit or have potential to emit ≥10 TPY of any HAP or ≥25 TPY of any combination); MACT floor based on top 12% of existing sources. (4) GACT standards — Generally Available Control Technology for area sources (below major source thresholds); less stringent than MACT. (5) Residual risk — Section 112(f) requires EPA to evaluate residual risk 8 years after MACT promulgation; promulgate additional standards if MACT does not provide ample margin of safety. (6) Key NESHAPs for oil/gas: Subpart HH (oil/gas production), Subpart OOOO/OOOOa/OOOOb (NSPS but related), Subpart HHH (natural gas transmission/storage), Subpart CC (petroleum refineries), Subpart DDDDD (industrial boilers). (7) Compliance — initial notification, performance testing, continuous monitoring, periodic reporting (semi-annual). (8) Title V integration — NESHAP requirements incorporated into Title V operating permits. (9) Case-by-case MACT — EPA 112(g) requires case-by-case MACT for new major sources in categories where standards not yet promulgated. (10) Penalties — CAA Section 113; up to $109,024/day per violation (2024 adjusted); criminal penalties for knowing violations. (11) State delegation — most states, including Texas, have delegation to implement NESHAPs.",
        authority="42 USC 7412 (CAA Section 112); 40 CFR Part 63 (NESHAPs); 30 TAC Chapter 113 (Texas implementation)",
        keywords=["neshap", "hap", "mact", "gact", "hazardous air pollutant", "section 112", "residual risk", "source category"],
        statute="42 USC 7412",
        cfr_reference="40 CFR Part 63; 30 TAC Chapter 113",
        confidence=0.93,
        cross_references=["caa_nsps", "caa_naaqs", "tceq_air_permits", "tsca_chemical_review"],
        texas_notes="TCEQ implements NESHAPs in Texas under delegation; TCEQ may impose additional state-only HAP requirements under 30 TAC 113; Title V permits incorporate all applicable NESHAPs",
    ),
    DoctrineCacheBlock(
        topic="environmental_insurance_programs",
        category="environmental_insurance",
        summary="Environmental insurance programs including Pollution Legal Liability (PLL), Contractors Pollution Liability (CPL), and Remediation Stop Loss policies transfer environmental risk and provide financial assurance for cleanup obligations, permit requirements, and third-party claims.",
        analysis="Environmental Insurance Products: (1) Pollution Legal Liability (PLL) — covers pre-existing and new pollution conditions at owned/operated sites; bodily injury, property damage, cleanup costs, defense costs from third-party claims. Key underwriting: Phase I/II ESA results, compliance history, operations type. (2) Contractors Pollution Liability (CPL) — covers pollution arising from contractor's operations (remediation contractors, construction, environmental consultants); professional liability for errors/omissions in environmental work. (3) Remediation Stop Loss (RSL) — cost cap policy for known contamination; insures cleanup costs above a predetermined self-insured retention; used when cleanup cost uncertainty is high. Requires baseline cost estimate. (4) Secured Creditor/Lender — protects lenders from environmental liability when borrower defaults and lender acquires property through foreclosure. (5) Financial Assurance — insurance policies can satisfy RCRA, CERCLA, state VCP, and UST financial assurance requirements. (6) Storage Tank Liability — specific policies for UST/AST owners meeting RCRA/state financial responsibility requirements (40 CFR 280 Subpart H). (7) Coverage triggers — discovery-based vs. claims-made; most environmental policies are claims-made requiring timely reporting. (8) Key exclusions — intentional discharge, known pre-existing conditions (unless specifically covered in PLL), fines/penalties, asbestos/lead in some policies. (9) Premium factors — property size, operations, contamination history, cleanup estimates, coverage limits. (10) Market trends — increasing demand for M&A transaction environmental insurance (Representations and Warranties plus PLL); growing role of parametric insurance for climate-related environmental risks. (11) Claims process — immediate notice required; insurer often has right to approve remedial contractors and approach.",
        authority="State insurance regulation; 40 CFR 264/265 Subpart H (RCRA FA); 40 CFR 280 Subpart H (UST FA); contract and policy terms",
        keywords=["environmental insurance", "pll", "cpl", "remediation stop loss", "financial assurance", "pollution liability", "cost cap"],
        statute="42 USC 6991b (UST FA); 42 USC 6924 (RCRA FA); state insurance codes",
        cfr_reference="40 CFR 264/265 Subpart H; 40 CFR 280 Subpart H",
        confidence=0.87,
        cross_references=["environmental_insurance", "rcra_subtitle_c", "cercla_prp_liability", "phase_i_esa"],
        texas_notes="Texas Department of Insurance regulates environmental insurance products; TCEQ Petroleum Storage Tank (PST) program provides state fund coverage for certain eligible UST releases (THSC Chapter 26 Subchapter I); PST fund sunset provisions important for coverage timing",
    ),
    DoctrineCacheBlock(
        topic="permian_methane_regulation",
        category="permian_basin",
        summary="Methane emissions regulation in the Permian Basin involves overlapping federal EPA NSPS OOOOb/OOOOc rules, RRC statewide rules on flaring and venting, TCEQ air permits, and emerging ESG/investor pressure for methane intensity reduction.",
        analysis="Permian Basin Methane Regulation: (1) EPA Methane Rules — NSPS OOOOb (new/modified sources) and Emission Guidelines OOOOc (existing sources) finalized December 2023 under CAA Section 111; require LDAR at well sites, compressor stations; zero-routine-flaring for new wells; super-emitter response program; phased compliance 2025-2028. (2) Methane Fee (IRA Section 60113) — Waste Emissions Charge (WEC) on methane from facilities reporting to GHGRP Subpart W; $900/ton in 2024, $1,200 in 2025, $1,500 in 2026+; exemptions for facilities below 25,000 tCO2e threshold and facilities meeting OOOOb standards. (3) RRC flaring rules — Statewide Rule 32 prohibits wasteful flaring; permits required for flaring/venting beyond initial production period; RRC has tightened flaring permits in Permian Basin (2021 amendments). (4) TCEQ air permits — permit by rule (PBR 106.352) for oil and gas facilities; flexible permits may cap basin-wide emissions. (5) Measurement — EPA GHGRP Subpart W requires annual reporting from facilities emitting ≥25,000 tCO2e; satellite detection (MethaneSAT, TROPOMI) increasingly used for basin-wide monitoring. (6) Super-emitter program — OOOOb/OOOOc establish framework for third-party detection notification; operators must investigate and repair within specified timeframes. (7) State preemption issues — Texas SB 1420 (2023) addressed potential federal-state conflicts; Texas industry argues state programs are sufficient. (8) Voluntary programs — ONE Future Coalition, OGMP 2.0, EPA Methane Challenge; many operators adopting voluntary methane intensity targets (e.g., 0.20%). (9) Financial implications — ESG investors track Scope 1 methane; SEC climate disclosure rule (stayed pending litigation) would require methane reporting. (10) Technology — LDAR via OGI cameras, continuous monitors, aerial surveys, satellite; pneumatic device replacement; zero-bleed controllers; vapor recovery units; green completions.",
        authority="40 CFR Part 60 Subpart OOOOb, OOOOc; 42 USC 7411 (CAA Section 111); IRA Section 60113; 16 TAC 3.32 (RRC Rule 32); 30 TAC 106.352",
        keywords=["methane", "permian basin", "flaring", "venting", "ooob", "oooc", "ldar", "ghgrp", "waste emissions charge", "super emitter"],
        statute="42 USC 7411 (CAA Section 111); IRA Section 60113 (Methane Fee)",
        cfr_reference="40 CFR 60 Subpart OOOOb, OOOOc; 40 CFR 98 Subpart W",
        confidence=0.91,
        cross_references=["caa_nsps", "permian_flaring", "carbon_credits", "tceq_air_permits"],
        practice_tips=[
            "Track OOOOb compliance dates — phased implementation 2025-2028 based on source type",
            "Waste Emissions Charge applies to 2024 emissions reported in 2025 — calculate exposure now",
            "Super-emitter response requires investigation within 15 days of notification — have SOPs ready",
        ],
        texas_notes="RRC and TCEQ have overlapping methane jurisdiction; RRC controls flaring permits and waste gas; TCEQ controls air emissions from equipment; both agencies coordinate on Permian Basin enforcement",
    ),
    DoctrineCacheBlock(
        topic="citizen_suit_standing",
        category="compliance_enforcement",
        summary="Citizen suit provisions in federal environmental statutes (CWA, CAA, RCRA, CERCLA, ESA, SDWA) allow private parties to sue violators or agencies, subject to Article III standing requirements (injury-in-fact, causation, redressability) and statutory prerequisites.",
        analysis="Environmental Citizen Suits: (1) Statutory authorization — virtually all major federal environmental statutes include citizen suit provisions: CWA Section 505, CAA Section 304, RCRA Section 7002, ESA Section 11(g), SDWA Section 1449, TSCA Section 20, EPCRA Section 326. (2) Two types — suits against violators (against any person alleged to be in violation) and suits against EPA (for failure to perform non-discretionary duty). (3) Standing — Article III requires (a) injury-in-fact: concrete, particularized, actual/imminent (not conjectural); (b) causation: injury fairly traceable to defendant's conduct; (c) redressability: favorable decision would likely remedy injury. Lujan v. Defenders of Wildlife (1992), Friends of the Earth v. Laidlaw (2000), Sierra Club v. Morton (1972). (4) Notice requirement — 60-day pre-suit notice to alleged violator, EPA, and state (90 days for RCRA); notice must specify standard violated, activity constituting violation, and violator identity. (5) Diligent prosecution bar — citizen suit barred if EPA or state has commenced and is diligently prosecuting an enforcement action. Gwaltney of Smithfield v. CBE (1987). (6) Wholly past violations — cannot maintain citizen suit for wholly past violations (Gwaltney); must allege ongoing violation or reasonable likelihood of future violation. (7) Remedies — injunctive relief (compliance orders) and civil penalties (payable to US Treasury); some statutes allow recovery of litigation costs and attorney fees. No damages to plaintiffs. (8) Fee-shifting — prevailing or substantially prevailing party may recover reasonable attorney fees and costs; significant incentive for environmental litigation. (9) Settlement — consent decrees require DOJ review; Supplemental Environmental Projects (SEPs) may be included. (10) SLAPP protection — some states have anti-SLAPP statutes protecting environmental citizen suit plaintiffs from retaliatory litigation. (11) Texas-specific — THSC Chapter 361.233 provides limited state citizen suit authority for solid waste violations.",
        authority="33 USC 1365 (CWA 505); 42 USC 7604 (CAA 304); 42 USC 6972 (RCRA 7002); 16 USC 1540(g) (ESA 11(g)); Lujan v. Defenders of Wildlife, 504 US 555 (1992); Friends of Earth v. Laidlaw, 528 US 167 (2000)",
        keywords=["citizen suit", "standing", "notice", "diligent prosecution", "injunction", "attorney fees", "enforcement", "private attorney general"],
        statute="33 USC 1365; 42 USC 7604; 42 USC 6972; 16 USC 1540(g)",
        cfr_reference="40 CFR 135 (CWA citizen suits)",
        confidence=0.93,
        cross_references=["environmental_standing", "epa_enforcement_priorities", "cwa_npdes", "caa_naaqs"],
        texas_notes="Texas has limited state citizen suit authority compared to federal statutes; THSC 361.233 for solid waste; most Texas environmental citizen suits filed under federal statutes in federal court",
    ),
    DoctrineCacheBlock(
        topic="climate_adaptation_regulation",
        category="carbon_climate",
        summary="Climate adaptation regulation encompasses federal and state requirements for resilience planning, flood risk management, infrastructure design standards, and disclosure of climate-related physical risks to facilities and operations.",
        analysis="Climate Adaptation Regulatory Framework: (1) Federal — Executive Order 14008 (Tackling the Climate Crisis at Home and Abroad) directs agencies to integrate climate adaptation into planning and programs. FEMA updates flood maps and Building Resilient Infrastructure and Communities (BRIC) grants. National Climate Assessment informs federal planning. (2) SEC climate disclosure rule (2024, stayed pending litigation) would require registrants to disclose material climate-related risks including physical risks (flooding, extreme heat, drought, wildfire). (3) NEPA — climate impacts must be considered in EIS for federal actions; CEQ 2023 guidance on assessing climate change effects and GHG emissions. (4) Infrastructure — IIJA (2021) and IRA (2022) include billions for resilient infrastructure, flood mitigation, drought response, and wildfire prevention. (5) State-level — California SB 261 (climate risk disclosure), New York Climate Act (CLCPA), Texas State Water Plan (drought adaptation). (6) Facility design — updated flood standards (ASCE 7, ASCE 24); FEMA flood insurance requirements for federally backed mortgages. (7) Insurance implications — increasing climate risk affecting availability and cost of property insurance in coastal and wildfire-prone areas. (8) Industrial facilities — climate risk assessment for chemical facilities (EPA RMP considerations), refineries, power plants; process safety implications of extreme weather events. (9) Permian Basin — drought conditions affecting water availability for hydraulic fracturing; extreme heat implications for worker safety and equipment performance; wildfire risk for surface facilities. (10) Litigation — climate-related lawsuits against energy companies (nuisance, negligence, consumer protection theories); municipal climate adaptation cost recovery claims.",
        authority="EO 14008; SEC Climate Disclosure Rule (2024); FEMA NFIP; CEQ NEPA Guidance (2023); IIJA Section 40101 et seq.; IRA Climate Provisions",
        keywords=["climate adaptation", "resilience", "flood risk", "physical risk", "climate disclosure", "sec", "infrastructure", "drought"],
        statute="42 USC 4321 (NEPA climate); 42 USC 4001 (NFIP); IRA Section 60103",
        cfr_reference="40 CFR 1502.16(a) (NEPA climate); 44 CFR 59-77 (NFIP); SEC Rule S7-10-22",
        confidence=0.84,
        cross_references=["carbon_credits", "nepa_eis", "environmental_justice"],
        texas_notes="Texas has no state climate disclosure law; Texas State Water Plan addresses drought; coastal Texas counties face increasing hurricane and flood risk; Permian Basin drought conditions affect produced water recycling economics",
    ),
    DoctrineCacheBlock(
        topic="toxic_tort_causation",
        category="toxic_tort",
        summary="Toxic tort causation requires proof of both general causation (substance can cause the disease) and specific causation (substance did cause this plaintiff's disease), applying Daubert standards to expert testimony on dose-response, exposure pathways, and differential diagnosis.",
        analysis="Toxic Tort Causation Framework: (1) General causation — plaintiff must prove the substance is capable of causing the alleged injury/disease in humans. Evidence includes epidemiological studies, animal studies, mechanistic data, regulatory determinations. Bradford Hill criteria (strength of association, consistency, specificity, temporality, biological gradient, plausibility, coherence, experimental evidence, analogy). (2) Specific causation — plaintiff must prove the substance more likely than not caused this particular plaintiff's condition. Requires differential diagnosis (rule-in/rule-out methodology), exposure reconstruction, dose-response analysis. (3) Daubert standard — federal courts and most states (including Texas) require scientific expert testimony to be reliable and relevant. Four factors: testable hypothesis, peer review, known error rate, general acceptance. Texas follows Robinson v. Commonwealth (Tex. 2002) applying similar reliability requirements. (4) Exposure proof — plaintiff must demonstrate sufficient dose/duration of exposure; requires industrial hygiene testimony, exposure modeling, biomonitoring data if available. (5) Latency — many environmental diseases have long latency periods (mesothelioma 20-50 years, some cancers 10-30 years); statute of limitations typically runs from discovery of injury. (6) Multiple exposures — apportioning causation among multiple chemical exposures and defendants; several vs. joint and several liability varies by jurisdiction. (7) Medical monitoring — some jurisdictions allow claims for future medical monitoring costs even absent current disease (no present injury required). (8) Epidemiological threshold — relative risk >2.0 is commonly cited as threshold for legal significance (more probable than not), but not universally required. (9) Novel contaminants — PFAS, microplastics, endocrine disruptors present evolving causation challenges as scientific understanding develops. (10) Class certification — causation individualization may defeat class certification under Rule 23(b)(3) predominance; mass tort MDL proceedings more common.",
        authority="Daubert v. Merrell Dow Pharmaceuticals, 509 US 579 (1993); General Electric Co. v. Joiner, 522 US 136 (1997); Robinson v. Commonwealth, 110 SW3d 18 (Tex. 2002); 42 USC 9607 (CERCLA liability); Restatement (Third) of Torts: Liability for Physical and Emotional Harm",
        keywords=["toxic tort", "causation", "daubert", "epidemiology", "exposure", "differential diagnosis", "general causation", "specific causation"],
        statute="Federal Rules of Evidence 702; Texas Rules of Evidence 702; 42 USC 9607",
        cfr_reference="N/A — common law and evidentiary standards",
        confidence=0.90,
        cross_references=["environmental_insurance", "tsca_pfas", "cercla_prp_liability", "citizen_suit_standing"],
        texas_notes="Texas follows Daubert/Robinson for expert testimony reliability; 2-year statute of limitations from discovery; proportionate responsibility under CPRC Chapter 33; medical monitoring claims limited in Texas",
    ),
    DoctrineCacheBlock(
        topic="environmental_justice_compliance",
        category="environmental_justice",
        summary="Environmental justice compliance encompasses EO 12898, EPA's EJ Strategy, Title VI considerations, EJScreen analysis, meaningful community engagement, and cumulative impact assessment requirements affecting permitting, enforcement, and remediation decisions.",
        analysis="Environmental Justice Compliance: (1) EO 12898 (1994) — each federal agency shall make achieving environmental justice part of its mission; identify/address disproportionately high adverse effects on minority and low-income populations. (2) EO 14096 (2023) — Revitalizing Our Nation's Commitment to Environmental Justice; broadened scope to include all federal activities; established White House Environmental Justice Council. (3) EPA EJ Strategy — integrate EJ into permitting (Title V, NPDES, RCRA), enforcement (targeting high-EJ-concern areas), rulemaking (EJ analysis in regulatory impact assessments), and cleanup (community involvement at Superfund/RCRA sites). (4) Title VI, Civil Rights Act — EPA recipients of federal funding must not discriminate; disparate impact analysis in permitting decisions; EPA External Civil Rights Compliance Office processes complaints. (5) EJScreen — EPA's environmental justice screening tool; identifies communities with disproportionate environmental burden + vulnerable demographics; used in permit review, enforcement targeting, grant allocation. (6) Cumulative impacts — emerging regulatory concept requiring assessment of total environmental and health burden on communities, not just incremental impact of proposed action. California SB 1000 model. (7) Community engagement — meaningful involvement (not just public comment period); language access, accessible meeting locations, early engagement, technical assistance. EPA's Plan EJ 2014 and subsequent guidance. (8) Permitting — EPA and state agencies increasingly considering EJ in permit decisions; some states require EJ assessment for major permits (New Jersey EJ Law 2020; New York climate justice provisions). (9) Enforcement — EPA's Office of Enforcement and Compliance Assurance (OECA) prioritizes enforcement in overburdened communities. (10) Texas — no state EJ law; TCEQ considers some EJ factors but no formal EJ analysis requirement in permitting; community engagement opportunities exist but limited compared to states with EJ statutes.",
        authority="EO 12898; EO 14096; Title VI, Civil Rights Act of 1964 (42 USC 2000d); EPA EJ Strategy; EPA EJScreen; CEQ Environmental Justice Guidance (1997)",
        keywords=["environmental justice", "ej", "ejscreen", "title vi", "cumulative impact", "disproportionate", "community engagement", "overburdened"],
        statute="42 USC 2000d (Title VI); EO 12898; EO 14096; 42 USC 4321 (NEPA EJ considerations)",
        cfr_reference="40 CFR 7 (EPA Title VI); CEQ NEPA EJ Guidance",
        confidence=0.88,
        cross_references=["nepa_eis", "caa_naaqs", "citizen_suit_standing", "environmental_standing"],
        texas_notes="Texas lacks state EJ legislation; TCEQ has no formal EJ analysis requirement; federal EJ requirements apply to federally-permitted facilities in Texas; EJScreen identifies numerous overburdened communities in Permian Basin, Gulf Coast, and East Texas",
    ),
    DoctrineCacheBlock(
        topic="ust_regulatory_framework",
        category="site_assessment",
        summary="Underground Storage Tank (UST) regulation under RCRA Subtitle I requires registration, leak detection, corrosion protection, financial responsibility, closure, and corrective action for UST systems storing petroleum or hazardous substances, with TCEQ administering the Texas UST program and Petroleum Storage Tank remediation fund.",
        analysis="UST Regulatory Framework (42 USC 6991, 40 CFR 280/281): (1) Applicability — USTs storing petroleum products or hazardous substances; excludes farm/residential tanks <1,100 gallons, heating oil for consumptive use, septic tanks, flow-through process tanks, and certain others. (2) Technical standards — spill prevention (catchment basin), overfill prevention (automatic shutoff/alarm/ball float), corrosion protection (cathodic protection or fiberglass), release detection (monthly monitoring — SIR, ATG, CSLD, groundwater monitoring, or vapor monitoring). (3) Financial responsibility — owners/operators must maintain financial responsibility for taking corrective action and compensating third parties (40 CFR 280 Subpart H): $1M per occurrence for petroleum, $500K for non-marketer of 100 or fewer tanks; $2M aggregate. (4) Release reporting — owners must report confirmed/suspected releases within 24 hours to state agency (TCEQ in Texas); investigation and corrective action required. (5) Closure — proper closure requires notification (30 days advance in Texas), tank emptying/cleaning, removal or closure in place, site assessment for contamination. (6) Texas PST program — TCEQ administers UST program under 30 TAC Chapter 334. Texas PST Remediation Fund (THSC Chapter 26 Subchapter I) reimburses eligible costs for corrective action at eligible PST sites. (7) Fund eligibility — owner/operator must be current on registration/delivery fees, report release timely, and cooperate with TCEQ. Maximum reimbursement amounts set by rule. (8) LUST Trust Fund — federal Leaking Underground Storage Tank Trust Fund provides money for EPA/state cleanup of UST releases where responsible party unknown or unable/unwilling to clean up. Funded by 0.1 cent/gallon motor fuel tax. (9) Operator training — EPA 2015 regulation requires designated Class A (knowledgeable), Class B (day-to-day), and Class C (on-site) operators. (10) UST compatibility — systems must be compatible with stored substance; particular concern with biofuel blends (E15+, B20+) and UST material compatibility. (11) Delivery prohibition — if UST system lacks required spill/overfill/release detection equipment, delivery is prohibited (red tag). (12) Historic releases — many UST releases from pre-regulation (pre-1988) tanks; legacy contamination may trigger CERCLA liability if petroleum exclusion does not apply (e.g., lead additives).",
        authority="42 USC 6991-6991m (RCRA Subtitle I); 40 CFR Parts 280, 281; 30 TAC Chapter 334 (Texas UST); THSC Chapter 26 Subchapter I (Texas PST Fund)",
        keywords=["ust", "underground storage tank", "petroleum", "leak detection", "pst", "lust", "corrective action", "financial responsibility", "closure"],
        statute="42 USC 6991-6991m",
        cfr_reference="40 CFR 280-281; 30 TAC 334",
        confidence=0.94,
        cross_references=["phase_i_esa", "brownfield_liability_protection", "rcra_corrective_action", "tceq_remediation"],
        practice_tips=[
            "Check UST registration status and compliance history before property acquisition — PST fund eligibility depends on prior owner compliance",
            "Historic UST sites (pre-1988) often have undocumented releases — Phase I ESA should flag any evidence of former USTs",
            "Texas PST fund reimbursement is not guaranteed — verify eligibility criteria carefully before relying on fund coverage",
            "Delivery prohibition (red tag) can shut down fuel operations immediately — maintain equipment compliance",
        ],
        penalties="Civil: up to $70,117/day per violation (2024 adjusted); Texas: up to $25,000/day (THSC 382.085); criminal penalties for knowingly releasing hazardous substances",
        texas_notes="TCEQ administers Texas UST program under 30 TAC 334; PST remediation fund covers eligible cleanup costs (owner must be in compliance with registration/fee requirements); approximately 26,000 active USTs in Texas; TCEQ LPST list tracks leaking PST sites statewide",
    ),
]


# ============================================================================
# DOCTRINE STATISTICS
# ============================================================================

# Pre-computed doctrine block inventory for fast reference
_DOCTRINE_TOPIC_COUNT = len(DOCTRINE_BLOCKS)
_DOCTRINE_CATEGORIES_PRESENT = sorted(set(b.category for b in DOCTRINE_BLOCKS))
_DOCTRINE_STATUTES_REFERENCED = sorted(set(
    b.statute for b in DOCTRINE_BLOCKS if b.statute
))
_DOCTRINE_KEYWORDS_TOTAL = sum(len(b.keywords) for b in DOCTRINE_BLOCKS)
_DOCTRINE_CROSS_REFERENCES_TOTAL = sum(len(b.cross_references) for b in DOCTRINE_BLOCKS)

logger.info(
    f"Doctrine inventory: {_DOCTRINE_TOPIC_COUNT} blocks, "
    f"{len(_DOCTRINE_CATEGORIES_PRESENT)} categories, "
    f"{_DOCTRINE_KEYWORDS_TOTAL} keywords, "
    f"{_DOCTRINE_CROSS_REFERENCES_TOTAL} cross-references"
)


# ============================================================================
# MODULE-LEVEL CACHE
# ============================================================================

_cache: Optional[DoctrineCacheIndex] = None


def build_doctrine_cache() -> DoctrineCacheIndex:
    """Build the doctrine cache from all blocks."""
    global _cache
    cache = DoctrineCacheIndex()
    for block in DOCTRINE_BLOCKS:
        cache.add(block)
    _cache = cache
    logger.info(f"Doctrine cache built: {cache.total_blocks} blocks, {len(cache.categories)} categories")
    return cache


def get_doctrine_cache() -> DoctrineCacheIndex:
    """Get or build the doctrine cache."""
    global _cache
    if _cache is None:
        return build_doctrine_cache()
    return _cache


def get_doctrine_block(topic: str) -> Optional[DoctrineCacheBlock]:
    """Get a specific doctrine block by topic."""
    return get_doctrine_cache().get(topic)


def search_doctrines(query: str, max_results: int = 10) -> List[DoctrineCacheBlock]:
    """Search doctrine blocks by keyword."""
    return get_doctrine_cache().search(query, max_results)


def get_all_doctrine_categories() -> List[str]:
    """Get all doctrine categories."""
    return get_doctrine_cache().categories


def get_all_doctrine_topics() -> List[str]:
    """Get all doctrine topics."""
    return get_doctrine_cache().topics


def get_doctrine_cache_stats() -> Dict[str, Any]:
    """Get cache statistics."""
    return get_doctrine_cache().get_stats()


def get_doctrine_cache_hash() -> str:
    """Get an integrity hash of the entire cache."""
    content = "|".join(b.block_hash for b in DOCTRINE_BLOCKS)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def get_coverage_map() -> Dict[str, List[str]]:
    """Get the coverage map (category -> topics)."""
    cache = get_doctrine_cache()
    result: Dict[str, List[str]] = {}
    for cat in cache.categories:
        result[cat] = [b.topic for b in cache.get_by_category(cat)]
    return result


def verify_doctrine_integrity() -> Tuple[bool, List[str]]:
    """Verify all doctrine blocks have valid hashes."""
    errors: List[str] = []
    for block in DOCTRINE_BLOCKS:
        expected_content = f"{block.topic}|{block.summary}|{block.analysis}|{block.authority}"
        expected_hash = hashlib.sha256(expected_content.encode("utf-8")).hexdigest()
        if block.block_hash != expected_hash:
            errors.append(f"Hash mismatch for {block.topic}: stored={block.block_hash[:16]}... expected={expected_hash[:16]}...")
    return len(errors) == 0, errors


def get_stale_doctrines(max_age_days: int = 365) -> List[str]:
    """Get topics that haven't been updated recently."""
    from datetime import timedelta
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    stale: List[str] = []
    for block in DOCTRINE_BLOCKS:
        try:
            updated = datetime.fromisoformat(block.last_updated)
            if updated < cutoff:
                stale.append(block.topic)
        except ValueError:
            stale.append(block.topic)
    return stale
