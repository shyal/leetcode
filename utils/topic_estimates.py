#!/usr/bin/env python3

from rich import print
from rich.console import Console
import os
import sys
from datetime import datetime, timezone, timedelta
import json
import subprocess as _subprocess
from history_builder import get_history_string

console = Console()


def main():
    history_str = get_history_string(0)
    assert history_str

    system_prompt = """You are an expert LeetCode coach specializing in assessing candidate readiness.

Based on the user's solve history and previous estimates (if provided), estimate readiness per topic:

{
    "binary_search": 0.5, # floating point value as fraction of readiness (50%)
    "heaps": 0.3, # floating point value as fraction of readiness (30%)
    "two_pointer": 0.7, # floating point value as fraction of readiness (70%)
    etc.
}

The goal is to be leetcode contest ready by 2025-11-15. If previous estimates are provided, use them as a baseline and adjust based on new information. Generate valid JSON and nothing else.
"""

    # Load existing data to find previous estimates
    data = []
    previous_estimates = None
    if os.path.exists("readiness.json"):
        try:
            with open("readiness.json", "r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                data = []
        except json.JSONDecodeError:
            data = []

        # Sort by run_date descending to find the latest with contest_topics_readiness
        data.sort(key=lambda x: x.get("run_date", "0000-00-00"), reverse=True)
        for entry in data:
            if "contest_topics_readiness" in entry:
                previous_estimates = entry["contest_topics_readiness"]
                break

    user_prompt = f"""Here is my LeetCode solve history (most recent last):\n\n{history_str}\n\nBased on this, estimate my readiness percentages."""
    if previous_estimates:
        user_prompt += (
            f"\n\nPrevious topic estimates:\n{json.dumps(previous_estimates, indent=2)}"
        )

    with open("_estimate_prompt.txt", "w") as w:
        w.write(user_prompt)

    try:
        result = _subprocess.run(
            ["claude", "-p", user_prompt, "--system-prompt", system_prompt],
            capture_output=True, text=True,
        )
        recommendation = result.stdout.strip()
        estimates = json.loads(recommendation)
        print(estimates)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from API response: {e}")
        print(f"Response: {recommendation}")
        sys.exit(1)
    except Exception as e:
        print(f"Error calling xAI API: {e}")
        sys.exit(1)

    manila_tz = timezone(timedelta(hours=8))
    today = datetime.now(manila_tz).strftime("%Y-%m-%d")

    new_entry = {"run_date": today, "contest_topics_readiness": estimates}
    data.append(new_entry)

    # Resort the data by run_date ascending before saving
    data.sort(key=lambda x: x.get("run_date", "0000-00-00"))

    print(data)

    with open("readiness.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
