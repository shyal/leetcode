"""mu ide: hover, completion, go-to-definition and signature help for VS Code.

    python mu/ide.py    serve: one JSON request per line on stdin,
                        one JSON reply per line on stdout

A request is {"id", "cmd", "root", "text", "line", "col"}; line and col are
0-based, as in VS Code. cmd is hover, complete, definition or signature. The
reply is {"id", "result"}.

The file is transpiled with its line map (transpile(mapped=True)) and Jedi
answers on the Python. A mu line that does not parse is blanked and the rest
is transpiled again, so a half-typed line costs only itself. For completion
the cursor line is replaced by the name chain before the cursor, `q.pu`,
which always transpiles; for signature help, by the call up to its last
comma, closed. Positions go through the map both ways: the k-th occurrence
of a word on a mu line is taken to be the k-th on the Python lines it made.
"""

import ast
import json
import re
import sys
from functools import cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from session import mu_type  # noqa: E402

from mu import VERSION, MuError, transpile  # noqa: E402

HERE = Path(__file__).parent
ROOT = HERE.parent
SPEC = HERE / "spec" / f"v{VERSION}.md"
HARNESS = ROOT / "utils" / "harness"
BUFFER = ".mu_ide.py"  # the name Jedi sees for the transpiled text
WORD = re.compile(r"[A-Za-z_]\w*")
# the name chain before the cursor: `q.pu`, `q.`, `nu`, or nothing
CHAIN = re.compile(r"(?:[A-Za-z_]\w*\.)*(?:[A-Za-z_]\w*)?$")
LINE_ERR = re.compile(r"^line (\d+):")
DEFINED = re.compile(r"^(?:def|class) ([A-Za-z_]\w*)", flags=re.M)
KEYWORDS = sorted(
    {"def", "memo", "for", "in", "if", "elif", "else", "while", "return", "ret"}
    | {"break", "continue", "pass", "del", "assert", "yield", "from", "import"}
    | {"extends", "and", "or", "not", "is", "true", "false", "none", "inf"}
    | {"first", "sum", "max", "min", "count", "lambda"}
)
TRIES = 200


def helper_docs():
    """The Helpers block of the spec: name -> its lines, `call  # what it is`."""
    text = SPEC.read_text()
    block = text.split("## Helpers", 1)[1].split("```python", 1)[1].split("```", 1)[0]
    docs = {}
    for line in block.strip().splitlines():
        m = WORD.search(line)
        if m:
            docs.setdefault(m.group(), []).append(line)
    return docs


@cache
def spec_lines():
    """name -> the 0-based line of the spec where the helper is first listed."""
    lines = SPEC.read_text().splitlines()
    start = next(k for k, ln in enumerate(lines) if ln.startswith("## Helpers"))
    at = {}
    for k in range(start, len(lines)):
        m = WORD.search(lines[k])
        if m and m.group() in HELPERS and m.group() not in at:
            at[m.group()] = k
    return at


HELPERS = helper_docs()


@cache
def harness_defs():
    """name -> (path, 0-based line) of every def and class in utils/harness."""
    out = {}
    for path in sorted(HARNESS.glob("*.py")):
        text = path.read_text()
        for m in DEFINED.finditer(text):
            out.setdefault(m.group(1), (str(path), text[: m.start()].count("\n")))
    return out


def depth_after(text, depth):
    """The bracket depth after this line; strings and the comment are skipped."""
    k = 0
    while k < len(text):
        ch = text[k]
        if ch == "#":
            break
        if ch in "\"'":
            end = text.find(ch, k + 1)
            k = len(text) if end < 0 else end + 1
            continue
        depth += (ch in "([{") - (ch in ")]}")
        k += 1
    return depth


