"""
DRILL: Island Key
TRAINS: sql-gaps-islands

Given the table `Seats`, return `id` and `grp` for every row, where `grp`
is the same number for every `id` in one run of consecutive ids and a
different number for each run. Number the rows by `id` starting at 1; `grp`
is the `id` minus that row number. No ordering required.

Table: Seats

    +-------------+------+
    | Column Name | Type |
    +-------------+------+
    | id          | int  |
    +-------------+------+
    id is the primary key. Ids may be missing.

Example 1:

Input:
Seats table:
+----+
| id |
+----+
| 1  |
| 2  |
| 3  |
| 5  |
| 6  |
| 9  |
+----+
Output:
+----+-----+
| id | grp |
+----+-----+
| 1  | 0   |
| 2  | 0   |
| 3  | 0   |
| 5  | 1   |
| 6  | 1   |
| 9  | 3   |
+----+-----+
Explanation: Three runs: 1-3, 5-6 and 9. Row 5 is the 4th row, so its grp is 5 - 4 = 1.

Example 2:

Input:
Seats table:
+----+
| id |
+----+
| 4  |
| 5  |
| 6  |
+----+
Output:
+----+-----+
| id | grp |
+----+-----+
| 4  | 3   |
| 5  | 3   |
| 6  | 3   |
+----+-----+
Explanation: One run, so every row has the same grp.

Constraints:

    1 <= number of rows <= 10^5
    1 <= id <= 10^9

    REQUIRED: one pass over Seats with a window function, rows numbered by
    id.

    FORBIDDEN: a self-join; a correlated subquery; numbering by physical
    order.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Seats (id INTEGER);
INSERT INTO Seats VALUES (1);
INSERT INTO Seats VALUES (2);
INSERT INTO Seats VALUES (3);
INSERT INTO Seats VALUES (5);
INSERT INTO Seats VALUES (6);
INSERT INTO Seats VALUES (9);
"""

EXAMPLE_2 = """
CREATE TABLE Seats (id INTEGER);
INSERT INTO Seats VALUES (4);
INSERT INTO Seats VALUES (5);
INSERT INTO Seats VALUES (6);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(1, 0), (2, 0), (3, 0), (5, 1), (6, 1), (9, 3)]
# assert sol.run(EXAMPLE_2) == [(4, 3), (5, 3), (6, 3)]
