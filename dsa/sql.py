import sqlite3


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
        cur = con.execute(self.query())
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
