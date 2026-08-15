---
name: high-level-walkthrough
description: Explain the current drill/problem's technique in plain english, numbered steps, before the operator implements it. Use when asked for the high-level version, pseudocode, or a walkthrough of how a technique works.
---

Give the high-level version of the technique behind the current drill or problem (read `current.py` if you don't already know it).

Format rules — these are hard rules:

1. Plain english words only. No code, no near-python, no symbols, no `parent[x] == x` style notation. If you're tempted to write a variable name, describe the thing instead ("a node whose parent is itself").
2. Numbered steps, one idea per step. Usually 3-5 steps total.
3. Two layers max: the core mechanism first, then one step for how the drill sits on top of it.
4. Short. No preamble, no recap, no "that's it" outro, no list of sub-drills or variations unless asked.
5. This is scaffolding the operator implements from — describe the mechanism, never paste an implementation. Keep his variable names if he already has some and you must refer to them.
