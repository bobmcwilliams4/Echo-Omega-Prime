# Echo Omega Prime

An autonomous AI operating system built on Cloudflare Workers — multi-agent orchestration, domain intelligence engines, persistent memory, and self-healing error recovery.

## What Is This?

Echo Omega Prime is infrastructure for running reliable AI agent systems at scale. It solves the problems that break most AI agent setups: memory loss between sessions, cascading errors, lack of domain expertise, and coordination between multiple agents.

### Core Systems

- **674 Domain Intelligence Engines** — Specialized knowledge across 178 tiers (legal, tax, energy, medical, drilling, aviation, and 170+ more). Each engine contains curated doctrine blocks for accurate, domain-specific responses.
- **5-Tier Persistent Memory** — R2 Vault (permanent), Shared Brain (cross-instance), OmniSync (plans/todos), Memory Cortex V2 (cognitive with decay/promote/consolidate), Crystal Memory (indexed/searchable).
- **Multi-Agent Fleet** — Architect + Worker pattern with 128 concurrent agents. Task claiming, message passing, and handoff coordination.
- **GS343 Error Healing** — 45,962 error templates with pattern matching and automated fix suggestions. Errors get resolved, not repeated.
- **Knowledge Scout** — Daily automated scanning of GitHub, HuggingFace, ArXiv, Reddit, Hacker News, and Product Hunt for relevant developments.
- **Voice Synthesis** — Multi-personality TTS with emotional control via ElevenLabs and Qwen3-TTS.

## Architecture

```
┌─────────────────────────────────────────────────┐
│              ECHO OMEGA PRIME                   │
├─────────────────────────────────────────────────┤
│  Fleet Layer    │ Architect + 128 Worker Agents │
│  Memory Layer   │ 5-tier: R2 → Brain → Cortex  │
│  Engine Layer   │ 674 engines, 30K+ doctrines   │
│  Tool Layer     │ MCP tools via Echo Relay      │
│  Cloud Layer    │ 26 Workers, 10 R2, 10 D1      │
│  Voice Layer    │ Multi-personality TTS/STT      │
│  Healing Layer  │ GS343 + Phoenix auto-recovery │
└─────────────────────────────────────────────────┘
```

## Cloud Services

All services run as Cloudflare Workers with D1 (SQLite), R2 (object storage), KV (key-value), and Vectorize (embeddings).

| Service | Purpose |
|---------|---------|
| **Shared Brain** | Cross-instance memory with vector search |
| **Engine Runtime** | 674 engines with hybrid keyword + semantic search |
| **Knowledge Forge** | 5,387 documents, knowledge graph |
| **Knowledge Scout** | Daily automated scanning from 7 sources |
| **Build Orchestrator** | Engine build pipeline coordination |
| **OmniSync** | Cross-instance todos, policies, broadcasts |
| **Memory Prime** | 9-pillar cloud memory, 44 endpoints |
| **GS343** | Error healing with 45K+ templates |
| **Echo Chat** | 14-personality AI chat |

## Tech Stack

- **Runtime**: Cloudflare Workers (TypeScript, Hono framework)
- **Databases**: D1 (SQLite at the edge), R2, KV, Vectorize
- **Local Services**: Python 3.11, FastAPI, loguru
- **AI Models**: Claude (Anthropic), GPT-4.1 (Azure), local LLMs
- **Voice**: ElevenLabs v3, Qwen3-TTS, Whisper STT
- **Protocol**: MCP (Model Context Protocol) for tool integration

## Repo Structure

```
apps/                    # Web applications (Next.js on Vercel)
engines/                 # Domain intelligence engines by tier
  _shared/               # Shared utilities (cloud retriever, etc.)
  tier_01_legal/         # Legal engines (LG01-LG18)
  tier_02_landman/       # Land/title engines (LM01-LM22)
  tier_03_tax/           # Tax engines (TX01-TX14)
  ...                    # 30 tiers total
backbone/                # Gold-standard reference engines
specs/                   # Tier specifications with eval packs
workers/                 # Cloudflare Workers (one dir per worker)
services/                # Local services (GS343, Forge-X, etc.)
tools/                   # Build and migration tools
config/                  # Registry, ports, quality gates
.github/workflows/       # CI: quality gates run eval packs on PRs
```

## Quality Gates

Every engine goes through automated quality checks:

1. **Eval Pack** (50%) — 70%+ golden queries must pass
2. **Doctrine Count** (20%) — Minimum 30 DoctrineBlock instances
3. **Line Count** (15%) — 500+ lines minimum
4. **Structure** (15%) — Required components present

## Building

Workers are deployed via Wrangler:

```bash
cd workers/echo-gs343
npm install
npx wrangler deploy
```

Local engines run as FastAPI services:

```bash
cd engines/tier_03_tax/TX01_income_tax
python -m uvicorn main:app --port 8391
```

## Related Repositories

| Repo | Description |
|------|-------------|
| [echo-gs343](https://github.com/bobmcwilliams4/echo-gs343) | Error healing system (Cloudflare Worker) |
| [echo-knowledge-scout](https://github.com/bobmcwilliams4/echo-knowledge-scout) | Daily knowledge scanner |
| [shadowglass-browser](https://github.com/bobmcwilliams4/shadowglass-browser) | Privacy-first Electron browser |
| [echo-companion](https://github.com/bobmcwilliams4/echo-companion) | AI companion application |

## Author

**Bobby Don McWilliams II** — AI Systems Architect, Midland TX
📧 bobmcwilliams4@outlook.com · 🌐 [echo-op.com](https://echo-op.com)

## License

Proprietary — see [AGENTS.md](AGENTS.md) for system capabilities and integration details.
