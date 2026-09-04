"""kg_streak_svg: a streak is a run of consecutive Manila solving days. The
current one counts back from today, or from yesterday while today is still
open; the best one is the longest run in the history."""
import os
from datetime import date, timedelta
from importlib.machinery import SourceFileLoader

HERE = os.path.dirname(os.path.abspath(__file__))
streak = SourceFileLoader(
    "kg_streak_svg", os.path.join(HERE, "..", "readme", "kg_streak_svg")).load_module()

D = date(2026, 9, 4)


def days(*offsets):
    return {D - timedelta(days=o) for o in offsets}


def test_current_streak_counts_back_from_today():
    assert streak.current_streak(days(0, 1, 2, 4), D) == 3


def test_current_streak_survives_an_open_day():
    assert streak.current_streak(days(1, 2, 3), D) == 3


def test_current_streak_is_zero_after_a_missed_day():
    assert streak.current_streak(days(2, 3), D) == 0


def test_best_streak_is_the_longest_run():
    assert streak.best_streak(days(0, 5, 6, 7, 8, 20)) == 4
    assert streak.best_streak(set()) == 0


def test_badge_is_green_only_when_today_has_a_rep():
    assert streak.GREEN in streak.badge(3, 9, streak.GREEN)
    assert "3 days · best 9" in streak.badge(3, 9, streak.GREEN)
    assert "1 day · best 1" in streak.badge(1, 1, streak.MUTED)
