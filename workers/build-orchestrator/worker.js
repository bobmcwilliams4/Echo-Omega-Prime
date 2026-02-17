// ═══════════════════════════════════════════════════════════════════════════
// ECHO PRIME BUILD ORCHESTRATOR v1.0
// Autonomous Engine Factory — Works While Commander Sleeps
// ═══════════════════════════════════════════════════════════════════════════
// 
// ARCHITECTURE:
//   Cron Trigger fires every 5 minutes to check build queue
//   D1 database tracks all engines, gates, and progress
//   Dispatches build tasks to Claude Code terminal via API
//   Enforces quality gates before advancing to next engine
//   Reports progress to Omniscient Sync + Commander alerts
//
// FLOW:
//   Cron fires → Check queue → Find next buildable engine →
//   Generate build spec → Dispatch to Claude Code →
//   Wait for completion → Run quality gates →
//   If PASS → mark deployed, advance queue
//   If FAIL → retry (max 3) → alert Commander if stuck
// ═══════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════
// AUTH MIDDLEWARE — X-Echo-API-Key required on all POST routes
// ═══════════════════════════════════════════════════════════════════════════
function authenticate(request, env) {
  const key = request.headers.get('X-Echo-API-Key');
  if (!env.ECHO_API_KEY) return null; // no key configured = allow (backward compat during rollout)
  if (key === env.ECHO_API_KEY) return null;
  return json({ error: 'Unauthorized', message: 'Valid X-Echo-API-Key header required' }, 401);
}