def unclosed(lines):
    """The lines with every logical line whose brackets do not close blanked:
    one still open when a line no deeper than its first line arrives, or at
    the end, and one that closes more than it opens. Returns the blanked
    line numbers too."""
    lines = list(lines)
    blanked = set()
    depth, start, start_ind = 0, 0, 0
    for k, text in enumerate(lines + [""]):
        if not text.strip() and k < len(lines):
            continue
        ind = len(text) - len(text.lstrip())
        if depth and (ind <= start_ind or k == len(lines)):
            blanked |= set(range(start, k))
            depth = 0
        if depth == 0:
            start, start_ind = k, ind
        depth = depth_after(text, depth)
        if depth < 0:
            blanked |= set(range(start, k + 1))
            depth = 0
    for k in blanked:
        lines[k] = ""
    return lines, blanked


def repaired(lines):
    """Transpile the lines, blanking any line that fails until it parses:
    (code, origin, blanked). When a line the parser names is blank already,
    the nearest line above it goes; an error with no line starts from the
    end. None when nothing parses."""
    lines, blanked = unclosed(lines)
    for _ in range(TRIES):
        try:
            code, origin = transpile("\n".join(lines) + "\n", mapped=True)
            return code, origin, blanked
        except MuError as err:
            m = LINE_ERR.match(str(err))
            k = (int(m.group(1)) if m else len(lines)) - 1
            if not 0 <= k < len(lines):
                k = len(lines) - 1
            while k >= 0 and (k in blanked or not lines[k].strip()):
                k -= 1
            if k < 0:
                return None
            lines[k] = ""
            blanked.add(k)
    return None


def word_at(text, col):
    """(word, start, end) of the name under col, or None."""
    for m in WORD.finditer(text):
        if m.start() <= col <= m.end():
            return m.group(), m.start(), m.end()
    return None


def occurrence(text, word, col):
    """Which occurrence of word, counting from 0, holds col."""
    return sum(1 for m in re.finditer(rf"\b{word}\b", text) if m.end() < col)


def py_lines(origin, line):
    """The 1-based Python lines a 0-based mu line made."""
    return [k + 1 for k, o in enumerate(origin) if o == line + 1]


def nth(code, rows, word, k):
    """(1-based line, column after the word) of the k-th occurrence of word
    on these Python rows, the last one when there are fewer; None if none."""
    hits = []
    text = code.splitlines()
    for row in rows:
        for m in re.finditer(rf"\b{word}\b", text[row - 1]):
            hits.append((row, m.end()))
    if not hits:
        return None
    return hits[min(k, len(hits) - 1)]


def script(code, root):
    import jedi

    paths = [root, f"{root}/utils", f"{root}/utils/harness"]
    project = jedi.Project(root, added_sys_path=paths)
    return jedi.Script(code=code, path=f"{root}/{BUFFER}", project=project)


class File:
    """One request's view of the file: its lines, the Python, and the map."""

    def __init__(self, req):
        self.root = req.get("root") or str(ROOT)
        self.lines = req["text"].split("\n")
        self.line, self.col = req["line"], req["col"]
        self.text = self.lines[self.line] if self.line < len(self.lines) else ""
        self.code = self.origin = None
        self.blanked = set()

    def build(self, lines=None):
        """Transpile (a variant of) the lines; True when something parsed."""
        got = repaired(self.lines if lines is None else lines)
        if got is None:
            return False
        self.code, self.origin, self.blanked = got
        return True

    def rows(self, line=None):
        return py_lines(self.origin, self.line if line is None else line)

    def at(self):
        """The Python (line, col) of the word under the cursor, and the word."""
        w = word_at(self.text, self.col)
        if not w or self.line in self.blanked:
            return None
        word, start, _ = w
        pos = nth(self.code, self.rows(), word, occurrence(self.text, word, start + 1))
        return (pos, word) if pos else None

    def back(self, name):
        """A Jedi name in the buffer as (path, 0-based line, col) in the mu
        file, or in the harness or the spec for a pasted helper."""
        mu = self.origin[name.line - 1]
        if mu is None:
            return helper_location(name.name)
        line = mu - 1
        m = re.search(rf"\b{name.name}\b", self.lines[line])
        return (None, line, m.start() if m else 0)

    def head(self, name):
        """The mu def or memo line a buffer function is bound on, as markdown."""
        if name.type != "function" or name.module_path is None:
            return None
        if name.module_path.name != BUFFER:
            return None
        mu = self.origin[name.line - 1]
        if mu is None:
            return None
        text = self.lines[mu - 1].strip()
        if text.split(" ")[0] in ("def", "memo"):
            return f"```mu\n{text}\n```"
        return None

    def is_helper(self, name):
        return (
            name.module_path is not None
            and name.module_path.name == BUFFER
            and self.origin[name.line - 1] is None
            and name.name in HELPERS
        )


