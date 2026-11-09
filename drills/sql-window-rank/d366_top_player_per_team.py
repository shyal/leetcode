"""
Given the table `Players(name varchar, team varchar, points int)`, return
the `name` and `team` of every player whose points equal the highest points
in their team, including all ties. No ordering required.

Table: Players

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | name        | varchar |
    | team        | varchar |
    | points      | int     |
    +-------------+---------+
    Names are unique.

Example 1:

Input:
Players table:
+------+------+--------+
| name | team | points |
+------+------+--------+
| Ava  | A    | 30     |
| Bo   | A    | 50     |
| Cy   | B    | 20     |
| Di   | A    | 50     |
| Ed   | B    | 40     |
| Flo  | A    | 10     |
+------+------+--------+
Output:
+------+------+
| name | team |
+------+------+
| Bo   | A    |
| Di   | A    |
| Ed   | B    |
+------+------+
Explanation: Bo and Di tie at 50 in team A; Ed's 40 is the highest in team B.

Example 2:

Input:
Players table:
+------+------+--------+
| name | team | points |
+------+------+--------+
| Gus  | C    | 5      |
| Hal  | D    | 7      |
| Ivy  | D    | 7      |
+------+------+--------+
Output:
+------+------+
| name | team |
+------+------+
| Gus  | C    |
| Hal  | D    |
| Ivy  | D    |
+------+------+
Explanation: Gus is alone in team C; Hal and Ivy tie in team D.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: O(n log n). NO GROUP BY, NO subquery in a WHERE clause.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Players (name TEXT, team TEXT, points INTEGER);
INSERT INTO Players VALUES ('Ava', 'A', 30);
INSERT INTO Players VALUES ('Bo', 'A', 50);
INSERT INTO Players VALUES ('Cy', 'B', 20);
INSERT INTO Players VALUES ('Di', 'A', 50);
INSERT INTO Players VALUES ('Ed', 'B', 40);
INSERT INTO Players VALUES ('Flo', 'A', 10);
"""

EXAMPLE_2 = """
CREATE TABLE Players (name TEXT, team TEXT, points INTEGER);
INSERT INTO Players VALUES ('Gus', 'C', 5);
INSERT INTO Players VALUES ('Hal', 'D', 7);
INSERT INTO Players VALUES ('Ivy', 'D', 7);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [('Bo', 'A'), ('Di', 'A'), ('Ed', 'B')]
# assert sol.run(EXAMPLE_2) == [('Gus', 'C'), ('Hal', 'D'), ('Ivy', 'D')]
