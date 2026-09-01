"""Recognition: the step before execution. A node's drill bank trains the
move once it is named; nothing trained reading an unnamed statement and
reaching for the right move. 84 (2026-08-21) and 1760 (2026-09-01) were both
that failure, on nodes whose execution evidence was clean.

A spot rep is a problem statement with the title, number and tags removed,
answered in free text: which move solves it, or "direct" when none does.
No code. The rep lives on a branch like a solve (`make prepare spot` writes
current.md, `make solved` files it under recognition/), and its evidence
goes to graph/recognition.json, a second axis per node next to
evidence.json: execution says whether the move runs once named,
recognition says whether the statement triggers it.

Records, keyed by file like evidence.json, verdicts "hit" / "missed":

    recognition/s1760_..._2026_09_01T05_12_00Z.md   a spot rep
    solved/p84_..._2026_08_21T01_19_20Z.py          a solve whose notes say
                                                    a move was not seen

Status per node is derived at query time, never stored: FAILED_TO_RECOGNIZE when
the latest event is a miss, RECOGNIZED when it is a hit inside the window,
UNTESTED otherwise (no event, or a hit that has lapsed). The window is
SOLID_WINDOW_DAYS grown 1.3x per hit, the same shape execution uses."""

import glob
import json
import os
import re
from datetime import date, timedelta
from html.parser import HTMLParser

from kg.kg_lib import (
    GRAPH_DIR, REPO_ROOT, SOLID, SOLID_WINDOW_DAYS, gentleness, pnum_key,
    solved_problems, taxonomy_summary, claude_json, load_predicted,
    problem_difficulty, ev_index,
)

RECOGNITION_JSON = os.path.join(GRAPH_DIR, "recognition.json")
RECOGNITION_DIR = os.path.join(REPO_ROOT, "recognition")
SPOT_META = os.path.join(REPO_ROOT, ".spot.json")  # untracked: branch -> pick
CACHE_DIR = os.path.join(REPO_ROOT, ".prepare_cache")

RECOGNIZED, FAILED_TO_RECOGNIZE, UNTESTED = "RECOGNIZED", "FAILED_TO_RECOGNIZE", "UNTESTED"
HIT, MISSED = "hit", "missed"
ANSWER_MARK = "<!-- answer -->"
FOOTER_RE = re.compile(r"<!-- spot (\{.*?\}) -->\s*$", re.S)
SPOT_FNAME_RE = re.compile(r"^s(\d+)_")
# the ratio: one spot rep per SPOT_EVERY solves, counted over the day. The
# first rep of the day is due before the first solve; the next after
# SPOT_EVERY more solves (drills count). 0 turns spot reps off.
SPOT_EVERY = int(os.environ.get("SPOT_EVERY", 3))


# ---- storage ---------------------------------------------------------------

def load_recognition():
    try:
        with open(RECOGNITION_JSON) as f:
            return json.load(f)["recognition"]
    except (OSError, ValueError, KeyError):
        return {}


def save_recognition(recog):
    doc = {
        "_comment": (
            "Per file: whether the statement triggered the move. Verdicts: hit "
            "(the entry move was named from the statement alone), missed (it was "
            "not). Spot reps (recognition/*.md) and solves whose notes say a move "
            "was not seen (solved/*.py) both land here. Append-only; "
            "utils/kg/kg_extract writes it. Status is derived at query time by "
            "kg.recognition.recognition_status."
        ),
        "recognition": recog,
    }
    tmp = RECOGNITION_JSON + ".tmp"
    with open(tmp, "w") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, RECOGNITION_JSON)


def load_spot_meta():
    try:
        with open(SPOT_META) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_spot_meta(meta):
    with open(SPOT_META, "w") as f:
        json.dump(meta, f, indent=2)


# ---- the walk's entry ------------------------------------------------------

