"""
OFE03 - Frac Pump Diagnostics Engine
TIE Gold Standard Implementation

Domain: Oilfield Equipment - Fracturing Pump Systems
Authority: Quintuplex frac pumps, power end/fluid end diagnostics, treating iron,
          high-pressure operations (15K PSI), pump fleet management

Port: 9003
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ═══════════════════════════════════════════════════════════════════════════
# ENUMERATIONS
# ═══════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    FLUID_END = "fluid_end"
    POWER_END = "power_end"
    TREATING_IRON = "treating_iron"
    PUMP_PERFORMANCE = "pump_performance"
    PRESSURE_SYSTEMS = "pressure_systems"
    CHEMICAL_COMPATIBILITY = "chemical_compatibility"
    SAFETY_SYSTEMS = "safety_systems"
    COLD_WEATHER = "cold_weather"
    MONITORING = "monitoring"
    FLEET_MANAGEMENT = "fleet_management"


class AnalysisZone(str, Enum):
    DIAGNOSTIC = "DIAGNOSTIC"
    MAINTENANCE = "MAINTENANCE"
    SAFETY = "SAFETY"


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE BLOCKS - REAL FRAC PUMP EXPERTISE
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    category: IssueCategory
    zone: AnalysisZone


DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Quintuplex Pump Plunger Wear Analysis",
        keywords=["plunger", "wear", "quintuplex", "fluid end", "packing", "scoring"],
        conclusion_template=[
            "Plunger wear is detected through pressure fluctuations, packing leak rates, and visual inspection showing scoring or erosion.",
            "Premature plunger failure typically results from abrasive proppant in recirculated fluid, misaligned packing, or inadequate lubrication.",
            "Replace plungers when scoring depth exceeds 0.015 inches or diameter reduction exceeds 0.005 inches per API RP 11ER guidelines."
        ],
        reasoning_framework="""
        Quintuplex frac pumps operate at 2500-5000 HP with five plungers cycling 60-120 SPM. Each plunger
        experiences extreme cyclic loading through packing sets rated for 15,000 PSI. Wear analysis follows:

        1. NORMAL WEAR PATTERN: Uniform polishing across plunger length, symmetrical wear rings at packing
           contact zones, predictable wear rate of 0.001-0.003 inches per 500 pump hours.

        2. ABNORMAL WEAR INDICATORS: Longitudinal scoring (indicates proppant contamination), asymmetric
           wear (misalignment), rapid diameter loss (chemical attack or cavitation erosion), surface
           pitting (corrosion from produced water or acid).

        3. MEASUREMENT PROTOCOL: Micrometer readings at three zones (suction end, midpoint, discharge end),
           comparison to baseline OEM specifications (typically 4.500" diameter for 2500 HP units, 5.000"
           for 5000 HP units), tracking wear rate trends across pump fleet.

        4. FAILURE MODES: Catastrophic plunger failure releases high-pressure fluid into power end,
           destroying packing sets, damaging crankshaft seals, potentially causing injuries. Prevention
           requires adherence to inspection intervals.

        5. ROOT CAUSE DETERMINATION: Proppant contamination (check frac tank cleanout procedures),
           packing misalignment (inspect stuffing box bore), inadequate lubrication (verify packing
           lube injection system operation), chemical incompatibility (crosslinked gel attack on
           chrome plating).
        """,
        key_factors=[
            "Plunger diameter measurements vs. OEM baseline specifications",
            "Scoring depth and pattern (longitudinal indicates proppant, circumferential indicates packing)",
            "Packing leak rate trends (normal <0.5 BPM per plunger, excessive >2 BPM indicates wear)",
            "Pump discharge pressure fluctuations (±200 PSI swings indicate plunger seal loss)",
            "Proppant concentration in recirculated fluid (should be <0.1 lb/gal)",
            "Packing lube injection rate (typical 1-2 quarts per hour per plunger)"
        ],
        primary_authority=[
            "API RP 11ER: Recommended Practice for Guarding Reciprocating Pumps",
            "SPE 174839: Frac Pump Reliability Analysis and Failure Mode Prevention",
            "OEM service bulletins (SPM TWS-600, QWS-2500, Halliburton Q-10)",
            "OSHA 1910.269: High-pressure pump safety requirements"
        ],
        burden_holder="Frac vendor service supervisor",
        adversary_position="Plungers wear at rates exceeding industry norms due to operator-controlled factors (dirty tanks, improper chemical blends, poor maintenance)",
        counter_arguments=[
            "Wear rates within OEM specifications for actual operating hours and fluid conditions",
            "Proppant contamination traced to E&P operator tank cleaning procedures",
            "Packing lube system malfunction caused by operator-supplied glycol contamination",
            "Chemical incompatibility from operator-specified gel system not disclosed pre-job",
            "Normal wear-and-tear under extreme service conditions (24-hour pumping, arctic temperatures)"
        ],
        resolution_strategy="Establish baseline wear rates for specific fluid systems, implement mid-job plunger inspections for stages exceeding 50 per pump, maintain photographic evidence of plunger condition at install and removal, correlate wear to proppant type and concentration.",
        entity_scope="Frac service companies operating quintuplex pump fleets",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High certainty on measurement protocols and OEM specifications, moderate certainty on root cause attribution without detailed fluid analysis",
        controlling_precedent="API RP 11ER plunger inspection intervals and replacement criteria",
        category=IssueCategory.FLUID_END,
        zone=AnalysisZone.DIAGNOSTIC
    ),

    DoctrineBlock(
        topic="Fluid End Crack Detection and NDT",
        keywords=["fluid end", "crack", "NDT", "magnetic particle", "ultrasonic", "failure"],
        conclusion_template=[
            "Fluid end cracks initiate at stress concentration points: discharge valve bores, crossbore intersections, and external mounting bolt holes.",
            "Magnetic particle inspection (MPI) is the primary detection method for surface and near-surface cracks; ultrasonic testing (UT) for internal defects.",
            "Any crack propagation exceeding 0.125 inches requires immediate fluid end retirement per API and OEM safety bulletins."
        ],
        reasoning_framework="""
        Fluid ends on quintuplex frac pumps are forged or cast steel pressure vessels rated for 15,000-20,000
        PSI working pressure. Cyclic fatigue loading causes crack initiation and propagation:

        1. CRITICAL STRESS ZONES: Discharge valve bore (highest cyclic pressure), suction valve bore (rapid
           pressure reversal), crossbore intersection (stress concentration from perpendicular holes),
           external mounting surfaces (bolt preload plus operational stress).

        2. CRACK INITIATION MECHANISMS: High-cycle fatigue (typical 50-100 million cycles before crack
           initiation at design life), corrosion-assisted cracking (acid or produced water exposure),
           hydrogen embrittlement (from cathodic protection or corrosion), thermal shock (cold weather
           operations with inadequate preheat).

        3. INSPECTION PROTOCOL: Magnetic particle inspection every 2000 pump hours or annually, ultrasonic
           testing for internal defects on high-hour units (>8000 hours), dye penetrant for inaccessible
           areas, visual inspection under 10x magnification at every plunger change.

        4. CRACK CLASSIFICATION: Surface hairline cracks <0.050" (monitor, increase inspection frequency),
           propagating cracks 0.050-0.125" (repair if accessible, otherwise retire), through-wall cracks
           or cracks >0.125" (immediate retirement, catastrophic failure risk).

        5. FAILURE CONSEQUENCES: Fluid end rupture releases high-pressure fracturing fluid, creating
           high-velocity shrapnel hazards, potential for multiple injuries or fatalities. Industry has
           documented 12+ fatalities from fluid end failures 2010-2020.
        """,
        key_factors=[
            "Cumulative pump hours and cycle count (track via engine hour meter)",
            "MPI inspection results showing linear indications vs. OEM acceptance criteria",
            "Ultrasonic thickness measurements at crossbore intersections (baseline vs. current)",
            "Fluid chemistry exposure history (acid concentration, produced water chlorides)",
            "Prior repair history (welded areas are stress risers for crack re-initiation)",
            "Operating pressure profile (percentage of time at >12,000 PSI)"
        ],
        primary_authority=[
            "API RP 11ER: Pressure vessel inspection requirements for reciprocating pumps",
            "ASME Section VIII: Pressure vessel design and inspection standards",
            "SPE 184836: Frac Pump Fluid End Fatigue Life Analysis",
            "OEM service bulletins on NDT protocols and retirement criteria"
        ],
        burden_holder="Frac service company safety manager",
        adversary_position="Fluid end cracks result from manufacturing defects or material flaws, not operational abuse",
        counter_arguments=[
            "Cracks at low cycle counts (<2000 hours) suggest material or manufacturing defect",
            "Multiple units from same foundry batch exhibiting cracks indicates systemic quality issue",
            "Operating pressures maintained below rated capacity throughout service life",
            "NDT performed by certified Level II technicians per ASNT SNT-TC-1A requirements",
            "Immediate retirement upon crack detection demonstrates proactive safety culture"
        ],
        resolution_strategy="Maintain comprehensive NDT records with photographic documentation, correlate crack locations to operational stress analysis, implement finite element modeling for crack propagation prediction, establish retirement criteria based on crack growth rate trending.",
        entity_scope="All frac service companies operating high-pressure quintuplex pumps",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Extremely high certainty on NDT protocols and retirement criteria, high certainty on failure mode analysis",
        controlling_precedent="API RP 11ER mandatory retirement criteria for propagating cracks",
        category=IssueCategory.FLUID_END,
        zone=AnalysisZone.SAFETY
    ),

    DoctrineBlock(
        topic="Power End Bearing Failure Analysis",
        keywords=["power end", "bearing", "crankshaft", "connecting rod", "failure", "lubrication"],
        conclusion_template=[
            "Power end bearing failures manifest as increased vibration, elevated lube oil temperature, and metallic debris in oil analysis.",
            "Root causes include inadequate lubrication (oil starvation), contamination (water or proppant intrusion), or misalignment from improper assembly.",
            "Catastrophic bearing failure destroys crankshaft journals, connecting rods, and crossheads, requiring complete power end rebuild costing $150K-$300K."
        ],
        reasoning_framework="""
        Quintuplex pump power ends transmit 2500-5000 HP through crankshaft and connecting rod assemblies
        operating at 60-120 SPM. Bearing systems experience extreme cyclic loading:

        1. BEARING TYPES AND LOADING: Main crankshaft bearings (radial load from belt drive plus cyclic
           load from connecting rods), connecting rod bearings (cyclic tensile/compressive loading at
           discharge pressure), crosshead bearings (lateral loading from misalignment plus linear thrust).

        2. LUBRICATION SYSTEM REQUIREMENTS: Forced-feed pressure lubrication at 30-60 PSI, oil flow rate
           8-12 GPM, filtration to 10 microns absolute, oil temperature maintained 120-160°F, ISO VG 220
           gear oil or equivalent meeting API CF specifications.

        3. FAILURE PROGRESSION: Initial stage shows elevated bearing temperatures (10-20°F above normal),
           intermediate stage exhibits vibration increase and metallic particles in oil (copper from
           bearing babbit, iron from journal wear), final stage involves catastrophic seizure with
           connecting rod separation or crankshaft fracture.

        4. OIL ANALYSIS MONITORING: Spectrometric analysis for wear metals (Fe >100 PPM, Cu >50 PPM,
           Al >20 PPM indicate abnormal wear), particle count trending (ISO 4406 code degradation),
           water content (<0.5% acceptable, >2% critical), TAN/TBN tracking for oil degradation.

        5. VIBRATION ANALYSIS: Baseline vibration signature at commissioning, trending analysis for
           1x, 2x, and 3x running speed harmonics, bearing defect frequencies (BPFI, BPFO, BSF, FTF),
           alarm thresholds at 0.3 inches/second RMS, shutdown at 0.5 inches/second RMS.
        """,
        key_factors=[
            "Lube oil pressure and temperature trends (monitor via SCADA or local gauges)",
            "Oil analysis results showing wear metal concentrations and particle counts",
            "Vibration spectrum showing bearing defect frequencies or elevated harmonics",
            "Visual inspection of removed bearings (scoring, spalling, discoloration patterns)",
            "Crankshaft journal micrometer measurements vs. OEM tolerances (typically +/-0.002 in)",
            "Oil filtration system performance (bypass events, filter differential pressure)"
        ],
        primary_authority=[
            "API RP 11ER: Lubrication system requirements for reciprocating pumps",
            "ISO 4406: Oil cleanliness classification standards",
            "SPE 190038: Predictive Maintenance for Frac Pump Power Ends",
            "Bearing manufacturer specifications (Timken, SKF, Rollway)"
        ],
        burden_holder="Frac service company maintenance manager",
        adversary_position="Bearing failures result from manufacturing defects or inadequate OEM design margins",
        counter_arguments=[
            "Oil analysis performed at recommended intervals showing acceptable wear metal trends",
            "Lubrication system maintained per OEM specifications with documented oil changes",
            "Vibration monitoring implemented with documented trending and alarm response",
            "Bearing failures occurring at low operating hours suggest defective bearing batches",
            "Crankshaft journal dimensions within OEM tolerances at time of bearing installation"
        ],
        resolution_strategy="Implement comprehensive oil analysis program with 250-hour sampling intervals, install vibration sensors with continuous SCADA monitoring, maintain detailed bearing replacement records with photographic documentation, perform metallurgical analysis on failed bearings to determine root cause.",
        entity_scope="All frac pump power end maintenance programs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High certainty on failure mode analysis and preventive maintenance protocols, moderate certainty on root cause attribution without metallurgical analysis",
        controlling_precedent="API RP 11ER lubrication and bearing inspection requirements",
        category=IssueCategory.POWER_END,
        zone=AnalysisZone.DIAGNOSTIC
    ),

    DoctrineBlock(
        topic="Discharge Valve Inspection and Failure Modes",
        keywords=["discharge valve", "wing valve", "poppet", "seat", "spring", "failure"],
        conclusion_template=[
            "Discharge valve failures cause immediate pressure loss, fluid recirculation, and reduced pump efficiency typically noticed as pump rate decline at constant SPM.",
            "Common failure modes include poppet/seat erosion from proppant, spring fatigue from over-stroking, and valve body cracking from pressure spikes.",
            "Replace discharge valves when seat erosion exceeds 0.030 inches, poppet sealing surface shows >25% wear, or spring free length is reduced >10% from new."
        ],
        reasoning_framework="""
        Discharge valves (wing valves) in quintuplex pumps control fluid exit from the fluid end chambers.
        Operating at discharge pressures up to 15,000 PSI with cyclic loading 60-120 times per minute:

        1. VALVE DESIGN PARAMETERS: Poppet-style or wing-style seats, spring-loaded closure (typical
           spring force 800-1200 lbs), carbide or ceramic seats for abrasion resistance, flow area
           sized for velocity <30 ft/sec to minimize erosion.

        2. FAILURE MODE ANALYSIS: Erosive wear from proppant-laden fluid (40/70 mesh sand at 2-3 lb/gal
           causes rapid seat degradation), spring fatigue from million-cycle loading, poppet guide wear
           allowing misalignment and leakage, valve body cracking from pressure transients during pump
           start/stop.

        3. INSPECTION PROTOCOL: Remove and inspect valves every 500 pump hours or after 100 stages,
           measure seat inside diameter with pin gauges (typical new dimension 2.250", reject at 2.280"),
           measure poppet sealing surface width (new 0.250", reject at 0.187"), measure spring free
           length and load/deflection curve against OEM specifications.

        4. PERFORMANCE INDICATORS: Pump volumetric efficiency decline (normal >95%, investigate at <90%),
           discharge pressure fluctuations exceeding ±5% of average, temperature rise at discharge
           manifold (indicates recirculation and fluid shear heating), power consumption increase at
           constant pump rate and pressure.

        5. PROPPANT IMPACT MITIGATION: Carbide seats increase life 3-5x over steel seats, ceramic seats
           provide maximum erosion resistance but are brittle and crack-prone, flush valves with clean
           fluid between stages to remove settled proppant, avoid pump operation at <50% rated speed
           which causes valve flutter and accelerated wear.
        """,
        key_factors=[
            "Valve seat erosion measurements using pin gauges or bore gauge",
            "Poppet sealing surface wear pattern and remaining material thickness",
            "Spring free length and load testing vs. OEM specifications",
            "Pump volumetric efficiency calculated from discharge flow vs. theoretical displacement",
            "Proppant concentration and type in fracturing fluid (ceramic vs. sand, mesh size)",
            "Operational profile (percentage of time at high pressure, number of start/stop cycles)"
        ],
        primary_authority=[
            "API RP 11ER: Valve inspection and replacement criteria for reciprocating pumps",
            "SPE 174841: Frac Pump Valve Optimization and Failure Analysis",
            "OEM service manuals (SPM, Gardner Denver, Cornell)",
            "Industry best practices from Schlumberger, Halliburton, Baker Hughes"
        ],
        burden_holder="Frac service company operations supervisor",
        adversary_position="Valve failures are normal wear items expected in high-pressure pumping service",
        counter_arguments=[
            "Valve life meets or exceeds OEM published service intervals for given fluid conditions",
            "Premature valve failures correlate to customer-specified proppant type or concentration",
            "Inspection records demonstrate proactive replacement before failure occurs",
            "Use of premium carbide or ceramic seats shows investment in reliability",
            "Pump efficiency maintained above 90% throughout service period demonstrates proper valve function"
        ],
        resolution_strategy="Track valve life by proppant type and concentration, implement condition-based replacement using efficiency trending, maintain valve inventory stratified by anticipated service severity, perform metallurgical analysis on early failures to identify root cause.",
        entity_scope="All frac pumping operations using proppant-laden fluids",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High certainty on wear mechanisms and inspection criteria, moderate certainty on optimal replacement intervals for specific proppant types",
        controlling_precedent="API RP 11ER valve inspection requirements and OEM replacement criteria",
        category=IssueCategory.FLUID_END,
        zone=AnalysisZone.MAINTENANCE
    ),

    DoctrineBlock(
        topic="Treating Iron Integrity - Hammer Unions and Swivels",
        keywords=["treating iron", "hammer union", "swivel", "FMC", "leak", "failure"],
        conclusion_template=[
            "Treating iron failures at hammer unions result from improper makeup torque, worn or damaged seals, or thread galling from inadequate lubrication.",
            "Swivel joint failures typically involve bearing wear, seal degradation, or body cracking from pressure transients or overtorquing.",
            "Pressure test all treating iron connections to 1.5x maximum anticipated treating pressure before every job per API RP 53 requirements."
        ],
        reasoning_framework="""
        Treating iron systems connect frac pumps to wellhead, operating at 10,000-15,000 PSI with rapid
        pressure fluctuations. Hammer unions (Fig 1502, Fig 1002) and swivel joints are critical pressure
        containment components:

        1. HAMMER UNION DESIGN: Two flanged connections with sealing ring (typically Buna-N or Viton),
           retained by threaded nut with wing lugs, makeup torque 250-500 ft-lbs depending on size
           (2" or 3"), seal compression provides pressure containment up to rated working pressure.

        2. COMMON FAILURE MODES: Seal extrusion from over-pressure or worn seal grooves, leak at seal
           interface from under-torquing or seal damage, thread galling from dry makeup (must use
           thread compound), wing lug fracture from over-torquing or impact damage, flange face
           erosion from proppant-laden fluid leakage.

        3. SWIVEL JOINT OPERATION: Rotating bearing assembly allows manifold repositioning without
           disconnecting lines, pressure seals (typically quad-ring or metal-to-metal) contain
           high-pressure fluid, bearing lubrication critical (grease injection at 500 PSI minimum),
           rated for limited rotation cycles (typically 360° rotation limited to 50 cycles per year).

        4. INSPECTION PROTOCOL: Visual inspection of all unions before makeup (seal condition, flange
           face damage, thread condition), torque verification using calibrated wrench or torque
           multiplier, pressure testing to 1.5x maximum anticipated pressure for 5 minutes minimum,
           leak check during pump operation at 25%, 50%, 75%, and 100% rate.

        5. PRESSURE TESTING REQUIREMENTS: Hydrostatic test using water or light oil, never air (stored
           energy hazard), test pressure maintained for duration per API RP 53, any visible leakage
           requires disassembly and seal replacement, retesting after makeup, pressure relief protection
           during test (pop-off valve set at 1.1x test pressure).
        """,
        key_factors=[
            "Hammer union torque values documented for each connection (verify with torque wrench)",
            "Seal condition inspection results (cuts, extrusion, compression set)",
            "Flange face condition (erosion, gouges, perpendicularity)",
            "Thread condition and lubrication (anti-seize compound applied)",
            "Swivel joint bearing play measurement (axial and radial)",
            "Pressure test results (test pressure, duration, leakage observations)"
        ],
        primary_authority=[
            "API RP 53: Recommended Practices for Blowout Prevention Equipment Systems",
            "FMC Technologies: Hammer union installation and maintenance guidelines",
            "SPE 184523: High-Pressure Treating Iron Integrity Management",
            "OSHA 1910.269: High-pressure piping system safety requirements"
        ],
        burden_holder="Frac service company iron hand (treating iron supervisor)",
        adversary_position="Treating iron leaks or failures result from improper installation or maintenance",
        counter_arguments=[
            "Documented torque values for all connections using calibrated tools",
            "Pressure test records showing successful testing before pump operation",
            "Inspection records documenting seal and flange condition at makeup",
            "Use of OEM-supplied seals and proper thread lubricants",
            "Training records for iron hands on proper makeup procedures"
        ],
        resolution_strategy="Implement treating iron inspection checklist with photographic documentation, use torque measurement devices with data logging, perform pressure testing with chart recorder or SCADA documentation, maintain seal and component inventory with batch traceability.",
        entity_scope="All frac operations using high-pressure treating iron systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Extremely high certainty on installation and testing protocols, high certainty on failure mode analysis",
        controlling_precedent="API RP 53 pressure testing and makeup requirements",
        category=IssueCategory.TREATING_IRON,
        zone=AnalysisZone.SAFETY
    ),

    DoctrineBlock(
        topic="Pump Rate Optimization and Efficiency",
        keywords=["pump rate", "efficiency", "volumetric", "horsepower", "optimization", "BHP"],
        conclusion_template=[
            "Optimal pump rate balances volumetric efficiency (>95%), mechanical reliability (bearing/valve life), and hydraulic efficiency (minimum pressure loss).",
            "Pump efficiency degrades rapidly below 50% rated speed due to valve flutter and above 95% rated speed due to fluid acceleration losses.",
            "Target operating range: 70-90% of maximum rated speed for best balance of efficiency and component life."
        ],
        reasoning_framework="""
        Quintuplex frac pump efficiency depends on speed (SPM), pressure, fluid properties, and mechanical
        condition. Optimization requires balancing multiple competing factors:

        1. VOLUMETRIC EFFICIENCY ANALYSIS: Theoretical displacement (cylinder bore area × stroke × SPM ×
           number of plungers), actual flow rate (measured via flow meter or manifold totalizer),
           efficiency = (actual / theoretical) × 100%, normal efficiency >95%, investigate if <90%,
           causes include valve leakage, plunger seal wear, or fluid end cracks.

        2. SPEED-DEPENDENT EFFECTS: Low speed operation (<50 SPM on 120 SPM rated pumps) causes valve
           flutter (valves don't seat properly due to low differential pressure), high speed operation
           (>110 SPM) causes fluid acceleration losses (pressure drop due to flow velocity), valve
           bounce (valve impacts seat with excessive force), increased vibration and bearing loads.

        3. HORSEPOWER CALCULATIONS: Hydraulic horsepower (HHP) = (flow rate in BPM × pressure in PSI) ÷
           1714, brake horsepower (BHP) = HHP ÷ mechanical efficiency (typically 85-92%), mechanical
           efficiency degrades with bearing wear, misalignment, or lubrication issues, power consumption
           trending identifies developing mechanical problems.

        4. PRESSURE-DEPENDENT OPTIMIZATION: Higher discharge pressure increases volumetric efficiency
           (better valve sealing) but reduces mechanical efficiency (higher bearing loads), optimal
           operating pressure typically 60-80% of maximum rated pressure, pressure pulsation dampeners
           reduce cyclic stress on treating iron and improve pump efficiency.

        5. FLUID PROPERTY IMPACTS: High-viscosity fluids (crosslinked gels at 1000+ cP) reduce volumetric
           efficiency due to valve restriction, slickwater (3-5 cP) provides best volumetric efficiency,
           proppant concentration >10 lb/gal causes severe erosion and efficiency loss, temperature
           affects viscosity and seal performance (cold weather reduces efficiency).
        """,
        key_factors=[
            "Volumetric efficiency trending over pump operating hours",
            "Pump speed (SPM) vs. manufacturer's recommended operating range",
            "Discharge pressure and pressure pulsation amplitude",
            "Hydraulic horsepower and brake horsepower calculations from field data",
            "Fluid viscosity and proppant concentration profiles during job",
            "Power consumption trending (kW or HP from engine monitoring)"
        ],
        primary_authority=[
            "SPE 184523: Frac Pump Performance Optimization and Diagnostics",
            "API RP 11ER: Reciprocating pump efficiency and performance monitoring",
            "OEM performance curves (SPM TWS-600, QWS-2500 published data)",
            "Industry benchmarking studies from service company engineering groups"
        ],
        burden_holder="Frac service company pumping engineer",
        adversary_position="Pump performance meets contractual obligations for delivered rate and pressure",
        counter_arguments=[
            "Delivered pump rate within ±3% of contracted rate throughout job",
            "Discharge pressure maintained at or above minimum required for fracture propagation",
            "Volumetric efficiency within OEM specifications for fluid conditions",
            "Power consumption and efficiency consistent with published performance curves",
            "Operational adjustments made in response to changing reservoir conditions or wellbore restrictions"
        ],
        resolution_strategy="Establish baseline efficiency for each pump unit at commissioning, trend efficiency vs. cumulative operating hours, implement predictive maintenance when efficiency drops below 92%, optimize speed and pressure for specific fluid systems through field testing.",
        entity_scope="All frac pumping operations seeking performance optimization",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High certainty on efficiency calculation methods and optimization principles, moderate certainty on optimal operating parameters for novel fluid systems",
        controlling_precedent="API RP 11ER performance monitoring guidelines and OEM performance specifications",
        category=IssueCategory.PUMP_PERFORMANCE,
        zone=AnalysisZone.DIAGNOSTIC
    ),

    DoctrineBlock(
        topic="Suction Valve Inspection and Cavitation Damage",
        keywords=["suction valve", "cavitation", "NPSH", "vapor lock", "erosion"],
        conclusion_template=[
            "Suction valve failures typically result from cavitation damage when NPSH (Net Positive Suction Head) falls below minimum required values.",
            "Cavitation manifests as pitting erosion on valve seats and poppets, unusual noise (gravel sound), and pump performance degradation.",
            "Maintain minimum 15 PSI suction pressure at pump inlet and ensure NPSH >10 feet to prevent cavitation in most frac applications."
        ],
        reasoning_framework="""
        Suction valves control fluid entry into pump cylinders during the suction stroke. Inadequate suction
        conditions cause cavitation damage:

        1. CAVITATION MECHANISM: When local fluid pressure drops below vapor pressure, vapor bubbles form
           (typically during rapid flow acceleration into pump cylinder), bubbles collapse when exposed
           to higher pressure in compression stroke, collapse generates shock waves that erode metal
           surfaces, resulting in characteristic pitting pattern on valve seats and poppets.

        2. NPSH REQUIREMENTS: Net Positive Suction Head = (suction pressure + atmospheric pressure -
           vapor pressure) converted to feet of liquid head, required NPSH typically 8-15 feet depending
           on pump speed and fluid properties, available NPSH must exceed required NPSH by minimum 3
           feet margin, inadequate NPSH causes vapor lock and pump efficiency loss.

        3. SUCTION SYSTEM DESIGN: Suction manifold sized for fluid velocity <5 ft/sec (minimize friction
           loss), suction line sloped continuously upward toward pump (prevent air pockets), suction
           strainer mesh size balances debris removal vs. pressure drop (typically 20-40 mesh), elevated
           frac tanks or suction boost pumps increase available NPSH.

        4. CAVITATION DAMAGE PROGRESSION: Early stage shows fine surface pitting on valve seats (0.005-
           0.010" depth), intermediate stage exhibits coalesced pits forming rough surface (0.020-0.030"
           depth), advanced stage results in material loss exposing subsurface (>0.050" depth), ultimate
           failure involves valve breakage or severe leakage requiring immediate replacement.

        5. FIELD INDICATORS: Unusual noise from suction end (sounds like pumping gravel or rocks),
           erratic discharge pressure readings (indicates incomplete cylinder filling), pump rate decline
           at constant SPM (volumetric efficiency loss), excessive vibration at suction end of pump,
           temperature rise at suction manifold (indicates flow restriction and fluid shear heating).
        """,
        key_factors=[
            "Suction pressure measurement at pump inlet (minimum 15 PSI recommended)",
            "NPSH calculation based on tank elevation, line losses, and fluid properties",
            "Suction valve seat and poppet inspection for cavitation pitting pattern",
            "Pump inlet fluid velocity calculation (target <5 ft/sec)",
            "Suction strainer differential pressure (high delta-P indicates plugging)",
            "Volumetric efficiency trending (rapid decline suggests suction issues)"
        ],
        primary_authority=[
            "API RP 11ER: Suction system design and NPSH requirements for reciprocating pumps",
            "Hydraulic Institute Standards: NPSH calculations and cavitation prevention",
            "SPE 190041: Cavitation Damage Prevention in Frac Pump Suction Systems",
            "OEM installation manuals specifying minimum suction conditions"
        ],
        burden_holder="Frac service company operations engineer",
        adversary_position="Cavitation damage results from inadequate suction system design or operation below minimum NPSH",
        counter_arguments=[
            "Suction pressure monitored and maintained above minimum specified values",
            "NPSH calculations documented showing adequate margin for operating conditions",
            "Suction system designed per API RP 11ER guidelines (line sizing, tank elevation)",
            "Suction valves inspected at proper intervals with documented condition assessments",
            "Pump operation suspended when suction conditions degraded below minimums"
        ],
        resolution_strategy="Install suction pressure monitoring with alarm at 12 PSI (shutdown at 8 PSI), calculate NPSH for each frac tank configuration and fluid density, implement suction boost pumps for marginal NPSH conditions, maintain suction valve inspection photographic records.",
        entity_scope="All frac pumping operations using suction-fed fluid systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High certainty on cavitation mechanisms and prevention methods, moderate certainty on optimal NPSH margins for extreme fluid conditions",
        controlling_precedent="API RP 11ER minimum NPSH requirements and suction system design criteria",
        category=IssueCategory.FLUID_END,
        zone=AnalysisZone.DIAGNOSTIC
    ),

    DoctrineBlock(
        topic="Cold Weather Pump Operations and Freeze Protection",
        keywords=["cold weather", "freeze", "winterization", "glycol", "heating"],
        conclusion_template=[
            "Cold weather operations require comprehensive freeze protection: fluid end heating, glycol addition to water systems, and insulation of all wetted components.",
            "Pump startup in freezing conditions without proper preheat causes thermal shock cracking of fluid ends and valve failures.",
            "Maintain minimum fluid end temperature of 40°F before pressurization and 60°F during operation for reliable performance."
        ],
        reasoning_framework="""
        Frac pump operations in freezing temperatures (below 32°F ambient) create multiple failure modes
        requiring proactive mitigation:

        1. THERMAL SHOCK MECHANISMS: Cold-soaked metal components (fluid ends at ambient temperature)
           experience rapid heating when pumping begins (fluid temperature 40-80°F), differential thermal
           expansion creates internal stresses, stress concentrations at crossbores and valve bores
           initiate cracks, repeated thermal cycling propagates cracks to failure. Industry documented
           15+ fluid end failures from thermal shock in Bakken winter operations.

        2. FREEZE DAMAGE SCENARIOS: Water-filled pump left idle in freezing weather freezes inside fluid
           end chambers, ice expansion cracks fluid end (water expands 9% when frozen), frozen valves
           cannot open/close causing bent valve springs or broken poppets, frozen treating iron unions
           cannot be made up or broken out, frozen packing sets prevent plunger movement causing mechanical
           damage on startup attempt.

        3. PREHEAT REQUIREMENTS: Circulate heated fluid (120-150°F) through pump for minimum 30 minutes
           before pressurization, monitor fluid end temperature using contact thermometers or IR camera
           (target 60°F minimum at valve bodies), gradual pressure ramp (0-5000 PSI over 5 minutes,
           hold 5 min, 5000-10000 PSI over 5 min, hold 5 min, then to operating pressure), allows
           thermal equalization and stress relaxation.

        4. GLYCOL ANTIFREEZE SYSTEMS: Ethylene glycol or propylene glycol added to circulating water
           systems at 30-50% concentration (freeze protection to -20°F or lower), glycol in packing
           lube systems prevents freezing of stuffing boxes, glycol concentration monitoring using
           refractometer (maintain adequate freeze protection), glycol degradation from oxidation
           requires periodic replacement.

        5. INSULATION AND HEATING: Insulating blankets for fluid ends and treating iron (maintain
           heat during idle periods), electric heat tracing on manifolds and piping, hot air blowers
           for pump enclosures, engine jacket water heat exchangers to warm frac fluid, wind breaks
           and enclosures to reduce convective cooling.
        """,
        key_factors=[
            "Ambient temperature and wind chill conditions during operations",
            "Fluid end preheat time and temperature measurements before pressurization",
            "Glycol concentration in water systems and packing lube",
            "Insulation coverage and heat tracing operation status",
            "Pressure ramp rate during cold-start procedures (target <1000 PSI/min)",
            "Historical freeze damage incidents and root cause analysis results"
        ],
        primary_authority=[
            "API RP 11ER: Cold weather operating procedures for reciprocating pumps",
            "SPE 184528: Winter Frac Operations Best Practices and Lessons Learned",
            "OEM cold weather operation bulletins (SPM, Halliburton, SLB)",
            "Industry incident reports from Bakken, Marcellus winter operations"
        ],
        burden_holder="Frac service company operations supervisor",
        adversary_position="Cold weather damage is preventable through proper operating procedures",
        counter_arguments=[
            "Documented preheat procedures followed with temperature verification",
            "Glycol antifreeze systems installed and concentration verified",
            "Insulation and heat tracing systems maintained in operational condition",
            "Pressure ramp procedures implemented per OEM cold weather guidelines",
            "Training provided to crews on cold weather operational requirements",
            "Equipment damage occurred despite proper procedures due to extreme weather conditions"
        ],
        resolution_strategy="Develop comprehensive cold weather operating plan including preheat checklists and temperature monitoring, install permanent fluid end temperature monitoring with SCADA logging, implement glycol concentration testing program, maintain photographic documentation of insulation and heating system condition.",
        entity_scope="All frac operations in climates experiencing freezing temperatures",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High certainty on failure mechanisms and prevention methods, extremely high certainty on minimum temperature requirements",
        controlling_precedent="API RP 11ER cold weather operating procedures and OEM temperature specifications",
        category=IssueCategory.COLD_WEATHER,
        zone=AnalysisZone.SAFETY
    ),

    DoctrineBlock(
        topic="Proppant Erosion and Wear Mitigation",
        keywords=["proppant", "erosion", "wear", "ceramic", "carbide", "sand"],
        conclusion_template=[
            "Proppant erosion affects all wetted components: valve seats, plungers, treating iron, and manifold internals at rates proportional to proppant concentration and hardness.",
            "Ceramic proppant (bauxite, sintered) causes 2-3x more erosion than silica sand due to higher hardness (7-8 Mohs vs. 6-7 Mohs).",
            "Mitigation strategies include carbide/ceramic component upgrades, reduced flow velocities, and flush procedures between high-proppant stages."
        ],
        reasoning_framework="""
        Proppant-laden fracturing fluids cause abrasive erosion throughout the frac pump and treating
        iron system. Erosion rate depends on multiple factors:

        1. EROSION MECHANISMS: Abrasive particles (proppant) impact component surfaces at high velocity,
           material removal through micro-cutting and fatigue, erosion rate proportional to particle
           kinetic energy (velocity squared relationship), concentrated at flow direction changes
           (elbows, valve seats, crossbore intersections), cumulative material loss over job duration.

        2. PROPPANT PROPERTIES: Silica sand (20/40, 30/50, 40/70, 100 mesh) hardness 6-7 Mohs scale,
           ceramic proppant (intermediate strength) hardness 7-8 Mohs, resin-coated sand similar
           erosivity to base sand, typical concentrations 0.5-3 lb/gal during pad stage ramping to
           8-12 lb/gal at end of stage, ultra-high proppant concentration jobs (slickwater) up to
           15 lb/gal.

        3. VELOCITY-DEPENDENT EROSION: Erosion rate proportional to velocity^2.5 to velocity^3 depending
           on material and particle type, reducing flow velocity from 30 ft/sec to 15 ft/sec reduces
           erosion 5-8x, critical erosion locations: discharge valve throats (highest velocity),
           treating iron elbows and tees, manifold flow splitters, goat head (zipper) connections.

        4. MATERIAL SELECTION FOR EROSION RESISTANCE: Tungsten carbide coatings or inserts (8.5-9 Mohs
           hardness) provide 10-20x life extension vs. steel, ceramic valve seats (alumina, zirconia)
           resist erosion but are brittle and crack-prone, chrome plating on plungers provides moderate
           erosion resistance, hardened steel (RC 55-60) for treating iron internal flow paths.

        5. OPERATIONAL MITIGATION: Flush pumps with clean fluid between stages (remove settled proppant
           from fluid ends), gradual proppant ramp (0.5 lb/gal increments) reduces shock loading on
           valves, avoid pump operation at <50% speed with proppant (causes valve erosion from flutter),
           distribute high-proppant stages across pump fleet (equalize wear), inspect and replace
           heavily-worn components mid-job.
        """,
        key_factors=[
            "Proppant type and mesh size (sand vs. ceramic, 20/40 vs. 100 mesh)",
            "Proppant concentration profile during job (lb/gal vs. time)",
            "Flow velocity at critical erosion points (calculated from geometry and flow rate)",
            "Component material hardness and erosion resistance ratings",
            "Cumulative proppant pumped through specific components (lbs or tons)",
            "Inspection results showing erosion patterns and material loss measurements"
        ],
        primary_authority=[
            "SPE 184525: Proppant Erosion in Frac Pumps and Treating Iron",
            "NACE International: Erosion-corrosion studies in oilfield applications",
            "OEM component erosion resistance data (SPM carbide seats, ceramic valves)",
            "Industry benchmarking data from high-proppant slickwater operations"
        ],
        burden_holder="Frac service company engineering manager",
        adversary_position="Erosion damage is normal wear-and-tear in proppant pumping service",
        counter_arguments=[
            "Component life meets or exceeds OEM specifications for proppant type and concentration",
            "Use of premium erosion-resistant materials (carbide, ceramic) demonstrates proactive approach",
            "Operational procedures minimize erosion (flush cycles, velocity management)",
            "Premature erosion failures correlate to customer-specified proppant exceeding design basis",
            "Inspection and replacement performed at appropriate intervals based on actual wear"
        ],
        resolution_strategy="Track component erosion life by proppant type and cumulative tons pumped, perform erosion rate testing for novel proppant types, implement flow modeling to identify high-velocity erosion zones, upgrade critical components to carbide or ceramic in severe service applications.",
        entity_scope="All frac operations pumping proppant-laden fluids",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High certainty on erosion mechanisms and material performance, moderate certainty on optimal velocity limits for specific proppant types",
        controlling_precedent="Industry best practices and OEM erosion resistance data",
        category=IssueCategory.FLUID_END,
        zone=AnalysisZone.MAINTENANCE
    ),

    DoctrineBlock(
        topic="Chemical Compatibility and Fluid End Corrosion",
        keywords=["chemical", "corrosion", "acid", "compatibility", "degradation"],
        conclusion_template=[
            "Frac fluid chemical compatibility with pump materials prevents corrosion failures including stress corrosion cracking, pitting, and uniform metal loss.",
            "High-strength steel fluid ends are susceptible to hydrogen embrittlement from acid exposure and cathodic protection systems.",
            "Flush pumps with neutralizing solution after acid jobs and inspect for corrosion damage before returning to service."
        ],
        reasoning_framework="""
        Fracturing fluids contain numerous chemicals: acids (HCl 15-28% for acid frac), biocides
        (glutaraldehyde, THPS), corrosion inhibitors, friction reducers, scale inhibitors, breakers.
        Chemical compatibility analysis is critical:

        1. ACID CORROSION MECHANISMS: Hydrochloric acid (HCl) attacks steel fluid ends causing uniform
           corrosion and pitting, corrosion rate depends on acid concentration (28% HCl > 15% HCl),
           temperature (higher temperature accelerates), and inhibitor effectiveness, hydrogen generated
           during corrosion diffuses into high-strength steel (yield strength >140 ksi) causing hydrogen
           embrittlement, delayed cracking can occur hours to days after acid exposure.

        2. MATERIAL SUSCEPTIBILITY: AISI 4140 steel (common fluid end material) susceptible to hydrogen
           embrittlement when exposed to acid, 300-series stainless steel more corrosion resistant but
           subject to chloride stress corrosion cracking, Inconel/Hastelloy alloys provide excellent
           acid resistance but cost-prohibitive for fluid ends, corrosion inhibitor films (filming
           amines, quaternary ammonium compounds) provide temporary protection.

        3. STRESS CORROSION CRACKING: Combination of tensile stress (operational pressure creates hoop
           stress in fluid end), corrosive environment (acid, chlorides from produced water), and
           susceptible material (high-strength steel) results in crack initiation and propagation,
           cracks typically initiate at stress concentrations (crossbores, thread roots), propagate
           rapidly under continued stress and exposure.

        4. BIOCIDE COMPATIBILITY: Glutaraldehyde and THPS (tetrakis hydroxymethyl phosphonium sulfate)
           biocides can attack elastomer seals and packing, degradation manifests as swelling, hardening,
           or cracking of seals, compatibility testing required for novel biocide formulations, Viton
           seals generally more resistant than Buna-N to aggressive chemicals.

        5. POST-ACID FLUSH PROCEDURES: Circulate neutralizing solution (sodium bicarbonate 5-10% in
           water) through pumps for minimum 30 minutes after acid job, measure pH of discharge water
           (target pH 7-9 before shutdown), visual inspection of fluid ends for corrosion pitting or
           surface attack, consider NDT inspection (MPI, UT) after high-concentration acid exposure,
           document chemical exposure history for each pump unit.
        """,
        key_factors=[
            "Acid type and concentration (HCl 15% vs. 28%, HF/HCl mixtures)",
            "Total acid volume pumped and exposure duration (hours of contact time)",
            "Corrosion inhibitor type and concentration (effectiveness testing)",
            "Fluid end material composition and heat treatment (hardness, yield strength)",
            "Neutralization flush procedures and pH verification",
            "Post-acid inspection results (visual, MPI, UT for cracks)"
        ],
        primary_authority=[
            "NACE SP0390: Management of Corrosion in the Oilfield",
            "SPE 184520: Frac Pump Corrosion from Acid and Chemical Exposure",
            "API RP 11ER: Chemical compatibility and corrosion prevention for reciprocating pumps",
            "Material compatibility charts from fluid end manufacturers"
        ],
        burden_holder="Frac service company HSE manager and operations supervisor",
        adversary_position="Corrosion damage results from inadequate post-job flush procedures or improper chemical selection",
        counter_arguments=[
            "Documented neutralization flush procedures following all acid jobs",
            "Corrosion inhibitor performance verified through coupon testing or electrochemical methods",
            "Material selection appropriate for anticipated chemical exposure (fluid end specifications)",
            "Post-acid inspection performed with documented results before return to service",
            "Chemical exposure history maintained for each pump unit (cumulative acid volume, concentrations)"
        ],
        resolution_strategy="Implement chemical exposure tracking database for each pump unit, perform corrosion coupon testing for novel chemical systems, require post-acid NDT inspection for high-concentration exposures, establish material upgrade criteria for severe service (stainless wetted components).",
        entity_scope="All frac operations using acid or aggressive chemical systems",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="High certainty on corrosion mechanisms and prevention methods, moderate certainty on long-term effects of novel chemical formulations without field data",
        controlling_precedent="NACE standards and API RP 11ER chemical compatibility requirements",
        category=IssueCategory.CHEMICAL_COMPATIBILITY,
        zone=AnalysisZone.SAFETY
    ),

    DoctrineBlock(
        topic="Pressure Relief Valve Sizing and Testing",
        keywords=["pressure relief", "pop-off", "safety valve", "overpressure"],
        conclusion_template=[
            "Pressure relief valves must be sized to pass full pump capacity at set pressure to prevent overpressure conditions during blockage or valve closure.",
            "Relief valve set pressure typically 110-115% of maximum anticipated treating pressure, tested annually per ASME Section VIII requirements.",
            "Relief valve discharge must be piped to safe location (frac pit) to prevent high-pressure fluid spray hazards."
        ],
        reasoning_framework="""
        Pressure relief protection prevents catastrophic overpressure failures when treating iron valves
        close or wellbore restrictions occur during pumping:

        1. OVERPRESSURE SCENARIOS: Operator closes wellhead valve while pumps operating (deliberate or
           accidental), wellbore bridges or screens out causing rapid pressure buildup, automated
           emergency shutdown closes valves but pumps continue briefly (control lag time), pump pressure
           can rise from 10,000 PSI to 18,000+ PSI in <2 seconds without relief protection.

        2. RELIEF VALVE SIZING: Required capacity = maximum pump flow rate at relief set pressure,
           typical frac pump 10-12 BPM at 15,000 PSI, relief valve must pass full flow at set pressure
           (typically 16,500-17,000 PSI for 15,000 PSI rated system), undersized relief valve cannot
           prevent overpressure (pressure continues rising even with relief open), multiple pumps
           require larger relief valves or multiple relief points.

        3. SET PRESSURE SELECTION: Maximum anticipated treating pressure (typically 12,000-14,000 PSI
           for most formations), relief set pressure at 110-115% of maximum treating pressure (provides
           protection margin while preventing nuisance trips), must be below minimum component pressure
           rating in system (treating iron 15,000 PSI working pressure, 22,500 PSI test pressure per
           API spec).

        4. TESTING REQUIREMENTS: Annual pressure testing per ASME Section VIII or manufacturer
           recommendations, pop test (verify opening pressure within ±3% of set pressure), reseat test
           (verify valve closes and holds pressure after relieving), flow capacity test (verify valve
           passes rated flow at set pressure), inspection of internal components (disc, seat, spring),
           documentation of test results and any repairs or adjustments.

        5. DISCHARGE PIPING: Relief discharge piped to frac pit or other safe collection point (never
           open to atmosphere creating spray hazard), discharge line sized for relief flow capacity
           (minimize backpressure on relief valve), avoid elbows and restrictions in discharge line
           (backpressure reduces relief capacity), consider noise levels from high-velocity discharge
           (hearing protection required in vicinity).
        """,
        key_factors=[
            "Relief valve set pressure vs. maximum treating pressure and component ratings",
            "Relief valve flow capacity vs. total pump capacity at set pressure",
            "Annual testing results (pop pressure, reseat pressure, leakage)",
            "Discharge piping adequacy (size, routing, backpressure calculation)",
            "Overpressure incident history (unintended relief actuations, pressure spikes)",
            "Multiple pump configurations and total flow requiring relief capacity"
        ],
        primary_authority=[
            "ASME Section VIII: Pressure relief device requirements for pressure vessels",
            "API RP 520: Sizing, Selection, and Installation of Pressure Relief Devices",
            "API RP 53: Blowout prevention equipment systems (includes pressure relief)",
            "OEM relief valve testing and maintenance procedures"
        ],
        burden_holder="Frac service company HSE manager",
        adversary_position="Pressure relief systems installed and tested per industry standards",
        counter_arguments=[
            "Relief valves sized per API RP 520 for full pump flow capacity",
            "Annual testing performed by qualified technicians with documented results",
            "Relief discharge piped to safe location per API RP 53 requirements",
            "Set pressures appropriate for equipment ratings and operational pressures",
            "Overpressure incidents prevented through proper relief system design and maintenance"
        ],
        resolution_strategy="Maintain comprehensive relief valve test records with set pressure trending, perform flow capacity verification testing (not just pop testing), implement relief actuation event investigation protocol, consider redundant relief valves for critical high-capacity applications.",
        entity_scope="All frac operations using high-pressure pumping systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Extremely high certainty on relief valve sizing and testing requirements, high certainty on overpressure scenario analysis",
        controlling_precedent="ASME Section VIII and API RP 520 relief valve requirements",
        category=IssueCategory.SAFETY_SYSTEMS,
        zone=AnalysisZone.SAFETY
    ),

    DoctrineBlock(
        topic="Real-Time Pump Monitoring and SCADA Integration",
        keywords=["SCADA", "monitoring", "sensors", "telemetry", "automation"],
        conclusion_template=[
            "Real-time monitoring systems track pump performance (pressure, rate, power), mechanical health (vibration, temperature, oil analysis), and safety parameters.",
            "SCADA integration enables automated shutdown on critical alarms (low suction pressure, high vibration, lube oil loss) preventing catastrophic failures.",
            "Monitoring data provides predictive maintenance insights reducing unplanned downtime by 30-50% compared to reactive maintenance approaches."
        ],
        reasoning_framework="""
        Modern frac pump operations implement comprehensive monitoring and automation for performance
        optimization and failure prevention:

        1. SENSOR SUITE: Discharge pressure transducers (0-20,000 PSI range, ±0.25% accuracy), suction
           pressure transducers (0-100 PSI), flow meters (Coriolis or magnetic for rate verification),
           vibration sensors (accelerometers on power end, alarm at 0.3 in/sec RMS), temperature sensors
           (lube oil, bearing housings, fluid end), engine monitoring (RPM, fuel rate, exhaust temp,
           coolant temp, oil pressure).

        2. SCADA ARCHITECTURE: Field sensors connected to PLC or RTU (remote terminal unit), data
           transmitted to central control van via wireless (900 MHz, 2.4 GHz) or hardwired network,
           HMI (human-machine interface) displays real-time trends and alarm status, data historian
           stores time-series data for analysis (typical 1-second sampling rate), automated control
           logic implements safety interlocks and optimization algorithms.

        3. CRITICAL ALARM LOGIC: Low suction pressure (<10 PSI triggers warning, <8 PSI automatic
           shutdown to prevent cavitation), high vibration (>0.3 in/sec warning, >0.5 in/sec shutdown
           prevents bearing failure), low lube oil pressure (<20 PSI warning, <15 PSI shutdown prevents
           bearing damage), high bearing temperature (>200°F warning, >220°F shutdown), overpressure
           (>16,000 PSI triggers automatic pump shutdown).

        4. PERFORMANCE ANALYTICS: Volumetric efficiency calculation from flow meter vs. theoretical
           displacement, hydraulic horsepower trending (detects valve leakage or plunger wear), power
           consumption analysis (identifies mechanical inefficiency), pressure pulsation analysis
           (FFT to detect valve timing issues or fluid end cracks), rate variance trending (indicates
           developing mechanical problems).

        5. PREDICTIVE MAINTENANCE INTEGRATION: Vibration spectrum analysis for bearing fault frequencies
           (BPFI, BPFO, BSF, FTF), oil analysis data integration (wear metal trending triggers inspection),
           temperature trending for bearing condition (gradual rise indicates developing failure),
           efficiency trending triggers valve inspection (drop from 95% to 90% efficiency), machine
           learning algorithms predict remaining useful life for components.
        """,
        key_factors=[
            "Sensor calibration status and accuracy verification (annual calibration recommended)",
            "SCADA system uptime and data quality (percentage of valid data points)",
            "Alarm setpoint appropriateness vs. actual failure thresholds",
            "Historical data retention period (minimum 1 year for trending analysis)",
            "Automated response system reliability (verify shutdown logic testing)",
            "Integration with maintenance management system (work order generation from alarms)"
        ],
        primary_authority=[
            "ISA-95: Enterprise-Control System Integration standards",
            "API RP 11ER: Monitoring and control recommendations for reciprocating pumps",
            "SPE 190044: Real-Time Frac Pump Monitoring and Predictive Maintenance",
            "Industry best practices from major service companies (SLB, HAL, Liberty)"
        ],
        burden_holder="Frac service company automation engineer",
        adversary_position="Monitoring systems installed and alarmed per industry standards",
        counter_arguments=[
            "Comprehensive sensor suite providing real-time visibility to pump health",
            "Automated shutdown logic prevents equipment damage from critical failures",
            "Historical data trending enables predictive maintenance planning",
            "Alarm setpoints established based on OEM specifications and field experience",
            "Regular calibration and testing of monitoring systems ensures data quality"
        ],
        resolution_strategy="Implement centralized monitoring dashboard for entire pump fleet, integrate real-time monitoring data with maintenance management system (CMMS), perform periodic alarm response testing to verify automated safety functions, use historical data for component life modeling and inventory optimization.",
        entity_scope="All frac service companies operating modern pump fleets",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High certainty on monitoring system design and alarm logic, moderate certainty on optimal predictive maintenance algorithms without extensive field validation",
        controlling_precedent="ISA-95 standards and API RP 11ER monitoring recommendations",
        category=IssueCategory.MONITORING,
        zone=AnalysisZone.DIAGNOSTIC
    ),

    DoctrineBlock(
        topic="Pump Fleet Management and Deployment Optimization",
        keywords=["fleet", "deployment", "utilization", "lifecycle", "replacement"],
        conclusion_template=[
            "Optimal fleet management balances pump utilization (target 70-85% annual utilization), lifecycle cost management, and reliability for contracted performance obligations.",
            "Pump retirement decisions consider cumulative operating hours, major component replacement history, and cost per operating hour trending.",
            "Strategic spare component inventory (fluid ends, power ends, valves) minimizes downtime and enables rapid job recovery from failures."
        ],
        reasoning_framework="""
        Frac service companies operate pump fleets of 50-500+ units requiring strategic management for
        financial and operational performance:

        1. LIFECYCLE PHASES: New pump commissioning (0-2000 hours, break-in period, higher failure rates
           from initial defects), prime operating life (2000-10,000 hours, peak reliability and efficiency),
           mature phase (10,000-20,000 hours, increasing maintenance frequency and component replacement
           costs), end-of-life consideration (>20,000 hours, evaluate rebuild vs. replacement economics).

        2. UTILIZATION OPTIMIZATION: Target annual utilization 70-85% (6100-7400 hours per year),
           underutilization (<60%) indicates excess fleet capacity or poor market positioning,
           overutilization (>90%) increases failure rates and reduces maintenance windows, rotating pumps
           across jobs distributes wear and allows maintenance scheduling, high-hour units assigned to
           lower-intensity jobs (pad stages, lower pressure applications).

        3. COMPONENT REPLACEMENT STRATEGY: Fluid end replacement at 8,000-12,000 hours or when crack
           detection occurs, power end rebuild at 12,000-18,000 hours (bearings, crankshaft inspection),
           engine overhaul at manufacturer intervals (typically 20,000-30,000 hours for oil field engines),
           preventive component replacement before failure (valves, plungers, packing at recommended
           intervals).

        4. COST PER HOUR TRENDING: Track total operating cost per pump hour (fuel, labor, maintenance,
           major repairs), new pumps typically $45-65 per operating hour, mature pumps $75-120 per
           operating hour as maintenance increases, cost trajectory analysis triggers rebuild vs.
           replacement decision, residual value assessment for end-of-life units (parts recovery,
           resale, scrap).

        5. SPARE INVENTORY OPTIMIZATION: Critical spares (complete fluid ends, valve sets, plunger sets)
           sized for 5-10% of fleet based on failure rate analysis, common consumables (packing, seals,
           fasteners) stocked at field locations, regional warehousing for major components (power ends,
           engines) to serve multiple operating areas, inventory turns target 4-6x annually (balance
           availability vs. carrying cost).
        """,
        key_factors=[
            "Fleet utilization rate (operating hours vs. available hours)",
            "Cost per operating hour by pump unit and age cohort",
            "Major component replacement frequency and costs",
            "Failure rate trending by component type and pump age",
            "Market demand forecasting for capacity planning",
            "Residual value assessment for aging units"
        ],
        primary_authority=[
            "SPE 190045: Frac Pump Fleet Management and Lifecycle Cost Optimization",
            "Industry benchmarking data from service company financial reports",
            "OEM residual value and rebuild cost estimates",
            "Equipment financing and leasing analysis standards"
        ],
        burden_holder="Frac service company CFO and operations VP",
        adversary_position="Fleet management practices optimize equipment utilization and lifecycle costs",
        counter_arguments=[
            "Fleet utilization within industry benchmark ranges (70-85%)",
            "Preventive maintenance program extends pump life and controls cost per hour",
            "Component replacement strategy balances reliability and cost optimization",
            "Spare inventory levels support contractual uptime commitments",
            "Pump retirement decisions based on comprehensive lifecycle cost analysis"
        ],
        resolution_strategy="Implement fleet management software tracking utilization, cost per hour, and component life, develop predictive models for component replacement timing, perform annual fleet optimization analysis (retire/rebuild/acquire decisions), benchmark performance against industry peers.",
        entity_scope="All frac service companies operating multi-unit pump fleets",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High certainty on fleet management principles and cost analysis methods, moderate certainty on optimal utilization targets varying by market conditions",
        controlling_precedent="Industry best practices and financial management standards",
        category=IssueCategory.FLEET_MANAGEMENT,
        zone=AnalysisZone.MAINTENANCE
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    question: str = Field(..., description="Frac pump diagnostic question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    triggered_doctrines: List[str]
    categories: List[IssueCategory]
    analysis_zone: AnalysisZone
    determinism_hash: str
    timestamp: str
    query_duration_ms: float


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrine_count: int
    categories: List[str]
    uptime_seconds: float
    total_queries: int
    avg_query_ms: float


# ═══════════════════════════════════════════════════════════════════════════
# CORE ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class FracPumpDiagnosticsEngine:
    def __init__(self):
        self.start_time = time.time()
        self.query_count = 0
        self.total_query_time = 0.0

        # Telemetry
        self.telemetry: Dict[str, Any] = {
            "queries": [],
            "doctrine_hits": Counter(),
            "category_hits": Counter(),
            "mode_distribution": Counter(),
            "confidence_distribution": Counter(),
        }

        # Build semantic keyword index
        self.keyword_index: Dict[str, List[int]] = defaultdict(list)
        for idx, doctrine in enumerate(DOCTRINE_CACHE):
            for keyword in doctrine.keywords:
                normalized = keyword.lower().strip()
                self.keyword_index[normalized].append(idx)

        logger.info(f"OFE03 Frac Pump Diagnostics Engine initialized with {len(DOCTRINE_CACHE)} doctrine blocks")

    def three_layer_response(self, question: str, mode: ResponseMode, context: Optional[Dict] = None) -> Tuple[str, List[DoctrineBlock], ConfidenceLevel, AnalysisZone]:
        """
        Layer 1: Doctrine Cache (0-200ms)
        Layer 2: Semantic Retrieval (200-500ms)
        Layer 3: Deep Analysis (500ms+)
        """
        start = time.time()

        # Layer 1: Fast doctrine cache lookup
        triggered = self._doctrine_cache_lookup(question)

        if triggered and mode == ResponseMode.FAST:
            answer = self._format_fast_response(triggered)
            confidence = self._determine_confidence(triggered)
            zone = self._determine_zone(triggered)
            logger.info(f"Layer 1 cache hit: {len(triggered)} doctrines, {(time.time()-start)*1000:.1f}ms")
            return answer, triggered, confidence, zone

        # Layer 2: Semantic expansion
        if not triggered or len(triggered) < 3:
            triggered = self._semantic_retrieval(question)

        if mode == ResponseMode.DEFENSE:
            answer = self._format_defense_response(question, triggered, context)
            confidence = self._determine_confidence(triggered)
            zone = self._determine_zone(triggered)
            logger.info(f"Layer 2 semantic: {len(triggered)} doctrines, {(time.time()-start)*1000:.1f}ms")
            return answer, triggered, confidence, zone

        # Layer 3: Deep analysis for MEMO mode
        answer = self._format_memo_response(question, triggered, context)
        confidence = self._determine_confidence(triggered)
        zone = self._determine_zone(triggered)
        logger.info(f"Layer 3 deep analysis: {len(triggered)} doctrines, {(time.time()-start)*1000:.1f}ms")
        return answer, triggered, confidence, zone

    def _doctrine_cache_lookup(self, question: str) -> List[DoctrineBlock]:
        """Fast keyword-based doctrine retrieval"""
        question_lower = question.lower()
        question_tokens = set(question_lower.split())

        scores: Dict[int, float] = defaultdict(float)

        # Keyword matching
        for token in question_tokens:
            if token in self.keyword_index:
                for doc_idx in self.keyword_index[token]:
                    scores[doc_idx] += 1.0

        # Topic matching (partial)
        for idx, doctrine in enumerate(DOCTRINE_CACHE):
            topic_tokens = set(doctrine.topic.lower().split())
            overlap = len(question_tokens & topic_tokens)
            if overlap > 0:
                scores[idx] += overlap * 0.5

        # Sort by score and return top matches
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, score in ranked[:5] if score > 0]

        return [DOCTRINE_CACHE[idx] for idx in top_indices]

    def _semantic_retrieval(self, question: str) -> List[DoctrineBlock]:
        """Semantic expansion when cache misses"""
        question_lower = question.lower()

        # Broader semantic matching
        all_scores: Dict[int, float] = defaultdict(float)

        for idx, doctrine in enumerate(DOCTRINE_CACHE):
            score = 0.0

            # Check reasoning framework
            if any(word in doctrine.reasoning_framework.lower() for word in question_lower.split()):
                score += 2.0

            # Check key factors
            for factor in doctrine.key_factors:
                if any(word in factor.lower() for word in question_lower.split()):
                    score += 1.0

            # Check category relevance
            if doctrine.category.value in question_lower:
                score += 3.0

            all_scores[idx] = score

        ranked = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, score in ranked[:8] if score > 0]

        return [DOCTRINE_CACHE[idx] for idx in top_indices]

    def _format_fast_response(self, doctrines: List[DoctrineBlock]) -> str:
        """Concise answer for FAST mode"""
        if not doctrines:
            return "No specific doctrine matched. Recommend detailed inspection and diagnostic testing."

        primary = doctrines[0]
        answer_parts = [
            f"**{primary.topic}**\n",
            "\n".join(f"• {conclusion}" for conclusion in primary.conclusion_template[:2]),
        ]

        if len(doctrines) > 1:
            answer_parts.append(f"\n\n**Related areas:** {', '.join(d.topic for d in doctrines[1:3])}")

        return "\n".join(answer_parts)

    def _format_defense_response(self, question: str, doctrines: List[DoctrineBlock], context: Optional[Dict]) -> str:
        """Audit-ready response for DEFENSE mode"""
        if not doctrines:
            return self._format_fallback_response(question)

        primary = doctrines[0]

        sections = [
            f"# {primary.topic}\n",
            "## Executive Summary",
            "\n".join(primary.conclusion_template),
            "\n## Technical Analysis",
            primary.reasoning_framework[:800],
            "\n## Key Diagnostic Factors",
            "\n".join(f"• {factor}" for factor in primary.key_factors[:6]),
            "\n## Authoritative References",
            "\n".join(f"• {ref}" for ref in primary.primary_authority),
            f"\n## Confidence Assessment",
            f"**Level:** {primary.confidence.value}",
            f"**Basis:** {primary.confidence_stratification}",
        ]

        if len(doctrines) > 1:
            sections.append("\n## Related Considerations")
            for doc in doctrines[1:3]:
                sections.append(f"**{doc.topic}:** {doc.conclusion_template[0]}")

        return "\n".join(sections)

    def _format_memo_response(self, question: str, doctrines: List[DoctrineBlock], context: Optional[Dict]) -> str:
        """Comprehensive memo for MEMO mode"""
        if not doctrines:
            return self._format_fallback_response(question)

        primary = doctrines[0]

        sections = [
            f"# DIAGNOSTIC MEMORANDUM: {primary.topic}\n",
            f"**Date:** {datetime.utcnow().strftime('%Y-%m-%d')}",
            f"**Subject:** {question}",
            f"**Classification:** {primary.zone.value} | {primary.category.value.replace('_', ' ').title()}\n",
            "## EXECUTIVE SUMMARY",
            "\n".join(primary.conclusion_template),
            "\n## DETAILED TECHNICAL ANALYSIS",
            primary.reasoning_framework,
            "\n## CRITICAL DIAGNOSTIC FACTORS",
            "\n".join(f"{i+1}. {factor}" for i, factor in enumerate(primary.key_factors)),
            "\n## AUTHORITATIVE BASIS",
            "\n".join(f"• {ref}" for ref in primary.primary_authority),
            "\n## RISK ASSESSMENT",
            f"**Primary Risk Holder:** {primary.burden_holder}",
            f"\n**Adversarial Position:** {primary.adversary_position}",
            "\n**Counter-Arguments:**",
            "\n".join(f"• {arg}" for arg in primary.counter_arguments[:5]),
            f"\n## RESOLUTION STRATEGY",
            primary.resolution_strategy,
            f"\n## CONFIDENCE ASSESSMENT",
            f"**Level:** {primary.confidence.value}",
            f"**Stratification:** {primary.confidence_stratification}",
            f"**Controlling Precedent:** {primary.controlling_precedent}",
        ]

        if len(doctrines) > 1:
            sections.append("\n## RELATED TECHNICAL DOMAINS")
            for doc in doctrines[1:4]:
                sections.append(f"\n### {doc.topic}")
                sections.append(doc.conclusion_template[0])
                sections.append(f"**Key Factors:** {', '.join(doc.key_factors[:3])}")

        sections.append("\n---")
        sections.append("*This analysis is based on industry best practices, OEM specifications, and field experience in frac pump operations.*")

        return "\n".join(sections)

    def _format_fallback_response(self, question: str) -> str:
        """Generic response when no doctrines match"""
        return f"""
# Frac Pump Diagnostic Analysis

**Question:** {question}

**Assessment:** No specific pre-compiled doctrine matched this query. Recommend:

1. **Immediate Actions:**
   - Detailed visual inspection of affected components
   - Review recent operational history and maintenance records
   - Check SCADA monitoring data for abnormal trends

2. **Diagnostic Testing:**
   - Pressure testing of suspected components
   - NDT inspection (MPI, UT) if structural integrity concerns
   - Oil analysis if power end or lubrication related
   - Vibration analysis if mechanical issues suspected

3. **Expert Consultation:**
   - Contact OEM technical support with specific symptoms
   - Engage qualified pump technicians for hands-on diagnosis
   - Review similar incidents in industry databases (SPE, IADC)

4. **Documentation:**
   - Photograph all relevant components and conditions
   - Log operational parameters at time of issue
   - Maintain chain of custody for failed components (metallurgical analysis)

**Confidence:** DISCLOSURE - Generic guidance pending specific diagnostic data.
"""

    def _determine_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Determine overall confidence from triggered doctrines"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        primary = doctrines[0]
        if len(doctrines) >= 3 and primary.confidence == ConfidenceLevel.DEFENSIBLE:
            return ConfidenceLevel.DEFENSIBLE

        return primary.confidence

    def _determine_zone(self, doctrines: List[DoctrineBlock]) -> AnalysisZone:
        """Determine primary analysis zone"""
        if not doctrines:
            return AnalysisZone.DIAGNOSTIC

        zone_counts = Counter(d.zone for d in doctrines)
        return zone_counts.most_common(1)[0][0]

    def _calculate_determinism_hash(self, question: str, answer: str, triggered: List[DoctrineBlock]) -> str:
        """SHA-256 hash for response reproducibility"""
        content = f"{question}||{answer}||{','.join(d.topic for d in triggered)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def query(self, request: QueryRequest) -> QueryResponse:
        """Main query endpoint"""
        start = time.time()

        answer, triggered, confidence, zone = self.three_layer_response(
            request.question, request.mode, request.context
        )

        duration_ms = (time.time() - start) * 1000

        # Telemetry
        self.query_count += 1
        self.total_query_time += duration_ms
        self.telemetry["queries"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "question": request.question[:100],
            "mode": request.mode.value,
            "duration_ms": duration_ms,
            "doctrines_triggered": len(triggered),
        })

        for doc in triggered:
            self.telemetry["doctrine_hits"][doc.topic] += 1
            self.telemetry["category_hits"][doc.category.value] += 1

        self.telemetry["mode_distribution"][request.mode.value] += 1
        self.telemetry["confidence_distribution"][confidence.value] += 1

        categories = list(set(d.category for d in triggered))

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            mode=request.mode,
            triggered_doctrines=[d.topic for d in triggered],
            categories=categories,
            analysis_zone=zone,
            determinism_hash=self._calculate_determinism_hash(request.question, answer, triggered),
            timestamp=datetime.utcnow().isoformat(),
            query_duration_ms=round(duration_ms, 2)
        )

    def health(self) -> HealthResponse:
        """Health check endpoint"""
        uptime = time.time() - self.start_time
        avg_query_ms = self.total_query_time / self.query_count if self.query_count > 0 else 0

        return HealthResponse(
            status="healthy",
            engine="OFE03_frac_pump_diagnostics",
            version="1.0.0",
            port=9003,
            doctrine_count=len(DOCTRINE_CACHE),
            categories=[cat.value for cat in IssueCategory],
            uptime_seconds=round(uptime, 1),
            total_queries=self.query_count,
            avg_query_ms=round(avg_query_ms, 2)
        )


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

APP = FastAPI(
    title="OFE03 - Frac Pump Diagnostics Engine",
    description="TIE Gold Standard engine for quintuplex frac pump diagnostics and maintenance",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = FracPumpDiagnosticsEngine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Main diagnostic query endpoint

    Modes:
    - FAST: Concise answer (0-200ms)
    - DEFENSE: Audit-ready analysis (200-500ms)
    - MEMO: Comprehensive technical memorandum (500ms+)
    """
    try:
        return engine.query(request)
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check and statistics"""
    return engine.health()


@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "zone": d.zone.value,
                "keywords": d.keywords[:5],
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


@APP.get("/telemetry")
async def telemetry_endpoint():
    """Query telemetry and analytics"""
    return {
        "total_queries": engine.query_count,
        "avg_query_ms": round(engine.total_query_time / engine.query_count, 2) if engine.query_count > 0 else 0,
        "doctrine_hits": dict(engine.telemetry["doctrine_hits"].most_common(10)),
        "category_distribution": dict(engine.telemetry["category_hits"]),
        "mode_distribution": dict(engine.telemetry["mode_distribution"]),
        "confidence_distribution": dict(engine.telemetry["confidence_distribution"]),
        "recent_queries": engine.telemetry["queries"][-20:]
    }


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info("Starting OFE03 Frac Pump Diagnostics Engine on port 9003")
    uvicorn.run(APP, host="0.0.0.0", port=9003, log_level="info")
