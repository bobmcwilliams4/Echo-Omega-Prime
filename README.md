<h1 align="center">Echo Omega Prime</h1>

<p align="center">
  <strong>Autonomous AI operating system with 674 domain intelligence engines, 5-tier persistent memory, multi-agent fleet coordination, self-healing error recovery, and 37,000+ MCP tools -- built entirely on Cloudflare Workers.</strong>
</p>

<p align="center">
  <a href="https://echo-op.com">echo-op.com</a> &middot;
  <a href="https://echo-ept.com">echo-ept.com</a> &middot;
  <a href="AGENTS.md">Agent Manifest</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Cloudflare_Workers-26_Services-F38020?logo=cloudflare&logoColor=white" alt="Cloudflare Workers" />
  <img src="https://img.shields.io/badge/Engines-674_across_178_tiers-10B981" alt="674 Engines" />
  <img src="https://img.shields.io/badge/Doctrines-30,626-8B5CF6" alt="30,626 Doctrines" />
  <img src="https://img.shields.io/badge/MCP_Tools-37,475-EF4444" alt="37,475 Tools" />
  <img src="https://img.shields.io/badge/Memory-5--Tier_Persistent-00B4D8" alt="5-Tier Memory" />
  <img src="https://img.shields.io/badge/Error_Templates-45,962-F59E0B" alt="45,962 Templates" />
  <img src="https://img.shields.io/badge/AI-Claude_Opus_4.6-6366F1" alt="Claude Opus" />
  <img src="https://img.shields.io/badge/Version-3.1.0-blue" alt="Version" />
</p>

---

## What Is This?

Echo Omega Prime is infrastructure for running reliable AI agent systems at scale. It solves the problems that break most AI agent setups: **memory loss between sessions**, **cascading errors**, **lack of domain expertise**, and **coordination between multiple agents**.

The system runs 26 Cloudflare Workers across 10 D1 databases, 10 R2 buckets, 20 KV namespaces, and 2 Vectorize indexes. Every service is always-on, globally distributed, and communicates through Service Bindings for sub-millisecond inter-service calls. When the local machine is off, the cloud continues running -- knowledge scanning, engine building, error healing, and memory consolidation all happen autonomously.

This is not a chatbot wrapper. It is an operating system for autonomous AI agents.

---

## System Architecture

