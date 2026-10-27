#!/usr/bin/env node
// contest_field.mjs: a sample of the field of each contest in contests/*.json,
// written to contests/<stem>.field.json, for the virtual contest rating
// (kg::contests::leetcode_rating). Run by `make contest-field`.
//
// LeetCode's rating formula needs the rating of every participant in the
// field. The ranking API lists the field 25 users to a page, and the
// GraphQL endpoints give a user's rating. Both sit behind Cloudflare, so
// the requests go through the Brave session (~/dev/claude-brave-control):
// each ranking page opens in a background tab of its own and the JSON is
// read from the page once the tab's title is no longer the challenge; the
// ratings are fetched from a leetcode.com tab (US users) and a leetcode.cn
// tab (CN users). FIELD_PAGES random pages are drawn with a fixed seed, so
// a rerun draws the same pages.
//
// A tab is only attached to (DevTools) after its page has loaded: the
// challenge does not complete in a tab that is already attached.
//
// The field file records the rating of each sampled user as of the fetch
// date, not as of the contest. For a contest sat days ago that is the same
// number; for an old contest it is the field as it stands today.
//
// A contest is skipped when its field file already holds every page; a
// partial file (an interrupted run) is continued.

import { existsSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { connect } from '/Users/orb/dev/claude-brave-control/lib/cdp.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const CONTESTS = path.join(ROOT, 'contests');
const PAGES = Number(process.env.FIELD_PAGES || 24);
const PER_PAGE = 25;
const SEED = 20261027;
const BATCH = 25;
const WAIT_MS = 120000;

const US = 'https://leetcode.com';
const CN = 'https://leetcode.cn';
const US_GQL = '/graphql';
const CN_GQL = '/graphql/noj-go/';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/// mulberry32: a small seeded generator, the same pages on every run.
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/// k distinct pages in 1..=n, in draw order.
function samplePages(n, k) {
  const next = rng(SEED);
  const seen = new Set();
  const out = [];
  while (out.length < Math.min(k, n)) {
    const p = 1 + Math.floor(next() * n);
    if (!seen.has(p)) {
      seen.add(p);
      out.push(p);
    }
  }
  return out;
}

/// Open url in a background tab and return the tab once its title is a
/// page and not the challenge. The title comes from the DevTools list,
/// so nothing attaches to the tab while the challenge runs.
async function openSettled(browser, url) {
  const page = await browser.contexts()[0].newPage(url);
  const start = Date.now();
  while (Date.now() - start < WAIT_MS) {
    await sleep(1500);
    const title = await page.title().catch(() => '');
    if (title && !/just a moment|security verification/i.test(title)) return page;
  }
  await page.close().catch(() => {});
  throw new Error(`${url}: still on the challenge after ${WAIT_MS / 1000}s`);
}

/// The JSON a URL serves, read from a tab of its own.
async function readJson(browser, url) {
  const page = await openSettled(browser, url);
  try {
    const text = await page.evaluate('document.body ? document.body.innerText : ""');
    return JSON.parse(text);
  } finally {
    await page.close().catch(() => {});
  }
}

/// POST a GraphQL query from the tab; the data object, or null.
async function gql(page, pathname, query) {
  for (let attempt = 0; attempt < 4; attempt++) {
    const r = await page
      .evaluate(
        `(async () => { const r = await fetch(${JSON.stringify(pathname)}, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ query: ${JSON.stringify(query)} }) }); return { status: r.status, text: await r.text() }; })()`,
      )
      .catch((e) => ({ status: 0, text: String(e) }));
    if (r.status === 200) {
      try {
        return JSON.parse(r.text).data || null;
      } catch {
        // fall through to the retry
      }
    }
    await sleep(3000 * (attempt + 1));
  }
  return null;
}

/// {user: {rating, contests}} for the users that answer; a user with no
/// contest history answers null and is left out (rated 1500 later).
async function ratings(page, pathname, users, arg) {
  const out = {};
  for (let i = 0; i < users.length; i += BATCH) {
    const chunk = users.slice(i, i + BATCH);
    const q = chunk
      .map((u, j) => `u${j}: userContestRanking(${arg}: ${JSON.stringify(u)}) { rating attendedContestsCount }`)
      .join(' ');
    const d = await gql(page, pathname, `query { ${q} }`);
    if (!d) {
      console.log(`  ${pathname}: no answer for a batch of ${chunk.length}`);
      continue;
    }
    chunk.forEach((u, j) => {
      const e = d[`u${j}`];
      if (e && typeof e.rating === 'number') out[u] = { rating: e.rating, contests: e.attendedContestsCount || 0 };
    });
  }
  return out;
}

function load(p) {
  return JSON.parse(readFileSync(p, 'utf8'));
}

function save(p, v) {
  writeFileSync(p, JSON.stringify(v, null, 1) + '\n');
}

async function field(browser, contest, out) {
  const slug = contest.slug;
  const api = (p) => `${US}/contest/api/ranking/${slug}/?pagination=${p}&region=global`;
  let f = existsSync(out) ? load(out) : null;
  if (!f) {
    const first = await readJson(browser, api(1));
    const n = Math.ceil(first.user_num / PER_PAGE);
    f = {
      slug,
      fetched: new Date().toISOString().slice(0, 10),
      user_num: first.user_num,
      pages_total: n,
      pages: samplePages(n, PAGES),
      pages_done: [],
      users: [],
    };
    save(out, f);
  }
  for (const p of f.pages) {
    if (f.pages_done.includes(p)) continue;
    const j = await readJson(browser, api(p));
    for (const u of j.total_rank) {
      f.users.push({ username: u.username, slug: u.user_slug, region: u.data_region, rank: u.rank, rating: null, contests: null });
    }
    f.pages_done.push(p);
    save(out, f);
    console.log(`${slug}: page ${p} (${f.pages_done.length}/${f.pages.length}), ${f.users.length} users`);
  }
  const missing = f.users.filter((u) => !u.asked);
  if (missing.length) {
    const usNames = missing.filter((u) => u.region !== 'CN').map((u) => u.username);
    const cnSlugs = missing.filter((u) => u.region === 'CN').map((u) => u.slug);
    let got = {};
    if (usNames.length) {
      const us = await openSettled(browser, `${US}/contest/`);
      try {
        got = await ratings(us, US_GQL, usNames, 'username');
      } finally {
        await us.close().catch(() => {});
      }
    }
    let gotCn = {};
    if (cnSlugs.length) {
      const cn = await openSettled(browser, `${CN}/contest/`);
      try {
        gotCn = await ratings(cn, CN_GQL, cnSlugs, 'userSlug');
      } finally {
        await cn.close().catch(() => {});
      }
    }
    for (const u of missing) {
      const r = u.region === 'CN' ? gotCn[u.slug] : got[u.username];
      if (r) {
        u.rating = r.rating;
        u.contests = r.contests;
      }
      u.asked = true;
    }
    save(out, f);
    const rated = f.users.filter((u) => u.rating !== null).length;
    console.log(`${slug}: ${rated} of ${f.users.length} sampled users have a rating`);
  }
}

async function main() {
  const names = readdirSync(CONTESTS).filter((n) => n.endsWith('.json') && !n.endsWith('.field.json')).sort();
  const browser = await connect();
  try {
    for (const name of names) {
      const contest = load(path.join(CONTESTS, name));
      if (!contest.slug) {
        console.log(`${name}: no slug, skipped`);
        continue;
      }
      const out = path.join(CONTESTS, name.replace(/\.json$/, '.field.json'));
      if (existsSync(out)) {
        const f = load(out);
        if (f.pages_done.length === f.pages.length && f.users.every((u) => u.asked)) {
          console.log(`${name}: field complete, skipped`);
          continue;
        }
      }
      await field(browser, contest, out);
    }
  } finally {
    await browser.close();
  }
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
