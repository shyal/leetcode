from rich.console import Console
from rich.markdown import Markdown
import subprocess
import os
import re
import sys
from datetime import datetime
from xai_sdk import Client
from xai_sdk.chat import system, user

console = Console()


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


api_key = os.getenv("GROK_API_KEY")
if not api_key:
    raise ValueError("GROK_API_KEY environment variable not set")

client = Client(api_key=api_key)


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


def main():
    solved_problems = get_solved_problems()

    if not solved_problems:
        history_str = "No previous solves recorded."
    else:
        history_str = "\n".join(
            [
                f"{p[2].strftime('%Y-%m-%d %H:%M')}: {p[0]}. {p[1]}{f' (time: {p[3]})' if p[3] else ''}"
                for p in solved_problems
            ]
        )

    system_prompt = """You are an expert LeetCode coach specializing in building strong fundamentals. Analyze the user's solve history to identify patterns in topics covered (e.g., arrays, strings, linked lists, trees, graphs, stacks/queues, dynamic programming, sorting/searching, etc.), difficulties attempted, and potential weak areas (e.g., topics rarely or never attempted, or where solve times were unusually long if provided). 

Recommend EXACTLY ONE next problem to solve. 
Your goal is for the user to hit his average number of solves over the last few days.
To do that, try to sandwich the day: for the first N / 3 solves (where N is the average over the last few days), start with easy questions that he can solve easily. This is to build confidence.
Then for the middle (N / 3) solves, pick a mix of easy and medium questions that will reinforce gaps in his fundamentals knowledge.
For the last (N / 3) solves, pick easy questions again so he can wrap up the day nicely.

For your recommendation, specify:
- Problem number and full title (e.g., "1. Two Sum").
- Difficulty: Easy or Medium.
- Main topic(s): 1-3 key topics (e.g., Array, Hash Table).
- Why this problem: A brief explanation (2-4 sentences) on how it targets weaknesses, builds skills, or progresses learning.

Keep the response concise, structured, and encouraging. Do not recommend hard problems."""

    user_prompt = f"""Here is my LeetCode solve history (most recent last):\n\n{history_str}\n\nBased on this, recommend my next problem."""

    try:
        chat = client.chat.create(
            model="grok-4-0709",
            messages=[
                system(system_prompt),
                user(user_prompt),
            ],
        )
        response = chat.sample()
        recommendation = response.content
        md = Markdown(recommendation)
        console.print(md)
    except Exception as e:
        print(f"Error calling xAI API: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
