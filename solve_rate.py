# solve_rate.py

import subprocess
import re
from datetime import datetime, timedelta, timezone
import argparse
import math
from rich import print
from rich.table import Table
import parse  # Import the modified parse.py for code reuse
import itertools


def is_stub(section_lines):
    in_class = False
    in_def = False
    indent_level = 0
    body = []
    for line in section_lines:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if not in_class and line.strip().startswith("class Solution"):
            in_class = True
            indent_level = indent
            continue
        if in_class and not in_def and line.strip().startswith("def "):
            in_def = True
            indent_level = indent
            continue
        if in_def:
            if indent > indent_level:
                stripped = line.strip()
                if stripped and stripped != "pass" and not stripped.startswith("#"):
                    body.append(stripped)
            else:
                # end of def if indent decreases
                break
    return len(body) == 0


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
    message = message.strip().lower()
    if "stub" in message:
        return False
    return re.match(r"^\d+\.", message) is not None


def parse_date(date_str):
    date_str = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_str)
    date_str = date_str.replace("of ", "")
    try:
        dt = datetime.strptime(date_str, "%d %B %Y")
        return dt.date()
    except ValueError:
        raise ValueError("Invalid date format. Use like '1st of August 2026'")


def parse_time(time_str):
    try:
        dt = datetime.strptime(time_str, "%I%p")
        return dt.time()
    except ValueError:
        raise ValueError("Invalid time format. Use like '5pm'")


