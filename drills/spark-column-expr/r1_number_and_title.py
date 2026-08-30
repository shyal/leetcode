"""
DRILL: Number And Title
TRAINS: spark-column-expr

Given the DataFrame `problems`, return `num` and `title` of every problem.
No ordering required.

DataFrame: problems

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | num         | string  |
    | title       | string  |
    | difficulty  | string  |
    +-------------+---------+
    num is unique.

Example 1:

Input:
problems:
+-----+---------------------+------------+
| num | title               | difficulty |
+-----+---------------------+------------+
| 42  | Trapping Rain Water | Hard       |
| 1   | Two Sum             | Easy       |
+-----+---------------------+------------+
Output:
+-----+---------------------+
| num | title               |
+-----+---------------------+
| 42  | Trapping Rain Water |
| 1   | Two Sum             |
+-----+---------------------+

Example 2:

Input:
problems:
+-----+---------+------------+
| num | title   | difficulty |
+-----+---------+------------+
| 1   | Two Sum | Easy       |
+-----+---------+------------+
Output:
+-----+---------+
| num | title   |
+-----+---------+
| 1   | Two Sum |
+-----+---------+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the output has exactly the two columns named, in that
    order. NO collect(), NO toPandas().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, problems):
        pass


PROBLEMS = "num string, title string, difficulty string"

EXAMPLE_1 = {
    "problems": (
        [
            ("42", "Trapping Rain Water", "Hard"),
            ("1", "Two Sum", "Easy"),
        ],
        PROBLEMS,
    ),
}

EXAMPLE_2 = {
    "problems": (
        [
            ("1", "Two Sum", "Easy"),
        ],
        PROBLEMS,
    ),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("1", "Two Sum"), ("42", "Trapping Rain Water")]
# assert sol.run(EXAMPLE_2) == [("1", "Two Sum")]
