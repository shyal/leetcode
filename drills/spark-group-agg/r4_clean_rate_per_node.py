"""
DRILL: Clean Rate Per Node
TRAINS: spark-group-agg

Given the DataFrame `verdicts`, return one row per `node_id` with the
number of verdicts in the `reps` column and the fraction of those verdicts
equal to 'clean', rounded to two decimals, in the `clean_rate` column. No
ordering required.

DataFrame: verdicts

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | node_id     | string  |
    | verdict     | string  |
    +-------------+---------+
    (file, node_id) is unique. verdict is 'clean', 'struggled' or 'avoided'.

Example 1:

Input:
verdicts:
+------+-----------------+-----------+
| file | node_id         | verdict   |
+------+-----------------+-----------+
| a.py | monotonic-stack | clean     |
| b.py | monotonic-stack | struggled |
| c.py | monotonic-stack | clean     |
| c.py | two-pointers    | avoided   |
+------+-----------------+-----------+
Output:
+-----------------+------+------------+
| node_id         | reps | clean_rate |
+-----------------+------+------------+
| monotonic-stack | 3    | 0.67       |
| two-pointers    | 1    | 0.0        |
+-----------------+------+------------+
Explanation: monotonic-stack has two clean verdicts out of three.

Example 2:

Input:
verdicts:
+------+--------------+---------+
| file | node_id      | verdict |
+------+--------------+---------+
| a.py | two-pointers | clean   |
+------+--------------+---------+
Output:
+--------------+------+------------+
| node_id      | reps | clean_rate |
+--------------+------+------------+
| two-pointers | 1    | 1.0        |
+--------------+------+------------+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: both numbers must come out of one groupBy and one agg over the
    rows as they are; a node with no clean verdict must still appear with
    0.0. NO filtering to clean rows first, NO join of two aggregates.

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, verdicts):
        pass


VERDICTS = "file string, node_id string, verdict string"

EXAMPLE_1 = {
    "verdicts": ([
        ("a.py", "monotonic-stack", "clean"),
        ("b.py", "monotonic-stack", "struggled"),
        ("c.py", "monotonic-stack", "clean"),
        ("c.py", "two-pointers", "avoided"),
    ], VERDICTS),
}

EXAMPLE_2 = {
    "verdicts": ([
        ("a.py", "two-pointers", "clean"),
    ], VERDICTS),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("monotonic-stack", 3, 0.67), ("two-pointers", 1, 0.0)]
# assert sol.run(EXAMPLE_2) == [("two-pointers", 1, 1.0)]
