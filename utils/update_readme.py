def main():
    import git
    import os
    import re
    import subprocess
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

    with open("readiness.json", "r") as f:
        readiness_data = json.load(f)

    readiness_data.sort(key=lambda item: item["run_date"])

    run_dates = [item["run_date"] for item in readiness_data]
    contest_readiness = [item["contest_readiness"] for item in readiness_data]
    faang_readiness = [item["faang_interview"] for item in readiness_data]

    run_dt = [datetime.strptime(d, "%Y-%m-%d") for d in run_dates]
    contest_dt = [datetime.strptime(d, "%Y-%m-%d") for d in contest_readiness]
    faang_dt = [datetime.strptime(d, "%Y-%m-%d") for d in faang_readiness]

    contest_variance_img = ""
    if run_dates:
        min_run = min(run_dt)
        min_contest = min(contest_dt)
        x_num = [(dt - min_run).days for dt in run_dt]
        y_num = [(dt - min_contest).days for dt in contest_dt]

        # Compute 7-point moving averages for contest y_num
        ma_y_contest = []
        for i in range(len(y_num)):
            if i < 6:
                ma_y_contest.append(sum(y_num[: i + 1]) / (i + 1))
            else:
                ma_y_contest.append(sum(y_num[i - 6 : i + 1]) / 7)

        label_step = max(1, len(run_dates) // 10)
        tick_pos_x = x_num[::label_step]
        tick_labels_x = run_dates[::label_step]

        unique_contest = sorted(set(contest_dt))
        tick_pos_y = [(dt - min_contest).days for dt in unique_contest]
        tick_labels_y = [dt.strftime("%Y-%m-%d") for dt in unique_contest]

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(
            x_num,
            y_num,
            marker="o",
            label="Projected Days",
            color="#1f77b4",
            linestyle="-",
        )
        ax.plot(
            x_num, ma_y_contest, label="7-Point MA", color="#ff7f0e", linestyle="--"
        )
        ax.set_xticks(tick_pos_x)
        ax.set_xticklabels(tick_labels_x, rotation=45)
        ax.set_yticks(tick_pos_y)
        ax.set_yticklabels(tick_labels_y)
        ax.set_title("Contest Readiness Projection Over Time")
        ax.set_xlabel("Run Date")
        ax.set_ylabel("Projected Readiness Date")
        ax.legend()
        local_path = "/tmp/contest_variance.png"
        fig.savefig(local_path)
        s3_key_contest_variance = f"contest_variance_{timestamp}.png"
        queue_upload(local_path, s3_key_contest_variance, {"ContentType": "image/png"})
        plt.close(fig)
        contest_variance_img = f"![Contest Readiness Projection Over Time](https://shyal.s3.amazonaws.com/{s3_key_contest_variance})"

    # Deterministic simulator (utils/kg_predict) projection over time — separate
    # series from the LLM guess above; only entries that recorded faang_predict.
    faang_predict_variance_img = ""
    predict_entries = [e for e in readiness_data if "faang_predict" in e]
    if predict_entries:
        p_run_dt = [datetime.strptime(e["run_date"], "%Y-%m-%d") for e in predict_entries]
        p_pred_dt = [datetime.strptime(e["faang_predict"], "%Y-%m-%d") for e in predict_entries]
        p_min_run, p_min_pred = min(p_run_dt), min(p_pred_dt)
        px = [(dt - p_min_run).days for dt in p_run_dt]
        py = [(dt - p_min_pred).days for dt in p_pred_dt]

        p_label_step = max(1, len(predict_entries) // 10)
        unique_pred = sorted(set(p_pred_dt))

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(px, py, marker="o", label="Simulated Ready Date", color="#2ca02c", linestyle="-")
        ax.set_xticks(px[::p_label_step])
        ax.set_xticklabels([e["run_date"] for e in predict_entries][::p_label_step], rotation=45)
        ax.set_yticks([(dt - p_min_pred).days for dt in unique_pred])
        ax.set_yticklabels([dt.strftime("%Y-%m-%d") for dt in unique_pred])
        ax.set_title("FAANG Readiness (Curve Simulator) Projection Over Time")
        ax.set_xlabel("Run Date")
        ax.set_ylabel("Simulated Readiness Date")
        ax.legend()
        fig.tight_layout()
        local_path = "/tmp/faang_predict_variance.png"
        fig.savefig(local_path)
        s3_key_faang_predict = f"faang_predict_variance_{timestamp}.png"
        queue_upload(local_path, s3_key_faang_predict, {"ContentType": "image/png"})
        plt.close(fig)
        faang_predict_variance_img = f"![FAANG Readiness (Curve Simulator) Projection Over Time](https://shyal.s3.amazonaws.com/{s3_key_faang_predict})"

    faang_variance_img = ""
    if run_dates:
        min_faang = min(faang_dt)
        y_num_faang = [(dt - min_faang).days for dt in faang_dt]

        # Compute 7-point moving averages for faang y_num_faang
        ma_y_faang = []
        for i in range(len(y_num_faang)):
            if i < 6:
                ma_y_faang.append(sum(y_num_faang[: i + 1]) / (i + 1))
            else:
                ma_y_faang.append(sum(y_num_faang[i - 6 : i + 1]) / 7)

        unique_faang = sorted(set(faang_dt))
        tick_pos_y_faang = [(dt - min_faang).days for dt in unique_faang]
        tick_labels_y_faang = [dt.strftime("%Y-%m-%d") for dt in unique_faang]

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(
            x_num,
            y_num_faang,
            marker="o",
            label="Projected Days",
            color="#1f77b4",
            linestyle="-",
        )
        ax.plot(x_num, ma_y_faang, label="7-Point MA", color="#ff7f0e", linestyle="--")
        ax.set_xticks(tick_pos_x)
        ax.set_xticklabels(tick_labels_x, rotation=45)
        ax.set_yticks(tick_pos_y_faang)
        ax.set_yticklabels(tick_labels_y_faang)
        ax.set_title("FAANG Interview Readiness Projection Over Time")
        ax.set_xlabel("Run Date")
        ax.set_ylabel("Projected Readiness Date")
        ax.legend()
        local_path = "/tmp/faang_variance.png"
        fig.savefig(local_path)
        s3_key_faang_variance = f"faang_variance_{timestamp}.png"
        queue_upload(local_path, s3_key_faang_variance, {"ContentType": "image/png"})
        plt.close(fig)
        faang_variance_img = f"![FAANG Interview Readiness Projection Over Time](https://shyal.s3.amazonaws.com/{s3_key_faang_variance})"

    if readiness_data:
        last_readiness = readiness_data[-1]
        contest_end_str = last_readiness["contest_readiness"]
        # prefer the deterministic simulator's date over the LLM guess
        faang_end_str = last_readiness.get("faang_predict", last_readiness["faang_interview"])
        faang_hours = last_readiness.get("faang_predict_hours")

        if all_problem_dates:
            # Progress = current skill measured by the technique graph, NOT elapsed
            # time. SOLID = fresh evidence; STALE/FRAGILE discount for forgetting.
            from kg_lib import load_nodes, load_evidence, node_status, SOLID, STALE, FRAGILE

            kg_nodes = load_nodes()
            kg_evidence = load_evidence()
            kg_statuses = {n: node_status(n, kg_evidence)[0] for n in kg_nodes}
            status_weight = {SOLID: 1.0, STALE: 0.5, FRAGILE: 0.25}
            progress_contest = sum(
                status_weight.get(s, 0.0) for s in kg_statuses.values()
            ) / len(kg_statuses)
            progress_faang = sum(
                1 for s in kg_statuses.values() if s == SOLID
            ) / len(kg_statuses)

            fig, ax = plt.subplots(figsize=(10, 2))
            ax.barh([0], [progress_contest * 100], height=0.5, color="#00FF00")
            ax.set_yticks([0])
            ax.set_yticklabels(["Progress"])
            ax.set_xlim(0, 100)
            ax.set_xlabel("Graph-weighted skill %  (solid=1, stale=0.5, fragile=0.25)")
            ax.set_title(f"Contest Readiness (projected ready {contest_end_str})")
            local_path = "/tmp/contest_progress.png"
            fig.savefig(local_path, bbox_inches="tight")
            s3_key_contest_progress = f"contest_progress_{timestamp}.png"
            queue_upload(local_path, s3_key_contest_progress, {"ContentType": "image/png"})
            plt.close(fig)
            contest_progress_img = f"![Contest Readiness Progress (Ready by {contest_end_str})](https://shyal.s3.amazonaws.com/{s3_key_contest_progress})"

            fig, ax = plt.subplots(figsize=(10, 2))
            ax.barh([0], [progress_faang * 100], height=0.5, color="#00FF00")
            ax.set_yticks([0])
            ax.set_yticklabels(["Progress"])
            ax.set_xlim(0, 100)
            ax.set_xlabel("Fraction of technique nodes SOLID (fresh evidence only)")
            faang_title = f"FAANG Interview Readiness (simulated ready {faang_end_str}"
            faang_title += f" at {faang_hours:g}h/day)" if faang_hours else ")"
            ax.set_title(faang_title)
            local_path = "/tmp/faang_progress.png"
            fig.savefig(local_path, bbox_inches="tight")
            s3_key_faang_progress = f"faang_progress_{timestamp}.png"
            queue_upload(local_path, s3_key_faang_progress, {"ContentType": "image/png"})
            plt.close(fig)
            faang_progress_img = f"![FAANG Interview Readiness Progress (Ready by {faang_end_str})](https://shyal.s3.amazonaws.com/{s3_key_faang_progress})"
        else:
            contest_progress_img = "No repo history for progress calculation."
            faang_progress_img = "No repo history for progress calculation."

        historical_topics = [
            item for item in readiness_data if "contest_topics_readiness" in item
        ]
        contest_topics_img = ""
        if historical_topics:
            # Static sorted snapshot of the LATEST scores only — older entries used
            # a different topic vocabulary (LLM tags vs graph groups) and animating
            # across the union reads as chaos.
            last_entry = historical_topics[-1]
            last_topics_data = last_entry["contest_topics_readiness"]
            topics = sorted(last_topics_data, key=last_topics_data.get)  # barh: biggest on top
            scores = [last_topics_data[t] for t in topics]

            fig, ax = plt.subplots(figsize=(10, max(2, len(topics) * 0.4)))
            bar_colors = ["#00AA00" if s >= 0.8 else "#FFA500" if s >= 0.5 else "#DD0000" for s in scores]
            ax.barh(topics, scores, color=bar_colors)
            ax.set_xlim(0, 1)
            ax.set_xlabel("Readiness Score (from technique graph)")
            ax.set_title(f"Topic Readiness ({last_entry['run_date']})")
            fig.tight_layout()
            local_path = "/tmp/contest_topics_readiness.png"
            fig.savefig(local_path)
            s3_key_contest_topics = f"contest_topics_readiness_{timestamp}.png"
            queue_upload(local_path, s3_key_contest_topics, {"ContentType": "image/png"})
            plt.close(fig)
            contest_topics_img = f"![Topic Readiness](https://shyal.s3.amazonaws.com/{s3_key_contest_topics})"
        else:
            contest_topics_img = "No contest topics data."

    else:
        contest_progress_img = "No readiness data."
        faang_progress_img = "No readiness data."
        contest_topics_img = "No readiness data."

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
    if run_dates:
        readme = fill(readme, "CONTEST_VARIANCE_CHART", contest_variance_img)
        readme = fill(readme, "FAANG_VARIANCE_CHART", faang_variance_img)
    readme = fill(readme, "FAANG_PREDICT_VARIANCE_CHART", faang_predict_variance_img)
    readme = fill(readme, "KG_MOVIE", kg_movie_img)
    readme = fill(readme, "MOCK_DIST_CHART", mock_dist_img)
    readme = fill(readme, "MOCK_SWARM_CHART", mock_swarm_img)
    readme = fill(readme, "MOCK_BLAME_CHART", mock_blame_img)
    readme = fill(readme, "POSITIONS_SVG", positions_svg_img)
    readme = fill(readme, "CURVE_CALIBRATION_CHART", curve_calibration_img)
    readme = fill(readme, "REVIEW_TIMING_CHART", review_timing_img)
    readme = fill(readme, "PASS_PROB_CHART", pass_prob_img)
    readme = fill(readme, "CONTEST_PROGRESS", contest_progress_img)
    readme = fill(readme, "FAANG_PROGRESS", faang_progress_img)
    readme = fill(readme, "CONTEST_TOPICS_CHART", contest_topics_img)

    with open("README.md", "w") as f:
        f.write(readme)

    print("README updated with S3 image links!")
    print(f"Total solves: {sum(solves_data)}")


if __name__ == "__main__":
    main()
