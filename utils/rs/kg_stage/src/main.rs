// kg_stage - the gate of the three stages of a problem solve (kg::stage).
//
//   kg_stage --serve   `make prepare`, after the stub: put the prompt of
//                      stage 1 in the notes of a fresh problem serve. A
//                      drill, a spot rep and a file that holds work are
//                      left alone.
//   kg_stage           `make solved`, first: exit 0 when the solve is to be
//                      filed (stage 3, or a file that is not staged), and
//                      exit 1 when make solved stops here:
//                        stage 1  the approach in the notes is judged
//                        stage 2  the pseudocode in the solve is judged
//                      A pass opens the next stage. A miss says "miss" and
//                      no more (the reason would be a hint), or "miss
//                      (slow)" when the plan is correct and too slow for
//                      the constraints. Then it asks:
//                      try again, a hint, the answer of the stage, or stop
//                      (make failed). The choice is written in the notes,
//                      where the judge of the filed solve reads the help
//                      (kg_extract: ASSIST, recognition failure).
//
//   kg_stage --judge FILE   print the verdict on FILE, write nothing
//                      (check.sh: the cases that test the judge)
//
// The judge lists the nested loops of the plan with their sizes at the
// largest input; the tool multiplies them and decides "slow" from the
// product (stage::OPS_LIMIT).
//
// The judge's model is JUDGE_MODEL (kg::llm), with the reasoning model
// in the place of deepseek's chat model (model()). The cached solution of the
// problem (.prepare_cache), when there is one, is its reference.

use std::io::{BufRead, Write};
use std::path::Path;
use std::process::{exit, Command};

use kg::console::Console;
use kg::data::{load_envrc, repo_root, value_str};
use kg::lang::{current_drill, header, subject, MU, MU_STUB};
use kg::llm::{claude_json, judge_model};
use kg::stage;
use serde_json::Value;

const FILE: &str = "current.mu";

/// The problem number of a mu file that holds a leetcode problem.
fn problem(root: &Path, text: &str) -> Option<String> {
    if current_drill(root).is_some() {
        return None;
    }
    let (id, _) = subject(&header(text, &MU)?)?;
    id.chars().all(|c| c.is_ascii_digit()).then_some(id)
}

fn serve(root: &Path) {
    let path = root.join(FILE);
    let Ok(text) = std::fs::read_to_string(&path) else {
        return;
    };
    // a fresh serve only: the file is the stub as served
    if text.trim().is_empty() || std::fs::read_to_string(root.join(MU_STUB)).ok().as_ref() != Some(&text) {
        return;
    }
    if problem(root, &text).is_none() {
        return;
    }
    let Some(staged) = stage::served(&text) else {
        return;
    };
    std::fs::write(&path, &staged).expect("write current.mu");
    std::fs::write(root.join(MU_STUB), &staged).expect("write .mu_stub");
    println!("Stage 1 of 3: write the approach in the notes of current.mu. Then run make solved.");
}

/// The reference solution in the prepare cache, or "".
fn reference(root: &Path, num: &str) -> String {
    kg::pyjson::load(&root.join(".prepare_cache").join(format!("{num}.json")))
        .and_then(|e| e.get("solution").and_then(Value::as_str).map(String::from))
        .unwrap_or_default()
}

const RULES: &str = "Write in simple English: short sentences, common words, no idioms, no metaphors. Do not use en-dashes or em-dashes.";

fn context(statement: &str, reference: &str) -> String {
    let head: String = statement.chars().take(6000).collect();
    let mut out = format!("STATEMENT:\n{head}\n");
    if !reference.trim().is_empty() {
        let r: String = reference.chars().take(6000).collect();
        out.push_str(&format!(
            "\nAN ACCEPTED SOLUTION (one of the correct solutions, not the only one):\n{r}\n"
        ));
    }
    out
}

