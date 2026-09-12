// kg_sleep - park the problem you are blocked on; face it when YOU choose.
//
//   make sleep            # mid-exercise: parks the problem on the current branch
//   make sleep 108        # park an explicit problem (its branch must exist)
//   make wake 108         # resume a parked problem on its own branch
//   make sleep -- --list  # show park state (also printed by kg_status)
//
// A parked problem IS its `<num>-slept` branch - no metadata file. Parking
// commits the WIP with a `sleeping:` marker, renames the branch, and returns
// you to master; waking renames it back and stamps a `woke:` marker, so the
// branch history carries every park/resume cycle and `make solved` can report
// the true active solve time (awake intervals only, kg::git::active_seconds).
//
// A park SLEEPS UNTIL `make wake` - no timers, no readiness trigger, nothing
// auto-wakes (settled 2026-08-28). The picker excludes it and warms its
// walk's rusty moves meanwhile (kg_next rule 0). The only pressure is the
// cap: at most MAX_ASLEEP parks at once - at the cap, `make sleep` refuses
// until you face one.
//
// Sleep when you are looping - no new idea in ~15 minutes - not when you are
// merely uncomfortable; discomfort means retrieval is working.
//
// Ported from utils/kg/kg_sleep (Python) on 2026-09-12.

use std::path::Path;
use std::process::Command;

use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, max_asleep, repo_root};
use kg::evidence::Evidence;
use kg::git::{active_seconds, sleep_lines, sleep_records, sleep_state};
use kg::status::{all_statuses, input_tree, SOLID};

struct Git<'a> {
    root: &'a Path,
}

impl Git<'_> {
    fn run(&self, args: &[&str]) -> std::process::Output {
        Command::new("git")
            .args(args)
            .current_dir(self.root)
            .output()
            .unwrap_or_else(|e| die(&format!("git: {e}")))
    }

    /// subprocess.run(check=True): a failing git command ends the run.
    fn checked(&self, args: &[&str]) -> String {
        let out = self.run(args);
        if !out.status.success() {
            die(&format!(
                "git {} failed: {}",
                args.join(" "),
                String::from_utf8_lossy(&out.stderr).trim()
            ));
        }
        String::from_utf8_lossy(&out.stdout).into_owned()
    }

    fn current_branch(&self) -> String {
        self.checked(&["rev-parse", "--abbrev-ref", "HEAD"])
            .trim()
            .to_string()
    }

    fn branch_exists(&self, name: &str) -> bool {
        self.run(&[
            "rev-parse",
            "--verify",
            "--quiet",
            &format!("refs/heads/{name}"),
        ])
        .status
        .success()
    }
}

/// sys.exit(message): the message on stderr, exit code 1.
fn die(msg: &str) -> ! {
    eprintln!("{msg}");
    std::process::exit(1)
}

fn hm(secs: i64) -> String {
    let (h, m) = (secs / 60 / 60, secs / 60 % 60);
    if h > 0 {
        format!("{h}h {m:02}m")
    } else {
        format!("{m}m")
    }
}

fn now() -> i64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_secs() as i64)
        .unwrap_or(0)
}

fn switch_chat(root: &Path) {
    let chat = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|d| d.join("kg_chat")))
        .unwrap_or_else(|| root.join("utils/rs/target/release/kg_chat"));
    let _ = Command::new(chat)
        .arg("--switch")
        .current_dir(root)
        .status();
}

fn wake(ctx: &Ctx, pv: &PView, ev: &Evidence, problem: Option<String>) {
    let git = Git { root: &ctx.root };
    let pnum = match problem {
        Some(p) => p,
        None => {
            let asleep = sleep_state(ctx, pv, ev);
            if asleep.len() != 1 {
                die("which one? make wake <problem>");
            }
            asleep[0].clone()
        }
    };
    let branch = format!("{pnum}-slept");
    if !git.branch_exists(&branch) {
        die(&format!("no parked branch {branch}"));
    }
    let cur = git.current_branch();
    if cur != "master" {
        die(&format!("wake from master (you are on {cur})"));
    }
    let title = pv
        .map
        .get(&pnum)
        .map(|p| p.title.clone())
        .unwrap_or_else(|| "?".to_string());
    git.checked(&["branch", "-M", &branch, &pnum]);
    git.checked(&["checkout", &pnum]);
    // the woke marker is a MERGE from master: checking out an old park would
    // otherwise time-travel the whole tree (Makefile, utils, graph data) back
    // to the day it was cut. -X ours keeps the parked current.py; everything
    // else comes forward to master. The merge commit's timestamp is the wake
    // event active_seconds reads.
    let msg = format!("woke: {pnum}. {title}");
    let merged = git.run(&["merge", "-X", "ours", "-m", &msg, "master"]);
    if !merged.status.success() {
        git.run(&["merge", "--abort"]);
        let err = String::from_utf8_lossy(&merged.stderr).trim().to_string();
        let out = String::from_utf8_lossy(&merged.stdout).trim().to_string();
        println!(
            "could not sync with master — tree may be stale:\n{}",
            if err.is_empty() { out } else { err }
        );
    }
    if !git
        .checked(&["log", "-1", "--format=%s"])
        .starts_with("woke:")
    {
        // master had nothing new (or the merge failed): stamp the wake anyway
        git.checked(&["commit", "--allow-empty", "-m", &msg]);
    }
    let (active, slept, sleeps) = active_seconds(&ctx.root, &pnum, now());
    println!(
        "{pnum}. {title} is awake on branch {pnum} — {} fought so far, {} slept over {sleeps} park(s). make solved / make sleep as usual.",
        hm(active),
        hm(slept)
    );
    // the Claude Code pane follows the branch: back to the problem's conversation
    switch_chat(&ctx.root);
}

