"""
DRILL: Consecutive Numbers
TRAINS: sql-window-offset

Given the table Logs, return every num that appears at least three times in a
row when the rows are ordered by id. Each qualifying num appears once in the
result. Order by num.

Table: Logs

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | num         | int     |
    +-------------+---------+
    id is the primary key and increases by one per row.

Example 1:

Input:
Logs table:
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |
+----+-----+
Output:
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
Explanation: 1 appears at ids 1, 2, 3. 2 appears only twice in a row.

Example 2:

Input:
Logs table:
+----+-----+
| id | num |
+----+-----+
| 1  | 5   |
| 2  | 5   |
| 3  | 5   |
| 4  | 5   |
| 5  | 3   |
| 6  | 3   |
+----+-----+
Output:
+-----------------+
| ConsecutiveNums |
+-----------------+
| 5               |
+-----------------+
Explanation: 5 appears four times in a row and is listed once; 3 only twice.

Constraints:

    1 <= number of rows <= 10^5

    REQUIRED: LAG(num) OVER (ORDER BY id) and LEAD(num) OVER (ORDER BY id),
    then keep rows where both equal num, and DISTINCT. The window must ORDER
    BY id; an empty OVER () relies on physical row order and is the failure
    mode this drill exists to kill. (A double self-join on id - 1 and id + 1
    is the pre-window form.)

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Logs (id INTEGER, num INTEGER);
INSERT INTO Logs VALUES (1, 1);
INSERT INTO Logs VALUES (2, 1);
INSERT INTO Logs VALUES (3, 1);
INSERT INTO Logs VALUES (4, 2);
INSERT INTO Logs VALUES (5, 1);
INSERT INTO Logs VALUES (6, 2);
INSERT INTO Logs VALUES (7, 2);
"""

EXAMPLE_2 = """
CREATE TABLE Logs (id INTEGER, num INTEGER);
INSERT INTO Logs VALUES (1, 5);
INSERT INTO Logs VALUES (2, 5);
INSERT INTO Logs VALUES (3, 5);
INSERT INTO Logs VALUES (4, 5);
INSERT INTO Logs VALUES (5, 3);
INSERT INTO Logs VALUES (6, 3);
"""


class Solution:

    def query(self) -> str:
        return """

        """


def run(schema: str, sql: str) -> list[tuple]:
    con = sqlite3.connect(":memory:")
    con.executescript(schema)
    return [tuple(row) for row in con.execute(sql).fetchall()]


sol = Solution()

print(run(EXAMPLE_1, sol.query()))  # [(1,)]

# assert run(EXAMPLE_1, sol.query()) == [(1,)]
# assert run(EXAMPLE_2, sol.query()) == [(5,)]