def entry_nodes(pnum, problems):
    """The moves a statement can trigger: the first move of the mapped walk
    and of every alt walk. Later moves (solve-pair-condition inside 1760)
    are reached while executing, not read off the statement, so they are
    never scored. The mapped walk's first move is the primary entry."""
    p = problems.get(str(pnum), {})
    walks = [p.get("moves", [])] + [w for w in p.get("alt_walks", []) if w]
    return [w[0] for w in walks if w]


def walk_nodes(pnum, problems):
    p = problems.get(str(pnum), {})
    out = set(p.get("moves", []))
    for w in p.get("alt_walks", []):
        out.update(w)
    return out


def score(named, pnum, problems):
    """Deterministic verdicts for one spot rep. `named` is the list of node
    ids the answer named (empty for "direct" or "don't know").

    Every named move that some walk of the problem uses is a hit: an
    answer that works the example through to a convincing solve has read
    the whole route, not only its first move (2026-09-01). The primary
    entry is recorded as missed only when no entry move was named at all.
    `false` is every named move no walk of the problem uses:
    over-triggering, the failure in the other direction."""
    entries = entry_nodes(pnum, problems)
    if not entries:
        return {}, sorted(set(named))
    walk = walk_nodes(pnum, problems)
    moves = {n: HIT for n in dict.fromkeys(named) if n in walk}
    if not any(e in named for e in entries):
        moves[entries[0]] = MISSED
    false = sorted(set(named) - walk)
    return moves, false


# ---- derived status --------------------------------------------------------

class _Index:
    def __init__(self, recog):
        self.by_node = {}     # node -> [(date, verdict, key)]
        self.by_problem = {}  # problem -> [(date, key, rec)]
        self.spots = []       # [(date, key, rec)] of spot reps
        self._n = len(recog)
        for key, rec in recog.items():
            d = date.fromisoformat(rec["date"])
            for node, v in rec.get("moves", {}).items():
                self.by_node.setdefault(node, []).append((d, v, key))
            pnum = rec.get("problem")
            if pnum is not None:
                self.by_problem.setdefault(str(pnum), []).append((d, key, rec))
            if rec.get("kind") == "spot":
                self.spots.append((d, key, rec))
        for v in self.by_node.values():
            v.sort()
        for v in self.by_problem.values():
            v.sort(key=lambda t: t[0])
        self.spots.sort(key=lambda t: t[0])


_INDEX = {}


def index(recog):
    idx = _INDEX.get(id(recog))
    if idx is None or idx._n != len(recog):
        idx = _Index(recog)
        _INDEX.clear()
        _INDEX[id(recog)] = idx
    return idx


def recognition_window(hits):
    return SOLID_WINDOW_DAYS * (1.3 ** max(hits - 1, 0))


def recognition_status(node_id, recog, today=None):
    """(status, last_event_date) for a node's recognition axis."""
    today = today or date.today()
    events = index(recog).by_node.get(node_id, ())
    if not events:
        return UNTESTED, None
    last_date, last_verdict, _ = events[-1]
    if last_verdict == MISSED:
        return FAILED_TO_RECOGNIZE, last_date
    hits = sum(1 for _, v, _ in events if v == HIT)
    if (today - last_date).days <= recognition_window(hits):
        return RECOGNIZED, last_date
    return UNTESTED, last_date


def spotted_problems(recog):
    """Problems that have had a spot rep: the statement has been seen with
    its walk revealed, so it is never served for recognition again."""
    return {p for p, evs in index(recog).by_problem.items()
            if any(r.get("kind") == "spot" for _, _, r in evs)}


def spotted_before(pnum, day, recog):
    """(date, verdict) of the latest spot rep on this problem strictly
    before `day`, or None. A solve after a MISSED rep is not unaided: the
    reveal handed over the walk (kg_extract floors its assist to hint). A
    solve after a HIT is: the reveal showed nothing the candidate had not
    produced, and both records stay side by side for the data."""
    day = date.fromisoformat(day) if isinstance(day, str) else day
    reps = [(d, r) for d, _, r in index(recog).by_problem.get(str(pnum), ())
            if r.get("kind") == "spot" and d < day]
    if not reps:
        return None
    d, r = max(reps, key=lambda t: t[0])
    verdict = HIT if any(v == HIT for v in r.get("moves", {}).values()) else MISSED
    return d, verdict


