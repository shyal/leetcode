from functools import cache
import ast
import os
import re
from datetime import timezone, timedelta
from datetime import datetime
from git import Repo
import glob
from dataclasses import dataclass
from collections import defaultdict
import json
import os
import re

grok_available = None

try:
    from xai_sdk import Client
    from xai_sdk.chat import system, user

    grok_available = True
except:
    grok_available = False

from metadata import get_problems_metadata


@dataclass
class SolvedProblem:
    num: int
    title: str
    date: datetime
    solve_time: str | None
    file: str
    content: str
    status: str
    difficulty: str


def strip_triple_ticks(text: str) -> str:
    pattern = r"^```(?:\w+)?\n|```$"
    result = re.sub(pattern, "", text, flags=re.MULTILINE)
    return result.strip()


def grok(user_prompt):
    chat = client.chat.create(
        model="grok-4-0709",
        messages=[
            system(
                "You are a helpful assistant that generates concise summaries for LeetCode problem solutions, including key ideas from the code and notes."
            ),
            user(user_prompt),
        ],
    )
    response = chat.sample()
    summary = response.content
    return strip_triple_ticks(summary)


if grok_available:
    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        raise ValueError("GROK_API_KEY environment variable not set")
    client = Client(api_key=api_key)


def parse_timestamp(ts_str):
    pattern = (
        r"(\d{4})_(\d{2})_(\d{2})T(\d{2})_(\d{2})_(\d{2})_(\d{6})(_(\d{2})_(\d{2})Z)?"
    )
    match = re.match(pattern, ts_str)
    if not match:
        return None
    year, month, day, hour, minute, second, micro, offset_group, offset_h, offset_m = (
        match.groups()
    )
    micro = int(micro)
    if offset_group:
        oh = int(offset_h) if offset_h else 0
        om = int(offset_m) if offset_m else 0
        offset = timedelta(hours=oh, minutes=om)
    else:
        offset = timedelta(0)  # assume UTC
    tz = timezone(offset)
    try:
        dt = datetime(
            int(year),
            int(month),
            int(day),
            int(hour),
            int(minute),
            int(second),
            microsecond=micro,
            tzinfo=tz,
        )
        manila_tz = timezone(timedelta(hours=8))
        return dt.astimezone(manila_tz)
    except ValueError:
        return None


@cache
def get_solved_problems():
    METADATA_FILE = ".problems_metadata.json"
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            metadata = json.load(f)
    else:
        metadata = get_problems_metadata()

    repo = Repo(os.getcwd())
    git = repo.git
    log_output = git.log("--pretty=format:%H%n%an%n%ad%n%B%n---").strip()

    blocks = log_output.strip().split("---\n")
    solved = []
    manila_tz = timezone(timedelta(hours=8))
    seen = set([])
    for block in blocks:
        if not block.strip():
            continue
        lines = block.split("\n")
        if len(lines) < 3:
            continue
        commit_hash = lines[0].strip()
        date_str = lines[2].strip()
        message_lines = lines[3:]
        message = "\n".join(message_lines).strip()

        prob_num = None
        prob_title = None
        for line in message_lines:
            stripped = line.strip()
            if stripped:
                m = re.match(r"(\d+)\.\s*(.*)", stripped)
                if m:
                    prob_num = int(m.group(1))
                    prob_title = m.group(2).strip()
                    break

        if prob_num is None or prob_title is None:
            continue

        solve_time_match = re.search(
            r"solve time:\s*([\d\sm ]+)", message, re.IGNORECASE
        )
        solve_time = solve_time_match.group(1).strip() if solve_time_match else None

        status = (
            "learning"
            if re.search(r"still learning", message, re.IGNORECASE)
            else "solved"
        )

        try:
            commit_date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z")
            commit_date = commit_date.astimezone(manila_tz)
        except ValueError:
            print(
                f"Warning: Could not parse date '{date_str}' for commit {commit_hash}"
            )
            continue

        if commit_hash in [
            "64e894ff464bf9da48d109173c73b2c162f41401",
            "940c3eb4cabff002ef5b4f85bc1290b74309d262",
            "a10feb0e416afe998eef468f3cb59b424fbe896e",
            "17e20cbe3d01e559a62d49243494af145e638559",
            "8420b5a5255242000e7e767cffe90e1c3d4afcf4",
            "f2a7c0fb52de619c89acb721f71c4dfb45428dba",
        ]:
            continue

        prob_title_clean = prob_title.replace(" ", "_").replace("'", "")
        expected_prefix = f"p{prob_num}_{prob_title_clean}_"
        candidates = [
            f
            for f in os.listdir("./solved")
            if f.startswith(expected_prefix) and f.endswith(".py")
        ]

        matching_file = None
        if candidates:
            min_delta = float("inf")
            closest_file = None
            for cand in candidates:
                timestamp_str = cand[len(expected_prefix) : -3]  # remove .py
                file_dt = parse_timestamp(timestamp_str)
                if file_dt:
                    delta = abs((commit_date - file_dt).total_seconds())
                    if delta < min_delta:
                        min_delta = delta
                        closest_file = cand
            if closest_file:
                matching_file = f"solved/{closest_file}"

        if matching_file:
            content = open(matching_file).read()

            difficulty = metadata.get(str(prob_num), {}).get("difficulty", "Unknown")

            solved.append(
                SolvedProblem(
                    num=prob_num,
                    title=prob_title,
                    date=commit_date,
                    solve_time=solve_time,
                    file=matching_file,
                    content=content,
                    status=status,
                    difficulty=difficulty,
                )
            )

    solved.sort(key=lambda x: x.date)  # Sort by date ascending
    return solved


