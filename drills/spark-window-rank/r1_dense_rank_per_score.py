"""
DRILL: Dense Rank Per Score
TRAINS: spark-window-rank

Given the DataFrame `scores`, return `score` and `rank` for every row,
ranked from highest `score` to lowest. Equal scores share a rank, and the
rank after a tie is the next consecutive integer: no holes. No ordering
required.

DataFrame: scores

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | score       | double  |
    +-------------+---------+
    id is unique.

Example 1:

Input:
scores:
+----+-------+
| id | score |
+----+-------+
| 1  | 3.5   |
| 2  | 3.65  |
| 3  | 4.0   |
| 4  | 3.85  |
| 5  | 4.0   |
| 6  | 3.65  |
+----+-------+
Output:
+-------+------+
| score | rank |
+-------+------+
| 4.0   | 1    |
| 4.0   | 1    |
| 3.85  | 2    |
| 3.65  | 3    |
| 3.65  | 3    |
| 3.5   | 4    |
+-------+------+
Explanation: 4.0 twice at rank 1, then 3.85 at rank 2, 3.65 twice at rank 3, 3.5 at rank 4.

Example 2:

Input:
scores:
+----+-------+
| id | score |
+----+-------+
| 1  | 7.0   |
| 2  | 7.0   |
| 3  | 7.0   |
+----+-------+
Output:
+-------+------+
| score | rank |
+-------+------+
| 7.0   | 1    |
| 7.0   | 1    |
| 7.0   | 1    |
+-------+------+
Explanation: all equal: everyone is rank 1.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: equal scores share a rank and the next rank is the next
    integer; a ranking that leaves holes after a tie (1, 1, 3) fails, and
    one that breaks ties (1, 2, 3) fails. NO collect().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import Window
from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, scores):
        pass


SCORES = "id int, score double"

EXAMPLE_1 = {
    "scores": (
        [
            (1, 3.5),
            (2, 3.65),
            (3, 4.0),
            (4, 3.85),
            (5, 4.0),
            (6, 3.65),
        ],
        SCORES,
    ),
}

EXAMPLE_2 = {
    "scores": (
        [
            (1, 7.0),
            (2, 7.0),
            (3, 7.0),
        ],
        SCORES,
    ),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(3.5, 4), (3.65, 3), (3.65, 3), (3.85, 2), (4.0, 1), (4.0, 1)]
# assert sol.run(EXAMPLE_2) == [(7.0, 1), (7.0, 1), (7.0, 1)]
