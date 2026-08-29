"""
DRILL: Points Per Solve
TRAINS: spark-column-expr

Given the DataFrame `solves`, return every row with a new integer column
`points`: 3 when `assist` is 'none', 2 when 'hint', 1 when 'walkthrough',
and 0 for anything else. No ordering required.

DataFrame: solves

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | assist      | string  |
    +-------------+---------+
    file is unique. assist is any string or null.

Example 1:

Input:
solves:
+------+-------------+
| file | assist      |
+------+-------------+
| a.py | none        |
| b.py | hint        |
| c.py | walkthrough |
| d.py | spoiled     |
+------+-------------+
Output:
+------+-------------+--------+
| file | assist      | points |
+------+-------------+--------+
| a.py | none        | 3      |
| b.py | hint        | 2      |
| c.py | walkthrough | 1      |
| d.py | spoiled     | 0      |
+------+-------------+--------+

Example 2:

Input:
solves:
+------+--------+
| file | assist |
+------+--------+
| a.py | NULL   |
+------+--------+
Output:
+------+--------+--------+
| file | assist | points |
+------+--------+--------+
| a.py | NULL   | 0      |
+------+--------+--------+
Explanation: a null assist matches no branch and falls to 0.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: points must be one Column expression added in one call; a row
    that matches no branch must still get 0, not null. NO UDF, NO collect().

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
    "solves": ([
        ("a.py", "none"),
        ("b.py", "hint"),
        ("c.py", "walkthrough"),
        ("d.py", "spoiled"),
    ], SOLVES),
}

EXAMPLE_2 = {
    "solves": ([
        ("a.py", None),
    ], SOLVES),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("a.py", "none", 3), ("b.py", "hint", 2), ("c.py", "walkthrough", 1), ("d.py", "spoiled", 0)]
# assert sol.run(EXAMPLE_2) == [("a.py", None, 0)]