def spots_today(recog, today=None):
    today = today or date.today()
    return sum(1 for d, _, _ in index(recog).spots if d == today)


def solves_today(evidence, today=None):
    today = (today or date.today()).isoformat()
    return len(ev_index(evidence).by_date.get(today, ()))


def spot_due_by_ratio(recog, evidence, today=None, every=None):
    """True while today's spot reps are behind the ratio: fewer than
    1 + solves_today // every. With every=3: one before the first solve,
    another after the third, the sixth, ..."""
    every = SPOT_EVERY if every is None else every
    if every <= 0:
        return False
    return spots_today(recog, today) <= solves_today(evidence, today) // every


# ---- the pick --------------------------------------------------------------

def drafted_carriers(problems, predicted=None):
    """graph/predicted.json problems not in problems.json, as in-memory
    entries the way kg_next promotes a draft: one drafted walk, no missing
    move, difficulty from the metadata. The bank of mapped unsolved
    problems is ~30 and mostly Hards; the drafts are ~2300. A drafted
    walk is only a guess about the entry move, so the judge re-derives the
    walk (map_problem) before scoring, and the map is what is stored."""
    predicted = load_predicted() if predicted is None else predicted
    out = {}
    for pnum, v in predicted.items():
        if pnum in problems:
            continue
        walks = v.get("walks", [])
        if len(walks) != 1 or walks[0].get("missing") or not walks[0].get("moves"):
            continue
        out[pnum] = {"title": v.get("title", ""),
                     "difficulty": problem_difficulty(pnum, problems),
                     "moves": list(walks[0]["moves"]), "drafted": True}
    return out


def spot_carriers(target, problems, evidence, recog, nodes, statuses=None,
                  skip=(), predicted=None):
    """Unsolved, unspotted, unbanned problems whose entry moves include
    target: reachable ones (every move of the walk SOLID) before the rest,
    mapped before drafted (a mapped walk is evidence, a draft a guess),
    gentlest first within each. Hards are allowed: a Hard statement is
    where the trigger fails in practice, and reading it is not climbing it."""
    solved = solved_problems(evidence)
    seen = spotted_problems(recog)
    statuses = statuses or {}
    pool = dict(drafted_carriers(problems, predicted))
    pool.update(problems)
    out = []
    for pnum, p in pool.items():
        if (pnum in solved or pnum in seen or pnum in skip or p.get("banned")
                or not p.get("moves") or not all(m in nodes for m in p["moves"])):
            continue
        if target in entry_nodes(pnum, pool):
            out.append(pnum)

    def reachable(q):
        return all(statuses.get(m, (None,))[0] == SOLID for m in pool[q]["moves"])

    out.sort(key=lambda q: (not reachable(q), pool[q].get("drafted", False),
                            gentleness(q, pool, nodes), pnum_key(q)))
    return out


def reach_through(nodes, problems, evidence, recog, statuses, skip=(), predicted=None):
    """{node: [reachable carriers]} - for each node, the unsolved problems
    whose walk is all SOLID and enters through it. This is the reach a
    node carries today; whether the statement triggers the node is what
    decides if that reach is real."""
    solved = solved_problems(evidence)
    seen = spotted_problems(recog)
    pool = dict(drafted_carriers(problems, predicted))
    pool.update(problems)
    reach = {}
    for pnum, p in pool.items():
        moves = p.get("moves", [])
        if (pnum in solved or pnum in seen or pnum in skip or p.get("banned")
                or not moves or not all(m in nodes for m in moves)
                or any(statuses.get(m, (None,))[0] != SOLID for m in moves)):
            continue
        for e in dict.fromkeys(entry_nodes(pnum, pool)):
            reach.setdefault(e, []).append(pnum)
    for e in reach:
        reach[e].sort(key=lambda q: (pool[q].get("drafted", False),
                                     gentleness(q, pool, nodes), pnum_key(q)))
    return reach


