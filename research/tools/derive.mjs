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

const ENGINE = path.join(CORPUS, 'site', 'engine.js');
const CARDS = path.join(CORPUS, 'research', 'cards');
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

// Workloads. All fixed; see README for why these three.
const BASE = {
  os: 'linux', arch: 'any', gpu: 'none', gpuCount: 1, ipv4: 0, seats: 1,
  persistentDisk: false, snapshotGiB: 0, egress: 0, alwaysOn: 0,
  sessions: 0, sessionMin: 0, concurrency: 0, cpuUtil: 0.1, ramUtil: 0.5,
};
const WORKLOADS = {
  'nano-box': {
    description: 'One tiny always-on box: 1 vCPU / 1 GiB / 10 GiB, 24/7, 20 GiB egress out. The floor of the market.',
    w: { vcpu: 1, ram: 1, disk: 10, alwaysOn: 1, egress: 20, persistentDisk: true },
  },
  'agent-box': {
    description: 'One always-on agent box: 2 vCPU / 4 GiB / 20 GiB, 24/7, 100 GiB egress out.',
    w: { vcpu: 2, ram: 4, disk: 20, alwaysOn: 1, egress: 100, persistentDisk: true },
  },
  'interp': {
    description: 'Code-interpreter bursts: 1 vCPU / 2 GiB / 5 GiB, 200,000 sessions of 1 minute, 100 at once.',
    w: { vcpu: 1, ram: 2, disk: 5, sessions: 200000, sessionMin: 1, concurrency: 100, egress: 20 },
  },
  'devbox': {
    description: 'A 24/7 developer box: 4 vCPU / 8 GiB / 50 GiB, 50 GiB egress out.',
    w: { vcpu: 4, ram: 8, disk: 50, alwaysOn: 1, egress: 50, persistentDisk: true },
  },
};

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
    boot_overhead_s: m.boot_overhead_s ?? null, commit_note: m.commit_note || null,
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

const providers = cards.map(card => {
  const cost = {};
  for (const [id, def] of Object.entries(WORKLOADS)) {
    const withCredits = price(card, def.w, true);
    const noCredits = price(card, def.w, false);
    cost[id] = Object.assign({}, withCredits, {
      total_no_credit: noCredits.total,
      plan_limit: noCredits.plan === withCredits.plan ? null : noCredits.plan,
    });
  }
  return {
    id: card.id,
    name: card.name,
    url: card.url,
    category: card.category,
    isolation: card.isolation,
    free: card.free || null,
    cost,
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
  workloads: Object.fromEntries(Object.entries(WORKLOADS).map(([k, v]) => [k, v])),
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
