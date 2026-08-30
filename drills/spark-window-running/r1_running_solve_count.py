"""
DRILL: Running Solve Count
TRAINS: spark-window-running

Given the DataFrame `daily`, return every row with a new column `running`:
the total of `solves` for that `difficulty` on that `date` and every earlier
date. No ordering required.

Syntax:

    w = (Window.partitionBy("customer").orderBy("day")
                .rowsBetween(Window.unboundedPreceding, Window.currentRow))
    orders.withColumn("running", F.sum("amount").over(w))

    rowsBetween sets the frame: which rows around this one the aggregate
    sees. From the first row of the partition up to this row gives a running
    total.

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
| Easy       | 2026-08-27 | 2      |
| Easy       | 2026-08-28 | 3      |
| Easy       | 2026-08-29 | 1      |
| Hard       | 2026-08-28 | 1      |
| Hard       | 2026-08-29 | 1      |
+------------+------------+--------+
Output:
+------------+------------+--------+---------+
| difficulty | date       | solves | running |
+------------+------------+--------+---------+
| Easy       | 2026-08-27 | 2      | 2       |
| Easy       | 2026-08-28 | 3      | 5       |
| Easy       | 2026-08-29 | 1      | 6       |
| Hard       | 2026-08-28 | 1      | 1       |
| Hard       | 2026-08-29 | 1      | 2       |
+------------+------------+--------+---------+
Explanation: each difficulty restarts its total from its own first date.

Example 2:

Input:
daily:
+------------+------------+--------+
| difficulty | date       | solves |
+------------+------------+--------+
| Hard       | 2026-08-29 | 4      |
+------------+------------+--------+
Output:
+------------+------------+--------+---------+
| difficulty | date       | solves | running |
+------------+------------+--------+---------+
| Hard       | 2026-08-29 | 4      | 4       |
+------------+------------+--------+---------+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: every input row survives with its running value attached, and
    a difficulty's total must never include another difficulty's rows. A
    window with no partitioning sums across difficulties and fails. NO
    self-join, NO collect().

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
        ("Easy", "2026-08-27", 2),
        ("Easy", "2026-08-28", 3),
        ("Easy", "2026-08-29", 1),
        ("Hard", "2026-08-28", 1),
        ("Hard", "2026-08-29", 1),
    ], DAILY),
}

EXAMPLE_2 = {
    "daily": ([
        ("Hard", "2026-08-29", 4),
    ], DAILY),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("Easy", "2026-08-27", 2, 2), ("Easy", "2026-08-28", 3, 5), ("Easy", "2026-08-29", 1, 6), ("Hard", "2026-08-28", 1, 1), ("Hard", "2026-08-29", 1, 2)]
# assert sol.run(EXAMPLE_2) == [("Hard", "2026-08-29", 4, 4)]