def due_spot(nodes, problems, evidence, recog, statuses, today=None, skip=(),
             predicted=None, every=None, force=False):
    """The spot rep due today, or None: (target, pnum, reason).

    One rule, at the SPOT_EVERY ratio. Recognition is the check on reach: the graph
    says these problems are reachable because every move in their walk is
    SOLID; the spot rep asks whether the statement actually triggers the
    move they enter through. So the node served is the one carrying the
    most reach whose trigger has not been shown recently (not RECOGNIZED
    inside the window). A FAILED_TO_RECOGNIZE node ranks by the same
    number; ties go to it, then to the older event. The carrier is the
    gentlest problem it reaches. `force` (make prepare spot) skips the
    ratio: asking for a rep is always answered while a node has reach."""
    today = today or date.today()
    if not force and not spot_due_by_ratio(recog, evidence, today, every):
        return None
    reach = reach_through(nodes, problems, evidence, recog, statuses, skip, predicted)
    ranked = []
    for n, carriers in reach.items():
        status, last = recognition_status(n, recog, today)
        if status == RECOGNIZED:
            continue
        ranked.append((-len(carriers), status != FAILED_TO_RECOGNIZE,
                       last or date.min, n))
    if not ranked:
        return None
    _, _, _, n = min(ranked)
    status = recognition_status(n, recog, today)[0]
    why = "failed to recognize last time" if status == FAILED_TO_RECOGNIZE else "untested"
    return n, reach[n][0], f"{why}, {len(reach[n])} reachable through it"


# ---- the statement ---------------------------------------------------------

