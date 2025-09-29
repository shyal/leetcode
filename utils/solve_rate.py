# solve_rate.py

import subprocess
import re
from datetime import datetime, timedelta, timezone
import argparse
import math
from rich import print
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
import time
import parse  # Import the modified parse.py for code reuse
import itertools
import pyfiglet


def render_big_time(secs: int, font_name: str, width: int = 200) -> str:
    if secs <= 0:
        return pyfiglet.figlet_format("TIME'S UP!", font=font_name, width=width)
    hh = secs // 3600
    mm = (secs // 60) % 60
    ss = secs % 60
    time_str = f"{hh:02d}:{mm:02d}:{ss:02d}"
    return pyfiglet.figlet_format(time_str, font=font_name, width=width)


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


def get_available_start(proposed_start, duration, task_intervals):
    current_start = proposed_start
    while True:
        overlap = False
        for task_start, task_end in task_intervals:
            if current_start < task_end and task_start < current_start + duration:
                current_start = max(current_start, task_end)
                overlap = True
                break  # Restart check after shifting
        if not overlap:
            return current_start


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
        "--break_minutes",
        type=int,
        default=10,
        help="Minutes for a break between activities (default: 10, set to 0 to disable)",
    )
    parser.add_argument(
        "--timer-font",
        type=str,
        choices=["doh", "ogre", "doom", "big", "slant", "term"],
        default="doh",
        help="Figlet font for the timer (requires pyfiglet installed)",
    )
    parser.add_argument(
        "--timer-width",
        type=int,
        default=200,
        help="Width for the timer rendering to prevent wrapping (default: 200)",
    )
    args = parser.parse_args()

    total = args.total

    if total <= 0:
        print("Total must be a positive integer.")
        exit(1)

    with open("leetcode.py", "r") as f:
        lines = f.readlines()
    with open("leetcode_easy.py", "r") as f:
        lines.extend(f.readlines())
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

    periods = [
        (1, "1 day"),
        (2, "2 days"),
        (3, "3 days"),
        (4, "4 days"),
        (5, "5 days"),
        (6, "6 days"),
        (7, "1 week"),
        (7 * 2, "2 weeks"),
    ]

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

            done_tasks = set()
            try:
                with open("done_tasks.txt", "r") as f:
                    for line in f:
                        done_task = line.strip()
                        if done_task:
                            done_tasks.add(done_task)
            except FileNotFoundError:
                pass  # File doesn't exist, assume no tasks done

            all_tasks = []
            try:
                with open("tasks.txt", "r") as f:
                    for line in f:
                        parts = [p.strip() for p in line.strip().split("|")]
                        if len(parts) == 2:
                            all_tasks.append(parts)
            except FileNotFoundError:
                all_tasks = []

            planned_tasks = []
            done_task_items = []
            early_time = today_start - timedelta(hours=1)
            for task_name, time_str in all_tasks:
                try:
                    task_time_obj = parse_time(time_str)
                    task_time = datetime.combine(
                        current_time.date(), task_time_obj, tzinfo=local_tz
                    )
                    if task_name in done_tasks:
                        done_task_items.append(
                            ("Task", task_name + " (done)", early_time, None)
                        )
                    else:
                        planned_time = max(task_time, current_time)
                        planned_tasks.append((task_name, planned_time))
                except ValueError:
                    print(f"Invalid time for task '{task_name}': {time_str}")
                    continue

            num_tasks = len(planned_tasks)
            total_planned = num_to_do_today + num_tasks

            day_end = datetime.combine(current_time.date(), end_time, tzinfo=local_tz)
            all_todays = list(solved_today)

            planned_items = []
            if total_planned > 0:
                # Compute planned_start
                if solved_today:
                    solved_today.sort(key=lambda x: x[2])
                    last_done_time = solved_today[-1][2]
                    if args.break_minutes > 0 and num_to_do_today > 0:
                        planned_start = last_done_time + timedelta(
                            minutes=args.break_minutes
                        )
                    else:
                        planned_start = last_done_time
                    planned_start = max(planned_start, current_time)
                else:
                    planned_start = current_time

                if planned_start >= day_end:
                    print("Past end time for today.")
                else:
                    remaining_time = day_end - planned_start
                    break_minutes = args.break_minutes
                    num_breaks = max(0, num_to_do_today - 1) if break_minutes > 0 else 0
                    total_break_time = num_breaks * timedelta(minutes=break_minutes)
                    if total_break_time > remaining_time:
                        print(
                            "Warning: Not enough time for all breaks; skipping breaks."
                        )
                        num_breaks = 0
                        total_break_time = timedelta(0)

                    task_duration = timedelta(hours=1)
                    estimated_task_seconds = num_tasks * 3600
                    estimated_break_seconds = total_break_time.total_seconds()
                    total_estimated_seconds = (
                        estimated_task_seconds + estimated_break_seconds
                    )
                    if total_estimated_seconds > remaining_time.total_seconds():
                        print(
                            "Warning: Not enough time for tasks and breaks; adjusting durations."
                        )

                    if num_to_do_today > 0:
                        work_seconds = (
                            remaining_time.total_seconds() - total_estimated_seconds
                        )
                        if work_seconds < 0:
                            work_seconds = 0
                        activity_duration = timedelta(
                            seconds=work_seconds / num_to_do_today
                        )
                    else:
                        activity_duration = timedelta(0)

                    # Planned problems
                    planned_problems = (
                        remaining_problems[:num_to_do_today]
                        if num_to_do_today > 0
                        else []
                    )
                    task_intervals = [
                        (task_start, task_start + task_duration)
                        for _, task_start in planned_tasks
                    ]
                    planned_problem_items = []
                    current = planned_start
                    for i, prob in enumerate(planned_problems):
                        start_time = get_available_start(
                            current, activity_duration, task_intervals
                        )
                        if start_time + activity_duration > day_end:
                            print(f"Cannot schedule problem {prob}: exceeds end time.")
                            break
                        planned_problem_items.append(
                            (prob, "", start_time, activity_duration)
                        )
                        next_current = start_time + activity_duration
                        if i < len(planned_problems) - 1 and break_minutes > 0:
                            next_current += timedelta(minutes=break_minutes)
                        current = next_current

                    # Planned tasks
                    task_planned_items = []
                    for task_name, task_start in planned_tasks:
                        task_end = task_start + task_duration
                        if task_end > day_end:
                            print(f"Warning: Task '{task_name}' exceeds end time.")
                        task_planned_items.append(
                            ("Task", task_name, task_start, task_duration)
                        )

                    planned_items = planned_problem_items + task_planned_items

            all_todays += done_task_items + planned_items

            if all_todays:
                all_todays.sort(key=lambda x: x[2])
                table2 = Table(title="Today's Schedule")
                table2.add_column("Activity", justify="left")
                table2.add_column("Details", justify="left")
                table2.add_column("Time of Day", justify="left")
                for item in all_todays:
                    if len(item) == 3:
                        activity, details, t = item
                        duration = None
                    else:
                        activity, details, t, duration = item
                    if activity == "Task" and t < today_start:
                        time_str = "Done"
                    else:
                        time_str = t.strftime("%I:%M %p")
                    style = None
                    if duration and t <= current_time < (t + duration):
                        style = "bold yellow"
                    table2.add_row(
                        str(activity) if isinstance(activity, int) else activity,
                        details,
                        time_str,
                        style=style,
                    )
                print(table2)
            else:
                print("No activities planned or done today.")

            # Check for ongoing task and start countdown if applicable
            ongoing_activity = None
            for item in all_todays:
                if len(item) == 4 and isinstance(item[0], str) and item[0] == "Task":
                    activity, details, start_t, dur = item
                    if dur and start_t <= current_time < (start_t + dur):
                        ongoing_activity = (details, start_t + dur)
                        break

            if ongoing_activity:
                task_name, end_time = ongoing_activity

                def make_display(now):
                    remaining_td = end_time - now
                    if remaining_td <= timedelta(0):
                        art = pyfiglet.figlet_format(
                            "TIME'S UP!", font=args.timer_font, width=args.timer_width
                        )
                        return Panel(
                            art + f"\n\nTask completed: {task_name}",
                            title="Timer",
                            style="bold red",
                        )
                    secs = int(remaining_td.total_seconds())
                    art = render_big_time(secs, args.timer_font, args.timer_width)
                    return Panel(
                        art, title=f"Remaining for {task_name}", style="bold cyan"
                    )

                now = datetime.now(local_tz)
                initial_display = make_display(now)
                with Live(initial_display, screen=True, refresh_per_second=1) as live:
                    while datetime.now(local_tz) < end_time:
                        time.sleep(1)
                        now = datetime.now(local_tz)
                        live.update(make_display(now))


if __name__ == "__main__":
    main()