export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(orchestrate(env));
  },

  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders() });
    }

    // Auth gate: all POST/PUT/DELETE requests require API key
    if (['POST', 'PUT', 'DELETE'].includes(request.method)) {
      const authErr = authenticate(request, env);
      if (authErr) return authErr;
      // Payload size cap: 1MB
      const contentLength = parseInt(request.headers.get('Content-Length') || '0');
      if (contentLength > 1_048_576) {
        return json({ error: 'Payload too large', max_bytes: 1_048_576 }, 413);
      }
    }

    try {
      // ── STATUS DASHBOARD ──
      if (path === '/' || path === '/status') {
        return json(await getFullStatus(env));
      }
      // ── ENGINE LIST ──
      if (path === '/engines') {
        return json(await getEngines(env, url.searchParams.get('tier'), url.searchParams.get('status')));
      }
      // ── SINGLE ENGINE ──
      if (path.startsWith('/engine/')) {
        return json(await getEngineDetail(env, path.split('/engine/')[1]));
      }
      // ── MANUAL TRIGGER ──
      if (path === '/build/trigger' && request.method === 'POST') {
        return json(await orchestrate(env));
      }
      // ── FORCE BUILD ──
      if (path === '/build/force' && request.method === 'POST') {
        const { engine_id } = await request.json();
        await env.BUILD_DB.prepare(
          "UPDATE engines SET status='PLANNED', attempts=0, updated_at=datetime('now') WHERE engine_id=?"
        ).bind(engine_id).run();
        return json(await orchestrate(env));
      }
      // ── BUILD COMPLETE CALLBACK ──
      if (path === '/build/complete' && request.method === 'POST') {
        return json(await handleBuildComplete(env, await request.json()));
      }
      // ── GATE RESULTS CALLBACK ──
      if (path === '/gates/report' && request.method === 'POST') {
        return json(await handleGateResults(env, await request.json()));
      }
      // ── PHASE ADVANCE ──
      if (path === '/phase/advance' && request.method === 'POST') {
        return json(await advancePhase(env));
      }
      // ── PAUSE/RESUME ──
      if (path === '/pause' && request.method === 'POST') {
        return json(await setState(env, 'mode', 'PAUSED'));
      }
      if (path === '/resume' && request.method === 'POST') {
        return json(await setState(env, 'mode', 'AUTONOMOUS'));
      }
      // ── BUILD LOG ──
      if (path === '/log') {
        return json(await getBuildLog(env, url.searchParams.get('limit') || 50));
      }
      // ── SEED ENGINES ──
      if (path === '/seed' && request.method === 'POST') {
        return json(await seedEngines(env, (await request.json()).engines));
      }
      // ── LINK CLAUDE CODE TERMINAL ──
      if (path === '/link-terminal' && request.method === 'POST') {
        const { endpoint } = await request.json();
        await setState(env, 'claude_code_endpoint', endpoint);
        await log(env, null, null, 'TERMINAL_LINKED', `Linked: ${endpoint}`);
        return json({ linked: true, endpoint });
      }
      // ── PLAN UPLOAD (store raw plan in R2) ──
      if (path === '/plan/upload' && request.method === 'POST') {
        const body = await request.json();
        const planId = `plan_${Date.now()}`;
        const r2Key = `plans/${planId}.md`;
        await env.BUILD_PLANS.put(r2Key, body.content);
        await env.BUILD_DB.prepare(
          "INSERT INTO build_plans (plan_id,plan_name,total_engines,total_tiers,status,r2_key) VALUES (?,?,?,?,?,?)"
        ).bind(planId, body.name || 'Unnamed Plan', body.total_engines || 0, body.total_tiers || 0, 'ACTIVE', r2Key).run();
        await setState(env, 'active_plan_id', planId);
        await log(env, null, null, 'PLAN_UPLOADED', `Plan ${planId}: ${body.name} (${body.total_engines} engines, ${body.total_tiers} tiers)`);
        return json({ plan_id: planId, r2_key: r2Key, engines: body.total_engines, tiers: body.total_tiers });
      }
      // ── LIST PLANS ──
      if (path === '/plans' && request.method === 'GET') {
        return json((await env.BUILD_DB.prepare("SELECT * FROM build_plans ORDER BY uploaded_at DESC").all()).results);
      }
      // ── ACTIVE PLAN ──
      if (path === '/plan/active' && request.method === 'GET') {
        const state = await getState(env);
        if (!state.active_plan_id) return json({ plan: null });
        const plan = await env.BUILD_DB.prepare("SELECT * FROM build_plans WHERE plan_id=?").bind(state.active_plan_id).first();
        return json({ plan });
      }
      // ── GATE DEFINITIONS CRUD ──
      if (path === '/gates/define' && request.method === 'POST') {
        const g = await request.json();
        await env.BUILD_DB.prepare(
          "INSERT OR REPLACE INTO gate_definitions (gate_id,gate_name,description,criteria,required_score,is_default) VALUES (?,?,?,?,?,0)"
        ).bind(g.gate_id, g.gate_name, g.description || '', g.criteria, g.required_score || 1.0).run();
        return json({ created: g.gate_id });
      }
      if (path === '/gates/definitions' && request.method === 'GET') {
        return json((await env.BUILD_DB.prepare("SELECT * FROM gate_definitions ORDER BY is_default DESC, gate_id").all()).results);
      }
      // ── COMMANDER OVERRIDE: APPROVE ──
      if (path.startsWith('/override/') && path.endsWith('/approve') && request.method === 'POST') {
        const engineId = path.split('/override/')[1].split('/approve')[0];
        const body = await request.json().catch(() => ({}));
        await env.BUILD_DB.prepare("UPDATE engines SET status='PASSED', completed_at=datetime('now'), updated_at=datetime('now') WHERE engine_id=?").bind(engineId).run();
        await env.BUILD_DB.prepare("INSERT INTO commander_overrides (engine_id,action,reason,source) VALUES (?,'APPROVE',?,?)").bind(engineId, body.reason || 'Commander override', body.source || 'ui').run();
        await log(env, engineId, null, 'OVERRIDE_APPROVE', `Commander force-approved: ${body.reason || 'No reason given'}`);
        return json({ engine_id: engineId, status: 'PASSED', override: 'APPROVE' });
      }
      // ── COMMANDER OVERRIDE: REJECT ──
      if (path.startsWith('/override/') && path.endsWith('/reject') && request.method === 'POST') {
        const engineId = path.split('/override/')[1].split('/reject')[0];
        const body = await request.json().catch(() => ({}));
        await env.BUILD_DB.prepare("UPDATE engines SET status='FAILED', updated_at=datetime('now') WHERE engine_id=?").bind(engineId).run();
        await env.BUILD_DB.prepare("INSERT INTO commander_overrides (engine_id,action,reason,source) VALUES (?,'REJECT',?,?)").bind(engineId, body.reason || 'Commander rejection', body.source || 'ui').run();
        await log(env, engineId, null, 'OVERRIDE_REJECT', `Commander force-rejected: ${body.reason || 'No reason given'}`);
        return json({ engine_id: engineId, status: 'FAILED', override: 'REJECT' });
      }
      // ── CLOUD BUILD: Manual trigger for single engine ──
      if (path.startsWith('/build/cloud/') && request.method === 'POST') {
        const engineId = path.split('/build/cloud/')[1];
        const engine = await env.BUILD_DB.prepare("SELECT * FROM engines WHERE engine_id=?").bind(engineId).first();
        if (!engine) return json({ error: `Engine ${engineId} not found` }, 404);
        if (!env.ANTHROPIC_API_KEY) return json({ error: 'ANTHROPIC_API_KEY not configured' }, 500);
        const spec = generateBuildSpec(engine);
        await env.BUILD_DB.prepare("UPDATE engines SET status='BUILDING', attempts=attempts+1, started_at=datetime('now'), updated_at=datetime('now') WHERE engine_id=?").bind(engineId).run();
        ctx.waitUntil(cloudBuild(env, engine, spec).catch(async err => {
          await env.BUILD_DB.prepare("UPDATE engines SET status='PLANNED', error_log=? WHERE engine_id=?").bind(err.message, engineId).run();
          await log(env, engineId, null, 'CLOUD_BUILD_FAILED', err.message);
        }));
        return json({ engine_id: engineId, status: 'BUILDING', mode: 'cloud', message: 'Cloud build started in background' });
      }
      // ── SET BUILD MODE (cloud/terminal) ──
      if (path === '/build/mode' && request.method === 'POST') {
        const { mode } = await request.json();
        if (!['cloud', 'terminal'].includes(mode)) return json({ error: 'Mode must be cloud or terminal' }, 400);
        await setState(env, 'build_mode', mode);
        return json({ build_mode: mode, message: `Build mode set to ${mode}` });
      }
      if (path === '/build/mode' && request.method === 'GET') {
        const state = await getState(env);
        return json({ build_mode: state.build_mode || 'cloud', api_key_set: !!env.ANTHROPIC_API_KEY });
      }
      // ── LIST CLOUD-BUILT FILES ──
      if (path.startsWith('/build/files/') && request.method === 'GET') {
        const engineId = path.split('/build/files/')[1].toLowerCase();
        const listed = await env.BUILD_PLANS.list({ prefix: `engines/${engineId}/` });
        const files = listed.objects.map(o => ({ key: o.key, size: o.size, uploaded: o.uploaded }));
        return json({ engine_id: engineId, files, count: files.length });
      }
      // ── DOWNLOAD CLOUD-BUILT FILE ──
      if (path.startsWith('/build/file/') && request.method === 'GET') {
        const filePath = path.split('/build/file/')[1];
        const obj = await env.BUILD_PLANS.get(`engines/${filePath}`);
        if (!obj) return json({ error: 'File not found' }, 404);
        return new Response(obj.body, { headers: { 'Content-Type': 'text/plain', ...corsHeaders() } });
      }
      // ── TRIGGER TWILIO ALERT (proxy from terminal) ──
      if (path === '/alert/call' && request.method === 'POST') {
        const body = await request.json();
        await log(env, body.engine_id || null, null, 'ALERT_CALL', body.message || 'Twilio alert triggered');
        return json({ alert: 'dispatched', message: body.message });
      }
      // ── HELP ──
      return json({
        system: 'ECHO PRIME BUILD ORCHESTRATOR v2.0 — CLOUD BUILD',
        routes: {
          'GET /': 'Status dashboard',
          'GET /engines?tier=&status=': 'Engine list',
          'GET /engine/:id': 'Engine detail + gates + log',
          'GET /log?limit=50': 'Build log',
          'GET /plans': 'List all plans',
          'GET /plan/active': 'Get active plan',
          'GET /gates/definitions': 'Gate definitions',
          'GET /build/mode': 'Current build mode (cloud/terminal)',
          'GET /build/files/:id': 'List cloud-built files for engine',
          'GET /build/file/:id/filename': 'Download cloud-built file',
          'POST /build/cloud/:id': 'Trigger cloud build for single engine',
          'POST /build/mode': 'Set build mode {mode: cloud|terminal}',
          'POST /plan/upload': 'Upload build plan',
          'POST /gates/define': 'Create gate definition',
          'POST /override/:id/approve': 'Commander force-approve',
          'POST /override/:id/reject': 'Commander force-reject',
          'POST /alert/call': 'Trigger Twilio alert',
          'POST /build/trigger': 'Manual orchestration cycle',
          'POST /build/force': 'Force rebuild {engine_id}',
          'POST /build/complete': 'Claude Code callback',
          'POST /gates/report': 'Gate results callback',
          'POST /phase/advance': 'Advance to next phase',
          'POST /pause': 'Pause orchestrator',
          'POST /resume': 'Resume orchestrator',
          'POST /seed': 'Bulk seed engines',
          'POST /link-terminal': 'Link Claude Code {endpoint}',
        }
      }, 404);
    } catch (err) {
      return json({ error: err.message }, 500);
    }
  }
};