def get_today_solves():
    solved = get_solved_problems()
    manila_tz = timezone(timedelta(hours=8))
    today = datetime.now(manila_tz).date()
    today_solves = [p for p in solved if p.date.date() == today]
    return today_solves


def get_learning():
    all_problems = get_solved_problems()
    groups = defaultdict(list)
    for p in all_problems:
        groups[p.num].append(p)
    learning = []
    for num, probs in groups.items():
        probs.sort(key=lambda x: x.date, reverse=True)  # latest first
        latest = probs[0]
        if latest.status == "learning":
            learning.append(latest)
    learning.sort(key=lambda x: x.date)  # Sort by date ascending
    return learning


def parse_content(content: str) -> tuple[str, str]:
    module = ast.parse(content)

    # Extract and process docstring for notes
    doc = ast.get_docstring(module)
    if doc is None:
        notes = ""
    else:
        if "---" in doc:
            _, notes_part = doc.split("---", 1)
            notes = "notes: \n\n" + notes_part.strip()
        else:
            notes = ""

    # Collect defined class names
    class_names = {node.name for node in module.body if isinstance(node, ast.ClassDef)}

    # Find the start of tests: the first top-level assign like var = ClassName(...) where ClassName is defined
    test_start = len(module.body)
    for i, node in enumerate(module.body):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id in class_names
        ):
            test_start = i
            break

    # Build solution body: exclude docstring if present, and exclude tests
    body_start = (
        1
        if (
            module.body
            and isinstance(module.body[0], ast.Expr)
            and isinstance(module.body[0].value, ast.Constant)
            and isinstance(module.body[0].value.value, str)
        )
        else 0
    )
    solution_body = module.body[body_start:test_start]

    # Unparse back to code string
    code_ast = ast.Module(body=solution_body, type_ignores=[])
    code = ast.unparse(code_ast).strip()

    return notes, code


def get_history_string(
    compress_older_than: int = 10, filter_out_easy: bool = False, include_notes=True
):
    solved_problems = get_solved_problems()
    manila_tz = timezone(timedelta(hours=8))

    if not solved_problems:
        return "No previous solves recorded."

    events = []

    if include_notes:
        # Collect review notes if the directory exists
        notes_dir = "./misc/review_notes/"
        notes_list = []
        if os.path.exists(notes_dir):
            notes_files = glob.glob(os.path.join(notes_dir, "*.md"))
            for f in notes_files:
                base = os.path.basename(f)
                dt_str = base[:-3]  # remove .md
                try:
                    note_dt = datetime.strptime(dt_str, "%Y-%m-%d_%H-%M-%S")
                    note_dt = note_dt.replace(tzinfo=manila_tz)
                except ValueError:
                    print(f"Warning: Could not parse date from filename '{base}'")
                    continue
                content = open(f).read().strip()
                notes_list.append((note_dt, content))
        for note in notes_list:
            events.append(("note", note[0], note[1]))

    for prob in solved_problems:
        events.append(("solve", prob.date, prob))

    # Sort events by timestamp ascending
    events.sort(key=lambda x: x[1])

    # Determine recent solves if compression is enabled
    if compress_older_than > 0:
        solve_events = [e for e in events if e[0] == "solve"]
        recent_solves = (
            set(id(e[2]) for e in solve_events[-compress_older_than:])
            if solve_events
            else set()
        )
    else:
        recent_solves = set()

    # Load or initialize summaries
    SUMMARIES_FILE = ".summaries.json"
    if os.path.exists(SUMMARIES_FILE):
        with open(SUMMARIES_FILE, "r") as f:
            summaries = json.load(f)
    else:
        summaries = {}

    # Build the history string
    history_parts = []
    for event_type, ts, data in events:
        ts_str = ts.strftime("%Y-%m-%d %H:%M")
        if event_type == "solve":
            problem = data
            if filter_out_easy and problem.difficulty.lower() == "easy":
                continue
            problem_id = problem.num
            problem_title = problem.title
            solve_time = problem.solve_time
            content = problem.content
            status = problem.status
            difficulty = problem.difficulty

            time_str = f" (time: {solve_time})" if solve_time else ""
            status_str = f" - {status}" if status != "solved" else ""

            notes, code = parse_content(content)

            if (
                grok_available
                and compress_older_than > 0
                and id(problem) not in recent_solves
            ):
                key = problem.file
                if key in summaries:
                    summary = summaries[key]
                else:
                    user_prompt = f"Generate a 10 words max summary of the solution the candidate wrote for problem {problem.num}. {problem.title}.\n\nCode:\n{code}\n\nNotes:\n{notes}."
                    print(user_prompt)
                    summary = grok(user_prompt)
                    summaries[key] = summary
                    with open(SUMMARIES_FILE, "w") as f:
                        json.dump(summaries, f, indent=4)
                entry = f"# {ts_str}: {problem_id}. {problem_title} ({difficulty}){status_str}{time_str} (compressed):\n\n{summary}\n\n---------------------\n\n"
            else:
                entry = f"# {ts_str}: {problem_id}. {problem_title} ({difficulty}){status_str}{time_str}:\n\n"
                entry += f"```python3\n{code}\n```"
                if notes:
                    entry += f"\n\n## {notes}"
                entry += "\n\n---------------------\n\n"
            history_parts.append(entry)
        elif event_type == "note":
            entry = f"# {ts_str}: Review Notes\n\n{data}\n\n---------------------\n\n"
            history_parts.append(entry)

    history_str = "".join(history_parts)  # Join without extra newlines between entries
    return history_str
