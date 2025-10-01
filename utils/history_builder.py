# history_builder.py

from datetime import datetime

import re
from typing import List, Tuple
import subprocess
import sys


def run_git(cmd):
    """Run a git command and return its output."""
    try:
        return (
            subprocess.check_output(["git"] + cmd, stderr=subprocess.STDOUT)
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(cmd)}\nOutput: {e.output.decode()}")
        sys.exit(1)


def get_solved_problems():
    log_output = run_git(["log", "--pretty=format:%H%n%an%n%ad%n%B%n---"])
    blocks = log_output.strip().split("---\n")
    solved = []
    for block in blocks:
        if not block.strip():
            continue
        lines = block.split("\n")
        if len(lines) < 3:
            continue
        commit_hash = lines[0].strip()
        author = lines[1].strip()
        date_str = lines[2].strip()
        message_lines = lines[3:]
        message = "\n".join(message_lines).strip()

        # Parse problem from first matching line
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

        # Parse solve time if present
        solve_time_match = re.search(
            r"solve time:\s*([\d\sm ]+)", message, re.IGNORECASE
        )
        solve_time = solve_time_match.group(1).strip() if solve_time_match else None

        try:
            commit_date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z")
        except ValueError:
            print(
                f"Warning: Could not parse date '{date_str}' for commit {commit_hash}"
            )
            continue

        solved.append((prob_num, prob_title, commit_date, solve_time))

    solved.sort(key=lambda x: x[2])  # Sort by date ascending
    return solved


def parse_content(content: str) -> Tuple[str, str]:
    """
    Parses the given content to extract notes and user code.

    :param content: The string content to parse.
    :return: A tuple (notes, code)
    """
    if not content.startswith('"""'):
        return "", content  # If no docstring, assume all is code, no notes

    end_doc = content.find('"""', 3)
    if end_doc == -1:
        return "", content  # Incomplete docstring

    docstring = content[3:end_doc].strip()
    code_part = content[end_doc + 3 :].strip()

    # Extract notes: anything after ---
    if "---" in docstring:
        _, notes = docstring.split("---", 1)
        notes = "notes: \n\n" + notes.strip()
    else:
        notes = ""

    # Extract code: everything before 'sol = Solution()'
    sol_index = code_part.find("sol = Solution()")
    if sol_index != -1:
        code = code_part[:sol_index].strip()
    else:
        code = code_part  # If no marker, take all code_part

    return notes, code
