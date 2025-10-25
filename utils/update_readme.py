def main():
    import git
    import re
    from datetime import datetime, timedelta, date
    from collections import defaultdict
    import matplotlib as mpl
    import boto3
    import numpy as np
    import math
    import requests
    import json
    import os

    mpl.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    s3 = boto3.client("s3")
    bucket_name = "shyal"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    def get_problems_metadata():
        METADATA_FILE = ".problems_metadata.json"
        if os.path.exists(METADATA_FILE):
            os.remove(METADATA_FILE)  # Force refetch for debug
            print("Debug: Removed old metadata file to force refetch.")

        url = "https://leetcode.com/api/problems/all/"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            problems = {}
            for stat in data["stat_status_pairs"]:
                s = stat["stat"]
                num = s["frontend_question_id"]
                title = s["question__title"]
                slug = s["question__title_slug"]
                diff = stat["difficulty"]["level"]  # 1,2,3
                diff_str = {1: "Easy", 2: "Medium", 3: "Hard"}[diff]
                problems[num] = {"title": title, "slug": slug, "difficulty": diff_str}

            with open(METADATA_FILE, "w") as f:
                json.dump(problems, f)

            return problems
        else:
            raise ValueError("Failed to fetch problems metadata")

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
        faang_end_str = last_readiness["faang_interview"]

        if all_problem_dates:
            start_dt = datetime.strptime(min_date_str, "%Y-%m-%d")
            current_dt = datetime.combine(date.today(), datetime.min.time())

            contest_end_dt = datetime.strptime(contest_end_str, "%Y-%m-%d")
            total_days_contest = (contest_end_dt - start_dt).days
            elapsed_days_contest = (current_dt - start_dt).days
            progress_contest = max(
                0,
                min(
                    1,
                    (
                        elapsed_days_contest / total_days_contest
                        if total_days_contest > 0
                        else 0
                    ),
                ),
            )

            fig, ax = plt.subplots(figsize=(10, 2))
            ax.barh([0], [progress_contest * 100], height=0.5, color="#00FF00")
            ax.set_yticks([0])
            ax.set_yticklabels(["Progress"])
            ax.set_xlim(0, 100)
            ax.set_xlabel("Percentage Complete")
            ax.set_title(f"Contest Readiness Progress (Ready by {contest_end_str})")
            local_path = "/tmp/contest_progress.png"
            fig.savefig(local_path)
            s3_key_contest_progress = f"contest_progress_{timestamp}.png"
            s3.upload_file(
                local_path,
                bucket_name,
                s3_key_contest_progress,
                ExtraArgs={"ContentType": "image/png"},
            )
            plt.close(fig)
            contest_progress_img = f"![Contest Readiness Progress (Ready by {contest_end_str})](https://shyal.s3.amazonaws.com/{s3_key_contest_progress})"

            faang_end_dt = datetime.strptime(faang_end_str, "%Y-%m-%d")
            total_days_faang = (faang_end_dt - start_dt).days
            elapsed_days_faang = (current_dt - start_dt).days
            progress_faang = max(
                0,
                min(
                    1,
                    (
                        elapsed_days_faang / total_days_faang
                        if total_days_faang > 0
                        else 0
                    ),
                ),
            )

            fig, ax = plt.subplots(figsize=(10, 2))
            ax.barh([0], [progress_faang * 100], height=0.5, color="#00FF00")
            ax.set_yticks([0])
            ax.set_yticklabels(["Progress"])
            ax.set_xlim(0, 100)
            ax.set_xlabel("Percentage Complete")
            ax.set_title(
                f"FAANG Interview Readiness Progress (Ready by {faang_end_str})"
            )
            local_path = "/tmp/faang_progress.png"
            fig.savefig(local_path)
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
            all_topics = set()
            for item in historical_topics:
                all_topics.update(item["contest_topics_readiness"].keys())
            last_topics_data = historical_topics[-1]["contest_topics_readiness"]
            topics = sorted(
                all_topics, key=lambda x: last_topics_data.get(x, 0), reverse=True
            )
            dates_with_data = [item["run_date"] for item in historical_topics]
            scores_over_time = []
            for item in historical_topics:
                scores = [
                    item["contest_topics_readiness"].get(topic, 0) for topic in topics
                ]
                scores_over_time.append(scores)

            fig, ax = plt.subplots(figsize=(10, len(topics) * 0.5))
            colors = plt.cm.tab20(np.linspace(0, 1, len(topics)))
            bars = ax.barh(topics, [0] * len(topics), color=colors)
            ax.set_xlim(0, 1)
            ax.set_xlabel("Readiness Score")
            ax.set_title("Contest Topics Readiness Over Time")
            date_text = ax.text(0.5, 1.01, "", transform=ax.transAxes, ha="center")

            def update(frame):
                scores = scores_over_time[frame]
                for bar, height in zip(bars, scores):
                    bar.set_width(height)
                date_text.set_text(dates_with_data[frame])
                return list(bars) + [date_text]

            anim = FuncAnimation(fig, update, frames=len(scores_over_time), blit=True)
            local_path = "/tmp/contest_topics_readiness.gif"
            anim.save(local_path, writer="pillow", fps=1)
            s3_key_contest_topics = f"contest_topics_readiness_{timestamp}.gif"
            s3.upload_file(
                local_path,
                bucket_name,
                s3_key_contest_topics,
                ExtraArgs={"ContentType": "image/gif"},
            )
            plt.close(fig)
            contest_topics_img = f"![Contest Topics Readiness Over Time](https://shyal.s3.amazonaws.com/{s3_key_contest_topics})"
        else:
            contest_topics_img = "No contest topics data."

    else:
        contest_progress_img = "No readiness data."
        faang_progress_img = "No readiness data."
        contest_topics_img = "No readiness data."

    # New animation: Problem grid
    grid_anim_img = ""
    if dates_for_plot:
        total_problems = 3302
        grid_size = math.ceil(math.sqrt(total_problems))
        problem_ids = list(range(1, total_problems + 1))  # Use ints for consistency
        all_positions = []
        for idx in range(total_problems):
            row = idx // grid_size
            col = idx % grid_size
            all_positions.append(
                (col, grid_size - row - 1)
            )  # Invert y for top-left start

        problem_solve_dates = {}
        for date_str, probs in uniques_per_day.items():
            for prob in probs:
                problem_solve_dates[prob] = date_str

        solve_dates = {}
        for prob, date_str in problem_solve_dates.items():
            solve_dates[prob] = datetime.strptime(date_str, "%Y-%m-%d")

        dates_dt = [datetime.strptime(d, "%Y-%m-%d") for d in dates_for_plot]

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(-0.5, grid_size - 0.5)
        ax.set_ylim(-0.5, grid_size - 0.5)
        ax.set_axis_off()
        ax.set_aspect("equal")

        colors = {
            "Easy": "#00FF00",
            "Medium": "#FFA500",
            "Hard": "#FF0000",
            "Unknown": "#A9A9A9",  # Different from grey for unsolved if needed
        }

        all_positions_x, all_positions_y = (
            zip(*all_positions) if all_positions else ([], [])
        )

        grey_scatter = ax.scatter(
            all_positions_x, all_positions_y, s=10, c="#808080", marker="s"
        )

        solved_scatters = {}
        for diff in colors:
            solved_scatters[diff] = ax.scatter([], [], s=10, c=colors[diff], marker="s")

        date_text = ax.text(0.5, -0.05, "", transform=ax.transAxes, ha="center")

        def update(frame):
            current_dt = dates_dt[frame]
            solved_positions = defaultdict(list)
            unsolved_positions = []
            for i, prob in enumerate(problem_ids):
                solve_dt = solve_dates.get(prob)
                pos = all_positions[i]
                if solve_dt and solve_dt <= current_dt:
                    num = prob
                    diff = metadata.get(num, {}).get("difficulty", "Unknown")
                    solved_positions[diff].append(pos)
                else:
                    unsolved_positions.append(pos)
            # Update unsolved (grey)
            if unsolved_positions:
                ux, uy = zip(*unsolved_positions)
                grey_scatter.set_offsets(np.c_[ux, uy])
            else:
                grey_scatter.set_offsets(np.empty((0, 2)))
            # Update solved
            for diff, positions in solved_positions.items():
                if positions:
                    sx, sy = zip(*positions)
                    solved_scatters[diff].set_offsets(np.c_[sx, sy])
                else:
                    solved_scatters[diff].set_offsets(np.empty((0, 2)))
            date_text.set_text(dates_for_plot[frame])
            return [grey_scatter] + list(solved_scatters.values()) + [date_text]

        anim = FuncAnimation(fig, update, frames=len(dates_dt), blit=True)
        local_path = "/tmp/problem_grid.gif"
        anim.save(local_path, writer="pillow", fps=10)
        s3_key_grid = f"problem_grid_{timestamp}.gif"
        s3.upload_file(
            local_path,
            bucket_name,
            s3_key_grid,
            ExtraArgs={"ContentType": "image/gif"},
        )
        plt.close(fig)
        grid_anim_img = (
            f"![Problem Grid Animation](https://shyal.s3.amazonaws.com/{s3_key_grid})"
        )
    else:
        grid_anim_img = "No data for problem grid animation."

    with open("README.md.template", "r") as f:
        readme = f.read()

    readme = readme.replace("<!-- SOLVES_CHART -->", solves_img)
    readme = readme.replace("<!-- UNIQUES_CHART -->", uniques_img)

    if run_dates:
        readme = readme.replace("<!-- CONTEST_VARIANCE_CHART -->", contest_variance_img)
        readme = readme.replace("<!-- FAANG_VARIANCE_CHART -->", faang_variance_img)

    readme = readme.replace("<!-- CONTEST_PROGRESS -->", contest_progress_img)
    readme = readme.replace("<!-- FAANG_PROGRESS -->", faang_progress_img)
    readme = readme.replace("<!-- CONTEST_TOPICS_CHART -->", contest_topics_img)
    readme = readme.replace(
        "<!-- GRID_ANIM -->", grid_anim_img
    )  # Add this to your template

    with open("README.md", "w") as f:
        f.write(readme)

    print("README updated with S3 image links!")
    print(f"Total solves: {sum(solves_data)}")


if __name__ == "__main__":
    main()