/// The model of the stage judge. JUDGE_MODEL=deepseek is the chat model
/// for the other judges; here it is the reasoning model. On the cases of
/// check.sh (2026-11-13) deepseek-chat put loops that run one after the
/// other into one nest in about one run of ten; deepseek-reasoner and opus
/// did not.
fn model() -> String {
    match judge_model("opus").as_str() {
        "deepseek" | "deepseek-chat" => "deepseek-reasoner".to_string(),
        m => m.to_string(),
    }
}

fn ask(prompt: &str, system: &str) -> Result<Value, String> {
    claude_json(prompt, system, &model(), 2).map_err(|e| e.to_string())
}

/// How the judge lists the loops of a plan. The tool, not the model,
/// multiplies the sizes and decides whether the plan is slow
/// (stage::OPS_LIMIT): the model lists loops well and multiplies badly.
const COUNT: &str = "Work through the plan first (\"work\"), then list its loops (\"nest\"), then judge it:\n- \"nest\": the deepest nest of loops in the plan, from the outside to the inside, one entry for each loop: what the loop goes through, and its largest size at the largest input that the constraints allow, as an integer in digits. The tool multiplies the sizes. Use the plan as the candidate wrote it: do not replace a slow step with the fast step that you know, and do not add a step that the plan does not have.\n- A step that reads a whole collection is a loop of the size of that collection, and it is one more entry of the nest when it is inside a loop: a sum, a max, a min, a sort, a count, a copy, a slice, a join, a reversal, a set or a list made from a collection, a search in a list or in a string, a comparison of two strings or two lists, a pass through the keys or the values of a map, a search (bfs, dfs) that starts again with nothing visited.\n- A step that reads or changes one item is not a loop and is not an entry: one key of a map or a set (a lookup, an add, a delete, a +1), one index of a list, a push or a pop, the length of a collection.\n- The size of a collection is its size in the worst input, not in a typical input. A map of counts has one key for each different value that is present (no key has the count 0). That is as many keys as the input has items, or the number of different values that the constraints allow when that is smaller (26 for lowercase letters, 10 for digits).\n- A test of the size of a collection is one operation. A step behind such a test reads only the size that the test allows: in \"the map has exactly two keys and the larger key is twice the smaller\", the test reads a length, and the max and the min read two keys, so the whole line is not a loop and not an entry.\n- A pointer that only moves forward during the whole run is not a nested loop, and a collection where each item goes in one time and comes out one time is not a nested loop: the left end of a sliding window, a stack, a queue, a heap, the visited cells of one search over the whole input. They are not entries of the nest.\n- A recursion or a dp is one entry: the number of different calls or states. The work in one call is one more entry when it is a loop. A recursion with no memo is one entry of the size of all the calls it makes at the largest input (a call that makes two calls, to depth 45, is 2^45 = 35184372088832 calls).\n- An entry is in the nest only when it runs again from its start for each step of the loop outside it. Two sorts one after the other, or a first pass and a second pass, are different nests. A search that keeps its visited cells for the whole run (a flood fill from each cell that is not visited yet) visits each cell one time in the whole run: it is not inside the scan of the cells.\n- Do not divide a size by a constant: the inner of two nested loops over n items has the size n, not n / 2. A sort of n items is one entry of size n * log2(n).\n- Loops that are one after the other are not in the same nest: give the nest with the largest product.\n- When you are not sure that a step is a loop, it is not an entry.\n- Do not decide if the plan is fast enough. The tool decides that.";

const SHAPE: &str = "Output STRICT JSON only, the keys in this order: {\"work\": \"<go through the plan step by step: for each step say if it reads one item or a whole collection, and if it is inside another loop or after it; then say if the plan gives the right answers>\", \"nest\": [{\"loop\": \"<what it goes through>\", \"size\": <integer>}, ...], \"correct\": true|false, \"why\": \"<one sentence>\"}";

