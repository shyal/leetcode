"""Ask a cheap model for a shorter mu solution, and keep it only when it is
right: it must pass the problem's asserts and agree with the original
Python on the mutated inputs of difftest.py.

python mu/shorten.py N ...           try problems N
python mu/shorten.py all             try every cached problem
python mu/shorten.py --model M ...   use model M: gpt-* through the OpenAI
                                     API, any other (haiku) through claude -p
python mu/shorten.py --redo ...      try again problems already done

Every problem tried is kept in mu/.shorten.json, so a run stopped halfway
resumes where it was. Each shorter solution is also written, above the
mechanical one it replaces, to /tmp/mu_short/NNNN.mu.
"""

import ast
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from py2mu import CACHE, check, code_lines, one  # noqa: E402

from mu import MuError, fmt, transpile  # noqa: E402

SPEC = HERE / "spec" / "v0.4.md"
STORE = HERE / ".shorten.json"
MODEL = "gpt-5-mini"
WIDTH = 100  # a longer line is lines packed into one, not fewer lines

# a hand-written solution, the model's picture of what short means
EXAMPLE_MECHANICAL = """def maximumSafenessFactor(grid: [[int]]) -> int
  n, thieves = len(grid), list(cells(grid, eq=1))
  dist, queue = like(grid, fill=-1), deque()
  for (r, c) in thieves
    dist[r][c] = 0
    queue <- (r, c)
  for (_, (r, c)) in levels(queue)
    for (nr, nc) in nbrs(grid, r, c)
      if dist[nr][nc] == -1
        dist[nr][nc] = dist[r][c] + 1
        queue <- (nr, nc)
  def can_reach(safeness)
    if dist[0][0] < safeness
      return false
    visited = like(grid, fill=false)
    visited[0][0] = true
    q = deque([(0, 0)])
    for (_, (r, c)) in levels(q)
      if r == n - 1 and c == n - 1
        return true
      for (nr, nc) in nbrs(grid, r, c)
        if not visited[nr][nc] and dist[nr][nc] >= safeness
          visited[nr][nc] = true
          q <- (nr, nc)
    false
  left, right, ans = 0, (max for row in dist: max(row)), 0
  while left <= right
    mid = (left + right) // 2
    if can_reach(mid)
      ans, left = mid, mid + 1
    else
      right = mid - 1
  ans
"""
EXAMPLE_SHORT = """def maximumSafenessFactor(grid: [[int]]) -> int
  thieves, done = deque(cells(grid, eq=1)), set()
  for (d, p) in levels(thieves, seen=done)
    grid[p] = d
    thieves += nbrs(grid, p)
  def reach(k)
    q, seen = deque([(0, 0)]), set()
    for (_, c) in levels(q, grid, seen, gte=k)
      q += nbrs(grid, c)
    shape(grid, last_index=True) in seen
  (first k in 1..2 * len(grid) if not reach(k)) - 1
"""

SYSTEM = """You write mu, a small language for LeetCode that transpiles to Python.
The full specification follows. Use only what it describes; any Python
builtin or preloaded LeetCode name (deque, heapq, Counter, defaultdict,
bisect, math, itertools, functools) may be called as in Python.

{spec}

Your task: given a problem, a correct Python solution, and a mechanical
mu translation of it, write the SHORTEST correct mu solution, counted in
lines. You may change the algorithm, but it must stay within the time
limits the constraints imply. Prefer the helpers (cells, nbrs, levels with
seen and comparisons, like, table, adjacency, indegrees, components,
dijkstra, pairs), folds, `first`, and `memo` cases. Never put a statement
on the line of an if, for or while: every block is indented under its
header, and no line is longer than 100 characters. Keep the method name
and parameters. The method's last line is its
value.

Example. The mechanical translation of 2812. Find the Safest Path in a Grid:

{mechanical}
A shortest solution, which reuses the grid for the distances, lets levels
skip seen cells and cells below k, and replaces the binary search with
first:

{short}
Answer with a JSON object: {{"mu": "<the whole mu solution>"}}."""


def key():
    k = os.environ.get("OPENAI_API_KEY_LEET")
    path = Path.home() / ".openai_key_leet"
    return k or (path.read_text().strip() if path.exists() else None)


