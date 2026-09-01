"""The curve-fit knobs (utils/kg/kg_curve): the era boundary drops trials,
recency weighting discounts them by age, and a weighted fit follows the
era the weights favor. Synthetic trials only; nothing here reads the repo's
evidence."""

import os
from datetime import date
from importlib.machinery import SourceFileLoader

KG = os.path.join(os.path.dirname(__file__), "..", "kg")
kgc = SourceFileLoader("kg_curve", os.path.join(KG, "kg_curve")).load_module()

OLD, NEW = date(2025, 11, 1), date(2026, 8, 20)


def dated(gap, success, day):
    # (gap, success, cleans, struggles, assist, conn, date)
    return (gap, success, 1, 0, 0.0, 4.0, day)


def test_no_knobs_returns_all_trials_unweighted():
    trials, weights = kgc.select_trials([dated(30, 1, OLD), dated(30, 0, NEW)])
    assert trials == [(30, 1, 1, 0, 0.0, 4.0), (30, 0, 1, 0, 0.0, 4.0)]
    assert weights is None


def test_era_boundary_drops_older_trials():
    trials, _ = kgc.select_trials([dated(30, 1, OLD), dated(30, 0, NEW)],
                                  since=date(2026, 1, 1))
    assert trials == [(30, 0, 1, 0, 0.0, 4.0)]
    assert kgc.select_trials([dated(30, 1, OLD)], since=date(2026, 1, 1)) == ([], None)


def test_half_life_discounts_by_age_from_newest():
    rows = [dated(30, 1, date(2026, 8, 1)), dated(30, 1, date(2026, 7, 2)),
            dated(30, 1, date(2026, 8, 31))]
    _, weights = kgc.select_trials(rows, half_life=30)
    assert weights == [0.5, 0.25, 1.0]


def test_recency_weighted_fit_follows_the_recent_era():
    # one era says gap-30 recall holds, a later era says it fails
    rows = [dated(30, 1, OLD)] * 40 + [dated(30, 0, NEW)] * 40

    def pred_at_30(params):
        a, b, c, d, e, conn_mean, beta, slip = params
        s = kgc.math.exp(a + b * kgc.math.log1p(1))  # k=1, no struggles/assist, conn centered
        return (1 - slip) * (1 + 30 / s) ** (-beta)

    t_plain, w_plain = kgc.select_trials(rows)
    t_rec, w_rec = kgc.select_trials(rows, half_life=30)
    plain = pred_at_30(kgc.fit(t_plain, weights=w_plain))
    weighted = pred_at_30(kgc.fit(t_rec, weights=w_rec))
    assert 0.3 < plain < 0.7          # unweighted: the eras split the vote
    assert weighted < 0.25            # weighted: the old era barely votes
    assert weighted < plain - 0.2
