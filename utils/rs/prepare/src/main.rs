// prepare - fetch a leetcode problem, generate a validated solution+asserts
// file with an LLM, and load its stub into current.py on a branch.
//
//   prepare 2413                 # one problem: cache, then branch + current.py
//   prepare --warm 1 2 3         # only populate .prepare_cache
//   prepare --jobs 1 4 5         # problems generated concurrently (default 4)
//   prepare --model gpt-5-mini 6 # the model for the LLM calls
//   prepare monotonic-stack      # a node id routes to the drill picker
//   prepare spot                 # the recognition rep (utils/rs/spot)
//
// A number's pipeline: leetcode's graphql for the statement and the python3
// signature; the model writes the whole file (docstring, solution, demo
// print, the official asserts); it is executed and failures are looped back
// up to three times; the house format is enforced (stub::sanitize, then one
// corrective call on stub::structure_problems); the model proposes edge-case
// expressions whose values the validated solution computes; the one-line
// labelled asserts of assert_gen are appended; both the black-formatted
// solution and its stripped stub (stub::strip_solution) land in
// .prepare_cache/<num>.json. Warming an entry cached before the labelled
// asserts existed adds them.
//
// Ported from utils/kg/prepare (Python) on 2026-09-14.

use std::io::Write;
use std::path::Path;
use std::process::{Command, Stdio};
use std::sync::Mutex;
use std::time::Duration;

use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root, rs_bin};
use kg::evidence::Evidence;
use kg::git::{clear_branch, sleep_records};
use prepare::assert_gen::{extra_asserts, has_extra, strip_fences};
use prepare::stub::{sanitize, strip_solution, structure_problems};
use prepare::{cache_load, cache_save, pool, pyrun};
use serde_json::{json, Value};

const SYSTEM_PROMPT: &str = "You are a helpful assistant that generates Python stubs for \
LeetCode problems. Output ONLY the raw Python source code for \
the stub \u{2014} no explanations, no markdown fences, no preamble, \
no postamble. Do NOT attempt to use any tools; the caller \
writes your stdout straight to disk.";

const EXAMPLE_STUB: &str = r#"
"""
URL: https://leetcode.com/problems/smallest-even-multiple/description/?envType=problem-list-v2&envId=vn57k9wr

2413. Smallest Even Multiple

Given a positive integer n, return the smallest positive integer that is a multiple of both 2 and n.


Example 1:

Input: n = 5
Output: 10
Explanation: The smallest multiple of both 5 and 2 is 10.

Example 2:

Input: n = 6
Output: 6
Explanation: The smallest multiple of both 6 and 2 is 6. Note that a number is a multiple of itself.


Constraints:

    1 <= n <= 150
"""


class Solution:
    def smallestEvenMultiple(self, n: int) -> int:
        i = 1
        while True:
            if i % 2 == 0 and i % n == 0:
                return i
            i += 1


sol = Solution()

print(sol.smallestEvenMultiple(5))  # 10

assert sol.smallestEvenMultiple(5) == 10
assert sol.smallestEvenMultiple(6) == 6
"#;

struct Args {
    numbers: Vec<u64>,
    node_ids: Vec<String>,
    spot: bool,
    warm: bool,
    jobs: usize,
    model: Option<String>,
}

fn usage() -> ! {
    eprintln!(
        "usage: prepare [--warm] [--jobs N] [--model M] targets...\n\nPrepare leetcode questions or bank drills.\n\n  targets  leetcode question numbers, or drill node ids (drills/<node-id>/)\n  --warm   only populate .prepare_cache; skip the git branch/commit step\n  --jobs   max problems generated concurrently (default 4)\n  --model  model for the claude calls (default: your CLI default)"
    );
    std::process::exit(2)
}

