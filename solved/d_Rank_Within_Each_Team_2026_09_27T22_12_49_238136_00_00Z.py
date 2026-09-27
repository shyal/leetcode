"""
DRILL: Rank Within Each Team

Given the table `Players`, return `name`, `team` and `rank` for every row.
The rank counts within the player's own team, from highest `points` to
lowest, and starts at 1 in every team. Equal points share a rank, and the
rank after a tie is the next consecutive integer: no holes. No ordering
required.

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
+------+------+------+
| name | team | rank |
+------+------+------+
| Bo   | A    | 1    |
| Di   | A    | 1    |
| Ava  | A    | 2    |
| Flo  | A    | 3    |
| Ed   | B    | 1    |
| Cy   | B    | 2    |
+------+------+------+
Explanation: Team B starts again at 1: Ed's 40 is the highest in B even though team A has higher points.

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
+------+------+------+
| name | team | rank |
+------+------+------+
| Gus  | C    | 1    |
| Hal  | D    | 1    |
| Ivy  | D    | 1    |
+------+------+------+
Explanation: Gus is alone in team C; Hal and Ivy tie in team D.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the rank must restart at 1 in every team, with shared ranks
    and no holes.

    FORBIDDEN: a correlated subquery per row; one rank over the whole table
    (Ed gets 2, not 1).

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


# mu 0.6
# extends SQLDrill
#
# def query() -> str
#   return '\n\n    select name, team, dense_rank() over (partition by team order by points desc) as rank from Players;   '

class Solution(SQLDrill):
    def query(self) -> str:
        return '\n\n    select name, team, dense_rank() over (partition by team order by points desc) as rank from Players;   '


EXAMPLE_1 = "\nCREATE TABLE Players (name TEXT, team TEXT, points INTEGER);\nINSERT INTO Players VALUES ('Ava', 'A', 30);\nINSERT INTO Players VALUES ('Bo', 'A', 50);\nINSERT INTO Players VALUES ('Cy', 'B', 20);\nINSERT INTO Players VALUES ('Di', 'A', 50);\nINSERT INTO Players VALUES ('Ed', 'B', 40);\nINSERT INTO Players VALUES ('Flo', 'A', 10);\n"
EXAMPLE_2 = "\nCREATE TABLE Players (name TEXT, team TEXT, points INTEGER);\nINSERT INTO Players VALUES ('Gus', 'C', 5);\nINSERT INTO Players VALUES ('Hal', 'D', 7);\nINSERT INTO Players VALUES ('Ivy', 'D', 7);\n"
sol = Solution()
sol.show(EXAMPLE_1)
assert sol.run(EXAMPLE_1) == [('Ava', 'A', 2), ('Bo', 'A', 1), ('Cy', 'B', 2), ('Di', 'A', 1), ('Ed', 'B', 1), ('Flo', 'A', 3)]
assert sol.run(EXAMPLE_2) == [('Gus', 'C', 1), ('Hal', 'D', 1), ('Ivy', 'D', 1)]