fn park(ctx: &Ctx, pv: &PView, ev: &Evidence, problem: Option<String>) {
    let git = Git { root: &ctx.root };
    let branch = git.current_branch();
    let pnum = match problem {
        Some(p) => p,
        None if pv.map.contains_key(&branch) => branch.clone(),
        None => die(&format!(
            "can't tell which problem to sleep (branch '{branch}'); pass one: make sleep 108"
        )),
    };
    if !pv.map.contains_key(&pnum) {
        die(&format!(
            "can't tell which problem to sleep (branch '{branch}'); pass one: make sleep 108"
        ));
    }
    let recs = sleep_records(ctx, pv, ev);
    let slept_branch = format!("{pnum}-slept");
    if git.branch_exists(&slept_branch) && recs.iter().any(|r| r.pnum == pnum) {
        die(&format!("{pnum} is already parked"));
    }
    let cap = max_asleep();
    if recs.len() as i64 >= cap {
        let mut parked: Vec<&kg::git::SleepRec> = recs.iter().collect();
        parked.sort_by(|a, b| a.pnum.cmp(&b.pnum));
        let parked: Vec<String> = parked
            .iter()
            .map(|r| format!("{}. {}", r.pnum, r.title))
            .collect();
        die(&format!(
            "cap ({cap}) reached — face one first (make wake <n>): {}",
            parked.join(", ")
        ));
    }

    let title = pv.map[&pnum].title.clone();
    let msg = format!("sleeping: {pnum}. {title}");
    if branch == pnum {
        let fought = active_seconds(&ctx.root, &pnum, now()).0;
        // park ONLY current.py on the branch. Other bystander files stay in
        // the working tree — sweeping them onto the parked branch would strip
        // them from master's checkout. --allow-empty: the sleeping commit is
        // the park timestamp even when current.py is already committed.
        git.checked(&["add", "current.py"]);
        git.checked(&["commit", "--allow-empty", "-m", &msg]);
        git.checked(&["branch", "-M", &pnum, &slept_branch]);
        git.checked(&["checkout", "master"]);
        println!(
            "WIP parked on branch {slept_branch} ({} fought); back on master.",
            hm(fought)
        );
        // the Claude Code pane follows the branch: a fresh conversation on master
        switch_chat(&ctx.root);
    } else if git.branch_exists(&pnum) {
        // park an attempt whose branch exists but isn't checked out: stamp
        // the marker on it, rename, come back to where we were
        git.checked(&["checkout", &pnum]);
        git.checked(&["commit", "--allow-empty", "-m", &msg]);
        git.checked(&["branch", "-M", &pnum, &slept_branch]);
        git.checked(&["checkout", &branch]);
        println!("branch {pnum} parked as {slept_branch}.");
    } else {
        die(&format!(
            "no attempt to park — no branch {pnum}. Parking marks what you are BLOCKED on; start it first (make prepare {pnum})."
        ));
    }

    let statuses = all_statuses(ctx, ev, ctx.today());
    let mut rusty: Vec<String> = input_tree(&pv.map[&pnum].moves, &ctx.nodes)
        .into_iter()
        .filter(|n| statuses.get(n).is_some_and(|s| s.0 != SOLID))
        .collect();
    rusty.sort();
    println!("{pnum}. {title} sleeps until you wake it (make wake {pnum}).");
    println!(
        "kg_next will warm meanwhile: {}",
        if rusty.is_empty() {
            "nothing — its walk is already solid; the simmer alone is the treatment".to_string()
        } else {
            rusty.join(", ")
        }
    );
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_sleep [--wake] [--list] [problem]\n\nPark the current problem until you wake it.\n\n  problem  problem number (default: current branch)\n  --wake   resume a parked problem\n  --list   show park state and exit");
        return;
    }
    let list = args.iter().any(|a| a == "--list");
    let do_wake = args.iter().any(|a| a == "--wake");
    let problem = args.iter().find(|a| !a.starts_with("--")).cloned();
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let pv = PView::new(ctx.evidenced());
    let ev = Evidence::new(recs);
    if list {
        let lines = sleep_lines(&ctx, &pv, &ev, &all_statuses(&ctx, &ev, ctx.today()));
        if lines.is_empty() {
            println!("nothing parked");
        } else {
            println!("{}", lines.join("\n"));
        }
    } else if do_wake {
        wake(&ctx, &pv, &ev, problem);
    } else {
        park(&ctx, &pv, &ev, problem);
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn hours_and_minutes() {
        assert_eq!(super::hm(59), "0m");
        assert_eq!(super::hm(25 * 60), "25m");
        assert_eq!(super::hm(3 * 3600 + 5 * 60), "3h 05m");
    }
}