def main():
    parser = argparse.ArgumentParser(
        description="Predict time to solve remaining LeetCode questions based on past solve rate."
    )
    parser.add_argument(
        "--total", type=int, required=True, help="Total number of questions."
    )
    parser.add_argument(
        "--end-date", type=str, help="End date like '1st of August 2026'"
    )
    parser.add_argument(
        "--end-time", type=str, default="5pm", help="Daily end time like '5pm'"
    )
    parser.add_argument(
        "--tz-offset",
        type=float,
        default=8,
        help="Local timezone offset from UTC in hours, e.g., 8 for UTC+8",
    )
    parser.add_argument(
        "--task",
        action="append",
        default=[],
        help="Tasks to intersperse into the schedule",
    )
    parser.add_argument(
        "--break_minutes",
        type=int,
        default=10,
        help="Minutes for a break between activities (default: 10, set to 0 to disable)",
    )
    args = parser.parse_args()

    total = args.total

    if total <= 0:
        print("Total must be a positive integer.")
        exit(1)

    # Parse the current leetcode.py to get solved problems, ignoring stubs
    with open("leetcode.py", "r") as f:
        lines = f.readlines()
    _, sections = parse.extract_sections(lines)
    solved_problems = set()
    for number, section_lines in sections:
        if not is_stub(section_lines):
            solved_problems.add(number)

    solved = len(solved_problems)
    remaining = total - solved
    if remaining <= 0:
        print(f"You have solved {solved} out of {total}, so no remaining questions.")
        exit(0)

    remaining_problems = [i for i in range(1, total + 1) if i not in solved_problems]
    remaining_problems.sort()

    log_output = get_git_log()
    commits = parse_commits(log_output)

    local_tz = timezone(timedelta(hours=args.tz_offset))
    current_time = datetime.now(local_tz)

    periods = [(1, "1 day"), (2, "2 days"), (7, "1 week"), (30, "1 month")]

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
                ).astimezone(local_tz)
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

    if args.end_date:
        try:
            end_date = parse_date(args.end_date)
        except ValueError as e:
            print(e)
            exit(1)

        try:
            end_time = parse_time(args.end_time)
        except ValueError as e:
            print(e)
            exit(1)

        days_left = (end_date - current_time.date()).days
        if days_left <= 0:
            print("End date is in the past or today.")
        else:
            daily_rate = remaining / days_left
            print(
                f"\nRequired daily rate to finish by {end_date.strftime('%B %d, %Y')}: {daily_rate:.2f} problems/day"
            )

            # Today's solves: done and planned
            solved_today = []
            today_start = current_time.replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            for commit in commits:
                try:
                    commit_time = datetime.strptime(
                        commit["date_str"], "%a %b %d %H:%M:%S %Y %z"
                    ).astimezone(local_tz)
                    if commit_time >= today_start and is_problem_commit(
                        commit["message"]
                    ):
                        m = re.match(r"^(\d+)\.\s*(.*)", commit["message"].strip())
                        if m:
                            prob_num = int(m.group(1))
                            msg = m.group(2)
                            solved_today.append((prob_num, msg, commit_time))
                except ValueError:
                    continue

            num_solved_today = len(solved_today)
            target_per_day = math.ceil(daily_rate)
            num_to_do_today = max(0, target_per_day - num_solved_today)

            tasks = args.task
            num_tasks = len(tasks)

            done_tasks = set()
            try:
                with open("done_tasks.txt", "r") as f:
                    for line in f:
                        done_task = line.strip()
                        if done_task:
                            done_tasks.add(done_task)
            except FileNotFoundError:
                pass  # File doesn't exist, assume no tasks done

            # Filter tasks to ignore those already done
            planned_tasks = [task for task in tasks if task not in done_tasks]
            num_tasks = len(planned_tasks)

            total_planned = num_to_do_today + num_tasks

            day_end = datetime.combine(current_time.date(), end_time, tzinfo=local_tz)
            all_todays = list(solved_today)

            # Compute interleaved without breaks first
            planned_problems = (
                remaining_problems[:num_to_do_today] if num_to_do_today > 0 else []
            )
            interleaved = [
                item
                for item in itertools.chain.from_iterable(
                    itertools.zip_longest(planned_problems, planned_tasks)
                )
                if item is not None
            ]

            # Compute planned_start
            if solved_today:
                solved_today.sort(key=lambda x: x[2])
                last_done_time = solved_today[-1][2]
                if (
                    args.break_minutes > 0
                    and interleaved
                    and isinstance(interleaved[0], int)
                ):
                    planned_start = last_done_time + timedelta(
                        minutes=args.break_minutes
                    )
                else:
                    planned_start = last_done_time
                planned_start = max(planned_start, current_time)
            else:
                planned_start = current_time

            planned_items = []
            if planned_start >= day_end:
                print("Past end time for today.")
            else:
                if total_planned > 0:
                    remaining_time = day_end - planned_start

                    # Insert breaks if enabled, only after problems if next is also a problem
                    break_minutes = args.break_minutes
                    if break_minutes > 0 and total_planned > 1:
                        with_breaks = []
                        for i, activity in enumerate(interleaved):
                            with_breaks.append(activity)
                            if (
                                i < len(interleaved) - 1
                                and isinstance(activity, int)
                                and isinstance(interleaved[i + 1], int)
                            ):
                                with_breaks.append("Break")
                        interleaved = with_breaks

                    total_slots = len(interleaved)
                    num_breaks = total_slots - total_planned if break_minutes > 0 else 0
                    total_break_time = num_breaks * timedelta(minutes=break_minutes)
                    if total_break_time > remaining_time:
                        print(
                            f"Warning: Not enough time for all breaks; skipping breaks."
                        )
                        interleaved = [item for item in interleaved if item != "Break"]
                        total_slots = len(interleaved)
                        num_breaks = 0
                        total_break_time = timedelta(0)
                        work_time = remaining_time
                    else:
                        work_time = remaining_time - total_break_time

                    activity_duration = (
                        work_time / total_planned if total_planned > 0 else timedelta(0)
                    )

                    # Assign start times
                    current_slot_start = planned_start
                    for activity in interleaved:
                        if activity == "Break":
                            duration = timedelta(minutes=break_minutes)
                            planned_items.append(
                                (
                                    "Break",
                                    f"{break_minutes} min break",
                                    current_slot_start,
                                    duration,
                                )
                            )
                        else:
                            duration = activity_duration
                            if isinstance(activity, int):  # problem
                                planned_items.append(
                                    (activity, "", current_slot_start, duration)
                                )
                            else:  # task
                                planned_items.append(
                                    ("Task", activity, current_slot_start, duration)
                                )
                        current_slot_start += duration

            all_todays += planned_items

            if all_todays:
                all_todays.sort(key=lambda x: x[2])
                table2 = Table(title="Today's Solves")
                table2.add_column("Problem", justify="left")
                table2.add_column("Commit Message", justify="left")
                table2.add_column("Time of Day", justify="left")
                for item in all_todays:
                    if len(item) == 3:
                        prob, msg, t = item
                        duration = None
                    else:
                        prob, msg, t, duration = item
                    time_str = t.strftime("%I:%M %p")
                    style = (
                        "bold yellow"
                        if duration is not None and (t <= current_time < t + duration)
                        else None
                    )
                    table2.add_row(str(prob), msg, time_str, style=style)
                print(table2)
            else:
                print("No solves planned or done today.")


if __name__ == "__main__":
    main()
