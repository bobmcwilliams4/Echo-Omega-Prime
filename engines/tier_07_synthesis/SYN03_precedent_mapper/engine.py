"""
SYN03 Precedent Mapper Engine v1.0.0
TIE-Grade Legal Precedent Network Analysis
Port: 9163

Maps citation networks, authority hierarchies, treatment tracking, circuit splits,
binding vs persuasive authority, overruling analysis, trend identification.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# === CONFIGURATION ===
ENGINE_ID = "SYN03"
ENGINE_NAME = "Precedent Mapper"
VERSION = "1.0.0"
PORT = 9163

# === PYDANTIC MODELS ===
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    mode: Literal["FAST", "DEFENSE", "MEMO"] = "FAST"
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query_id: str
    query: str
    mode: str
    response: str
    confidence: str
    authority_chain: List[str]
    determinism_hash: str
    latency_ms: float
    triggered_doctrines: List[str]
    metadata: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    engine_name: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float
    error_rate: float

# === DOCTRINE BLOCK MODEL ===
class DoctrineBlock:
    def __init__(self, topic: str, keywords: List[str], conclusion_template: str,
                 reasoning_framework: str, key_factors: List[str], primary_authority: List[str],
                 burden_holder: str, adversary_position: str, counter_arguments: List[str],
                 resolution_strategy: str, entity_scope: str, confidence: str,
                 confidence_stratification: str, controlling_precedent: str):
        self.topic = topic
        self.keywords = keywords
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.burden_holder = burden_holder
        self.adversary_position = adversary_position
        self.counter_arguments = counter_arguments
        self.resolution_strategy = resolution_strategy
        self.entity_scope = entity_scope
        self.confidence = confidence
        self.confidence_stratification = confidence_stratification
        self.controlling_precedent = controlling_precedent

# === DOCTRINE CACHE ===
DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Stare Decisis Principles",
        keywords=["stare decisis", "precedent binding", "follow precedent", "overrule standard", "settled law"],
        conclusion_template="Under stare decisis, courts follow precedent unless special justification exists. Vertical stare decisis is absolute; horizontal allows reconsideration in rare cases. Overruling requires changed circumstances, unworkability, or serious injustice.",
        reasoning_framework="""Stare decisis promotes stability, predictability, uniformity. Lower courts MUST follow higher courts (vertical). Same-level courts generally follow own precedent (horizontal) but may overrule. Supreme Court overrules only when: (1) precedent unworkable, (2) badly reasoned, (3) circumstances changed, (4) reliance minimal. Factors: age of precedent, reliance interests, consistency with other doctrine, quality of reasoning.""",
        key_factors=["vertical vs horizontal", "overruling standard", "reliance interests", "workability", "quality of reasoning"],
        primary_authority=["Payne v Tennessee 501 US 808", "Planned Parenthood v Casey 505 US 833", "Dobbs v Jackson 142 S Ct 2228"],
        burden_holder="Party seeking to overturn precedent",
        adversary_position="Precedent creates settled expectations",
        counter_arguments=["Precedent wrongly decided", "Changed social conditions", "Unworkable in practice", "Outlier vs other circuits"],
        resolution_strategy="Apply special justification standard. Assess reliance, workability, reasoning quality.",
        entity_scope="All courts",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Dobbs v Jackson 2022"
    ),
    DoctrineBlock(
        topic="Binding vs Persuasive Authority",
        keywords=["binding authority", "persuasive authority", "mandatory precedent", "authority weight", "jurisdictional hierarchy"],
        conclusion_template="Binding authority is precedent from higher court in same jurisdiction that must be followed. Persuasive authority from coordinate/lower courts or other jurisdictions may be considered but not controlling.",
        reasoning_framework="""Hierarchical structure: SCOTUS binds all federal/state courts. Circuit Court binds district courts in circuit. State supreme court binds lower state courts. Same-circuit panel binds itself absent en banc overruling. Different circuit decisions are persuasive only. State court decisions persuasive in federal court on state law issues. Persuasive weight factors: court prestige, reasoning quality, factual similarity, recency, consensus among jurisdictions.""",
        key_factors=["jurisdictional hierarchy", "vertical stare decisis", "lateral persuasion", "quality of reasoning", "trend among jurisdictions"],
        primary_authority=["Hart v Massanari 266 F3d 1155", "Camreta v Greene 563 US 692"],
        burden_holder="Party arguing against binding precedent must distinguish or seek overruling",
        adversary_position="Persuasive authority shows better approach",
        counter_arguments=["Binding precedent distinguishable on facts", "Persuasive authority better reasoned", "Trend away from binding precedent"],
        resolution_strategy="Identify jurisdiction. Apply vertical stare decisis strictly. Consider persuasive authority for reasoning guidance.",
        entity_scope="All courts",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Hart v Massanari 9th Cir 2001"
    ),
    DoctrineBlock(
        topic="Circuit Split Identification",
        keywords=["circuit split", "intercircuit conflict", "certiorari factor", "conflicting precedent", "forum shopping"],
        conclusion_template="Circuit split exists when different federal circuits reach conflicting conclusions on same legal issue. Creates forum shopping risk and certiorari likelihood under Supreme Court Rule 10.",
        reasoning_framework="""Split types: (1) direct conflict - opposite holdings on identical issue, (2) approach conflict - different tests/standards, (3) outcome conflict - same rule different results. Supreme Court grants cert to resolve splits (Rule 10(a)). District courts follow own circuit even if minority view. Forum shopping incentivizes litigants to file in favorable circuit. Depth of split matters - 2 circuits vs 8 circuits. Recency and practical importance affect cert likelihood.""",
        key_factors=["direct vs approach conflict", "number of circuits split", "practical importance", "forum shopping risk", "cert likelihood"],
        primary_authority=["Sup Ct Rule 10", "Wisniewski v United States 353 US 901"],
        burden_holder="Party seeking cert based on split must show genuine conflict",
        adversary_position="No real split, cases distinguishable",
        counter_arguments=["Factual differences", "Different statutory language", "Split acknowledged but issue unimportant", "Percolation beneficial"],
        resolution_strategy="Compare holdings and reasoning. Identify identical legal question. Count circuits. Assess practical impact.",
        entity_scope="Federal appellate courts",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Supreme Court Rule 10"
    ),
    DoctrineBlock(
        topic="En Banc Reconsideration",
        keywords=["en banc", "mini en banc", "panel decision", "intra-circuit conflict", "overrule panel"],
        conclusion_template="En banc review allows full circuit to reconsider panel decisions. Granted for exceptionally important questions or to maintain circuit uniformity. Panel decisions binding until overruled en banc.",
        reasoning_framework="""Federal Rule of Appellate Procedure 35: en banc for (1) conflict with circuit precedent, or (2) exceptional importance. Standards strict - most petitions denied. Three-judge panel cannot overrule prior panel; only en banc can. Ninth Circuit uses limited en banc (11 judges). En banc decisions have greater precedential weight than panel. Signals circuit-wide commitment to rule. Party must petition within 45 days of judgment.""",
        key_factors=["intra-circuit conflict", "exceptional importance", "uniformity need", "petition timeliness", "en banc size"],
        primary_authority=["FRAP 35", "Miller v Gammie 335 F3d 889 (9th Cir en banc)"],
        burden_holder="Party petitioning for en banc must show conflict or exceptional importance",
        adversary_position="Panel decision correct, en banc unnecessary",
        counter_arguments=["No real conflict", "Issue not exceptionally important", "Panel decision correct"],
        resolution_strategy="Identify intra-circuit conflict or exceptional question. File petition within 45 days. Argue uniformity need.",
        entity_scope="Federal circuit courts",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="FRAP 35"
    ),
    DoctrineBlock(
        topic="Supreme Court Certiorari Factors",
        keywords=["certiorari", "cert petition", "Rule 10", "circuit split", "important question"],
        conclusion_template="Supreme Court grants certiorari when: (1) circuit split, (2) state court conflicts with SCOTUS/other state courts, (3) important federal question, (4) lower court departed from accepted judicial practice. Discretionary - grants under 1% of petitions.",
        reasoning_framework="""Rule 10 lists factors but cert is discretionary. Circuit split strongest factor. Important question without split occasionally granted (e.g., major constitutional issue). State court conflicts with SCOTUS decisions. Lower court defied SCOTUS precedent. Practical importance matters - affects many parties, recurring issue. Poor vehicle denied despite split - factual problems, jurisdictional defects, alternative holdings. Rule of four - 4 justices must vote to grant. Timing - petition within 90 days of judgment.""",
        key_factors=["circuit split", "important federal question", "state court conflict", "defiance of SCOTUS precedent", "vehicle quality"],
        primary_authority=["Supreme Court Rule 10", "Supreme Court Rule 13"],
        burden_holder="Petitioner must show cert-worthy issue",
        adversary_position="Issue not cert-worthy, vehicle flawed",
        counter_arguments=["No real split", "Issue unimportant", "Factual problems", "Alternative holding", "Percolation needed"],
        resolution_strategy="Identify Rule 10 factor. Show practical importance. Ensure clean vehicle. File within 90 days.",
        entity_scope="All courts - appeals to Supreme Court",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Supreme Court Rule 10"
    ),
    DoctrineBlock(
        topic="Overruling Signals",
        keywords=["overruling", "abrogation", "departure from precedent", "special justification", "changed circumstances"],
        conclusion_template="Courts signal potential overruling through: questioning precedent reasoning, noting criticism, changed-circumstance discussion, limiting holdings, inviting reconsideration. Actual overruling requires majority opinion explicitly abandoning prior rule.",
        reasoning_framework="""Overruling signals: (1) dicta questioning precedent, (2) limiting to facts, (3) noting circuit splits or criticism, (4) concurrences urging reconsideration, (5) changed legal landscape discussion. Not overruling: distinguishing, narrowing, harmonizing. True overruling requires majority holding abandoning prior rule. Prospective vs retroactive application. Good-faith reliance protected. Age of precedent cuts both ways - ancient precedent may be embedded or outdated.""",
        key_factors=["explicit vs implicit signals", "dicta vs holding", "majority vs concurrence", "reliance interests", "changed circumstances"],
        primary_authority=["Payne v Tennessee 501 US 808", "Janus v AFSCME 138 S Ct 2448"],
        burden_holder="Party seeking overruling",
        adversary_position="Precedent correct, no special justification",
        counter_arguments=["Precedent unworkable", "Badly reasoned", "Circumstances changed", "Minimal reliance"],
        resolution_strategy="Identify clear signals. Distinguish narrowing from overruling. Show special justification.",
        entity_scope="All courts",
        confidence="HIGH",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="Janus v AFSCME 2018"
    ),
    DoctrineBlock(
        topic="Distinguishing Methodology",
        keywords=["distinguish precedent", "factual distinction", "material difference", "analogical reasoning", "precedent scope"],
        conclusion_template="Distinguishing precedent requires showing material factual or legal difference that makes precedent inapplicable. Not mere difference but difference that matters to the rule's rationale.",
        reasoning_framework="""Effective distinguishing: (1) identify precedent's holding and ratio decidendi, (2) isolate material facts, (3) show current case differs on those facts, (4) explain why difference matters to rule's purpose. Weak distinguishing: immaterial factual variations, policy disagreement framed as distinction. Analogical reasoning - cases similar on material facts follow same rule; cases different on material facts may diverge. Precedent's scope determined by its reasoning not facts alone.""",
        key_factors=["material vs immaterial facts", "ratio decidendi", "rule's purpose", "analogical reasoning", "precedent scope"],
        primary_authority=["Allegheny County v ACLU 492 US 573 (Kennedy concurrence on distinguishing)", "Roe v Wade 410 US 113"],
        burden_holder="Party distinguishing precedent must show material difference",
        adversary_position="Cases analogous on material facts",
        counter_arguments=["Factual differences immaterial", "Precedent's reasoning applies equally", "Attempted distinction is policy disagreement"],
        resolution_strategy="Identify precedent's core holding. Isolate material facts. Show meaningful difference tied to rule's rationale.",
        entity_scope="All courts",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Common law methodology"
    ),
    DoctrineBlock(
        topic="Case Treatment Taxonomy",
        keywords=["followed", "distinguished", "overruled", "questioned", "criticized", "limited"],
        conclusion_template="Case treatment categories: Positive (followed, affirmed, applied), Negative (overruled, abrogated, reversed), Cautionary (questioned, criticized, limited, distinguished). Treatment affects precedential weight.",
        reasoning_framework="""Positive treatment: followed - applied to similar facts; affirmed - upheld on appeal; cited with approval. Negative treatment: overruled - holding abandoned; reversed - judgment overturned; abrogated by statute. Cautionary: questioned - reasoning doubted; criticized - unfavorably analyzed; limited - confined to facts; distinguished - held inapplicable. Subsequent treatment tracked via Shepard's/KeyCite. Multiple treatments possible - case followed in some contexts, distinguished in others. Red flag = negative treatment. Yellow flag = cautionary.""",
        key_factors=["positive vs negative vs cautionary", "treatment strength", "frequency of citation", "treatment consistency", "temporal pattern"],
        primary_authority=["Shepard's Citations methodology", "KeyCite treatment flags"],
        burden_holder="Researcher must verify current precedential status",
        adversary_position="Case still good law despite treatment",
        counter_arguments=["Treatment limited to different issue", "Criticism in dicta", "Questioned but not overruled"],
        resolution_strategy="Use citator services. Identify all negative/cautionary treatments. Assess impact on precedential weight.",
        entity_scope="All courts",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legal research methodology"
    ),
    DoctrineBlock(
        topic="Authority Weight Scoring",
        keywords=["precedential weight", "authority strength", "citation influence", "landmark case", "weight factors"],
        conclusion_template="Authority weight depends on: court level, reasoning quality, age, subsequent treatment, citation frequency, subject matter importance, factual similarity. Supreme Court unanimous decisions carry greatest weight.",
        reasoning_framework="""Weight factors: (1) Court hierarchy - SCOTUS > Circuit > District; state supreme > appellate > trial. (2) Reasoning quality - thorough analysis, policy consideration, doctrinal coherence. (3) Age - recent cases reflect current law but landmarks endure. (4) Treatment - frequently followed vs frequently distinguished. (5) Citation influence - high-citation cases shape doctrine. (6) Opinion type - majority > plurality > concurrence > dissent. (7) Unanimity - 9-0 > 5-4. (8) Factual similarity - on-point facts vs analogous. (9) Subject importance - constitutional > statutory > common law.""",
        key_factors=["court level", "reasoning quality", "citation frequency", "subsequent treatment", "factual similarity"],
        primary_authority=["Academic citation analysis", "Judicial opinion writing guides"],
        burden_holder="Researcher must assess weight, not just cite",
        adversary_position="Cited case lacks sufficient weight",
        counter_arguments=["Low court level", "Poor reasoning", "Frequently distinguished", "Factually dissimilar"],
        resolution_strategy="Apply multi-factor scoring. Consider hierarchical and qualitative factors. Compare weight of competing authorities.",
        entity_scope="Legal research methodology",
        confidence="MEDIUM",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="Research best practices"
    ),
    DoctrineBlock(
        topic="Recency vs Landmark Weight",
        keywords=["recent precedent", "landmark case", "temporal weight", "doctrinal evolution", "foundational precedent"],
        conclusion_template="Recent cases reflect current legal landscape; landmark cases establish foundational principles. Both carry weight. Recency matters for evolving areas; landmarks control settled doctrine. Conflict resolved by hierarchy and reasoning quality.",
        reasoning_framework="""Temporal dynamics: Recent cases (under 5 years) show current court thinking, reflect latest statutory amendments, incorporate new facts/technology. Landmark cases (Brown, Roe/Dobbs, Chevron/Loper Bright) establish frameworks lasting decades. Recency favored when: law rapidly evolving, statutory interpretation, technology-driven issues. Landmarks favored when: constitutional fundamentals, settled doctrine, framework tests. Middle-ground: recent case applies landmark framework to new facts. Overruling breaks landmark status. Citation frequency correlates with landmark status.""",
        key_factors=["recency advantage", "landmark status", "doctrinal stability", "evolutionary speed", "citation influence"],
        primary_authority=["Brown v Board 347 US 483 (landmark)", "Dobbs v Jackson 142 S Ct 2228 (overruling landmark)"],
        burden_holder="Researcher must balance temporal factors",
        adversary_position="Recent case controls vs landmark controls",
        counter_arguments=["Landmark outdated", "Recent case wrongly decided", "Intervening change in law"],
        resolution_strategy="Assess area's evolutionary speed. Identify landmarks. Check for recent shifts. Balance recency and foundational weight.",
        entity_scope="All legal research",
        confidence="MEDIUM",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="Research methodology"
    ),
    DoctrineBlock(
        topic="Vertical Stare Decisis Absolute",
        keywords=["vertical stare decisis", "hierarchical binding", "mandatory precedent", "supreme court binding", "appellate binding"],
        conclusion_template="Vertical stare decisis is absolute - lower courts MUST follow higher courts in same jurisdiction. No exception for disagreement. Only distinguishing facts or en banc/higher court overruling allows departure.",
        reasoning_framework="""Hierarchical structure creates mandatory precedent. Federal: SCOTUS binds all courts. Circuit binds districts within circuit. State: Supreme court binds all lower state courts. Lower court cannot refuse to follow based on disagreement with reasoning. Options if lower court believes precedent wrong: (1) follow but signal disagreement, (2) distinguish on facts, (3) certify question to higher court. Prediction rule - if clearly established SCOTUS precedent, lower courts predict SCOTUS would rule same way. Intercircuit - district courts follow own circuit even if disagree with other circuits.""",
        key_factors=["hierarchical binding", "no disagreement exception", "distinguishing permitted", "certification option", "own-circuit rule"],
        primary_authority=["Hutto v Davis 454 US 370", "Agostini v Felton 521 US 203"],
        burden_holder="Lower court must follow unless can distinguish",
        adversary_position="Precedent wrongly decided, should not follow",
        counter_arguments=["Case factually distinguishable", "Precedent implicitly overruled by later case", "Intervening change in law"],
        resolution_strategy="Apply vertical stare decisis strictly. Distinguish on facts if possible. Signal disagreement in dicta. Certify question if appropriate.",
        entity_scope="All courts in hierarchical system",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Hutto v Davis 1981"
    ),
    DoctrineBlock(
        topic="Horizontal Stare Decisis Flexibility",
        keywords=["horizontal stare decisis", "panel precedent", "overrule own precedent", "coordinate court", "same-level binding"],
        conclusion_template="Horizontal stare decisis - court following own prior decisions - is strong but not absolute. Supreme Court may overrule itself with special justification. Circuit panels bound by prior panels absent en banc overruling.",
        reasoning_framework="""Same-level courts generally follow own precedent but may overrule. Supreme Court standard: precedent unworkable, badly reasoned, changed circumstances, reliance minimal (Payne factors). Circuit panels strictly bound by prior panels - only en banc can overrule. State supreme courts vary - some require special justification, others more flexible. Horizontal stare decisis weaker than vertical but still substantial. Overruling triggers: doctrinal inconsistency, unworkability, intervening legal change, original error, minimal reliance. Dissents signal potential future overruling.""",
        key_factors=["special justification standard", "panel vs en banc", "overruling triggers", "reliance interests", "doctrinal consistency"],
        primary_authority=["Payne v Tennessee 501 US 808", "Planned Parenthood v Casey 505 US 833"],
        burden_holder="Party seeking overruling must show special justification",
        adversary_position="Precedent settled, stare decisis controls",
        counter_arguments=["Precedent unworkable", "Badly reasoned", "Changed circumstances", "Minimal reliance"],
        resolution_strategy="Apply Payne factors for SCOTUS. Petition en banc for circuit. Show special justification if state court.",
        entity_scope="Courts overruling own precedent",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Payne v Tennessee 1991"
    ),
    DoctrineBlock(
        topic="Persuasive Authority Weight Factors",
        keywords=["persuasive precedent", "non-binding authority", "sister circuit", "coordinate jurisdiction", "persuasive weight"],
        conclusion_template="Persuasive authority (sister circuits, state courts, foreign jurisdictions) carries weight based on: reasoning quality, court prestige, factual similarity, jurisdictional consensus, recency. Not binding but may influence.",
        reasoning_framework="""Persuasive weight factors: (1) Reasoning quality - thorough, policy-aware, doctrinally sound. (2) Court prestige - Second/DC Circuits high prestige in certain areas. (3) Factual similarity - closer facts = stronger persuasion. (4) Consensus - 10 circuits agree vs 1 outlier. (5) Recency - reflects current thinking. (6) Subject expertise - Delaware chancery on corporate law. (7) Judge reputation - influential jurist. Courts frequently cite persuasive authority when binding precedent absent. State courts cite sister states. Federal courts cite state courts on state law. Foreign law persuasive in constitutional/human rights cases.""",
        key_factors=["reasoning quality", "court prestige", "jurisdictional consensus", "factual similarity", "judge reputation"],
        primary_authority=["Roper v Simmons 543 US 551 (citing foreign law)", "Spectrum Brands v Benitec 783 F3d 1336"],
        burden_holder="Party citing persuasive authority must show persuasive strength",
        adversary_position="Persuasive authority distinguishable or unpersuasive",
        counter_arguments=["Poorly reasoned", "Factually dissimilar", "Outlier jurisdiction", "Overruled in source jurisdiction"],
        resolution_strategy="Cite high-quality persuasive authority. Show consensus if available. Highlight reasoning strength.",
        entity_scope="All courts considering persuasive precedent",
        confidence="MEDIUM",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="Research best practices"
    ),
    DoctrineBlock(
        topic="Shepardizing and Citator Services",
        keywords=["shepardize", "keycite", "citator", "treatment verification", "good law check"],
        conclusion_template="Shepardizing (or KeyCiting) verifies case remains good law by tracking subsequent treatment. Red flag = negative treatment; yellow flag = cautionary. Mandatory step before citing precedent.",
        reasoning_framework="""Citator services track: (1) Direct history - appeals, remands, affirmances. (2) Negative treatment - overruled, reversed, abrogated. (3) Cautionary treatment - questioned, criticized, limited, distinguished. (4) Positive treatment - followed, affirmed, cited with approval. (5) Secondary sources - law review, treatise citations. Shepard's signals: Red stop sign = strong negative. Orange Q = questioned. Yellow triangle = caution. Green plus = positive. No signal = cited. KeyCite uses flags similarly. Treatment analysis requires reading citing cases, not just flags.""",
        key_factors=["treatment flags", "direct history", "negative treatment", "cautionary treatment", "citation depth"],
        primary_authority=["Shepard's Citations methodology", "KeyCite user guides"],
        burden_holder="Researcher must verify precedent validity",
        adversary_position="Case no longer good law",
        counter_arguments=["Negative treatment limited to different issue", "Overruling case itself overruled", "Treatment in dicta only"],
        resolution_strategy="Shepardize all cases before citing. Review negative/cautionary treatments. Update research if precedent undermined.",
        entity_scope="All legal research",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legal research standards"
    ),
    DoctrineBlock(
        topic="Analogical Reasoning Framework",
        keywords=["analogical reasoning", "case analogy", "material similarity", "legal reasoning", "precedent application"],
        conclusion_template="Analogical reasoning applies precedent by comparing material facts and legal issues. Cases materially similar on facts relevant to legal rule follow same outcome. Differences on immaterial facts do not distinguish.",
        reasoning_framework="""Analogical process: (1) Identify precedent rule and ratio decidendi. (2) Determine material facts - facts that matter to rule's application. (3) Compare current case facts to precedent facts. (4) If materially similar, apply precedent rule. (5) If materially different, distinguish or apply different rule. Material facts are those relevant to rule's purpose/policy. Immaterial facts (procedural posture, party names, non-legal details) do not distinguish. Strong analogy: identical legal issue, similar key facts, same policy considerations. Weak analogy: different facts, policy cut differently.""",
        key_factors=["material fact identification", "ratio decidendi", "rule purpose", "factual similarity", "policy alignment"],
        primary_authority=["Eisenstadt v Baird 405 US 438", "Griswold v Connecticut 381 US 479"],
        burden_holder="Party asserting analogy must show material similarity",
        adversary_position="Cases materially different, analogy fails",
        counter_arguments=["Key factual differences", "Different policy considerations", "Precedent's rule inapplicable"],
        resolution_strategy="Identify material facts. Compare systematically. Assess policy alignment. Apply or distinguish based on similarity.",
        entity_scope="All common law reasoning",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Common law methodology"
    ),
    DoctrineBlock(
        topic="Plurality Opinion Precedential Effect",
        keywords=["plurality opinion", "marks rule", "narrowest grounds", "fragmented court", "controlling opinion"],
        conclusion_template="Plurality opinions (no majority for reasoning) have limited precedential effect. Marks rule: holding on narrowest grounds controls. If no narrowest grounds identifiable, precedential value unclear.",
        reasoning_framework="""Plurality occurs when no majority agrees on rationale. Marks v United States rule: 'narrowest grounds' controls when plurality + concurrence reach same result via different reasoning. Narrowest grounds = reasoning that all in majority would agree with. Often difficult to identify. If no clear narrowest grounds, lower courts struggle. Some circuits treat plurality as persuasive only. Supreme Court pluralities particularly problematic - circuit splits on interpretation common. Concurring opinions may provide guidance but not binding. Dissents irrelevant to holding but may signal future direction.""",
        key_factors=["Marks rule application", "narrowest grounds identification", "majority fragmentation", "concurrence role", "precedential uncertainty"],
        primary_authority=["Marks v United States 430 US 188", "Rapanos v United States 547 US 715 (plurality)"],
        burden_holder="Party relying on plurality must identify narrowest grounds",
        adversary_position="No controlling opinion, precedent unclear",
        counter_arguments=["No identifiable narrowest grounds", "Concurrence broader", "Plurality reasoning flawed"],
        resolution_strategy="Apply Marks rule. Identify overlap between plurality and concurrence. If uncertain, argue persuasive value only.",
        entity_scope="Courts interpreting fragmented decisions",
        confidence="MEDIUM",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="Marks v United States 1977"
    ),
    DoctrineBlock(
        topic="Concurring and Dissenting Opinion Value",
        keywords=["concurrence", "dissent", "dicta", "non-binding opinion", "future direction signal"],
        conclusion_template="Concurrences and dissents are not binding but carry persuasive weight. Concurrences may clarify majority or signal narrower reading. Dissents may become law if later adopted by majority.",
        reasoning_framework="""Concurring opinions: agree with result but offer different reasoning or limiting principle. May signal narrower reading of majority. Relevant for Marks narrowest-grounds analysis. Persuasive but not binding. Dissents: disagree with majority. Not precedential. Value: (1) identify weaknesses in majority reasoning, (2) signal potential future overruling, (3) persuade other courts or legislatures, (4) historic vindication if later adopted. Famous dissents later became law (e.g., Plessy dissent vindicated by Brown). Separate opinions by influential jurists carry extra weight.""",
        key_factors=["concurrence limiting function", "dissent critique value", "future adoption potential", "jurist reputation", "persuasive reasoning"],
        primary_authority=["Plessy v Ferguson 163 US 537 (Harlan dissent)", "Brown v Board 347 US 483 (vindicating Harlan)"],
        burden_holder="Party citing concurrence/dissent must show persuasive value",
        adversary_position="Not binding, no precedential effect",
        counter_arguments=["Persuasive reasoning", "Signals future direction", "Adopted by other courts", "Influential jurist"],
        resolution_strategy="Cite concurrences for limiting principles. Cite dissents to attack majority or predict change. Note non-binding status.",
        entity_scope="All courts",
        confidence="MEDIUM",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="Opinion-type hierarchy"
    ),
    DoctrineBlock(
        topic="Per Curiam Opinion Precedential Weight",
        keywords=["per curiam", "unsigned opinion", "summary reversal", "precedential effect", "unanimous court"],
        conclusion_template="Per curiam opinions (unsigned, issued by court as whole) carry full precedential weight if reasoned. Summary per curiams (reversals without full briefing) have limited precedential scope.",
        reasoning_framework="""Per curiam types: (1) Reasoned per curiam - full analysis, unanimous or near-unanimous, precedentially equivalent to signed opinion. (2) Summary per curiam - brief reversal, often citing clear error or circuit defiance, narrow precedential scope. (3) Memorandum decisions - no published reasoning, minimal precedential value. Supreme Court summary reversals signal lower court clearly wrong but don't establish broad rule. Circuit per curiams vary - some circuits use for routine cases, others reserve for special situations. Unsigned suggests consensus but doesn't reduce binding force if reasoned.""",
        key_factors=["reasoned vs summary", "precedential scope", "court consensus", "publication status", "reasoning depth"],
        primary_authority=["Mandel v Bradley 432 US 173 (per curiam)", "FRAP 32.1 on unpublished opinions"],
        burden_holder="Party relying on per curiam must assess scope",
        adversary_position="Per curiam has limited precedential value",
        counter_arguments=["Summary reversal only", "Fact-specific", "No broad rule established"],
        resolution_strategy="Distinguish reasoned from summary per curiams. Assess reasoning depth. Apply precedential weight accordingly.",
        entity_scope="All courts",
        confidence="MEDIUM",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="FRAP 32.1, court rules"
    ),
    DoctrineBlock(
        topic="Unpublished Opinion Citation",
        keywords=["unpublished opinion", "non-precedential", "FRAP 32.1", "unreported decision", "citation rules"],
        conclusion_template="Federal Rule of Appellate Procedure 32.1 allows citation of unpublished opinions issued after January 1, 2007, but they lack precedential weight. Courts may consider reasoning but not bound.",
        reasoning_framework="""Pre-FRAP 32.1, many circuits barred citing unpublished opinions. Rule 32.1 (2006) permits citation but doesn't create precedential status. Unpublished opinions typically: (1) routine application of settled law, (2) fact-specific, (3) minimal reasoning, (4) marked non-precedential. Persuasive value low. Trial courts may cite for reasoning but appellate courts not bound. State courts vary - some allow citation, others prohibit. Strategic use: cite unpublished when no published precedent available, for factual analogy, or to show court's consistency.""",
        key_factors=["FRAP 32.1 date threshold", "non-precedential status", "citation permission", "persuasive weight", "court practice"],
        primary_authority=["FRAP 32.1", "Anastasoff v United States 223 F3d 898 (vacated)"],
        burden_holder="Party citing unpublished must note non-precedential status",
        adversary_position="Unpublished opinion lacks weight",
        counter_arguments=["Shows court's reasoning approach", "Factual analogy", "No published precedent available"],
        resolution_strategy="Cite unpublished opinions sparingly. Note non-precedential status. Use for reasoning guidance not binding authority.",
        entity_scope="Federal courts post-2007",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="FRAP 32.1"
    ),
    DoctrineBlock(
        topic="Interlocutory vs Final Judgment Precedent",
        keywords=["interlocutory appeal", "final judgment", "precedential effect", "pretrial ruling", "partial summary judgment"],
        conclusion_template="Precedential effect depends on finality. Final judgments reviewed on appeal create binding precedent. Interlocutory rulings may be revisited and have limited precedential scope.",
        reasoning_framework="""Final judgment rule: appellate jurisdiction generally requires final decision. Interlocutory appeals exceptional (certified questions, injunctions, collateral orders). Precedential impact: Final judgment precedent is full binding precedent. Interlocutory ruling precedent is tentative - trial court may reconsider, later appeals may reach different conclusion. Partial summary judgment rulings not final until whole case resolved. Mandamus review of discovery orders has limited precedential scope. Class certification appeals under Rule 23(f) precedential on certification law.""",
        key_factors=["finality requirement", "interlocutory exception", "precedential scope", "revisability", "judgment type"],
        primary_authority=["28 USC 1291 final judgment rule", "28 USC 1292 interlocutory appeal exceptions"],
        burden_holder="Party citing interlocutory precedent must note limited scope",
        adversary_position="Interlocutory ruling not binding precedent",
        counter_arguments=["Ruling tentative", "Subject to revision", "Not final judgment"],
        resolution_strategy="Distinguish final from interlocutory rulings. Apply full precedential weight to final judgments. Treat interlocutory precedent as persuasive.",
        entity_scope="Federal courts, final judgment rule jurisdictions",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="28 USC 1291-1292"
    ),
    DoctrineBlock(
        topic="Dictum vs Holding Distinction",
        keywords=["obiter dictum", "holding", "ratio decidendi", "precedential force", "dicta"],
        conclusion_template="Holdings are binding; dicta are not. Holding is rule necessary to decision. Dictum is commentary unnecessary to outcome. Only holdings create precedent.",
        reasoning_framework="""Holding: legal rule necessary to judgment on facts presented. Ratio decidendi. Binding under stare decisis. Dictum (obiter dictum): statement unnecessary to decision, hypothetical, alternative ground, policy discussion. Not binding but persuasive. Identifying holding: apply but-for test - if statement removed, would outcome change? If yes, holding. If no, dictum. Broad vs narrow holdings - courts may characterize precedent's holding narrowly to limit scope. Alternative holdings (multiple independent grounds) both binding per some courts, primary ground only per others.""",
        key_factors=["necessity to decision", "but-for test", "alternative holdings", "broad vs narrow holding", "binding force"],
        primary_authority=["Cohens v Virginia 19 US 264", "Central Green Co v United States 531 US 425"],
        burden_holder="Party relying on language must show it is holding not dictum",
        adversary_position="Statement is dictum, not binding",
        counter_arguments=["Unnecessary to decision", "Hypothetical", "Alternative ground", "Policy discussion"],
        resolution_strategy="Apply but-for test. Identify necessary legal rule. Distinguish holding from dictum. Argue dictum if weakens opposing precedent.",
        entity_scope="All courts",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Common law methodology"
    ),
    DoctrineBlock(
        topic="State Court Precedent in Federal Court",
        keywords=["Erie doctrine", "state law issues", "certified questions", "diversity jurisdiction", "federal-state precedent"],
        conclusion_template="Under Erie, federal courts apply state substantive law in diversity cases. State supreme court precedent on state law is binding. Absence of state supreme court precedent, federal court predicts how state high court would rule.",
        reasoning_framework="""Erie v Tompkins: federal courts apply state substantive law in diversity cases. State supreme court decisions on state law binding on federal courts. Lower state court decisions persuasive, not binding. If no state supreme court precedent: federal court predicts how state high court would decide, considering lower state court decisions, trends, sister state precedent, policy. Certified questions: federal court may certify unsettled state law question to state supreme court. Reverse-Erie: state courts not bound by federal court interpretations of state law. Federal question cases: federal law controls, state precedent irrelevant unless incorporated.""",
        key_factors=["Erie doctrine", "diversity jurisdiction", "state law prediction", "certified questions", "binding vs persuasive"],
        primary_authority=["Erie RR v Tompkins 304 US 64", "Salve Regina College v Russell 499 US 225"],
        burden_holder="Federal court must apply state law correctly",
        adversary_position="State precedent controls vs federal court may choose rule",
        counter_arguments=["State supreme court has spoken", "No clear state precedent", "Certification appropriate"],
        resolution_strategy="Identify state supreme court precedent. If absent, predict based on lower courts and trends. Certify if unsettled important question.",
        entity_scope="Federal courts in diversity cases",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Erie RR v Tompkins 1938"
    ),
    DoctrineBlock(
        topic="Superseded by Statute Doctrine",
        keywords=["statutory override", "abrogation by statute", "common law superseded", "legislative reversal", "codification"],
        conclusion_template="Court precedent superseded if legislature enacts statute changing legal rule. Statutory abrogation makes precedent no longer good law on that issue. Precedent retained for pre-statute conduct or unaffected issues.",
        reasoning_framework="""Legislative supremacy: Congress or state legislature may override common law or constitutional interpretation (non-constitutional only). Abrogation types: (1) Explicit reversal - statute states it overrules case. (2) Implicit reversal - statute adopts different rule. (3) Codification - statute adopts case law rule, freezing it. Precedent superseded for post-statute conduct; may remain good law for pre-statute. Citator services flag statutory abrogation. Constitutional holdings not subject to statutory override (requires amendment). Statutory interpretation holdings may be overridden. Examples: Lilly Ledbetter Act overruling Ledbetter v Goodyear.""",
        key_factors=["legislative override", "explicit vs implicit", "temporal scope", "constitutional vs statutory", "codification effect"],
        primary_authority=["Lilly Ledbetter Fair Pay Act (overruling Ledbetter v Goodyear)", "Civil Rights Act 1991 (overruling multiple cases)"],
        burden_holder="Party citing precedent must check for statutory override",
        adversary_position="Precedent superseded by statute",
        counter_arguments=["Statute doesn't address same issue", "Precedent still good for pre-statute conduct", "Constitutional holding immune"],
        resolution_strategy="Check citator for statutory abrogation. Review legislative history. Assess temporal scope. Distinguish constitutional holdings.",
        entity_scope="All courts",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legislative supremacy doctrine"
    ),
    DoctrineBlock(
        topic="Landmark Case Identification Criteria",
        keywords=["landmark case", "seminal decision", "foundational precedent", "doctrinal shift", "high citation"],
        conclusion_template="Landmark cases: establish new doctrine, overrule major precedent, resolve constitutional question, create framework test, highly cited, shape generations of law. Examples: Brown, Miranda, Chevron/Loper Bright, Roe/Dobbs.",
        reasoning_framework="""Landmark criteria: (1) Doctrinal innovation - creates new legal framework. (2) Constitutional significance - resolves fundamental right or structure question. (3) Overruling importance - reverses major precedent. (4) Citation influence - cited thousands of times. (5) Framework establishment - test/standard widely applied. (6) Social impact - affects millions, cultural significance. (7) Longevity - shapes law for decades. (8) Unanimous/near-unanimous - reflects consensus. Non-landmarks: incremental clarifications, fact-specific applications, quickly superseded, low citation.""",
        key_factors=["doctrinal innovation", "citation influence", "framework creation", "longevity", "social impact"],
        primary_authority=["Brown v Board 347 US 483", "Miranda v Arizona 384 US 436", "Chevron v NRDC 467 US 837"],
        burden_holder="Researcher identifies landmarks for framework understanding",
        adversary_position="Case not truly landmark, merely important",
        counter_arguments=["Limited doctrinal innovation", "Low citation", "Quickly superseded", "Narrow holding"],
        resolution_strategy="Assess citation influence, doctrinal impact, longevity, framework creation. Identify cases shaping field.",
        entity_scope="All legal areas",
        confidence="MEDIUM",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="Legal historiography"
    ),
    DoctrineBlock(
        topic="Trend Analysis Across Jurisdictions",
        keywords=["jurisdictional trend", "majority rule", "minority rule", "emerging consensus", "doctrinal shift"],
        conclusion_template="Trend analysis identifies majority/minority rules, emerging consensus, doctrinal shifts. Majority rule persuasive in undecided jurisdictions. Trend toward new rule signals future adoption.",
        reasoning_framework="""Trend identification: (1) Count jurisdictions adopting each rule. (2) Identify temporal pattern - old rule vs new rule. (3) Assess reasoning quality - which approach better reasoned. (4) Note influential jurisdictions - ALI Restatements, leading states. (5) Track recent adoptions - momentum toward new rule. Majority rule: most jurisdictions follow, strong persuasive weight. Minority rule: fewer jurisdictions, may be better reasoned. Emerging consensus: recent trend toward uniform rule. Doctrinal shift: movement from old to new approach. Courts cite trends when adopting new rule.""",
        key_factors=["majority vs minority rule", "temporal trend", "reasoning quality", "influential jurisdiction adoption", "momentum"],
        primary_authority=["Restatement (Third) Torts", "Uniform Commercial Code"],
        burden_holder="Party advocating rule must show jurisdictional support",
        adversary_position="Majority rule vs minority but better rule",
        counter_arguments=["Minority rule better reasoned", "Majority trend reversing", "Jurisdiction-specific factors"],
        resolution_strategy="Count jurisdictions. Identify trend direction. Assess reasoning. Argue majority or emerging consensus.",
        entity_scope="Multi-jurisdiction analysis",
        confidence="MEDIUM",
        confidence_stratification="AGGRESSIVE",
        controlling_precedent="Comparative jurisdiction methodology"
    ),
    DoctrineBlock(
        topic="Negative Precedent Treatment Analysis",
        keywords=["overruled", "reversed", "vacated", "abrogated", "superseded"],
        conclusion_template="Negative treatment destroys or weakens precedential value. Overruled = no longer good law. Reversed = judgment overturned. Vacated = set aside. Abrogated = superseded by statute. Superseded = replaced by later rule.",
        reasoning_framework="""Negative treatment hierarchy: (1) Overruled - holding explicitly abandoned, no precedential value. (2) Abrogated by statute - legislature reversed, statute controls. (3) Superseded by rule - later court adopted different rule. (4) Reversed - appellate court overturned judgment. (5) Vacated - judgment set aside, no preclusive effect. Scope of negative treatment: entire case vs specific holding. Temporal scope: prospective vs retroactive. Partial overruling: some holdings survive. Citator red flags indicate negative treatment. Must read citing case to assess scope.""",
        key_factors=["treatment type", "scope of overruling", "temporal effect", "partial vs complete", "citator flags"],
        primary_authority=["Shepard's/KeyCite treatment categories"],
        burden_holder="Researcher must identify negative treatment before citing",
        adversary_position="Precedent no longer good law",
        counter_arguments=["Negative treatment limited to different issue", "Overruling case itself overruled", "Partial overruling, some holdings survive"],
        resolution_strategy="Shepardize thoroughly. Identify all negative treatment. Read citing cases. Assess scope and temporal effect.",
        entity_scope="All legal research",
        confidence="HIGH",
        confidence_stratification="DEFENSIBLE",
        controlling_precedent="Legal research standards"
    )
]

