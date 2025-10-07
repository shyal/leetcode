import git
import re
from datetime import datetime, timedelta, date
from collections import defaultdict
import matplotlib as mpl

mpl.use("module://mpl_ascii")  # Set backend before importing pyplot
import matplotlib.pyplot as plt
import sys
import io
import json

repo = git.Repo(".")
commits = list(repo.iter_commits("HEAD"))  # Fetch ALL commits since repo start

solves_per_day = defaultdict(int)
uniques_per_day = defaultdict(set)
all_problem_dates = set()  # For full timeline from problem commits

for commit in commits:
    msg = commit.message.strip()
    if not msg:
        continue

    date_str = commit.committed_datetime.strftime("%Y-%m-%d")

    # Check if it's a problem commit: starts with number. Title
    prob_match = re.match(r"(\d+)\.\s+(.+)", msg)
    if not prob_match:
        continue  # Skip non-problem commits

    prob_num = prob_match.group(1)
    all_problem_dates.add(date_str)

    # Check for unsolved or stub
    is_unsolved = (
        "unsolved" in msg.lower()
        or "still learning" in msg.lower()
        or "stub" in msg.lower()
        or "readme" in msg.lower()
    )

    if not is_unsolved:
        solves_per_day[date_str] += 1
        uniques_per_day[date_str].add(prob_num)

# Get timeline from earliest to latest problem commit date (with zeros on quiet days)
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
    dates_for_plot = all_dates
else:
    dates_for_plot = []
    solves_data = []
    uniques_data = []


# Function to capture ASCII from plt.show()
def capture_ascii_plot():
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    plt.show()
    sys.stdout = old_stdout
    return mystdout.getvalue().strip()  # Strip extra newlines


# Common logic for x-ticks (numerical indices, sparse date labels)
if dates_for_plot:
    x = list(range(len(dates_for_plot)))
    label_step = max(1, len(dates_for_plot) // 10)  # ~10 labels for readability
    tick_positions = x[::label_step]
    tick_labels = dates_for_plot[::label_step]

# Generate Solves Per Day (line chart)
fig, ax = plt.subplots(figsize=(12, 5))  # Size affects ASCII density
if dates_for_plot:
    ax.plot(x, solves_data, marker="o")
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45)
ax.set_title("Solves Per Day (Full Repo History)")
ax.set_xlabel("Date")
ax.set_ylabel("Solves")
solves_ascii = capture_ascii_plot()
plt.close()

# Generate Unique Problems Solved Daily (bar chart)
fig, ax = plt.subplots(figsize=(12, 5))
if dates_for_plot:
    ax.bar(x, uniques_data)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45)
ax.set_title("Unique Problems Solved Daily (Full Repo History)")
ax.set_xlabel("Date")
ax.set_ylabel("Unique Solves")
uniques_ascii = capture_ascii_plot()
plt.close()

# Load readiness.json and generate variance charts
with open("readiness.json", "r") as f:
    readiness_data = json.load(f)

# Sort by run_date
readiness_data.sort(key=lambda item: item["run_date"])

run_dates = [item["run_date"] for item in readiness_data]
contest_readiness = [item["contest_readiness"] for item in readiness_data]
faang_readiness = [item["faang_interview"] for item in readiness_data]

# Convert to datetime objects
run_dt = [datetime.strptime(d, "%Y-%m-%d") for d in run_dates]
contest_dt = [datetime.strptime(d, "%Y-%m-%d") for d in contest_readiness]
faang_dt = [datetime.strptime(d, "%Y-%m-%d") for d in faang_readiness]