class _MD(HTMLParser):
    """LeetCode's statement HTML as markdown: emphasis, code, lists, images,
    superscripts and example blocks kept; everything else is text."""

    BLOCK = {"p", "div", "ul", "ol", "pre", "table", "tr", "h1", "h2", "h3", "blockquote"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.pending = []
        self.pre = 0
        self.list_stack = []
        self.cell = None
        self.row = None
        self.table = None

    def emit(self, s):
        if self.cell is not None:
            self.cell.append(s)
        else:
            self.out.append(s)

    def sink(self):
        return self.cell if self.cell is not None else self.out

    def open_mark(self, mark):
        """An inline marker (** * `) is held until the next text, so that
        <strong> a</strong> becomes " **a**": whitespace inside the
        markers is what breaks markdown emphasis."""
        if self.pre:
            return
        self.pending.append(mark)

    def close_mark(self, mark):
        if self.pre:
            return
        if self.pending and self.pending[-1] == mark:
            self.pending.pop()  # empty element: nothing to mark
            return
        sink = self.sink()
        if sink and sink[-1].strip() and sink[-1] != sink[-1].rstrip():
            body = sink[-1].rstrip()
            tail = sink[-1][len(body):]
            sink[-1] = body
            sink.append(mark + tail)
        else:
            sink.append(mark)

    def handle_data(self, data):
        if self.pre:
            self.emit(data)
            return
        data = re.sub(r"[ \t\r\n]+", " ", data)
        if self.pending and data.strip():
            lead = data[: len(data) - len(data.lstrip())]
            sink = self.sink()
            if sink and sink[-1][-1:].isspace():
                lead = ""  # the text before the marker already ends in one
            self.emit(lead + "".join(self.pending))
            self.pending = []
            data = data.lstrip()
        self.emit(data)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "pre":
            self.pre += 1
            self.emit("\n```\n")
        elif tag in ("strong", "b"):
            self.open_mark("**")
        elif tag in ("em", "i"):
            self.open_mark("*")
        elif tag == "code":
            self.open_mark("`")
        elif tag == "sup":
            self.emit("^")
        elif tag == "br":
            self.emit("\n")
        elif tag == "img":
            self.emit(f"\n![{a.get('alt', '')}]({a.get('src', '')})\n")
        elif tag in ("ul", "ol"):
            if not self.list_stack:
                self.emit("\n")
            self.list_stack.append(0)
        elif tag == "li":
            depth = len(self.list_stack)
            if self.list_stack:
                self.list_stack[-1] += 1
            self.emit("\n" + "  " * (depth - 1) + "- ")
        elif tag == "table":
            self.table = []
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []
        elif tag in self.BLOCK:
            self.emit("\n")

    def handle_endtag(self, tag):
        if tag == "pre":
            self.pre -= 1
            self.emit("\n```\n")
        elif tag in ("strong", "b"):
            self.close_mark("**")
        elif tag in ("em", "i"):
            self.close_mark("*")
        elif tag == "code":
            self.close_mark("`")
        elif tag in ("ul", "ol"):
            self.list_stack.pop()
            if not self.list_stack:
                self.emit("\n")
        elif tag in ("td", "th"):
            cell = "".join(self.cell).strip().replace("\n", " ")
            self.cell = None
            if self.row is not None:
                self.row.append(cell)
        elif tag == "tr":
            if self.table is not None and self.row is not None:
                self.table.append(self.row)
            self.row = None
        elif tag == "table":
            rows = self.table or []
            self.table = None
            if rows:
                width = max(len(r) for r in rows)
                rows = [r + [""] * (width - len(r)) for r in rows]
                lines = ["| " + " | ".join(rows[0]) + " |",
                         "|" + "---|" * width]
                lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
                self.out.append("\n" + "\n".join(lines) + "\n")
        elif tag in ("p", "div", "h1", "h2", "h3", "blockquote"):
            self.emit("\n")

    def text(self):
        s = "".join(self.out)
        s = s.replace("\xa0", " ")
        s = re.sub(r"[ \t]+\n", "\n", s)
        s = re.sub(r"\n (?=\S)", "\n", s)  # one stray space, never list indentation
        s = re.sub(r"```\n\n+", "```\n", s)
        s = re.sub(r"\n\n+```", "\n```", s)
        s = re.sub(r"\n{3,}", "\n\n", s)
        return s.strip() + "\n"


def html_to_markdown(html):
    p = _MD()
    p.feed(html or "")
    p.close()
    return p.text()


def content_cache_path(num):
    return os.path.join(CACHE_DIR, f"{num}.content.json")


def fetch_content(num):
    """LeetCode's statement HTML for a problem, with title, slug and
    difficulty; cached in .prepare_cache/<num>.content.json."""
    try:
        with open(content_cache_path(num)) as f:
            return json.load(f)
    except (OSError, ValueError):
        pass
    import requests
    url = "https://leetcode.com/graphql/"
    headers = {"Content-Type": "application/json"}
    q1 = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
      problemsetQuestionList: questionList(categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters) {
        questions: data { difficulty frontendQuestionId: questionFrontendId paidOnly: isPaidOnly title titleSlug }
      }
    }"""
    r = requests.post(url, headers=headers, json={
        "query": q1,
        "variables": {"categorySlug": "", "limit": 1, "skip": int(num) - 1, "filters": {}}},
        timeout=60)
    r.raise_for_status()
    qs = r.json()["data"]["problemsetQuestionList"]["questions"]
    if not qs or qs[0]["frontendQuestionId"] != str(num):
        raise ValueError(f"no question found for number {num}")
    q = qs[0]
    if q["paidOnly"]:
        raise ValueError(f"question {num} is paid only")
    q2 = """
    query questionDetails($titleSlug: String!) {
      question(titleSlug: $titleSlug) { content }
    }"""
    r = requests.post(url, headers=headers,
                      json={"query": q2, "variables": {"titleSlug": q["titleSlug"]}},
                      timeout=60)
    r.raise_for_status()
    content = r.json()["data"]["question"]["content"]
    entry = {"title": q["title"], "slug": q["titleSlug"],
             "difficulty": q["difficulty"], "content": content}
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(content_cache_path(num), "w") as f:
        json.dump(entry, f)
    return entry


def spot_document(markdown_statement):
    """current.md for a spot rep: the statement, then the answer section."""
    return (
        f"{markdown_statement.rstrip()}\n\n"
        f"{ANSWER_MARK}\n---\n\n"
    )


def split_answer(text):
    """(statement, answer) from a spot file; the footer comment, if any,
    is not part of the answer."""
    text = FOOTER_RE.sub("", text)
    if ANSWER_MARK in text:
        head, tail = text.split(ANSWER_MARK, 1)
        tail = re.sub(r"^\s*---\s*", "", tail, count=1)
        return head.strip(), tail.strip()
    return text.strip(), ""


def read_footer(text):
    m = FOOTER_RE.search(text)
    if not m:
        return {}
    try:
        return json.loads(m.group(1))
    except ValueError:
        return {}


# ---- the judge -------------------------------------------------------------

def judge_answer(statement, answer, nodes, model="haiku"):
    """One small claude call: the moves the candidate's free-text answer
    names or describes, as taxonomy ids. "direct" / "don't know" map to
    none. Returns (named, summary)."""
    system = f"""A candidate read a LeetCode problem statement (title hidden) and wrote, in free text, which technique they would reach for. You map that answer onto a fixed taxonomy.

