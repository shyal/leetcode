// kg_force - constrained solve mode.
//
//   kg_force <problem>    # `make prepare` + arm the style judge: the solve
//                         # must exercise the problem's mapped walk, spelled
//                         # out as a human-readable blurb
//   kg_force --check      # gate for `make solved`: exits 1 (blocking the
//                         # merge) if a forced move went unexercised
//   kg_force --clear      # drop the constraint (`make unforce`)
//
// Free mode is just `make prepare`: solve however you like, evidence records
// what you actually did, no style verdicts.
//
// Ported from utils/kg/kg_force (Python) on 2026-09-12.

use std::path::Path;
use std::process::{Command, Stdio};
use std::time::{Duration, Instant};

use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root};
use kg::llm::claude_json;
use kg::pyjson;
use regex::Regex;
use serde_json::{json, Value};

fn blurb(ctx: &Ctx, mv: &str) -> String {
    let n = &ctx.nodes[mv];
    format!("{}: {}", n.name, n.desc)
}

fn current_branch(root: &Path) -> String {
    Command::new("git")
        .args(["rev-parse", "--abbrev-ref", "HEAD"])
        .current_dir(root)
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
        .unwrap_or_default()
}

fn arm(console: &Console, ctx: &Ctx, num: &str) {
    let pv = PView::new(ctx.evidenced());
    let Some(p) = pv.map.get(num) else {
        console.print(&format!(
            "[red]{num} is not mapped in graph/problems.json — run `make preflight {num}` first.[/red]"
        ));
        std::process::exit(1);
    };
    let moves: Vec<String> = p
        .moves
        .iter()
        .filter(|m| ctx.nodes.contains_key(*m))
        .cloned()
        .collect();

    let status = Command::new(ctx.root.join(".venv/bin/python3"))
        .args(["utils/kg/prepare", num])
        .current_dir(&ctx.root)
        .status();
    match status {
        Ok(s) if s.success() => {}
        Ok(s) => std::process::exit(s.code().unwrap_or(1)),
        Err(_) => std::process::exit(1),
    }

    let mut header =
        vec!["# FORCED STYLE — `make solved` will reject this solve unless it uses:".to_string()];
    for m in &moves {
        header.push(format!("#   • {}", blurb(ctx, m)));
    }
    header.push("# (`make unforce` drops the constraint)".to_string());
    let cur = ctx.root.join("current.py");
    let body = std::fs::read_to_string(&cur).unwrap_or_default();
    std::fs::write(&cur, format!("{}\n\n{body}", header.join("\n"))).expect("write current.py");
    pyjson::save(
        &ctx.root.join(".force.json"),
        &json!({"problem": num, "moves": moves}),
        None,
    )
    .expect("write .force.json");

    console.print("\n[bold]Forced style:[/bold]");
    for m in &moves {
        console.print(&format!("  • {}", blurb(ctx, m)));
    }
}

/// subprocess.run(timeout=30): None when the run outlived the timeout.
fn run_with_timeout(mut cmd: Command, secs: u64) -> Option<std::process::ExitStatus> {
    let mut child = cmd
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .ok()?;
    let start = Instant::now();
    loop {
        if let Ok(Some(st)) = child.try_wait() {
            return Some(st);
        }
        if start.elapsed() > Duration::from_secs(secs) {
            let _ = child.kill();
            let _ = child.wait();
            return None;
        }
        std::thread::sleep(Duration::from_millis(50));
    }
}

