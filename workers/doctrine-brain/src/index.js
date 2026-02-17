/**
 * ECHO DOCTRINE BRAIN v1.0.0
 *
 * The unified doctrinal brain runtime.
 * One Worker. All domains. Retrieval-grounded reasoning.
 *
 * Replaces: 408 separate Python FastAPI engine files.
 * Architecture: D1 (metadata) + R2 (content) + Vectorize (semantic) + KV (cache) + AI (embeddings)
 */

const MODES = { FAST: 'FAST', DEFENSE: 'DEFENSE', MEMO: 'MEMO' };
const CONFIDENCE_LEVELS = ['DEFENSIBLE', 'AGGRESSIVE', 'DISCLOSURE', 'HIGH_RISK'];
const MAX_BLOCKS = 20;
const CACHE_TTL_SECONDS = 3600;

// ═══════════════════════════════════════════════════════════════════════════
// AUTH MIDDLEWARE
// ═══════════════════════════════════════════════════════════════════════════

function authenticate(request, env) {
  // Public endpoints (health, protocol, spec reads, task reads)
  const url = new URL(request.url);
  if (url.pathname === '/health' || url.pathname === '/protocol' || url.pathname === '/') {
    return true;
  }
  // GET on specs and tasks are public (read-only)
  if (request.method === 'GET' && (url.pathname === '/specs' || url.pathname.startsWith('/spec/') || url.pathname.startsWith('/task/'))) {
    return true;
  }
  const key = request.headers.get('X-Echo-API-Key') || request.headers.get('Authorization')?.replace('Bearer ', '');
  if (!key || key !== env.ECHO_API_KEY) {
    return false;
  }
  return true;
}

// ═══════════════════════════════════════════════════════════════════════════
// RATE LIMITER (KV-based token bucket)
// ═══════════════════════════════════════════════════════════════════════════

async function checkRateLimit(request, env) {
  if (!env.CACHE) return true;
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const key = `ratelimit:${ip}`;
  const now = Math.floor(Date.now() / 1000);
  const window = 60; // 1 minute
  const maxRequests = 60;

  try {
    const data = await env.CACHE.get(key, 'json');
    if (!data || data.window !== Math.floor(now / window)) {
      await env.CACHE.put(key, JSON.stringify({ window: Math.floor(now / window), count: 1 }), { expirationTtl: window * 2 });
      return true;
    }
    if (data.count >= maxRequests) return false;
    data.count++;
    await env.CACHE.put(key, JSON.stringify(data), { expirationTtl: window * 2 });
    return true;
  } catch {
    return true; // Fail open on rate limit errors
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// RESPONSE HELPERS
// ═══════════════════════════════════════════════════════════════════════════

function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Echo-API-Key, Authorization',
      'X-Brain-Version': '1.0.0',
    },
  });
}

function error(message, status = 400) {
  return json({ error: message, timestamp: new Date().toISOString() }, status);
}

// ═══════════════════════════════════════════════════════════════════════════
// CORE: DOCTRINE QUERY ENGINE
// ═══════════════════════════════════════════════════════════════════════════

async function queryDoctrine(env, { question, domains, mode, top_k }) {
  const start = Date.now();
  mode = MODES[mode] || MODES.FAST;
  top_k = Math.min(top_k || 10, MAX_BLOCKS);

  // Layer 1: Cache check (KV)
  const cacheKey = `query:${hashString(question + (domains || []).join(',') + mode)}`;
  if (env.CACHE) {
    try {
      const cached = await env.CACHE.get(cacheKey, 'json');
      if (cached) {
        cached.meta.cache_hit = true;
        cached.meta.latency_ms = Date.now() - start;
        return cached;
      }
    } catch { /* cache miss, continue */ }
  }

  // Layer 2: Semantic search (Vectorize)
  let blocks = [];
  if (env.VECTORS && env.AI) {
    try {
      const embedding = await env.AI.run('@cf/baai/bge-base-en-v1.5', { text: [question] });
      const vector = embedding.data[0];

      const filter = domains && domains.length > 0
        ? { domain_id: { $in: domains } }
        : undefined;

      const results = await env.VECTORS.query(vector, {
        topK: top_k,
        filter,
        returnMetadata: 'all',
      });

      if (results.matches && results.matches.length > 0) {
        const blockIds = results.matches.map(m => m.id);
        blocks = await fetchBlocksFromD1(env, blockIds);

        // Attach relevance scores
        for (const block of blocks) {
          const match = results.matches.find(m => m.id === block.block_id);
          if (match) block._relevance = match.score;
        }
        blocks.sort((a, b) => (b._relevance || 0) - (a._relevance || 0));
      }
    } catch (err) {
      console.error('Vectorize search failed:', err.message);
      // Fall through to D1 keyword search
    }
  }

  // Layer 3: D1 keyword fallback (if Vectorize returned nothing)
  if (blocks.length === 0) {
    blocks = await keywordSearch(env, question, domains, top_k);
  }

  // Format response based on mode
  const response = formatResponse(blocks, question, mode);

  // Add metadata
  response.meta = {
    query: question,
    domains_requested: domains || 'all',
    domains_matched: [...new Set(blocks.map(b => b.domain_id))],
    mode,
    blocks_retrieved: blocks.length,
    latency_ms: Date.now() - start,
    cache_hit: false,
    determinism_hash: hashString(JSON.stringify(response.blocks || [])),
    timestamp: new Date().toISOString(),
  };

  // Cache result
  if (env.CACHE) {
    try {
      await env.CACHE.put(cacheKey, JSON.stringify(response), { expirationTtl: CACHE_TTL_SECONDS });
    } catch { /* cache write failure is non-fatal */ }
  }

  // Audit log
  await auditLog(env, 'QUERY', null, null, 'doctrine-brain',
    `${mode} query: ${question.substring(0, 100)} → ${blocks.length} blocks from [${response.meta.domains_matched.join(',')}]`);

  return response;
}

