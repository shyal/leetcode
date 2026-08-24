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
    from metadata import get_problems_metadata

    mpl.use("Agg")
    import matplotlib.pyplot as plt

    s3 = boto3.client("s3")
    bucket_name = "shyal"

    # every chart lands in a unique local path, so uploads can be queued as
    # they're produced and pushed concurrently at the end
    upload_jobs = []

    def queue_upload(local, key, extra):
        upload_jobs.append((local, key, extra))

    # The four synced SMIL animations (kg_movie / kg_pass / positions /
    # calibration) go up gzipped with a Content-Encoding header — camo passes
    # it through, and near-equal transfer sizes keep their independent SMIL
    # clocks starting in near-lockstep.
    def upload_svg_gz(path, key):
        import gzip

        local = f"/tmp/{os.path.basename(key)}.gz"
        with open(path, "rb") as f, gzip.open(local, "wb", compresslevel=9) as g:
            g.write(f.read())
        queue_upload(
            local,
            key,
            {"ContentType": "image/svg+xml", "ContentEncoding": "gzip"},
        )

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    metadata = get_problems_metadata()
    print(f"Debug: Metadata loaded with {len(metadata)} problems")
    print(
        f"Debug: Example problem 1 difficulty: {metadata.get(1, {}).get('difficulty', 'Not found')}"
    )
    print(
        f"Debug: Example problem 2 difficulty: {metadata.get(2, {}).get('difficulty', 'Not found')}"
    )

    repo = git.Repo(".")
    commits = list(repo.iter_commits("HEAD"))

    solves_per_day = defaultdict(int)
    uniques_per_day = defaultdict(set)
    uniques_per_day_diff = defaultdict(lambda: defaultdict(set))
    all_problem_dates = set()
    diff_counts = defaultdict(int)
    sample_probs = []

    for commit in commits:
        msg = commit.message.strip()
        if not msg:
            continue

        date_str = commit.committed_datetime.strftime("%Y-%m-%d")

        prob_match = re.match(r"(\d+)\.\s+(.+)", msg)
        if not prob_match:
            continue

        prob_num = int(prob_match.group(1))  # int for metadata lookup
        all_problem_dates.add(date_str)

        is_unsolved = (
            "unsolved" in msg.lower()
            or "still learning" in msg.lower()
            or "stub" in msg.lower()
            or "readme" in msg.lower()
        )

        if not is_unsolved:
            solves_per_day[date_str] += 1
            uniques_per_day[date_str].add(prob_num)
            diff = metadata.get(prob_num, {}).get("difficulty", "Unknown")
            uniques_per_day_diff[date_str][diff].add(prob_num)
            diff_counts[diff] += 1
            if len(sample_probs) < 10:
                sample_probs.append(f"Prob {prob_num}: {diff}")

    print("Debug: Difficulty counts for solved problems: " + str(dict(diff_counts)))
    print("Debug: Sample problem difficulties: " + ", ".join(sample_probs))

    if all_problem_dates:
        min_date_str = min(all_problem_dates)
        max_date_str = max(all_problem_dates)
        start = datetime.strptime(min_date_str, "%Y-%m-%d")
        end = datetime.strptime(max_date_str, "%Y-%m-%d")
        all_dates = []
        current = start
        while current <= end:
            d_str = current.strftime("%Y-%m-%d")
            all_dates.append(d_str)
            current += timedelta(days=1)
        solves_data = [solves_per_day.get(d, 0) for d in all_dates]
        uniques_data = [len(uniques_per_day.get(d, set())) for d in all_dates]
        uniques_easy = [
            len(uniques_per_day_diff[d].get("Easy", set())) for d in all_dates
        ]
        uniques_medium = [
            len(uniques_per_day_diff[d].get("Medium", set())) for d in all_dates
        ]
        uniques_hard = [
            len(uniques_per_day_diff[d].get("Hard", set())) for d in all_dates
        ]
        uniques_unknown = [
            len(uniques_per_day_diff[d].get("Unknown", set())) for d in all_dates
        ]
        dates_for_plot = all_dates
        print(f"Debug: Total Easy uniques: {sum(uniques_easy)}")
        print(f"Debug: Total Medium uniques: {sum(uniques_medium)}")
        print(f"Debug: Total Hard uniques: {sum(uniques_hard)}")
        print(f"Debug: Total Unknown uniques: {sum(uniques_unknown)}")
    else:
        dates_for_plot = []
        solves_data = []
        uniques_data = []
        uniques_easy = []
        uniques_medium = []
        uniques_hard = []
        uniques_unknown = []

    if dates_for_plot:
        x = list(range(len(dates_for_plot)))
        label_step = max(1, len(dates_for_plot) // 10)
        tick_positions = x[::label_step]
        tick_labels = dates_for_plot[::label_step]

    # Compute 7-day moving averages for solves
    ma_solves = []
    for i in range(len(solves_data)):
        if i < 6:
            ma_solves.append(sum(solves_data[: i + 1]) / (i + 1))
        else:
            ma_solves.append(sum(solves_data[i - 6 : i + 1]) / 7)

    # Compute 7-day moving averages for uniques
    ma_uniques = []
    for i in range(len(uniques_data)):
        if i < 6:
            ma_uniques.append(sum(uniques_data[: i + 1]) / (i + 1))
        else:
            ma_uniques.append(sum(uniques_data[i - 6 : i + 1]) / 7)

    fig, ax = plt.subplots(figsize=(12, 5))
    if dates_for_plot:
        ax.plot(
            x,
            solves_data,
            marker="o",
            label="Daily Solves",
            color="#1f77b4",
            linestyle="-",
        )
        ax.plot(x, ma_solves, label="7-Day MA", color="#ff7f0e", linestyle="--")
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, rotation=45)
        ax.legend()
    ax.set_title("Solves Per Day (Full Repo History)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Solves")
    local_path = "/tmp/solves_per_day.png"
    fig.savefig(local_path)
    s3_key_solves = f"solves_per_day_{timestamp}.png"
    queue_upload(local_path, s3_key_solves, {"ContentType": "image/png"})
    plt.close(fig)
    solves_img = f"![Solves Per Day (Full Repo History)](https://shyal.s3.amazonaws.com/{s3_key_solves})"

    fig, ax = plt.subplots(figsize=(12, 5))
    if dates_for_plot:
        bottom = np.zeros(len(x))
        ax.bar(x, uniques_easy, label="Easy", color="#00FF00", bottom=bottom)
        bottom += np.array(uniques_easy)
        ax.bar(x, uniques_medium, label="Medium", color="#FFA500", bottom=bottom)
        bottom += np.array(uniques_medium)
        ax.bar(x, uniques_hard, label="Hard", color="#FF0000", bottom=bottom)
        bottom += np.array(uniques_hard)
        ax.bar(x, uniques_unknown, label="Unknown", color="#808080", bottom=bottom)
        ax.plot(x, ma_uniques, label="7-Day MA", color="#000000", linestyle="--")
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, rotation=45)
        ax.legend()
    ax.set_title("Unique Problems Solved Daily (Full Repo History)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Unique Solves")
    local_path = "/tmp/uniques_per_day.png"
    fig.savefig(local_path)
    s3_key_uniques = f"uniques_per_day_{timestamp}.png"
    queue_upload(local_path, s3_key_uniques, {"ContentType": "image/png"})
    plt.close(fig)
    uniques_img = f"![Unique Problems Solved Daily (Full Repo History)](https://shyal.s3.amazonaws.com/{s3_key_uniques})"

    # One projection-stability chart: each model's projected ready date over
    # run date, recomputed on the fly for EVERY day since the first evidence
    # record (no stored snapshots): kg_mock --history-json replays the
    # Monte-Carlo mock milestones, kg_predict --history-json the work-done
    # simulator. Each day's point uses only the evidence and git log visible
    # on that day; the math is today's model throughout.
    mock_bin = "utils/kg_mock_rs/target/release/kg_mock"
    mock_history = json.loads(
        subprocess.run([mock_bin, "--history-json"],
                       capture_output=True, text=True, check=True).stdout
    )
    predict_history = json.loads(
        subprocess.run([sys.executable, "utils/kg_predict", "--history-json"],
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
        s3_key_projection = f"readiness_projection_{timestamp}.png"
        queue_upload(local_path, s3_key_projection, {"ContentType": "image/png"})
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
            s3_key = f"{s3_prefix}_{timestamp}.png"
            queue_upload(local_path, s3_key, {"ContentType": "image/png"})
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

    # Forgetting-curve calibration (utils/kg_calibration_svg): model vs
    # observed clean-recall by gap, replayed weekly as a SMIL SVG on the
    # shared clock — the fourth synced animation.
    curve_calibration_img = ""
    if os.path.exists("graph/calibration.svg"):
        s3_key_calib = f"curve_calibration_{timestamp}.svg"
        upload_svg_gz("graph/calibration.svg", s3_key_calib)
        curve_calibration_img = f"![Curve calibration](https://shyal.s3.amazonaws.com/{s3_key_calib})"

    # Review timing (utils/kg_timing_svg): every recall trial's gap vs the
    # predicted solid window — the scheduler's report card, on the shared
    # clock.
    review_timing_img = ""
    if os.path.exists("graph/timing.svg"):
        s3_key_timing = f"review_timing_{timestamp}.svg"
        upload_svg_gz("graph/timing.svg", s3_key_timing)
        review_timing_img = f"![Was each review on time?](https://shyal.s3.amazonaws.com/{s3_key_timing})"

    # Problems in reach (utils/kg_reach_svg): today's walked frontier replayed
    # against historical node states - the payoff curve, on the shared clock.
    reach_img = ""
    if os.path.exists("graph/reach.svg"):
        s3_key_reach = f"reach_{timestamp}.svg"
        upload_svg_gz("graph/reach.svg", s3_key_reach)
        reach_img = f"![Problems in reach](https://shyal.s3.amazonaws.com/{s3_key_reach})"

    # P(pass) history — the headline "how good am i" line, now rendered by
    # utils/kg_movie_rs (`make movie`) as a SMIL-animated SVG synced with the
    # technique-graph movie: the same weekly replay + kg_lib cold-mock Monte
    # Carlo (the kg_mock lib reproduces the math bit-for-bit), revealed
    # left-to-right on the movie's clock.
    pass_prob_img = ""
    if os.path.exists("graph/kg_pass.svg"):
        s3_key_pass = f"pass_probability_{timestamp}.svg"
        upload_svg_gz("graph/kg_pass.svg", s3_key_pass)
        pass_prob_img = f"![P(pass a mock) over time](https://shyal.s3.amazonaws.com/{s3_key_pass})"

    # Yield chart (utils/kg_movie_rs, same binary): P(pass) against
    # cumulative solves instead of time - a plateau is a long flat slog,
    # consolidation a near-vertical climb, segments colored by re-solve share.
    yield_img = ""
    if os.path.exists("graph/kg_yield.svg"):
        s3_key_yield = f"yield_{timestamp}.svg"
        upload_svg_gz("graph/kg_yield.svg", s3_key_yield)
        yield_img = f"![What a solve buys](https://shyal.s3.amazonaws.com/{s3_key_yield})"

    # Its calendar twin (same binary): the P(pass) lines over each week's
    # composition (new problems vs re-solves) - the two kinds of sideways.
    yield_time_img = ""
    if os.path.exists("graph/kg_yield_time.svg"):
        s3_key_yield_time = f"yield_time_{timestamp}.svg"
        upload_svg_gz("graph/kg_yield_time.svg", s3_key_yield_time)
        yield_time_img = f"![Two kinds of sideways](https://shyal.s3.amazonaws.com/{s3_key_yield_time})"

    # Mock outcome distribution (utils/kg_movie_rs, same binary): the Monte
    # Carlo mass behind the P(pass) central line, stepping weekly on the
    # shared clock.
    mock_dist_img = ""
    if os.path.exists("graph/kg_dist.svg"):
        s3_key_dist = f"mock_dist_{timestamp}.svg"
        upload_svg_gz("graph/kg_dist.svg", s3_key_dist)
        mock_dist_img = f"![Simulated mock outcomes over time](https://shyal.s3.amazonaws.com/{s3_key_dist})"

    # Its dot-level companion (same binary): individual simulated mocks with
    # fixed dice, hopping bins as skill improves.
    mock_swarm_img = ""
    if os.path.exists("graph/kg_swarm.svg"):
        s3_key_swarm = f"mock_swarm_{timestamp}.svg"
        upload_svg_gz("graph/kg_swarm.svg", s3_key_swarm)
        mock_swarm_img = f"![Individual simulated mocks over time](https://shyal.s3.amazonaws.com/{s3_key_swarm})"

    # And the failure-attribution view (same binary): failed simulated
    # problems blamed on the weakest move in their walk, by technique group.
    mock_blame_img = ""
    if os.path.exists("graph/kg_blame.svg"):
        s3_key_blame = f"mock_blame_{timestamp}.svg"
        upload_svg_gz("graph/kg_blame.svg", s3_key_blame)
        mock_blame_img = f"![Why simulated mocks fail, over time](https://shyal.s3.amazonaws.com/{s3_key_blame})"

    # Animated SVG (utils/kg_positions_svg): every node sliding down its
    # personal forgetting curve, replaying the same history on the same clock
    # as the two SVGs above.
    positions_svg_img = ""
    if os.path.exists("graph/positions.svg"):
        s3_key_positions = f"positions_{timestamp}.svg"
        upload_svg_gz("graph/positions.svg", s3_key_positions)
        positions_svg_img = f"![Nodes sliding down their forgetting curves](https://shyal.s3.amazonaws.com/{s3_key_positions})"

    # Technique-graph movie (utils/kg_movie_rs, `make movie`): the history
    # replayed as a SMIL-animated SVG. Like positions.svg it survives GitHub's
    # camo/<img> pipeline as-is with an svg content type.
    kg_movie_img = ""
    if os.path.exists("graph/kg_movie.svg"):
        s3_key_kg_movie = f"kg_movie_{timestamp}.svg"
        upload_svg_gz("graph/kg_movie.svg", s3_key_kg_movie)
        kg_movie_img = f"![Technique graph growing solve by solve](https://shyal.s3.amazonaws.com/{s3_key_kg_movie})"

    # push everything queued above concurrently; boto3 clients are thread-safe.
    # Any failure raises here, before the README is touched.
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = [
            pool.submit(s3.upload_file, local, bucket_name, key, ExtraArgs=extra)
            for local, key, extra in upload_jobs
        ]
        for f in futures:
            f.result()

    # README.md is the single source of truth: prose is edited there directly,
    # and each generated block lives between <!-- NAME --> ... <!-- /NAME -->
    # markers (invisible on GitHub). fill() rewrites only the inside of a
    # region, so the script is idempotent and never touches the prose. Empty
    # content leaves a region as-is (same semantics as the old conditionals).
    with open("README.md", "r") as f:
        readme = f.read()

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

    readme = fill(readme, "SOLVES_CHART", solves_img)
    readme = fill(readme, "UNIQUES_CHART", uniques_img)
    readme = fill(readme, "READINESS_PROJECTION_CHART", projection_img)
    readme = fill(readme, "KG_MOVIE", kg_movie_img)
    readme = fill(readme, "MOCK_DIST_CHART", mock_dist_img)
    readme = fill(readme, "MOCK_SWARM_CHART", mock_swarm_img)
    readme = fill(readme, "MOCK_BLAME_CHART", mock_blame_img)
    readme = fill(readme, "POSITIONS_SVG", positions_svg_img)
    readme = fill(readme, "CURVE_CALIBRATION_CHART", curve_calibration_img)
    readme = fill(readme, "REVIEW_TIMING_CHART", review_timing_img)
    readme = fill(readme, "REACH_CHART", reach_img)
    readme = fill(readme, "PASS_PROB_CHART", pass_prob_img)
    readme = fill(readme, "YIELD_CHART", yield_img)
    readme = fill(readme, "YIELD_TIME_CHART", yield_time_img)
    readme = fill(readme, "CONTEST_PROGRESS", contest_progress_img)
    readme = fill(readme, "FAANG_PROGRESS", faang_progress_img)

    with open("README.md", "w") as f:
        f.write(readme)

    print("README updated with S3 image links!")
    print(f"Total solves: {sum(solves_data)}")


if __name__ == "__main__":
    main()
