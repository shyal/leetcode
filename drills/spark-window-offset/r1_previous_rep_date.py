"""
DRILL: Previous Rep Date
TRAINS: spark-window-offset

Given the DataFrame `verdicts`, return every row with a new date column
`prev`: the `date` of the previous verdict on the same `node_id`. The first
verdict on a node gets a null `prev`. No ordering required.

DataFrame: verdicts

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | node_id     | string  |
    | date        | date    |
    | verdict     | string  |
    +-------------+---------+
    (node_id, date) is unique.

Example 1:

Input:
verdicts:
+-----------------+------------+-----------+
| node_id         | date       | verdict   |
+-----------------+------------+-----------+
| monotonic-stack | 2026-08-01 | struggled |
| monotonic-stack | 2026-08-10 | clean     |
| monotonic-stack | 2026-08-20 | clean     |
| two-pointers    | 2026-08-05 | clean     |
+-----------------+------------+-----------+
Output:
+-----------------+------------+-----------+------------+
| node_id         | date       | verdict   | prev       |
+-----------------+------------+-----------+------------+
| monotonic-stack | 2026-08-01 | struggled | NULL       |
| monotonic-stack | 2026-08-10 | clean     | 2026-08-01 |
| monotonic-stack | 2026-08-20 | clean     | 2026-08-10 |
| two-pointers    | 2026-08-05 | clean     | NULL       |
+-----------------+------------+-----------+------------+
Explanation: two-pointers has one verdict, so it has no previous one.

Example 2:

Input:
verdicts:
+--------------+------------+---------+
| node_id      | date       | verdict |
+--------------+------------+---------+
| two-pointers | 2026-08-05 | clean   |
| two-pointers | 2026-08-06 | clean   |
+--------------+------------+---------+
Output:
+--------------+------------+---------+------------+
| node_id      | date       | verdict | prev       |
+--------------+------------+---------+------------+
| two-pointers | 2026-08-05 | clean   | NULL       |
| two-pointers | 2026-08-06 | clean   | 2026-08-05 |
+--------------+------------+---------+------------+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: every row survives with its own node's previous date; a
    window without partitioning hands two-pointers the last monotonic-stack
    date and fails. NO self-join, NO collect().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from datetime import date

from pyspark.sql import Window
from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, verdicts):
        pass


VERDICTS = "node_id string, date date, verdict string"

EXAMPLE_1 = {
    "verdicts": ([
        ("monotonic-stack", date(2026, 8, 1), "struggled"),
        ("monotonic-stack", date(2026, 8, 10), "clean"),
        ("monotonic-stack", date(2026, 8, 20), "clean"),
        ("two-pointers", date(2026, 8, 5), "clean"),
    ], VERDICTS),
}

EXAMPLE_2 = {
    "verdicts": ([
        ("two-pointers", date(2026, 8, 5), "clean"),
        ("two-pointers", date(2026, 8, 6), "clean"),
    ], VERDICTS),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("monotonic-stack", date(2026, 8, 1), "struggled", None), ("monotonic-stack", date(2026, 8, 10), "clean", date(2026, 8, 1)), ("monotonic-stack", date(2026, 8, 20), "clean", date(2026, 8, 10)), ("two-pointers", date(2026, 8, 5), "clean", None)]
# assert sol.run(EXAMPLE_2) == [("two-pointers", date(2026, 8, 5), "clean", None), ("two-pointers", date(2026, 8, 6), "clean", date(2026, 8, 5))]
