# Layout guards for utils/: every command the makefile (and the tooling itself)
# points at exists where it says, every script still imports after the move
# into subfolders, and the path constants they derive from __file__ still land
# on real directories. Cheap import tests, so a future move breaks loudly here
# rather than in the middle of `make solved`.
import ast
import glob
import os
import re
import subprocess
import sys
from importlib.machinery import SourceFileLoader

import pytest

TESTS = os.path.dirname(os.path.abspath(__file__))
UTILS = os.path.dirname(TESTS)
ROOT = os.path.dirname(UTILS)
KG = os.path.join(UTILS, "kg")
README = os.path.join(UTILS, "readme")
HISTORY = os.path.join(UTILS, "history")
HARNESS = os.path.join(UTILS, "harness")
VENV_PY = os.path.join(ROOT, ".venv", "bin", "python3")
PY = VENV_PY if os.path.exists(VENV_PY) else sys.executable


def _scripts(d):
    return sorted(
        f
        for f in os.listdir(d)
        if os.path.isfile(os.path.join(d, f))
        and not f.startswith("__")
        and not f.endswith((".txt", ".pyc"))
    )


def _has_main_guard(path):
    src = open(path).read()
    return '__name__ == "__main__"' in src or "__name__ == '__main__'" in src


# --- the makefile only names files that exist ------------------------------


def test_makefile_paths_exist():
    """Every utils/ path the makefile names exists, except cargo build
    outputs under target/, which the makefile builds itself and a fresh
    checkout (CI) does not have."""
    text = open(os.path.join(ROOT, "makefile")).read()
    missing = sorted(
        {
            p
            for p in re.findall(r"utils/[\w./-]+", text)
            if "/target/" not in p
            and not os.path.exists(os.path.join(ROOT, p.rstrip("/")))
        }
    )
    assert missing == [], f"makefile points at files that do not exist: {missing}"


def test_tooling_paths_exist():
    """Scripts that spawn each other name the target by a utils/... path."""
    seen = set()
    for d in (KG, README, HISTORY, HARNESS):
        for f in _scripts(d):
            for line in open(os.path.join(d, f)):
                if line.lstrip().startswith("#"):
                    continue
                for p in re.findall(r"[\"']utils/([\w./-]+)[\"']", line):
                    seen.add(p)
    missing = sorted(
        p for p in seen if not os.path.exists(os.path.join(ROOT, "utils", p))
    )
    assert seen, "expected at least one cross-script utils/ path (kg_force -> prepare)"
    assert missing == [], f"scripts point at utils/ files that do not exist: {missing}"


def test_rs_bin_names_are_crates():
    """Every Rust binary a script runs through kg_lib.rs_bin("...") is a
    crate of the utils/rs workspace (the binary is named after its crate)."""
    rs = os.path.join(UTILS, "rs")
    names = set()
    for d in (KG, README, HISTORY):
        for f in _scripts(d):
            names |= set(
                re.findall(r'rs_bin\("([\w-]+)"\)', open(os.path.join(d, f)).read())
            )
    assert {"kg_chat", "is_session_start"} <= names
    missing = sorted(
        n for n in names if not os.path.exists(os.path.join(rs, n, "Cargo.toml"))
    )
    assert missing == [], missing


# --- every tooling script still imports ------------------------------------

_KG_MODULES = [
    f for f in _scripts(KG) if _has_main_guard(os.path.join(KG, f)) or f.endswith(".py")
]


@pytest.mark.parametrize("name", _KG_MODULES)
def test_kg_script_loads(name):
    path = os.path.join(KG, name)
    if name.endswith(".py"):
        mod = __import__(f"kg.{name[:-3]}", fromlist=["_"])
    else:
        mod = SourceFileLoader(f"_layout_{name}", path).load_module()
    # __file__-derived roots must point at real directories after the move
    for attr in ("REPO_ROOT", "GRAPH_DIR", "DRILLS_DIR", "UTILS", "UTILS_DIR", "ROOT"):
        if hasattr(mod, attr):
            assert os.path.isdir(
                getattr(mod, attr)
            ), f"{name}.{attr} = {getattr(mod, attr)}"


