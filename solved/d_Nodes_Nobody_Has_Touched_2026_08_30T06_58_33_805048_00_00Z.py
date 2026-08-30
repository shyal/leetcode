"""
DRILL: Nodes Nobody Has Touched
TRAINS: spark-join

Given the DataFrames `nodes` and `verdicts`, return `id` and `name` for
every node that has no verdict at all. No ordering required.

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
    node_id refers to nodes.id. A node can have many verdicts.

Example 1:

Input:
nodes:
+-----------------+------------------+
| id              | name             |
+-----------------+------------------+
| monotonic-stack | Monotonic stack  |
| two-pointers    | Two pointers     |
| union-find      | Union find       |
+-----------------+------------------+
verdicts:
+------+-----------------+
| file | node_id         |
+------+-----------------+
| a.py | monotonic-stack |
| b.py | monotonic-stack |
| c.py | two-pointers    |
+------+-----------------+
Output:
+------------+------------+
| id         | name       |
+------------+------------+
| union-find | Union find |
+------------+------------+

Example 2:

Input:
nodes:
+--------------+--------------+
| id           | name         |
+--------------+--------------+
| two-pointers | Two pointers |
+--------------+--------------+
verdicts:
+------+--------------+
| file | node_id      |
+------+--------------+
| a.py | two-pointers |
+------+--------------+
Output: no rows.

Constraints:

    1 <= number of rows in each DataFrame <= 10^4

    REQUIRED: one join whose output carries only the columns of nodes, one
    row per untouched node however many verdicts the others have. NO
    collect() of node ids into a Python list, NO distinct() to repair
    duplicates.

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.

---

New to left_anti. Assisted to add it as an argument to join.

"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, nodes, verdicts):
        return nodes.join(verdicts, nodes.id == verdicts.node_id, "left_anti").select(
            ["id", "name"]
        )


NODES = "id string, name string"
VERDICTS = "file string, node_id string"

EXAMPLE_1 = {
    "nodes": (
        [
            ("monotonic-stack", "Monotonic stack"),
            ("two-pointers", "Two pointers"),
            ("union-find", "Union find"),
        ],
        NODES,
    ),
    "verdicts": (
        [
            ("a.py", "monotonic-stack"),
            ("b.py", "monotonic-stack"),
            ("c.py", "two-pointers"),
        ],
        VERDICTS,
    ),
}

EXAMPLE_2 = {
    "nodes": (
        [
            ("two-pointers", "Two pointers"),
        ],
        NODES,
    ),
    "verdicts": (
        [
            ("a.py", "two-pointers"),
        ],
        VERDICTS,
    ),
}


sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [("union-find", "Union find")]
assert sol.run(EXAMPLE_2) == []
