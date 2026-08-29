import atexit
import contextlib
import io
import os
import socket
import subprocess
import sys
import tempfile
import time

from pyspark.sql import DataFrame, SparkSession

# Two engines behind one PySpark API. "sail" is a Rust Spark Connect server
# spawned per run (about half a second); "jvm" is real Spark in a local JVM
# (about four seconds). A drill pins itself to the JVM when the point of the
# drill is Spark's own behaviour: its physical plan text, df.rdd partition
# counts, or dynamic partition overwrite, none of which Sail reproduces.
_sessions: dict[str, SparkSession] = {}


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _sail_binary() -> str | None:
    path = os.path.join(os.path.dirname(sys.executable), "sail")
    return path if os.path.exists(path) else None


def _sail_session() -> SparkSession:
    port = _free_port()
    proc = subprocess.Popen(
        [_sail_binary(), "spark", "server", "--port", str(port)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(200):
        try:
            socket.create_connection(("127.0.0.1", port), 0.05).close()
            break
        except OSError:
            time.sleep(0.02)
    spark = SparkSession.builder.remote(f"sc://localhost:{port}").getOrCreate()

    def stop():
        try:
            spark.stop()
        except Exception:
            pass
        finally:
            proc.kill()
            proc.wait(timeout=5)

    atexit.register(stop)
    return spark


def _jvm_session() -> SparkSession:
    os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
    log4j = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spark-log4j2.properties")
    spark = (
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
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def spark_session(engine: str = "sail") -> SparkSession:
    """One session per engine per process. Sail falls back to the JVM when
    the `sail` binary is not installed in the venv."""
    if engine == "sail" and _sail_binary() is None:
        engine = "jvm"
    if engine not in _sessions:
        _sessions[engine] = _sail_session() if engine == "sail" else _jvm_session()
    return _sessions[engine]


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
        sol.spark                       -> the session, for drills that read
                                           or write files

    `engine` is "sail" (default, fast) or "jvm" (real Spark). The JVM
    session is local[2] with adaptive execution and auto-broadcast OFF, so
    a plan shows exactly the shuffles and joins the code asked for.
    """

    engine = "sail"

    def transform(self, **frames) -> DataFrame:
        raise NotImplementedError

    @property
    def spark(self) -> SparkSession:
        return spark_session(self.engine)

    def frames(self, example: dict) -> dict:
        return {
            name: self.spark.createDataFrame(rows, schema)
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
