"""
DRILL: One Shuffle
TRAINS: spark-plan-shuffles

Given the DataFrames `verdicts` and `nodes`, return `name` and `reps` for
every node that has at least one verdict, where `reps` is the number of
verdicts on that node. The physical plan of the result must contain exactly
one Exchange. No ordering required.

Syntax:

    big.join(F.broadcast(small), big["key"] == small["id"])

    F.broadcast copies the small frame whole to every task, so the join
    runs inside each partition and adds no Exchange. Without it Spark shuffles
    both sides.

DataFrame: verdicts

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | node_id     | string  |
    +-------------+---------+
    node_id refers to nodes.id. This is the big side: millions of rows in
    production.

DataFrame: nodes

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | string  |
    | name        | string  |
    +-------------+---------+
    id is unique. This is the small side: under a hundred rows.

Example 1:

Input:
verdicts:
+------+-----------------+
| file | node_id         |
+------+-----------------+
| a.py | monotonic-stack |
| b.py | monotonic-stack |
| c.py | two-pointers    |
+------+-----------------+
nodes:
+-----------------+-----------------+
| id              | name            |
+-----------------+-----------------+
| monotonic-stack | Monotonic stack |
| two-pointers    | Two pointers    |
| union-find      | Union find      |
+-----------------+-----------------+
Output:
+-----------------+------+
| name            | reps |
+-----------------+------+
| Monotonic stack | 2    |
| Two pointers    | 1    |
+-----------------+------+
Explanation: the count needs one shuffle; the lookup of names does not.

Example 2:

Input:
verdicts:
+------+--------------+
| file | node_id      |
+------+--------------+
| a.py | two-pointers |
+------+--------------+
nodes:
+--------------+--------------+
| id           | name         |
+--------------+--------------+
| two-pointers | Two pointers |
+--------------+--------------+
Output:
+--------------+------+
| name         | reps |
+--------------+------+
| Two pointers | 1    |
+--------------+------+

Constraints:

    1 <= number of rows in verdicts <= 10^7
    1 <= number of rows in nodes <= 100

    REQUIRED: sol.plan(example) must contain "Exchange hashpartitioning"
    exactly once and must not contain SortMergeJoin; auto-broadcast is off
    in the runner, so a join left to its default strategy adds two more and
    fails. NO collect() of nodes into a Python dict.

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    engine = "jvm"  # this drill reads Spark's own plan

    def transform(self, verdicts, nodes):
        pass


VERDICTS = "file string, node_id string"
NODES = "id string, name string"

EXAMPLE_1 = {
    "verdicts": ([
        ("a.py", "monotonic-stack"),
        ("b.py", "monotonic-stack"),
        ("c.py", "two-pointers"),
    ], VERDICTS),
    "nodes": ([
        ("monotonic-stack", "Monotonic stack"),
        ("two-pointers", "Two pointers"),
        ("union-find", "Union find"),
    ], NODES),
}

EXAMPLE_2 = {
    "verdicts": ([
        ("a.py", "two-pointers"),
    ], VERDICTS),
    "nodes": ([
        ("two-pointers", "Two pointers"),
    ], NODES),
}


sol = Solution()

sol.show(EXAMPLE_1)
print(sol.plan(EXAMPLE_1))

# assert sol.run(EXAMPLE_1) == [("Monotonic stack", 2), ("Two pointers", 1)]
# assert sol.run(EXAMPLE_2) == [("Two pointers", 1)]
# assert sol.plan(EXAMPLE_1).count("Exchange hashpartitioning") == 1
# assert "SortMergeJoin" not in sol.plan(EXAMPLE_1)