def ask(messages, model):
    """The model's mu. A gpt-* model goes to the OpenAI API; any other name
    goes to `claude -p`, which runs on the Claude subscription."""
    if not model.startswith("gpt-"):
        return ask_claude(messages, model)
    from openai import OpenAI

    client = OpenAI(api_key=key())
    r = client.chat.completions.create(
        model=model, messages=messages, response_format={"type": "json_object"}
    )
    text = r.choices[0].message.content or "{}"
    try:
        return json.loads(text).get("mu", "")
    except json.JSONDecodeError:
        return ""


def ask_claude(messages, model):
    system = messages[0]["content"]
    turns = []
    for m in messages[1:]:
        who = "You answered" if m["role"] == "assistant" else "User"
        turns.append(f"{who}:\n{m['content']}")
    prompt = "\n\n".join(turns) + "\n\nAnswer with the JSON object only."
    try:
        r = subprocess.run(
            ["claude", "-p", prompt, "--system-prompt", system, "--model", model,
             "--output-format", "json", "--max-turns", "1"],
            capture_output=True, text=True, timeout=600, cwd=tempfile.gettempdir(),
        )  # fmt: skip
    except subprocess.TimeoutExpired:
        return ""
    try:
        out = json.loads(r.stdout)
    except json.JSONDecodeError:
        out = {"is_error": True, "result": r.stdout}
    text = str(out.get("result", ""))
    if out.get("is_error") or r.returncode:
        low = (text + r.stderr).lower()
        if "usage limit" in low or "limit reached" in low or "limit will reset" in low:
            raise UsageLimit(text[:200])
        if "429" in low or "rate limit" in low or "overloaded" in low or "529" in low:
            raise RateLimited(text[:200])
    m = re.search(r"\{.*\}", text, re.S)
    try:
        return json.loads(m.group()).get("mu", "") if m else ""
    except json.JSONDecodeError:
        return ""


class RateLimited(Exception):
    """Too many calls at once: fewer in parallel, then again."""


class UsageLimit(Exception):
    """The plan's usage window is spent: wait for it to reset."""


