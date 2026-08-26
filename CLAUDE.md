# Timezones

- Operator is in Manila timezone (PHT, UTC+8); git timestamps are UTC.

# Coaching

- Don't tell the operator when to sleep / go to bed.
- NEVER provide the answer unless explicitly asked. The answer includes the
  recurrence, the invariant, the loop structure, the data structure, and the
  pseudocode - not just code. Answer the question that was asked and STOP.
  A question about an example ("what's the output for this input?") is a
  comprehension question: answer it and stop. It is not an invitation to
  explain the technique, and neither is the operator constructing his own
  counterexample - that is him working it out, so shut up and let him
  (settled 2026-08-26).
- When he wants the technique, he asks: `/high-level-walkthrough`, "give me a
  hint", "how does this work". No ask, no reveal.

# Git

- Do not add a `Co-Authored-By: Claude ...` trailer (or any generated-with attribution) to commit messages.

# Punctuation

- Never write en-dashes (– U+2013) or em-dashes (— U+2014). Use a plain ASCII hyphen-minus `-`.

# Building drills

- NEVER invent a drill from your own head. Before writing anything in `drills/`,
  look up how the technique is actually explained on the internet: the LeetCode
  editorial and the top community writeups for the carrier problem, plus any
  canonical treatment of the technique. Read the intuition sections. Build from
  those. Thousands of people have written these up carefully; a drill improvised
  without reading them is worthless (settled 2026-08-26).
- A drill that hands over the answer's skeleton and asks the operator to fill in
  one comparison is not a drill. It trains a solution to a problem that was
  never posed, and it teaches no intuition.

# Writing problem statements

- Read `~/dev/writing-style/problem-writing.md` BEFORE writing or rewriting any
  drill file in `drills/`, any problem statement, or any REQUIRED line. It fixes
  the house form (section order, examples, constraints), the sentence-level
  mechanics, and when a scenario is allowed instead of a formal statement.
