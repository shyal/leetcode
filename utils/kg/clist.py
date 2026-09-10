#!/usr/bin/env python3

# clist - CLIST's problem table for leetcode, cached on disk.
#
# CLIST (clist.by) rates problems from contest standings, computed
# independently of zerotrac's table in data/leetcode_ratings.tsv. Both cover
# only problems that ran in a contest, but their contest coverage differs, so
# the union is larger than either.
#
#   utils/kg/clist.py --refresh        # fetch every leetcode problem, cache it
#   utils/kg/clist.py --stats          # coverage and agreement with zerotrac
#
# Importing this module never touches the network: rating() and problems()
# answer from data/clist_problems.json and raise if it is missing. The API
# wants CLIST_USERNAME and CLIST_API_KEY (both in .envrc) and allows 10
# requests a minute, so a refresh paces itself and takes about a minute.

import functools
import json
import os
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(ROOT, "data", "clist_problems.json")
METADATA = os.path.join(ROOT, "data", "problems_metadata.json")
RATINGS = os.path.join(ROOT, "data", "leetcode_ratings.tsv")

API = "https://clist.by/api/v4/problem/"
RESOURCE_ID = 102  # leetcode.com
PAGE = 1000
SECONDS_PER_REQUEST = 6.5  # the documented limit is 10 requests a minute
FIELDS = ("name", "slug", "rating", "n_accepted", "n_total", "time", "kinds")


def _fetch_page(offset, user, key):
    url = (
        f"{API}?resource_id={RESOURCE_ID}&limit={PAGE}&offset={offset}"
        f"&order_by=id&format=json"
    )
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"ApiKey {user}:{key}",
            "User-Agent": "leet/clist.py",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def refresh(verbose=True):
    """Page through every leetcode problem CLIST knows and write the cache."""
    user = os.environ.get("CLIST_USERNAME")
    key = os.environ.get("CLIST_API_KEY")
    if not user or not key:
        raise SystemExit("set CLIST_USERNAME and CLIST_API_KEY (see .envrc)")
    rows, offset = [], 0
    while True:
        if offset:
            time.sleep(SECONDS_PER_REQUEST)
        data = _fetch_page(offset, user, key)
        objs = data["objects"]
        for o in objs:
            if o.get("slug"):
                rows.append({f: o.get(f) for f in FIELDS})
        if verbose:
            print(f"  offset {offset}: {len(objs)} problems, {len(rows)} kept")
        if len(objs) < PAGE:
            break
        offset += PAGE
    rows.sort(key=lambda r: r["slug"])
    with open(CACHE, "w") as f:
        json.dump(rows, f, indent=1, sort_keys=True)
    if verbose:
        rated = sum(1 for r in rows if r["rating"])
        print(f"wrote {CACHE}: {len(rows)} problems, {rated} rated")
    return rows


@functools.lru_cache(maxsize=1)
def problems():
    """The cached table, oldest cache is fine - ratings barely move. Parsed
    once per process: the picker asks for ratings on every pick."""
    if not os.path.exists(CACHE):
        raise SystemExit(f"no cache at {CACHE}; run utils/kg/clist.py --refresh")
    with open(CACHE) as f:
        return tuple(tuple(sorted(r.items())) for r in json.load(f))


def by_slug():
    return {dict(r)["slug"]: dict(r) for r in problems()}


def slug_of_number():
    """leetcode number -> slug, from data/problems_metadata.json."""
    with open(METADATA) as f:
        meta = json.load(f)
    return {num: m["slug"] for num, m in meta.items() if m.get("slug")}


def ratings_by_number():
    """leetcode number -> CLIST rating, for the problems it rates."""
    table = by_slug()
    out = {}
    for num, slug in slug_of_number().items():
        row = table.get(slug)
        if row and row.get("rating"):
            out[num] = float(row["rating"])
    return out


def zerotrac_by_number():
    """leetcode number -> zerotrac rating, from data/leetcode_ratings.tsv."""
    import csv

    with open(RATINGS) as f:
        return {r["id"]: float(r["rating"]) for r in csv.DictReader(f, delimiter="\t")}


def rescale():
    """(intercept, slope) putting CLIST ratings on zerotrac's scale, fitted on
    the problems both rate. The two correlate at r = 0.97 but CLIST's scale is
    the wider one, so a rating is only comparable after this."""
    import statistics

    clist, zt = ratings_by_number(), zerotrac_by_number()
    both = sorted(set(clist) & set(zt))
    xs = [clist[n] for n in both]
    ys = [zt[n] for n in both]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    var = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / var
    return my - slope * mx, slope


@functools.lru_cache(maxsize=1)
def _combined():
    a, b = rescale()
    out = {n: a + b * r for n, r in ratings_by_number().items()}
    out.update(zerotrac_by_number())
    return out


def combined_ratings():
    """leetcode number -> rating, zerotrac where it has one and rescaled CLIST
    everywhere else. This is the only table with the classic pre-contest hards
    (42, 23, 124) in it."""
    return _combined()


def write_ratings(path=None):
    """graph/ratings.json: problem number -> rating, the combined table. The
    Rust mock reads it; kg_curve rewrites it on every fit."""
    path = path or os.path.join(ROOT, "graph", "ratings.json")
    table = {
        n: round(r, 1)
        for n, r in sorted(combined_ratings().items(), key=lambda kv: int(kv[0]))
    }
    with open(path, "w") as f:
        json.dump(table, f, indent=1)
    return path


def rating(number):
    """One problem's rating on zerotrac's scale, or None."""
    return combined_ratings().get(str(number))


def main():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="fetch from the API and rewrite the cache",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="coverage against zerotrac and where they disagree",
    )
    parser.add_argument(
        "--write", action="store_true", help="rewrite graph/ratings.json from the cache"
    )
    args = parser.parse_args()
    if args.refresh:
        refresh()
    if args.write:
        print(f"wrote {write_ratings()}")
    if args.stats:
        import statistics

        clist, zt = ratings_by_number(), zerotrac_by_number()
        both = sorted(set(clist) & set(zt))
        print(
            f"clist rates {len(clist)}, zerotrac rates {len(zt)}, "
            f"both {len(both)}, union {len(set(clist) | set(zt))}"
        )
        print(
            f"clist only: {len(set(clist) - set(zt))}   "
            f"zerotrac only: {len(set(zt) - set(clist))}"
        )
        if both:
            d = [clist[n] - zt[n] for n in both]
            d.sort()
            print(
                f"clist - zerotrac on the overlap: median {statistics.median(d):+.0f}, "
                f"mean {statistics.mean(d):+.0f}, sd {statistics.pstdev(d):.0f}"
            )
            print(
                f"  p10 {d[len(d) // 10]:+.0f}  p90 {d[9 * len(d) // 10]:+.0f}  "
                f"within 100 points: {sum(1 for x in d if abs(x) <= 100) / len(d):.0%}"
            )
            a, b = rescale()
            res = [zt[n] - (a + b * clist[n]) for n in both]
            print(
                f"on zerotrac's scale: zerotrac ~ {a:.0f} + {b:.3f} * clist, "
                f"residual sd {statistics.pstdev(res):.0f}"
            )
            print(f"combined table: {len(combined_ratings())} problems rated")
    if not (args.refresh or args.stats or args.write):
        parser.print_help()


if __name__ == "__main__":
    main()