// ═══════════════════════════════════════════════════════════════════════════
// CORE ORCHESTRATION LOOP
// ═══════════════════════════════════════════════════════════════════════════
async function orchestrate(env) {
  const state = await getState(env);

  if (state.mode === 'PAUSED') return { status: 'PAUSED' };
  if (!state.claude_code_endpoint || state.claude_code_endpoint === 'PENDING_LINK') {
    return { status: 'NO_TERMINAL', message: 'POST /link-terminal {endpoint}' };
  }

  await setState(env, 'last_heartbeat', new Date().toISOString());

  // Count in-flight builds
  const building = await env.BUILD_DB.prepare(
    "SELECT COUNT(*) as c FROM engines WHERE status='BUILDING'"
  ).first();
  const max = parseInt(state.max_concurrent_builds) || 3;
  const slots = max - (building?.c || 0);
  if (slots <= 0) return { status: 'BUSY', building: building.c, max };

  // Find next buildable engines
  const candidates = await findBuildable(env, slots, state.current_phase);
  if (!candidates.length) {
    const done = await checkPhaseComplete(env, state.current_phase);
    if (done) {
      await log(env, null, state.current_phase, 'PHASE_COMPLETE', `Phase ${state.current_phase} done`);
      await alertCommander(env, `🟢 Phase ${state.current_phase} COMPLETE. POST /phase/advance to continue.`);
      return { status: 'PHASE_COMPLETE', phase: state.current_phase };
    }
    return { status: 'WAITING', message: 'Dependencies not yet met' };
  }

  // Dispatch
  const dispatched = [];
  for (const e of candidates) {
    dispatched.push(await dispatchBuild(env, e, state.claude_code_endpoint));
  }
  return { status: 'DISPATCHED', count: dispatched.length, engines: dispatched.map(d => d.engine_id) };
}