# === ENGINE STATE ===
class EngineState:
    def __init__(self):
        self.start_time = time.time()
        self.total_queries = 0
        self.total_latency = 0.0
        self.errors = 0
        self.triggered_doctrines_history: List[str] = []
        self.drift_events: List[Dict] = []
        self.coverage_map: Dict[str, int] = {d.topic: 0 for d in DOCTRINE_CACHE}

STATE = EngineState()

# === TELEMETRY ===
def record_query(latency_ms: float, triggered: List[str], error: bool = False):
    STATE.total_queries += 1
    STATE.total_latency += latency_ms
    if error:
        STATE.errors += 1
    STATE.triggered_doctrines_history.extend(triggered)
    for doctrine in triggered:
        if doctrine in STATE.coverage_map:
            STATE.coverage_map[doctrine] += 1

def get_metrics() -> Dict[str, Any]:
    avg_latency = STATE.total_latency / STATE.total_queries if STATE.total_queries > 0 else 0.0
    error_rate = STATE.errors / STATE.total_queries if STATE.total_queries > 0 else 0.0
    return {
        "total_queries": STATE.total_queries,
        "avg_latency_ms": round(avg_latency, 2),
        "error_rate": round(error_rate, 4),
        "uptime_seconds": round(time.time() - STATE.start_time, 2)
    }

