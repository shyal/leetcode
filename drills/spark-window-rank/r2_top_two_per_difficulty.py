"""
DRILL: Top Two Per Difficulty
TRAINS: spark-window-rank

Given the DataFrame counts, return num, difficulty and solves for the two
most solved problems of each difficulty. When two problems have the same
solves, the smaller num (compared as a string) ranks first. Any row order.

DataFrame: counts

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | num         | string  |
    | difficulty  | string  |
    | solves      | int     |
    +-------------+---------+
    num is unique.

Example 1:

Input:
counts:
+-----+------------+--------+
| num | difficulty | solves |
+-----+------------+--------+
| 1   | Easy       | 5      |
| 20  | Easy       | 2      |
| 26  | Easy       | 5      |
| 42  | Hard       | 3      |
| 76  | Hard       | 1      |
| 84  | Hard       | 3      |
+-----+------------+--------+
Output:
+-----+------------+--------+
| num | difficulty | solves |
+-----+------------+--------+
| 1   | Easy       | 5      |
| 26  | Easy       | 5      |
| 42  | Hard       | 3      |
| 84  | Hard       | 3      |
+-----+------------+--------+
Explanation: Easy keeps 1 and 26 (five solves each); Hard keeps 42 and 84.

Example 2:

Input:
counts:
+-----+------------+--------+
| num | difficulty | solves |
+-----+------------+--------+
| 42  | Hard       | 3      |
+-----+------------+--------+
Output:
+-----+------------+--------+
| num | difficulty | solves |
+-----+------------+--------+
| 42  | Hard       | 3      |
+-----+------------+--------+
Explanation: a difficulty with fewer than two problems returns what it has.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: at most two rows per difficulty, and the output must carry
    only the three columns named. A ranking that lets ties share a place
    returns three Easy rows on a three-way tie and fails. NO collect(),
    NO Python loop over difficulties.

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import Window
from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, counts):
        pass


COUNTS = "num string, difficulty string, solves int"

EXAMPLE_1 = {
    "counts": ([
        ("1", "Easy", 5),
        ("20", "Easy", 2),
        ("26", "Easy", 5),
        ("42", "Hard", 3),
        ("76", "Hard", 1),
        ("84", "Hard", 3),
    ], COUNTS),
}

EXAMPLE_2 = {
    "counts": ([
        ("42", "Hard", 3),
    ], COUNTS),
}

EXAMPLE_3 = {
    "counts": ([
        ("1", "Easy", 5),
        ("20", "Easy", 5),
        ("26", "Easy", 5),
    ], COUNTS),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("1", "Easy", 5), ("26", "Easy", 5), ("42", "Hard", 3), ("84", "Hard", 3)]
# assert sol.run(EXAMPLE_2) == [("42", "Hard", 3)]
# assert sol.run(EXAMPLE_3) == [("1", "Easy", 5), ("20", "Easy", 5)]