fn check(console: &Console, ctx: &Ctx) {
    let force_file = ctx.root.join(".force.json");
    let Some(force) = pyjson::load(&force_file) else {
        return;
    };
    if current_branch(&ctx.root) != kg::data::value_str(&force["problem"]) {
        let _ = std::fs::remove_file(&force_file); // stale: a different problem was prepared since
        return;
    }
    let moves: Vec<String> = force["moves"]
        .as_array()
        .map(|a| {
            a.iter()
                .map(kg::data::value_str)
                .filter(|m| ctx.nodes.contains_key(m))
                .collect()
        })
        .unwrap_or_default();

    let cur = ctx.root.join("current.py");
    let pythonpath = format!(
        "{}:{}:{}",
        ctx.root.join("utils").display(),
        ctx.root.join("utils/harness").display(),
        std::env::var("PYTHONPATH").unwrap_or_default()
    );
    let mut cmd = Command::new(ctx.root.join(".venv/bin/python3"));
    cmd.arg(&cur)
        .current_dir(&ctx.root)
        .env("PYTHONPATH", pythonpath);
    match run_with_timeout(cmd, 30) {
        None => {
            console.print(
                "[red]⛔ forced solve timed out when executed — fix it before `make solved`.[/red]",
            );
            std::process::exit(1);
        }
        Some(st) if !st.success() => {
            console.print(
                "[red]⛔ forced solve fails when executed — fix it before `make solved`.[/red]",
            );
            std::process::exit(1);
        }
        Some(_) => {}
    }

    let text = std::fs::read_to_string(&cur).unwrap_or_default();
    let body = Regex::new(r"^(#[^\n]*\n)+")
        .unwrap()
        .replace(&text, "")
        .into_owned();
    let body = Regex::new(r#"(?s)^\s*""".*?"""\s*"#)
        .unwrap()
        .replace(&body, "")
        .into_owned();
    let body: String = body.chars().take(6000).collect();
    let required: Vec<String> = moves
        .iter()
        .map(|m| format!("- {m}: {}", blurb(ctx, m)))
        .collect();
    let system = "You judge whether a working LeetCode solution genuinely exercises each required technique.\nThe code was executed and passed; judge only WHICH techniques it uses, strictly.\nA technique counts only if the code actually performs it — routing around it with a different approach does not count.\nOutput STRICT JSON only: {\"<id>\": true|false, ...} with exactly one key per required technique.";
    let prompt = format!(
        "Required techniques:\n{}\n\nCode:\n{body}",
        required.join("\n")
    );
    let result = match claude_json(&prompt, system, "haiku", 2) {
        Ok(v) => v,
        Err(e) => {
            console.print(&format!("[red]{e}[/red]"));
            std::process::exit(1);
        }
    };
    let missing: Vec<&String> = moves
        .iter()
        .filter(|m| !result.get(m.as_str()).is_some_and(kg::data::truthy))
        .collect();
    if missing.is_empty() {
        console.print("[green]✓ forced style satisfied[/green]");
        let _ = std::fs::remove_file(&force_file);
        return;
    }
    console.print("[red]⛔ REJECTED — solve works, but the forced style was not used:[/red]");
    for m in missing {
        console.print(&format!("  [red]•[/red] {}", blurb(ctx, m)));
    }
    console.print("[dim]rework current.py and run `make solved` again, or `make unforce` to file it freestyle.[/dim]");
    std::process::exit(1);
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_force [--check] [--clear] [problem]\n\nConstrained solve mode.\n\n  problem  problem number to prepare with a forced style\n  --check  gate for make solved\n  --clear  drop the constraint");
        return;
    }
    let root = repo_root();
    load_envrc(&root);
    let console = Console::full_width();
    if args.iter().any(|a| a == "--clear") {
        let f = root.join(".force.json");
        if f.exists() {
            let _ = std::fs::remove_file(&f);
            console.print("constraint dropped — freestyle solve.");
        }
        return;
    }
    let (ctx, _) = Ctx::load(root);
    if args.iter().any(|a| a == "--check") {
        check(&console, &ctx);
        return;
    }
    let Some(problem) = args.iter().find(|a| !a.starts_with("--")) else {
        eprintln!("usage: kg_force [-h] [--check] [--clear] [problem]\nkg_force: error: problem number required (or --check/--clear)");
        std::process::exit(2);
    };
    arm(&console, &ctx, problem.trim().trim_end_matches('.'));
    let _ = Value::Null;
}