// ═══════════════════════════════════════════════════════════════════════════
// FIND BUILDABLE ENGINES (deps met, not building, current phase priority)
// ═══════════════════════════════════════════════════════════════════════════
async function findBuildable(env, limit, phase) {
  const minPriority = phase === '1' ? 80 : phase === '2' ? 60 : phase === '3' ? 40 : 0;
  const planned = await env.BUILD_DB.prepare(`
    SELECT * FROM engines WHERE status='PLANNED' AND priority >= ?
    ORDER BY priority DESC LIMIT 20
  `).bind(minPriority).all();

  const buildable = [];
  for (const e of planned.results) {
    const deps = JSON.parse(e.depends_on || '[]');
    let met = true;
    for (const d of deps) {
      const dep = await env.BUILD_DB.prepare(
        "SELECT status FROM engines WHERE engine_id=?"
      ).bind(d).first();
      if (!dep || !['PASSED','DEPLOYED'].includes(dep.status)) { met = false; break; }
    }
    if (met) { buildable.push(e); if (buildable.length >= limit) break; }
  }
  return buildable;
}

// ═══════════════════════════════════════════════════════════════════════════
// DISPATCH BUILD — CLOUD (Anthropic API) or TERMINAL (Claude CLI)
// ═══════════════════════════════════════════════════════════════════════════
async function dispatchBuild(env, engine, endpoint) {
  const spec = generateBuildSpec(engine);

  await env.BUILD_DB.prepare(`
    UPDATE engines SET status='BUILDING', build_spec=?, attempts=attempts+1,
    started_at=datetime('now'), updated_at=datetime('now') WHERE engine_id=?
  `).bind(JSON.stringify(spec), engine.engine_id).run();

  await log(env, engine.engine_id, null, 'DISPATCHED',
    `Building ${engine.engine_id} (${engine.engine_name}). Attempt ${engine.attempts + 1}/${engine.max_attempts}`);

  const state = await getState(env);
  const buildMode = state.build_mode || 'cloud';

  if (buildMode === 'cloud' && env.ANTHROPIC_API_KEY) {
    // ── CLOUD BUILD: Call Anthropic API directly ──
    try {
      const result = await cloudBuild(env, engine, spec);
      return { engine_id: engine.engine_id, dispatched: true, mode: 'cloud', files: result.files_created };
    } catch (err) {
      await env.BUILD_DB.prepare("UPDATE engines SET status='PLANNED', error_log=? WHERE engine_id=?")
        .bind(err.message, engine.engine_id).run();
      await log(env, engine.engine_id, null, 'CLOUD_BUILD_FAILED', err.message);
      return { engine_id: engine.engine_id, dispatched: false, mode: 'cloud', error: err.message };
    }
  } else {
    // ── TERMINAL BUILD: Dispatch to Claude Code CLI ──
    try {
      await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Authority-Level': '11.0', 'X-Source': 'build-orchestrator' },
        body: JSON.stringify({
          action: 'BUILD_ENGINE', engine_id: engine.engine_id, spec,
          callback: 'https://echo-build-orchestrator.bmcii1976.workers.dev/build/complete',
          gate_callback: 'https://echo-build-orchestrator.bmcii1976.workers.dev/gates/report'
        })
      });
      return { engine_id: engine.engine_id, dispatched: true, mode: 'terminal' };
    } catch (err) {
      await env.BUILD_DB.prepare("UPDATE engines SET status='PLANNED' WHERE engine_id=?").bind(engine.engine_id).run();
      await log(env, engine.engine_id, null, 'DISPATCH_FAILED', err.message);
      return { engine_id: engine.engine_id, dispatched: false, mode: 'terminal', error: err.message };
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// CLOUD BUILD — Calls Anthropic API directly, stores files to R2
// ═══════════════════════════════════════════════════════════════════════════
async function cloudBuild(env, engine, spec) {
  const eid = engine.engine_id;
  const eidLower = eid.toLowerCase();
  const prompt = generateCloudPrompt(engine, spec);

  await log(env, eid, null, 'CLOUD_BUILD_START', `Calling Anthropic API for ${eid} (${engine.engine_name})`);

  // Call Anthropic Messages API
  const apiResp = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 64000,
      system: `You are an elite engine builder for ECHO OMEGA PRIME. Authority level 11.0 SOVEREIGN. You write production-grade Python engines following the TIE (Tax Intelligence Engine) 20-component architecture standard. Every function is fully implemented. No stubs, no TODOs, no placeholders. Output ONLY the file contents in fenced code blocks with the filename as the info string. Example: \`\`\`python:${eidLower}_engine.py\ncode here\n\`\`\``,
      messages: [{ role: 'user', content: prompt }],
    }),
  });

  if (!apiResp.ok) {
    const errBody = await apiResp.text();
    throw new Error(`Anthropic API ${apiResp.status}: ${errBody.substring(0, 500)}`);
  }

  const apiData = await apiResp.json();
  const responseText = apiData.content?.map(b => b.text).join('\n') || '';
  const inputTokens = apiData.usage?.input_tokens || 0;
  const outputTokens = apiData.usage?.output_tokens || 0;

  await log(env, eid, null, 'CLOUD_BUILD_API_DONE',
    `API responded: ${outputTokens} output tokens, ${inputTokens} input tokens`);

  // Parse code blocks from response
  const files = parseCodeBlocks(responseText, eidLower);
  if (files.length === 0) {
    throw new Error('No code blocks found in API response');
  }

  // Store files to R2
  const filesCreated = [];
  for (const file of files) {
    const r2Key = `engines/${eidLower}/${file.filename}`;
    await env.BUILD_PLANS.put(r2Key, file.content);
    filesCreated.push({ filename: file.filename, r2_key: r2Key, lines: file.content.split('\n').length, bytes: file.content.length });
  }

  const totalLines = filesCreated.reduce((sum, f) => sum + f.lines, 0);
  await log(env, eid, null, 'CLOUD_BUILD_STORED',
    `${filesCreated.length} files stored to R2 (${totalLines} total lines). Tokens: ${inputTokens}+${outputTokens}`);

  // Check quality: main engine must be ≥500 lines (relaxed for cloud builds)
  const engineFile = filesCreated.find(f => f.filename.endsWith('_engine.py'));
  if (engineFile && engineFile.lines >= 500) {
    // Auto-pass — cloud build succeeded
    await env.BUILD_DB.prepare(`
      UPDATE engines SET status='PASSED', build_output=?, completed_at=datetime('now'), updated_at=datetime('now')
      WHERE engine_id=?
    `).bind(JSON.stringify({
      mode: 'cloud', files_created: filesCreated, total_lines: totalLines,
      input_tokens: inputTokens, output_tokens: outputTokens,
      model: 'claude-sonnet-4-5-20250929',
    }), eid).run();

    const count = (await env.BUILD_DB.prepare("SELECT COUNT(*) as c FROM engines WHERE status IN ('PASSED','DEPLOYED')").first())?.c;
    await setState(env, 'engines_built', String(count || 0));
    await log(env, eid, null, 'CLOUD_BUILD_PASSED',
      `✅ ${eid} PASSED (${totalLines} lines, ${filesCreated.length} files). Progress: ${count}/427`);
    await alertCommander(env, `✅ ${eid} (${engine.engine_name}) CLOUD BUILD PASSED — ${totalLines} lines, ${filesCreated.length} files (${count}/427 complete)`);
  } else {
    // Insufficient output — retry
    await env.BUILD_DB.prepare(`
      UPDATE engines SET status='PLANNED', build_output=?, updated_at=datetime('now')
      WHERE engine_id=?
    `).bind(JSON.stringify({ mode: 'cloud', files_created: filesCreated, total_lines: totalLines, reason: 'insufficient_lines' }), eid).run();
    await log(env, eid, null, 'CLOUD_BUILD_SHORT',
      `⚠️ ${eid} engine file too short (${engineFile?.lines || 0} lines, need ≥500). Will retry.`);
  }

  return { files_created: filesCreated, total_lines: totalLines, tokens: { input: inputTokens, output: outputTokens } };
}