# === CORE FUNCTIONS ===
def doctrine_cache_lookup(query: str) -> List[DoctrineBlock]:
    query_lower = query.lower()
    matched = []
    for doctrine in DOCTRINE_CACHE:
        if any(kw in query_lower for kw in doctrine.keywords):
            matched.append(doctrine)
    return matched

def three_layer_response(query: str, mode: str) -> tuple[str, List[str], str]:
    matched = doctrine_cache_lookup(query)
    triggered = [d.topic for d in matched]

    if matched:
        if mode == "FAST":
            response = matched[0].conclusion_template
            confidence = matched[0].confidence
        elif mode == "DEFENSE":
            response = f"{matched[0].conclusion_template}\n\nReasoning: {matched[0].reasoning_framework}\n\nAuthority: {', '.join(matched[0].primary_authority)}"
            confidence = matched[0].confidence_stratification
        else:
            response = f"MEMORANDUM ANALYSIS\n\nIssue: {query}\n\nConclusion: {matched[0].conclusion_template}\n\nReasoning Framework: {matched[0].reasoning_framework}\n\nKey Factors: {', '.join(matched[0].key_factors)}\n\nPrimary Authority: {', '.join(matched[0].primary_authority)}\n\nAdversary Position: {matched[0].adversary_position}\n\nCounter-Arguments: {', '.join(matched[0].counter_arguments)}\n\nResolution Strategy: {matched[0].resolution_strategy}\n\nControlling Precedent: {matched[0].controlling_precedent}"
            confidence = matched[0].confidence_stratification
    else:
        response = "No cached doctrine matched. Semantic retrieval layer would engage (not implemented in this build). Deep analysis: Precedent mapping requires citation network data, case treatment tracking, and authority hierarchy scoring. This engine provides framework for such analysis but full implementation requires integration with legal databases (Westlaw, Lexis, CourtListener) for live citation data."
        confidence = "LOW"

    return response, triggered, confidence