// ═══════════════════════════════════════════════════════════════════════════
// BLOCK RETRIEVAL
// ═══════════════════════════════════════════════════════════════════════════

async function fetchBlocksFromD1(env, blockIds) {
  if (!blockIds.length) return [];
  const placeholders = blockIds.map(() => '?').join(',');
  const { results } = await env.DB.prepare(
    `SELECT block_id, domain_id, subdomain, topic, keywords, confidence,
            authority_level, content_r2_key, token_count
     FROM doctrine_blocks WHERE block_id IN (${placeholders})`
  ).bind(...blockIds).all();

  // Fetch full content from R2 for each block
  const enriched = await Promise.all(results.map(async (block) => {
    if (block.content_r2_key && env.R2) {
      try {
        const obj = await env.R2.get(block.content_r2_key);
        if (obj) {
          block.content = await obj.json();
        }
      } catch { /* R2 fetch failure — return metadata only */ }
    }
    return block;
  }));

  return enriched;
}

async function keywordSearch(env, question, domains, limit) {
  const words = question.toLowerCase().split(/\s+/).filter(w => w.length > 3).slice(0, 5);
  if (!words.length) return [];

  let sql = `SELECT block_id, domain_id, subdomain, topic, keywords, confidence,
                    authority_level, content_r2_key, token_count
             FROM doctrine_blocks WHERE (`;
  const binds = [];

  // Match keywords JSON array against query words
  const conditions = words.map(w => {
    binds.push(`%${w}%`);
    return `LOWER(keywords) LIKE ?`;
  });
  sql += conditions.join(' OR ') + ')';

  if (domains && domains.length > 0) {
    sql += ` AND domain_id IN (${domains.map(() => '?').join(',')})`;
    binds.push(...domains);
  }

  sql += ` ORDER BY authority_level DESC LIMIT ?`;
  binds.push(limit);

  const { results } = await env.DB.prepare(sql).bind(...binds).all();

  // Enrich with R2 content
  return Promise.all(results.map(async (block) => {
    if (block.content_r2_key && env.R2) {
      try {
        const obj = await env.R2.get(block.content_r2_key);
        if (obj) block.content = await obj.json();
      } catch {}
    }
    return block;
  }));
}

// ═══════════════════════════════════════════════════════════════════════════
// RESPONSE FORMATTING (FAST / DEFENSE / MEMO)
// ═══════════════════════════════════════════════════════════════════════════