fn judge(st: u8, ctx: &str, approach: &str, answer: &str) -> Result<stage::Verdict, String> {
    let system = if st == 1 {
        format!("A candidate read a LeetCode problem and wrote, in plain English, the approach they will take. This is stage 1 of 3: the pseudocode and the code come later. You judge the approach.\n\n{COUNT}\n- When the approach does not say how a step is done, count that step as the fastest usual way to do it. When the approach says how, count what it says.\n\nRules for \"correct\":\n- \"correct\" is true when the approach has the key idea of a solution to this exact problem, and a solution that follows it gives the right answer on every input. The approach can be short. Details, edge cases and data structure choices are not necessary at this stage. An approach different from the reference is correct when it gives the right answers.\n- \"correct\" is false when the approach is wrong on some input, restates the problem without an idea, or is too vague to tell which solution it describes.\n- The speed is not a part of \"correct\": a brute force that gives the right answers is correct.\n- Judge what the candidate wrote, not the solution you would write.\n\n{SHAPE}")
    } else {
        format!("A candidate read a LeetCode problem and wrote pseudocode for it. This is stage 2 of 3: the code comes later, and the code is run and tested there. You judge the PLAN only: the steps and their order.\n\n{COUNT}\n\nRules for \"correct\":\n- \"correct\" is true when the steps are the steps of a solution that gives the right answer on every input, in an order that works. The candidate can write the lines in plain English, in code-like shorthand, or in a mix: read every line as a description of a step, never as code.\n- IGNORE every error that is in one line and not in the plan: a wrong index, a wrong method or function name, wrong or missing syntax, a wrong operator, a missing initialisation, a wrong return type or shape, an off-by-one, a variable name that changes, an edge case that one line of code repairs. Stage 3 finds those when the code runs.\n- \"correct\" is false only when the plan is wrong: a necessary step is missing, a step computes the wrong thing, the order does not work, or a step hides the hard part (\"find the answer\", \"do the dp\").\n- The speed is not a part of \"correct\": a slow plan that gives the right answers is correct.\n- If you are not sure, \"correct\" is true.\n- Judge what the candidate wrote, not the solution you would write. A plan different from the reference is correct when it gives the right answers.\n\n{SHAPE}")
    };
    let prompt = if st == 1 {
        format!("{ctx}\nCANDIDATE'S APPROACH:\n{answer}")
    } else {
        format!(
            "{ctx}\nCANDIDATE'S APPROACH (stage 1):\n{}\n\nCANDIDATE'S PSEUDOCODE:\n{answer}",
            if approach.is_empty() { "(none)" } else { approach }
        )
    };
    let v = stage::Verdict::read(&ask(&prompt, &system)?);
    if std::env::var("KG_STAGE_WHY").is_ok() {
        eprintln!("loops: {}\noperations: {}\nwhy: {}", v.loops, v.operations, v.why);
    }
    Ok(v)
}

fn hint(st: u8, slow: bool, ctx: &str, approach: &str, answer: &str, before: &[String]) -> Result<String, String> {
    let about = if slow {
        "was judged correct but too slow for the constraints, and they asked for a hint.\n\nRules:\n- The hint is ONE question about the largest input that the constraints allow: it names the step of the plan that is done again and again, and asks how many times the plan does it on that input. The candidate works out the number.\n"
    } else {
        "was judged wrong or incomplete, and they asked for a hint.\n\nRules:\n- The hint is ONE question about one small input, from the examples of the statement or made by you, that the candidate can work out with pen and paper and that shows where the plan goes wrong. Write the input in full in the question.\n"
    };
    let system = format!(
        "A candidate works on a LeetCode problem in stages. Their {} {about}- The hint never states a fact, a formula, a count, the correct step or what is wrong. It does not name an algorithm or a data structure. It gives no code and it is never about syntax.\n- Do not repeat a hint that was given before: ask about a different input.\n- {RULES}\n\nOutput STRICT JSON only: {{\"hint\": \"<the hint>\"}}",
        if st == 1 { "approach" } else { "pseudocode" }
    );
    let mut prompt = format!("{ctx}\nCANDIDATE'S APPROACH:\n{}", if approach.is_empty() { "(none)" } else { approach });
    if st == 2 {
        prompt.push_str(&format!("\n\nCANDIDATE'S PSEUDOCODE:\n{answer}"));
    }
    if !before.is_empty() {
        prompt.push_str(&format!("\n\nHINTS GIVEN BEFORE:\n{}", before.join("\n")));
    }
    let result = ask(&prompt, &system)?;
    let text = result.get("hint").map(value_str).unwrap_or_default().trim().to_string();
    if text.is_empty() {
        return Err("the model gave no hint".into());
    }
    Ok(text)
}

