"""
DRILL: Reps Per Node, Zeros Included
TRAINS: spark-join, spark-group-agg

Given the DataFrames `nodes` and `verdicts`, return `id` and `reps` for
every node, where `reps` is the number of verdicts on that node. A node with
no verdict gets `reps` 0. No ordering required.

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
    node_id refers to nodes.id.

Example 1:

Input:
nodes:
+-----------------+-----------------+
| id              | name            |
+-----------------+-----------------+
| monotonic-stack | Monotonic stack |
| two-pointers    | Two pointers    |
| union-find      | Union find      |
+-----------------+-----------------+
verdicts:
+------+-----------------+
| file | node_id         |
+------+-----------------+
| a.py | monotonic-stack |
| b.py | monotonic-stack |
| c.py | two-pointers    |
+------+-----------------+
Output:
+-----------------+------+
| id              | reps |
+-----------------+------+
| monotonic-stack | 2    |
| two-pointers    | 1    |
| union-find      | 0    |
+-----------------+------+

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
| id         | reps |
+------------+------+
| union-find | 0    |
+------------+------+

Constraints:

    1 <= number of rows in nodes <= 10^4
    0 <= number of rows in verdicts <= 10^4

    REQUIRED: every node must survive the join, and an unmatched node must
    count as 0, not 1 and not null. NO union of a separate zero-rows frame,
    NO collect().

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.

---

Still new to .agg and .alias behaviour. Assisted.

"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    def transform(self, nodes, verdicts):
        return (
            nodes.join(verdicts, nodes.id == verdicts.node_id, "left")
            .groupBy("id")
            .agg(F.count(verdicts.node_id))
            .alias("resp")
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
            ("union-find", "Union find"),
        ],
        NODES,
    ),
    "verdicts": ([], VERDICTS),
}


sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [
    ("monotonic-stack", 2),
    ("two-pointers", 1),
    ("union-find", 0),
]
assert sol.run(EXAMPLE_2) == [("union-find", 0)]