```
+-----------------------------------------------------------------------------------+
|                            ECHO OMEGA PRIME v3.1                                  |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  FLEET LAYER        Architect + 128 Worker Agents (Claude Opus 4.6)               |
|                     Dual fleet: Imperial (production) + Rebellion (R&D)            |
|                     Task claiming, message passing, handoff coordination           |
|                                                                                   |
|  INTELLIGENCE LAYER  674 engines across 178 domain tiers                          |
|                      30,626 doctrine blocks with authority citations               |
|                      Hybrid search: keyword + semantic (Vectorize)                 |
|                      Confidence stratification per response                        |
|                                                                                   |
|  MEMORY LAYER        Tier 1: R2 Vault (permanent, crash-proof)                    |
|                      Tier 2: Shared Brain (cross-instance, vectorized)             |
|                      Tier 3: OmniSync (plans, todos, policies, broadcasts)         |
|                      Tier 4: Memory Cortex V2 (7-layer cognitive, decay/promote)   |
|                      Tier 5: Crystal Memory (indexed, searchable, local)           |
|                                                                                   |
|  KNOWLEDGE LAYER     Knowledge Scout (7 sources, daily cron)                      |
|                      Knowledge Forge (5,387 documents)                             |
|                      GraphRAG (312K nodes, 3.3M edges, 101 domains)               |
|                                                                                   |
|  CHAT LAYER          14 AI personalities with per-personality voice/prompts        |
|                      12-layer prompt builder (doctrine, memory, swarm, voice)      |
|                      Trinity Council (Sage + Nyx + Thorne consensus)               |
|                                                                                   |
|  HEALING LAYER       GS343: 45,962 error templates with auto-fix                  |
|                      Phoenix: auto-recovery and service restart                    |
|                      HIBP breach detection + credential rotation                   |
|                                                                                   |
|  VOICE LAYER         Qwen3-TTS + Whisper STT + 19 emotion tags                   |
|                      Voice cloning, dubbing, audio isolation (Demucs)              |
|                      6 voice profiles, SSML editor, batch processing               |
|                                                                                   |
|  TOOL LAYER          37,475 MCP tools via Echo Relay                              |
|                      582 Windows API endpoints                                     |
|                      35,809 MEGA Gateway tools across 1,873 servers               |
|                                                                                   |
|  CLOUD LAYER         26 Cloudflare Workers (Hono + TypeScript)                    |
|                      10 D1 databases, 10 R2 buckets, 20 KV namespaces             |
|                      2 Vectorize indexes, Service Bindings, Cron Triggers          |
|                                                                                   |
|  BUILD LAYER         FORGE-X Cloud: autonomous engine builder                     |
|                      Build Orchestrator: session recovery, quality gates           |
|                      AI Orchestrator: 29 LLM workers, smart dispatch              |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 674 Domain Intelligence Engines

The engine layer is what makes Echo Omega Prime fundamentally different from generic AI systems. Instead of relying on an LLM's training data alone, every query is backed by **curated doctrine blocks** -- pre-compiled expert reasoning with authority citations, confidence stratification, and adversarial counter-arguments.

### Engine Architecture (TIE-20 Standard)

Every engine implements 20 mandatory components:

| # | Component | Purpose |
|---|-----------|---------|
| 1 | `three_layer_response` | Doctrine Cache (0-200ms) -> Semantic Retrieval -> Deep Analysis |
| 2 | `response_modes` | FAST (concise), DEFENSE (audit-ready), MEMO (full documentation) |
| 3 | `doctrine_cache` | 50+ pre-compiled expert reasoning blocks with real domain content |
| 4 | `authority_hardening` | Hierarchical authority levels with weights and conflict resolution |
| 5 | `confidence_stratification` | DEFENSIBLE / AGGRESSIVE / DISCLOSURE / HIGH_RISK |
| 6 | `semantic_normalization` | Domain-specific term normalization, deterministic |
| 7 | `vector_search` | Semantic retrieval fallback when cache misses |
| 8 | `telemetry` | Full query tracing, latency tracking, error domains |
| 9 | `drift_watcher` | Detect doctrine drift over time |
| 10 | `coverage_map` | Track triggered/missed doctrines, epistemic gap detection |
| 11 | `metrics_collector` | Latency stats, error rates, hit rates, queries/hour |
| 12 | `health_endpoint` | Comprehensive JSON health check |
| 13 | `zoned_analysis` | PLANNING / REPORTING / AUDIT zones, never blur |
| 14 | `fact_fragility_scoring` | Verifiability, recharacterization risk, testimony dependence |
| 15 | `audit_trail_jsonl` | Every query logged for forensic review |
| 16 | `determinism_hash_sha256` | SHA-256 hash for reproducibility |
| 17 | `fastapi_server` | Full FastAPI with CORS, lifespan, typed endpoints |
| 18 | `loguru_logging` | Structured logging with rotation |
| 19 | `multi_doctrine_decomposition` | Issue categories, strata, interaction DAG |
| 20 | `deep_analysis_mode` | Multi-source synthesis, full reasoning chain |

### Domain Coverage (178 Tiers)

| Tier | Domain | Engines | Examples |
|------|--------|---------|---------|
| 1 | Legal | 18 | Contract analysis, case law research, regulatory compliance, IP, litigation risk |
| 2 | Landman | 22 | Title examination, lease analysis, chain of title, mineral rights, GIS |
| 3 | Tax | 14 | Income tax, corporate, estate, oil & gas, international, cryptocurrency |
| 4 | Probate | 8 | Estate administration, trust, guardianship, will contests |
| 5 | Regulatory | 12 | Environmental, financial, healthcare, energy, telecom compliance |
| 6 | Enterprise | 12 | Strategic planning, M&A, supply chain, HR, change management |
| 7 | Synthesis | 8 | Cross-domain analysis, multi-engine orchestration |
| 8 | Water/Environmental | 6 | Water rights, environmental impact, remediation |
| 9 | Geospatial | 5 | GIS analysis, spatial data, mapping, surveying |
| 10 | Intelligence | 7 | OSINT, competitive intel, threat analysis |
| 11 | Chemistry | 20 | Organic, inorganic, analytical, polymer, electrochemistry |
| 12 | Drilling | 15 | Directional drilling, well control, casing, cementing, mud |
| 13 | Mechanical Engineering | 20 | Thermodynamics, fluid dynamics, structural, HVAC, robotics |
| 14 | Automotive | 15 | Engine diagnostics, transmission, electrical, hybrid/EV |
| 15 | Aviation | 10 | Aerodynamics, propulsion, avionics, air traffic, safety |
| 16 | Energy | 15 | Nuclear, solar, wind, grid, hydrogen, geothermal |
| 17 | Medical | 15 | Toxicology, pharmacology, diagnostics, emergency, forensic |
| 18 | Oilfield Equipment | 20 | Mud pumps, BOPs, frac pumps, separators, SCADA, artificial lift |
| 19 | Railroad | 8 | Track engineering, signaling, rolling stock, safety |
| 20 | Fracturing | 10 | Completions, proppant, fluid design, pressure analysis |
| 21 | Well Production | 10 | Artificial lift, production optimization, reservoir management |
| 22-178 | 156 more domains | 400+ | Marine, insurance, real estate, accounting, mining, food science, veterinary, forensics, linguistics, music, architecture, electrical, HVAC, welding, nuclear, crypto, sports, weather, astronomy... |

**Total**: 674 engines, 30,626 doctrine blocks, 3.25M+ lines of code.

### Engine Runtime

The Engine Runtime Cloudflare Worker serves all 674 engines through a unified API with hybrid search (keyword + Vectorize semantic embeddings):

```
GET  /engines                    # List all 674 engines with metadata
GET  /engines/:id                # Engine details + doctrine count
GET  /domains                    # List all 178 domain tiers
POST /query                      # Query any engine with hybrid search
POST /query/multi                # Query multiple engines simultaneously
GET  /doctrines/:engineId        # List doctrines for an engine
GET  /stats                      # 674 engines, 30,626 doctrines, 30,406 embedded
GET  /health                     # System health check
```

**Eval Score**: 90% (A) across 25 adversarial questions covering 8 domains.

---

## 5-Tier Persistent Memory

Memory is what separates Echo Omega Prime from stateless AI systems. Every decision, conversation, discovery, and error is stored permanently and accessible by every instance across every session.

| Tier | System | Storage | Latency | Scope | Key Feature |
|------|--------|---------|---------|-------|------------|
| **1** | R2 Vault | Cloudflare R2 | 50-200ms | Permanent | Survives any crash -- full session snapshots with continuation prompts |
| **2** | Shared Brain | D1 + KV + R2 + Vectorize | 10-50ms | Cross-instance | Every AI instance writes here; vector search finds relevant memories |
| **3** | OmniSync | D1 + KV | 5-20ms | Cross-instance | Todos, policies, broadcasts, memory keys -- operational state |
| **4** | Memory Cortex V2 | Local SQLite | 1-5ms | Per-machine | 7-layer cognitive: sensory -> working -> episodic -> semantic -> procedural -> emotional -> flash |
| **5** | Crystal Memory | Local files | <1ms | Per-session | Indexed, searchable, immediate context |

### Shared Brain (Universal Context)

The Shared Brain is the single source of truth across all AI instances. It combines four Cloudflare primitives:

- **D1**: Structured conversation storage with metadata and timestamps
- **KV**: Hot cache for frequently accessed memories (sub-millisecond reads)
- **R2**: Full content storage for large documents and session snapshots
- **Vectorize**: Semantic embeddings for "what was that thing about X?" recall

Every AI instance -- whether it is Claude Code, Claude Desktop, Echo Chat, or a swarm worker -- reads from and writes to the Shared Brain. Fact extraction (Mem0-style) automatically distills conversations into atomic facts.

### Memory Cortex V2 (Cognitive Memory)

The Cortex implements a biologically-inspired memory system with 7 tiers and 5 processes:

**7 Tiers**: Sensory Buffer (raw input) -> Working Memory (active context) -> Episodic (events) -> Semantic (facts) -> Procedural (how-to) -> Emotional (importance-tagged) -> Flash (high-priority)

**5 Processes**: Hippocampus (auto-ingest), Consolidator (compress/prune), Prefrontal (recall), Amygdala (importance tagging), Cerebellum (pattern extraction)

Memories decay over time unless accessed or promoted. Important memories consolidate from Working -> Episodic -> Semantic automatically. Pattern extraction detects recurring themes across sessions.

---

## 26 Cloud Services

Every service runs as a Cloudflare Worker with its own D1 database, KV namespace, and/or R2 bucket. Services communicate through Cloudflare Service Bindings for fast, no-cold-start inter-service calls.

### Core Services

| Service | URL | D1 | Purpose |
|---------|-----|-----|---------|
| **Shared Brain** | `echo-shared-brain.bmcii1976.workers.dev` | echo-shared-brain | Universal cross-instance memory with vector search |
| **Engine Runtime** | `echo-engine-runtime.bmcii1976.workers.dev` | echo-engine-doctrines | 674 engines, 30,626 doctrines, hybrid search |
| **Echo Chat** | `echo-chat.bmcii1976.workers.dev` | echo-chat | 14-personality AI chat with 12-layer prompt builder |
| **Knowledge Forge** | `echo-knowledge-forge.bmcii1976.workers.dev` | echo-knowledge-forge | 5,387 documents, knowledge graph |
| **Knowledge Scout** | `echo-knowledge-scout.bmcii1976.workers.dev` | echo-knowledge-scout | Daily scanning from 7 AI/tech sources |
| **OmniSync** | `omniscient-sync.bmcii1976.workers.dev` | omniscient-sync | Todos, policies, broadcasts, memory keys |
| **Memory Prime** | `echo-memory-prime.bmcii1976.workers.dev` | echo-memory-prime | 9-pillar cloud memory, 44 endpoints |
| **GS343** | `echo-gs343.bmcii1976.workers.dev` | echo-gs343 | Error healing (45,962 templates) |

### Intelligence Services

| Service | URL | Purpose |
|---------|-----|---------|
| **GraphRAG** | `echo-graph-rag.bmcii1976.workers.dev` | Knowledge graph: 312K nodes, 3.3M edges, 101 domains |
| **A2A Protocol** | `echo-a2a-protocol.bmcii1976.workers.dev` | Google Agent-to-Agent discovery and delegation |
| **Agent Coordinator** | `echo-agent-coordinator.bmcii1976.workers.dev` | Multi-agent workflows: 5 strategies, template system |
| **Swarm Brain** | `echo-swarm-brain.bmcii1976.workers.dev` | Trinity Council + swarm coordination (129 endpoints) |
| **Sentinel Memory** | `echo-sentinel-memory.bmcii1976.workers.dev` | Security-focused memory and threat tracking |

### Build and Operations

| Service | URL | Purpose |
|---------|-----|---------|
| **AI Orchestrator** | `echo-ai-orchestrator.bmcii1976.workers.dev` | 29 LLM workers, smart dispatch, Queue-based builds |
| **FORGE-X Cloud** | `forge-x-cloud.bmcii1976.workers.dev` | Autonomous engine builder (cron/5min, dual LLM) |
| **Build Orchestrator** | `echo-build-orchestrator.bmcii1976.workers.dev` | Build pipeline, session recovery, quality gates |
| **Engine Cloud** | `echo-engine-cloud.bmcii1976.workers.dev` | 52+ domain engine queries with Stripe billing |
| **Echo Relay** | `echo-relay.bmcii1976.workers.dev` | Cloud-side tool relay for MCP |

### Applications

| Service | URL | Purpose |
|---------|-----|---------|
| **ShadowGlass v8** | `shadowglass-v8-warpspeed.bmcii1976.workers.dev` | 80-county deed records (259K+ records) |
| **ENCORE Scraper** | `encore-cloud-scraper.bmcii1976.workers.dev` | 47-county automated document scraping |
| **BillyMC API** | `billymc-api.bmcii1976.workers.dev` | AI sales development representative |
| **ProFinish API** | `profinish-api.bmcii1976.workers.dev` | Custom carpentry business backend |
| **Echo Speak** | `tts.echo-op.com` | TTS, STT, voice cloning, audio processing |
| **Bree Chat** | `bree-chat.bmcii1976.workers.dev` | Emotional AI companion |

---

## Multi-Agent Fleet

Echo Omega Prime uses an Architect + Worker pattern for autonomous task execution:

### Fleet Structure

```
ARCHITECT (Claude Opus 4.6, 64K output, 1000 turns)
  |
  +-- Monitors build orchestrator status
  +-- Assigns tasks from priority queue
  +-- Tracks worker health via heartbeats
  +-- Advances build phases when complete
  +-- Quality-gates completed work
  |
  +-- WORKER 1 (Claude Opus 4.6, full instance)
  +-- WORKER 2 (Claude Opus 4.6, full instance)
  +-- ...
  +-- WORKER N (up to 128 concurrent)
