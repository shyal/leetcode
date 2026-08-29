"""
DRILL: Read One Day
TRAINS: spark-parquet-partitioned

Given a `path` holding solves as Parquet laid out one directory per `date`,
and a date string `day`, return `file` and `problem` for every solve on that
day while reading only that day's directory. No ordering required.

Layout under path:

    date=2026-08-28/part-....parquet
    date=2026-08-29/part-....parquet

    Each file has columns file (string) and problem (string); date is the
    directory name, not a column inside the file.

Example 1:

Input: path with the layout above, holding
    date=2026-08-28: (a.py, 1), (b.py, 42)
    date=2026-08-29: (c.py, 1), (d.py, 76)
day = "2026-08-29"
Output:
+------+---------+
| file | problem |
+------+---------+
| c.py | 1       |
| d.py | 76      |
+------+---------+
Explanation: sol.plan_for(path, day) shows PartitionFilters naming date;
the 2026-08-28 directory is never opened.

Example 2:

Input: the same path, day = "2026-08-30"
Output: no rows.

Constraints:

    1 <= number of directories <= 1000
    1 <= number of rows per directory <= 10^4

    REQUIRED: the plan must carry a PartitionFilters entry on date, so only
    one directory is scanned; the output must carry only file and problem.
    NO listing directories in Python, NO collect() then filter.

    Runner: local PySpark, adaptive execution and auto-broadcast off. Row
    order is not part of the answer.
"""

import contextlib
import io

from pyspark.sql import functions as F

from dsa.spark import SparkDrill, null_safe, scratch_dir


class Solution(SparkDrill):

    engine = "jvm"  # PartitionFilters is Spark's own plan text

    def read(self, path: str, day: str):
        pass

    def rows(self, path, day):
        df = self.read(path, day)
        return sorted((tuple(r) for r in df.collect()), key=null_safe) if df is not None else []

    def plan_for(self, path, day):
        df = self.read(path, day)
        if df is None:
            return ""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            df.explain()
        return out.getvalue()


def prepared_path():
    spark = sol.spark
    path = scratch_dir()
    rows = [("a.py", "2026-08-28", "1"), ("b.py", "2026-08-28", "42"),
            ("c.py", "2026-08-29", "1"), ("d.py", "2026-08-29", "76")]
    df = spark.createDataFrame(rows, "file string, date string, problem string")
    df.repartition("date").write.partitionBy("date").parquet(path)
    return path


sol = Solution()
PATH = prepared_path()

print(sol.rows(PATH, "2026-08-29"))
print(sol.plan_for(PATH, "2026-08-29"))

# assert sol.rows(PATH, "2026-08-29") == [("c.py", "1"), ("d.py", "76")]
# assert sol.rows(PATH, "2026-08-30") == []
# assert "PartitionFilters: [" in sol.plan_for(PATH, "2026-08-29") and "PartitionFilters: []" not in sol.plan_for(PATH, "2026-08-29")
