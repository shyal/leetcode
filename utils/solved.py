import subprocess
import os
import time


def main():
    # Find the start time
    # First, check for commit with message "started"
    result = subprocess.run(
        ["git", "log", "-1", "--grep=^started$", "--format=%ct"],
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip()

    if output:
        start_time = int(output)
    else:
        # Get the first commit on the branch
        result = subprocess.run(
            ["git", "log", "--reverse", "--format=%ct"], capture_output=True, text=True
        )
        if result.returncode != 0 or not result.stdout.strip():
            print("No commits found. Exiting.")
            return
        start_time = int(result.stdout.splitlines()[0].strip())

    current_time = time.time()
    delta_seconds = current_time - start_time

    if delta_seconds < 600:  # < 10 minutes
        target_file = "leetcode_easy.py"
    elif delta_seconds < 1800:  # < 30 minutes
        target_file = "leetcode_medium.py"
    else:
        target_file = "leetcode_hard.py"

    if not os.path.exists("current.py"):
        print("current.py does not exist. Exiting.")
        return

    with open("current.py", "r") as f:
        content = f.read()

    with open(target_file, "a") as f:
        f.write(content + "\n\n")  # Add some separation

    with open("current.py", "w") as f:
        f.write("")

    try:
        subprocess.run(["git", "add", "."], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running git add: {e}")
        return

    try:
        subprocess.run(["git", "commit", "-m", "solved"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running git commit: {e}")
        return

    try:
        subprocess.run(["make", "rebase"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running make rebase: {e}")
        return

    print("Operations completed successfully.")


if __name__ == "__main__":
    main()
