"""
DRILL: Top Two Distinct Scores

Given the table `Scores`, return `id` and `score` for every row whose
`score` is among the two highest distinct scores. No ordering required.

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
+----+-------+
| id | score |
+----+-------+
| 3  | 4.0   |
| 4  | 3.85  |
| 5  | 4.0   |
+----+-------+
Explanation: The two highest distinct scores are 4.0 and 3.85; both rows with 4.0 appear.

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
+----+-------+
| id | score |
+----+-------+
| 1  | 7.0   |
| 2  | 7.0   |
| 3  | 7.0   |
+----+-------+
Explanation: There is only one distinct score, so every row is kept.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the dense rank must be computed in a WITH clause and filtered
    in the query that reads from it.

    FORBIDDEN: a scalar subquery for the cutoff score; referencing the
    window in the WHERE of the query that computes it.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


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


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(3, 4.0), (4, 3.85), (5, 4.0)]
# assert sol.run(EXAMPLE_2) == [(1, 7.0), (2, 7.0), (3, 7.0)]
