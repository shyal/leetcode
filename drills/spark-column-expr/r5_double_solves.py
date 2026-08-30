"""
DRILL: Double Solves
TRAINS: spark-column-expr

Given the DataFrame `counts`, return every row with a new integer column
`doubled` holding twice `solves`. No ordering required.

Syntax:

    employees.withColumn("doubled", F.col("salary") * 2)

    A Column and a number, or two Columns, combine with + - * / into a new
    Column.

DataFrame: counts

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | num         | string  |
    | solves      | int     |
    +-------------+---------+
    num is unique.

Example 1:

Input:
counts:
+-----+--------+
| num | solves |
+-----+--------+
| 42  | 5      |
| 1   | 3      |
+-----+--------+
Output:
+-----+--------+---------+
| num | solves | doubled |
+-----+--------+---------+
| 42  | 5      | 10      |
| 1   | 3      | 6       |
+-----+--------+---------+

Example 2:

Input:
counts:
+-----+--------+
| num | solves |
+-----+--------+
| 1   | 0      |
+-----+--------+
Output:
+-----+--------+---------+
| num | solves | doubled |
+-----+--------+---------+
| 1   | 0      | 0       |
+-----+--------+---------+

Constraints:

    1 <= number of rows <= 10^4
    0 <= solves <= 10^4

    REQUIRED: doubled is added in one call as a Column expression built
    from solves. NO UDF, NO collect().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, counts):
        pass


COUNTS = "num string, solves int"

EXAMPLE_1 = {
    "counts": (
        [
            ("42", 5),
            ("1", 3),
        ],
        COUNTS,
    ),
}

EXAMPLE_2 = {
    "counts": (
        [
            ("1", 0),
        ],
        COUNTS,
    ),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("1", 3, 6), ("42", 5, 10)]
# assert sol.run(EXAMPLE_2) == [("1", 0, 0)]
