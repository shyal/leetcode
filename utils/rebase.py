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


def main(branch_name):
    if not branch_name:
        print("Usage: python script.py <branch_name>")
        sys.exit(1)

    # Checkout the branch
    run_git(["checkout", branch_name])

    # Rebase the branch onto master
    run_git(["rebase", "master"])

    # Get the commits unique to the branch (after rebase, on top of master)
    commits = run_git(["rev-list", "master.." + branch_name]).splitlines()
    # Reverse to process from oldest to newest
    commits.reverse()

    # Collect messages from non-fixup commits
    message_parts = []
    for commit_hash in commits:
        subject = run_git(["log", "-1", "--format=%s", commit_hash])
        if not (subject.startswith("fixup! ") or subject.startswith("squash! ")):
            body = run_git(["log", "-1", "--format=%b", commit_hash])
            full_msg = subject
            if body:
                full_msg += "\n\n" + body
            message_parts.append(full_msg)

    if not message_parts:
        print("No non-fixup commits found on the branch.")
        sys.exit(1)

    final_message = "\n\n".join(message_parts)

    # Checkout master
    run_git(["checkout", "master"])

    # Perform the squash merge
    run_git(["merge", "--squash", branch_name])

    # Commit with the constructed message
    subprocess.check_call(["git", "commit", "-m", final_message])

    print("Squash commit created on master with non-fixup messages.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <branch_name>")
        sys.exit(1)
    main(sys.argv[1])