Taxonomy (use ONLY these ids):
{taxonomy_summary(nodes)}

Rules:
- "named" lists every taxonomy move the answer names or unmistakably describes ("binary search over the answer with a feasibility check" names binary-search-on-answer). Do not add moves the answer only implies, and never add the move YOU think solves the problem: you are reading the candidate, not solving.
- An answer of "direct", "just simulate", "no technique", "don't know", or similar names nothing: "named": [].
- "summary": one or two plain sentences saying what the answer reached for, in the candidate's terms. Facts only, no grading.

Output STRICT JSON only: {{"named": ["<node-id>"], "summary": "<sentence>"}}"""
    prompt = f"STATEMENT:\n{statement[:5000]}\n\nCANDIDATE'S ANSWER:\n{answer[:2000] or '(empty)'}"
    result = claude_json(prompt, system, model=model)
    named = [n for n in result.get("named", []) if n in nodes]
    return named, str(result.get("summary", "")).strip()


def judge_alternative(statement, answer, named, nodes, model="sonnet"):
    """The candidate named moves no mapped walk of the problem uses. One
    call on the stronger model answers a narrow question: is the approach
    the answer describes a standard, accepted, correct solution to this
    statement (the kind an editorial lists), not merely a plausible idea?
    Returns (valid, why). No code runs: a hit through here is marked as
    an alternative walk not yet evidenced by code, and stays marked."""
    system = """You judge whether a candidate's proposed approach to a LeetCode problem (title hidden) is a correct solution.

Rules:
- "valid" is true ONLY when the approach, as the candidate describes it, is a standard accepted solution to this exact problem: correct on every input within the constraints and within the intended complexity, the kind of solution an editorial or a top community writeup lists. A plausible idea that would need repair, a heuristic, an approach that fails an edge case, or one that exceeds the constraints is false.
- Judge what the candidate wrote, not the solution you would write. If the description is too vague to be sure it is correct, "valid" is false.
- "why": one sentence naming the accepted solution it matches, or the input or constraint it fails on.

