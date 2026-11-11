---
name: audio-report
description: Write and render the spoken training report (mp3) about the mental models that are being installed and the operator's progress. Use when asked for the audio report, the training brief, or the spoken report.
---

Make the spoken training report. The output is two files in `graph/` (ignored by git):

- `graph/training_brief_<YYYY-MM-DD>.script.txt`
- `graph/training_brief_<YYYY-MM-DD>.mp3`

The date is today in Manila time.

## Subject

The report has two subjects, in this order:

1. The mental models that are being installed. A mental model is a node in `graph/nodes.json`. Say which models are installed, which models are being installed now, and which models are not installed.
2. The operator's progress since the last report.

His goal is to get mental models installed properly. A pass on a problem that he sees for the first time is the check on that goal. It is not the goal.

## Step 1. Find the window

The window starts on the date of the newest `graph/training_brief_*.script.txt` and ends today. Read that script. The new report must not repeat it. If a verdict in it changed, say so.

## Step 2. Read the data

Read all of this before you write a sentence. The data is for you. The report contains only the ideas that you find in it.

- `graph/evidence.json`, key `evidence`: each solve in the window. Fields: `date`, `problem`, `moves` (node id to `clean` or `struggled`), `assist`, `note`, `summary`, `seconds`, `learning`. A file name with `FAILED` is a fail. A drill has `problem == "drill"`.
- `graph/nodes.json`: the node `name` and `desc` for each node id.
- `graph/problems.json`: the `title` for each problem number.
- `graph/node_notes/`: the notes for each node.
- `make kg-status`, `make stats 30`, `make progress`, `make queue`.
- `git log` since the last report.
- The memory notes written since the last report.

Divide the solves into first sight and repeat. The first evidence date of a problem tells you which it is. A solve with `learning` is not a scored solve.

For each model, read all its solves in the window together. Then put it in one group:

- Installed: clean on first sight problems, with no help.
- Being installed: clean on repeats or in learning solves, but not yet on a first sight problem.
- Not installed: the fails and the `struggled` marks continue.

Read all the fail notes together. Name what they have in common before you write.

Make sure that each claim agrees with `evidence.json` before you write it.

## Step 3. Write the script

Shape:

1. The verdict, in two sentences. Is the training healthy or not, and on what.
2. The models. The three groups from Step 2. For each claim, give one or two problems as evidence.
3. The one pattern behind most of the fails. Show it on one problem of his from the window.
4. The smaller issues, in order of importance, each with an opinion.
5. An opinion on the training, including what he will not like.
6. The verdict again, and a maximum of three actions.

Rules. These are hard rules:

- A problem is given by its name. Never say its number. "Linked List In Binary Tree", not "1367". Say a Roman numeral in a title as a word: "Permutations Two".
- A model is given by its `name` from `nodes.json`, not its id.
- Words, not numbers. No counts, ratios, minutes, percentages or ratings. Say "almost always", "less than half", "most of them".
- No chronology. No list of problems. A problem is in the report only as evidence for an idea.
- Judgment and opinion are necessary. One position, with no hedge.
- No praise that is not earned, no reassurance, no silver lining, no blame on other things.
- Do not say when to sleep. Do not say "leetcode is a gate". Do not say "struggling".
- No technique or solution for a problem that he failed and did not solve after. Say what went wrong in general words only.
- Simple words, short sentences (ASD-STE100). No metaphors, no idioms, no coined words.
- No dashes. Dates as "November 11". The text is for a voice: no code, no symbols, no lists, no headings. Paragraphs are divided by an empty line.
- The length comes from the ideas. Do not add text to get a length.

## Step 4. Render

```
BRIEF_TMP=$(mktemp -d) .venv/bin/python misc/brief_tts.py graph/training_brief_<YYYY-MM-DD>.script.txt
```

- The voice speed is 1.0. Do not change it.
- Use a new `BRIEF_TMP` directory each time. The part files are cached by name.
- The key is in `~/.openai_key_leet`.
- If the mp3 for today exists, render again only when the operator asks.

## Step 5. Reply

Give the path of the mp3 and its duration. Then give the verdict in four short paragraphs, in words. Give nothing more.