def generate_determinism_hash(query: str, response: str) -> str:
    combined = f"{query}|{response}|{VERSION}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]

def authority_chain_builder(triggered: List[str]) -> List[str]:
    chain = []
    for topic in triggered:
        for doctrine in DOCTRINE_CACHE:
            if doctrine.topic == topic:
                chain.extend(doctrine.primary_authority[:2])
                break
    return chain[:5]

# === FASTAPI APP ===
app = FastAPI(title=f"{ENGINE_NAME} v{VERSION}", version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health", response_model=HealthResponse)
def health_check():
    metrics = get_metrics()
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=metrics["uptime_seconds"],
        total_queries=metrics["total_queries"],
        avg_latency_ms=metrics["avg_latency_ms"],
        error_rate=metrics["error_rate"]
    )

@app.post("/query", response_model=QueryResponse)
def query_endpoint(req: QueryRequest):
    start = time.time()
    query_id = str(uuid4())

    try:
        response, triggered, confidence = three_layer_response(req.query, req.mode)
        authority_chain = authority_chain_builder(triggered)
        determinism_hash = generate_determinism_hash(req.query, response)

        latency_ms = (time.time() - start) * 1000
        record_query(latency_ms, triggered, error=False)

        logger.info(f"[{query_id}] Query processed | Mode: {req.mode} | Latency: {latency_ms:.2f}ms | Triggered: {len(triggered)}")

        return QueryResponse(
            query_id=query_id,
            query=req.query,
            mode=req.mode,
            response=response,
            confidence=confidence,
            authority_chain=authority_chain,
            determinism_hash=determinism_hash,
            latency_ms=round(latency_ms, 2),
            triggered_doctrines=triggered,
            metadata={"engine_id": ENGINE_ID, "version": VERSION}
        )
    except Exception as e:
        latency_ms = (time.time() - start) * 1000
        record_query(latency_ms, [], error=True)
        logger.error(f"[{query_id}] Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics_endpoint():
    return get_metrics()

@app.get("/doctrines")
def doctrines_endpoint():
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": [d.topic for d in DOCTRINE_CACHE],
        "coverage": STATE.coverage_map
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    uvicorn.run(app, host="127.0.0.1", port=PORT)
