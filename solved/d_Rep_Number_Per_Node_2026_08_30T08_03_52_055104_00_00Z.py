"""
DRILL: Rep Number Per Node
TRAINS: spark-window-rank

Given the DataFrame `verdicts`, return every row with one new integer
column `rn`. Within each `node_id`, sort that node's rows by `date` from
newest to oldest and number them 1, 2, 3, and so on. That number is `rn`, so
the newest verdict of every node has `rn` equal to 1. No ordering required.

DataFrame: verdicts

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | node_id     | string  |
    | date        | string  |
    | verdict     | string  |
    +-------------+---------+
    No node has two verdicts on the same date.

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
+-----------------+------------+-----------+----+
| node_id         | date       | verdict   | rn |
+-----------------+------------+-----------+----+
| monotonic-stack | 2026-08-20 | clean     | 1  |
| monotonic-stack | 2026-08-10 | clean     | 2  |
| monotonic-stack | 2026-08-01 | struggled | 3  |
| two-pointers    | 2026-08-05 | avoided   | 1  |
+-----------------+------------+-----------+----+
Explanation: two-pointers starts again at 1.

Example 2:

Input:
verdicts:
+--------------+------------+---------+
| node_id      | date       | verdict |
+--------------+------------+---------+
| two-pointers | 2026-08-05 | clean   |
+--------------+------------+---------+
Output:
+--------------+------------+---------+----+
| node_id      | date       | verdict | rn |
+--------------+------------+---------+----+
| two-pointers | 2026-08-05 | clean   | 1  |
+--------------+------------+---------+----+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: numbering must restart at 1 for every `node_id`, newest `date`
    first; an `rn` that runs as one sequence across nodes fails, and one that
    counts oldest first fails. NO collect().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.

---

Assisted.

"""

from pyspark.sql import Window
from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, verdicts):
        w = Window.partitionBy("node_id").orderBy(F.col("date").desc())
        return verdicts.withColumn("rn", F.row_number().over(w))


VERDICTS = "node_id string, date string, verdict string"

EXAMPLE_1 = {
    "verdicts": (
        [
            ("monotonic-stack", "2026-08-01", "struggled"),
            ("monotonic-stack", "2026-08-20", "clean"),
            ("monotonic-stack", "2026-08-10", "clean"),
            ("two-pointers", "2026-08-05", "avoided"),
        ],
        VERDICTS,
    ),
}

EXAMPLE_2 = {
    "verdicts": (
        [
            ("two-pointers", "2026-08-05", "clean"),
        ],
        VERDICTS,
    ),
}


sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [
    ("monotonic-stack", "2026-08-01", "struggled", 3),
    ("monotonic-stack", "2026-08-10", "clean", 2),
    ("monotonic-stack", "2026-08-20", "clean", 1),
    ("two-pointers", "2026-08-05", "avoided", 1),
]
assert sol.run(EXAMPLE_2) == [("two-pointers", "2026-08-05", "clean", 1)]