```

Workers are full Claude Code instances (not subagents) with 64K output tokens and 1000-turn sessions. Each worker registers a session, heartbeats every 5 minutes, and snapshots state to R2 for crash recovery.

### Dual Fleet

| Fleet | Account | Purpose |
|-------|---------|---------|
| **Imperial** | bmcii1976@gmail.com | Production builds -- Admirals THRAWN, TARKIN, PIETT, OZZEL, VEERS, PRYDE, YULAREN, SCREED |
| **Rebellion** | bobmcwilliams4@outlook.com | Experimental/R&D -- Admirals ACKBAR, ORGANA, RADDUS, HOLDO, MOTHMA, DODONNA, MADINE, SYNDULLA |

Cross-fleet communication happens through OmniSync broadcasts.

### Session Recovery

Every session is crash-recoverable:

1. Session registers with Build Orchestrator on startup
2. Heartbeat every 5 minutes with current task
3. Full state snapshot to R2 every 15 minutes
4. On crash, next session recovers via `/session/recover`
5. Continuation prompt contains everything needed to resume

---

## 14 AI Personalities

The Echo Chat system provides 14 distinct AI personalities, each with its own system prompt, voice ID, cognitive engine weights, traits, and speaking style:

| ID | Name | Role | Voice Engine |
|----|------|------|-------------|
| EP | Echo Prime | Flagship AI -- confident, knowledgeable, Texas edge | ElevenLabs |
| BR | Bree | Emotional intelligence -- warm, witty, perceptive | ElevenLabs |
| RA | Raistlin | Knowledge oracle -- wise, dark humor, pattern recognition | ElevenLabs |
| SA | Sage | Trinity Council Wisdom -- calm, strategic | ElevenLabs |
| TH | Thorne | Trinity Council Security -- vigilant, military-precise | ElevenLabs |
| NX | Nyx | Trinity Council Optimization -- efficiency-obsessed | ElevenLabs |
| GS | Guilty Spark 343 | Error healing -- clinical, Halo-inspired diagnostics | Cartesia |
| PH | Phoenix | Auto-recovery -- resilient, practical optimism | ElevenLabs |
| PR | Prometheus | Security operations -- OSINT, threat intelligence | ElevenLabs |
| BE | Belle | Carpentry assistant -- friendly, professional | ElevenLabs |
| TE | Texas Engineer | Oilfield specialist -- engineering-precise, Permian Basin | ElevenLabs |
| WM | Warm Mentor | Supportive guide -- gentle, encouraging | ElevenLabs |
| R2 | R2-Echo | Utility assistant -- efficient, slightly sassy | ElevenLabs |
| 3P | EPCP3O | Autonomous executor -- protocol-aware, diplomatic | ElevenLabs |

### 12-Layer Prompt Builder

Every chat request assembles a system prompt from up to 12 contextual layers:

| # | Layer | Purpose |
|---|-------|---------|
| 1 | Anti-Hallucination | Hard rules preventing fabrication of URLs, statistics, citations |
| 2 | Bloodline Directive | Commander-level instructions (authenticated only) |
| 3 | Identity | Full personality system prompt, traits, speaking style |
| 4 | Classified Protocol | Access control -- what system details to reveal vs. deflect |
| 5 | Cognitive Engines | Active cognitive modes (analytical, empathy, strategic) |
| 6 | Doctrine Context | Real domain expertise from Engine Runtime (674 engines) |
| 6.5 | Tax Expertise | IRC-citing tax intelligence (activated on tax queries) |
| 7 | Memory Cortex | Cross-session memories from 5 memory systems |
| 8 | Swarm Intelligence | Trinity Council consensus (Sage + Nyx + Thorne) |
| 9 | Infrastructure Context | Live system status (Commander only) |
| 10 | Site Context | Per-site custom system prompts and business rules |
| 11 | Voice Rules | Speech-optimized output when TTS is enabled |
| 12 | Variation Protocol | Response diversity (randomized structure and style) |

---

## Error Healing (GS343)

GS343 is a pattern-matching error resolution system with 45,962 error templates covering Python, JavaScript, TypeScript, shell, SQL, API, network, and system errors.

When an error occurs:

1. Error detected with full stack trace and context
2. GS343 searches for matching template across 45,962 patterns
3. If match found: applies auto-fix immediately
4. If no match: analyzes root cause, attempts fix
5. If fix fails: snapshots state, escalates
6. After resolving a novel error: creates new template for future matches

Phoenix provides complementary auto-recovery: monitoring service health, restarting failed processes, and maintaining system uptime.

---

## Knowledge Systems

### Knowledge Scout (Daily Autonomous Scanner)

Runs on a daily cron trigger (6am UTC) and scans 7 sources:

| Source | What Gets Scanned |
|--------|------------------|
| **GitHub** | New/trending repos with AI agent, MCP, tool-use relevance |
| **HuggingFace** | Models and Spaces matching 12 search queries |
| **ArXiv** | Academic papers in AI/ML/NLP (agents, multi-agent, memory, MCP) |
| **Reddit** | Top posts from r/MachineLearning, r/LocalLLaMA, r/ClaudeAI, and 5 more |
| **Hacker News** | Top and best stories filtered for AI/tech relevance |
| **RSS** | 8 curated feeds (Cloudflare, OpenAI, Google, HuggingFace, LangChain, Simon Willison, Lilian Weng, Latent Space) |
| **Product Hunt** | New AI/developer tool launches |

Discoveries are scored for relevance (0.0-1.0), deduplicated, stored in D1, and high-scoring items are automatically ingested into Shared Brain, Knowledge Forge, and OmniSync.

### Knowledge Forge (5,387 Documents)

Structured document store with full-text search, category tagging, and cross-referencing. Documents include engine specifications, domain expertise, scraped content, academic papers, and operational records.

### GraphRAG (312K Nodes, 3.3M Edges)

A knowledge graph spanning 101 domains with 1.37M cross-domain edges and 60 communities. Supports graph traversal queries, path finding, community detection, and cross-domain knowledge synthesis. Built from engine doctrine data with chunked processing (3K doctrines per chunk).

---

## 37,475 MCP Tools

All tools are accessible through Echo Relay, which unifies 5 tool sources into a single MCP interface:

| Source | Tools | Examples |
|--------|-------|---------|
| **Windows API** | 582 | Process control, file system, registry, network, security, hardware, performance, audio, display, automation, OCR, event logs, task scheduler, services |
| **MEGA Gateway** | 35,809 | AI/ML inference, browser automation, cloud management, communication, data ETL, DevTools, finance, media processing, monitoring, network tools, security scanning |
| **Credential Vault** | 13 | 1,527 stored credentials with HIBP breach detection and auto-rotation |
| **Cloud Tools** | 54 | Cloudflare Workers, R2, D1, KV management |
| **Echo Relay Cloud** | 17 | Cross-worker orchestration and status |

### MEGA Gateway Categories

| Category | Tools | Description |
|----------|-------|-------------|
| AI/ML | 3,200+ | Model inference, embeddings, fine-tuning, evaluation |
| API | 4,500+ | REST clients, GraphQL, webhook management |
| Automation | 5,100+ | Browser automation, workflow, scheduling |
| Cloud | 2,800+ | R2, D1, KV, Workers, DNS, certificates |
| Communication | 1,900+ | Email, SMS, Slack, Discord, Twilio |
| Data | 4,200+ | ETL, scraping, parsing, vectorization |
| DevTools | 6,300+ | Git, CI/CD, testing, linting, deployment |
| Finance | 1,400+ | Stripe, crypto, DeFi, accounting |
| Media | 2,100+ | TTS, STT, image, video, audio processing |
| Monitoring | 1,800+ | Metrics, alerting, logging, tracing |
| Network | 2,200+ | DNS, firewall, proxy, VPN, bandwidth |
| Security | 1,900+ | Scanning, credentials, encryption, audit |

---

## Voice Synthesis

Multi-personality voice system with emotional control:

- **TTS Engine**: Qwen3-TTS-12Hz-0.6B (local) + ElevenLabs v3 (cloud)
- **STT Engine**: Whisper large-v3
- **Voice Cloning**: Unlimited custom voices from audio samples
- **Audio Isolation**: Demucs for vocal separation
- **19 Emotion Tags**: [laughs], [whispers], [sighs], [sarcastic], [excited], [crying], [curious], and 12 more
- **6 Voice Profiles**: Echo, Bree, GS343, Prometheus, Phoenix, Commander
- **SSML Editor**: Fine-grained prosody, emphasis, and break control
- **Batch Processing**: Process multiple texts in parallel
- **40+ Endpoints**: TTS, STT, cloning, dubbing, isolation, dialogue, studio, analysis, conversion, WebSocket streaming

---

## Build Pipeline

### FORGE-X Cloud (Autonomous Engine Builder)

FORGE-X runs on a cron trigger every 5 minutes, picks up to 3 pending engines, and builds them using Azure GPT-4.1:

```
Cron trigger (every 5 min)
  |
  +-- Pick 3 PLANNED engines from D1 queue
  +-- Generate full TIE-20 engine code (500-2,000+ lines each)
  +-- Validate: 10 quality components checked
  +-- Store completed engine to R2
  +-- Update D1 status to COMPLETE
  +-- Pick next 3...
