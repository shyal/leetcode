import re
import sqlite3


def locate_error(con, sql: str, err: str):
    """Character offset of the token sqlite choked on, or None.

    sqlite (3.43, python 3.10) only says `near "as"` and the token can occur
    several times. Prepare each prefix ending at a candidate occurrence: a
    prefix that is fine so far fails with "incomplete input" (or runs), the
    first one that reproduces a syntax error ends at the culprit."""
    m = re.search(r'near "(.+?)"', err)
    if not m:
        return None
    tok = m.group(1)
    pat = re.compile(re.escape(tok) + (r"\b" if tok[-1].isalnum() else ""), re.I)
    for hit in pat.finditer(sql):
        try:
            con.execute(sql[: hit.end()])
        except sqlite3.OperationalError as e:
            if "incomplete input" not in str(e):
                return hit.start()
        except sqlite3.Error:
            return hit.start()
    return None


def show_error(sql: str, err: str, at) -> None:
    """The query with the failing line marked and a caret under the token."""
    print(f"\nsqlite: {err}\n")
    lines = sql.split("\n")
    seen = 0
    for i, line in enumerate(lines, 1):
        hit = at is not None and seen <= at < seen + len(line) + 1
        print(f"{'>' if hit else ' '} {i:2} | {line}")
        if hit:
            print(f"     | {' ' * (at - seen)}^")
        seen += len(line) + 1
    print()


def null_safe(row):
    """Sort key that never compares NULL with a value."""
    return [(v is None, v) for v in row]


class SQLDrill:
    """Base for SQL drills: subclass, write `query()`, done.

        sol.run(schema)                -> row tuples, sorted (row order is
                                          not part of the drill)
        sol.run(schema, ordered=True)  -> row tuples in engine order, for a
                                          drill where ORDER BY is the move
        sol.show(schema)               -> prints the result as a +---+ table
    """

    def query(self) -> str:
        raise NotImplementedError

    def _execute(self, schema: str):
        con = sqlite3.connect(":memory:")
        con.executescript(schema)
        sql = self.query()
        try:
            cur = con.execute(sql)
        except sqlite3.OperationalError as e:
            show_error(sql, str(e), locate_error(con, sql, str(e)))
            raise
        if cur.description is None:
            return [], []  # no SELECT yet: the skeleton is still blank
        cols = [d[0] for d in cur.description]
        return cols, [tuple(row) for row in cur.fetchall()]

    def run(self, schema: str, ordered: bool = False) -> list[tuple]:
        rows = self._execute(schema)[1]
        return rows if ordered else sorted(rows, key=null_safe)

    def show(self, schema: str) -> None:
        cols, rows = self._execute(schema)
        if not cols:
            print("(no query yet)")
            return
        cells = [[str(c) for c in cols]] + [
            ["NULL" if v is None else str(v) for v in row] for row in rows
        ]
        widths = [max(len(r[i]) for r in cells) for i in range(len(cols))]
        rule = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
        line = lambda r: "| " + " | ".join(v.ljust(w) for v, w in zip(r, widths)) + " |"
        print(rule)
        print(line(cells[0]))
        print(rule)
        for r in cells[1:]:
            print(line(r))
        print(rule)