fn parse_args() -> Args {
    let mut targets: Vec<String> = Vec::new();
    let mut warm = false;
    let mut jobs = 4usize;
    let mut model = None;
    let mut it = std::env::args().skip(1);
    while let Some(a) = it.next() {
        let (flag, inline) = match a.split_once('=') {
            Some((f, v)) if f.starts_with("--") => (f.to_string(), Some(v.to_string())),
            _ => (a.clone(), None),
        };
        match flag.as_str() {
            "-h" | "--help" => usage(),
            "--warm" => warm = true,
            "--jobs" => {
                jobs = inline
                    .or_else(|| it.next())
                    .and_then(|v| v.parse().ok())
                    .unwrap_or_else(|| usage());
            }
            "--model" => model = Some(inline.or_else(|| it.next()).unwrap_or_else(|| usage())),
            _ if a.starts_with('-')
                && a.len() > 1
                && !a[1..].chars().all(|c| c.is_ascii_digit()) =>
            {
                usage()
            }
            _ => targets.push(a),
        }
    }
    if targets.is_empty() {
        usage();
    }
    let numbers = targets
        .iter()
        .filter(|t| t.chars().all(|c| c.is_ascii_digit()))
        .filter_map(|t| t.parse().ok())
        .collect();
    let node_ids = targets
        .iter()
        .filter(|t| !t.chars().all(|c| c.is_ascii_digit()) && *t != "spot")
        .cloned()
        .collect();
    Args {
        numbers,
        node_ids,
        spot: targets.iter().any(|t| t == "spot"),
        warm,
        jobs,
        model,
    }
}

fn llm(prompt: &str, model: Option<&str>) -> Result<String, String> {
    kg::llm::text(prompt, SYSTEM_PROMPT, model)
        .map(|t| strip_fences(&t))
        .map_err(|e| e.to_string())
}

/// Execute a solution+asserts stub: (ok, combined output).
fn validate(root: &Path, code: &str) -> (bool, String) {
    let o = pyrun::run(root, code, Duration::from_secs(60));
    if o.timed_out {
        return (
            false,
            "Timed out after 60s (likely an infinite loop).".to_string(),
        );
    }
    (o.ok, o.output)
}

/// Evaluate model-proposed test expressions against the validated solution
/// and append `assert expr == <computed value>` lines for the ones that
/// yield a stable literal. Anything that fails to parse, raises, or returns
/// a non-literal is silently dropped.
fn append_computed_asserts(root: &Path, code: &str, exprs_text: &str) -> String {
    let exprs: Vec<&str> = exprs_text
        .lines()
        .map(|l| l.trim().trim_end_matches(','))
        .filter(|l| !l.is_empty() && !l.starts_with('#') && !l.starts_with("```"))
        .filter(|l| ruff_python_parser::parse_expression(l).is_ok())
        .collect();
    if exprs.is_empty() {
        return code.to_string();
    }
    let mut harness = vec![code.to_string(), String::new()];
    for (i, e) in exprs.iter().enumerate() {
        harness.push(format!(
            "try:\n    print('@@EXPR', {i}, repr(({e})))\nexcept Exception:\n    pass"
        ));
    }
    let (_, output) = validate(root, &harness.join("\n"));
    let mut results: Vec<(usize, String)> = Vec::new();
    for line in output.lines() {
        let Some(rest) = line.strip_prefix("@@EXPR ") else {
            continue;
        };
        let Some((idx, rep)) = rest.split_once(' ') else {
            continue;
        };
        if rep.chars().count() > 400 {
            continue; // a wall of output makes a useless, bloated assert
        }
        // reprs like <TreeNode ...> can't be asserted against
        if !prepare::assert_gen::is_literal(rep) || rep == "None" {
            continue;
        }
        let Some(idx) = idx.parse::<usize>().ok().filter(|i| *i < exprs.len()) else {
            continue;
        };
        results.retain(|(i, _)| *i != idx);
        results.push((idx, rep.to_string()));
    }
    results.sort_by_key(|(i, _)| *i);
    let new: Vec<String> = results
        .iter()
        .map(|(i, rep)| format!("assert {} == {rep}", exprs[*i]))
        .collect();
    if new.is_empty() {
        return code.to_string();
    }
    format!("{}\n\n{}\n", code.trim_end(), new.join("\n"))
}

