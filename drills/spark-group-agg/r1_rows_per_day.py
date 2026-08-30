"""
DRILL: Rows Per Day
TRAINS: spark-group-agg

Given the DataFrame `solves`, return each `date` with the number of solves
on that date in the `count` column. No ordering required.

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
+------+------------+
Output:
+------------+-------+
| date       | count |
+------------+-------+
| 2026-08-28 | 2     |
| 2026-08-29 | 1     |
+------------+-------+

Example 2:

Input:
solves:
+------+------------+
| file | date       |
+------+------------+
| a.py | 2026-08-29 |
+------+------------+
Output:
+------------+-------+
| date       | count |
+------------+-------+
| 2026-08-29 | 1     |
+------------+-------+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one groupBy and its own count; the output column is named
    count. NO agg, NO collect().

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
    "solves": (
        [
            ("a.py", "2026-08-28"),
            ("b.py", "2026-08-28"),
            ("c.py", "2026-08-29"),
        ],
        SOLVES,
    ),
}

EXAMPLE_2 = {
    "solves": (
        [
            ("a.py", "2026-08-29"),
        ],
        SOLVES,
    ),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("2026-08-28", 2), ("2026-08-29", 1)]
# assert sol.run(EXAMPLE_2) == [("2026-08-29", 1)]