def test_kg_lib_roots():
    from kg import kg_lib

    assert kg_lib.REPO_ROOT == ROOT
    assert kg_lib.UTILS_DIR == UTILS
    assert kg_lib.GRAPH_DIR == os.path.join(ROOT, "graph")
    assert kg_lib.DRILLS_DIR == os.path.join(ROOT, "drills")
    assert os.path.isfile(kg_lib.SITECUSTOMIZE)
    assert (
        kg_lib.sitecustomize_names()
    ), "builtin names are read from sitecustomize.py; empty means the path is wrong"


@pytest.mark.parametrize(
    "name",
    [
        f
        for f in _scripts(README)
        if _has_main_guard(os.path.join(README, f)) or f.endswith(".py")
    ],
)
def test_readme_script_loads(name):
    path = os.path.join(README, name)
    if name.endswith(".py"):
        __import__(f"readme.{name[:-3]}", fromlist=["_"])
    else:
        SourceFileLoader(f"_layout_{name}", path).load_module()


@pytest.mark.parametrize("name", ["history_builder", "metadata", "solve_rate"])
def test_history_module_loads(name):
    __import__(f"history.{name}", fromlist=["_"])


def test_mock_binary_paths_agree():
    """solve_rate and the tests must point at the workspace's kg_mock."""
    from history import solve_rate  # noqa: F401

    rs = os.path.join(UTILS, "rs")
    # one line or one segment per line, whichever way black laid it out
    src = re.sub(r"\s+", " ", open(os.path.join(HISTORY, "solve_rate.py")).read())
    assert '"rs", "target", "release", "kg_mock"' in src
    # every crate directory is a workspace member, so one build makes them all
    crates = sorted(
        d for d in os.listdir(rs) if os.path.exists(os.path.join(rs, d, "Cargo.toml"))
    )
    members = re.search(
        r"members = \[([^\]]*)\]", open(os.path.join(rs, "Cargo.toml")).read()
    )
    assert members, "utils/rs/Cargo.toml has no [workspace] members list"
    assert sorted(re.findall(r'"([^"]+)"', members.group(1))) == crates
    assert {
        "kg",
        "kg_mock",
        "kg_movie",
        "kg_next",
        "kg_rep",
        "kg_status",
        "estimate",
        "kg_predict",
        "kg_sleep",
        "kg_mirror",
        "kg_solved",
        "drill",
        "kg_force",
        "timer",
        "kg_curve",
        "kg_solvecost",
    } <= set(crates)


# --- the harness stays a flat namespace (what solves import) --------------

HARNESS_MODULES = [
    "Types",
    "TreeFormatter",
    "tree_utils",
    "bst_utils",
    "linked_list_utils",
    "graph_utils",
    "bs_utils",
    "debug_utils",
    "heap_utils",
]


@pytest.mark.parametrize("name", HARNESS_MODULES)
def test_harness_module_importable_flat(name):
    __import__(name)


def test_harness_modules_all_present():
    on_disk = {f[:-3] for f in os.listdir(HARNESS) if f.endswith(".py")}
    assert set(HARNESS_MODULES) <= on_disk, sorted(set(HARNESS_MODULES) - on_disk)


