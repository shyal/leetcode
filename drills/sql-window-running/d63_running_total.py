"""
Given a table Queue, return turn and total for every row.

For each row, total is the sum of weight for all rows whose turn is less
than or equal to that row's turn. In other words, each row's total includes
its own weight and the weights of all rows with earlier turns.

The output may be in any order.

Table: Queue

    +-------------+------+
    | Column Name | Type |
    +-------------+------+
    | weight      | int  |
    | turn        | int  |
    +-------------+------+
    turn contains every integer from 1 to n exactly once.

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
Explanation:

    Turn 1: 250
    Turn 2: 250 + 400 = 650
    Turn 3: 250 + 400 + 350 = 1000

The rows in the input aren't necessarily stored in turn order.

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

Constraints:

    1 <= number of rows <= 10^5
    1 <= weight <= 1000

Requirements:

    Calculate the running total using a window function in a single query.
    Do not use a self-join or a correlated subquery.
    The calculation must run in O(n) time in terms of the number of rows,
    excluding any sorting required by the database.
    The solution must work with SQLite.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Queue (weight INTEGER, turn INTEGER);
INSERT INTO Queue VALUES (250, 1);
INSERT INTO Queue VALUES (350, 3);
INSERT INTO Queue VALUES (400, 2);
"""

EXAMPLE_2 = """
CREATE TABLE Queue (weight INTEGER, turn INTEGER);
INSERT INTO Queue VALUES (600, 1);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(1, 250), (2, 650), (3, 1000)]
# assert sol.run(EXAMPLE_2) == [(1, 600)]
