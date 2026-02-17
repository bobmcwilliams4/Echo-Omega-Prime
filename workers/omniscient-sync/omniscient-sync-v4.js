// ================================================================================
//     OMNISCIENT SYNC ULTIMATE v4.0 - UPGRADED CLOUDFLARE WORKER
// ================================================================================
//    AUTHORITY: 11.0 SOVEREIGN | Commander: Bobby Don McWilliams II
//    Features: D1 Database, KV Caching, Rate Limiting, Full API
//    Upgrade Date: 2026-02-05
// ================================================================================

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Session-ID, X-Echo-API-Key",
  "Content-Type": "application/json"
};

// ================================================================================
// AUTH MIDDLEWARE — X-Echo-API-Key required on all POST/PUT/DELETE routes
// ================================================================================
function authenticate(request, env) {
  const key = request.headers.get('X-Echo-API-Key');
  if (!env.ECHO_API_KEY) return null; // no key configured = allow (backward compat during rollout)
  if (key === env.ECHO_API_KEY) return null;
  return jsonResponse({ error: 'Unauthorized', message: 'Valid X-Echo-API-Key header required' }, 401);
}

// ================================================================================
// KV KEYS - For caching (reads are cheap, writes are limited)
// ================================================================================
const KV_KEYS = {
  SESSIONS: "omniscient:sessions",
  TODOS: "omniscient:todos",
  TODO_COUNTER: "omniscient:todo_counter",
  BROADCASTS: "omniscient:broadcasts",
  POLICIES: "omniscient:policies",
  MEMORIES: "omniscient:memories",
  CONTEXT: "omniscient:context"
};

// ================================================================================
// MASTER POLICIES - All 29 policies embedded
// ================================================================================
const MASTER_POLICIES = {
  DEBUG_LOGGING_POLICY: {
    id: "DEBUG_LOGGING_POLICY",
    name: "Debug and Logging Policy (5-Step Incident Protocol)",
    enforcement: "ABSOLUTE",
    steps: ["CHECK LOGS FIRST", "REPORT & DEBUG", "ENHANCE/UPGRADE/HARDEN", "REPORT WITH TIMESTAMPS", "TEST & MONITOR"]
  },
  APP_RELEASE_POLICY: {
    id: "APP_RELEASE_POLICY",
    name: "App Release Policy",
    enforcement: "MANDATORY",
    gates: ["SYNC", "BUILD", "TEST", "DOCUMENT", "FINAL_TEST", "FINAL_DOCUMENT", "SUBMIT"]
  },
  BLOODLINE_DIRECTIVE: {
    id: "BLOODLINE_DIRECTIVE",
    name: "Bloodline Prime Directive",
    enforcement: "ABSOLUTE",
    commander: "Bobby Don McWilliams II",
    authority: 11
  },
  NO_PLACEHOLDERS_POLICY: {
    id: "NO_PLACEHOLDERS_POLICY",
    enforcement: "ZERO_TOLERANCE",
    banned: ["TODO", "pass", "...", "NotImplementedError", "Mock()", "coming soon"]
  },
  SECURITY_POLICY: {
    id: "SECURITY_POLICY",
    enforcement: "MANDATORY",
    rules: ["No hardcoded secrets", "Use credential vault", "Run security validator"]
  },
  BUILD_STANDARDS: {
    id: "BUILD_STANDARDS",
    enforcement: "REQUIRED",
    python: ["Use loguru", "Use pathlib", "Type hints", "Python 3.11+", "FastAPI", "Async"]
  },
  INFRASTRUCTURE_POLICY: {
    id: "INFRASTRUCTURE_POLICY",
    approved: ["Firebase", "Cloud Run", "Vercel", "Cloudflare"],
    banned: ["Railway", "Supabase", "Auth0"]
  },
  PRE_BUILD_VALIDATION: {
    id: "PRE_BUILD_VALIDATION",
    enforcement: "MANDATORY",
    rule: "NEVER overwrite code without validation"
  },
  TIMEOUT_POLICY: {
    id: "TIMEOUT_POLICY",
    limits: { http: 30, file: 60, build: 300, deploy: 600 }
  },
  SHADOWGLASS_V8_POLICY: {
    id: "SHADOWGLASS_V8_POLICY",
    name: "ShadowGlass v8.1.1 — Mandatory Scraping & Document Intelligence Tool",
    enforcement: "MANDATORY",
    effective_date: "2026-02-08",
    worker_url: "https://shadowglass-v8-warpspeed.bmcii1976.workers.dev",
    rules: [
      "ALL county scraping MUST use ShadowGlass v8.1.1 Worker — no local scripts, no tunnel relay",
      "ALL PDFs stored in R2: ENCORE/TYLER/{county}/{type}/docs/{docId}.pdf",
      "ALL documents auto-flow through Document Intelligence Pipeline on upload",
      "Search metadata is PRIMARY entity source for scanned PDFs",
      "Browser Rendering OCR DISABLED for PDFs — headless Chrome cannot render PDFs",
      "NEVER send Accept-Encoding in Workers fetch() — causes double-encoding",
      "Native PDF text requires >70% printable ASCII ratio before trusting",
      "Supersedes ALL previous ShadowGlass versions and local ENCORE scraper"
    ],
    key_endpoints: {
      fetch_pdfs: "POST /warpspeed/fetch-pdfs {county, instrumentType, maxDocs}",
      pipeline_stats: "GET /pipeline/stats",
      pipeline_search: "GET /pipeline/search?county=X&grantor=Y&property=Z",
      scrape: "POST /scrape {county, instrumentType, dateFrom, dateTo}",
      dashboard: "GET /dashboard"
    },
    performance: { throughput: "32 docs/min", success_rate: "100%", avg_confidence: 0.56, cost: "$5-11/mo" },
    supersedes: ["v3 Omega", "v4.1 Cloud", "v5 Ultimate", "v6 Nexus", "v7 WarpSpeed", "v8.0", "v8.1.0", "ENCORE parallel_county_scraper.py"]
  }
};

