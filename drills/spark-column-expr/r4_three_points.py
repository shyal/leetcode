"""
DRILL: Three Points
TRAINS: spark-column-expr

Given the DataFrame `solves`, return every row with a new integer column
`points` holding 3. No ordering required.

Syntax:

    employees.withColumn("bonus", F.lit(100))

    withColumn adds one column and keeps every other. A plain Python value
    must be wrapped in F.lit to become a Column.

DataFrame: solves

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | assist      | string  |
    +-------------+---------+
    file is unique.

Example 1:

Input:
solves:
+------+--------+
| file | assist |
+------+--------+
| a.py | none   |
| b.py | hint   |
+------+--------+
Output:
+------+--------+--------+
| file | assist | points |
+------+--------+--------+
| a.py | none   | 3      |
| b.py | hint   | 3      |
+------+--------+--------+

Example 2:

Input:
solves:
+------+--------+
| file | assist |
+------+--------+
| a.py | none   |
+------+--------+
Output:
+------+--------+--------+
| file | assist | points |
+------+--------+--------+
| a.py | none   | 3      |
+------+--------+--------+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: points is added in one call. Passing the Python int 3
    raises NOT_EXPECTED_TYPE. NO collect(), NO toPandas().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, solves):
        pass


SOLVES = "file string, assist string"

EXAMPLE_1 = {
    "solves": (
        [
            ("a.py", "none"),
            ("b.py", "hint"),
        ],
        SOLVES,
    ),
}

EXAMPLE_2 = {
    "solves": (
        [
            ("a.py", "none"),
        ],
        SOLVES,
    ),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("a.py", "none", 3), ("b.py", "hint", 3)]
# assert sol.run(EXAMPLE_2) == [("a.py", "none", 3)]
