"""tabulate with no headers prints a grid with index headers and row labels."""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.join(os.path.dirname(HERE), "harness")


def _load():
    spec = importlib.util.spec_from_file_location(
        "sc", os.path.join(HARNESS, "sitecustomize.py")
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _rows(sc, *args, **kwargs):
    from rich.console import Console

    con = Console(width=80, record=True, file=open(os.devnull, "w"))
    sc.console = con
    sc.tabulate(*args, **kwargs)
    text = con.export_text()
    return [line.strip() for line in text.splitlines() if "│" in line or "┃" in line]


def test_bare_grid_gets_index_headers_and_row_labels():
    sc = _load()
    rows = _rows(sc, [[1, 0, 2], [3, 1, 4]])
    assert rows[0].replace(" ", "") == "┃┃0┃1┃2┃"
    assert rows[1].replace(" ", "") == "│0│1│0│2│"
    assert rows[2].replace(" ", "") == "│1│3│1│4│"


def test_flat_list_is_one_row():
    sc = _load()
    rows = _rows(sc, [1, 0, 2])
    assert rows[0].replace(" ", "") == "┃┃0┃1┃2┃"
    assert rows[1].replace(" ", "") == "│0│1│0│2│"


def test_explicit_headers_unchanged():
    sc = _load()
    rows = _rows(sc, [[1, 0], [3, 1]], headers="ab", row_labels="xy")
    assert rows[0].replace(" ", "") == "┃┃a┃b┃"
    assert rows[1].replace(" ", "") == "│x│1│0│"


def test_pprint_picks_a_drawer_per_kind():
    sc = _load()
    assert sc._drawer_for(sc.build_linked_list([1, 2])) is sc.draw_linked_list
    assert sc._drawer_for(sc.build_tree([1, 2, 3])) is sc.draw_tree
    assert sc._drawer_for({0: [1], 1: []}) is sc.draw_ascii_graph
    assert sc._drawer_for([[0, 1], [1, 0]]) is sc.tabulate
    assert sc._drawer_for([[1, 2], [2], []]) is not sc.tabulate
    assert sc._drawer_for(sc.build_graph([[2], [1]])) is not None
    for plain in (3, "s", [1, 2, 3], {"a": 1}, {}, [], [[1], [[2]]]):
        assert sc._drawer_for(plain) is None, plain


def _capture(sc):
    from rich.console import Console

    con = Console(width=80, record=True, file=open(os.devnull, "w"))
    sc.console = con
    return con


def test_pprint_plain_args_keep_sep_and_end():
    sc = _load()
    con = _capture(sc)
    sc.pprint("x", 1, sep="-", end="!\n")
    sc.pprint()
    assert con.export_text() == "x-1!\n\n"


def test_pprint_draws_and_keeps_plain_neighbours():
    sc = _load()
    con = _capture(sc)
    sc.pprint("dp", [[1, 2]], "done")
    out = con.export_text()
    assert out.startswith("dp\n")
    assert out.endswith("done\n")
    assert "│" in out


def test_pretty_print_env_overrides_print():
    import subprocess
    import sys

    code = "print([[1, 2], [3, 4]]); print(print is pprint, print_orig is not print)"
    for env, expect in (("1", "True True"), ("0", "False False")):
        out = subprocess.run(
            [sys.executable, "-c", code],
            env={**os.environ, "PRETTY_PRINT": env},
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        assert expect in out, (env, out)
