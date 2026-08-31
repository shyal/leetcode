def main():
    import git
    import os
    import re
    import subprocess
    import sys
    from datetime import datetime, timedelta, date
    from collections import defaultdict
    import matplotlib as mpl
    import boto3
    import numpy as np
    import json
    from history.metadata import get_problems_metadata

    mpl.use("Agg")
    import matplotlib.pyplot as plt

    import hashlib
    from concurrent.futures import ThreadPoolExecutor
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

    # Solve and drill rates (utils/readme/kg_rates_svg): one SVG, two
    # stacked panels (per day, unique per day), replacing the two matplotlib
    # PNGs that only knew about problems.
    rates_img = ""
    if os.path.exists("graph/rates.svg"):
        s3_key_rates = upload_svg_gz("graph/rates.svg", "rates")
        rates_img = f"![Solves and drills per day](https://shyal.s3.amazonaws.com/{s3_key_rates})"

    # Cumulative tooling commits versus solve commits
    # (utils/readme/kg_commits_svg): one panel, two lines.
    commits_img = ""
    if os.path.exists("graph/commits.svg"):
        s3_key_commits = upload_svg_gz("graph/commits.svg", "commits")
        commits_img = f"![Tooling commits versus solves](https://shyal.s3.amazonaws.com/{s3_key_commits})"

    # One projection-stability chart: each model's projected ready date over
    # run date, recomputed on the fly for EVERY day since the first evidence
    # record (no stored snapshots): kg_mock --history-json replays the
    # Monte-Carlo mock milestones, kg_predict --history-json the work-done
    # simulator. Each day's point uses only the evidence and git log visible
    # on that day; the math is today's model throughout.
    mock_bin = "utils/kg/kg_mock_rs/target/release/kg_mock"
    mock_history = json.loads(
        subprocess.run([mock_bin, "--history-json"],
                       capture_output=True, text=True, check=True).stdout
    )
    predict_history = json.loads(
        subprocess.run([sys.executable, "utils/kg/kg_predict", "--history-json"],
                       capture_output=True, text=True, check=True,
                       env={**os.environ, "PYTHONPATH": "utils"}).stdout
    )

    projection_img = ""
    proj_series = [
        (mock_history, "hard_competent", "contest: mock hard-competent", "#1f77b4"),
        (mock_history, "onsite_ready", "onsite: mock P(onsite)>=50%", "#ff7f0e"),
        (predict_history, "ready", "work done: kg_predict", "#2ca02c"),
    ]
    fig, ax = plt.subplots(figsize=(12, 5))
    plotted_any = False
    for series, key, label, color in proj_series:
        pts = [(e["run_date"], e[key]) for e in series if e.get(key)]
        if not pts:
            continue
        xs = [datetime.strptime(x, "%Y-%m-%d") for x, _ in pts]
        ys = [datetime.strptime(y, "%Y-%m-%d") for _, y in pts]
        ax.plot(xs, ys, label=label, color=color)
        plotted_any = True
    if plotted_any:
        ax.set_title("Projected Ready Dates Over Time")
        ax.set_xlabel("Run Date")
        ax.set_ylabel("Projected Ready Date")
        ax.legend()
        fig.autofmt_xdate()
        fig.tight_layout()
        local_path = "/tmp/readiness_projection.png"
        fig.savefig(local_path)
        s3_key_projection = queue_upload(
            local_path, "readiness_projection", "png", {"ContentType": "image/png"})
        projection_img = f"![Projected ready dates over time](https://shyal.s3.amazonaws.com/{s3_key_projection})"
    plt.close(fig)

    if mock_history:
        last_readiness = mock_history[-1]
        # headline dates come from the Monte-Carlo mock milestones (contest =
        # hard-competent, onsite = central P(onsite) >= 50%); kg_predict's
        # work-done date is the only fallback
        contest_date_str = last_readiness.get("hard_competent")
        faang_date_str = last_readiness.get("onsite_ready") or predict_history[-1]["ready"]
        faang_hours = last_readiness.get("hours")
        run_day = datetime.strptime(last_readiness["run_date"], "%Y-%m-%d")

        def days_out(d_str):
            return (datetime.strptime(d_str, "%Y-%m-%d") - run_day).days

        contest_end_str = (
            f"{contest_date_str}, in {days_out(contest_date_str)} days"
            if contest_date_str else None
        )
        faang_end_str = faang_date_str
        if faang_end_str:
            if faang_hours:
                faang_end_str = f"{faang_end_str} at {faang_hours:g}h/day"
            faang_end_str = f"{faang_end_str}, in {days_out(faang_date_str)} days"

        # The bars plot the SAME quantity the projected dates are defined by:
        # today's central Monte-Carlo pass rate, against the 50% ready mark.
        # A 9% bar next to a 2027 date is coherent; the old graph-solidity
        # bars (90%+ next to a far date) were not.
        def prob_bar(p, ready_date, title, xlabel, color, fname, s3_prefix, alt):
            fig, ax = plt.subplots(figsize=(10, 2))
            ax.barh([0], [p * 100], height=0.5, color=color)
            ax.axvline(50, color="#DD0000", linestyle="--", linewidth=1.5)
            ax.text(51, 0.18, "ready = 50%", color="#DD0000", fontsize=9)
            ax.text(p * 100 + 1, 0, f"{p * 100:.0f}%", va="center", fontweight="bold")
            ax.set_yticks([])
            ax.set_xlim(0, 100)
            ax.set_xlabel(xlabel)
            note = f" (projected ready {ready_date})" if ready_date else ""
            ax.set_title(title + note)
            local_path = f"/tmp/{fname}.png"
            fig.savefig(local_path, bbox_inches="tight")
            s3_key = queue_upload(local_path, s3_prefix, "png", {"ContentType": "image/png"})
            plt.close(fig)
            alt_note = f" (Ready by {ready_date})" if ready_date else ""
            return f"![{alt}{alt_note}](https://shyal.s3.amazonaws.com/{s3_key})"

        mock_hard = last_readiness.get("hard")
        mock_onsite = last_readiness.get("onsite")
        contest_progress_img = ""
        faang_progress_img = ""
        if mock_hard is not None:
            contest_progress_img = prob_bar(
                mock_hard, contest_end_str,
                "Contest Readiness",
                "today's central P(clear a single hard), %",
                "#1f77b4", "contest_progress", "contest_progress",
                "Contest Readiness Progress",
            )
        if mock_onsite is not None:
            faang_progress_img = prob_bar(
                mock_onsite, faang_end_str,
                "FAANG Interview Readiness",
                "today's central P(pass onsite: 2E + 2M + >=1 hard), %",
                "#ff7f0e", "faang_progress", "faang_progress",
                "FAANG Interview Readiness Progress",
            )

    else:
        contest_progress_img = "No readiness data."
        faang_progress_img = "No readiness data."

    # History and forecast (utils/readme/kg_forecast_svg): cumulative solves,
    # STALE/FRAGILE counts and the pass rates day by day, then kg_simulate's
    # run of the real picker until P(onsite) reaches 50%, on one time axis.
    forecast_img = ""
    if os.path.exists("graph/forecast.svg"):
        s3_key_forecast = upload_svg_gz("graph/forecast.svg", "forecast")
        forecast_img = f"![History and forecast to a 50% pass rate](https://shyal.s3.amazonaws.com/{s3_key_forecast})"

    # Forgetting-curve calibration (utils/readme/kg_calibration_svg): model vs
    # observed clean-recall by gap, replayed weekly as a SMIL SVG on the
    # shared clock — the fourth synced animation.
    curve_calibration_img = ""
    if os.path.exists("graph/calibration.svg"):
        s3_key_calib = upload_svg_gz("graph/calibration.svg", "curve_calibration")
        curve_calibration_img = f"![Curve calibration](https://shyal.s3.amazonaws.com/{s3_key_calib})"

    # Residuals over time (utils/readme/kg_residuals_svg): make residuals as a
    # running z per group, stepping trial by trial on the shared clock.
    residuals_img = ""
    if os.path.exists("graph/residuals.svg"):
        s3_key_residuals = upload_svg_gz("graph/residuals.svg", "residuals")
        residuals_img = f"![Residuals per group over time](https://shyal.s3.amazonaws.com/{s3_key_residuals})"

    # Review timing (utils/readme/kg_timing_svg): every recall trial's gap vs the
    # predicted solid window — the scheduler's report card, on the shared
    # clock.
    review_timing_img = ""
    if os.path.exists("graph/timing.svg"):
        s3_key_timing = upload_svg_gz("graph/timing.svg", "review_timing")
        review_timing_img = f"![Review timing](https://shyal.s3.amazonaws.com/{s3_key_timing})"

    # Solve-time drivers (utils/readme/kg_solvetime_svg): paired re-solve ratios
    # warm vs cold, and median minutes by move connectivity.
    solvetime_img = ""
    if os.path.exists("graph/solvetime.svg"):
        s3_key_solvetime = upload_svg_gz("graph/solvetime.svg", "solvetime")
        solvetime_img = f"![How solve time changes with repetition and shared moves](https://shyal.s3.amazonaws.com/{s3_key_solvetime})"

    # Connectivity zoom (utils/readme/kg_connectivity_svg): every timed solve vs how
    # many problems share its moves, running medians per difficulty.
    connectivity_img = ""
    if os.path.exists("graph/connectivity.svg"):
        s3_key_conn = upload_svg_gz("graph/connectivity.svg", "connectivity")
        connectivity_img = f"![Move connectivity vs solve time](https://shyal.s3.amazonaws.com/{s3_key_conn})"

    # Problems in reach (utils/readme/kg_reach_svg): today's walked frontier replayed
    # against historical node states - the payoff curve, on the shared clock.
    reach_img = ""
    if os.path.exists("graph/reach.svg"):
        s3_key_reach = upload_svg_gz("graph/reach.svg", "reach")
        reach_img = f"![Problems in reach](https://shyal.s3.amazonaws.com/{s3_key_reach})"

    # P(pass) history — the headline "how good am i" line, now rendered by
    # utils/kg/kg_movie_rs (`make movie`) as a SMIL-animated SVG synced with the
    # technique-graph movie: the same weekly replay + kg_lib cold-mock Monte
    # Carlo (the kg_mock lib reproduces the math bit-for-bit), revealed
    # left-to-right on the movie's clock.
    pass_prob_img = ""
    if os.path.exists("graph/kg_pass.svg"):
        s3_key_pass = upload_svg_gz("graph/kg_pass.svg", "pass_probability")
        pass_prob_img = f"![P(pass a mock) over time](https://shyal.s3.amazonaws.com/{s3_key_pass})"

    # Mock swarm (utils/kg/kg_movie_rs, same binary): individual simulated
    # mocks with fixed dice, hopping bins as skill improves, on the shared
    # clock.
    mock_swarm_img = ""
    if os.path.exists("graph/kg_swarm.svg"):
        s3_key_swarm = upload_svg_gz("graph/kg_swarm.svg", "mock_swarm")
        mock_swarm_img = f"![Individual simulated mocks over time](https://shyal.s3.amazonaws.com/{s3_key_swarm})"

    # And the failure-attribution view (same binary): failed simulated
    # problems blamed on the weakest move in their walk, by technique group.
    mock_blame_img = ""
    if os.path.exists("graph/kg_blame.svg"):
        s3_key_blame = upload_svg_gz("graph/kg_blame.svg", "mock_blame")
        mock_blame_img = f"![Share of simulated problems failed, by group](https://shyal.s3.amazonaws.com/{s3_key_blame})"

    # Animated SVG (utils/readme/kg_positions_svg): every node sliding down its
    # personal forgetting curve, replaying the same history on the same clock
    # as the two SVGs above.
    positions_svg_img = ""
    if os.path.exists("graph/positions.svg"):
        s3_key_positions = upload_svg_gz("graph/positions.svg", "positions")
        positions_svg_img = f"![Nodes sliding down their forgetting curves](https://shyal.s3.amazonaws.com/{s3_key_positions})"

    # Zone of proximal development (utils/readme/kg_zpd_svg): the input tree
    # of each of the last 50 solves as `make next` drew it at the time, one
    # solve per second, SMIL like the others.
    zpd_svg_img = ""
    if os.path.exists("graph/zpd.svg"):
        s3_key_zpd = upload_svg_gz("graph/zpd.svg", "zpd")
        zpd_svg_img = f"![The input tree of each of my last 50 solves, one per second](https://shyal.s3.amazonaws.com/{s3_key_zpd})"

    # Technique-graph movie (utils/kg/kg_movie_rs, `make movie`): the history
    # replayed as a SMIL-animated SVG. Like positions.svg it survives GitHub's
    # camo/<img> pipeline as-is with an svg content type.
    kg_movie_img = ""
    if os.path.exists("graph/kg_movie.svg"):
        s3_key_kg_movie = upload_svg_gz("graph/kg_movie.svg", "kg_movie")
        kg_movie_img = f"![Technique graph growing solve by solve](https://shyal.s3.amazonaws.com/{s3_key_kg_movie})"

    # The graph in three dimensions (utils/readme/kg_3d_svg): the same replay
    # on the same clock, the layout turning once per three loops.
    kg_3d_img = ""
    if os.path.exists("graph/kg_3d.svg"):
        s3_key_kg_3d = upload_svg_gz("graph/kg_3d.svg", "kg_3d")
        kg_3d_img = f"![The technique graph in three dimensions, turning while the history replays](https://shyal.s3.amazonaws.com/{s3_key_kg_3d})"

    # push everything queued above concurrently; boto3 clients are thread-safe.
    # Any failure raises here, before the README is touched.
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = [
            pool.submit(s3.upload_file, local, bucket_name, key,
                        ExtraArgs=extra, Config=transfer_config)
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
            lambda _: f"<!-- {name} -->{lead}{content}{trail}<!-- /{name} -->", text)

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
        readme = fill_inline(readme, "N_REACH_TODAY", f"~{round(r['predicted_reach'], -2):.0f}")

    readme = fill(readme, "SOLVES_CHART", rates_img)
    readme = fill(readme, "COMMITS_CHART", commits_img)
    readme = fill(readme, "READINESS_PROJECTION_CHART", projection_img)
    readme = fill(readme, "KG_MOVIE", kg_movie_img)
    readme = fill(readme, "KG_3D", kg_3d_img)
    readme = fill(readme, "MOCK_SWARM_CHART", mock_swarm_img)
    readme = fill(readme, "MOCK_BLAME_CHART", mock_blame_img)
    readme = fill(readme, "POSITIONS_SVG", positions_svg_img)
    readme = fill(readme, "ZPD_SVG", zpd_svg_img)
    readme = fill(readme, "CURVE_CALIBRATION_CHART", curve_calibration_img)
    readme = fill(readme, "RESIDUALS_CHART", residuals_img)
    readme = fill(readme, "REVIEW_TIMING_CHART", review_timing_img)
    readme = fill(readme, "SOLVETIME_CHART", solvetime_img)
    readme = fill(readme, "CONNECTIVITY_CHART", connectivity_img)
    readme = fill(readme, "REACH_CHART", reach_img)
    readme = fill(readme, "PASS_PROB_CHART", pass_prob_img)
    readme = fill(readme, "CONTEST_PROGRESS", contest_progress_img)
    readme = fill(readme, "FAANG_PROGRESS", faang_progress_img)
    readme = fill(readme, "FORECAST_CHART", forecast_img)

    with open("README.md", "w") as f:
        f.write(readme)

    print("README updated with S3 image links!")


if __name__ == "__main__":
    main()