def test_solve_sees_harness_like_kg_extract_runs_it():
    """kg_extract.run_solve executes a solve with PYTHONPATH=root:utils:utils/harness;
    a solve that says `from Types import TreeNode` must still resolve."""
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([ROOT, UTILS, HARNESS])
    code = (
        "from Types import TreeNode, ListNode\n"
        "from tree_utils import build_tree\n"
        "from kg import kg_lib\n"
        "print(build_tree([1, 2, 3]).left.val)\n"
    )
    r = subprocess.run(
        [PY, "-c", code], env=env, cwd=ROOT, capture_output=True, text=True, timeout=60
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "2"


def test_sitecustomize_puts_harness_and_utils_on_path():
    """The venv copy of sitecustomize (installed by `make all`) is what every
    solve relies on; it must insert utils/ and utils/harness from its
    site-packages location."""
    src = open(os.path.join(HARNESS, "sitecustomize.py")).read()
    assert 'os.path.join(project_root, "utils", "harness")' in src
    assert 'os.path.join(project_root, "utils")' in src
    installed = os.path.join(
        ROOT, ".venv", "lib", "python3.10", "site-packages", "sitecustomize.py"
    )
    if os.path.exists(installed):
        assert (
            open(installed).read() == src
        ), "venv sitecustomize is stale: run `make all`"


def test_no_stray_files_at_utils_top_level():
    """Everything lives in a subfolder now; a new file dropped at utils/ is a
    regression of the layout, not a convention."""
    stray = sorted(
        f for f in os.listdir(UTILS) if os.path.isfile(os.path.join(UTILS, f))
    )
    assert stray == [], stray


def test_attic_is_not_imported_anywhere():
    """Retired scripts are kept for reference only."""
    attic = os.path.join(UTILS, "attic")
    names = {f.split(".")[0] for f in os.listdir(attic)}
    offenders = []
    for d in (KG, README, HISTORY, HARNESS, TESTS):
        for f in _scripts(d):
            if f == os.path.basename(__file__):
                continue
            src = open(os.path.join(d, f)).read()
            try:
                tree = ast.parse(src)
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.ImportFrom)
                    and node.module
                    and node.module.split(".")[-1] in names
                ):
                    offenders.append(f"{f}: from {node.module}")
                if isinstance(node, ast.Import) and any(
                    a.name.split(".")[-1] in names for a in node.names
                ):
                    offenders.append(f"{f}: import")
    assert offenders == [], offenders


# --------------------------------------------------------------------------
# the drill bank's house rules (2026-09-02)
# --------------------------------------------------------------------------

DRILLS = os.path.join(ROOT, "drills")
_DRILL_FILES = sorted(glob.glob(os.path.join(DRILLS, "*", "*.py")))


@pytest.mark.parametrize("path", _DRILL_FILES, ids=lambda p: os.path.relpath(p, DRILLS))
def test_drill_imports_nothing_sitecustomize_provides(path):
    """sitecustomize mirrors LeetCode's preloaded names (List, Callable,
    defaultdict, ...). A drill never imports one of them: the operator
    would not type the import on LeetCode, so it is noise in the rep."""
    from kg import kg_lib

    names = set(kg_lib.sitecustomize_names())
    for node in ast.walk(ast.parse(open(path).read())):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            dup = [
                a.asname or a.name for a in node.names if (a.asname or a.name) in names
            ]
            assert (
                not dup
            ), f"{os.path.relpath(path, ROOT)} imports {dup}; sitecustomize already provides them"


@pytest.mark.parametrize("path", _DRILL_FILES, ids=lambda p: os.path.relpath(p, DRILLS))
def test_drill_asserts_uncomment_in_one_swoop(path):
    """From the Solution instantiation down, stripping one '#' from every
    comment line must leave code that parses: the operator toggles the
    whole block at once, so a prose line there carries '##' and stays a
    comment after the toggle."""
    src = open(path).read()
    m = re.search(r"^\w+ = Solution\(", src, re.M)
    assert m, f"{os.path.relpath(path, ROOT)}: no `sol = Solution(...)` line"
    lines = src[m.start() :].split("\n")
    block = "\n".join(
        l[2:] if l.startswith("# ") else l[1:] if l.startswith("#") else l
        for l in lines
    )
    compile(block, path, "exec")


# --- the gates see what runs --------------------------------------------------


def test_ruff_builtins_match_sitecustomize():
    """pyproject's ruff builtins list is the names sitecustomize injects; ruff
    cannot read them at run time, so the copy is pinned here."""
    import tomli as tomllib

    from kg import kg_lib

    with open(os.path.join(ROOT, "pyproject.toml"), "rb") as f:
        cfg = tomllib.load(f)
    assert cfg["tool"]["ruff"]["builtins"] == kg_lib.sitecustomize_names()


def test_check_scripts_cover_the_tooling():
    """utils/check/pyfiles lists every tooling script the makefile runs."""
    listed = set(
        subprocess.run(
            [os.path.join(UTILS, "check", "pyfiles")],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.split()
    )
    for d, name in (("kg", "kg_next"), ("kg", "kg_lib.py"), ("readme", "kg_full_svg")):
        assert f"utils/{d}/{name}" in listed
    assert "utils/harness/sitecustomize.py" in listed
    assert not any(f.startswith(("solved/", "drills/", "utils/attic/")) for f in listed)
