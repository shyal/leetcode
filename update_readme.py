import git
import re
from datetime import datetime, timedelta
from io import BytesIO
import base64
from collections import defaultdict
import matplotlib.pyplot as plt

repo = git.Repo(".")
commits = list(repo.iter_commits("HEAD"))  # Fetch ALL commits since repo start

solves_per_day = defaultdict(int)
uniques_per_day = defaultdict(set)
all_problem_dates = set()  # For full timeline from problem commits

for commit in commits:
    msg = commit.message.strip()
    if not msg:
        continue

    date_str = commit.committed_datetime.strftime("%Y-%m-%d")

    # Check if it's a problem commit: starts with number. Title
    prob_match = re.match(r"(\d+)\.\s+(.+)", msg)
    if not prob_match:
        continue  # Skip non-problem commits

    prob_num = prob_match.group(1)
    all_problem_dates.add(date_str)

    # Check for unsolved or stub
    is_unsolved = (
        "unsolved" in msg.lower()
        or "still learning" in msg.lower()
        or "stub" in msg.lower()
        or "readme" in msg.lower()
    )

    if not is_unsolved:
        solves_per_day[date_str] += 1
        uniques_per_day[date_str].add(prob_num)

# Get timeline from earliest to latest problem commit date (with zeros on quiet days)
if all_problem_dates:
    min_date_str = min(all_problem_dates)
    max_date_str = max(all_problem_dates)
    start = datetime.strptime(min_date_str, "%Y-%m-%d")
    end = datetime.strptime(max_date_str, "%Y-%m-%d")
    all_dates = []
    current = start
    while current <= end:
        d_str = current.strftime("%Y-%m-%d")
        all_dates.append(d_str)
        current += timedelta(days=1)
    solves_data = [solves_per_day.get(d, 0) for d in all_dates]
    uniques_data = [len(uniques_per_day.get(d, set())) for d in all_dates]
    dates_for_plot = all_dates
else:
    dates_for_plot = []
    solves_data = []
    uniques_data = []

# Generate Solves Per Day (line chart)
fig, ax = plt.subplots(figsize=(12, 5))  # Wider for longer timelines
if dates_for_plot:
    ax.plot(dates_for_plot, solves_data, marker="o")
ax.set_title("Solves Per Day (Full Repo History)")
ax.set_xlabel("Date")
ax.set_ylabel("Solves")
plt.xticks(rotation=45)
img_buffer = BytesIO()
plt.savefig(img_buffer, format="png", bbox_inches="tight")
img_buffer.seek(0)
img_data = base64.b64encode(img_buffer.getvalue()).decode()
solves_html = (
    f'<img src="data:image/png;base64,{img_data}" alt="Solves Per Day" width="800"/>'
)
plt.close()

# Generate Unique Problems Solved Daily (bar chart)
fig, ax = plt.subplots(figsize=(12, 5))
if dates_for_plot:
    ax.bar(dates_for_plot, uniques_data)
ax.set_title("Unique Problems Solved Daily (Full Repo History)")
ax.set_xlabel("Date")
ax.set_ylabel("Unique Solves")
plt.xticks(rotation=45)
img_buffer = BytesIO()
plt.savefig(img_buffer, format="png", bbox_inches="tight")
img_buffer.seek(0)
img_data = base64.b64encode(img_buffer.getvalue()).decode()
uniques_html = f'<img src="data:image/png;base64,{img_data}" alt="Unique Problems Solved Daily" width="800"/>'
plt.close()

with open("README.md.template", "r") as f:  # Use a template file
    readme = f.read()

readme = readme.replace("<!-- SOLVES_CHART -->", solves_html)
readme = readme.replace("<!-- UNIQUES_CHART -->", uniques_html)

with open("README.md", "w") as f:
    f.write(readme)

repo.git.add("README.md")
repo.index.commit("Update charts from full git log")
print("README updated!")
print(f"Total solves: {sum(solves_data)}")  # Bonus: Print total for verification
