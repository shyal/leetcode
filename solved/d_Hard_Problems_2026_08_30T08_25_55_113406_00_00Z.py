"""
DRILL: Hard Problems
TRAINS: spark-column-expr

Given the DataFrame `problems`, return every row whose `difficulty` is
'Hard'. No ordering required.

Syntax:

    employees.filter(F.col("dept") == "sales")

    F.col names a column. == on it builds a condition, which is itself a
    Column and holds no value yet. filter keeps the rows where it is true.

DataFrame: problems

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | num         | string  |
    | title       | string  |
    | difficulty  | string  |
    +-------------+---------+
    num is unique. difficulty is one of 'Easy', 'Medium', 'Hard'.

Example 1:

Input:
problems:
+-----+---------------------+------------+
| num | title               | difficulty |
+-----+---------------------+------------+
| 42  | Trapping Rain Water | Hard       |
| 1   | Two Sum             | Easy       |
| 76  | Minimum Window      | Hard       |
+-----+---------------------+------------+
Output:
+-----+---------------------+------------+
| num | title               | difficulty |
+-----+---------------------+------------+
| 42  | Trapping Rain Water | Hard       |
| 76  | Minimum Window      | Hard       |
+-----+---------------------+------------+

Example 2:

Input:
problems:
+-----+---------+------------+
| num | title   | difficulty |
+-----+---------+------------+
| 1   | Two Sum | Easy       |
+-----+---------+------------+
Output: no rows.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the condition is a Column expression. NO collect(), NO
    toPandas().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, problems):
        return problems.filter(F.col("difficulty") == "Hard")


PROBLEMS = "num string, title string, difficulty string"

EXAMPLE_1 = {
    "problems": (
        [
            ("42", "Trapping Rain Water", "Hard"),
            ("1", "Two Sum", "Easy"),
            ("76", "Minimum Window", "Hard"),
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

assert sol.run(EXAMPLE_1) == [
    ("42", "Trapping Rain Water", "Hard"),
    ("76", "Minimum Window", "Hard"),
]
assert sol.run(EXAMPLE_2) == []
