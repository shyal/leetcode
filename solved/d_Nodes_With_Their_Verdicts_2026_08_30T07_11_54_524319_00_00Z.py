"""
DRILL: Nodes With Their Verdicts
TRAINS: spark-join

Given the DataFrames `nodes` and `verdicts`, return `id` and `file` for
every verdict on every node, and one row with a null `file` for a node that
has no verdict. No ordering required.

DataFrame: nodes

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | string  |
    | name        | string  |
    +-------------+---------+
    id is unique.

DataFrame: verdicts

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | node_id     | string  |
    +-------------+---------+
    node_id is an id in nodes.

Example 1:

Input:
nodes:
+-----------------+-----------------+
| id              | name            |
+-----------------+-----------------+
| monotonic-stack | Monotonic stack |
| union-find      | Union find      |
+-----------------+-----------------+
verdicts:
+------+-----------------+
| file | node_id         |
+------+-----------------+
| a.py | monotonic-stack |
| b.py | monotonic-stack |
+------+-----------------+
Output:
+-----------------+------+
| id              | file |
+-----------------+------+
| monotonic-stack | a.py |
| monotonic-stack | b.py |
| union-find      | NULL |
+-----------------+------+
Explanation: union-find has no verdict and appears once, with a null file.

Example 2:

Input:
nodes:
+------------+------------+
| id         | name       |
+------------+------------+
| union-find | Union find |
+------------+------------+
verdicts: no rows.
Output:
+------------+------+
| id         | file |
+------------+------+
| union-find | NULL |
+------------+------+

Constraints:

    1 <= number of rows in nodes <= 10^4
    0 <= number of rows in verdicts <= 10^4

    REQUIRED: one join; every node survives, and a node without a verdict
    appears once with a null file. An inner join drops union-find and
    fails. NO union, NO collect().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, nodes, verdicts):
        return nodes.join(verdicts, nodes.id == verdicts.node_id, "left").select(
            ["id", "file"]
        )


NODES = "id string, name string"
VERDICTS = "file string, node_id string"

EXAMPLE_1 = {
    "nodes": (
        [
            ("monotonic-stack", "Monotonic stack"),
            ("union-find", "Union find"),
        ],
        NODES,
    ),
    "verdicts": (
        [
            ("a.py", "monotonic-stack"),
            ("b.py", "monotonic-stack"),
        ],
        VERDICTS,
    ),
}

EXAMPLE_2 = {
    "nodes": (
        [
            ("union-find", "Union find"),
        ],
        NODES,
    ),
    "verdicts": ([], VERDICTS),
}


sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [
    ("monotonic-stack", "a.py"),
    ("monotonic-stack", "b.py"),
    ("union-find", None),
]
assert sol.run(EXAMPLE_2) == [("union-find", None)]