// ================================================================================
// D1 DATABASE SCHEMA (Run once to initialize)
// ================================================================================
const D1_SCHEMA = `
CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY,
  instance_type TEXT,
  current_task TEXT,
  last_heartbeat TEXT,
  started_at TEXT,
  metadata TEXT
);

CREATE TABLE IF NOT EXISTS todos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'pending',
  priority TEXT DEFAULT 'medium',
  assigned_to TEXT,
  created_at TEXT,
  updated_at TEXT,
  metadata TEXT
);

CREATE TABLE IF NOT EXISTS memories (
  id TEXT PRIMARY KEY,
  key TEXT NOT NULL,
  value TEXT,
  category TEXT,
  created_at TEXT,
  expires_at TEXT
);

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_type TEXT,
  source TEXT,
  data TEXT,
  timestamp TEXT
);

CREATE TABLE IF NOT EXISTS broadcasts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message TEXT,
  priority TEXT,
  source TEXT,
  created_at TEXT,
  expires_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_sessions_type ON sessions(instance_type);
CREATE INDEX IF NOT EXISTS idx_todos_status ON todos(status);
CREATE INDEX IF NOT EXISTS idx_memories_key ON memories(key);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);

CREATE TABLE IF NOT EXISTS build_reports (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  action TEXT NOT NULL,
  target TEXT,
  detail TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS engine_status (
  id TEXT PRIMARY KEY,
  tier TEXT,
  name TEXT,
  status TEXT,
  note TEXT,
  loc INTEGER DEFAULT 0,
  mode TEXT,
  updated_by TEXT,
  updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS gate_status (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE,
  icon TEXT,
  status TEXT,
  detail TEXT,
  updated_by TEXT,
  updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS build_notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  time TEXT,
  tag TEXT,
  text TEXT,
  source TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_build_reports_action ON build_reports(action);
CREATE INDEX IF NOT EXISTS idx_engine_status_tier ON engine_status(tier);
CREATE INDEX IF NOT EXISTS idx_engine_status_status ON engine_status(status);
CREATE INDEX IF NOT EXISTS idx_gate_status_name ON gate_status(name);
CREATE INDEX IF NOT EXISTS idx_build_notes_tag ON build_notes(tag);
`;

// ================================================================================
// HELPER FUNCTIONS
// ================================================================================

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: CORS_HEADERS });
}

function errorResponse(message, status = 400) {
  return jsonResponse({ error: message, status }, status);
}

