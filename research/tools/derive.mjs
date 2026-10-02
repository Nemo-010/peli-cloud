#!/usr/bin/env node
// derive.mjs - instrument header
// Question: what does each provider charge for a fixed agent workload,
// once free credits and subscription floors are applied, and is the
// provider eligible at all?
//
// This is the driver only. The pricing engine and the 366 provider cards
// are third-party corpus (ariana-dot-dev/battleships, no licence published)
// and are NOT in this repository. Fetch them with tools/fetch-corpus.sh
// first. research/cards-extra is loaded if present and is empty in this pass. Run:
//
//   node research/tools/derive.mjs --corpus research/corpus --out data/derived.json
//
// Conditions are printed at the end. Exit 0 = ran, 2 = could not run.

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
function arg(name, dflt) {
  const i = process.argv.indexOf(name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : dflt;
}
const CORPUS = arg('--corpus', 'research/corpus');
const OUT = arg('--out', 'data/derived.json');

const ENGINE = path.resolve(CORPUS, 'site', 'engine.js');
const CARDS = path.resolve(CORPUS, 'research', 'cards');
if (!fs.existsSync(ENGINE) || !fs.existsSync(CARDS)) {
  console.error(`corpus not found at ${CORPUS}. Run tools/fetch-corpus.sh first.`);
  process.exit(2);
}
require(ENGINE);
const PM = globalThis.PM;

const EXTRA = path.join(path.dirname(new URL(import.meta.url).pathname), '..', 'cards-extra');
const cardFiles = [
  ...fs.readdirSync(CARDS).filter(f => f.endsWith('.json')).map(f => path.join(CARDS, f)),
  ...(fs.existsSync(EXTRA) ? fs.readdirSync(EXTRA).filter(f => f.endsWith('.json')).map(f => path.join(EXTRA, f)) : []),
];
const cards = cardFiles.map(f => JSON.parse(fs.readFileSync(f, 'utf8')));

// One fixed shape, billed over six durations. Sandboxes are bursty: they do
// not usually live 24/7 for a month, so the catalogue leads with the short
// horizons and treats the always-on month as the last column, not the default.
const BASE = {
  os: 'linux', arch: 'any', gpu: 'none', gpuCount: 1, ipv4: 0, seats: 1,
  persistentDisk: false, snapshotGiB: 0, egress: 0, alwaysOn: 0,
  concurrency: 1, cpuUtil: 0.5, ramUtil: 0.5,
};
const SHAPE = { vcpu: 2, ram: 4, disk: 20 };
// Each horizon is a number of real sessions, not one uninterrupted run: a
// sandbox is stopped between calls, so a month of 10 h/day is 30 ten-hour
// sessions and a 24/7 month is 30 day-long sessions. Providers whose session
// cap is shorter than one session are ineligible at that horizon and say so.
const WORKLOADS = {
  r1h:  { sessions: 1,  minutes: 60,    description: '1 hour' },
  r10h: { sessions: 1,  minutes: 600,   description: '10 hours (one agent workday)' },
  d1:   { sessions: 1,  minutes: 1440,  description: '24 hours (one day-long session)' },
  w1:   { sessions: 7,  minutes: 1440,  description: '7 days, one day-long session per day' },
  m10h: { sessions: 30, minutes: 600,   description: '10 h/day for 30 days (30 x 10 h sessions, 300 h)' },
  m30:  { sessions: 30, minutes: 1440,  description: '24/7 for 30 days (30 x 24 h sessions, 720 h)' },
};
for (const def of Object.values(WORKLOADS)) {
  def.total_minutes = def.sessions * def.minutes;
}

// Bursty use: the same 10 h/day a month, delivered the way an agent that starts
// a sandbox per tool call actually does it - twenty 30-minute sessions a day
// (600 over the month), not one 10 h session. The engine applies each mode's
// minimum billable unit and granularity per start, so this is the pessimistic
// side of the same demand: a provider that rounds any start up to an hour shows
// a 2x penalty here and 1x in the m10h column above. Compared like for like, so
// the three columns are the same 300 hours of demand.
const BURSTY = {
  b30m: { sessions: 600, minutes: 30, description: '10 h/day as 20 x 30-min sessions (bursty agent month)' },
};
for (const def of Object.values(BURSTY)) {
  def.total_minutes = def.sessions * def.minutes;
}

function price(card, W, credits) {
  try {
    const r = PM.priceCard(card, Object.assign({}, BASE, W), { credits });
    if (!r) return { eligible: false, reasons: ['no result'] };
    return {
      eligible: !!r.eligible,
      total: typeof r.total === 'number' && isFinite(r.total) ? +r.total.toFixed(4) : null,
      mode: r.modeLabel || null,
      plan: r.plan || null,
      caveats: (r.caveats || []).slice(),
      reasons: (r.reasons || []).slice(),
    };
  } catch (e) {
    return { eligible: false, reasons: ['CRASH ' + String(e).slice(0, 120)] };
  }
}

// Facts only: plans, mode flags, storage and network knobs, and the small
// feature set that decides whether a workload can run at all. No prose.
function facts(card) {
  const plans = (card.plans || []).filter(p => !p.trial_only).map(p => ({
    name: p.name, fee: p.fee, fee_is_credit: !!p.fee_is_credit, per_seat: p.per_seat || 0,
    included_usd: p.included_usd || 0, concurrency: p.concurrency ?? null,
    max_session_h: p.max_session_h ?? null, max_starts_per_min: p.max_starts_per_min ?? null,
  }));
  const modes = (card.modes || []).map(m => ({
    key: m.key, label: m.label, flags: m.flags || [], cpu_class: m.cpu_class || null,
    pricing: m.pricing || null, vcpu_h: m.vcpu_h ?? null, ram_gib_h: m.ram_gib_h ?? null,
    sizes: (m.sizes || []).map(s => ({ name: s.name, vcpu: s.vcpu, ram_gib: s.ram_gib, disk_gib: s.disk_gib ?? null, hour: s.hour ?? null, month_cap: s.month_cap ?? null })),
    min_billed_seconds: m.min_billed_seconds ?? null, granularity_s: m.granularity_s ?? null,
    start_fee: m.start_fee ?? null, boot_overhead_s: m.boot_overhead_s ?? null, commit_note: m.commit_note || null,
    vcpu_options: m.vcpu_options || null, min_vcpu: m.min_vcpu ?? null, max_vcpu: m.max_vcpu ?? null, max_ram_gib: m.max_ram_gib ?? null,
    always_on_month_per_instance: m.always_on_month_per_instance ?? null, requires_always_on: !!m.requires_always_on,
  }));
  const f = card.features || {};
  const keep = ['persistent_disk', 'docker_inside', 'browser', 'desktop', 'ssh', 'root', 'systemd', 'gpu', 'arm64',
    'pause_resume', 'snapshot', 'max_session_h', 'auto_stop_idle', 'open_source', 'self_host', 'byoc', 'regions'];
  const features = Object.fromEntries(keep.filter(k => f[k] !== undefined).map(k => [k, f[k]]));
  return {
    plans,
    modes,
    storage: card.storage || null,
    network: card.network ? {
      egress_free_gib: card.network.egress_free_gib ?? null,
      egress_gib: card.network.egress_gib ?? null,
      ipv4_month: card.network.ipv4_month ?? null,
      internet_default: card.network.internet ? card.network.internet.default : null,
    } : null,
    features,
  };
}

// A horizon can be delivered as one long session or split into shorter ones.
// A provider whose session cap is 8 h can still serve a 10 h day as two 5 h
// sessions; a user would do that. Every whole-minute session length of at least
// 30 minutes is tried and the cheapest eligible plan wins; on a tie the plan
// with fewest sessions (fewest restarts) is kept. The 30-minute floor keeps a
// 1-hour horizon from being gamed as sixty one-minute sessions.
const MIN_SESSION_MIN = 30;
function sessionPlans(totalHours) {
  const plans = [];
  const totalMin = Math.round(totalHours * 60);
  for (let n = 1; n <= Math.min(totalMin, 720); n++) {
    const sessionMin = totalMin / n;
    if (sessionMin < MIN_SESSION_MIN) break;
    if (Math.abs(sessionMin - Math.round(sessionMin)) > 1e-6) continue;
    plans.push({ sessions: n, sessionMin });
  }
  return plans;
}

const providers = cards.map(card => {
  const cost = {};
  for (const [id, def] of Object.entries(WORKLOADS)) {
    let best = null;
    let firstReasons = [];
    let firstMode = null;
    for (const pl of sessionPlans(def.total_minutes / 60)) {
      const w = Object.assign({}, SHAPE, { sessions: pl.sessions, sessionMin: pl.sessionMin });
      const r = price(card, w, true);
      if (!firstReasons.length) firstReasons = r.reasons;
      if (!firstMode) firstMode = r.mode;
      if (!r.eligible || r.total === null) continue;
      const nc = price(card, w, false);
      if (!best || r.total < best.total) {
        best = Object.assign({}, r, {
          sessions: pl.sessions, session_min: +pl.sessionMin.toFixed(2), mode: r.mode || firstMode,
          total_no_credit: nc.total,
          plan_limit: nc.plan === r.plan ? null : nc.plan,
        });
      }
    }
    cost[id] = best || { eligible: false, total: null, reasons: firstReasons, caveats: [], mode: firstMode };
  }
  const burst = {};
  for (const [id, def] of Object.entries(BURSTY)) {
    const w = Object.assign({}, SHAPE, { sessions: def.sessions, sessionMin: def.minutes });
    const r = price(card, w, true);
    const nc = price(card, w, false);
    burst[id] = {
      eligible: r.eligible, total: r.total, total_no_credit: nc.total,
      mode: r.mode, plan: r.plan, reasons: r.reasons, caveats: r.caveats,
      sessions: def.sessions, session_min: def.minutes,
    };
  }
  return {
    id: card.id,
    name: card.name,
    url: card.url,
    category: card.category,
    isolation: card.isolation,
    free: card.free || null,
    cost,
    burst,
    facts: facts(card),
  };
});

const out = {
  generated: new Date().toISOString().slice(0, 10),
  corpus: {
    source: 'ariana-dot-dev/battleships',
    commit: arg('--commit', 'f6a71ab09fefa68e355ef47c52315e099f99c921'),
    cards: cards.length,
    extra_cards: fs.existsSync(EXTRA) ? fs.readdirSync(EXTRA).filter(f => f.endsWith('.json')).map(f => f.replace(/\.json$/, '')) : [],
  },
  shape: SHAPE,
  method: 'each horizon is delivered as the cheapest eligible split into sessions (a 10 h day may be one 10 h session or two 5 h sessions); providers are ranked on that cheapest price',
  workloads: Object.fromEntries(Object.entries(WORKLOADS).map(([k, v]) => [k, { description: v.description, sessions: v.sessions, minutes: v.minutes, total_minutes: v.total_minutes }])),
  bursty: Object.fromEntries(Object.entries(BURSTY).map(([k, v]) => [k, { description: v.description, sessions: v.sessions, minutes: v.minutes, total_minutes: v.total_minutes }])),
  providers,
};
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
console.log(`wrote ${OUT}: ${providers.length} providers, ${Object.keys(WORKLOADS).length} workloads`);
console.log(`node ${process.version} on ${process.platform}/${process.arch}`);
for (const [id, def] of Object.entries(WORKLOADS)) {
  const n = providers.filter(p => p.cost[id].eligible).length;
  console.log(`  ${id}: ${n} eligible`);
}
