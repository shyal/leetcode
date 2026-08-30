"""
DRILL: Clean Rate Per Node
TRAINS: spark-group-agg, spark-column-expr

Given the DataFrame `verdicts`, return one row per `node_id` with the
fraction of its verdicts equal to 'clean', in the `clean_rate` column. A
node with no clean verdict shows 0.0. No ordering required.

DataFrame: verdicts

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | node_id     | string  |
    | verdict     | string  |
    +-------------+---------+
    verdict is one of 'clean', 'struggled', 'avoided'.

Example 1:

Input:
verdicts:
+------+-----------------+-----------+
| file | node_id         | verdict   |
+------+-----------------+-----------+
| a.py | monotonic-stack | clean     |
| b.py | monotonic-stack | struggled |
| c.py | monotonic-stack | clean     |
| d.py | monotonic-stack | avoided   |
| e.py | two-pointers    | avoided   |
+------+-----------------+-----------+
Output:
+-----------------+------------+
| node_id         | clean_rate |
+-----------------+------------+
| monotonic-stack | 0.5        |
| two-pointers    | 0.0        |
+-----------------+------------+
Explanation: monotonic-stack has two clean verdicts out of four.

Example 2:

Input:
verdicts:
+------+--------------+---------+
| file | node_id      | verdict |
+------+--------------+---------+
| a.py | two-pointers | clean   |
+------+--------------+---------+
Output:
+--------------+------------+
| node_id      | clean_rate |
+--------------+------------+
| two-pointers | 1.0        |
+--------------+------------+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one groupBy and one agg over all rows; a node with no clean
    verdict shows 0.0. NO filter to clean rows first, NO join of two
    aggregates, NO collect().

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
    "verdicts": (
        [
            ("a.py", "monotonic-stack", "clean"),
            ("b.py", "monotonic-stack", "struggled"),
            ("c.py", "monotonic-stack", "clean"),
            ("d.py", "monotonic-stack", "avoided"),
            ("e.py", "two-pointers", "avoided"),
        ],
        VERDICTS,
    ),
}

EXAMPLE_2 = {
    "verdicts": (
        [
            ("a.py", "two-pointers", "clean"),
        ],
        VERDICTS,
    ),
}


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [("monotonic-stack", 0.5), ("two-pointers", 0.0)]
# assert sol.run(EXAMPLE_2) == [("two-pointers", 1.0)]
