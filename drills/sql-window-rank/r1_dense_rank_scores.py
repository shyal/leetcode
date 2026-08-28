"""
DRILL: Dense Rank Scores
TRAINS: sql-window-rank

Given the table Scores, return score and rank for every row, ranked from
highest score to lowest. Equal scores share a rank, and the rank after a tie
is the next consecutive integer: no holes. Order by score descending.

Table: Scores

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | score       | decimal |
    +-------------+---------+
    id is the primary key.

Example 1:

Input:
Scores table:
+----+-------+
| id | score |
+----+-------+
| 1  | 3.5   |
| 2  | 3.65  |
| 3  | 4.0   |
| 4  | 3.85  |
| 5  | 4.0   |
| 6  | 3.65  |
+----+-------+
Output:
+-------+------+
| score | rank |
+-------+------+
| 4.0   | 1    |
| 4.0   | 1    |
| 3.85  | 2    |
| 3.65  | 3    |
| 3.65  | 3    |
| 3.5   | 4    |
+-------+------+
Explanation: 4.00 twice at rank 1, then 3.85 at rank 2, 3.65 twice at rank 3, 3.50 at rank 4.

Example 2:

Input:
Scores table:
+----+-------+
| id | score |
+----+-------+
| 1  | 7.0   |
| 2  | 7.0   |
| 3  | 7.0   |
+----+-------+
Output:
+-------+------+
| score | rank |
+-------+------+
| 7.0   | 1    |
| 7.0   | 1    |
| 7.0   | 1    |
+-------+------+
Explanation: All equal: everyone is rank 1.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: DENSE_RANK() OVER (ORDER BY score DESC). RANK() leaves holes
    after a tie (1, 1, 3) and ROW_NUMBER() breaks ties (1, 2, 3); both are the
    failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Scores (id INTEGER, score REAL);
INSERT INTO Scores VALUES (1, 3.5);
INSERT INTO Scores VALUES (2, 3.65);
INSERT INTO Scores VALUES (3, 4.0);
INSERT INTO Scores VALUES (4, 3.85);
INSERT INTO Scores VALUES (5, 4.0);
INSERT INTO Scores VALUES (6, 3.65);
"""

EXAMPLE_2 = """
CREATE TABLE Scores (id INTEGER, score REAL);
INSERT INTO Scores VALUES (1, 7.0);
INSERT INTO Scores VALUES (2, 7.0);
INSERT INTO Scores VALUES (3, 7.0);
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

print(run(EXAMPLE_1, sol.query()))  # [(4.0, 1), (4.0, 1), (3.85, 2), (3.65, 3), (3.65, 3), (3.5, 4)]

# assert run(EXAMPLE_1, sol.query()) == [(4.0, 1), (4.0, 1), (3.85, 2), (3.65, 3), (3.65, 3), (3.5, 4)]
# assert run(EXAMPLE_2, sol.query()) == [(7.0, 1), (7.0, 1), (7.0, 1)]
