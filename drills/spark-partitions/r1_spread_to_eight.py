"""
DRILL: Spread To Eight
TRAINS: spark-partitions

Given the DataFrame solves, which arrives in two partitions, return the same
rows spread evenly over exactly eight partitions. Any row order.

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
is 8.

Example 2:

Input:
solves:
+------+------------+
| file | date       |
+------+------------+
| a.py | 2026-08-29 |
+------+------------+
Output: the same row, in 8 partitions, 7 of them empty.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the result must report exactly 8 partitions. The narrow
    resize cannot grow a frame: asked for 8 it silently keeps 2 and fails.
    NO collect() and rebuild.

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

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
# assert sol.result(EXAMPLE_1).rdd.getNumPartitions() == 8
# assert sol.run(EXAMPLE_2) == [("a.py", "2026-08-29")]
# assert sol.result(EXAMPLE_2).rdd.getNumPartitions() == 8