fn graphql(query: &str, variables: Value, what: &str) -> Result<Value, String> {
    let agent: ureq::Agent = ureq::Agent::config_builder()
        .http_status_as_error(false)
        .timeout_global(Some(Duration::from_secs(120)))
        .build()
        .into();
    let mut resp = agent
        .post("https://leetcode.com/graphql/")
        .header("Content-Type", "application/json")
        .send_json(json!({"query": query, "variables": variables}))
        .map_err(|e| format!("Failed to fetch {what}: {e}"))?;
    let status = resp.status().as_u16();
    let text = resp
        .body_mut()
        .read_to_string()
        .map_err(|e| format!("Failed to fetch {what}: {e}"))?;
    if status != 200 {
        return Err(format!("Failed to fetch {what}: {status} - {text}"));
    }
    let data: Value = serde_json::from_str(&text).map_err(|e| e.to_string())?;
    if let Some(errs) = data.get("errors") {
        return Err(format!(
            "GraphQL error: {}",
            kg::pyjson::dumps_unicode(errs, None)
        ));
    }
    Ok(data)
}

struct Question {
    title: String,
    slug: String,
    difficulty: String,
    content: String,
    example_testcases: String,
    python_stub: String,
}

fn get_question_info(num: u64) -> Result<Question, String> {
    // First query to get title, slug, difficulty using problemsetQuestionList
    let query1 = "
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
      problemsetQuestionList: questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
      ) {
        questions: data {
          difficulty
          frontendQuestionId: questionFrontendId
          paidOnly: isPaidOnly
          title
          titleSlug
        }
      }
    }
    ";
    let data1 = graphql(
        query1,
        json!({"categorySlug": "", "limit": 1, "skip": num - 1, "filters": {}}),
        "question list",
    )?;
    let questions = data1["data"]["problemsetQuestionList"]["questions"]
        .as_array()
        .cloned()
        .unwrap_or_default();
    let Some(q) = questions.first() else {
        return Err(format!("No question found for number {num}"));
    };
    let fid = kg::data::value_str(&q["frontendQuestionId"]);
    if fid != num.to_string() {
        return Err(format!(
            "Question frontend ID mismatch: expected {num}, got {fid}"
        ));
    }
    if q["paidOnly"].as_bool().unwrap_or(false) {
        return Err(format!("Question {num} is paid only"));
    }
    let title = kg::data::value_str(&q["title"]);
    let slug = kg::data::value_str(&q["titleSlug"]);
    let difficulty = kg::data::value_str(&q["difficulty"]);

    // Second query to get details
    let query2 = "
    query questionDetails($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        content
        exampleTestcases
        codeSnippets {
          lang
          langSlug
          code
        }
      }
    }
    ";
    let data2 = graphql(query2, json!({"titleSlug": slug}), "question details")?;
    let q2 = &data2["data"]["question"];
    let python_stub = q2["codeSnippets"]
        .as_array()
        .and_then(|sn| {
            sn.iter()
                .find(|s| s["langSlug"] == "python3")
                .and_then(|s| s["code"].as_str())
        })
        .filter(|c| !c.is_empty())
        .ok_or("No Python3 code snippet found")?
        .to_string();
    Ok(Question {
        title,
        slug,
        difficulty,
        content: kg::data::value_str(&q2["content"]),
        example_testcases: kg::data::value_str(&q2["exampleTestcases"]),
        python_stub,
    })
}

/// black.format_str(src, mode=black.Mode()) through the venv's black.
fn black(root: &Path, src: &str) -> Result<String, String> {
    let bin = root.join(".venv/bin/black");
    let mut child = Command::new(if bin.exists() { bin } else { "black".into() })
        .args(["-q", "-"])
        .current_dir(root)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| e.to_string())?;
    child
        .stdin
        .take()
        .unwrap()
        .write_all(src.as_bytes())
        .map_err(|e| e.to_string())?;
    let out = child.wait_with_output().map_err(|e| e.to_string())?;
    if !out.status.success() {
        return Err(String::from_utf8_lossy(&out.stderr).trim().to_string());
    }
    Ok(String::from_utf8_lossy(&out.stdout).into_owned())
}

fn read(root: &Path, rel: &str) -> String {
    std::fs::read_to_string(root.join(rel)).unwrap_or_else(|e| {
        eprintln!("{rel}: {e}");
        std::process::exit(1)
    })
}