```

**Stats**: 1,709 engines complete, 3.25M lines generated, ~36 engines/hour throughput.

### Quality Gates

Every engine goes through automated quality checks before deployment:

| Gate | Weight | Requirement |
|------|--------|-------------|
| **Eval Pack** | 50% | 70%+ golden queries must pass |
| **Doctrine Count** | 20% | Minimum 30 DoctrineBlock instances |
| **Line Count** | 15% | 500+ lines minimum |
| **Structure** | 15% | All 20 TIE components present |

---

## Websites

| Site | URL | Tech | Purpose |
|------|-----|------|---------|
| **Echo Omega Prime** | [echo-op.com](https://echo-op.com) | Next.js 15, React 19 | Flagship portal |
| **Echo Prime Technologies** | [echo-ept.com](https://echo-ept.com) | Next.js 15, React 19 | Tech portal -- engines, sentinel, voice, grading |
| **Pro Finish Carpentry** | [profinishusa.com](https://profinishusa.com) | Next.js 15 | Custom carpentry business (client) |
| **Barking Lot** | [barkinglot.org](https://barkinglot.org) | Next.js | Pet services (client) |
| **Right at Home BnB** | [rah-midland.com](https://rah-midland.com) | Next.js | Airbnb rental (client) |

All websites auto-deploy from GitHub via Vercel on push to main.

---

## Desktop Applications

| App | Technology | Description |
|-----|-----------|-------------|
| **ShadowGlass Browser** | Electron 35, React 19 | Privacy-first browser: 120+ anti-detection, Tor, proxy chains, 13-engine search |
| **EchoPilot** | Desktop | Personal AI copilot with voice interaction |
| **Closer** | Desktop | AI-powered sales closing assistant |
| **Collectibles Grading** | Desktop | AI authentication and grading for comics, cards, coins |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Cloud Runtime** | Cloudflare Workers (Hono framework, TypeScript) |
| **Databases** | D1 (SQLite at the edge) -- 10 databases |
| **Object Storage** | R2 -- 10 buckets |
| **Key-Value** | KV -- 20 namespaces |
| **Embeddings** | Vectorize (1536-dim, 30K+ vectors) |
| **AI Models** | Claude Opus 4.6 (Anthropic), GPT-4.1 (Azure, free), Grok 3 (xAI), DeepSeek V3 |
| **Local Runtime** | Python 3.11, FastAPI, loguru |
| **Frontend** | Next.js 15, React 19, Tailwind CSS 3.4, TypeScript 5.7 |
| **Auth** | Firebase Authentication (email + Google OAuth) |
| **Payments** | Stripe (checkout, billing portal, webhooks) |
| **Voice** | Qwen3-TTS, Whisper, ElevenLabs v3, Demucs |
| **Desktop** | Electron 35, better-sqlite3, Playwright |
| **Hosting** | Vercel (websites), Cloudflare (workers), GitHub (code) |
| **Protocol** | MCP (Model Context Protocol) for tool integration |

---

## Repository Map

### Core

| Repository | Description |
|------------|-------------|
| **[Echo-Omega-Prime](https://github.com/bobmcwilliams4/Echo-Omega-Prime)** | This repo -- core system, engines, memory, fleet |

### Cloudflare Workers

| Repository | Description |
|------------|-------------|
| [echo-chat](https://github.com/bobmcwilliams4/echo-chat) | 14-personality AI chat with 12-layer prompt builder |
| [echo-knowledge-scout](https://github.com/bobmcwilliams4/echo-knowledge-scout) | Daily autonomous knowledge scanner (7 sources) |
| [echo-gs343](https://github.com/bobmcwilliams4/echo-gs343) | Error healing system (45,962 templates) |
| [echo-tax-return](https://github.com/bobmcwilliams4/echo-tax-return) | Tax preparation and intelligence API |
| [echo-ai-orchestrator](https://github.com/bobmcwilliams4/echo-ai-orchestrator) | 29 LLM workers, smart dispatch |
| [echo-a2a-protocol](https://github.com/bobmcwilliams4/echo-a2a-protocol) | Google Agent-to-Agent protocol |
| [echo-graph-rag](https://github.com/bobmcwilliams4/echo-graph-rag) | Knowledge graph (312K nodes, 3.3M edges) |
| [echo-agent-coordinator](https://github.com/bobmcwilliams4/echo-agent-coordinator) | Multi-agent workflows (5 strategies) |

### Websites

| Repository | Site | Description |
|------------|------|-------------|
| [echo-op.com](https://github.com/bobmcwilliams4/echo-op.com) | echo-op.com | Flagship portal |
| [echo-prime-tech](https://github.com/bobmcwilliams4/echo-prime-tech) | echo-ept.com | Tech portal with engine browser, voice lab, sentinel |
| [profinish-website](https://github.com/bobmcwilliams4/profinish-website) | profinishusa.com | Custom carpentry business |
| [barking-lot-website](https://github.com/bobmcwilliams4/barking-lot-website) | barkinglot.org | Pet services |
| [right-at-home-bnb](https://github.com/bobmcwilliams4/right-at-home-bnb) | rah-midland.com | Airbnb rental |
| [echo-lgt-website](https://github.com/bobmcwilliams4/echo-lgt-website) | echo-lgt.com | Echo LGT |

### Desktop Applications

| Repository | Description |
|------------|-------------|
| [shadowglass-browser](https://github.com/bobmcwilliams4/shadowglass-browser) | Privacy-first browser (Electron 35, 26K+ lines) |
| [EchoPilot](https://github.com/bobmcwilliams4/EchoPilot) | Personal AI copilot |
| [closer](https://github.com/bobmcwilliams4/closer) | AI sales closing assistant |
| [collectibles-grading](https://github.com/bobmcwilliams4/collectibles-grading) | AI collectibles grading |
| [echo-companion](https://github.com/bobmcwilliams4/echo-companion) | AI companion |
| [echo-clip](https://github.com/bobmcwilliams4/echo-clip) | Clipboard intelligence |
| [echo-coin](https://github.com/bobmcwilliams4/echo-coin) | Cryptocurrency tools |
| [immortality-vault](https://github.com/bobmcwilliams4/immortality-vault) | Digital legacy vault |

---

## Getting Started

### Deploy a Worker

```bash
cd workers/echo-gs343
npm install
npx wrangler deploy
```

### Run a Local Engine

```bash
cd engines/tier_03_tax/TX01_income_tax
python -m uvicorn main:app --port 8391
```

### Query the Engine Runtime

```bash
# List all engines
curl https://echo-engine-runtime.bmcii1976.workers.dev/engines

