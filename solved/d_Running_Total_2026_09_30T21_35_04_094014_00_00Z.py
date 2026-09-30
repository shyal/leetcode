"""
DRILL: Running Total

Given the table `Queue`, return `turn` and `total` for every row, where
`total` is the sum of `weight` over every row whose `turn` is less than or
equal to this row's `turn`. No ordering required.

Table: Queue

    +-------------+------+
    | Column Name | Type |
    +-------------+------+
    | weight      | int  |
    | turn        | int  |
    +-------------+------+
    turn holds every integer from 1 to n exactly once.

Example 1:

Input:
Queue table:
+--------+------+
| weight | turn |
+--------+------+
| 250    | 1    |
| 350    | 3    |
| 400    | 2    |
+--------+------+
Output:
+------+-------+
| turn | total |
+------+-------+
| 1    | 250   |
| 2    | 650   |
| 3    | 1000  |
+------+-------+
Explanation: Turn 2 comes before turn 3 even though its row is stored later: 250 + 400 = 650.

Example 2:

Input:
Queue table:
+--------+------+
| weight | turn |
+--------+------+
| 600    | 1    |
+--------+------+
Output:
+------+-------+
| turn | total |
+------+-------+
| 1    | 600   |
+------+-------+
Explanation: The first row's total is its own weight.

Constraints:

    1 <= number of rows <= 10^5
    1 <= weight <= 1000

    REQUIRED: one pass over Queue with a window function.

    FORBIDDEN: a self-join; a correlated subquery (summing the earlier rows
    again for every row is O(n^2)).

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


# mu 0.7
# extends SQLDrill
#
# def query() -> str
#   return '\n\n      select turn, sum(weight) over (order by turn) as total from Queue;  '

class Solution(SQLDrill):
    def query(self) -> str:
        return '\n\n      select turn, sum(weight) over (order by turn) as total from Queue;  '


EXAMPLE_1 = '\nCREATE TABLE Queue (weight INTEGER, turn INTEGER);\nINSERT INTO Queue VALUES (250, 1);\nINSERT INTO Queue VALUES (350, 3);\nINSERT INTO Queue VALUES (400, 2);\n'
EXAMPLE_2 = '\nCREATE TABLE Queue (weight INTEGER, turn INTEGER);\nINSERT INTO Queue VALUES (600, 1);\n'
sol = Solution()
sol.show(EXAMPLE_1)
assert sol.run(EXAMPLE_1) == [(1, 250), (2, 650), (3, 1000)]
assert sol.run(EXAMPLE_2) == [(1, 600)]
