#!/usr/bin/env node
// contest_field.mjs: the field of each contest in contests/*.json, written
// to contests/<stem>.field.json for the virtual contest rating
// (kg::contests::leetcode_rating). Run by `make contest-field`.
//
// LeetCode's rating formula needs the rating of every participant in the
// field before the contest. CLIST keeps the standings of every LeetCode
// contest with each rated participant's place and rating change, so the
// rating before the contest is the new rating less the change. The
// contest is found by its event name on CLIST's LeetCode resource; the
// standings come 1000 rows a page, paced to CLIST's rate limit as
// kg::tables::fetch_clist is.
//
// LeetCode's own participant count (the contest JSON's "field") is larger
// than CLIST's rows: the difference is the participants CLIST has no
// rating row for, and the Rust side rates them 1500, LeetCode's rating
// for a first contest. The field file records both counts.
//
// A contest is skipped when its field file exists. Credentials:
// CLIST_USERNAME and CLIST_API_KEY, from the environment or .envrc.

import { existsSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const CONTESTS = path.join(ROOT, 'contests');
const API = 'https://clist.by/api/v4';
const RESOURCE = 102;
const PAGE = 1000;
const PAUSE_MS = 6500;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/// CLIST_USERNAME and CLIST_API_KEY from the environment, else .envrc.
function credentials() {
  let user = process.env.CLIST_USERNAME;
  let key = process.env.CLIST_API_KEY;
  if (!user || !key) {
    const envrc = path.join(ROOT, '.envrc');
    if (existsSync(envrc)) {
      const text = readFileSync(envrc, 'utf8');
      const get = (k) => (text.match(new RegExp(`^export ${k}=["']?([^"'\\n]+)`, 'm')) || [])[1];
      user = user || get('CLIST_USERNAME');
      key = key || get('CLIST_API_KEY');
    }
  }
  if (!user || !key) throw new Error('set CLIST_USERNAME and CLIST_API_KEY (see .envrc)');
  return `ApiKey ${user}:${key}`;
}

async function api(auth, query) {
  for (let attempt = 0; attempt < 4; attempt++) {
    const r = await fetch(`${API}/${query}`, { headers: { Authorization: auth } });
    const text = await r.text();
    if (r.status === 200) return JSON.parse(text);
    if (r.status === 429) {
      await sleep(PAUSE_MS * (attempt + 2));
      continue;
    }
    throw new Error(`clist ${r.status}: ${text.slice(0, 200)}`);
  }
  throw new Error(`clist: rate limited on ${query}`);
}

/// The CLIST contest with this event name, or null.
async function findContest(auth, event) {
  const re = encodeURIComponent(`^${event.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`);
  const d = await api(auth, `contest/?resource_id=${RESOURCE}&event__regex=${re}&format=json`);
  return d.objects[0] || null;
}

/// Every participant's rating before the contest, in place order.
async function ratings(auth, contestId) {
  const out = [];
  for (let offset = 0; ; offset += PAGE) {
    if (offset > 0) await sleep(PAUSE_MS);
    const d = await api(auth, `statistics/?contest_id=${contestId}&limit=${PAGE}&offset=${offset}&order_by=place&format=json`);
    for (const row of d.objects) {
      let before = null;
      if (typeof row.new_rating === 'number' && typeof row.rating_change === 'number') before = row.new_rating - row.rating_change;
      else if (typeof row.old_rating === 'number') before = row.old_rating;
      if (before !== null) out.push(before);
    }
    process.stdout.write(`  ${out.length} ratings\r`);
    if (d.objects.length < PAGE) break;
  }
  process.stdout.write('\n');
  return out;
}

function load(p) {
  return JSON.parse(readFileSync(p, 'utf8'));
}

async function main() {
  const auth = credentials();
  const names = readdirSync(CONTESTS)
    .filter((n) => n.endsWith('.json') && !n.endsWith('.field.json'))
    .sort();
  let failed = 0;
  for (const name of names) {
    const out = path.join(CONTESTS, name.replace(/\.json$/, '.field.json'));
    if (existsSync(out)) {
      console.log(`${name}: field present, skipped`);
      continue;
    }
    const contest = load(path.join(CONTESTS, name));
    try {
      const c = await findContest(auth, contest.contest);
      if (!c) throw new Error(`${contest.contest}: not on CLIST`);
      console.log(`${contest.contest}: CLIST contest ${c.id}, ${c.n_statistics} rows`);
      const rs = await ratings(auth, c.id);
      if (!rs.length) {
        throw new Error(
          `${contest.contest}: CLIST has its standings but no rating changes yet (LeetCode publishes them a day or two after the contest); run make contest-field again later`,
        );
      }
      const field = {
        source: 'clist',
        clist_contest_id: c.id,
        event: c.event,
        fetched: new Date().toISOString().slice(0, 10),
        user_num: Math.max(contest.field || 0, rs.length),
        rated: rs.length,
        ratings: rs,
      };
      writeFileSync(out, JSON.stringify(field) + '\n');
      console.log(`${name}: ${rs.length} rated of ${field.user_num} participants -> ${path.basename(out)}`);
    } catch (e) {
      failed += 1;
      console.log(`${name}: ${e.message || e}`);
    }
  }
  if (failed) process.exit(1);
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
