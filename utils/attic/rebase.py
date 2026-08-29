import subprocess
import sys
from datetime import datetime


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


def main(branch_name):
    run_git(["checkout", branch_name])
    run_git(["rebase", "master"])
    commits_output = run_git(["rev-list", "master.." + branch_name])
    if not commits_output:
        print("No commits unique to the branch.")
        sys.exit(1)
    commits = commits_output.splitlines()
    commits.reverse()
    initial_hash = commits[0]
    initial_msg = run_git(["log", "-1", "--format=%s", initial_hash])
    start_date = None
    end_date = None
    solved_body = ""
    for commit_hash in commits:
        subject = run_git(["log", "-1", "--format=%s", commit_hash])
        date_str = run_git(["log", "-1", "--format=%aI", commit_hash])
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
        if subject == "started":
            start_date = date
        if subject == "solved":
            end_date = date
            solved_body = run_git(["log", "-1", "--format=%b", commit_hash]).strip()
    if start_date is None:
        start_date_str = run_git(["log", "-1", "--format=%aI", initial_hash])
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S%z")
    if end_date is None:
        print("No 'solved' commit found.")
        sys.exit(1)
    delta = end_date - start_date
    total_sec = int(delta.total_seconds())
    minutes = total_sec // 60
    seconds = total_sec % 60
    solve_time_str = f"{minutes}m {seconds}s"
    final_message = f"{initial_msg}\n\nsolve time: {solve_time_str}"
    if solved_body:
        final_message += f"\n\n{solved_body}"
    run_git(["checkout", "master"])
    run_git(["merge", "--squash", branch_name])
    subprocess.check_call(["git", "commit", "-m", final_message])
    print(
        "Squash commit created on master with initial message, solve time, and notes."
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        branch_name = run_git(["branch", "--show-current"]).strip()
    else:
        branch_name = sys.argv[1]
    if not branch_name:
        print("Could not determine branch name.")
        sys.exit(1)
    main(branch_name)