def helper_location(name):
    """Where a helper is defined: its harness source, else its spec line."""
    if name in harness_defs():
        path, line = harness_defs()[name]
        return (path, line, 0)
    if name in spec_lines():
        return (str(SPEC), spec_lines()[name], 0)
    return None


def hint(name):
    """The type of a Jedi name, written as a mu type."""
    try:
        h = name.get_type_hint()
    except Exception:
        return None
    if not h:
        return None
    try:
        return mu_type(ast.parse(h, mode="eval").body)
    except SyntaxError:
        return h


def describe(f, name, word):
    """Markdown for one Jedi name: a helper's spec lines, a def's own mu
    line, or `word: type`."""
    if f.is_helper(name) or (name.module_path is None and word in HELPERS):
        return "```mu\n" + "\n".join(HELPERS[word]) + "\n```"
    if name.type in ("function", "class", "module"):
        head = name.docstring().split("\n", 1)[0]
        if name.module_path and name.module_path.name == BUFFER:
            mu = f.origin[name.line - 1]
            if mu is not None:
                head = f.lines[mu - 1].strip()
        doc = name.docstring(raw=True).strip()
        return f"```mu\n{head}\n```" + (f"\n\n{doc}" if doc else "")
    t = hint(name)
    return f"```mu\n{word}: {t}\n```" if t else None


def hover(req):
    f = File(req)
    w = word_at(f.text, f.col)
    if not w:
        return None
    if not f.build() or f.at() is None:
        return spec_hover(w[0])
    (line, col), word = f.at()
    s = script(f.code, f.root)
    parts = []
    for n in s.goto(line, col):  # a def or memo of the file: its own line
        h = f.head(n)
        if h and h not in parts:
            parts.append(h)
    for n in [] if parts else s.infer(line, col) or s.goto(line, col):
        d = describe(f, n, word)
        if d and d not in parts:
            parts.append(d)
    if not parts:
        return spec_hover(word)
    return {"contents": "\n\n".join(parts)}


def spec_hover(word):
    if word not in HELPERS:
        return None
    return {"contents": "```mu\n" + "\n".join(HELPERS[word]) + "\n```"}


def definition(req):
    f = File(req)
    if not f.build() or f.at() is None:
        w = word_at(f.text, f.col)
        loc = helper_location(w[0]) if w else None
        return [{"path": loc[0], "line": loc[1], "col": loc[2]}] if loc else []
    (line, col), _ = f.at()
    out = []
    for n in script(f.code, f.root).goto(line, col, follow_imports=True):
        if n.module_path is None:
            continue
        if n.module_path.name == BUFFER:
            loc = f.back(n)
        else:
            loc = (str(n.module_path), n.line - 1, n.column)
        if loc and loc not in out:
            out.append(loc)
    return [{"path": p, "line": ln, "col": c} for p, ln, c in out]


KINDS = {
    "module": "module",
    "class": "class",
    "instance": "variable",
    "function": "function",
    "param": "variable",
    "statement": "variable",
    "property": "property",
}


