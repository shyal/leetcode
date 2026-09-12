def main():
    import hashlib
    import json
    import os
    import re
    from concurrent.futures import ThreadPoolExecutor
    from datetime import datetime
    from typing import Any

    import boto3
    from boto3.s3.transfer import TransferConfig

    s3 = boto3.client("s3")
    bucket_name = "shyal"
    # single-part uploads only, so every object's ETag is the md5 of its
    # bytes and the dedupe below can compare without downloading
    transfer_config = TransferConfig(multipart_threshold=256 * 1024 * 1024)

    # README.md is the single source of truth (see fill() below); it is also
    # where the previous run's S3 keys live. Read it once up front and HEAD
    # every timestamped key it links, so an unchanged chart keeps its link
    # instead of landing on S3 again as a duplicate.
    f: Any
    with open("README.md", "r") as f:
        readme = f.read()
    existing = {}  # prefix -> key currently linked from README.md
    for key in re.findall(
        r"https://shyal\.s3\.amazonaws\.com/([a-z_]+_\d{14}\.(?:svg|png))", readme
    ):
        existing[key.rsplit("_", 1)[0]] = key

    def etag_of(key):
        try:
            return s3.head_object(Bucket=bucket_name, Key=key)["ETag"].strip('"')
        except s3.exceptions.ClientError:
            return None

    with ThreadPoolExecutor(max_workers=10) as pool:
        etags = dict(zip(existing, pool.map(etag_of, existing.values())))

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # every chart lands in a unique local path, so uploads can be queued as
    # they're produced and pushed concurrently at the end. Returns the S3 key
    # to link: the existing one when the bytes are identical to what is
    # already up there, else a fresh timestamped key queued for upload.
    upload_jobs = []
    unchanged = []

    def queue_upload(local, prefix, ext, extra):
        with open(local, "rb") as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        if prefix in existing and etags.get(prefix) == md5:
            unchanged.append(existing[prefix])
            return existing[prefix]
        key = f"{prefix}_{timestamp}.{ext}"
        upload_jobs.append((local, key, extra))
        return key

    # The four synced SMIL animations (kg_movie / kg_pass / positions /
    # calibration) go up gzipped with a Content-Encoding header — camo passes
    # it through, and near-equal transfer sizes keep their independent SMIL
    # clocks starting in near-lockstep. mtime=0 and no filename header keep
    # the gzip bytes a pure function of the SVG, so the dedupe can see
    # through the compression.
    def upload_svg_gz(path, prefix):
        import gzip

        local = f"/tmp/{prefix}.svg.gz"
        with open(path, "rb") as f, open(local, "wb") as raw, gzip.GzipFile(
            filename="", fileobj=raw, mode="wb", compresslevel=9, mtime=0
        ) as g:
            g.write(f.read())
        return queue_upload(
            local,
            prefix,
            "svg",
            {"ContentType": "image/svg+xml", "ContentEncoding": "gzip"},
        )

    # Chart generation is mostly disabled: the README carries the
    # problem-rating chart, the hours chart, the onsite chart, the backlog
    # chart and the two badges, nothing else. CHARTS is the
    # whole list of what gets picked up and linked - one row per generated
    # image. To bring a chart back, uncomment its row here and add its renderer
    # back to the readme target in the Makefile.
    #
    #   (graph file, s3 prefix, README region, alt text, inline region?)
    CHARTS = [
        # ("graph/elo.svg", "elo", "ELO_CHART", "Elo", False),
        (
            "graph/problem_rating.svg",
            "problem_rating",
            "PROBLEM_RATING_CHART",
            "Rating of the problems attempted",
            False,
        ),
        (
            "graph/hours.svg",
            "hours",
            "HOURS_CHART",
            "Elo against hours of recorded solving, with the Carnegie Mellon rate",
            False,
        ),
        (
            "graph/onsite.svg",
            "onsite",
            "ONSITE_CHART",
            "Elo history and its projection to the onsite line, on dates",
            False,
        ),
        (
            "graph/backlog.svg",
            "backlog",
            "BACKLOG_CHART",
            "Review backlog: open cards, due cards, due drills",
            False,
        ),
        ("graph/elo_badge.svg", "elo_badge", "ELO_BADGE", "Elo", True),
        ("graph/streak_badge.svg", "streak_badge", "STREAK_BADGE", "Streak", True),
        (
            "graph/rate_badge.svg",
            "rate_badge",
            "RATE_BADGE",
            "First-sight Elo per 100 hours",
            True,
        ),
        (
            "graph/rate_gauge.svg",
            "rate_gauge",
            "RATE_GAUGE",
            "Elo per 100 hours on problems seen for the first time",
            False,
        ),
        # ("graph/rates.svg", "rates", "SOLVES_CHART", "Solves and drills per day", False),
        # ("graph/commits.svg", "commits", "COMMITS_CHART", "Tooling commits versus solves", False),
        # ("graph/forecast.svg", "forecast", "FORECAST_CHART", "History and forecast to a 50% pass rate", False),
        # ("graph/calibration.svg", "curve_calibration", "CURVE_CALIBRATION_CHART", "Curve calibration", False),
        # ("graph/residuals.svg", "residuals", "RESIDUALS_CHART", "Residuals per group over time", False),
        # ("graph/timing.svg", "review_timing", "REVIEW_TIMING_CHART", "Review timing", False),
        # ("graph/solvetime.svg", "solvetime", "SOLVETIME_CHART", "How solve time changes with repetition and shared moves", False),
        # ("graph/connectivity.svg", "connectivity", "CONNECTIVITY_CHART", "Move connectivity vs solve time", False),
        # ("graph/reach.svg", "reach", "REACH_CHART", "Problems in reach", False),
        # ("graph/kg_pass.svg", "pass_probability", "PASS_PROB_CHART", "P(pass a mock) over time", False),
        # ("graph/kg_swarm.svg", "mock_swarm", "MOCK_SWARM_CHART", "Individual simulated mocks over time", False),
        # ("graph/kg_blame.svg", "mock_blame", "MOCK_BLAME_CHART", "Share of simulated problems failed, by group", False),
        # ("graph/positions.svg", "positions", "POSITIONS_SVG", "Nodes sliding down their forgetting curves", False),
        # ("graph/zpd.svg", "zpd", "ZPD_SVG", "The input tree of each of my last 50 solves, one per second", False),
        # ("graph/kg_movie.svg", "kg_movie", "KG_MOVIE", "Technique graph growing solve by solve", False),
        # ("graph/kg_3d.svg", "kg_3d", "KG_3D", "The technique graph in three dimensions, turning while the history replays", False),
        # ("graph/kg_full.svg", "kg_full", "KG_FULL", "Every node, problem and drill with every edge, each solve blinking its vertex", False),
        # ("graph/kg_compression.svg", "kg_compression", "KG_COMPRESSION", "One tile per node, one cell per problem or drill; tiles split as nodes are added, cells light as they are solved", False),
    ]
    # The two matplotlib readiness bars and the projection-stability chart went
    # with them; they were the only consumers of kg_mock --history-json and
    # kg_predict --history-json here (see git history to restore them).

    images = []  # (region, markdown, inline?)
    for path, prefix, region, alt, inline in CHARTS:
        if not os.path.exists(path):
            continue
        key = upload_svg_gz(path, prefix)
        images.append(
            (region, f"![{alt}](https://shyal.s3.amazonaws.com/{key})", inline)
        )

    # push everything queued above concurrently; boto3 clients are thread-safe.
    # Any failure raises here, before the README is touched.
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = [
            pool.submit(
                s3.upload_file,
                local,
                bucket_name,
                key,
                ExtraArgs=extra,
                Config=transfer_config,
            )
            for local, key, extra in upload_jobs
        ]
        for f in futures:
            f.result()
    print(f"uploaded {len(upload_jobs)}, unchanged {len(unchanged)}")

    # Prose is edited in README.md directly, and each generated block lives
    # between <!-- NAME --> ... <!-- /NAME --> markers (invisible on GitHub).
    # fill() rewrites only the inside of a region, so the script is idempotent
    # and never touches the prose. Empty content leaves a region as-is (same
    # semantics as the old conditionals).

    def fill(text, name, content):
        # keep the region's existing whitespace padding (formatters like to
        # put blank lines around the content; don't fight them)
        pat = re.compile(rf"<!-- {name} -->(\s*).*?(\s*)<!-- /{name} -->", re.S)
        if not content:
            return text
        m = pat.search(text)
        if not m:
            print(f"WARNING: no <!-- {name} --> region in README.md, skipped")
            return text
        lead = m.group(1) if "\n" in m.group(1) else "\n"
        trail = m.group(2) if "\n" in m.group(2) else "\n"
        return pat.sub(
            lambda _: f"<!-- {name} -->{lead}{content}{trail}<!-- /{name} -->", text
        )

    def fill_inline(text, name, value):
        # same markers, but inside a sentence: no forced newlines. Every
        # occurrence of the region gets the same value.
        pat = re.compile(rf"<!-- {name} -->.*?<!-- /{name} -->", re.S)
        if not pat.search(text):
            print(f"WARNING: no <!-- {name} --> region in README.md, skipped")
            return text
        return pat.sub(lambda _: f"<!-- {name} -->{value}<!-- /{name} -->", text)

    # inline numbers the prose claims, so they can never go stale
    with open("graph/nodes.json") as f:
        readme = fill_inline(readme, "N_NODES", len(json.load(f)["nodes"]))
    if os.path.exists("graph/reach.json"):
        with open("graph/reach.json") as f:
            r = json.load(f)
        readme = fill_inline(readme, "N_BANK", r["catalog"])
        readme = fill_inline(
            readme, "N_REACH_TODAY", f"~{round(r['predicted_reach'], -2):.0f}"
        )

    # the Elo figures the prose quotes: the median rating of the last problems
    # served, the moving average of the Elo, and that average's rate per 100
    # recorded hours, all from the chart scripts so the text and the charts
    # never disagree
    from importlib.machinery import SourceFileLoader

    def load(name):
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
        return SourceFileLoader(name, src).load_module()

    em, hm, om = load("kg_elo_svg"), load("kg_hours_svg"), load("kg_onsite_svg")
    gs = em.games()
    ma = em.elo_ma(gs)
    fs_rate, fs_early, fs_late = om.first_sight_rate(gs, hm.hours_by_day(), hm)
    readme = fill_inline(readme, "FS_RATE", f"{fs_rate * 100:+.0f}")
    readme = fill_inline(readme, "FS_EARLY", f"{fs_early:.0f}")
    readme = fill_inline(readme, "FS_LATE", f"{fs_late:.0f}")
    readme = fill_inline(readme, "FS_WINDOW", om.FS_WINDOW)
    readme = fill_inline(readme, "SERVED_MEDIAN", f"{om.served(gs)[-1][1]:.0f}")
    readme = fill_inline(readme, "ELO_MA", f"{ma[-1][1]:.0f}")
    readme = fill_inline(readme, "ELO_MA_WINDOW", em.MA)

    for region, markdown, inline in images:
        readme = (fill_inline if inline else fill)(readme, region, markdown)

    with open("README.md", "w") as f:
        f.write(readme)

    print("README updated with S3 image links!")


if __name__ == "__main__":
    main()
