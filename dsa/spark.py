import contextlib
import io
import os
import tempfile

from pyspark.sql import DataFrame, SparkSession

_spark = None


def spark_session() -> SparkSession:
    """One local session per process; the first call costs a few seconds."""
    global _spark
    if _spark is None:
        os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
        log4j = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spark-log4j2.properties")
        _spark = (
            SparkSession.builder.master("local[2]")
            .appName("drill")
            .config("spark.ui.enabled", "false")
            .config("spark.ui.showConsoleProgress", "false")
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.sql.adaptive.enabled", "false")
            .config("spark.sql.autoBroadcastJoinThreshold", "-1")
            .config("spark.sql.sources.partitionColumnTypeInference.enabled", "false")
            .config("spark.driver.extraJavaOptions", f"-Dlog4j2.configurationFile=file:{log4j}")
            .getOrCreate()
        )
        _spark.sparkContext.setLogLevel("ERROR")
    return _spark


def null_safe(row):
    """Sort key that never compares NULL with a value."""
    return [(v is None, v) for v in row]


class SparkDrill:
    """Base for PySpark drills: subclass, write `transform(...)`, done.

    An example is a dict of frame name -> (rows, schema string); the frames
    are built and passed to `transform` as keyword arguments. `transform`
    returns a DataFrame.

        sol.run(example)                -> row tuples, sorted (row order is
                                           not part of the drill)
        sol.run(example, ordered=True)  -> row tuples in engine order, for a
                                           drill where orderBy is the move
        sol.show(example)               -> prints the result as a +---+ table
        sol.plan(example)               -> the physical plan as a string
        sol.result(example)             -> the DataFrame itself
        sol.frames(example)             -> the input DataFrames, by name

    The session is local[2] with adaptive execution and auto-broadcast OFF,
    so a plan shows exactly the shuffles and joins the code asked for.
    """

    def transform(self, **frames) -> DataFrame:
        raise NotImplementedError

    def frames(self, example: dict) -> dict:
        spark = spark_session()
        return {
            name: spark.createDataFrame(rows, schema)
            for name, (rows, schema) in example.items()
        }

    def result(self, example: dict):
        return self.transform(**self.frames(example))

    def _result(self, example: dict):
        try:
            return self.result(example)
        except NotImplementedError:
            return None

    def run(self, example: dict, ordered: bool = False) -> list[tuple]:
        df = self._result(example)
        if df is None:
            return []
        rows = [tuple(r) for r in df.collect()]
        return rows if ordered else sorted(rows, key=null_safe)

    def show(self, example: dict) -> None:
        df = self._result(example)
        if df is None:
            print("(no transform yet)")
            return
        df.show(truncate=False)

    def plan(self, example: dict) -> str:
        df = self._result(example)
        if df is None:
            return ""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            df.explain()
        return out.getvalue()


def scratch_dir() -> str:
    """A fresh path that does not exist yet, for a drill that writes files."""
    return os.path.join(tempfile.mkdtemp(prefix="spark-drill-"), "out")


def tree(path: str) -> list[str]:
    """Relative paths of every non-hidden file under `path`, sorted."""
    out = []
    for root, dirs, files in os.walk(path):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for f in files:
            if f.startswith(".") or f.startswith("_"):
                continue
            out.append(os.path.relpath(os.path.join(root, f), path))
    return sorted(out)