Output STRICT JSON only: {"valid": true|false, "why": "<sentence>"}"""
    prompt = (f"STATEMENT:\n{statement[:5000]}\n\nCANDIDATE'S ANSWER:\n{answer[:2000]}"
              f"\n\nThe answer was read as these moves: {', '.join(named)}.")
    result = claude_json(prompt, system, model=model)
    return bool(result.get("valid")), str(result.get("why", "")).strip()


def apply_alternative(rec, named, problems, why):
    """A valid alternative walk: the rep becomes a hit on the first move
    the candidate named, marked "alternative" (recognition only, no code
    ran), and the walk is filed on the problem under `spotted_walks`,
    never `alt_walks`, which stays evidenced by code. A later solve that
    takes this walk promotes it (kg_extract.record_alt_walk)."""
    rec["moves"] = {named[0]: HIT}
    rec["false"] = []
    rec["alternative"] = list(named)
    rec["why"] = why
    entry = problems.setdefault(str(rec["problem"]), {})
    walks = entry.setdefault("spotted_walks", [])
    if list(named) not in walks:
        walks.append(list(named))
    return rec


MAP_SYSTEM = """You are mapping a LeetCode problem onto a fixed taxonomy of atomic technique moves.

Taxonomy (use ONLY these ids):
{taxonomy}

Determine the canonical clean solution for the problem, then output STRICT JSON, nothing else:
{{"title": "<full problem title>", "difficulty": "Easy|Medium|Hard", "moves": ["<node-id>", ...], "unmapped": ["<short description of any required move with no matching node>"]}}

List the moves in the order a candidate meets them: the move the statement triggers FIRST comes first. Include foundational micro-moves after it. Do not explain the solution."""


def map_problem(pnum, title, nodes, problems, model="sonnet"):
    """The preflight mapping call for a problem not in problems.json (or
    with a withdrawn walk); the walk is what a spot rep is scored against.
    Writes the entry into `problems` (caller saves)."""
    result = claude_json(f"LeetCode problem: {pnum}. {title}",
                         MAP_SYSTEM.format(taxonomy=taxonomy_summary(nodes)),
                         model=model)
    moves = [m for m in result.get("moves", []) if m in nodes]
    entry = problems.setdefault(str(pnum), {})
    entry.update({"title": result.get("title", title),
                  "difficulty": result.get("difficulty", ""),
                  "moves": moves, "source": "spot"})
    if result.get("unmapped"):
        entry["unmapped"] = result["unmapped"]
    return moves


# ---- solves: a miss written in the notes -----------------------------------

_MISS_WORDS = re.compile(
    r"recognition failure|(?:fail|did ?n[o']?t|never|could ?n[o']?t|missed|not)"
    r"[^.\n]{0,40}\brecogni[sz]", re.I)


def notes_say_missed(notes):
    """True when the candidate's own notes say a move was not recognised.
    The word in plain prose is the mark; nothing else is typed."""
    return bool(_MISS_WORDS.search(notes or ""))


def pending_spots(recog):
    """recognition/*.md files with no record yet, oldest first."""
    files = sorted(glob.glob(os.path.join(RECOGNITION_DIR, "*.md")),
                   key=os.path.getmtime)
    rel = [os.path.relpath(f, REPO_ROOT) for f in files]
    return [f for f in rel if f not in recog]


# ---- the reveal ------------------------------------------------------------

def reveal(rec):
    """The lines `make solved` prints after a spot rep is judged: the
    problem, the walk, the verdict, and what the answer reached for. The
    only time the title is shown."""
    title = rec.get("title", "")
    pnum = rec.get("problem", "?")
    walk = ", ".join(rec.get("walk", [])) or "(unmapped)"
    verdict = "missed" if MISSED in rec.get("moves", {}).values() else "hit"
    lines = [f"{pnum}. {title}", f"walk: {walk}", f"{verdict} in {rec.get('seconds', 0)}s"]
    if rec.get("alternative"):
        lines.append("hit through an alternative walk, not yet evidenced by code: "
                     + ", ".join(rec["alternative"]))
        if rec.get("why"):
            lines.append(rec["why"])
    if rec.get("named"):
        lines.append(f"named: {', '.join(rec['named'])}")
    if rec.get("false"):
        lines.append(f"named but not in any walk: {', '.join(rec['false'])}")
    if rec.get("summary"):
        lines.append(rec["summary"])
    if rec.get("reason"):
        lines.append(f"served: {rec['reason']}")
    return "\n".join(lines)
