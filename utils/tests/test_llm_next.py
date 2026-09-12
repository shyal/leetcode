# make next llm: the model's pick is cached under the evidence file, the day
# and the words after `next`, so `make next llm prepare` prepares the problem
# that was just read without a second model call, and a new rep or a new day
# asks again. The model itself is never called here.

import importlib.util
import json
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_tool():
    path = os.path.join(ROOT, "utils", "kg", "kg_llm_next")
    spec = importlib.util.spec_from_loader("kg_llm_next", loader=None, origin=path)
    mod = importlib.util.module_from_spec(spec)
    mod.__file__ = path
    with open(path) as f:
        exec(compile(f.read(), path, "exec"), mod.__dict__)
    return mod


PICK = {
    "problem": "543",
    "title": "Diameter of Binary Tree",
    "agrees": False,
    "reason": "one failed rep, nothing since.",
    "plan": [],
}


@pytest.fixture
def tool(tmp_path, monkeypatch):
    mod = load_tool()
    monkeypatch.setattr(mod, "CACHE", str(tmp_path / "llm_next.json"))
    calls = []

    def fake_ask(context, model):
        calls.append(model)
        return dict(PICK)

    monkeypatch.setattr(mod, "ask", fake_ask)
    monkeypatch.setattr(mod, "build_context", lambda words: {"words": words})
    monkeypatch.setenv("KG_TODAY", "2026-09-12")
    mod.calls = calls
    return mod


def test_second_read_is_cached(tool):
    pick, cached = tool.recommendation([], "opus")
    assert (pick["problem"], cached) == ("543", False)
    pick, cached = tool.recommendation([], "opus")
    assert (pick["problem"], cached) == ("543", True)
    assert tool.calls == ["opus"]


def test_words_and_day_are_part_of_the_key(tool, monkeypatch):
    tool.recommendation([], "opus")
    tool.recommendation(["sql"], "opus")
    monkeypatch.setenv("KG_TODAY", "2026-09-13")
    tool.recommendation([], "opus")
    assert len(tool.calls) == 3


def test_new_evidence_asks_again(tool, monkeypatch):
    tool.recommendation([], "opus")
    keys = [tool.context_key([])]
    monkeypatch.setattr(
        tool,
        "context_key",
        lambda words: "a different evidence file",
    )
    _, cached = tool.recommendation([], "opus")
    assert not cached and len(tool.calls) == 2 and keys[0] != "a different evidence file"


def test_fresh_ignores_the_cache(tool):
    tool.recommendation([], "opus")
    _, cached = tool.recommendation([], "opus", fresh=True)
    assert not cached and len(tool.calls) == 2


def test_cache_file_holds_key_and_pick(tool):
    tool.recommendation([], "opus")
    with open(tool.CACHE) as f:
        data = json.load(f)
    assert set(data) == {"key", "pick"} and data["pick"]["problem"] == "543"
