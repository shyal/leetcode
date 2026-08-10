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
    import math
    import json
    from metadata import get_problems_metadata

    mpl.use("Agg")
    import matplotlib.pyplot as plt

    s3 = boto3.client("s3")
    bucket_name = "shyal"

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
    s3.upload_file(
        local_path,
        bucket_name,
        s3_key_solves,
        ExtraArgs={"ContentType": "image/png"},
    )
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
    s3.upload_file(
        local_path,
        bucket_name,
        s3_key_uniques,
        ExtraArgs={"ContentType": "image/png"},
    )
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
        s3.upload_file(
            local_path,
            bucket_name,
            s3_key_contest_variance,
            ExtraArgs={"ContentType": "image/png"},
        )
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
        s3.upload_file(
            local_path,
            bucket_name,
            s3_key_faang_predict,
            ExtraArgs={"ContentType": "image/png"},
        )
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
        s3.upload_file(
            local_path,
            bucket_name,
            s3_key_faang_variance,
            ExtraArgs={"ContentType": "image/png"},
        )
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
            s3.upload_file(
                local_path,
                bucket_name,
                s3_key_contest_progress,
                ExtraArgs={"ContentType": "image/png"},
            )
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
            s3.upload_file(
                local_path,
                bucket_name,
                s3_key_faang_progress,
                ExtraArgs={"ContentType": "image/png"},
            )
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
            s3.upload_file(
                local_path,
                bucket_name,
                s3_key_contest_topics,
                ExtraArgs={"ContentType": "image/png"},
            )
            plt.close(fig)
            contest_topics_img = f"![Topic Readiness](https://shyal.s3.amazonaws.com/{s3_key_contest_topics})"
        else:
            contest_topics_img = "No contest topics data."

    else:
        contest_progress_img = "No readiness data."
        faang_progress_img = "No readiness data."
        contest_topics_img = "No readiness data."

    # Personal forgetting curve (graph/curve.json): the fitted family of curves
    # by rep count, plus a calibration check against the actual recall trials.
    curve_img = ""
    curve_calibration_img = ""
    if os.path.exists("graph/curve.json"):
        with open("graph/curve.json") as f:
            curve = json.load(f)
        cp = curve["params"]
        target = curve["target_retention"]

        gaps = np.arange(0, 181)
        fig, ax = plt.subplots(figsize=(12, 5))
        for k, color in zip((1, 2, 3, 5, 10),
                            ("#DD0000", "#FF8800", "#BBBB00", "#00AA00", "#1f77b4")):
            s = math.exp(cp["a"] + cp["b"] * k)
            mem = (1 + gaps / s) ** (-cp["beta"])
            window = s * (target ** (-1 / cp["beta"]) - 1)
            ax.plot(gaps, mem, color=color,
                    label=f"{k} clean rep{'s' if k > 1 else ''} — solid for ≈{window:.0f}d")
        ax.axhline(target, color="#888888", linestyle=":",
                   label=f"{target:.0%} retention = SOLID threshold")
        ax.set_ylim(min(0.85, target - 0.05), 1.001)
        ax.set_xlim(0, 180)
        ax.set_xlabel("Days since last clean solve")
        ax.set_ylabel("P(recall), memory component")
        ax.set_title(f"Fitted forgetting curve ({curve['fit']['trials']} recall trials): "
                     f"(1 + Δ/s)^(−{cp['beta']:.2f}),  s = exp({cp['a']:.2f} + {cp['b']:.2f}·reps)")
        ax.legend()
        fig.tight_layout()
        local_path = "/tmp/forgetting_curve.png"
        fig.savefig(local_path)
        s3_key_curve = f"forgetting_curve_{timestamp}.png"
        s3.upload_file(local_path, bucket_name, s3_key_curve,
                       ExtraArgs={"ContentType": "image/png"})
        plt.close(fig)
        curve_img = f"![Fitted forgetting curve](https://shyal.s3.amazonaws.com/{s3_key_curve})"

        # calibration: model vs observed clean-rate per gap bucket, over the
        # same trials kg_curve fitted on
        from importlib.machinery import SourceFileLoader
        utils_dir = os.path.dirname(os.path.abspath(__file__))
        kg_curve = SourceFileLoader("kg_curve", os.path.join(utils_dir, "kg_curve")).load_module()
        from kg_lib import load_evidence

        trials = kg_curve.extract_trials(load_evidence())

        def pred(g, k, m):
            s = math.exp(cp["a"] + cp["b"] * k - cp["c"] * m)
            return (1 - cp["slip"]) * (1 + g / s) ** (-cp["beta"])

        labels, model_rates, observed_rates, counts = [], [], [], []
        for lo, hi in ((1, 7), (8, 21), (22, 42), (43, 90), (91, 180), (181, 400)):
            rows = [t for t in trials if lo <= t[0] <= hi]
            if not rows:
                continue
            labels.append(f"{lo}–{hi}d")
            observed_rates.append(sum(s for _, s, _, _ in rows) / len(rows))
            model_rates.append(sum(pred(g, k, m) for g, _, k, m in rows) / len(rows))
            counts.append(len(rows))

        if labels:
            xb = np.arange(len(labels))
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.bar(xb - 0.2, model_rates, 0.4, label="Model", color="#1f77b4")
            ax.bar(xb + 0.2, observed_rates, 0.4, label="Observed", color="#00AA00")
            for i, n in enumerate(counts):
                ax.text(xb[i], max(model_rates[i], observed_rates[i]) + 0.02,
                        f"n={n}", ha="center", fontsize=9)
            ax.set_xticks(xb)
            ax.set_xticklabels(labels)
            ax.set_ylim(0, 1.1)
            ax.set_xlabel("Gap since last clean solve")
            ax.set_ylabel("Clean-recall rate")
            ax.set_title("Calibration: model prediction vs observed recall, by gap")
            ax.legend()
            fig.tight_layout()
            local_path = "/tmp/curve_calibration.png"
            fig.savefig(local_path)
            s3_key_calib = f"curve_calibration_{timestamp}.png"
            s3.upload_file(local_path, bucket_name, s3_key_calib,
                           ExtraArgs={"ContentType": "image/png"})
            plt.close(fig)
            curve_calibration_img = f"![Curve calibration](https://shyal.s3.amazonaws.com/{s3_key_calib})"

    # Technique-graph movie: GitHub strips <video>/HTML from READMEs, so ship
    # graph/kg.mp4 as an optimized GIF on the same S3 pipeline as the charts.
    kg_movie_img = ""
    if os.path.exists("graph/kg.mp4"):
        local_path = "/tmp/kg_movie.gif"
        try:
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-i", "graph/kg.mp4",
                 "-vf", "fps=20,scale=1280:-1:flags=lanczos,"
                        "split[s0][s1];[s0]palettegen=max_colors=128[p];"
                        "[s1][p]paletteuse=dither=bayer:bayer_scale=4",
                 local_path],
                check=True,
            )
            s3_key_kg_movie = f"kg_movie_{timestamp}.gif"
            s3.upload_file(
                local_path,
                bucket_name,
                s3_key_kg_movie,
                ExtraArgs={"ContentType": "image/gif"},
            )
            kg_movie_img = f"![Technique graph growing solve by solve](https://shyal.s3.amazonaws.com/{s3_key_kg_movie})"
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"kg movie skipped: {e}")

    with open("README.md.template", "r") as f:
        readme = f.read()

    readme = readme.replace("<!-- SOLVES_CHART -->", solves_img)
    readme = readme.replace("<!-- UNIQUES_CHART -->", uniques_img)

    if run_dates:
        readme = readme.replace("<!-- CONTEST_VARIANCE_CHART -->", contest_variance_img)
        readme = readme.replace("<!-- FAANG_VARIANCE_CHART -->", faang_variance_img)
    if faang_predict_variance_img:
        readme = readme.replace(
            "<!-- FAANG_PREDICT_VARIANCE_CHART -->", faang_predict_variance_img
        )
    if kg_movie_img:
        readme = readme.replace("<!-- KG_MOVIE -->", kg_movie_img)
    if curve_img:
        readme = readme.replace("<!-- CURVE_CHART -->", curve_img)
    if curve_calibration_img:
        readme = readme.replace("<!-- CURVE_CALIBRATION_CHART -->", curve_calibration_img)

    readme = readme.replace("<!-- CONTEST_PROGRESS -->", contest_progress_img)
    readme = readme.replace("<!-- FAANG_PROGRESS -->", faang_progress_img)
    readme = readme.replace("<!-- CONTEST_TOPICS_CHART -->", contest_topics_img)

    with open("README.md", "w") as f:
        f.write(readme)

    print("README updated with S3 image links!")
    print(f"Total solves: {sum(solves_data)}")


if __name__ == "__main__":
    main()
