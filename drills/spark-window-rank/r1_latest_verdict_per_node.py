"""
DRILL: Latest Verdict Per Node
TRAINS: spark-window-rank

Given the DataFrame verdicts, return node_id, date and verdict of the most
recent verdict on each node. Any row order.

DataFrame: verdicts

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | node_id     | string  |
    | date        | string  |
    | verdict     | string  |
    +-------------+---------+
    (node_id, date) is unique. date is YYYY-MM-DD, so string order is date
    order.

Example 1:

Input:
verdicts:
+-----------------+------------+-----------+
| node_id         | date       | verdict   |
+-----------------+------------+-----------+
| monotonic-stack | 2026-08-01 | struggled |
| monotonic-stack | 2026-08-20 | clean     |
| monotonic-stack | 2026-08-10 | clean     |
| two-pointers    | 2026-08-05 | avoided   |
+-----------------+------------+-----------+
Output:
+-----------------+------------+---------+
| node_id         | date       | verdict |
+-----------------+------------+---------+
| monotonic-stack | 2026-08-20 | clean   |
| two-pointers    | 2026-08-05 | avoided |
+-----------------+------------+---------+

Example 2:

Input:
verdicts:
+--------------+------------+---------+
| node_id      | date       | verdict |
+--------------+------------+---------+
| two-pointers | 2026-08-05 | clean   |
+--------------+------------+---------+
Output:
+--------------+------------+---------+
| node_id      | date       | verdict |
+--------------+------------+---------+
| two-pointers | 2026-08-05 | clean   |
+--------------+------------+---------+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: exactly one row per node, chosen by date, with the other
    columns of that same row; the output must carry only the three columns
    named. NO dropDuplicates (the survivor is arbitrary), NO groupBy max
    joined back, NO collect().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import Window
from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, verdicts):
        pass


VERDICTS = "node_id string, date string, verdict string"

EXAMPLE_1 = {
    "verdicts": ([
        ("monotonic-stack", "2026-08-01", "struggled"),
        ("monotonic-stack", "2026-08-20", "clean"),
        ("monotonic-stack", "2026-08-10", "clean"),
        ("two-pointers", "2026-08-05", "avoided"),
    ], VERDICTS),
}

EXAMPLE_2 = {
    "verdicts": ([
        ("two-pointers", "2026-08-05", "clean"),
    ], VERDICTS),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("monotonic-stack", "2026-08-20", "clean"), ("two-pointers", "2026-08-05", "avoided")]
# assert sol.run(EXAMPLE_2) == [("two-pointers", "2026-08-05", "clean")]
