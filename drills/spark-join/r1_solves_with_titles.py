"""
DRILL: Solves With Titles
TRAINS: spark-join

Given the DataFrames `solves` and `problems`, return `file`, `title` and
`difficulty` for every solve whose `problem` exists in `problems`. No
ordering required.

DataFrame: solves

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | problem     | string  |
    +-------------+---------+
    file is unique. problem refers to problems.num.

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
solves:
+------+---------+
| file | problem |
+------+---------+
| a.py | 1       |
| b.py | 42      |
| c.py | 1       |
| d.py | 999     |
+------+---------+
problems:
+-----+---------------------+------------+
| num | title               | difficulty |
+-----+---------------------+------------+
| 1   | Two Sum             | Easy       |
| 42  | Trapping Rain Water | Hard       |
+-----+---------------------+------------+
Output:
+------+---------------------+------------+
| file | title               | difficulty |
+------+---------------------+------------+
| a.py | Two Sum             | Easy       |
| b.py | Trapping Rain Water | Hard       |
| c.py | Two Sum             | Easy       |
+------+---------------------+------------+
Explanation: d.py points at 999, which is not in problems, so it vanishes.

Example 2:

Input:
solves:
+------+---------+
| file | problem |
+------+---------+
| a.py | 7       |
+------+---------+
problems:
+-----+---------+------------+
| num | title   | difficulty |
+-----+---------+------------+
| 1   | Two Sum | Easy       |
+-----+---------+------------+
Output: no rows.

Constraints:

    1 <= number of rows in each DataFrame <= 10^4

    REQUIRED: one join on the two differently named keys, and the output
    has exactly the three columns named, neither key included.
    NO renaming a key column before the join, NO collect().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, solves, problems):
        pass


SOLVES = "file string, problem string"
PROBLEMS = "num string, title string, difficulty string"

EXAMPLE_1 = {
    "solves": ([
        ("a.py", "1"),
        ("b.py", "42"),
        ("c.py", "1"),
        ("d.py", "999"),
    ], SOLVES),
    "problems": ([
        ("1", "Two Sum", "Easy"),
        ("42", "Trapping Rain Water", "Hard"),
    ], PROBLEMS),
}

EXAMPLE_2 = {
    "solves": ([
        ("a.py", "7"),
    ], SOLVES),
    "problems": ([
        ("1", "Two Sum", "Easy"),
    ], PROBLEMS),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("a.py", "Two Sum", "Easy"), ("b.py", "Trapping Rain Water", "Hard"), ("c.py", "Two Sum", "Easy")]
# assert sol.run(EXAMPLE_2) == []