function formatResponse(blocks, question, mode) {
  if (blocks.length === 0) {
    return {
      answer: null,
      confidence: 'DISCLOSURE',
      disclosure: 'No doctrine blocks matched this query. Response would be ungrounded.',
      blocks: [],
      citations: [],
    };
  }

  const citations = [];
  const blockSummaries = [];

  for (const block of blocks) {
    const content = block.content || {};
    blockSummaries.push({
      block_id: block.block_id,
      domain: block.domain_id,
      topic: block.topic,
      confidence: block.confidence,
      relevance: block._relevance || null,
      conclusion: content.conclusion_template || content.conclusion || null,
      key_factors: content.key_factors || [],
    });

    if (content.primary_authority) {
      citations.push(...(Array.isArray(content.primary_authority) ? content.primary_authority : [content.primary_authority]));
    }
  }

  const topBlock = blocks[0];
  const topContent = topBlock.content || {};

  if (mode === 'FAST') {
    return {
      answer: topContent.conclusion_template || topContent.conclusion || `Doctrine retrieved for: ${topBlock.topic}`,
      confidence: topBlock.confidence || 'DISCLOSURE',
      domain: topBlock.domain_id,
      topic: topBlock.topic,
      key_factors: (topContent.key_factors || []).slice(0, 5),
      citations: [...new Set(citations)].slice(0, 5),
      blocks: blockSummaries.slice(0, 3),
    };
  }

  if (mode === 'DEFENSE') {
    return {
      answer: topContent.conclusion_template || topContent.conclusion || null,
      confidence: topBlock.confidence || 'DISCLOSURE',
      confidence_stratification: {
        level: topBlock.confidence,
        authority_level: topBlock.authority_level,
        block_count: blocks.length,
        cross_domain: [...new Set(blocks.map(b => b.domain_id))].length > 1,
      },
      reasoning_framework: topContent.reasoning_framework || null,
      key_factors: topContent.key_factors || [],
      counter_arguments: topContent.counter_arguments || [],
      resolution_strategy: topContent.resolution_strategy || null,
      adversary_position: topContent.adversary_position || null,
      burden_holder: topContent.burden_holder || null,
      citations: [...new Set(citations)],
      blocks: blockSummaries,
      disclosure: topBlock.confidence === 'HIGH_RISK' || topBlock.confidence === 'DISCLOSURE'
        ? 'This analysis involves areas of legal uncertainty. Independent professional review is recommended.'
        : null,
    };
  }

  // MEMO mode — full documentation
  return {
    memorandum: {
      subject: question,
      date: new Date().toISOString().split('T')[0],
      domains_analyzed: [...new Set(blocks.map(b => b.domain_id))],
      conclusion: topContent.conclusion_template || topContent.conclusion || null,
      analysis: blockSummaries,
      reasoning: topContent.reasoning_framework || null,
      key_factors: topContent.key_factors || [],
      counter_arguments: topContent.counter_arguments || [],
      resolution_strategy: topContent.resolution_strategy || null,
      risk_assessment: {
        confidence: topBlock.confidence,
        authority_level: topBlock.authority_level,
        fact_fragility: topContent.fact_fragility || null,
      },
      citations: [...new Set(citations)],
      disclosure: 'This memorandum is generated from pre-compiled doctrine blocks and should be reviewed by qualified professionals before reliance.',
    },
    blocks: blockSummaries,
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// INGEST: Add doctrine blocks
// ═══════════════════════════════════════════════════════════════════════════

async function ingestBlock(env, block) {
  const blockId = block.block_id || `${block.domain_id}_${block.topic.toLowerCase().replace(/[^a-z0-9]+/g, '_')}`;
  const contentKey = `doctrines/${block.domain_id}/${blockId}.json`;

  // Store full content to R2
  if (env.R2) {
    await env.R2.put(contentKey, JSON.stringify(block.content || block, null, 2), {
      customMetadata: { domain_id: block.domain_id, topic: block.topic },
    });
  }

  // Compute content hash
  const contentHash = hashString(JSON.stringify(block.content || block));

  // Store metadata to D1
  await env.DB.prepare(`
    INSERT OR REPLACE INTO doctrine_blocks
    (block_id, domain_id, subdomain, topic, keywords, confidence, authority_level,
     content_hash, content_r2_key, token_count, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
  `).bind(
    blockId,
    block.domain_id,
    block.subdomain || null,
    block.topic,
    JSON.stringify(block.keywords || []),
    block.confidence || 'DISCLOSURE',
    block.authority_level || 5.0,
    contentHash,
    contentKey,
    block.token_count || estimateTokens(JSON.stringify(block.content || block)),
  ).run();

  // Embed and store in Vectorize
  if (env.AI && env.VECTORS) {
    try {
      const text = `${block.topic} ${(block.keywords || []).join(' ')} ${block.subdomain || ''} ${(block.content?.conclusion_template || '')}`;
      const embedding = await env.AI.run('@cf/baai/bge-base-en-v1.5', { text: [text] });
      await env.VECTORS.upsert([{
        id: blockId,
        values: embedding.data[0],
        metadata: {
          domain_id: block.domain_id,
          subdomain: block.subdomain || '',
          topic: block.topic,
          confidence: block.confidence || 'DISCLOSURE',
          authority_level: block.authority_level || 5.0,
        },
      }]);
    } catch (err) {
      console.error('Vectorize upsert failed:', err.message);
    }
  }

  // Update domain block count
  await env.DB.prepare(`
    UPDATE domains SET block_count = (
      SELECT COUNT(*) FROM doctrine_blocks WHERE domain_id = ?
    ), updated_at = datetime('now') WHERE domain_id = ?
  `).bind(block.domain_id, block.domain_id).run();

  await auditLog(env, 'INGEST', block.domain_id, blockId, 'api', `Block ingested: ${block.topic}`);

  return { block_id: blockId, domain_id: block.domain_id, stored: true };
}

async function ingestBatch(env, blocks) {
  const results = [];
  for (const block of blocks) {
    try {
      const r = await ingestBlock(env, block);
      results.push(r);
    } catch (err) {
      results.push({ block_id: block.block_id, error: err.message });
    }
  }
  return { ingested: results.filter(r => r.stored).length, failed: results.filter(r => r.error).length, results };
}

// ═══════════════════════════════════════════════════════════════════════════
// DOMAIN MANAGEMENT
// ═══════════════════════════════════════════════════════════════════════════

async function listDomains(env) {
  const { results } = await env.DB.prepare(
    `SELECT domain_id, domain_name, tier, subdomain_count, block_count, quality_score,
            created_at, updated_at FROM domains ORDER BY tier, domain_id`
  ).all();
  return { domains: results, count: results.length };
}

async function getDomain(env, domainId) {
  const domain = await env.DB.prepare(
    `SELECT * FROM domains WHERE domain_id = ?`
  ).bind(domainId).first();
  if (!domain) return null;

  const { results: blocks } = await env.DB.prepare(
    `SELECT block_id, subdomain, topic, confidence, authority_level, token_count, updated_at
     FROM doctrine_blocks WHERE domain_id = ? ORDER BY subdomain, topic`
  ).bind(domainId).all();

  return { ...domain, blocks };
}

async function createDomain(env, data) {
  await env.DB.prepare(`
    INSERT OR IGNORE INTO domains (domain_id, domain_name, tier, subdomain_count, block_count, quality_score)
    VALUES (?, ?, ?, ?, 0, 0.0)
  `).bind(data.domain_id, data.domain_name, data.tier || 0, data.subdomain_count || 0).run();
  return { domain_id: data.domain_id, created: true };
}

// ═══════════════════════════════════════════════════════════════════════════
// QUALITY AUDIT
// ═══════════════════════════════════════════════════════════════════════════

async function auditDomain(env, domainId) {
  const domain = await getDomain(env, domainId);
  if (!domain) return { error: 'Domain not found' };

  const blocks = domain.blocks || [];
  const rubric = {
    doctrine_count: { weight: 15, score: 0, detail: '' },
    authority_citations: { weight: 10, score: 0, detail: '' },
    confidence_stratification: { weight: 5, score: 0, detail: '' },
    subdomain_coverage: { weight: 5, score: 0, detail: '' },
    keyword_quality: { weight: 5, score: 0, detail: '' },
    content_depth: { weight: 10, score: 0, detail: '' },
  };

  // 1. Doctrine count (target: 50+)
  if (blocks.length >= 50) { rubric.doctrine_count.score = 100; rubric.doctrine_count.detail = `${blocks.length} blocks (target: 50+)`; }
  else if (blocks.length >= 30) { rubric.doctrine_count.score = 70; rubric.doctrine_count.detail = `${blocks.length} blocks (target: 50+)`; }
  else if (blocks.length >= 10) { rubric.doctrine_count.score = 40; rubric.doctrine_count.detail = `${blocks.length} blocks (target: 50+)`; }
  else { rubric.doctrine_count.score = 10; rubric.doctrine_count.detail = `${blocks.length} blocks (target: 50+)`; }

  // 2. Confidence stratification — check variety
  const confidences = new Set(blocks.map(b => b.confidence).filter(Boolean));
  rubric.confidence_stratification.score = Math.min(100, confidences.size * 25);
  rubric.confidence_stratification.detail = `${confidences.size}/4 levels used: ${[...confidences].join(', ')}`;

  // 3. Subdomain coverage
  const subdomains = new Set(blocks.map(b => b.subdomain).filter(Boolean));
  rubric.subdomain_coverage.score = Math.min(100, subdomains.size * 20);
  rubric.subdomain_coverage.detail = `${subdomains.size} subdomains: ${[...subdomains].slice(0, 5).join(', ')}`;

  // 4. Keyword quality — blocks with 5+ keywords
  const withGoodKeywords = blocks.filter(b => {
    try { return JSON.parse(b.keywords || '[]').length >= 5; } catch { return false; }
  });
  rubric.keyword_quality.score = blocks.length > 0 ? Math.round((withGoodKeywords.length / blocks.length) * 100) : 0;
  rubric.keyword_quality.detail = `${withGoodKeywords.length}/${blocks.length} blocks have 5+ keywords`;

  // 5 & 6. Content depth — need to sample R2 content
  // (Simplified: check if content_r2_key exists for all blocks)
  const withContent = blocks.filter(b => b.content_r2_key);
  rubric.content_depth.score = blocks.length > 0 ? Math.round((withContent.length / blocks.length) * 100) : 0;
  rubric.content_depth.detail = `${withContent.length}/${blocks.length} blocks have R2 content`;

  // Authority citations — sample 5 blocks and check R2 content for citations
  let citationScore = 0;
  const sampleSize = Math.min(5, blocks.length);
  if (sampleSize > 0 && env.R2) {
    let withCitations = 0;
    for (let i = 0; i < sampleSize; i++) {
      const block = blocks[i];
      if (block.content_r2_key) {
        try {
          const obj = await env.R2.get(block.content_r2_key);
          if (obj) {
            const content = await obj.json();
            if (content.primary_authority && content.primary_authority.length >= 2) {
              withCitations++;
            }
          }
        } catch {}
      }
    }
    citationScore = Math.round((withCitations / sampleSize) * 100);
  }
  rubric.authority_citations.score = citationScore;
  rubric.authority_citations.detail = `Sampled ${sampleSize} blocks for citation check`;

  // Calculate weighted total
  let totalWeight = 0, totalScore = 0;
  for (const [, gate] of Object.entries(rubric)) {
    totalWeight += gate.weight;
    totalScore += (gate.score / 100) * gate.weight;
  }
  const pct = Math.round((totalScore / totalWeight) * 100);

  // Grade
  let grade;
  if (pct >= 90) grade = 'A';
  else if (pct >= 70) grade = 'B';
  else if (pct >= 50) grade = 'C';
  else grade = 'F';

  // Update domain quality score
  await env.DB.prepare(
    `UPDATE domains SET quality_score = ?, updated_at = datetime('now') WHERE domain_id = ?`
  ).bind(pct / 100, domainId).run();

  return {
    domain_id: domainId,
    grade,
    score_pct: pct,
    block_count: blocks.length,
    rubric,
    recommendation: grade === 'F' ? 'REJECTED — rebuild required'
      : grade === 'C' ? 'QUARANTINE — enrichment needed'
      : grade === 'B' ? 'DEPLOYED — monitor'
      : 'DEPLOYED — production ready',
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// HEALTH + METRICS
// ═══════════════════════════════════════════════════════════════════════════

async function getHealth(env) {
  let domainCount = 0, blockCount = 0, avgQuality = 0;
  try {
    const stats = await env.DB.prepare(
      `SELECT COUNT(*) as domains, SUM(block_count) as blocks, AVG(quality_score) as avg_q FROM domains`
    ).first();
    domainCount = stats?.domains || 0;
    blockCount = stats?.blocks || 0;
    avgQuality = Math.round((stats?.avg_q || 0) * 100);
  } catch {}

  return {
    service: 'echo-doctrine-brain',
    version: '1.0.0',
    status: 'operational',
    architecture: 'unified-doctrinal-brain',
    stats: {
      domains: domainCount,
      doctrine_blocks: blockCount,
      avg_quality_pct: avgQuality,
    },
    bindings: {
      d1: !!env.DB,
      r2: !!env.R2,
      kv: !!env.CACHE,
      vectorize: !!env.VECTORS,
      ai: !!env.AI,
    },
    timestamp: new Date().toISOString(),
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0;
  }
  return Math.abs(hash).toString(16).padStart(8, '0');
}

function estimateTokens(text) {
  return Math.ceil(text.length / 4);
}

async function auditLog(env, eventType, domainId, blockId, actor, message) {
  try {
    await env.DB.prepare(
      `INSERT INTO audit_log (event_type, domain_id, block_id, actor, message) VALUES (?, ?, ?, ?, ?)`
    ).bind(eventType, domainId, blockId, actor, message).run();
  } catch { /* audit log failure is non-fatal */ }
}

// ═══════════════════════════════════════════════════════════════════════════
// TIER SPECS + TASK PACKAGES
// ═══════════════════════════════════════════════════════════════════════════

async function getSpec(env, tierPrefix) {
  tierPrefix = tierPrefix.toUpperCase();

  // Try R2 first
  if (env.R2) {
    try {
      const obj = await env.R2.get(`specs/${tierPrefix}.json`);
      if (obj) return await obj.json();
    } catch {}
  }

  // Try D1 tier_specs table
  try {
    const row = await env.DB.prepare(
      `SELECT spec_json FROM tier_specs WHERE tier_prefix = ?`
    ).bind(tierPrefix).first();
    if (row?.spec_json) return JSON.parse(row.spec_json);
  } catch {}

  return null;
}

async function listSpecs(env) {
  // List all specs from D1
  try {
    const { results } = await env.DB.prepare(
      `SELECT tier_prefix, tier_name, engine_count, updated_at FROM tier_specs ORDER BY tier_prefix`
    ).all();
    return { specs: results || [], count: (results || []).length };
  } catch {
    return { specs: [], count: 0 };
  }
}

async function upsertSpec(env, spec) {
  if (!spec.tier_prefix || !spec.tier_name) {
    return { error: 'tier_prefix and tier_name required' };
  }

  const specJson = JSON.stringify(spec);
  const engineCount = (spec.engines || []).length;

  // Store to D1
  await env.DB.prepare(`
    INSERT INTO tier_specs (tier_prefix, tier_name, engine_count, spec_json, updated_at)
    VALUES (?, ?, ?, ?, datetime('now'))
    ON CONFLICT(tier_prefix) DO UPDATE SET
      tier_name = excluded.tier_name,
      engine_count = excluded.engine_count,
      spec_json = excluded.spec_json,
      updated_at = datetime('now')
  `).bind(spec.tier_prefix.toUpperCase(), spec.tier_name, engineCount, specJson).run();

  // Store to R2 for fast retrieval
  if (env.R2) {
    await env.R2.put(`specs/${spec.tier_prefix.toUpperCase()}.json`, specJson, {
      customMetadata: { tier_name: spec.tier_name, engine_count: String(engineCount) },
    });
  }

  await auditLog(env, 'SPEC_UPSERT', spec.tier_prefix, null, 'api',
    `Tier spec upserted: ${spec.tier_name} (${engineCount} engines)`);

  return { tier_prefix: spec.tier_prefix.toUpperCase(), tier_name: spec.tier_name, engines: engineCount, stored: true };
}

async function generateTaskPackage(env, engineId) {
  engineId = engineId.toUpperCase();

  // Extract tier prefix from engine ID (strip trailing digits)
  const tierPrefix = engineId.replace(/\d+$/, '');
  const spec = await getSpec(env, tierPrefix);
  if (!spec) {
    return { error: `No spec found for tier prefix: ${tierPrefix}` };
  }

  // Find the engine in the spec
  const engineDef = (spec.engines || []).find(e => e.engine_id === engineId);
  if (!engineDef) {
    return { error: `Engine ${engineId} not found in spec ${tierPrefix}` };
  }

  // Build the task package
  const buildPrompt = composeBuildPrompt(spec, engineDef);

  return {
    task_id: `build_${engineId}_${new Date().toISOString().replace(/[-:T]/g, '').substring(0, 14)}`,
    engine_id: engineId,
    output_mode: 'doctrine_blocks',
    domain_context: {
      tier_prefix: spec.tier_prefix,
      tier_name: spec.tier_name,
      domain_description: spec.domain_description,
      authority_sources: spec.authority_sources,
      function: engineDef.function,
      doctrine_topics: engineDef.doctrine_topics,
    },
    build_prompt: buildPrompt,
    eval_pack: engineDef.eval_pack,
    quality_gates: [
      { gate: 'EVAL_PACK', weight: 50, criteria: '70%+ golden queries pass' },
      { gate: 'DOCTRINE_COUNT', weight: 20, criteria: '>= 30 blocks' },
      { gate: 'CITATION_DENSITY', weight: 15, criteria: '>= 2 citations/block avg' },
      { gate: 'SYNTAX', weight: 10, criteria: 'py_compile passes' },
      { gate: 'NO_PLACEHOLDERS', weight: 5, criteria: 'zero TODO/pass/NotImplementedError' },
    ],
    callback_url: 'https://echo-build-orchestrator.bmcii1976.workers.dev/build/complete',
    generated_at: new Date().toISOString(),
  };
}

function composeBuildPrompt(spec, engineDef) {
  return `You are building engine ${engineDef.engine_id}: ${engineDef.name}.

DOMAIN: ${spec.tier_name}
DESCRIPTION: ${spec.domain_description}

FUNCTION: ${engineDef.function}

AUTHORITY SOURCES (cite these):
${(spec.authority_sources || []).map(s => `- ${s}`).join('\n')}

DOCTRINE TOPICS (implement ALL as DoctrineBlock instances):
${(engineDef.doctrine_topics || []).map((t, i) => `${i + 1}. ${t}`).join('\n')}

REQUIREMENTS:
- Build a complete FastAPI engine with ALL 20 TIE components
- Each DoctrineBlock must have: topic, keywords(5-8), conclusion_template(3-5 sentences),
  reasoning_framework(20-40 lines), key_factors(5+), primary_authority(3-5 citations),
  burden_holder, adversary_position, counter_arguments(5+), resolution_strategy,
  entity_scope, confidence, confidence_stratification, controlling_precedent
- Minimum 50 doctrine blocks with REAL domain content
- Three response modes: FAST, DEFENSE, MEMO
- Health endpoint at /health returning JSON
- Loguru logging (never print)
- Pydantic models for all I/O
- Type hints on all functions
- ZERO placeholders (no TODO, pass, NotImplementedError, ...)
- Target: 8,000+ lines of production-ready code

GOLDEN QUERIES (your engine MUST handle these correctly):
${(engineDef.eval_pack?.golden_queries || []).map((q, i) => `
Query ${i + 1}: "${q.question}"
Required elements: ${(q.required_elements || []).join(', ')}
Failure signals: ${(q.failure_signals || []).join(', ')}
`).join('\n')}

OUTPUT: Complete engine.py file with all components implemented.`;
}

// ═══════════════════════════════════════════════════════════════════════════
// D1 SCHEMA INITIALIZATION
// ═══════════════════════════════════════════════════════════════════════════

async function initSchema(env) {
  const tables = [
    `CREATE TABLE IF NOT EXISTS domains (
      domain_id TEXT PRIMARY KEY,
      domain_name TEXT NOT NULL,
      tier INTEGER DEFAULT 0,
      subdomain_count INTEGER DEFAULT 0,
      block_count INTEGER DEFAULT 0,
      quality_score REAL DEFAULT 0.0,
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now'))
    )`,
    `CREATE TABLE IF NOT EXISTS doctrine_blocks (
      block_id TEXT PRIMARY KEY,
      domain_id TEXT NOT NULL,
      subdomain TEXT,
      topic TEXT NOT NULL,
      keywords TEXT NOT NULL DEFAULT '[]',
      confidence TEXT DEFAULT 'DISCLOSURE',
      authority_level REAL DEFAULT 5.0,
      content_hash TEXT,
      content_r2_key TEXT,
      vectorize_id TEXT,
      token_count INTEGER DEFAULT 0,
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now'))
    )`,
    `CREATE TABLE IF NOT EXISTS builds (
      build_id TEXT PRIMARY KEY,
      domain_id TEXT NOT NULL,
      status TEXT DEFAULT 'PLANNED',
      builder TEXT,
      blocks_created INTEGER DEFAULT 0,
      quality_grade TEXT,
      error_log TEXT,
      created_at TEXT DEFAULT (datetime('now')),
      completed_at TEXT
    )`,
    `CREATE TABLE IF NOT EXISTS quality_gates (
      gate_id INTEGER PRIMARY KEY AUTOINCREMENT,
      domain_id TEXT NOT NULL,
      gate_type TEXT NOT NULL,
      passed INTEGER NOT NULL DEFAULT 0,
      score REAL,
      details TEXT,
      created_at TEXT DEFAULT (datetime('now'))
    )`,
    `CREATE TABLE IF NOT EXISTS audit_log (
      log_id INTEGER PRIMARY KEY AUTOINCREMENT,
      event_type TEXT NOT NULL,
      domain_id TEXT,
      block_id TEXT,
      actor TEXT,
      message TEXT,
      created_at TEXT DEFAULT (datetime('now'))
    )`,
    `CREATE TABLE IF NOT EXISTS tier_specs (
      tier_prefix TEXT PRIMARY KEY,
      tier_name TEXT NOT NULL,
      engine_count INTEGER DEFAULT 0,
      spec_json TEXT NOT NULL,
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now'))
    )`,
  ];

  const indexes = [
    `CREATE INDEX IF NOT EXISTS idx_blocks_domain ON doctrine_blocks(domain_id)`,
    `CREATE INDEX IF NOT EXISTS idx_blocks_subdomain ON doctrine_blocks(domain_id, subdomain)`,
    `CREATE INDEX IF NOT EXISTS idx_builds_domain ON builds(domain_id)`,
    `CREATE INDEX IF NOT EXISTS idx_builds_status ON builds(status)`,
    `CREATE INDEX IF NOT EXISTS idx_audit_type ON audit_log(event_type)`,
    `CREATE INDEX IF NOT EXISTS idx_audit_domain ON audit_log(domain_id)`,
  ];

  for (const sql of [...tables, ...indexes]) {
    await env.DB.prepare(sql).run();
  }

  return { initialized: true, tables: tables.length, indexes: indexes.length };
}

// ═══════════════════════════════════════════════════════════════════════════
// ROUTER
// ═══════════════════════════════════════════════════════════════════════════

export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, X-Echo-API-Key, Authorization',
        },
      });
    }

    // Auth check
    if (!authenticate(request, env)) {
      return error('Unauthorized. Provide X-Echo-API-Key header.', 401);
    }

    // Rate limit
    if (!await checkRateLimit(request, env)) {
      return error('Rate limit exceeded. Max 60 requests/minute.', 429);
    }

    const url = new URL(request.url);
    const path = url.pathname;

    try {
      // ── PUBLIC ──
      if (path === '/' || path === '/health') {
        return json(await getHealth(env));
      }

      if (path === '/protocol') {
        return json({
          service: 'echo-doctrine-brain',
          version: '1.0.0',
          endpoints: {
            'GET /health': 'System health + stats',
            'GET /domains': 'List all domains with block counts and quality scores',
            'GET /domain/:id': 'Get domain details + block list',
            'POST /domain': 'Create domain {domain_id, domain_name, tier}',
            'POST /query': 'Query doctrine {question, domains?, mode?, top_k?}',
            'POST /ingest': 'Ingest single doctrine block',
            'POST /ingest/batch': 'Ingest multiple blocks {blocks: [...]}',
            'POST /audit/:domain_id': 'Run quality audit on domain',
            'GET /specs': 'List all uploaded tier specs',
            'GET /spec/:tier_prefix': 'Get tier spec by prefix (e.g. OFE, LG, TX)',
            'POST /spec': 'Upload/update a tier spec {tier_prefix, tier_name, engines: [...]}',
            'POST /spec/upload-batch': 'Upload multiple specs {specs: [...]}',
            'GET /task/:engine_id': 'Generate self-contained task package for an engine',
            'POST /init': 'Initialize D1 schema (run once)',
          },
          modes: ['FAST', 'DEFENSE', 'MEMO'],
          confidence_levels: CONFIDENCE_LEVELS,
          auth: 'X-Echo-API-Key header required for all non-public endpoints',
        });
      }

      // ── SCHEMA INIT ──
      if (path === '/init' && request.method === 'POST') {
        return json(await initSchema(env));
      }

      // ── QUERY ──
      if (path === '/query' && request.method === 'POST') {
        const body = await request.json();
        if (!body.question) return error('question field required');
        return json(await queryDoctrine(env, body));
      }

      // ── DOMAINS ──
      if (path === '/domains') {
        return json(await listDomains(env));
      }

      if (path.startsWith('/domain/') && request.method === 'GET') {
        const domainId = path.split('/')[2];
        const domain = await getDomain(env, domainId);
        return domain ? json(domain) : error('Domain not found', 404);
      }

      if (path === '/domain' && request.method === 'POST') {
        const body = await request.json();
        if (!body.domain_id || !body.domain_name) return error('domain_id and domain_name required');
        return json(await createDomain(env, body));
      }

      // ── INGEST ──
      if (path === '/ingest' && request.method === 'POST') {
        const block = await request.json();
        if (!block.domain_id || !block.topic) return error('domain_id and topic required');
        return json(await ingestBlock(env, block));
      }

      if (path === '/ingest/batch' && request.method === 'POST') {
        const { blocks } = await request.json();
        if (!blocks || !Array.isArray(blocks)) return error('blocks array required');
        return json(await ingestBatch(env, blocks));
      }

      // ── AUDIT ──
      if (path.startsWith('/audit/') && request.method === 'POST') {
        const domainId = path.split('/')[2];
        return json(await auditDomain(env, domainId));
      }

      // ── TIER SPECS ──
      if (path === '/specs' && request.method === 'GET') {
        return json(await listSpecs(env));
      }

      if (path.startsWith('/spec/') && request.method === 'GET') {
        const tierPrefix = path.split('/')[2];
        const spec = await getSpec(env, tierPrefix);
        return spec ? json(spec) : error(`Spec not found for tier: ${tierPrefix}`, 404);
      }

      if (path === '/spec' && request.method === 'POST') {
        const body = await request.json();
        return json(await upsertSpec(env, body));
      }

      if (path === '/spec/upload-batch' && request.method === 'POST') {
        const { specs } = await request.json();
        if (!specs || !Array.isArray(specs)) return error('specs array required');
        const results = [];
        for (const spec of specs) {
          try {
            results.push(await upsertSpec(env, spec));
          } catch (err) {
            results.push({ tier_prefix: spec?.tier_prefix, error: err.message });
          }
        }
        return json({ uploaded: results.filter(r => r.stored).length, failed: results.filter(r => r.error).length, results });
      }

      // ── TASK PACKAGES ──
      if (path.startsWith('/task/') && request.method === 'GET') {
        const engineId = path.split('/')[2];
        const pkg = await generateTaskPackage(env, engineId);
        return pkg.error ? error(pkg.error, 404) : json(pkg);
      }

      return error('Not found. GET /protocol for API docs.', 404);

    } catch (err) {
      console.error('Unhandled error:', err);
      return error(`Internal error: ${err.message}`, 500);
    }
  },
};
