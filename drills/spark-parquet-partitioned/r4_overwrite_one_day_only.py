"""
DRILL: Overwrite One Day Only
TRAINS: spark-parquet-partitioned

Given the DataFrame `solves` and a `path`, write `solves` there as Parquet
laid out one directory per `date`, replacing every date present in `solves`
and leaving every other date already at `path` untouched. Running the same
write twice must leave the data as after one run. Return nothing.

Syntax:

    (orders.write.mode("overwrite")
           .option("partitionOverwriteMode", "dynamic")
           .partitionBy("day").parquet(path))

    mode("overwrite") alone deletes the whole path first. With
    partitionOverwriteMode dynamic it replaces only the directories the frame
    writes and leaves the others in place.

DataFrame: solves

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | file        | string  |
    | date        | string  |
    | problem     | string  |
    +-------------+---------+
    file is unique. date is YYYY-MM-DD.

Example 1:

Input: path is empty. Write
    (a.py, 2026-08-28, 1), (c.py, 2026-08-29, 1)
then write
    (d.py, 2026-08-29, 76)
Output: reading path back yields
+------+------------+---------+
| file | date       | problem |
+------+------------+---------+
| a.py | 2026-08-28 | 1       |
| d.py | 2026-08-29 | 76      |
+------+------------+---------+
Explanation: the second write replaced 2026-08-29 and left 2026-08-28.

Example 2:

Input: path is empty. Write (a.py, 2026-08-28, 1) twice.
Output: reading path back yields the one row, once.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: a date in solves is replaced, a date not in solves survives,
    and a rerun adds nothing. Appending fails the rerun; a plain overwrite
    deletes 2026-08-28 and fails Example 1. NO deleting directories from
    Python.

    Runner: local PySpark, adaptive execution and auto-broadcast off.
    The session's partitionOverwriteMode is the Spark default, static.
"""

from pyspark.sql import functions as F

from dsa.spark import SparkDrill, scratch_dir


class Solution(SparkDrill):

    engine = "jvm"  # dynamic partition overwrite needs real Spark

    def write(self, solves, path: str) -> None:
        pass


SOLVES = "file string, date string, problem string"


def after_writes(*batches):
    path = scratch_dir()
    spark = sol.spark
    for rows in batches:
        sol.write(spark.createDataFrame(rows, SOLVES), path)
    try:
        return sorted(tuple(r) for r in spark.read.parquet(path).collect())
    except Exception:
        return []


sol = Solution()

FIRST = [("a.py", "2026-08-28", "1"), ("c.py", "2026-08-29", "1")]
SECOND = [("d.py", "2026-08-29", "76")]

print(after_writes(FIRST, SECOND))

# assert after_writes(FIRST, SECOND) == [("a.py", "1", "2026-08-28"), ("d.py", "76", "2026-08-29")]
# assert after_writes(FIRST[:1], FIRST[:1]) == [("a.py", "1", "2026-08-28")]