fn answer_of(st: u8, ctx: &str, approach: &str) -> Result<String, String> {
    let system = if st == 1 {
        format!("A candidate works on a LeetCode problem in stages and asked for the approach.\n\nRules:\n- Give the approach of the accepted solution in two to four sentences of plain English. No code, no pseudocode.\n- When the problem is a well-known problem with a small change, say that first, in one sentence.\n- {RULES}\n\nOutput STRICT JSON only: {{\"text\": \"<the approach>\"}}")
    } else {
        format!("A candidate works on a LeetCode problem in stages and asked for the pseudocode.\n\nRules:\n- Give the pseudocode of the accepted solution: plain English, one step on each line, structured by two-space indentation, each line small enough to replace with one to three lines of code. No code syntax.\n- Follow the candidate's approach when it is correct.\n- {RULES}\n\nOutput STRICT JSON only: {{\"text\": \"<the lines, separated by \\n>\"}}")
    };
    let prompt = format!("{ctx}\nCANDIDATE'S APPROACH:\n{}", if approach.is_empty() { "(none)" } else { approach });
    let result = ask(&prompt, &system)?;
    let text = result.get("text").map(value_str).unwrap_or_default().trim_end().to_string();
    if text.trim().is_empty() {
        return Err("the model gave no answer".into());
    }
    Ok(text)
}

fn name(st: u8) -> &'static str {
    if st == 1 {
        "approach"
    } else {
        "pseudocode"
    }
}

/// The choice after a miss: 1 to 4. No terminal or no answer: 1.
fn choice(st: u8) -> u8 {
    println!("  1  try again");
    println!("  2  a hint");
    println!("  3  the {}", name(st));
    println!("  4  stop (make failed)");
    loop {
        print!("choice [1]: ");
        let _ = std::io::stdout().flush();
        let mut line = String::new();
        match std::io::stdin().lock().read_line(&mut line) {
            Ok(0) | Err(_) => return 1,
            Ok(_) => {}
        }
        match line.trim() {
            "" | "1" => return 1,
            "2" => return 2,
            "3" => return 3,
            "4" => return 4,
            _ => {}
        }
    }
}

fn save(root: &Path, text: &str, lines: &[String]) -> String {
    let new = stage::with_notes(text, lines);
    std::fs::write(root.join(FILE), &new).expect("write current.mu");
    new
}

fn or_stop<T>(console: &Console, r: Result<T, String>) -> T {
    r.unwrap_or_else(|e| {
        console.print("[red]The stage was not judged: the model call failed.[/red] Run make solved again.");
        eprintln!("{e}");
        exit(1)
    })
}

