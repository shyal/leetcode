"""Every systems design drill, drills/<node>/dNNN_*.markdown, is prose: the
statement above a `## Answer` line that nothing follows, with DRILL, TRAINS
and REQUIRED lines; and its reference, graph/node_notes/<node>/dNNN_*.markdown,
names its SOURCE and lists the points the judge grades against under a
REQUIRED heading (kg_extract design_lead). The design twin of
test_reference_solutions.py: nothing runs, so the shape is what is checked."""

import glob
import os
import re

import pytest
from test_reference_solutions import ROOT, drill_for

REFERENCES = sorted(
    glob.glob(os.path.join(ROOT, "graph", "node_notes", "*", "d[0-9]*.markdown"))
)
DRILLS = sorted(glob.glob(os.path.join(ROOT, "drills", "*", "d[0-9]*.markdown")))
ANSWER_MARK = "## Answer"


def test_there_are_design_drills():
    assert DRILLS and len(DRILLS) == len(REFERENCES)


@pytest.mark.parametrize("reference", REFERENCES, ids=os.path.basename)
def test_design_reference_has_a_source_and_required_points(reference):
    drill = drill_for(reference)
    text = open(reference).read()
    did = os.path.basename(reference).split("_")[0]
    assert text.startswith(f"REFERENCE: {did} "), reference
    assert re.search(r"^SOURCE: .*https://", text, flags=re.M), reference
    head, _, points = text.partition("\nREQUIRED\n")
    required = re.findall(r"^- \S", points.split("\n\n")[0], flags=re.M)
    assert len(required) >= 2, f"{reference}: fewer than two REQUIRED points"
    node = os.path.basename(os.path.dirname(reference))
    assert f"TRAINS: {node}\n" in open(drill).read()


@pytest.mark.parametrize("drill", DRILLS, ids=os.path.basename)
def test_design_drill_is_a_statement_then_an_empty_answer(drill):
    text = open(drill).read()
    assert text.startswith("DRILL: "), drill
    statement, mark, answer = text.partition(f"\n{ANSWER_MARK}\n")
    assert mark, f"{drill}: no `{ANSWER_MARK}` line"
    assert not answer.strip(), f"{drill}: the answer is already written"
    assert re.search(r"^REQUIRED: \S", statement, flags=re.M), drill
    assert "—" not in text and "–" not in text, f"{drill}: a dash"
