from functools import cache
import ast
import os
import re
import sys
from datetime import timezone, timedelta
from datetime import datetime
from git import Repo, GitCommandError
import glob


@cache
def get_solved_problems():
    repo = Repo(os.getcwd())
    git = repo.git
    log_output = git.log("--pretty=format:%H%n%an%n%ad%n%B%n---").strip()

    blocks = log_output.strip().split("---\n")
    solved = []
    manila_tz = timezone(timedelta(hours=8))
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

        try:
            commit_date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z")
            commit_date = commit_date.astimezone(manila_tz)
        except ValueError:
            print(
                f"Warning: Could not parse date '{date_str}' for commit {commit_hash}"
            )
            continue

        try:
            files_output = git.diff_tree(
                "--no-commit-id", "--name-only", "-r", commit_hash
            ).strip()
        except GitCommandError as e:
            print(
                f"Git command failed: diff-tree --no-commit-id --name-only -r {commit_hash}\nOutput: {e.stdout}\nError: {e.stderr}"
            )
            sys.exit(1)

        files = files_output.split("\n") if files_output else []

        matching_file = None
        prob_title = prob_title.replace(" ", "_").replace("'", "")
        expected_prefix = f"solved/p{prob_num}_{prob_title}_"
        for f in files:
            if f.startswith(expected_prefix):
                matching_file = f
                break

        if not matching_file:
            for F in os.listdir("./solved"):
                F = f"solved/{F}"
                if F.startswith(expected_prefix):
                    matching_file = F
                    break

        if commit_hash in [
            "64e894ff464bf9da48d109173c73b2c162f41401",
            "940c3eb4cabff002ef5b4f85bc1290b74309d262",
            "a10feb0e416afe998eef468f3cb59b424fbe896e",
            "17e20cbe3d01e559a62d49243494af145e638559",
        ]:
            continue

        if not matching_file:
            pass

        solved.append(
            (
                prob_num,
                prob_title,
                commit_date,
                solve_time,
                matching_file,
                open(matching_file).read(),
            )
        )

    solved.sort(key=lambda x: x[2])  # Sort by date ascending
    return solved


def get_today_solves():
    solved = get_solved_problems()
    manila_tz = timezone(timedelta(hours=8))
    today = datetime.now(manila_tz).date()
    today_solves = [p for p in solved if p[2].date() == today]
    return today_solves


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


def get_history_string():
    solved_problems = get_solved_problems()
    manila_tz = timezone(timedelta(hours=8))

    if not solved_problems:
        return "No previous solves recorded."

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

    # Combine solves and notes into events
    events = []
    for prob in solved_problems:
        events.append(("solve", prob[2], prob))
    for note in notes_list:
        events.append(("note", note[0], note[1]))

    # Sort events by timestamp ascending
    events.sort(key=lambda x: x[1])

    # Build the history string
    history_parts = []
    for event_type, ts, data in events:
        ts_str = ts.strftime("%Y-%m-%d %H:%M")
        if event_type == "solve":
            problem = data
            problem_id = problem[0]
            problem_title = problem[1]
            solve_time = problem[3]
            content = problem[5]

            time_str = f" (time: {solve_time})" if solve_time else ""

            notes, code = parse_content(content)

            entry = f"# {ts_str}: {problem_id}. {problem_title}{time_str}:\n\n"
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


if __name__ == "__main__":
    res = get_solved_problems()
    rich_print(res)
    print(len(res))
