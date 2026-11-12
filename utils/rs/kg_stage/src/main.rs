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
//                      no more (the reason would be a hint), then asks:
//                      try again, a hint, the answer of the stage, or stop
//                      (make failed). The choice is written in the notes,
//                      where the judge of the filed solve reads the help
//                      (kg_extract: ASSIST, recognition failure).
//
// The judge's model is JUDGE_MODEL (kg::llm). The cached solution of the
// problem (.prepare_cache), when there is one, is its reference.

use std::io::{BufRead, Write};
use std::path::Path;
use std::process::{exit, Command};

use kg::console::Console;
use kg::data::{load_envrc, repo_root, truthy, value_str};
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

fn ask(prompt: &str, system: &str) -> Result<Value, String> {
    claude_json(prompt, system, &judge_model("sonnet"), 2).map_err(|e| e.to_string())
}

fn judge(st: u8, ctx: &str, approach: &str, answer: &str) -> Result<bool, String> {
    let system = if st == 1 {
        "A candidate read a LeetCode problem and wrote, in plain English, the approach they will take. This is stage 1 of 3: the pseudocode and the code come later. You judge the approach.\n\nRules:\n- \"valid\" is true when the approach has the key idea of an accepted solution to this exact problem, and a solution that follows it is correct on every input and fast enough for the constraints. The approach can be short. Details, edge cases and data structure choices are not necessary at this stage. An approach different from the reference is valid when it is correct and fast enough.\n- \"valid\" is false when the approach is wrong on some input, is too slow for the constraints (a brute force where the constraints forbid it), restates the problem without an idea, or is too vague to tell which solution it describes.\n- Judge what the candidate wrote, not the solution you would write.\n\nOutput STRICT JSON only: {\"valid\": true|false, \"why\": \"<one sentence>\"}"
    } else {
        "A candidate read a LeetCode problem and wrote pseudocode for it. This is stage 2 of 3: the code comes later, and the code is run and tested there. You judge the PLAN only: the steps and their order.\n\nRules:\n- \"valid\" is true when the steps are the steps of a correct solution, in an order that works, and fast enough for the constraints. The candidate can write the lines in plain English, in code-like shorthand, or in a mix: read every line as a description of a step, never as code.\n- IGNORE every error that is in one line and not in the plan: a wrong index, a wrong method or function name, wrong or missing syntax, a wrong operator, a missing initialisation, a wrong return type or shape, an off-by-one, a variable name that changes, an edge case that one line of code repairs. Stage 3 finds those when the code runs.\n- \"valid\" is false only when the plan is wrong: a necessary step is missing, a step computes the wrong thing, the order does not work, the plan is too slow, or a step hides the hard part (\"find the answer\", \"do the dp\").\n- If you are not sure, \"valid\" is true.\n- Judge what the candidate wrote, not the solution you would write. A plan different from the reference is valid when it is correct.\n\nOutput STRICT JSON only: {\"valid\": true|false, \"why\": \"<one sentence>\"}"
    };
    let prompt = if st == 1 {
        format!("{ctx}\nCANDIDATE'S APPROACH:\n{answer}")
    } else {
        format!(
            "{ctx}\nCANDIDATE'S APPROACH (stage 1):\n{}\n\nCANDIDATE'S PSEUDOCODE:\n{answer}",
            if approach.is_empty() { "(none)" } else { approach }
        )
    };
    let result = ask(&prompt, system)?;
    if std::env::var("KG_STAGE_WHY").is_ok() {
        eprintln!("why: {}", result.get("why").map(value_str).unwrap_or_default());
    }
    Ok(result.get("valid").is_some_and(truthy))
}

fn hint(st: u8, ctx: &str, approach: &str, answer: &str, before: &[String]) -> Result<String, String> {
    let system = format!(
        "A candidate works on a LeetCode problem in stages. Their {} was judged wrong or incomplete, and they asked for a hint.\n\nRules:\n- The hint is ONE question about one small input, from the examples of the statement or made by you, that the candidate can work out with pen and paper and that shows where the plan goes wrong. Write the input in full in the question.\n- The hint never states a fact, a formula, a count, the correct step or what is wrong. It does not name an algorithm or a data structure. It gives no code and it is never about syntax.\n- Do not repeat a hint that was given before: ask about a different input.\n- {RULES}\n\nOutput STRICT JSON only: {{\"hint\": \"<the hint>\"}}",
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
    if or_stop(console, judge(st, &ctx, &approach, &answer)) {
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
    let text = save(root, &text, &stage::miss(st));
    console.print(&format!("[red]Stage {st} of 3: miss.[/red]"));
    match choice(st) {
        2 => {
            let h = or_stop(console, hint(st, &ctx, &approach, &answer, &stage::hints(&text)));
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

fn main() {
    let root = repo_root();
    load_envrc(&root);
    if !stage::enabled() {
        return;
    }
    if std::env::args().any(|a| a == "--serve") {
        serve(&root);
    } else {
        gate(&Console::full_width(), &root);
    }
}