fn generation_prompt(root: &Path, num: u64, q: &Question) -> String {
    let problem_url = format!(
        "https://leetcode.com/problems/{}/description/?envType=problem-list-v2&envId=vn57k9wr",
        q.slug
    );
    // the static preamble (environment + rules) comes FIRST and is identical
    // for every problem, so API-side prefix caching can bill it at the cached
    // rate; everything problem-specific comes after it.
    format!(
        "You generate LeetCode solution files. The environment and rules below are FIXED and identical for every request; the problem comes at the end.

Here is the `sitecustomize.py`. Use builtins when necessary.

{sitecustomize}

Here are utility functions:



{tree_utils}




{bst_utils}




{linked_list_utils}


{graph_utils}


IMPORTANT: sitecustomize.py injects a large set of names into `builtins`. Do NOT import ANY of these \u{2014}
they are already available without imports:
- Typing: List, Optional, Dict, Tuple, Any, Callable, Iterable, Iterator, TypeVar, Union
- Collections: Counter, defaultdict, OrderedDict, deque
- Functools/itertools: cache, reduce, chain, combinations, permutations, product, accumulate,
  groupby, pairwise, zip_longest, takewhile, dropwhile, starmap, islice, compress
- Math: gcd, isclose, log2, log10, floor, ceil, prod, sqrt, maxsize
- Heapq: heapify, heappop, heappush, nlargest, nsmallest
- Bisect: bisect_left, bisect_right
- Strings: ascii_letters, ascii_lowercase, ascii_uppercase, digits, hexdigits
- Types: TreeNode, ListNode, GraphNode, Node
- Utilities: build_tree, build_linked_list, get_list_values, build_graph, draw_tree,
  draw_linked_list, tabulate, rich_print, and the rest of the helpers above.

Do NOT emit `from typing import ...`, `from collections import ...`, `from functools import ...`,
`from itertools import ...`, `from math import ...`, `from heapq import ...`, `from bisect import ...`,
or `from string import ...`. The file should have ZERO import statements unless it genuinely needs
something not listed above.

Likewise do NOT redefine any injected helper or class (build_tree, get_level_order,
build_linked_list, get_list_values, draw_tree, TreeNode, ListNode, ...) \u{2014} call the builtins.
The ONLY exception is a problem-specific class the problem statement itself defines (e.g. a
Node with a random pointer, graph neighbors, or quad-tree fields), which must shadow the
injected name. Same for helpers: if the builtin's signature does not fit the problem (e.g.
level order of a FOREST), define the variant locally rather than reshaping the builtin.

Parse the content to extract the problem statement, examples (including inputs, outputs, explanations), and constraints.
Format them properly in the docstring, removing HTML tags.

The docstring should start with the URL line given with the problem, then:

<num>. <title>

Then the cleaned problem statement.

Then the examples.

Then the constraints.

The solution should include this docstring,
the Solution class with the method implemented with a passable solution (generate one),
then instantiate sol = Solution().
The first example is invoked with a print() (or draw_tree, tabulate etc if special printing functions apply), with the expected result commented out.
A tree or linked list argument is never built inline in that call. Build it into a
variable named after the parameter, print the variable on its own line (the harness
draws it), then pass the variable:

root = build_tree([4, 2, 7, 1, 3, 6, 9])
print(root)

print(get_level_order(sol.invertTree(root)))  # [4,7,2,9,6,3,1]

This is so the user can run the code and see output without asserting.
Then generate all the examples as assert statements. ONLY the official examples
given in the problem content - do NOT invent additional test cases; their
expected values would be guesses, and extra coverage is added by a later stage
that computes expected values by execution.

Here is an example of how the file should look:

{example_stub}

Output only the description docstring, the Python code for the solution, and asserts. Indents are 4 spaces.

Now the problem. Please generate a usable solution for LeetCode problem {num}. {title}.

Use the following accurate data from LeetCode API:

Difficulty: {difficulty}

URL line for the docstring:

URL: {problem_url}

Content (HTML, please clean and format it nicely for the docstring):

{content}

Example inputs (newline-separated):

{example_testcases}

Python3 code snippet (use this for the Solution class and method signature):

{python_stub}
",
        sitecustomize = read(root, "utils/harness/sitecustomize.py"),
        tree_utils = read(root, "utils/harness/tree_utils.py"),
        bst_utils = read(root, "utils/harness/bst_utils.py"),
        linked_list_utils = read(root, "utils/harness/linked_list_utils.py"),
        graph_utils = read(root, "utils/harness/graph_utils.py"),
        example_stub = EXAMPLE_STUB,
        title = q.title,
        difficulty = q.difficulty,
        content = q.content,
        example_testcases = q.example_testcases,
        python_stub = q.python_stub,
    )
}