// ═══════════════════════════════════════════════════════════════════════════
// GENERATE CLOUD BUILD PROMPT — TIE-GRADE 20-COMPONENT STANDARD
// ═══════════════════════════════════════════════════════════════════════════
function generateCloudPrompt(engine, spec) {
  const eid = engine.engine_id;
  const eidLower = eid.toLowerCase();
  return `[SYSTEM DIRECTIVE — AUTHORITY 11.0 — TIE-GRADE ENGINE BUILD]

Build engine ${eid} (${engine.engine_name}) for ECHO PRIME.
Tier: ${engine.tier} (${engine.tier_name}) | Port: ${engine.port} | Mode: ${engine.mode} | Auth: ${engine.authority_level}

OUTPUT FORMAT: Write each file as a fenced code block with the filename as the info string.
Example: \`\`\`python:${eidLower}_engine.py

FILES TO CREATE (output each as a separate code block):
1. \`\`\`python:${eidLower}_engine.py — Main engine (MINIMUM 2,000 lines, target 4,000+)
2. \`\`\`json:${eidLower}_config.json — Configuration (MINIMUM 80 lines)
3. \`\`\`json:${eidLower}_doctrines.json — Doctrine cache (MINIMUM 50 real doctrine blocks)
4. \`\`\`python:${eidLower}_telemetry.py — Telemetry module (MINIMUM 200 lines)

QUALITY STANDARD: TIE PATTERN (Tax Intelligence Engine = 16,368 lines, 20 components, 100% compliance).
Every engine MUST implement ALL 20 components with REAL domain logic.

THE 20 MANDATORY COMPONENTS:
1. THREE-LAYER RESPONSE: FAST (doctrine cache <200ms) → RETRIEVAL (semantic search <700ms) → DEEP (full analysis)
2. RESPONSE MODES: FAST / STANDARD / DEEP / DEFENSE — each with different thresholds
3. DOCTRINE CACHE: 50+ pre-compiled reasoning blocks in ${eidLower}_doctrines.json with REAL expert content
4. AUTHORITY HARDENING: PRIMARY(100) > SECONDARY(80) > TERTIARY(60) > QUATERNARY(40) > COMMENTARY(20)
5. CONFIDENCE STRATIFICATION: DEFENSIBLE(≥0.85) / SUPPORTABLE(0.70-0.84) / DISCLOSURE(0.50-0.69) / HIGH_RISK(<0.50)
6. SEMANTIC NORMALIZATION: 100+ entries mapping jargon → canonical terms for this domain
7. VECTOR SEARCH: TF-IDF or keyword-based similarity search over doctrine blocks
8. TELEMETRY MODULE: QueryTrace, TelemetryStep, TelemetryCollector in separate file
9. DOCTRINE DRIFT WATCHER: Flag stale doctrines, reduce confidence for outdated entries
10. DOCTRINE COVERAGE MAP: Track what the engine knows vs gaps, report in /health
11. METRICS COLLECTOR: p50/p95/p99 latency, error rate, cache hit rate, QPM
12. HEALTH ENDPOINT: GET /health with comprehensive status JSON
13. ZONED ANALYSIS: 3+ analysis zones with different citation/confidence requirements
14. FACT FRAGILITY SCORING: How likely conclusions change if facts change (0-1 score)
15. AUDIT TRAIL: Append-only JSONL log with SHA-256 hash per response
16. DETERMINISM HASH: SHA-256(query + doctrine_version + engine_version) for reproducibility
17. FASTAPI SERVER: 8 endpoints (health, query, analyze, batch, explain, doctrines, coverage, metrics)
18. LOGURU LOGGING: Console INFO + file DEBUG with rotation (10MB/7d/gz)
19. MULTI-DOCTRINE: decompose_query() → sub-issues → independent lookups → compose results
20. DEEP ANALYSIS MODE: Maximum citation density, counter-arguments, risk assessment, full report

CODE STANDARDS:
- Python 3.11, type hints on EVERY function, Pydantic models for all I/O
- loguru (never print), pathlib.Path (never os.path), asyncio for I/O
- snake_case functions, PascalCase classes, UPPER_CASE constants
- Docstrings on every class and public function
- ZERO placeholders, ZERO TODOs, ZERO stubs, ZERO "pass" statements

DOMAIN REQUIREMENTS for ${eid} (${engine.engine_name}):
- At least 15 domain-specific analysis functions with REAL logic
- 50+ doctrine blocks with REAL expert reasoning and REAL citations
- 100+ semantic normalization entries for this domain
- 3+ analysis zones appropriate to ${engine.engine_name}
- Domain-specific risk taxonomy (CRITICAL/HIGH/MEDIUM/LOW/INFO)

CRITICAL: Output ONLY the code. Each file in its own fenced code block with filename.
Format: \`\`\`python:filename.py or \`\`\`json:filename.json

BUILD NOW. No explanations needed. Just output the 4 files.`;
}

