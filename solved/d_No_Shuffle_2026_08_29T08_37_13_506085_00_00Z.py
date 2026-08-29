"""
DRILL: No Shuffle
TRAINS: spark-plan-shuffles

Given the DataFrame solves, return file and date for every solve whose
assist is 'none', with a third column points holding the integer 3. The
physical plan of the result must contain no Exchange. Any row order.

DataFrame: solves

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | date        | string  |
    | assist      | string  |
    +-------------+---------+
    file is unique.

Example 1:

Input:
solves:
+------+------------+--------+
| file | date       | assist |
+------+------------+--------+
| a.py | 2026-08-28 | none   |
| b.py | 2026-08-28 | hint   |
| c.py | 2026-08-29 | none   |
+------+------------+--------+
Output:
+------+------------+--------+
| file | date       | points |
+------+------------+--------+
| a.py | 2026-08-28 | 3      |
| c.py | 2026-08-29 | 3      |
+------+------------+--------+
Explanation: every step is row-local, so the plan is a single stage.

Example 2:

Input:
solves:
+------+------------+--------+
| file | date       | assist |
+------+------------+--------+
| a.py | 2026-08-28 | hint   |
+------+------------+--------+
Output: no rows.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: sol.plan(example) must not contain the word Exchange; every
    step must stay inside its partition. NO orderBy, NO distinct, NO
    dropDuplicates, NO repartition.

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.

---

Assisted for: .withColumn("points", F.lit(3))

"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill


class Solution(SparkDrill):

    engine = "jvm"  # this drill reads Spark's own plan

    def transform(self, solves):
        return (
            solves.filter(F.col("assist") == "none")
            .withColumn("points", F.lit(3))
            .select(["file", "date", "points"])
        )


SOLVES = "file string, date string, assist string"

EXAMPLE_1 = {
    "solves": (
        [
            ("a.py", "2026-08-28", "none"),
            ("b.py", "2026-08-28", "hint"),
            ("c.py", "2026-08-29", "none"),
        ],
        SOLVES,
    ),
}

EXAMPLE_2 = {
    "solves": (
        [
            ("a.py", "2026-08-28", "hint"),
        ],
        SOLVES,
    ),
}


sol = Solution()

sol.show(EXAMPLE_1)
print(sol.plan(EXAMPLE_1))

assert sol.run(EXAMPLE_1) == [("a.py", "2026-08-28", 3), ("c.py", "2026-08-29", 3)]
assert sol.run(EXAMPLE_2) == []
assert "Exchange" not in sol.plan(EXAMPLE_1)
