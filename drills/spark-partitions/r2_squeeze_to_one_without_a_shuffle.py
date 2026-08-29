"""
DRILL: Squeeze To One Without A Shuffle
TRAINS: spark-partitions

Given the DataFrame solves, which arrives in two partitions, return the same
rows in exactly one partition without a shuffle, so that a later write
produces one file. Any row order.

DataFrame: solves

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | date        | string  |
    +-------------+---------+
    file is unique.

Example 1:

Input:
solves:
+------+------------+
| file | date       |
+------+------------+
| a.py | 2026-08-28 |
| b.py | 2026-08-28 |
| c.py | 2026-08-29 |
| d.py | 2026-08-29 |
+------+------------+
Output: the same four rows; sol.result(EXAMPLE_1).rdd.getNumPartitions()
is 1 and sol.plan(EXAMPLE_1) contains no Exchange.

Example 2:

Input:
solves:
+------+------------+
| file | date       |
+------+------------+
| a.py | 2026-08-29 |
+------+------------+
Output: the same row, in 1 partition, no Exchange in the plan.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the result must report exactly 1 partition and its plan must
    not contain the word Exchange; the full resize reaches 1 partition
    through a shuffle and fails on the plan. NO collect() and rebuild.

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    engine = "jvm"  # df.rdd and the plan need real Spark

    def transform(self, solves):
        pass


SOLVES = "file string, date string"

EXAMPLE_1 = {
    "solves": ([
        ("a.py", "2026-08-28"),
        ("b.py", "2026-08-28"),
        ("c.py", "2026-08-29"),
        ("d.py", "2026-08-29"),
    ], SOLVES),
}

EXAMPLE_2 = {
    "solves": ([
        ("a.py", "2026-08-29"),
    ], SOLVES),
}


sol = Solution()

sol.show(EXAMPLE_1)
print(sol.plan(EXAMPLE_1))

# assert sol.run(EXAMPLE_1) == [("a.py", "2026-08-28"), ("b.py", "2026-08-28"), ("c.py", "2026-08-29"), ("d.py", "2026-08-29")]
# assert sol.result(EXAMPLE_1).rdd.getNumPartitions() == 1
# assert "Exchange" not in sol.plan(EXAMPLE_1)
# assert sol.run(EXAMPLE_2) == [("a.py", "2026-08-29")]
# assert sol.result(EXAMPLE_2).rdd.getNumPartitions() == 1