class Gate:
    """How many calls may run at once. It halves on a rate limit and pauses,
    and grows by one after a run of calls that went through."""

    def __init__(self, start=12, most=24):
        self.limit, self.most, self.active, self.streak = start, most, 0, 0
        self.until = 0.0
        self.cv = threading.Condition()

    def call(self, fn, *args):
        while True:
            with self.cv:
                while self.active >= self.limit or time.time() < self.until:
                    self.cv.wait(timeout=max(1.0, self.until - time.time()))
                self.active += 1
            try:
                got = fn(*args)
            except RateLimited as e:
                self.ease(
                    60, f"rate limited ({e}); now {max(1, self.limit // 2)} at once"
                )
                continue
            except UsageLimit as e:
                self.ease(900, f"usage limit reached ({e}); waiting 15 minutes")
                continue
            finally:
                with self.cv:
                    self.active -= 1
                    self.cv.notify_all()
            with self.cv:
                self.streak += 1
                if self.streak >= 20 and self.limit < self.most:
                    self.limit, self.streak = self.limit + 1, 0
            return got

    def ease(self, pause, why):
        with self.cv:
            self.limit, self.streak = max(1, self.limit // 2), 0
            self.until = max(self.until, time.time() + pause)
            log(why)
            self.cv.notify_all()


GATE = Gate()
LOCK = threading.Lock()
SHOW = Path("/tmp/mu_short")  # every shorter solution, to read


def log(line):
    with LOCK:
        sys.stdout.write(f"{time.strftime('%H:%M:%S')} {line}\n")  # not the harness print
        sys.stdout.flush()


def attempt(src, entries, mu_src):
    """(ok, why): mu_src passes the asserts and agrees with the original."""
    try:
        mu_src = fmt(mu_src)
        py = transpile(mu_src)
    except MuError as e:
        return False, f"mu error: {e}", mu_src
    long = [ln for ln in mu_src.splitlines() if len(ln) > WIDTH]
    if long:
        return (
            False,
            f"a line is longer than {WIDTH} characters: {long[0].strip()[:60]}...",
            mu_src,
        )
    got = check(src, entries, py, diff=True)
    if got["status"] != "pass":
        return False, got.get("why", got["status"]), mu_src
    d = got.get("diff", {})
    if "differs" in d:
        method, args = d["differs"]
        return (
            False,
            f"wrong on {method}({', '.join(args)}): {d['mu']} vs {d['original']}",
            mu_src,
        )
    if not d.get("compared"):
        return False, "no mutated input could be compared", mu_src
    return True, "", mu_src


def shorten(num, model=MODEL, tries=2):
    """The shortest mu kept for problem num, and what happened."""
    base = one(num)
    if base.get("status") != "pass":
        return {"num": num, "kept": False, "why": "no mechanical translation"}
    data = json.loads((CACHE / f"{num}.json").read_text())
    src = data["solution"]
    entries = sorted(set(re.findall(r"\bsol\.(\w+)\(", src)))
    statement = ast.get_docstring(ast.parse(src)) or ""
    system = SYSTEM.format(
        spec=SPEC.read_text(), mechanical=EXAMPLE_MECHANICAL, short=EXAMPLE_SHORT
    )
    user = (
        f"Problem:\n{statement}\n\nPython solution:\n{solution_part(src)}\n\n"
        f"Mechanical mu ({base['mu_lines']} lines):\n{base['mu']}"
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    row = {
        "num": num,
        "title": data["title"],
        "before": base["mu_lines"],
        "kept": False,
    }
    for _ in range(tries):
        got = GATE.call(ask, messages, model)
        ok, why, got = attempt(src, entries, got)
        if ok and code_lines(got) < base["mu_lines"]:
            return {
                **row,
                "kept": True,
                "after": code_lines(got),
                "mu": got,
                "mechanical": base["mu"],
            }
        if ok:
            why = f"correct but {code_lines(got)} lines, not fewer than {base['mu_lines']}"
        row["why"] = why
        messages += [
            {"role": "assistant", "content": json.dumps({"mu": got})},
            {"role": "user", "content": f"That fails: {why}. Try again."},
        ]
    return {**row, "mechanical": base["mu"]}


def solution_part(src):
    tree = ast.parse(src)
    for n in tree.body:
        if isinstance(n, ast.ClassDef) and n.name == "Solution":
            return "\n".join(src.splitlines()[n.lineno - 1 : n.end_lineno])
    return src


def save(store, row, mechanical=None):
    """Keep row in the store and write it where it can be read:
    /tmp/mu_short/NNNN.mu holds the shorter mu over the mechanical one."""
    with LOCK:
        store[str(row["num"])] = row
        STORE.write_text(json.dumps(store, indent=1))
    if not row.get("kept"):
        return
    SHOW.mkdir(exist_ok=True)
    head = (
        f"# {row['num']}. {row['title']}: {row['before']} lines became {row['after']}\n"
    )
    body = head + row["mu"]
    if mechanical:
        quoted = "\n".join("# " + ln if ln else "#" for ln in mechanical.splitlines())
        body += "\n\n# the mechanical translation:\n" + quoted + "\n"
    (SHOW / f"{row['num']:04d}.mu").write_text(body)


def main(args):
    model, redo = MODEL, "--redo" in args
    args = [a for a in args if a != "--redo"]
    if args[:1] == ["--model"]:
        model, args = args[1], args[2:]
    if args == ["all"]:
        nums = sorted(int(p.stem) for p in CACHE.glob("*.json") if p.stem.isdigit())
    else:
        nums = [int(a) for a in args if a.isdigit()]
    if not nums:
        sys.exit(__doc__)
    store = json.loads(STORE.read_text()) if STORE.exists() else {}
    todo = [n for n in nums if redo or str(n) not in store]
    log(f"{len(nums) - len(todo)} already done; {len(todo)} to go with {model}.")
    from concurrent.futures import ThreadPoolExecutor

    counts = {"kept": 0, "tried": 0}

    def work(n):
        try:
            row = shorten(n, model)
        except Exception as e:  # one problem's crash must not stop the run
            row = {"num": n, "kept": False, "why": f"crashed: {e!r}"[:200]}
        save(store, row, row.pop("mechanical", None))
        counts["tried"] += 1
        counts["kept"] += row["kept"]
        if row["kept"]:
            log(f"{n}. {row['title']}: {row['before']} lines became {row['after']}.")
        if counts["tried"] % 25 == 0:
            log(
                f"{counts['tried']} of {len(todo)} tried, {counts['kept']} kept, {GATE.limit} at once."
            )

    with ThreadPoolExecutor(GATE.most) as pool:
        list(pool.map(work, todo))
    log(f"done: {counts['tried']} tried, {counts['kept']} kept.")


if __name__ == "__main__":
    main(sys.argv[1:])