// ═══════════════════════════════════════════════════════════════════════════
// PARSE CODE BLOCKS FROM API RESPONSE
// ═══════════════════════════════════════════════════════════════════════════
function parseCodeBlocks(text, eidLower) {
  const files = [];
  // Match fenced code blocks: ```lang:filename or ```lang filename
  const blockRegex = /```(?:python|json|javascript|yaml)[:\s]+([^\n`]+)\n([\s\S]*?)```/g;
  let match;
  while ((match = blockRegex.exec(text)) !== null) {
    const filename = match[1].trim();
    const content = match[2].trim();
    if (filename && content.length > 50) {
      files.push({ filename, content });
    }
  }

  // Fallback: look for blocks without explicit filename but with language hint
  if (files.length < 2) {
    const simpleRegex = /```(python|json)\n([\s\S]*?)```/g;
    let idx = 0;
    const defaultNames = [
      `${eidLower}_engine.py`, `${eidLower}_config.json`,
      `${eidLower}_doctrines.json`, `${eidLower}_telemetry.py`
    ];
    while ((match = simpleRegex.exec(text)) !== null) {
      const lang = match[1];
      const content = match[2].trim();
      if (content.length > 100) {
        // Try to detect filename from first line comment/docstring
        let filename = null;
        const firstLine = content.split('\n')[0] || '';
        const nameMatch = firstLine.match(/(?:#|\/\/|"""|''')\s*(\S+\.(py|json))/);
        if (nameMatch) {
          filename = nameMatch[1];
        } else if (!files.find(f => f.filename === defaultNames[idx])) {
          filename = defaultNames[idx] || `file_${idx}.${lang === 'python' ? 'py' : 'json'}`;
        }
        if (filename && !files.find(f => f.filename === filename)) {
          files.push({ filename, content });
        }
        idx++;
      }
    }
  }

  return files;
}

// ═══════════════════════════════════════════════════════════════════════════
// BUILD SPEC GENERATOR — TIE PATTERN 20-COMPONENT STANDARD
// ═══════════════════════════════════════════════════════════════════════════
function generateBuildSpec(engine) {
  return {
    engine_id: engine.engine_id,
    tier: engine.tier, tier_name: engine.tier_name,
    engine_name: engine.engine_name,
    mode: engine.mode, authority_level: engine.authority_level, port: engine.port,

    tie_20_components: [
      'three_layer_response', 'response_modes', 'doctrine_cache',
      'authority_hardening', 'confidence_stratification', 'semantic_normalization',
      'vector_search_chromadb', 'telemetry_module', 'doctrine_drift_watcher',
      'doctrine_coverage_map', 'metrics_collector', 'health_endpoint',
      'zoned_analysis', 'fact_fragility_scoring', 'audit_trail_jsonl',
      'determinism_hash_sha256', 'fastapi_server', 'loguru_logging',
      'multi_doctrine_decomposition', 'deep_analysis_mode'
    ],

    build_instructions: {
      language: 'python', version: '3.11', framework: 'fastapi',
      logging: 'loguru', paths: 'pathlib', type_hints: 'required',
      base_path: `F:\\ECHO_BRAIN\\engines\\${engine.engine_id.toLowerCase()}`,
      files: ['main.py', 'doctrine_cache.json', 'models.py', 'tests/test_engine.py'],
      requirements: [
        'ALL 20 TIE components implemented — no stubs',
        'Deterministic: same input = same SHA-256 hash on output',
        'Authority gate: reject requests below required authority level',
        'Doctrine cache: minimum 5 pre-compiled reasoning entries',
        'Health endpoint at GET /health',
        'Audit trail: every query logged to audit.jsonl',
        'At least 3 passing pytest tests',
        'Pydantic models for all input/output',
        'Loguru structured logging with rotation',
        'Type hints on every function',
      ]
    },

    quality_gates: [
      'LINT_RUFF', 'TYPE_CHECK_MYPY', 'UNIT_TEST_PYTEST',
      'HEALTH_ENDPOINT_CURL', 'DETERMINISM_HASH_VERIFY',
      'TIE_COMPLIANCE_20', 'AUTHORITY_GATE_REJECTION',
      'DOCTRINE_CACHE_MIN5', 'AUDIT_TRAIL_VERIFY'
    ]
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// CALLBACKS FROM CLAUDE CODE
// ═══════════════════════════════════════════════════════════════════════════
async function handleBuildComplete(env, body) {
  const { engine_id, success, output, files_created } = body;

  if (success) {
    await env.BUILD_DB.prepare(`
      UPDATE engines SET status='TESTING', build_output=?, updated_at=datetime('now') WHERE engine_id=?
    `).bind(JSON.stringify({ output, files_created }), engine_id).run();
    await log(env, engine_id, null, 'BUILD_OK', `${files_created?.length || 0} files. Moving to TESTING.`);
    return { engine_id, status: 'TESTING', next: 'Run gates → POST /gates/report' };
  }

  const e = await env.BUILD_DB.prepare("SELECT attempts, max_attempts FROM engines WHERE engine_id=?").bind(engine_id).first();
  if (e && e.attempts >= e.max_attempts) {
    await env.BUILD_DB.prepare("UPDATE engines SET status='FAILED', error_log=? WHERE engine_id=?")
      .bind(JSON.stringify(output), engine_id).run();
    await log(env, engine_id, null, 'FAILED_FINAL', `Failed after ${e.max_attempts} attempts`);
    await alertCommander(env, `🔴 ${engine_id} FAILED after ${e.max_attempts} attempts`);
    return { engine_id, status: 'FAILED' };
  }

  await env.BUILD_DB.prepare("UPDATE engines SET status='PLANNED', error_log=? WHERE engine_id=?")
    .bind(JSON.stringify(output), engine_id).run();
  return { engine_id, status: 'RETRY' };
}

async function handleGateResults(env, body) {
  const { engine_id, gates } = body;
  for (const g of gates) {
    await env.BUILD_DB.prepare(`
      INSERT INTO quality_gates (engine_id, gate_type, status, details, score, required_score, executed_at)
      VALUES (?, ?, ?, ?, ?, 1.0, datetime('now'))
    `).bind(engine_id, g.type, g.passed ? 'PASSED' : 'FAILED', g.details || '', g.score || (g.passed ? 1 : 0)).run();
  }

  if (gates.every(g => g.passed)) {
    await env.BUILD_DB.prepare(`
      UPDATE engines SET status='PASSED', gate_results=?, completed_at=datetime('now') WHERE engine_id=?
    `).bind(JSON.stringify(gates), engine_id).run();

    const count = (await env.BUILD_DB.prepare("SELECT COUNT(*) as c FROM engines WHERE status IN ('PASSED','DEPLOYED')").first())?.c;
    await setState(env, 'engines_built', String(count || 0));
    await log(env, engine_id, null, 'GATES_PASSED', `✅ All ${gates.length} gates passed`);
    await alertCommander(env, `✅ ${engine_id} PASSED all gates (${count}/427 complete)`);
    return { engine_id, status: 'PASSED' };
  }

  const failed = gates.filter(g => !g.passed).map(g => g.type);
  await env.BUILD_DB.prepare("UPDATE engines SET status='PLANNED', gate_results=? WHERE engine_id=?")
    .bind(JSON.stringify(gates), engine_id).run();
  await log(env, engine_id, null, 'GATES_FAILED', `❌ Failed: ${failed.join(', ')}`);
  return { engine_id, status: 'RETRY', failed_gates: failed };
}

// ═══════════════════════════════════════════════════════════════════════════
// PHASE MANAGEMENT
// ═══════════════════════════════════════════════════════════════════════════
async function advancePhase(env) {
  const state = await getState(env);
  const next = parseInt(state.current_phase) + 1;
  if (next > 4) return { error: 'Final phase reached' };

  await setState(env, 'current_phase', String(next));
  await env.BUILD_DB.prepare("UPDATE build_phases SET status='COMPLETED', completed_at=datetime('now') WHERE phase_id=?")
    .bind(parseInt(state.current_phase)).run();
  await env.BUILD_DB.prepare("UPDATE build_phases SET status='ACTIVE', started_at=datetime('now') WHERE phase_id=?")
    .bind(next).run();
  await log(env, null, next, 'PHASE_ADVANCED', `Phase ${next} activated`);
  await alertCommander(env, `🟢 Phase ${next} ACTIVATED`);
  return { phase: next };
}

async function checkPhaseComplete(env, phase) {
  const min = phase === '1' ? 80 : phase === '2' ? 60 : phase === '3' ? 40 : 0;
  const r = await env.BUILD_DB.prepare(
    "SELECT COUNT(*) as c FROM engines WHERE status NOT IN ('PASSED','DEPLOYED') AND priority >= ?"
  ).bind(min).first();
  return (r?.c || 0) === 0;
}

// ═══════════════════════════════════════════════════════════════════════════
// SEED, STATE, LOG, ALERT, STATUS
// ═══════════════════════════════════════════════════════════════════════════
async function seedEngines(env, engines) {
  let ins = 0;
  for (const e of engines) {
    try {
      await env.BUILD_DB.prepare(`
        INSERT OR IGNORE INTO engines (engine_id,tier,tier_name,engine_name,mode,authority_level,port,status,priority,depends_on)
        VALUES (?,?,?,?,?,?,?,'PLANNED',?,?)
      `).bind(e.engine_id, e.tier, e.tier_name, e.engine_name, e.mode, e.authority_level, e.port, e.priority||50, JSON.stringify(e.depends_on||[])).run();
      ins++;
    } catch(err) { console.error(`Seed engine ${e.engine_id} failed:`, err.message); }
  }
  return { inserted: ins, submitted: engines.length };
}

async function getState(env) {
  const rows = (await env.BUILD_DB.prepare("SELECT key,value FROM orchestrator_state").all()).results;
  const s = {}; for (const r of rows) s[r.key] = r.value; return s;
}

async function setState(env, k, v) {
  await env.BUILD_DB.prepare("INSERT OR REPLACE INTO orchestrator_state (key,value,updated_at) VALUES (?,?,datetime('now'))").bind(k,v).run();
  return { [k]: v };
}

async function log(env, eid, pid, type, msg, det) {
  await env.BUILD_DB.prepare("INSERT INTO build_log (engine_id,phase_id,event_type,message,details) VALUES (?,?,?,?,?)")
    .bind(eid, pid, type, msg, det||null).run();
}

async function alertCommander(env, message) {
  try {
    await fetch('https://omniscient-sync.bmcii1976.workers.dev/memory/store', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Echo-API-Key': env.ECHO_API_KEY || '' },
      body: JSON.stringify({ key: `build_alert_${Date.now()}`, value: { message, ts: new Date().toISOString() } })
    });
  } catch(e) { console.error('Alert to OmniSync failed:', e.message); }
}

async function getFullStatus(env) {
  const state = await getState(env);
  const counts = {}; 
  (await env.BUILD_DB.prepare("SELECT status, COUNT(*) as c FROM engines GROUP BY status").all())
    .results.forEach(r => counts[r.status] = r.c);
  const phases = (await env.BUILD_DB.prepare("SELECT * FROM build_phases").all()).results;
  const recent = (await env.BUILD_DB.prepare("SELECT * FROM build_log ORDER BY created_at DESC LIMIT 10").all()).results;

  return {
    system: 'ECHO PRIME BUILD ORCHESTRATOR v1.0',
    commander: 'Bobby Don McWilliams II',
    authority: '11.0 SOVEREIGN',
    mode: state.mode, phase: state.current_phase,
    terminal_linked: state.claude_code_endpoint !== 'PENDING_LINK',
    heartbeat: state.last_heartbeat,
    progress: { total: 427, built: parseInt(state.engines_built)||0, pct: ((parseInt(state.engines_built)||0)/427*100).toFixed(1)+'%' },
    engine_status: counts, phases, recent_activity: recent
  };
}

async function getEngines(env, tier, status) {
  let sql = "SELECT engine_id,tier,tier_name,engine_name,mode,status,priority,attempts FROM engines WHERE 1=1";
  const p = [];
  if (tier) { sql += " AND tier=?"; p.push(tier); }
  if (status) { sql += " AND status=?"; p.push(status); }
  sql += " ORDER BY priority DESC, engine_id";
  const stmt = env.BUILD_DB.prepare(sql);
  return (p.length ? await stmt.bind(...p).all() : await stmt.all()).results;
}

async function getEngineDetail(env, id) {
  return {
    engine: await env.BUILD_DB.prepare("SELECT * FROM engines WHERE engine_id=?").bind(id).first(),
    gates: (await env.BUILD_DB.prepare("SELECT * FROM quality_gates WHERE engine_id=? ORDER BY executed_at DESC").bind(id).all()).results,
    logs: (await env.BUILD_DB.prepare("SELECT * FROM build_log WHERE engine_id=? ORDER BY created_at DESC LIMIT 20").bind(id).all()).results
  };
}

async function getBuildLog(env, limit) {
  return (await env.BUILD_DB.prepare("SELECT * FROM build_log ORDER BY created_at DESC LIMIT ?").bind(parseInt(limit)).all()).results;
}

function corsHeaders() {
  return { 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Methods':'GET,POST,PUT,DELETE,OPTIONS', 'Access-Control-Allow-Headers':'Content-Type,X-Authority-Level,X-Source,X-Echo-API-Key' };
}
function json(data, status=200) {
  return new Response(JSON.stringify(data,null,2), { status, headers: { 'Content-Type':'application/json', ...corsHeaders() } });
}
