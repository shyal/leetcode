"""
DRILL: Num And Doubled
TRAINS: spark-column-expr

Given the DataFrame `counts`, return `num` and a column `doubled` holding
twice `solves`, and nothing else. No ordering required.

Syntax:

    employees.select("name", (F.col("salary") * 2).alias("doubled"))

    An expression inside select is named with .alias. Without it the column
    comes out called (salary * 2).

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
+-----+---------+
| num | doubled |
+-----+---------+
| 42  | 10      |
| 1   | 6       |
+-----+---------+

Example 2:

Input:
counts:
+-----+--------+
| num | solves |
+-----+--------+
| 1   | 0      |
+-----+--------+
Output:
+-----+---------+
| num | doubled |
+-----+---------+
| 1   | 0       |
+-----+---------+

Constraints:

    1 <= number of rows <= 10^4
    0 <= solves <= 10^4

    REQUIRED: the output has exactly the two columns named, in that order,
    from one select; a column called (solves * 2) fails. NO withColumn then
    drop, NO withColumnRenamed, NO collect().

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

# assert sol.run(EXAMPLE_1) == [("1", 6), ("42", 10)]
# assert sol.run(EXAMPLE_2) == [("1", 0)]