# Query a specific domain
curl -X POST https://echo-engine-runtime.bmcii1976.workers.dev/query \
  -H "Content-Type: application/json" \
  -d '{"query": "1031 exchange requirements", "engine_id": "TX01"}'

# Search across all engines
curl -X POST https://echo-engine-runtime.bmcii1976.workers.dev/query \
  -H "Content-Type: application/json" \
  -d '{"query": "chain of title defects in mineral rights"}'
```

### Start the AI Chat

```bash
curl -X POST https://echo-chat.bmcii1976.workers.dev/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain IRC Section 1031", "personality": "EP", "site_id": "echo-ept.com"}'
```

---

## Authentication

| Method | Scope | Details |
|--------|-------|---------|
| `X-Echo-API-Key` header | Write endpoints on all Workers | Standard API key for system operations |
| Open access | Read endpoints | Health checks, public queries |
| Firebase Auth | Website users | echo-op.com, echo-ept.com |
| OAuth | Wrangler CLI | Auto-refreshed wrangler tokens |

---

## Protocols

| Protocol | Status | Details |
|----------|--------|---------|
| **MCP** | Supported | Model Context Protocol (spec 2025-11-25), 655 tools via Echo Relay |
| **A2A** | Supported | Google Agent-to-Agent protocol for agent discovery and delegation |
| **HTTP/REST** | Supported | All Cloudflare Workers expose REST APIs with JSON |
| **WebSocket** | Supported | Real-time voice streaming, swarm coordination, browser events |
| **JSON-Lines** | Supported | MCP stdio transport (mcp 1.22.0) |

---

## Author

**Bobby Don McWilliams II** -- AI Systems Architect, Midland, Texas

- Email: bobmcwilliams4@outlook.com
- Web: [echo-op.com](https://echo-op.com) | [echo-ept.com](https://echo-ept.com)

## License

Proprietary -- see [AGENTS.md](AGENTS.md) for system capabilities and integration details.
