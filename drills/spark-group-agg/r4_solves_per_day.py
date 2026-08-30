"""
DRILL: Solves Per Day
TRAINS: spark-group-agg

Given the DataFrame `solves`, return one row per date with the number of
solves that day in the `solves` column and the number of distinct problems
that day in the `problems` column. No ordering required.

Syntax:

    orders.groupBy("customer").agg(
        F.count("id").alias("orders"),
        F.countDistinct("product").alias("products"),
    )

    One agg call takes any number of aggregates; each becomes a column.

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
+------------+--------+----------+
| date       | solves | problems |
+------------+--------+----------+
| 2026-08-28 | 3      | 2        |
| 2026-08-29 | 1      | 1        |
+------------+--------+----------+
Explanation: 2026-08-28 has three solves over problems 1 and 42.

Example 2:

Input:
solves:
+------+------------+---------+
| file | date       | problem |
+------+------------+---------+
| a.py | 2026-08-29 | 1       |
+------+------------+---------+
Output:
+------------+--------+----------+
| date       | solves | problems |
+------------+--------+----------+
| 2026-08-29 | 1      | 1        |
+------------+--------+----------+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one groupBy and one agg producing both numbers; the output
    columns must be named solves and problems, not count(file). NO second
    groupBy, NO collect().

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

# assert sol.run(EXAMPLE_1) == [("2026-08-28", 3, 2), ("2026-08-29", 1, 1)]
# assert sol.run(EXAMPLE_2) == [("2026-08-29", 1, 1)]
