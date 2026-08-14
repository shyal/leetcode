# metadata.py


import json
import os
import requests


def get_problems_metadata():
    METADATA_FILE = ".problems_metadata.json"
    url = "https://leetcode.com/api/problems/all/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        problems = {}
        for stat in data["stat_status_pairs"]:
            s = stat["stat"]
            num = s["frontend_question_id"]
            title = s["question__title"]
            slug = s["question__title_slug"]
            diff = stat["difficulty"]["level"]  # 1,2,3
            diff_str = {1: "Easy", 2: "Medium", 3: "Hard"}[diff]
            problems[num] = {"title": title, "slug": slug, "difficulty": diff_str}
            if s.get("total_submitted"):
                problems[num]["acceptance"] = round(
                    100 * s["total_acs"] / s["total_submitted"], 1)

        with open(METADATA_FILE, "w") as f:
            json.dump(problems, f)

        return problems
    else:
        raise ValueError("Failed to fetch problems metadata")
