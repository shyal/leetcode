import math
import os
from datetime import date, timedelta
from importlib.machinery import SourceFileLoader

README = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "readme"
)
kg_progress = SourceFileLoader(
    "kg_progress_svg", os.path.join(README, "kg_progress_svg")
).load_module()


def test_windows_mean_residual_and_its_error():
    """A window's residual is the mean of actual minus model over its last n
    games, its standard error the model's own: sqrt(sum p(1-p)) / n."""
    d0 = date(2026, 1, 1)
    rows = [(d0 + timedelta(days=i), float(i % 2), 0.5) for i in range(5)]
    win = kg_progress.windows(rows, n=4)
    assert [w[0] for w in win] == [rows[3][0], rows[4][0]]
    # games 0..3 score 0,1,0,1 against 0.5 each: residual 0; games 1..4
    # score 1,0,1,0: residual 0 too; the error is sqrt(4 * 0.25) / 4
    assert [round(w[1], 9) for w in win] == [0.0, 0.0]
    assert all(math.isclose(w[2], 0.25) for w in win)
    assert kg_progress.windows(rows[:3], n=4) == []


def test_runs_split_at_a_month():
    d0 = date(2026, 1, 1)
    series = [
        (d0, 0, 0),
        (d0 + timedelta(days=10), 0, 0),
        (d0 + timedelta(days=50), 0, 0),
    ]
    assert [len(r) for r in kg_progress.runs(series)] == [2, 1]
