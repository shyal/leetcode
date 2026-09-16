#!/usr/bin/env python3

# lc_mocks - pull every mock assessment from leetcode.com/assessment/reports
# into data/mock_assessments.json, one record per session: company, stage,
# start time, time allotted and spent, score, percentile, and per question the
# number, slug, difficulty and testcases passed.
#
#   utils/history/lc_mocks.py            # fetch and write the cache
#   utils/history/lc_mocks.py --show     # print the cache as a table
#
# Login: the cookie file LC_COOKIE_FILE (default ~/.leetcode_cookies.json)
# written by `make lc-login`, the same one lc_submit reads. The queries are
# the ones the reports page itself runs (interviewSessions, then
# sessionAndReportData per session).

import argparse
import datetime as dt
import functools
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(ROOT, "data", "mock_assessments.json")
METADATA = os.path.join(ROOT, "data", "problems_metadata.json")
URL = "https://leetcode.com/graphql/"

SESSIONS = """
query interviewSessions($first: Int!, $after: String) {
  interviewAllSessions(first: $first, after: $after) {
    pageInfo { hasNextPage endCursor }
    edges { node { id } }
  }
}"""

SESSION = """
query sessionAndReportData($id: ID!) {
  interviewSession(id: $id) {
    id
    interview {
      questions { questionId title titleSlug difficulty }
      timeConstraint
    }
    startTime
    endTime
    expiredTime
    status
    progress { questionId status }
    card { company { name stage } stage }
    report {
      score
      percentile
      isDuplicateAttempt
      questions {
        questionId
        submission { numCorrect total statusDisplay lang }
      }
    }
  }
}"""


def _session():
    import requests

    path = os.path.expanduser(os.environ.get("LC_COOKIE_FILE", "~/.leetcode_cookies.json"))
    try:
        with open(path) as f:
            cookies = json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"no cookie file at {path}; run make lc-login")
    s = requests.Session()
    s.cookies.update(cookies)
    s.headers.update(
        {
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com/assessment/reports/",
            "x-csrftoken": cookies.get("csrftoken", ""),
        }
    )
    return s


def _query(s, query, variables):
    r = s.post(URL, json={"query": query, "variables": variables}, timeout=60)
    r.raise_for_status()
    body = r.json()
    if body.get("errors"):
        raise SystemExit(json.dumps(body["errors"], indent=2))
    return body["data"]


def session_ids(s):
    """Every session id, newest first, following the cursor."""
    ids, after = [], None
    while True:
        page = _query(s, SESSIONS, {"first": 50, "after": after})["interviewAllSessions"]
        ids.extend(e["node"]["id"] for e in page["edges"])
        if not page["pageInfo"]["hasNextPage"]:
            return ids
        after = page["pageInfo"]["endCursor"]


@functools.lru_cache(maxsize=None)
def _number_by_slug():
    """slug -> leetcode number, from data/problems_metadata.json. The API's
    questionId is an internal id, not the number the site shows."""
    with open(METADATA) as f:
        return {v["slug"]: int(n) for n, v in json.load(f).items()}


def _record(node):
    """One flat record from the sessionAndReportData node."""
    numbers = _number_by_slug()
    report = node.get("report") or {}
    subs = {q["questionId"]: q.get("submission") for q in report.get("questions") or []}
    progress = {p["questionId"]: p["status"] for p in node.get("progress") or []}
    start, end, expired = node["startTime"], node.get("endTime"), node.get("expiredTime")
    spent = (expired if node.get("status") == "TIMEOUT" else end) - start if start else None
    questions = []
    for q in node["interview"]["questions"]:
        sub = subs.get(q["questionId"]) or {}
        questions.append(
            {
                "id": q["questionId"],
                "number": numbers.get(q["titleSlug"]),
                "title": q["title"],
                "slug": q["titleSlug"],
                "difficulty": q["difficulty"],
                "status": progress.get(q["questionId"]),
                "passed": sub.get("numCorrect"),
                "total": sub.get("total"),
                "verdict": sub.get("statusDisplay"),
                "lang": sub.get("lang"),
            }
        )
    card = node.get("card") or {}
    company = card.get("company") or {}
    return {
        "id": node["id"],
        "company": company.get("name") or "Random Set",
        "stage": card.get("stage") or company.get("stage"),
        "date": dt.datetime.fromtimestamp(start, dt.timezone.utc).isoformat() if start else None,
        "status": node.get("status"),
        "allotted_s": node["interview"].get("timeConstraint"),
        "spent_s": spent,
        "score": report.get("score"),
        "percentile": report.get("percentile"),
        "duplicate": report.get("isDuplicateAttempt"),
        "questions": questions,
    }


def fetch():
    s = _session()
    records = []
    for sid in session_ids(s):
        node = _query(s, SESSION, {"id": sid})["interviewSession"]
        records.append(_record(node))
        print(f"{records[-1]['date']}  {records[-1]['company']}  {records[-1]['score']}", file=sys.stderr)
    records.sort(key=lambda r: r["date"] or "")
    with open(CACHE, "w") as f:
        json.dump(records, f, indent=1)
        f.write("\n")
    return records


def show(records):
    for r in records:
        qs = ", ".join(
            f"{q['number']}. {q['title']} [{q['difficulty'][0]}] {q['passed']}/{q['total']}" for q in r["questions"]
        )
        spent = f"{r['spent_s'] // 60}m" if r["spent_s"] is not None else "-"
        print(f"{(r['date'] or '')[:10]}  {r['company']:<11} {r['status']:<9} {spent:>4}/{r['allotted_s'] // 60}m  {r['score']}  {qs}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true", help="print the cache, no fetch")
    args = ap.parse_args()
    if args.show:
        with open(CACHE) as f:
            show(json.load(f))
        return
    show(fetch())


if __name__ == "__main__":
    main()