# For contest variance chart
contest_variance_ascii = ""
if run_dates:
    min_run = min(run_dt)
    min_contest = min(contest_dt)
    x_num = [(dt - min_run).days for dt in run_dt]
    y_num = [(dt - min_contest).days for dt in contest_dt]

    # x ticks
    label_step = max(1, len(run_dates) // 10)
    tick_pos_x = x_num[::label_step]
    tick_labels_x = run_dates[::label_step]

    # y ticks: unique sorted dates
    unique_contest = sorted(set(contest_dt))
    tick_pos_y = [(dt - min_contest).days for dt in unique_contest]
    tick_labels_y = [dt.strftime("%Y-%m-%d") for dt in unique_contest]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(x_num, y_num, marker="o")
    ax.set_xticks(tick_pos_x)
    ax.set_xticklabels(tick_labels_x, rotation=45)
    ax.set_yticks(tick_pos_y)
    ax.set_yticklabels(tick_labels_y)
    ax.set_title("Contest Readiness Projection Over Time")
    ax.set_xlabel("Run Date")
    ax.set_ylabel("Projected Readiness Date")
    contest_variance_ascii = capture_ascii_plot()
    plt.close()

# For FAANG variance chart
faang_variance_ascii = ""
if run_dates:
    min_faang = min(faang_dt)
    y_num_faang = [(dt - min_faang).days for dt in faang_dt]

    unique_faang = sorted(set(faang_dt))
    tick_pos_y_faang = [(dt - min_faang).days for dt in unique_faang]
    tick_labels_y_faang = [dt.strftime("%Y-%m-%d") for dt in unique_faang]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(x_num, y_num_faang, marker="o")
    ax.set_xticks(tick_pos_x)
    ax.set_xticklabels(tick_labels_x, rotation=45)
    ax.set_yticks(tick_pos_y_faang)
    ax.set_yticklabels(tick_labels_y_faang)
    ax.set_title("FAANG Interview Readiness Projection Over Time")
    ax.set_xlabel("Run Date")
    ax.set_ylabel("Projected Readiness Date")
    faang_variance_ascii = capture_ascii_plot()
    plt.close()

# Get last readiness values
if readiness_data:
    last_readiness = readiness_data[-1]  # After sorting, last is latest
    contest_end_str = last_readiness["contest_readiness"]
    faang_end_str = last_readiness["faang_interview"]

    # Start date from repo
    if all_problem_dates:
        start_dt = datetime.strptime(min_date_str, "%Y-%m-%d")
        current_dt = datetime.combine(
            date.today(), datetime.min.time()
        )  # Fix: make current_dt a datetime

        # Contest progress
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
        ax.barh([0], [progress_contest * 100], height=0.5)
        ax.set_yticks([0])
        ax.set_yticklabels(["Progress"])
        ax.set_xlim(0, 100)
        ax.set_xlabel("Percentage Complete")
        ax.set_title(f"Contest Readiness Progress (Ready by {contest_end_str})")
        contest_progress_ascii = capture_ascii_plot()
        plt.close()

        # FAANG progress
        faang_end_dt = datetime.strptime(faang_end_str, "%Y-%m-%d")
        total_days_faang = (faang_end_dt - start_dt).days
        elapsed_days_faang = (current_dt - start_dt).days
        progress_faang = max(
            0,
            min(
                1, elapsed_days_faang / total_days_faang if total_days_faang > 0 else 0
            ),
        )

        fig, ax = plt.subplots(figsize=(10, 2))
        ax.barh([0], [progress_faang * 100], height=0.5)
        ax.set_yticks([0])
        ax.set_yticklabels(["Progress"])
        ax.set_xlim(0, 100)
        ax.set_xlabel("Percentage Complete")
        ax.set_title(f"FAANG Interview Readiness Progress (Ready by {faang_end_str})")
        faang_progress_ascii = capture_ascii_plot()
        plt.close()
    else:
        contest_progress_ascii = "No repo history for progress calculation."
        faang_progress_ascii = "No repo history for progress calculation."
else:
    contest_progress_ascii = "No readiness data."
    faang_progress_ascii = "No readiness data."

with open("README.md.template", "r") as f:  # Use a template file
    readme = f.read()

# Replace placeholders with Markdown code blocks for ASCII
solves_block = f"```\n{solves_ascii}\n```"
uniques_block = f"```\n{uniques_ascii}\n```"
readme = readme.replace("<!-- SOLVES_CHART -->", solves_block)
readme = readme.replace("<!-- UNIQUES_CHART -->", uniques_block)

# Add readiness charts (assume placeholders like <!-- CONTEST_VARIANCE_CHART --> and <!-- FAANG_VARIANCE_CHART --> in template)
if run_dates:
    contest_block = f"```\n{contest_variance_ascii}\n```"
    faang_block = f"```\n{faang_variance_ascii}\n```"
    readme = readme.replace("<!-- CONTEST_VARIANCE_CHART -->", contest_block)
    readme = readme.replace("<!-- FAANG_VARIANCE_CHART -->", faang_block)

# Add progress bars (assume placeholders <!-- CONTEST_PROGRESS --> and <!-- FAANG_PROGRESS -->)
contest_progress_block = f"```\n{contest_progress_ascii}\n```"
faang_progress_block = f"```\n{faang_progress_ascii}\n```"
readme = readme.replace("<!-- CONTEST_PROGRESS -->", contest_progress_block)
readme = readme.replace("<!-- FAANG_PROGRESS -->", faang_progress_block)

with open("README.md", "w") as f:
    f.write(readme)

# repo.git.add("README.md")
# repo.index.commit("Update charts from full git log and readiness.json via mpl_ascii")
print("README updated!")
print(f"Total solves: {sum(solves_data)}")  # Bonus: Print total for verification
