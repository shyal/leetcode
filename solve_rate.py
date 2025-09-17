import subprocess
import re
from datetime import datetime, timedelta, timezone
import argparse
import os
from rich import print
from rich.table import Table


def get_git_log():
    try:
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H%n%an%n%ad%n%s%n---"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e}")
        exit(1)


def parse_commits(log_output):
    commits = []
    blocks = log_output.strip().split("---\n")
    for block in blocks:
        if not block.strip():
            continue
        lines = block.strip().split("\n")
        if len(lines) >= 4:
            commit_hash = lines[0]
            author = lines[1]
            date_str = lines[2]
            message = "\n".join(lines[3:]).strip()
            commits.append(
                {
                    "hash": commit_hash,
                    "author": author,
                    "date_str": date_str,
                    "message": message,
                }
            )
    return commits


def is_problem_commit(message):
    return re.match(r"^\d+\.", message.strip()) is not None


def main():
    parser = argparse.ArgumentParser(
        description="Predict time to solve remaining LeetCode questions based on past solve rate."
    )
    parser.add_argument(
        "--total", type=int, required=True, help="Total number of questions."
    )
    args = parser.parse_args()

    total = args.total

    if total <= 0:
        print("Total must be a positive integer.")
        exit(1)

    if not os.path.exists("leetcode.py"):
        print("leetcode.py not found.")
        exit(1)

    with open("leetcode.py", "r") as f:
        content = f.read()
        solved = content.count("class Solution")

    remaining = total - solved
    if remaining <= 0:
        print(f"You have solved {solved} out of {total}, so no remaining questions.")
        exit(0)

    log_output = get_git_log()
    commits = parse_commits(log_output)

    current_time = datetime.now(timezone.utc)

    periods = [(1, "1 day"), (3, "3 days"), (7, "1 week"), (30, "1 month")]

    print(f"Solved so far: {solved}")
    print(f"Remaining: {remaining}")

    table = Table(title="Predictions Based on Past Periods")
    table.add_column("Period", justify="left")
    table.add_column("Solve Rate (prob/day)", justify="right")
    table.add_column("Days", justify="right")
    table.add_column("Weeks", justify="right")
    table.add_column("Months", justify="right")
    table.add_column("Years", justify="right")
    table.add_column("Completion Date", justify="left")

    for past_days, label in periods:
        since_time = current_time - timedelta(days=past_days)

        solve_count = 0
        for commit in commits:
            try:
                commit_time = datetime.strptime(
                    commit["date_str"], "%a %b %d %H:%M:%S %Y %z"
                )
                if commit_time >= since_time and is_problem_commit(commit["message"]):
                    solve_count += 1
            except ValueError:
                print(
                    f"Warning: Invalid date format in commit {commit['hash']}: {commit['date_str']}"
                )
                continue

        if solve_count == 0:
            table.add_row(label, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A")
            continue

        rate = solve_count / past_days
        time_days = remaining / rate

        time_weeks = time_days / 7
        time_months = time_days / 30.437
        time_years = time_days / 365.25

        completion_time = current_time + timedelta(days=time_days)
        completion_date = completion_time.strftime("%B %d, %Y")

        table.add_row(
            label,
            f"{rate:.2f}",
            f"{time_days:.2f}",
            f"{time_weeks:.2f}",
            f"{time_months:.2f}",
            f"{time_years:.2f}",
            completion_date,
        )

    print(table)


if __name__ == "__main__":
    main()
