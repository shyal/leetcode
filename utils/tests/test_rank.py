"""kg_rank_svg: the share of a population at or above the Elo. Against all
rated users it is read off a table of counts every 25 points, interpolated;
against regulars it is a share of a sample of their ratings."""

import os
from importlib.machinery import SourceFileLoader

HERE = os.path.dirname(os.path.abspath(__file__))
rank = SourceFileLoader(
    "kg_rank_svg", os.path.join(HERE, "..", "readme", "kg_rank_svg")
).load_module()

ALL = {"total": 1000, "rows": [[1500, 400], [1525, 300], [1550, 200]]}
REGULARS = {"ratings": [1400.0, 1500.0, 1600.0, 1700.0]}


def test_all_reads_a_row_exactly():
    assert rank.top_share_all(ALL, 1525) == 0.3


def test_all_interpolates_between_rows():
    assert rank.top_share_all(ALL, 1540) == 0.24


def test_all_clamps_at_the_ends():
    assert rank.top_share_all(ALL, 1200) == 0.4
    assert rank.top_share_all(ALL, 3000) == 0.2


def test_regulars_counts_at_or_above():
    assert rank.top_share_regulars(REGULARS, 1600) == 0.5
    assert rank.top_share_regulars(REGULARS, 1601) == 0.25


def test_badge_names_both_populations():
    assert "vs all rated" in rank.badge("vs all rated", "top 24%")
    assert "top 71%" in rank.badge("vs 20+ contests", "top 71%")
