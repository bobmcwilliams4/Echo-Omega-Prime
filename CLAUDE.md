# ECHO OMEGA PRIME -- Monorepo
## Commander: Bobby Don McWilliams II | Authority: 11.0

## 3 Active Systems
- **Orchestrator**: https://echo-build-orchestrator.bmcii1976.workers.dev
- **Doctrine Brain**: https://echo-doctrine-brain.bmcii1976.workers.dev
- **OmniSync**: https://omniscient-sync.bmcii1976.workers.dev

## On Startup (3 calls)
1. `GET orchestrator/status`
2. `GET omniscient-sync/todos`
3. `GET doctrine-brain/spec/{tier}` (if building)

## Building Engines
- **Specs**: `specs/*.json` (one per tier, eval packs included)
- **Task packages**: `GET doctrine-brain/task/{engine_id}`
- **Output modes**: `doctrine_blocks` (primary) or `engine_files` (legacy)
- **Quality**: eval pack is the primary gate -- builder does NOT self-grade
- **Report**: `POST orchestrator/build/complete`

## Auth
- All write endpoints require `X-Echo-API-Key` header
- Key stored as Cloudflare secret on all Workers

## Coding Standards
- `loguru` (never print), `pathlib.Path` (never os.path), type hints, Pydantic, FastAPI
- Zero: TODO, pass, stubs, NotImplementedError
- Python 3.11+ via `H:\Tools\PyManager\pythons\py311\python.exe`

## Repo Layout
```
apps/echo-op.com/        # Next.js website (Vercel)
engines/                  # All engine dirs, organized by tier prefix
  _shared/                # cloud_retriever.py, shared utilities
  tier_01_legal/          # LG01-LG18 + LIE backbone
  tier_02_landman/        # LM01-LM22 + LMIE backbone
  tier_03_tax/            # TX01-TX14 + TIE backbone
  ... (30 tiers)
backbone/                 # Gold-standard reference engines (TIE/PIE/ARCS)
specs/                    # Tier specs with eval packs (_schema.json + per-tier)
workers/                  # Cloudflare Workers (one dir per worker)
services/                 # Local services (prometheus, gs343, forge-x, etc.)
tools/                    # Build tools (migrate, validate, generate specs)
config/                   # engine_registry.json, ports.json, quality_gates.json
.github/workflows/        # CI: quality-gate.yml runs eval packs on PRs
```

## Quality Gates (CI runs on PR)
1. **EVAL_PACK** (50%): 70%+ golden queries pass
2. **DOCTRINE_COUNT** (20%): >= 30 DoctrineBlock instances
3. **CITATION_DENSITY** (15%): >= 2 citations per block average
4. **SYNTAX** (10%): py_compile passes
5. **NO_PLACEHOLDERS** (5%): zero TODO/pass/NotImplementedError

## Builder Selection
| Type | Builder | Reason |
|------|---------|--------|
| Standard | Azure GPT-4.1 | Free, 32K output |
| Backbone (2000+ lines) | Claude Sonnet 4.5 | 64K output |
| Failed 2x | Claude Code Worker | Can iterate/fix |

## Website
- **Current**: `echo-op.com` (untouched, existing Vercel project)
- **Rebuild**: `rebuild.echo-op.com` (monorepo `apps/echo-op.com/`)
- Swap when ready (Vercel domain swap, 30 seconds)

## Key Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /status` | Orchestrator dashboard |
| `GET /engines?status=PLANNED` | Engines needing builds |
| `POST /build/complete` | Builder callback |
| `POST /gates/report` | Quality gate results |
| `GET /spec/:tier` | Tier spec with eval pack |
| `GET /task/:engine_id` | Self-contained task package |
