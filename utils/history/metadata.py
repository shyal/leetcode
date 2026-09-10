# metadata.py


import json

import requests


def get_problems_metadata():
    METADATA_FILE = "data/problems_metadata.json"
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
            # premium problems: make prepare cannot fetch the statement
            # ("Question 261 is paid only"), so the picker must never offer
            # one. Recorded only when true - 783 of 4047 carry it.
            if stat.get("paid_only"):
                problems[num]["paid_only"] = True
            if s.get("total_submitted"):
                problems[num]["acceptance"] = round(
                    100 * s["total_acs"] / s["total_submitted"], 1
                )

        with open(METADATA_FILE, "w") as f:
            json.dump(problems, f)

        return problems
    else:
        raise ValueError("Failed to fetch problems metadata")