fn gate(console: &Console, root: &Path) {
    let Ok(text) = std::fs::read_to_string(root.join(FILE)) else {
        return;
    };
    let st = stage::stage(&text);
    if st == 0 || st >= stage::LAST {
        return;
    }
    let Some(num) = problem(root, &text) else {
        return;
    };
    let approach = stage::approach(&text);
    let answer = if st == 1 { approach.clone() } else { stage::pseudocode(&text) };
    if answer.trim().is_empty() {
        console.print(&if st == 1 {
            "[yellow]Stage 1 of 3:[/yellow] write the approach in the notes of current.mu, under the STAGE 1 line. Then run make solved.".to_string()
        } else {
            "[yellow]Stage 2 of 3:[/yellow] write the pseudocode as comment lines in the solve. Then run make solved.".to_string()
        });
        exit(1);
    }
    let ctx = context(&stage::statement(&text), &reference(root, &num));
    let verdict = or_stop(console, judge(st, &ctx, &approach, &answer));
    if verdict.valid() {
        save(root, &text, &stage::pass(st));
        console.print(&format!(
            "[green]Stage {st} of 3: pass.[/green] Stage {}: {}",
            st + 1,
            if st == 1 {
                "write the pseudocode as comment lines in the solve. Then run make solved."
            } else {
                "replace each pseudocode line with code. Then run make solved."
            }
        ));
        exit(1);
    }
    // a correct plan that is slow says so: the candidate cannot see that
    // from a bare miss, and the word gives no step of the solution
    let slow = verdict.correct && verdict.slow();
    let text = save(root, &text, &if slow { stage::miss_slow(st) } else { stage::miss(st) });
    console.print(&format!(
        "[red]Stage {st} of 3: miss{}.[/red]",
        if slow { " (slow)" } else { "" }
    ));
    match choice(st) {
        2 => {
            let h = or_stop(console, hint(st, slow, &ctx, &approach, &answer, &stage::hints(&text)));
            save(root, &text, &stage::hint(&h));
            println!("\nHint: {h}\n");
            println!("Change the {} in current.mu. Then run make solved.", name(st));
        }
        3 => {
            let a = or_stop(console, answer_of(st, &ctx, &approach));
            save(root, &text, &stage::given(st, &a));
            println!("\n{a}\n");
            println!(
                "Stage {}: {}",
                st + 1,
                if st == 1 {
                    "write the pseudocode as comment lines in the solve. Then run make solved."
                } else {
                    "replace each pseudocode line with code. Then run make solved."
                }
            );
        }
        4 => {
            let _ = Command::new("make").arg("failed").current_dir(root).status();
        }
        _ => println!("Change the {} in current.mu. Then run make solved.", name(st)),
    }
    exit(1);
}

/// `kg_stage --judge FILE`: judge the stage that FILE is at and print the
/// verdict as one JSON line. Nothing is written. The check of the judge
/// itself (utils/rs/kg_stage/check.sh) runs this on its cases.
fn judge_file(root: &Path, file: &str) {
    let text = std::fs::read_to_string(file).unwrap_or_else(|e| {
        eprintln!("{file}: {e}");
        exit(2)
    });
    let st = stage::stage(&text);
    if st == 0 || st >= stage::LAST {
        eprintln!("{file}: not at stage 1 or 2");
        exit(2);
    }
    let num = subject(&header(&text, &MU).unwrap_or_default()).map(|(id, _)| id).unwrap_or_default();
    let approach = stage::approach(&text);
    let answer = if st == 1 { approach.clone() } else { stage::pseudocode(&text) };
    let ctx = context(&stage::statement(&text), &reference(root, &num));
    match judge(st, &ctx, &approach, &answer) {
        Ok(v) => println!(
            "{}",
            serde_json::json!({
                "stage": st,
                "verdict": if v.valid() { "pass" } else if v.correct { "slow" } else { "wrong" },
                "operations": v.operations,
                "loops": v.loops,
                "why": v.why,
            })
        ),
        Err(e) => {
            eprintln!("{file}: {e}");
            exit(2)
        }
    }
}

fn main() {
    let root = repo_root();
    load_envrc(&root);
    if !stage::enabled() {
        return;
    }
    let args: Vec<String> = std::env::args().collect();
    if let Some(k) = args.iter().position(|a| a == "--judge") {
        judge_file(&root, args.get(k + 1).map(String::as_str).unwrap_or(""));
    } else if args.iter().any(|a| a == "--serve") {
        serve(&root);
    } else {
        gate(&Console::full_width(), &root);
    }
}