def complete(req):
    f = File(req)
    before = f.text[: f.col]
    indent = before[: len(before) - len(before.lstrip())]
    chain = CHAIN.search(before).group()
    dotted = "." in chain
    prefix = chain.rsplit(".", 1)[-1]
    probe = list(f.lines)
    probe[f.line] = indent + (chain or "x")
    items = []
    if f.build(probe) and f.line not in f.blanked:
        rows = f.rows()
        text = f.code.splitlines()
        hit = [(r, text[r - 1].find(chain or "x")) for r in rows]
        hit = [(r, c) for r, c in hit if c >= 0]
        if hit:
            row, c = hit[0]
            col = c + len(chain)
            for n in script(f.code, f.root).complete(row, col):
                if n.type == "keyword" or n.name.startswith("__") or n.name == "self":
                    continue
                items.append({"label": n.name, "kind": KINDS.get(n.type, "variable")})
    if dotted:
        return items
    seen = {i["label"] for i in items}
    for name in KEYWORDS:
        if name.startswith(prefix) and name not in seen:
            items.append({"label": name, "kind": "keyword"})
    for name, lines in HELPERS.items():
        if name.startswith(prefix) and name not in seen:
            items.append(
                {
                    "label": name,
                    "kind": "function",
                    "detail": lines[0],
                    "doc": "\n".join(lines),
                }
            )
    return items


def call_site(before):
    """The innermost open call in the text before the cursor: (callee,
    argument index, the text up to its last top-level comma, closed), or
    None outside any call."""
    opens = []  # index of each unclosed bracket
    commas = {}  # open index -> indexes of the commas directly inside it
    for k, ch in enumerate(before):
        if ch in "([{":
            opens.append(k)
            commas[k] = []
        elif ch in ")]}":
            if opens:
                commas.pop(opens.pop())
        elif ch == "," and opens:
            commas[opens[-1]].append(k)
    close = {"(": ")", "[": "]", "{": "}"}
    for k in reversed(opens):
        m = re.search(r"([A-Za-z_]\w*)\s*$", before[:k])
        if before[k] != "(" or not m:
            continue
        cut = commas[k][-1] + 1 if commas[k] else k + 1
        closers = "".join(close[before[o]] for o in reversed(opens))
        return m.group(1), len(commas[k]), before[:cut] + closers
    return None


def signature(req):
    f = File(req)
    site = call_site(f.text[: f.col])
    if not site:
        return None
    callee, index, line = site
    probe = list(f.lines)
    probe[f.line] = line
    sigs = []
    if f.build(probe) and f.line not in f.blanked:
        text = f.code.splitlines()
        for row in f.rows():
            m = re.search(rf"\b{callee}\(", text[row - 1])
            if m:
                sigs = script(f.code, f.root).get_signatures(row, m.end())
                break
    doc = "\n".join(HELPERS.get(callee, []))
    if not sigs:
        if not doc:
            return None
        return {
            "label": HELPERS[callee][0].split("#")[0].strip(),
            "params": [],
            "active": index,
            "doc": doc,
        }
    s = sigs[0]
    params = [p.to_string() for p in s.params]
    label = f"{s.name}({', '.join(params)})"
    return {
        "label": label,
        "params": params,
        "active": index,
        "doc": doc or s.docstring(raw=True).strip(),
    }


COMMANDS = {
    "hover": hover,
    "complete": complete,
    "definition": definition,
    "signature": signature,
}


def answer(req):
    try:
        return {"id": req.get("id"), "result": COMMANDS[req["cmd"]](req)}
    except Exception as err:  # a bad request must not end the server
        return {"id": req.get("id"), "error": f"{type(err).__name__}: {err}"}


def serve(stdin=sys.stdin, stdout=sys.stdout):
    for line in stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        stdout.write(json.dumps(answer(req)) + "\n")
        stdout.flush()


if __name__ == "__main__":
    try:
        import jedi  # noqa: F401
    except ImportError:
        sys.exit(
            "mu ide: jedi is not installed; run .venv/bin/pip install -r requirements.txt"
        )
    serve()