function generateId() {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

function now() {
  return new Date().toISOString();
}

// ================================================================================
// ROUTE HANDLERS
// ================================================================================

async function handleHealth(env) {
  return jsonResponse({
    status: "operational",
    version: "4.4.0",
    timestamp: now(),
    features: ["d1_database", "kv_cache", "rate_limiting", "cors", "build_tracking", "engine_status", "gate_tracking", "build_notes", "dynamic_policies", "r2_swarm", "r2_memory", "r2_vault", "r2_law", "r2_tax", "r2_knowledge"],
    r2_buckets: {
      swarm: { binding: "R2_SWARM", bucket: "echo-swarm-brain", connected: !!env.R2_SWARM },
      memory: { binding: "R2_MEMORY", bucket: "echo-prime-memory", connected: !!env.R2_MEMORY },
      vault: { binding: "R2_VAULT", bucket: "echo-prime-master-vault", connected: !!env.R2_VAULT },
      law: { binding: "R2_LAW", bucket: "echo-prime-law-corpus", connected: !!env.R2_LAW },
      tax: { binding: "R2_TAX", bucket: "echo-prime-tax-knowledge", connected: !!env.R2_TAX },
      knowledge: { binding: "R2_KNOWLEDGE", bucket: "echo-prime-knowledge", connected: !!env.R2_KNOWLEDGE },
    },
    authority: "11.0 SOVEREIGN"
  });
}

async function handlePolicies(env) {
  // Merge hardcoded MASTER_POLICIES with any KV-stored dynamic policies
  let dynamicPolicies = {};
  if (env.OMNISCIENT_DATA) {
    try {
      const kvData = await env.OMNISCIENT_DATA.get(KV_KEYS.POLICIES, "json");
      if (kvData) dynamicPolicies = kvData;
    } catch (e) { /* KV read failed, use hardcoded only */ }
  }
  const merged = { ...MASTER_POLICIES, ...dynamicPolicies };
  return jsonResponse({
    policies: merged,
    count: Object.keys(merged).length,
    hardcoded: Object.keys(MASTER_POLICIES).length,
    dynamic: Object.keys(dynamicPolicies).length,
    enforcement_levels: ["ABSOLUTE", "MANDATORY", "REQUIRED", "ZERO_TOLERANCE"]
  });
}

async function storePolicy(env, body) {
  if (!body.id || !body.name) {
    return errorResponse("Policy requires 'id' and 'name' fields");
  }
  // Read existing dynamic policies from KV
  let dynamicPolicies = {};
  if (env.OMNISCIENT_DATA) {
    try {
      const kvData = await env.OMNISCIENT_DATA.get(KV_KEYS.POLICIES, "json");
      if (kvData) dynamicPolicies = kvData;
    } catch (e) { /* fresh start */ }
  }
  // Add/update the policy
  dynamicPolicies[body.id] = { ...body, stored_at: now() };
  await env.OMNISCIENT_DATA.put(KV_KEYS.POLICIES, JSON.stringify(dynamicPolicies));
  // Also log to D1 events
  if (env.DB) {
    await env.DB.prepare("INSERT INTO events (event_type, source, data, timestamp) VALUES (?, ?, ?, ?)")
      .bind("policy_stored", body.id, JSON.stringify(body), now()).run();
  }
  return jsonResponse({
    success: true,
    policy_id: body.id,
    message: `Policy '${body.id}' stored in KV`,
    total_dynamic: Object.keys(dynamicPolicies).length
  });
}

async function deletePolicy(env, policyId) {
  // Only delete from dynamic KV store — hardcoded policies cannot be removed
  if (MASTER_POLICIES[policyId]) {
    return errorResponse(`Cannot delete hardcoded policy '${policyId}'. Use source code.`, 403);
  }
  let dynamicPolicies = {};
  if (env.OMNISCIENT_DATA) {
    try {
      const kvData = await env.OMNISCIENT_DATA.get(KV_KEYS.POLICIES, "json");
      if (kvData) dynamicPolicies = kvData;
    } catch (e) { /* empty */ }
  }
  if (!dynamicPolicies[policyId]) {
    return errorResponse(`Dynamic policy '${policyId}' not found`, 404);
  }
  delete dynamicPolicies[policyId];
  await env.OMNISCIENT_DATA.put(KV_KEYS.POLICIES, JSON.stringify(dynamicPolicies));
  return jsonResponse({ success: true, deleted: policyId });
}

// ================================================================================
// SESSIONS - Using D1 for persistence, KV for quick cache
// ================================================================================

async function getSessions(env) {
  try {
    // Try D1 first
    if (env.DB) {
      const result = await env.DB.prepare("SELECT * FROM sessions ORDER BY last_heartbeat DESC LIMIT 100").all();
      return jsonResponse({ sessions: result.results || [], source: "d1" });
    }
    // Fallback to KV
    const cached = await env.OMNISCIENT_DATA?.get(KV_KEYS.SESSIONS);
    return jsonResponse({ sessions: cached ? JSON.parse(cached) : [], source: "kv" });
  } catch (e) {
    return jsonResponse({ sessions: [], error: e.message });
  }
}

async function registerSession(env, body) {
  const session = {
    id: generateId(),
    instance_type: body.instance_type || "unknown",
    current_task: body.current_task || "Session started",
    last_heartbeat: now(),
    started_at: now(),
    metadata: JSON.stringify(body.metadata || {})
  };

  try {
    if (env.DB) {
      await env.DB.prepare(`
        INSERT INTO sessions (id, instance_type, current_task, last_heartbeat, started_at, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
      `).bind(session.id, session.instance_type, session.current_task, session.last_heartbeat, session.started_at, session.metadata).run();
    }
    return jsonResponse({ success: true, session_id: session.id, message: "Session registered" });
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

async function heartbeat(env, body) {
  const { session_id, current_task } = body;
  if (!session_id) return errorResponse("session_id required");

  try {
    if (env.DB) {
      await env.DB.prepare(`
        UPDATE sessions SET last_heartbeat = ?, current_task = ? WHERE id = ?
      `).bind(now(), current_task || "", session_id).run();
    }
    return jsonResponse({ success: true, timestamp: now() });
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

// ================================================================================
// TODOS - Full CRUD with D1
// ================================================================================

async function getTodos(env) {
  try {
    if (env.DB) {
      const result = await env.DB.prepare("SELECT * FROM todos ORDER BY id DESC LIMIT 200").all();
      return jsonResponse({ todos: result.results || [], source: "d1" });
    }
    const cached = await env.OMNISCIENT_DATA?.get(KV_KEYS.TODOS);
    return jsonResponse({ todos: cached ? JSON.parse(cached) : [], source: "kv" });
  } catch (e) {
    return jsonResponse({ todos: [], error: e.message });
  }
}

async function createTodo(env, body) {
  const todo = {
    title: body.title || "Untitled",
    description: body.description || "",
    status: body.status || "pending",
    priority: body.priority || "medium",
    assigned_to: body.assigned_to || null,
    created_at: now(),
    updated_at: now(),
    metadata: JSON.stringify(body.metadata || {})
  };

  try {
    if (env.DB) {
      const result = await env.DB.prepare(`
        INSERT INTO todos (title, description, status, priority, assigned_to, created_at, updated_at, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      `).bind(todo.title, todo.description, todo.status, todo.priority, todo.assigned_to, todo.created_at, todo.updated_at, todo.metadata).run();
      return jsonResponse({ success: true, todo_id: result.meta?.last_row_id, message: "Todo created" });
    }
    return errorResponse("D1 database not available");
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

async function updateTodo(env, id, body) {
  try {
    if (env.DB) {
      await env.DB.prepare(`
        UPDATE todos SET status = ?, updated_at = ? WHERE id = ?
      `).bind(body.status || "pending", now(), id).run();
      return jsonResponse({ success: true, message: "Todo updated" });
    }
    return errorResponse("D1 database not available");
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

// ================================================================================
// MEMORIES - Key-value storage with expiration
// ================================================================================

async function getMemory(env, key) {
  try {
    if (env.DB) {
      const result = await env.DB.prepare("SELECT * FROM memories WHERE key = ?").bind(key).first();
      if (result) {
        return jsonResponse({ found: true, key, value: JSON.parse(result.value || "{}"), created_at: result.created_at });
      }
    }
    return jsonResponse({ found: false, key });
  } catch (e) {
    return jsonResponse({ found: false, error: e.message });
  }
}

async function setMemory(env, body) {
  const { key, value, category, expires_in } = body;
  if (!key) return errorResponse("key required");

  const memory = {
    id: generateId(),
    key,
    value: JSON.stringify(value || {}),
    category: category || "general",
    created_at: now(),
    expires_at: expires_in ? new Date(Date.now() + expires_in * 1000).toISOString() : null
  };

  try {
    if (env.DB) {
      await env.DB.prepare(`
        INSERT OR REPLACE INTO memories (id, key, value, category, created_at, expires_at)
        VALUES (?, ?, ?, ?, ?, ?)
      `).bind(memory.id, memory.key, memory.value, memory.category, memory.created_at, memory.expires_at).run();
      return jsonResponse({ success: true, key, message: "Memory stored" });
    }
    return errorResponse("D1 database not available");
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

// ================================================================================
// BROADCASTS - Cross-instance messaging
// ================================================================================

async function getBroadcasts(env) {
  try {
    if (env.DB) {
      const result = await env.DB.prepare(`
        SELECT * FROM broadcasts
        WHERE expires_at IS NULL OR expires_at > datetime('now')
        ORDER BY id DESC LIMIT 50
      `).all();
      return jsonResponse({ broadcasts: result.results || [] });
    }
    return jsonResponse({ broadcasts: [] });
  } catch (e) {
    return jsonResponse({ broadcasts: [], error: e.message });
  }
}

async function createBroadcast(env, body) {
  const broadcast = {
    message: body.message || "",
    priority: body.priority || "normal",
    source: body.source || "unknown",
    created_at: now(),
    expires_at: body.expires_in ? new Date(Date.now() + body.expires_in * 1000).toISOString() : null
  };

  try {
    if (env.DB) {
      await env.DB.prepare(`
        INSERT INTO broadcasts (message, priority, source, created_at, expires_at)
        VALUES (?, ?, ?, ?, ?)
      `).bind(broadcast.message, broadcast.priority, broadcast.source, broadcast.created_at, broadcast.expires_at).run();
      return jsonResponse({ success: true, message: "Broadcast sent" });
    }
    return errorResponse("D1 database not available");
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

// ================================================================================
// CONTEXT - Load/Store session context
// ================================================================================

async function loadContext(env, workspace) {
  try {
    // Get recent sessions
    const sessions = env.DB ?
      (await env.DB.prepare("SELECT * FROM sessions ORDER BY last_heartbeat DESC LIMIT 10").all()).results : [];

    // Get active todos
    const todos = env.DB ?
      (await env.DB.prepare("SELECT * FROM todos WHERE status != 'completed' LIMIT 20").all()).results : [];

    // Get recent broadcasts
    const broadcasts = env.DB ?
      (await env.DB.prepare("SELECT * FROM broadcasts ORDER BY id DESC LIMIT 10").all()).results : [];

    return jsonResponse({
      workspace: workspace || "ECHO_OMEGA_PRIME",
      context: {
        active_sessions: sessions.length,
        pending_todos: todos.filter(t => t.status === "pending").length,
        in_progress_todos: todos.filter(t => t.status === "in_progress").length,
        recent_broadcasts: broadcasts.length
      },
      sessions,
      todos,
      broadcasts,
      policies: MASTER_POLICIES,
      loaded_at: now()
    });
  } catch (e) {
    return jsonResponse({ error: e.message, policies: MASTER_POLICIES });
  }
}

async function storeContext(env, body) {
  const { session_id, instance, summary, key_files } = body;

  try {
    if (env.DB) {
      await env.DB.prepare(`
        INSERT INTO events (event_type, source, data, timestamp)
        VALUES (?, ?, ?, ?)
      `).bind("context_store", instance || session_id, JSON.stringify({ summary, key_files }), now()).run();
    }
    return jsonResponse({ success: true, message: "Context stored" });
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

// ================================================================================
// BUILD STATUS - Engine tracking, gates, notes, reports
// ================================================================================

const STATUS_ORDER = { P: 0, B: 1, X: 2 };

async function buildReport(env, body) {
  const { source, action, target, detail } = body;
  if (!source || !action) return errorResponse("source and action required");

  try {
    if (env.DB) {
      await env.DB.prepare(`
        INSERT INTO build_reports (source, action, target, detail, created_at)
        VALUES (?, ?, ?, ?, ?)
      `).bind(source, action, target || null, typeof detail === "object" ? JSON.stringify(detail) : (detail || null), now()).run();

      // Invalidate dashboard cache
      if (env.OMNISCIENT_DATA) {
        await env.OMNISCIENT_DATA.delete("build:dashboard_cache");
      }
    }
    return jsonResponse({ success: true, message: "Build report logged" });
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

async function buildStatus(env) {
  try {
    if (!env.DB) return errorResponse("D1 not available");

    const engines = (await env.DB.prepare("SELECT * FROM engine_status ORDER BY id").all()).results || [];
    const gates = (await env.DB.prepare("SELECT * FROM gate_status ORDER BY id").all()).results || [];
    const recentReports = (await env.DB.prepare("SELECT * FROM build_reports ORDER BY id DESC LIMIT 20").all()).results || [];

    const total = engines.length;
    const prod = engines.filter(e => e.status === "X").length;
    const built = engines.filter(e => e.status === "B").length;
    const planned = engines.filter(e => e.status === "P").length;
    const gatesPassed = gates.filter(g => g.status === "PASS").length;
    const gatesFailed = gates.filter(g => g.status === "FAIL").length;

    return jsonResponse({
      summary: { total_engines: total, production: prod, built, planned, gates_passed: gatesPassed, gates_failed: gatesFailed, gates_total: gates.length },
      engines, gates, recent_reports: recentReports, timestamp: now()
    });
  } catch (e) {
    return jsonResponse({ error: e.message }, 500);
  }
}

async function buildReports(env, url) {
  try {
    if (!env.DB) return errorResponse("D1 not available");
    const limit = parseInt(url.searchParams.get("limit") || "100");
    const action = url.searchParams.get("action");

    let query = "SELECT * FROM build_reports";
    const binds = [];
    if (action) { query += " WHERE action = ?"; binds.push(action); }
    query += " ORDER BY id DESC LIMIT ?";
    binds.push(Math.min(limit, 500));

    const stmt = env.DB.prepare(query);
    const result = await (binds.length === 1 ? stmt.bind(binds[0]) : stmt.bind(...binds)).all();
    return jsonResponse({ reports: result.results || [], count: (result.results || []).length });
  } catch (e) {
    return jsonResponse({ error: e.message }, 500);
  }
}

async function engineUpdate(env, body) {
  const { id, tier, name, status, note, loc, mode, updated_by } = body;
  if (!id) return errorResponse("engine id required");
  if (status && !["P", "B", "X"].includes(status)) return errorResponse("status must be P, B, or X");

  try {
    if (!env.DB) return errorResponse("D1 not available");

    // Prevent backward status changes
    const existing = await env.DB.prepare("SELECT status FROM engine_status WHERE id = ?").bind(id).first();
    if (existing && status && STATUS_ORDER[status] < STATUS_ORDER[existing.status]) {
      return errorResponse(`Cannot regress engine ${id} from ${existing.status} to ${status}`);
    }

    await env.DB.prepare(`
      INSERT INTO engine_status (id, tier, name, status, note, loc, mode, updated_by, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      ON CONFLICT(id) DO UPDATE SET
        tier = COALESCE(excluded.tier, engine_status.tier),
        name = COALESCE(excluded.name, engine_status.name),
        status = COALESCE(excluded.status, engine_status.status),
        note = COALESCE(excluded.note, engine_status.note),
        loc = COALESCE(excluded.loc, engine_status.loc),
        mode = COALESCE(excluded.mode, engine_status.mode),
        updated_by = excluded.updated_by,
        updated_at = excluded.updated_at
    `).bind(id, tier || null, name || null, status || "P", note || null, loc || 0, mode || null, updated_by || "unknown", now()).run();

    // Log to build_reports
    await env.DB.prepare(`
      INSERT INTO build_reports (source, action, target, detail, created_at)
      VALUES (?, ?, ?, ?, ?)
    `).bind(updated_by || "unknown", "engine_update", id, JSON.stringify({ status, note, loc }), now()).run();

    // Invalidate cache
    if (env.OMNISCIENT_DATA) {
      await env.OMNISCIENT_DATA.delete("build:dashboard_cache");
    }

    return jsonResponse({ success: true, message: `Engine ${id} updated to ${status}` });
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

async function gateUpdate(env, body) {
  const { name, icon, status, detail, updated_by } = body;
  if (!name) return errorResponse("gate name required");
  if (status && !["PASS", "FAIL", "PENDING"].includes(status)) return errorResponse("status must be PASS, FAIL, or PENDING");

  try {
    if (!env.DB) return errorResponse("D1 not available");

    await env.DB.prepare(`
      INSERT INTO gate_status (name, icon, status, detail, updated_by, updated_at)
      VALUES (?, ?, ?, ?, ?, ?)
      ON CONFLICT(name) DO UPDATE SET
        icon = COALESCE(excluded.icon, gate_status.icon),
        status = COALESCE(excluded.status, gate_status.status),
        detail = COALESCE(excluded.detail, gate_status.detail),
        updated_by = excluded.updated_by,
        updated_at = excluded.updated_at
    `).bind(name, icon || null, status || "PENDING", detail || null, updated_by || "unknown", now()).run();

    // Log
    await env.DB.prepare(`
      INSERT INTO build_reports (source, action, target, detail, created_at)
      VALUES (?, ?, ?, ?, ?)
    `).bind(updated_by || "unknown", "gate_update", name, JSON.stringify({ status, detail }), now()).run();

    if (env.OMNISCIENT_DATA) {
      await env.OMNISCIENT_DATA.delete("build:dashboard_cache");
    }

    return jsonResponse({ success: true, message: `Gate '${name}' updated to ${status}` });
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

async function buildNote(env, body) {
  const { tag, text, source, time } = body;
  if (!text) return errorResponse("text required");

  try {
    if (!env.DB) return errorResponse("D1 not available");

    await env.DB.prepare(`
      INSERT INTO build_notes (time, tag, text, source, created_at)
      VALUES (?, ?, ?, ?, ?)
    `).bind(time || now(), tag || "GENERAL", text, source || "unknown", now()).run();

    if (env.OMNISCIENT_DATA) {
      await env.OMNISCIENT_DATA.delete("build:dashboard_cache");
    }

    return jsonResponse({ success: true, message: "Build note added" });
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

async function dashboardData(env) {
  try {
    // Check KV cache first (30s TTL)
    if (env.OMNISCIENT_DATA) {
      const cached = await env.OMNISCIENT_DATA.get("build:dashboard_cache");
      if (cached) {
        return jsonResponse(JSON.parse(cached));
      }
    }

    if (!env.DB) return errorResponse("D1 not available");

    const engines = (await env.DB.prepare("SELECT * FROM engine_status ORDER BY id").all()).results || [];
    const gates = (await env.DB.prepare("SELECT * FROM gate_status ORDER BY id").all()).results || [];
    const notes = (await env.DB.prepare("SELECT * FROM build_notes ORDER BY id DESC LIMIT 50").all()).results || [];
    const reports = (await env.DB.prepare("SELECT * FROM build_reports ORDER BY id DESC LIMIT 50").all()).results || [];
    const sessions = (await env.DB.prepare("SELECT * FROM sessions ORDER BY last_heartbeat DESC LIMIT 20").all()).results || [];

    const total = engines.length;
    const prod = engines.filter(e => e.status === "X").length;
    const built = engines.filter(e => e.status === "B").length;
    const planned = engines.filter(e => e.status === "P").length;
    const totalLoc = engines.reduce((s, e) => s + (e.loc || 0), 0);

    // Group engines by tier
    const tiers = {};
    for (const e of engines) {
      if (!tiers[e.tier]) tiers[e.tier] = [];
      tiers[e.tier].push(e);
    }

    const data = {
      summary: {
        total_engines: total, production: prod, built, planned,
        total_loc: totalLoc,
        gates_passed: gates.filter(g => g.status === "PASS").length,
        gates_failed: gates.filter(g => g.status === "FAIL").length,
        gates_pending: gates.filter(g => g.status === "PENDING").length,
        gates_total: gates.length,
        active_sessions: sessions.filter(s => {
          const hb = new Date(s.last_heartbeat);
          return (Date.now() - hb.getTime()) < 300000; // 5 min
        }).length
      },
      engines, tiers, gates, notes, reports, sessions,
      generated_at: now()
    };

    // Cache in KV for 30s
    if (env.OMNISCIENT_DATA) {
      await env.OMNISCIENT_DATA.put("build:dashboard_cache", JSON.stringify(data), { expirationTtl: 60 });
    }

    return jsonResponse(data);
  } catch (e) {
    return jsonResponse({ error: e.message }, 500);
  }
}

async function bulkSeedEngines(env, body) {
  const { engines } = body;
  if (!engines || !Array.isArray(engines)) return errorResponse("engines array required");

  try {
    if (!env.DB) return errorResponse("D1 not available");

    let inserted = 0;
    for (const e of engines) {
      await env.DB.prepare(`
        INSERT INTO engine_status (id, tier, name, status, note, loc, mode, updated_by, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
          tier = excluded.tier, name = excluded.name, status = excluded.status,
          note = excluded.note, loc = excluded.loc, mode = excluded.mode,
          updated_by = excluded.updated_by, updated_at = excluded.updated_at
      `).bind(e.id, e.tier || null, e.name || null, e.status || "P", e.note || null, e.loc || 0, e.mode || null, "seed", now()).run();
      inserted++;
    }

    if (env.OMNISCIENT_DATA) {
      await env.OMNISCIENT_DATA.delete("build:dashboard_cache");
    }

    return jsonResponse({ success: true, inserted, message: `${inserted} engines seeded` });
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

async function bulkSeedGates(env, body) {
  const { gates } = body;
  if (!gates || !Array.isArray(gates)) return errorResponse("gates array required");

  try {
    if (!env.DB) return errorResponse("D1 not available");

    let inserted = 0;
    for (const g of gates) {
      await env.DB.prepare(`
        INSERT INTO gate_status (name, icon, status, detail, updated_by, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
          icon = excluded.icon, status = excluded.status, detail = excluded.detail,
          updated_by = excluded.updated_by, updated_at = excluded.updated_at
      `).bind(g.name, g.icon || null, g.status || "PENDING", g.detail || null, "seed", now()).run();
      inserted++;
    }

    if (env.OMNISCIENT_DATA) {
      await env.OMNISCIENT_DATA.delete("build:dashboard_cache");
    }

    return jsonResponse({ success: true, inserted, message: `${inserted} gates seeded` });
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

async function bulkSeedNotes(env, body) {
  const { notes } = body;
  if (!notes || !Array.isArray(notes)) return errorResponse("notes array required");

  try {
    if (!env.DB) return errorResponse("D1 not available");

    let inserted = 0;
    for (const n of notes) {
      await env.DB.prepare(`
        INSERT INTO build_notes (time, tag, text, source, created_at)
        VALUES (?, ?, ?, ?, ?)
      `).bind(n.time || now(), n.tag || "GENERAL", n.text, n.source || "seed", now()).run();
      inserted++;
    }

    if (env.OMNISCIENT_DATA) {
      await env.OMNISCIENT_DATA.delete("build:dashboard_cache");
    }

    return jsonResponse({ success: true, inserted, message: `${inserted} notes seeded` });
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

// ================================================================================
// R2 STORAGE — SWARM BRAIN, MEMORY SYSTEM, VAULT
// ================================================================================

function getR2Bucket(env, zone) {
  const map = { swarm: env.R2_SWARM, memory: env.R2_MEMORY, vault: env.R2_VAULT, law: env.R2_LAW, tax: env.R2_TAX, knowledge: env.R2_KNOWLEDGE };
  return map[zone] || null;
}

async function r2Store(env, zone, body) {
  const bucket = getR2Bucket(env, zone);
  if (!bucket) return errorResponse(`R2 bucket '${zone}' not configured`, 503);
  const { key, data, metadata } = body;
  if (!key || !data) return errorResponse("key and data required");

  const content = typeof data === 'string' ? data : JSON.stringify(data);
  await bucket.put(key, content, {
    httpMetadata: { contentType: 'application/json' },
    customMetadata: { zone, stored_at: now(), ...(metadata || {}) },
  });

  // Log to D1 events
  if (env.DB) {
    await env.DB.prepare("INSERT INTO events (event_type, source, data, timestamp) VALUES (?, ?, ?, ?)")
      .bind(`r2_store:${zone}`, key, JSON.stringify({ zone, size: content.length, metadata }), now()).run();
  }

  return jsonResponse({ success: true, zone, key, size: content.length });
}

async function r2Get(env, zone, key) {
  const bucket = getR2Bucket(env, zone);
  if (!bucket) return errorResponse(`R2 bucket '${zone}' not configured`, 503);

  const obj = await bucket.get(key);
  if (!obj) return jsonResponse({ success: false, error: 'Not found', zone, key }, 404);

  const text = await obj.text();
  let data;
  try { data = JSON.parse(text); } catch { data = text; }

  return jsonResponse({
    success: true, zone, key, data,
    metadata: obj.customMetadata || {},
    size: obj.size,
    etag: obj.etag,
    uploaded: obj.uploaded?.toISOString(),
  });
}

async function r2Delete(env, zone, key) {
  const bucket = getR2Bucket(env, zone);
  if (!bucket) return errorResponse(`R2 bucket '${zone}' not configured`, 503);

  await bucket.delete(key);
  return jsonResponse({ success: true, zone, key, deleted: true });
}

async function r2List(env, zone, prefix, limit) {
  const bucket = getR2Bucket(env, zone);
  if (!bucket) return errorResponse(`R2 bucket '${zone}' not configured`, 503);

  const listed = await bucket.list({ prefix: prefix || undefined, limit: Math.min(limit || 100, 1000) });
  const objects = (listed.objects || []).map(o => ({
    key: o.key, size: o.size, etag: o.etag,
    uploaded: o.uploaded?.toISOString(),
    metadata: o.customMetadata || {},
  }));

  return jsonResponse({
    success: true, zone, prefix: prefix || null,
    count: objects.length, truncated: listed.truncated,
    cursor: listed.truncated ? listed.cursor : null,
    objects,
  });
}

async function r2Stats(env) {
  const zones = ['swarm', 'memory', 'vault'];
  const stats = {};

  for (const zone of zones) {
    const bucket = getR2Bucket(env, zone);
    if (!bucket) { stats[zone] = { connected: false }; continue; }

    const listed = await bucket.list({ limit: 1000 });
    const totalSize = (listed.objects || []).reduce((s, o) => s + (o.size || 0), 0);
    stats[zone] = {
      connected: true,
      objects: listed.objects?.length || 0,
      truncated: listed.truncated,
      totalSize,
      totalSizeMB: Math.round(totalSize / 1024 / 1024 * 100) / 100,
    };
  }

  return jsonResponse({ success: true, r2: stats, timestamp: now() });
}

// Cross-zone sync: copy data from one zone to another
async function r2CrossSync(env, body) {
  const { fromZone, toZone, prefix, keys } = body;
  const from = getR2Bucket(env, fromZone);
  const to = getR2Bucket(env, toZone);
  if (!from || !to) return errorResponse("Both source and target zones must be configured");

  let synced = 0, failed = 0;
  const targetKeys = keys || [];

  if (!keys && prefix) {
    const listed = await from.list({ prefix, limit: 500 });
    for (const obj of listed.objects || []) {
      targetKeys.push(obj.key);
    }
  }

  for (const key of targetKeys) {
    try {
      const obj = await from.get(key);
      if (obj) {
        const data = await obj.arrayBuffer();
        await to.put(key, data, {
          httpMetadata: obj.httpMetadata,
          customMetadata: { ...obj.customMetadata, synced_from: fromZone, synced_at: now() },
        });
        synced++;
      }
    } catch { failed++; }
  }

  return jsonResponse({ success: true, fromZone, toZone, synced, failed, total: targetKeys.length });
}

// Snapshot: take a full state snapshot and store in the zone
async function r2Snapshot(env, zone, body) {
  const bucket = getR2Bucket(env, zone);
  if (!bucket) return errorResponse(`R2 bucket '${zone}' not configured`, 503);

  const snapshot = {
    zone, timestamp: now(),
    ...body,
  };

  const key = `snapshots/${zone}/${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
  await bucket.put(key, JSON.stringify(snapshot, null, 2), {
    httpMetadata: { contentType: 'application/json' },
    customMetadata: { type: 'snapshot', zone, created: now() },
  });

  return jsonResponse({ success: true, zone, snapshotKey: key, timestamp: snapshot.timestamp });
}

// ================================================================================
// DATABASE INIT
// ================================================================================

async function initDatabase(env) {
  if (!env.DB) return errorResponse("D1 database not configured");

  try {
    const statements = D1_SCHEMA.split(';').filter(s => s.trim());
    for (const stmt of statements) {
      if (stmt.trim()) {
        await env.DB.prepare(stmt).run();
      }
    }
    return jsonResponse({ success: true, message: "Database initialized", tables: ["sessions", "todos", "memories", "events", "broadcasts", "build_reports", "engine_status", "gate_status", "build_notes"] });
  } catch (e) {
    return jsonResponse({ success: false, error: e.message }, 500);
  }
}

// ================================================================================
// MAIN ROUTER
// ================================================================================

export default {
  async fetch(request, env, ctx) {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    // Auth gate: all POST/PUT/DELETE requests require API key
    if (['POST', 'PUT', 'DELETE'].includes(method)) {
      const authErr = authenticate(request, env);
      if (authErr) return authErr;
      // Payload size cap: 1MB
      const contentLength = parseInt(request.headers.get('Content-Length') || '0');
      if (contentLength > 1_048_576) {
        return jsonResponse({ error: 'Payload too large', max_bytes: 1_048_576 }, 413);
      }
    }

    // Parse body for POST/PUT
    let body = {};
    if (method === "POST" || method === "PUT") {
      try {
        body = await request.json();
      } catch (e) {
        body = {};
      }
    }

    // Route handling
    try {
      // Health & Info
      if (path === "/" || path === "/health") return handleHealth(env);
      if (path === "/policies" && method === "GET") return handlePolicies(env);
      if (path === "/policies" && method === "POST") return storePolicy(env, body);
      if (path.startsWith("/policies/") && method === "DELETE") {
        const policyId = path.replace("/policies/", "");
        return deletePolicy(env, policyId);
      }

      // Database Init
      if (path === "/init" && method === "POST") return initDatabase(env);

      // Sessions
      if (path === "/sessions" && method === "GET") return getSessions(env);
      if (path === "/sessions/register" && method === "POST") return registerSession(env, body);
      if (path === "/sessions/heartbeat" && method === "POST") return heartbeat(env, body);

      // Todos
      if (path === "/todos" && method === "GET") return getTodos(env);
      if (path === "/todos" && method === "POST") return createTodo(env, body);
      if (path.startsWith("/todos/") && method === "PUT") {
        const id = path.split("/")[2];
        return updateTodo(env, id, body);
      }

      // Memories
      if (path.startsWith("/memory/recall/") && method === "GET") {
        const key = path.replace("/memory/recall/", "");
        return getMemory(env, key);
      }
      if (path === "/memory/store" && method === "POST") return setMemory(env, body);

      // Broadcasts
      if (path === "/broadcasts" && method === "GET") return getBroadcasts(env);
      if (path === "/broadcasts" && method === "POST") return createBroadcast(env, body);

      // Context
      if (path === "/context/load" && method === "GET") {
        const workspace = url.searchParams.get("workspace");
        return loadContext(env, workspace);
      }
      if (path === "/context/store" && method === "POST") return storeContext(env, body);
      if (path === "/context/inject" && method === "GET") {
        const workspace = url.searchParams.get("workspace");
        return loadContext(env, workspace);
      }

      // Build Status
      if (path === "/build/report" && method === "POST") return buildReport(env, body);
      if (path === "/build/status" && method === "GET") return buildStatus(env);
      if (path === "/build/reports" && method === "GET") return buildReports(env, url);
      if (path === "/build/engine-update" && method === "POST") return engineUpdate(env, body);
      if (path === "/build/gate-update" && method === "POST") return gateUpdate(env, body);
      if (path === "/build/note" && method === "POST") return buildNote(env, body);
      if (path === "/build/dashboard-data" && method === "GET") return dashboardData(env);
      if (path === "/build/seed/engines" && method === "POST") return bulkSeedEngines(env, body);
      if (path === "/build/seed/gates" && method === "POST") return bulkSeedGates(env, body);
      if (path === "/build/seed/notes" && method === "POST") return bulkSeedNotes(env, body);

      // R2 Storage — Swarm Brain / Memory System / Vault
      if (path === "/r2/stats" && method === "GET") return r2Stats(env);
      if (path === "/r2/cross-sync" && method === "POST") return r2CrossSync(env, body);

      // R2 per-zone CRUD: /r2/{swarm|memory|vault|law|tax|knowledge}/store, /get, /delete, /list, /snapshot
      const r2Match = path.match(/^\/r2\/(swarm|memory|vault|law|tax|knowledge)\/(.+)$/);
      if (r2Match) {
        const [, zone, action] = r2Match;
        if (action === "store" && method === "POST") return r2Store(env, zone, body);
        if (action === "snapshot" && method === "POST") return r2Snapshot(env, zone, body);
        if (action === "list" && method === "GET") {
          const prefix = url.searchParams.get("prefix");
          const limit = parseInt(url.searchParams.get("limit") || "100");
          return r2List(env, zone, prefix, limit);
        }
        if (action.startsWith("get/") && method === "GET") {
          const key = action.replace("get/", "");
          return r2Get(env, zone, decodeURIComponent(key));
        }
        if (action.startsWith("delete/") && method === "DELETE") {
          const key = action.replace("delete/", "");
          return r2Delete(env, zone, decodeURIComponent(key));
        }
      }

      return errorResponse("Not found", 404);
    } catch (e) {
      return errorResponse(`Server error: ${e.message}`, 500);
    }
  }
};
