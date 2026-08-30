"""
DRILL: Hard And Unbanned
TRAINS: spark-column-expr

Given the DataFrame `problems`, return every row whose `difficulty` is
'Hard' and whose `banned` flag is 0. No ordering required.

Syntax:

    employees.filter((F.col("dept") == "sales") & (F.col("age") > 30))

    Conditions combine with & (and), | (or) and ~ (not), each condition in
    its own parentheses. Python's and, or and not do not work on Columns.

DataFrame: problems

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | num         | string  |
    | title       | string  |
    | difficulty  | string  |
    | banned      | int     |
    +-------------+---------+
    num is unique. difficulty is one of 'Easy', 'Medium', 'Hard'.
    banned is 0 or 1.

Example 1:

Input:
problems:
+-----+---------------------+------------+--------+
| num | title               | difficulty | banned |
+-----+---------------------+------------+--------+
| 42  | Trapping Rain Water | Hard       | 0      |
| 1   | Two Sum             | Easy       | 0      |
| 84  | Largest Rectangle   | Hard       | 1      |
| 76  | Minimum Window      | Hard       | 0      |
+-----+---------------------+------------+--------+
Output:
+-----+---------------------+------------+--------+
| num | title               | difficulty | banned |
+-----+---------------------+------------+--------+
| 42  | Trapping Rain Water | Hard       | 0      |
| 76  | Minimum Window      | Hard       | 0      |
+-----+---------------------+------------+--------+
Explanation: 84 is Hard but banned; 1 is not Hard.

Example 2:

Input:
problems:
+-----+---------+------------+--------+
| num | title   | difficulty | banned |
+-----+---------+------------+--------+
| 1   | Two Sum | Easy       | 0      |
+-----+---------+------------+--------+
Output: no rows.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: both conditions in one Column expression. Python and/or
    raises CANNOT_CONVERT_COLUMN_INTO_BOOL. NO collect(), NO toPandas().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, problems):
        pass


PROBLEMS = "num string, title string, difficulty string, banned int"

EXAMPLE_1 = {
    "problems": (
        [
            ("42", "Trapping Rain Water", "Hard", 0),
            ("1", "Two Sum", "Easy", 0),
            ("84", "Largest Rectangle", "Hard", 1),
            ("76", "Minimum Window", "Hard", 0),
        ],
        PROBLEMS,
    ),
}

EXAMPLE_2 = {
    "problems": (
        [
            ("1", "Two Sum", "Easy", 0),
        ],
        PROBLEMS,
    ),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("42", "Trapping Rain Water", "Hard", 0), ("76", "Minimum Window", "Hard", 0)]
# assert sol.run(EXAMPLE_2) == []
