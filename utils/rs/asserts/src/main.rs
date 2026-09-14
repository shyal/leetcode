// asserts - generate the extra asserts for the problems the picker is about
// to serve.
//
//   asserts --next 5           # the picker's next five problems, in order
//   asserts 2349 1912          # just those cached numbers
//   asserts --next 5 --dry     # print the asserts instead of caching them
//   asserts --model haiku --jobs 2 ...
//
// The asserts come from prepare::assert_gen, one self-contained line each,
// frozen by running the validated reference solution in the prepare cache.
// Running it again on the same problem grows the block: the model is handed
// the labels already covered and hunts for the ones they miss. `--next N`
// replays the picker N problems ahead (kg::pick::upcoming) and does them in
// order, so a pick arrives with its coverage already cached; explicit
// numbers do just those.
//
// The asserts are folded into .prepare_cache/<num>.json, which is where
// `make prepare` reads them from; `--dry` prints them instead. Nothing here
// touches current.py, a branch, or anything under solved/.
//
// Ported from utils/kg/asserts (Python) on 2026-09-14.

use std::path::Path;
use std::sync::{Arc, Mutex};
use std::time::Duration;

use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::git::sleep_records;
use kg::pick::upcoming;
use prepare::assert_gen::{covered, extra_asserts};
use prepare::stub::strip_solution;
use prepare::{cache_entry, pool, pyrun, write_entry};

const SYSTEM_PROMPT: &str =
    "You generate Python test scaffolding for LeetCode solutions. Output ONLY \
raw Python source - no explanations, no markdown fences, no preamble. Do \
NOT use any tools; the caller writes your stdout straight to disk.";

struct Args {
    nums: Vec<String>,
    next: usize,
    dry: bool,
    model: Option<String>,
    jobs: usize,
}

fn usage() -> ! {
    eprintln!(
        "usage: asserts [--next N] [--dry] [--model M] [--jobs N] [nums...]\n\n  nums     cached leetcode numbers\n  --next N the next N problems the picker would serve\n  --dry    print the asserts instead of caching them\n  --jobs   problems generated concurrently (default 4)"
    );
    std::process::exit(2)
}

fn parse_args() -> Args {
    let mut args = Args {
        nums: Vec::new(),
        next: 0,
        dry: false,
        model: None,
        jobs: 4,
    };
    let mut it = std::env::args().skip(1);
    while let Some(a) = it.next() {
        let (flag, inline) = match a.split_once('=') {
            Some((f, v)) if f.starts_with("--") => (f.to_string(), Some(v.to_string())),
            _ => (a.clone(), None),
        };
        let mut value = || {
            inline
                .clone()
                .or_else(|| it.next())
                .unwrap_or_else(|| usage())
        };
        match flag.as_str() {
            "-h" | "--help" => usage(),
            "--dry" => args.dry = true,
            "--next" => args.next = value().parse().unwrap_or_else(|_| usage()),
            "--jobs" => args.jobs = value().parse().unwrap_or_else(|_| usage()),
            "--model" => args.model = Some(value()),
            _ if a.starts_with("--") => usage(),
            _ => args.nums.push(a),
        }
    }
    args
}

/// The picker's next `count` problem numbers, its own order.
fn next_problems(root: &Path, count: usize) -> Vec<String> {
    let (ctx, recs) = Ctx::load(root.to_path_buf());
    let pv = PView::new(ctx.evidenced());
    let ev = Evidence::new(recs);
    let asleep: Vec<String> = sleep_records(&ctx, &pv, &ev)
        .into_iter()
        .map(|r| r.pnum)
        .collect();
    upcoming(&ctx, &pv, &ev, count, &asleep, 30)
}

/// Execute a source file the way prepare's validate does.
fn run(root: &Path, code: &str) -> (bool, String) {
    let o = pyrun::run(root, code, Duration::from_secs(120));
    if o.timed_out {
        return (false, format!("{}\nTimed out after 120s.", o.output));
    }
    (o.ok, o.output)
}

/// What the two files have in common - the rest is this pass's work.
fn shared_prefix_len(old: &str, new: &str) -> usize {
    let mut end = old
        .bytes()
        .zip(new.bytes())
        .take_while(|(a, b)| a == b)
        .count();
    while !new.is_char_boundary(end) {
        end -= 1;
    }
    end
}

/// One problem, start to finish. `say` prints it in one piece, so two
/// workers finishing together cannot interleave their output.
fn generate(root: &Path, num: &str, args: &Args, say: &dyn Fn(String)) -> Result<(), String> {
    let mut entry = cache_entry(root, num).ok_or_else(|| format!("no cache entry for {num}"))?;
    let solution = entry
        .get("solution")
        .and_then(|s| s.as_str())
        .unwrap_or("")
        .to_string();
    if solution.is_empty() {
        say(format!("{num}: cache has no reference solution"));
        return Ok(());
    }
    let before = covered(&solution).len();
    let model = args.model.clone();
    let llm =
        |p: &str| kg::llm::text(p, SYSTEM_PROMPT, model.as_deref()).map_err(|e| e.to_string());
    let merged = extra_asserts(&solution, &llm, &|c| run(root, c))?;
    if merged == solution {
        say(format!("{num}: nothing new"));
        return Ok(());
    }
    let grown = covered(&merged).len() - before;
    if args.dry {
        say(format!(
            "--- {num}: {grown} more edge cases {}\n{}",
            "-".repeat(20),
            &merged[shared_prefix_len(&solution, &merged)..]
        ));
        return Ok(());
    }
    let code = strip_solution(&merged)?;
    entry["solution"] = serde_json::Value::String(merged);
    entry["code"] = serde_json::Value::String(code);
    write_entry(root, num, &entry);
    say(format!(
        "{num}: cached, {grown} more edge cases ({} total)",
        before + grown
    ));
    Ok(())
}

fn main() {
    let args = parse_args();
    let root = repo_root();
    load_envrc(&root);
    let nums = if args.nums.is_empty() {
        next_problems(&root, if args.next == 0 { 5 } else { args.next })
    } else {
        args.nums.clone()
    };
    let jobs = args.jobs;
    let shared = Arc::new((root, args, Mutex::new(())));
    pool(nums, jobs, move |num| {
        let (root, args, lock) = &*shared;
        let say = |text: String| {
            let _g = lock.lock().unwrap();
            println!("{text}");
        };
        if let Err(e) = generate(root, &num, args, &say) {
            say(format!("{num}: failed ({e})"));
        }
    });
}
