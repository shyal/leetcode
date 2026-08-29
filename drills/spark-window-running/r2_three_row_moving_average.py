"""
DRILL: Three Row Moving Average
TRAINS: spark-window-running

Given the DataFrame daily, return every row with a new column avg3: the
average of solves over that row and the two rows before it within the same
difficulty, in date order, rounded to two decimals. The first two rows of a
difficulty average over the rows that exist. Any row order.

DataFrame: daily

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | difficulty  | string  |
    | date        | string  |
    | solves      | int     |
    +-------------+---------+
    (difficulty, date) is unique. date is YYYY-MM-DD.

Example 1:

Input:
daily:
+------------+------------+--------+
| difficulty | date       | solves |
+------------+------------+--------+
| Easy       | 2026-08-26 | 2      |
| Easy       | 2026-08-27 | 4      |
| Easy       | 2026-08-28 | 3      |
| Easy       | 2026-08-29 | 8      |
| Hard       | 2026-08-29 | 1      |
+------------+------------+--------+
Output:
+------------+------------+--------+------+
| difficulty | date       | solves | avg3 |
+------------+------------+--------+------+
| Easy       | 2026-08-26 | 2      | 2.0  |
| Easy       | 2026-08-27 | 4      | 3.0  |
| Easy       | 2026-08-28 | 3      | 3.0  |
| Easy       | 2026-08-29 | 8      | 5.0  |
| Hard       | 2026-08-29 | 1      | 1.0  |
+------------+------------+--------+------+
Explanation: 2026-08-29 Easy averages 4, 3 and 8; 2026-08-27 averages 2 and 4.

Example 2:

Input:
daily:
+------------+------------+--------+
| difficulty | date       | solves |
+------------+------------+--------+
| Hard       | 2026-08-27 | 1      |
| Hard       | 2026-08-28 | 2      |
| Hard       | 2026-08-29 | 6      |
| Hard       | 2026-08-30 | 1      |
+------------+------------+--------+
Output:
+------------+------------+--------+------+
| difficulty | date       | solves | avg3 |
+------------+------------+--------+------+
| Hard       | 2026-08-27 | 1      | 1.0  |
| Hard       | 2026-08-28 | 2      | 1.5  |
| Hard       | 2026-08-29 | 6      | 3.0  |
| Hard       | 2026-08-30 | 1      | 3.0  |
+------------+------------+--------+------+
Explanation: 2026-08-30 averages 2, 6 and 1, so the first row has dropped out.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the frame must be exactly three rows wide once three exist;
    the default frame runs from the first row and returns 4.25 for the last
    Easy row, which fails. NO self-join, NO collect().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import Window
from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, daily):
        pass


DAILY = "difficulty string, date string, solves int"

EXAMPLE_1 = {
    "daily": ([
        ("Easy", "2026-08-26", 2),
        ("Easy", "2026-08-27", 4),
        ("Easy", "2026-08-28", 3),
        ("Easy", "2026-08-29", 8),
        ("Hard", "2026-08-29", 1),
    ], DAILY),
}

EXAMPLE_2 = {
    "daily": ([
        ("Hard", "2026-08-27", 1),
        ("Hard", "2026-08-28", 2),
        ("Hard", "2026-08-29", 6),
        ("Hard", "2026-08-30", 1),
    ], DAILY),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("Easy", "2026-08-26", 2, 2.0), ("Easy", "2026-08-27", 4, 3.0), ("Easy", "2026-08-28", 3, 3.0), ("Easy", "2026-08-29", 8, 5.0), ("Hard", "2026-08-29", 1, 1.0)]
# assert sol.run(EXAMPLE_2) == [("Hard", "2026-08-27", 1, 1.0), ("Hard", "2026-08-28", 2, 1.5), ("Hard", "2026-08-29", 6, 3.0), ("Hard", "2026-08-30", 1, 3.0)]
