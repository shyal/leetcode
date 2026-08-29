"""Timezone seams. The system clock and git run UTC; the operator's day is
Manila (UTC+8), which starts at 16:00 UTC. Solved filenames are stamped in
UTC (utils/kg/solved), so between 16:00 and 24:00 UTC — midnight to 8am Manila,
the usual session hours — the raw Y_M_D digits in a filename are one day
behind "today". kg_extract once read those digits straight into the evidence
date, so a drill solved after Manila midnight looked un-drilled the same
night and make next re-offered it. These tests pin the whole path: the UTC
stamp, the Manila conversion, the evidence invariant, and due_drill at the
boundary."""

import os
from datetime import date, datetime, timezone
from importlib.machinery import SourceFileLoader

from kg import kg_lib
from kg.kg_lib import MANILA, manila_date_from_filename, due_drill, last_drilled

KG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kg")
kg_extract = SourceFileLoader("kg_extract", os.path.join(KG, "kg_extract")).load_module()
# NOT module name "solved" — test_runner imports solve files as the package
# solved.<stem> from ./solved/, and that name in sys.modules would shadow it
solved = SourceFileLoader("solved_cli", os.path.join(KG, "solved")).load_module()


def utc(y, mo, d, h, mi=0, s=0, micro=0):
    return datetime(y, mo, d, h, mi, s, micro, tzinfo=timezone.utc)


# --- the toolchain's clock is pinned to Manila ---------------------------------

def test_today_means_the_manila_calendar_day():
    assert os.environ["TZ"] == "Asia/Manila"
    assert date.today() == datetime.now(MANILA).date()


# --- filename stamp -> Manila day ----------------------------------------------

def test_evening_utc_stamp_is_the_next_manila_day():
    # the actual incident: drill solved 19:44 UTC Aug 23 = 03:44 Manila Aug 24
    name = "d_Number_Scanner_2026_08_23T19_44_54_884512_00_00Z.py"
    assert manila_date_from_filename(name) == "2026-08-24"


def test_morning_utc_stamp_is_the_same_manila_day():
    name = "p1_Two_Sum_2026_08_23T08_00_00_000000_00_00Z.py"
    assert manila_date_from_filename(name) == "2026-08-23"


def test_manila_midnight_boundary():
    before = "p1_Two_Sum_2026_08_23T15_59_59_000000_00_00Z.py"
    after = "p1_Two_Sum_2026_08_23T16_00_00_000000_00_00Z.py"
    assert manila_date_from_filename(before) == "2026-08-23"
    assert manila_date_from_filename(after) == "2026-08-24"


def test_failed_marker_and_full_path_still_parse():
    name = "solved/p227_Basic_Calculator_II_FAILED_2026_08_18T23_51_13_723603_00_00Z.py"
    assert manila_date_from_filename(name) == "2026-08-19"


def test_offsetless_legacy_stamp_parses_as_utc():
    # the 2025-10-01 bulk import wrote no _00_00Z suffix
    name = "p88_Merge_Sorted_Array_2025_10_01T21_36_57_880900.py"
    assert manila_date_from_filename(name) == "2025-10-02"


def test_no_timestamp_returns_none():
    assert manila_date_from_filename("drill@2026-07-05-monotonic-stack") is None
    assert manila_date_from_filename("current.py@2006-attempt-2026-07-05") is None


# --- utils/kg/solved stamps in UTC and the round trip lands on the Manila day -----

def test_solved_filename_roundtrip_across_midnight():
    now = utc(2026, 8, 23, 19, 44, 54, 884512)
    name = solved.solved_filename("drill", "Number Scanner", now=now)
    assert name == "d_Number_Scanner_2026_08_23T19_44_54_884512_00_00Z.py"
    assert manila_date_from_filename(name) == "2026-08-24"


def test_solved_filename_roundtrip_daytime():
    now = utc(2026, 8, 23, 9, 5, 0)
    name = solved.solved_filename("560", "Subarray Sum Equals K", now=now)
    assert name.startswith("p560_Subarray_Sum_Equals_K_2026_08_23T09_05_00")
    assert manila_date_from_filename(name) == "2026-08-23"


def test_solved_filename_failed_marker_survives_roundtrip():
    now = utc(2026, 8, 23, 23, 59, 59)
    name = solved.solved_filename("227", "Basic Calculator II", failed=True, now=now)
    assert "_FAILED_" in name
    assert manila_date_from_filename(name) == "2026-08-24"


# --- kg_extract derives evidence dates through the shared helper ---------------

def test_extract_uses_the_manila_helper():
    assert kg_extract.manila_date_from_filename is kg_lib.manila_date_from_filename
    # the raw-digits regex must stay dead
    assert not hasattr(kg_extract, "DATE_RE")


# --- evidence.json invariant: stored dates ARE the Manila days -----------------

def test_every_evidence_date_matches_its_filename_manila_day():
    """Regression net for the whole seam: if kg_extract (or anything else)
    ever writes a UTC day into evidence again, this fails on the first solve
    after Manila midnight. Manually-dated entries — keys with no timestamp,
    or bulk imports whose date was set independently of the filename — are
    exempt: for those the stored date deliberately differs from the raw
    digits in the name."""
    for key, rec in kg_lib.load_evidence().items():
        m = kg_lib.FNAME_TS_RE.search(key)
        if not m:
            continue
        raw_utc_day = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        manila_day = manila_date_from_filename(key)
        if rec["date"] == raw_utc_day and manila_day != raw_utc_day:
            raise AssertionError(
                f"{key}: date {rec['date']} is the UTC day; the Manila day is {manila_day}"
            )


# --- due_drill at the boundary: the bug that started this ----------------------

def bank(tmp_path, monkeypatch, node, title):
    d = tmp_path / node
    d.mkdir()
    f = d / "r0_x.py"
    f.write_text(f'"""\nDRILL: {title}\n"""\n')
    monkeypatch.setattr(kg_lib, "DRILLS_DIR", str(tmp_path))
    return str(f)


def test_drill_solved_after_manila_midnight_is_not_due_again(tmp_path, monkeypatch):
    path = bank(tmp_path, monkeypatch, "recursive-descent", "Number Scanner")
    key = "solved/d_Number_Scanner_2026_08_23T19_44_54_884512_00_00Z.py"
    ev = {key: {"date": manila_date_from_filename(key), "problem": "drill", "moves": {}}}
    today = date(2026, 8, 24)  # Manila day of that solve
    assert last_drilled(path, ev) == "2026-08-24"
    assert due_drill("recursive-descent", ev, today=today) is None


def test_the_utc_date_bug_would_have_reoffered_it(tmp_path, monkeypatch):
    """What actually happened on 2026-08-24: the evidence carried the UTC day,
    so the drill looked a day old and was offered again the same night."""
    bank(tmp_path, monkeypatch, "recursive-descent", "Number Scanner")
    ev = {"solved/d_Number_Scanner_2026_08_23T19_44_54_884512_00_00Z.py":
          {"date": "2026-08-23", "problem": "drill", "moves": {}}}
    assert due_drill("recursive-descent", ev, today=date(2026, 8, 24)) is not None


def test_drill_solved_yesterday_is_due_today(tmp_path, monkeypatch):
    bank(tmp_path, monkeypatch, "recursive-descent", "Number Scanner")
    key = "solved/d_Number_Scanner_2026_08_22T19_44_54_884512_00_00Z.py"
    ev = {key: {"date": manila_date_from_filename(key), "problem": "drill", "moves": {}}}
    assert due_drill("recursive-descent", ev, today=date(2026, 8, 24)) is not None
