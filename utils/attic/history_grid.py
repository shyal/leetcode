# history_grid.py

from history_builder import *
from flask import Flask, render_template_string
import math
import html
from datetime import datetime
from collections import defaultdict


def parse_solve_time(s: str | None) -> int | None:
    if not s:
        return None
    total = 0
    for part in s.split():
        if "h" in part:
            total += int(part[:-1]) * 3600
        elif "m" in part:
            total += int(part[:-1]) * 60
        elif "s" in part:
            total += int(part[:-1])
    return total


def format_time(seconds: int) -> str:
    if seconds == 0:
        return "N/A"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if secs:
        parts.append(f"{secs}s")
    return " ".join(parts)


app = Flask(__name__)


@app.route("/")
def home():
    all_problems = get_solved_problems()
    groups = defaultdict(list)
    for p in all_problems:
        groups[p.num].append(p)

    problem_data = []
    time_now = datetime.now()
    for num, probs in groups.items():
        probs.sort(key=lambda x: x.date)
        count_learning = sum(1 for p in probs if p.status == "learning")
        solve_times_raw = [
            parse_solve_time(p.solve_time) for p in probs if p.solve_time
        ]
        solve_times = [t for t in solve_times_raw if t is not None]
        cumulative_time = sum(solve_times) if solve_times else 0
        avg_time = (
            cumulative_time / len(solve_times) if solve_times else 300
        )  # default 5min if no times
        latest = probs[-1]
        last_time = (
            parse_solve_time(latest.solve_time) if latest.solve_time else avg_time
        )
        time_diff = time_now - latest.date.replace(tzinfo=None)
        time_since_days = max(0, time_diff.total_seconds() / 86400)
        # Spaced repetition inspired score: higher if struggled more, longer ago, slower last time
        score = (
            count_learning
            * (cumulative_time + 1)
            * (time_since_days + 0.1)
            * ((last_time / 60) + 1)
        )
        problem_data.append(
            {
                "num": num,
                "title": latest.title,
                "difficulty": latest.difficulty,
                "status": latest.status,
                "score": score,
                "cumulative_time": cumulative_time,
            }
        )

    # Sort by score descending (struggled most first)
    problem_data.sort(key=lambda x: x["score"], reverse=True)

    # Compute grid dimensions
    N = len(problem_data)
    if N == 0:
        return "<h1>No problems found in solve history.</h1>"

    # Find min/max score for coloring
    all_scores = [p["score"] for p in problem_data]
    min_score = min(all_scores) if all_scores else 0
    max_score = max(all_scores) if all_scores else 1

    def get_color_and_text(score):
        if max_score == min_score:
            bg = "rgb(0,255,0)" if min_score == 0 else "rgb(255,0,0)"
            luminance = (
                0.299 * 0 + 0.587 * 255 + 0.114 * 0
                if min_score == 0
                else 0.299 * 255 + 0.587 * 0 + 0.114 * 0
            )
            text_color = "#fff" if luminance < 128 else "#000"
            return bg, text_color

        log_score = math.log(score + 1)
        log_min = math.log(min_score + 1)
        log_max = math.log(max_score + 1)

        if log_max - log_min == 0:
            bg = "rgb(0,255,0)" if log_min == 0 else "rgb(255,0,0)"
            luminance = (
                0.299 * 0 + 0.587 * 255 + 0.114 * 0
                if log_min == 0
                else 0.299 * 255 + 0.587 * 0 + 0.114 * 0
            )
            text_color = "#fff" if luminance < 128 else "#000"
            return bg, text_color

        norm = (log_score - log_min) / (log_max - log_min)

        if norm < 0.5:
            r = int(255 * (norm * 2))
            g = 255
        else:
            r = 255
            g = int(255 * (1 - (norm - 0.5) * 2))
        b = 0

        bg = f"rgb({r},{g},{b})"
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        text_color = "#fff" if luminance < 128 else "#000"
        return bg, text_color

    # Build HTML
    html_str = """
    <style>
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px;
        }
        .cell {
            padding: 10px;
            border: 1px solid #ccc;
            text-align: center;
            display: block;
            text-decoration: none;
        }
    </style>
    <div class="grid">
    """

    for cell in problem_data:
        color, text_color = get_color_and_text(cell["score"])
        time_str = format_time(cell["cumulative_time"])
        html_str += f'<a href="/problem/{cell["num"]}" class="cell" style="background-color: {color}; color: {text_color};">{cell["num"]}. {cell["title"]} ({cell["difficulty"]}) - {cell["status"]}<br>Cumulative Time: {time_str}</a>'

    html_str += "</div>"

    return render_template_string(html_str)


@app.route("/problem/<int:num>")
def problem(num):
    all_problems = get_solved_problems()
    groups = defaultdict(list)
    for p in all_problems:
        groups[p.num].append(p)

    attempts = groups.get(num, [])
    if not attempts:
        return "Problem not found", 404

    attempts.sort(key=lambda x: x.date)

    latest = attempts[-1]
    html_str = f"<h1>{num}. {latest.title} ({latest.difficulty})</h1>"
    html_str += '<a href="/">Back to Grid</a><br><br>'

    for att in attempts:
        ts_str = att.date.strftime("%Y-%m-%d %H:%M")
        status = att.status
        solve_time_sec = parse_solve_time(att.solve_time) or 0
        solve_time = format_time(solve_time_sec)
        notes, code = parse_content(att.content)
        code_escaped = html.escape(code)
        notes_escaped = html.escape(notes)

        html_str += f"<h2>Attempt on {ts_str} - {status} - Time: {solve_time}</h2>"
        html_str += f"<h3>Code:</h3><pre><code>{code_escaped}</code></pre>"
        if notes:
            html_str += f"<h3>Notes:</h3><pre><code>{notes_escaped}</code></pre>"
        html_str += "<hr>"

    return render_template_string(html_str)


if __name__ == "__main__":
    app.run(debug=True)