struct Job {
    root: std::path::PathBuf,
    warm: bool,
    model: Option<String>,
    lock: Mutex<()>,
}

impl Job {
    fn llm(&self, prompt: &str) -> Result<String, String> {
        llm(prompt, self.model.as_deref())
    }

    fn process_problem(&self, num: u64) -> Result<(), String> {
        let root = &self.root;
        let key = num.to_string();
        if let Some((title, code, solution)) = cache_load(root, &key) {
            let mut code = code;
            match solution {
                Some(solution) if self.warm && !has_extra(&solution) => {
                    println!("{num}. {title}: adding the extra asserts");
                    let merged =
                        extra_asserts(&solution, &|p| self.llm(p), &|c| validate(root, c))?;
                    if merged != solution {
                        code = match strip_solution(&merged) {
                            Ok(c) => c,
                            Err(e) => {
                                println!("{num}: could not strip the solution\n{e}");
                                return Ok(());
                            }
                        };
                        cache_save(root, &key, &title, &code, &merged);
                    }
                }
                _ => println!("Using cached stub for {num}. {title}"),
            }
            if !self.warm {
                self.finalize(num, &title, &code);
            }
            return Ok(());
        }

        let q = get_question_info(num)?;
        let mut code = self.llm(&generation_prompt(root, num, &q))?;

        // The generator can't execute anything, so its asserts are unverified.
        // Actually run solution+asserts here and loop failures back until green.
        let mut passed = false;
        let mut output = String::new();
        for attempt in 0..3 {
            let (ok, out) = validate(root, &code);
            output = out;
            if ok {
                passed = true;
                break;
            }
            println!(
                "{num}: validation attempt {} failed, asking for a fix",
                attempt + 1
            );
            code = self.llm(&format!(
                "
The following LeetCode stub (solution + asserts) FAILED when executed. Fix the
SOLUTION. The asserts encode the official examples from the problem statement:
their expected values are ground truth and must NOT be changed (only fix an
expected value if it plainly contradicts the Output shown in the docstring's
examples). If an assert is NOT one of the official examples, DELETE it rather
than guessing its value. Keep the format identical (description in docstring, solution,
instantiation, print of first example, asserts). Output only the raw Python
source.

Execution output:

{output}

The code:

{code}
"
            ))?;
        }
        if !passed {
            println!(
                "{num}: could not produce a passing solution+asserts, skipping.\nLast output:\n{output}"
            );
            return Ok(());
        }

        // Enforce the house format: first deterministically (drop redundant
        // imports / helper-class redefinitions), then one corrective call if the
        // file is still structurally wrong. sanitize can remove a class the file
        // genuinely needs (e.g. a quad-tree Node shadowing the injected graph
        // Node), so it only stands if the file still runs afterwards.
        let sanitized = sanitize(&code)?;
        if sanitized != code && validate(root, &sanitized).0 {
            code = sanitized;
        }
        let flaws = structure_problems(&code);
        if !flaws.is_empty() {
            println!("{num}: fixing structure ({})", flaws.join("; "));
            let listed: Vec<String> = flaws.iter().map(|f| format!("- {f}")).collect();
            code = self.llm(&format!(
                "
The following file works but violates the required format:
{}

Fix ONLY those violations. Keep the solution, docstring content, prints and asserts
otherwise identical. Output only the raw Python source.

{code}
",
                listed.join("\n")
            ))?;
            code = sanitize(&code)?;
            if !validate(root, &code).0 || !structure_problems(&code).is_empty() {
                println!("{num}: structure fix failed, skipping.");
                return Ok(());
            }
        }

        // Edge-case coverage: the model proposes test EXPRESSIONS only; the
        // validated solution computes each expected value locally, so no
        // hand-derived (and possibly wrong) value ever lands in an assert.
        let exprs = self.llm(&format!(
            "
The file below contains a correct, validated solution. Propose extra edge-case test
expressions for it: ONE Python expression per line, nothing else. Each expression must
call the solution and evaluate to a plain comparable value (wrap structure results with
helpers like get_level_order / get_list_values as the existing asserts do). Do NOT write
assert statements, expected values, comments, or blank lines. Cover boundary sizes,
duplicates, negatives, and constraint extremes. At most 12 lines.

{code}
"
        ))?;
        let with_edges = append_computed_asserts(root, &code, &exprs);
        if with_edges != code && validate(root, &with_edges).0 {
            code = with_edges;
        }
        // the stage above cannot express a design problem, whose answers depend
        // on a SEQUENCE of calls: these are one self-contained line each,
        // labelled, and frozen by running this same solution.
        code = extra_asserts(&code, &|p| self.llm(p), &|c| validate(root, c))?;
        // current.py is derived from it, deterministically, at write time.
        // both cache fields are stored black-formatted.
        let solution = match black(root, &code) {
            Ok(s) => s,
            Err(e) => {
                println!("{num}: black failed ({e}), storing unformatted");
                code
            }
        };
        let stub = match strip_solution(&solution) {
            Ok(s) => s,
            Err(e) => {
                println!("{num}: could not strip the solution, skipping.\n{e}");
                return Ok(());
            }
        };
        let stub = black(root, &stub).unwrap_or(stub);
        cache_save(root, &key, &q.title, &stub, &solution);
        if self.warm {
            println!("{num}: cached.");
        } else {
            self.finalize(num, &q.title, &stub);
        }
        Ok(())
    }

