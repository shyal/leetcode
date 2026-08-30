"""
DRILL: Problems Per Day
TRAINS: spark-group-agg

Given the DataFrame `solves`, return one row per date with the number of
distinct problems solved that day in the `problems` column. No ordering
required.

DataFrame: solves

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | date        | string  |
    | problem     | string  |
    +-------------+---------+
    file is unique. The same problem can be solved several times on one day.

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
+------------+----------+
| date       | problems |
+------------+----------+
| 2026-08-28 | 2        |
| 2026-08-29 | 1        |
+------------+----------+
Explanation: 2026-08-28 has three solves over problems 1 and 42.

Example 2:

Input:
solves:
+------+------------+---------+
| file | date       | problem |
+------+------------+---------+
| a.py | 2026-08-29 | 1       |
| b.py | 2026-08-29 | 1       |
+------+------------+---------+
Output:
+------------+----------+
| date       | problems |
+------------+----------+
| 2026-08-29 | 1        |
+------------+----------+
Explanation: two solves, one problem.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one groupBy and one agg; a problem solved twice on a day
    counts once; the output column must be named problems. NO
    dropDuplicates first, NO second groupBy, NO collect().

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
        ("b.py", "2026-08-29", "1"),
    ], SOLVES),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("2026-08-28", 2), ("2026-08-29", 1)]
# assert sol.run(EXAMPLE_2) == [("2026-08-29", 1)]
