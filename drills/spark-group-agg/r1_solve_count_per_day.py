"""
DRILL: Solve Count Per Day
TRAINS: spark-group-agg

Given the DataFrame `solves`, return one row per date with the number of
solves that day in the `solves` column. No ordering required.

DataFrame: solves

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | date        | string  |
    | problem     | string  |
    +-------------+---------+
    file is unique.

Example 1:

Input:
solves:
+------+------------+---------+
| file | date       | problem |
+------+------------+---------+
| a.py | 2026-08-28 | 1       |
| b.py | 2026-08-28 | 1       |
| c.py | 2026-08-28 | 42      |
| d.py | 2026-08-29 | 76      |
+------+------------+---------+
Output:
+------------+--------+
| date       | solves |
+------------+--------+
| 2026-08-28 | 3      |
| 2026-08-29 | 1      |
+------------+--------+
Explanation: three files carry the date 2026-08-28.

Example 2:

Input:
solves:
+------+------------+---------+
| file | date       | problem |
+------+------------+---------+
| a.py | 2026-08-29 | 1       |
+------+------------+---------+
Output:
+------------+--------+
| date       | solves |
+------------+--------+
| 2026-08-29 | 1      |
+------------+--------+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one groupBy and one agg; the output column must be named
    solves, not count(file). NO collect().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, solves):
        pass


SOLVES = "file string, date string, problem string"

EXAMPLE_1 = {
    "solves": ([
        ("a.py", "2026-08-28", "1"),
        ("b.py", "2026-08-28", "1"),
        ("c.py", "2026-08-28", "42"),
        ("d.py", "2026-08-29", "76"),
    ], SOLVES),
}

EXAMPLE_2 = {
    "solves": ([
        ("a.py", "2026-08-29", "1"),
    ], SOLVES),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("2026-08-28", 3), ("2026-08-29", 1)]
# assert sol.run(EXAMPLE_2) == [("2026-08-29", 1)]