    fn finalize(&self, num: u64, title: &str, code: &str) {
        let root = &self.root;
        let problem_title = format!("{num}. {title}");
        println!("problem_title {problem_title}");
        let file_name = "current.py";
        let _guard = self.lock.lock().unwrap();

        let (ctx, recs) = Ctx::load(root.clone());
        let pv = PView::new(ctx.evidenced());
        let ev = Evidence::new(recs);
        let key = num.to_string();
        if sleep_records(&ctx, &pv, &ev).iter().any(|r| r.pnum == key) {
            println!(
                "{num} is parked on branch {num}-slept - `make wake {num}` resumes it \
                 (delete the branch first for a truly fresh start)"
            );
            return;
        }
        if !clear_branch(root, &key) {
            return;
        }
        let git = |args: &[&str]| {
            let out = Command::new("git")
                .args(args)
                .current_dir(root)
                .output()
                .expect("git");
            if !out.status.success() {
                println!(
                    "Git command failed: {}\nOutput: {}{}",
                    args.join(" "),
                    String::from_utf8_lossy(&out.stdout),
                    String::from_utf8_lossy(&out.stderr)
                );
                std::process::exit(1);
            }
        };
        git(&["checkout", "master"]);
        std::fs::write(root.join(file_name), code).expect("write current.py");
        println!("Saved stub to {file_name}");
        git(&["checkout", "-b", &key]);
        git(&["add", "."]);
        git(&["commit", "-m", &problem_title]);
        // the Claude Code pane follows the branch: its conversation is the
        // problem's
        let _ = Command::new(rs_bin(root, "kg_chat"))
            .arg("--switch")
            .current_dir(root)
            .status();
    }
}

fn main() {
    let args = parse_args();
    let root = repo_root();
    load_envrc(&root);

    // `spot` routes to the recognition rep (utils/rs/spot): the picker's due
    // statement into current.md on a branch, same flow, no code
    if args.spot {
        let status = Command::new(rs_bin(&root, "spot"))
            .current_dir(&root)
            .status();
        let code = status.ok().and_then(|s| s.code()).unwrap_or(1);
        if code != 0 {
            std::process::exit(code);
        }
    }

    // a node id routes to the drill bank picker - same flow as `make drill
    // <node-id>`
    for nid in &args.node_ids {
        let status = Command::new(rs_bin(&root, "drill"))
            .arg(nid)
            .current_dir(&root)
            .env("PYTHONPATH", pyrun::pythonpath(&root))
            .status();
        let code = status.ok().and_then(|s| s.code()).unwrap_or(1);
        if code != 0 {
            std::process::exit(code);
        }
    }

    let job = std::sync::Arc::new(Job {
        root,
        warm: args.warm,
        model: args.model,
        lock: Mutex::new(()),
    });
    pool(args.numbers, args.jobs, move |num| {
        if let Err(e) = job.process_problem(num) {
            println!("{num}: failed ({e})");
        }
    });
}
