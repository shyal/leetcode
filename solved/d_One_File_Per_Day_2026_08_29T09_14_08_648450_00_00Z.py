"""
DRILL: One File Per Day
TRAINS: spark-parquet-partitioned

Given the DataFrame solves and an empty directory path, write solves there
as Parquet laid out one directory per date, with exactly one data file in
each directory. Return nothing.

DataFrame: solves

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | date        | string  |
    | problem     | string  |
    +-------------+---------+
    file is unique. date is YYYY-MM-DD. The frame arrives in two
    partitions with rows of one date spread across both.

Example 1:

Input:
solves:
+------+------------+---------+
| file | date       | problem |
+------+------------+---------+
| a.py | 2026-08-28 | 1       |
| c.py | 2026-08-29 | 1       |
| b.py | 2026-08-28 | 42      |
| d.py | 2026-08-29 | 76      |
+------+------------+---------+
Output: under path,
    date=2026-08-28/<one>.parquet
    date=2026-08-29/<one>.parquet
and reading path back yields the four rows.

Example 2:

Input:
solves:
+------+------------+---------+
| file | date       | problem |
+------+------------+---------+
| a.py | 2026-08-29 | 1       |
+------+------------+---------+
Output: under path, date=2026-08-29/<one>.parquet.

Constraints:

    1 <= number of rows <= 10^4
    1 <= number of distinct dates <= 100

    REQUIRED: one directory per date and exactly one .parquet file inside
    each; writing straight from the two input partitions produces two
    files per date and fails. NO collect(), NO Python file writing.

    Runner: local PySpark, adaptive execution and auto-broadcast off.
    dsa.spark.tree(path) lists the files written, relative to path.

---

New to parquet writes. Assisted.

"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill, scratch_dir, tree


class Solution(SparkDrill):

    engine = "jvm"  # two input partitions per date needs real Spark

    def write(self, solves, path: str) -> None:

        solves.repartition("date").write.partitionBy("date").parquet(path)


SOLVES = "file string, date string, problem string"

EXAMPLE_1 = {
    "solves": (
        [
            ("a.py", "2026-08-28", "1"),
            ("c.py", "2026-08-29", "1"),
            ("b.py", "2026-08-28", "42"),
            ("d.py", "2026-08-29", "76"),
        ],
        SOLVES,
    ),
}

EXAMPLE_2 = {
    "solves": (
        [
            ("a.py", "2026-08-29", "1"),
        ],
        SOLVES,
    ),
}


def layout(example):
    path = scratch_dir()
    sol.write(sol.frames(example)["solves"], path)
    files = tree(path)
    if not files:
        return [], []
    rows = sorted(tuple(r) for r in sol.spark.read.parquet(path).collect())
    return files, rows


sol = Solution()

files, rows = layout(EXAMPLE_1)
print("\n".join(files) or "(nothing written)")

files, rows = layout(EXAMPLE_1)
assert [f.split("/")[0] for f in files] == ["date=2026-08-28", "date=2026-08-29"]
assert all(f.endswith(".parquet") for f in files)
assert rows == [
    ("a.py", "1", "2026-08-28"),
    ("b.py", "42", "2026-08-28"),
    ("c.py", "1", "2026-08-29"),
    ("d.py", "76", "2026-08-29"),
]
files, rows = layout(EXAMPLE_2)
assert [f.split("/")[0] for f in files] == ["date=2026-08-29"]
