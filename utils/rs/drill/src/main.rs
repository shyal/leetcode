// drill - load a drill from the bank (drills/<node-id>/*.py) into current.py.
//
//   drill monotonic-stack        # least-recently-drilled servable file for that node
//   drill d14                    # one drill by its graph id (graph/drills.json)
//   drill drills/monotonic-stack/next_greater_index.py
//   drill monotonic-stack --list
//
// The workflow then matches leetcode problems exactly: a branch named after
// the node is created off master with the stub committed; solve current.py,
// run `make solved` - the DRILL header and its drills.json entry route it to
// a d_-prefixed file in solved/ and drill evidence in the graph, and the
// branch squash-merges into master like any problem branch.
//
// Ported from utils/kg/drill (Python) on 2026-09-12.

use std::path::{Path, PathBuf};
use std::process::Command;

use kg::bank::warm;
use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root};
use kg::drills::{last_drilled, servable_drills};
use kg::evidence::Evidence;
use kg::git::clear_branch;
use regex::Regex;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: drill [--list] target\n\nLoad a bank drill into current.py.\n\n  target  node id (drills/<node>/), a drill id (d14), or a path to a drill file\n  --list  list the node's drills and when last drilled");
        return;
    }
    let list = args.iter().any(|a| a == "--list");
    let Some(target) = args.iter().find(|a| !a.starts_with("--")).cloned() else {
        eprintln!("usage: drill [--list] target");
        std::process::exit(2);
    };
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let today = ctx.today();
    let console = Console::full_width();
    let is_id = Regex::new(r"^d\d+$").unwrap().is_match(&target);

    let candidates: Vec<PathBuf> = if is_id && ctx.drill_path(&target).is_some() {
        vec![ctx.drill_path(&target).unwrap()]
    } else if Path::new(&target).is_file() {
        vec![PathBuf::from(&target)]
    } else {
        let c = ctx.bank_paths(&target);
        if c.is_empty() {
            console.print(&format!(
                "[red]No drills found under drills/{target}/[/red]"
            ));
            let mut existing: Vec<String> = std::fs::read_dir(ctx.drills_dir())
                .map(|rd| {
                    rd.filter_map(Result::ok)
                        .filter(|e| e.path().is_dir())
                        .map(|e| e.file_name().to_string_lossy().into_owned())
                        .collect()
                })
                .unwrap_or_default();
            existing.sort();
            if !existing.is_empty() {
                console.print(&format!(
                    "[dim]Nodes with drills: {}[/dim]",
                    existing.join(", ")
                ));
            }
            std::process::exit(1);
        }
        c.as_ref().clone()
    };
    let ev = Evidence::new(recs);
    let pv = PView::new(ctx.evidenced());

    // a drill is held while an id in its "after" list (graph/drills.json)
    // is not warm, or a second node in its drills.json "trains" is not owned
    // (kg::drills::servable_drills). A direct file path bypasses the hold.
    let direct = Path::new(&target).is_file() || is_id;
    let released: Vec<PathBuf> = if direct {
        candidates.clone()
    } else {
        servable_drills(&ctx, &candidates, &ev, Some(&target), false)
    };

    let when_of = |p: &Path| {
        let w = last_drilled(&ctx, p, &ev);
        if w.is_empty() {
            "never".to_string()
        } else {
            w
        }
    };
    if list {
        for path in &candidates {
            let after: Vec<String> = ctx
                .drill_after(path)
                .into_iter()
                .filter(|a| warm(&ctx, a, &pv, &ev, today, false) == Some(false))
                .collect();
            let hold = if released.contains(path) {
                String::new()
            } else {
                format!(
                    "  [yellow]held by {}[/yellow]",
                    if after.is_empty() {
                        "TRAINS".to_string()
                    } else {
                        after.join(", ")
                    }
                )
            };
            console.print(&format!(
                "{:>4}  {}  [dim]last drilled: {}[/dim]{hold}",
                ctx.drill_id(path).unwrap_or_else(|| "-".to_string()),
                path.display(),
                when_of(path)
            ));
        }
        return;
    }

    if released.is_empty() {
        console.print(&format!(
            "[yellow]every drill of {target} is held[/yellow] - `--list` shows by what; `make dependents <id>` shows what a hold opens"
        ));
        std::process::exit(1);
    }
    // least-recently-drilled first; never-drilled sorts before everything
    let path = released
        .iter()
        .min_by_key(|p| last_drilled(&ctx, p, &ev))
        .unwrap()
        .clone();

    let current = ctx.root.join("current.py");
    if std::fs::read_to_string(&current).is_ok_and(|s| !s.trim().is_empty()) {
        console.print("[red]current.py is not empty — finish or clear it first.[/red]");
        std::process::exit(1);
    }

    let content = std::fs::read_to_string(&path).expect("read the drill");
    let title = Regex::new(r"(?m)^\s*DRILL:\s*(.+)$")
        .unwrap()
        .captures(&content)
        .map(|m| m[1].trim().to_string())
        .unwrap_or_else(|| path.file_stem().unwrap().to_string_lossy().into_owned());
    let node_id = path
        .parent()
        .and_then(|d| d.file_name())
        .map(|s| s.to_string_lossy().into_owned())
        .unwrap_or_default();
    // the branch is the drill's graph id: unique per drill, the way a
    // problem's branch is its number; the node name is shared by its bank
    let did = ctx.drill_id(&path);
    let branch = did.clone().unwrap_or(node_id);

    if !clear_branch(&ctx.root, &branch) {
        return;
    }
    let git = |args: &[&str]| {
        let out = Command::new("git")
            .args(args)
            .current_dir(&ctx.root)
            .output()
            .expect("git");
        if !out.status.success() {
            eprintln!(
                "git {} failed: {}",
                args.join(" "),
                String::from_utf8_lossy(&out.stderr).trim()
            );
            std::process::exit(1);
        }
    };
    // same branch flow as prepare: stub committed on a branch off master,
    // which `make solved` later squash-merges back and deletes
    git(&["checkout", "master"]);
    std::fs::write(&current, &content).expect("write current.py");
    git(&["checkout", "-b", &branch]);
    git(&["add", "."]);
    git(&["commit", "-m", &format!("drill: {title}")]);

    console.print(&format!(
        "Loaded [bold]{}. {title}[/bold] ({}) into current.py on branch [bold]{branch}[/bold]  [dim](last drilled: {})[/dim]",
        did.unwrap_or_default(),
        path.display(),
        when_of(&path)
    ));
    console.print("Solve it, then `make solved` as usual.");
    // the Claude Code pane follows the branch: its conversation is the drill's
    let chat = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|d| d.join("kg_chat")))
        .unwrap_or_else(|| ctx.root.join("utils/rs/target/release/kg_chat"));
    let _ = Command::new(chat)
        .arg("--switch")
        .current_dir(&ctx.root)
        .status();
}
