// kg_simulate - drive the real picker forward, one day at a time, until the
// central onsite pass rate reaches the target.
//
//   make simulate              # at the measured pace
//   make simulate 2            # 2 hours/day instead
//   make simulate seed 7       # another draw of the same policy
//
// Pace is measured, not assumed. Hours per day: minutes solved over the
// last 28 calendar days, lapses included, cut at a dead week (kg_mock_rs
// week_pace, the "avg of the current streak" make mock prints). Price of
// an attempt: the median timed minutes of your own attempts of that kind
// (Easy, Medium, Hard, drill) and verdict (clean, struggled), from the
// `solve time` trailers in the git log joined to evidence.json.
//
// Each simulated day: call kg::pick::pick on the simulated evidence (the
// same function `make next` runs, sleep and once-a-day rules included),
// draw the outcome of every move on its walk from the fitted forgetting
// curve (graph/curve.json; a first exposure uses the measured first-contact
// absorption). A problem never seen before also has to pass the pass
// model's own cold-solve odds (kg::model::solve_logit, the fitted model
// pass_rates scores an interview problem by: contest rating, walk recall,
// never-met moves); when it does not, the least-recalled move on the walk
// is the one recorded as struggled. Charge the attempt at the measured
// price for its verdict, append a record shaped like the one kg_extract
// writes, and repeat until the hours are spent. A struggled move goes
// FRAGILE the way it does for real, and the picker spends the next days
// repairing it. At the end of the day, the pass model behind `make mock`'s
// cold estimate on the simulated evidence - in closed form
// (expect::PassExpectation): the exact expectation of the sets
// kg_lib.pass_rates draws, without the draws.
//
// What `make predict` and `make mock` do not do: run the picker itself.
// Both simulate a policy of their own. This runs the policy that serves
// you, so a picker that starves or loops shows up here: days with no
// progress, and nodes that stay STALE or FRAGILE for weeks (the "picker
// starved" lines at the end; the tests below hold the caps).
//
// No mocks are simulated: a cold first solve is the same test, and the
// fitted model reads the walk, not a practice counter.
//
// The drill bank grows during the run the way it grows in the git log.
// The rate is measured: nodes whose first bank file landed in the last 28
// days, per calendar day (bank_rate; `make simulate bank-rate 0.5` sets
// it, 0 runs on the bank as it is). Each day earns that much of a bank;
// each whole bank goes to the bankless node the day's picks touched -
// the pick's target first, a struggled move before a clean one, the
// least-recalled move otherwise - and, with nothing touched, the least-
// recalled bankless node. Its size is drawn from the sizes of the banks
// on disk. A virtual bank file lives in a scratch copy of drills/ that the
// picker reads for the run: it trains its node, comes after nothing, and
// goes through due_drill's holds and the drill gate like a real one.
// Writing it costs no hours: pace is measured from solve time trailers,
// and authoring was never in them.
//
// Every attempt on a numbered problem is also returned as a row for the
// README's problem-rating chart (kg_readme problem-rating draws the run
// after the history), and a first sight is scored as an Elo game while it
// is at it: the cold-solve draw above IS the game. kg_curve fits that
// model on scored games - a win is unaided and inside the budget, a solve
// over the clock is a loss - so its odds already price the clock, and the
// draw that decides whether the walk holds up cold is the draw that
// decides the game. No second model of the solve time sits on top of it.
//
// The run is the picker on its own rules: every knob the repo's .envrc
// sets (the drill scheduler, the caps, the group caps) is dropped from the
// environment for the run and put back after, the way conftest drops them
// for the test suite. The operator's knobs are a session's preferences
// and moved with them - the anki scheduler and the one-new-drill cap ran
// the picker dry of problems after ten weeks on 2026-09-12 - so the
// forecast is of the picker, not of the .envrc of the day.
// TARGET_PASS_RATE is the exception: it says what "ready" means, is read
// first, and is honoured.
//
// The random stream is CPython's (kg::mock::PyRandom), so a seed draws the
// trajectory the Python original drew.
//
// Not modelled: fission of the taxonomy, assists, lapses in the hours.
// One trajectory per seed; run a few seeds for the spread.
//
// Ported from utils/kg/kg_simulate (Python) on 2026-09-14.

mod expect;
mod sim;

use chrono::Duration;
use kg::ctx::Ctx;
use kg::data::{load_envrc, repo_root};
use kg::status::STARVED_DAYS;
use serde_json::json;

use sim::{RunArgs, MAX_DAYS};

const USAGE: &str = "usage: kg_simulate [hours] [--seed N] [--days N] [--every N] \
[--draft-error X] [--bank-rate X] [--attempts-json | --json | --rates-json]";

struct Args {
    run: RunArgs,
    attempts_json: bool,
    json: bool,
    rates_json: bool,
}

fn parse_args() -> Args {
    let mut a = Args {
        run: RunArgs {
            hours: None,
            seed: 1,
            days: MAX_DAYS,
            every: 7,
            draft_error: 0.0,
            bank_rate: None,
        },
        attempts_json: false,
        json: false,
        rates_json: false,
    };
    let argv: Vec<String> = std::env::args().skip(1).collect();
    let mut i = 0;
    let value = |i: &mut usize, name: &str| -> String {
        *i += 1;
        argv.get(*i)
            .cloned()
            .unwrap_or_else(|| die(&format!("{name} needs a value")))
    };
    while i < argv.len() {
        let arg = argv[i].as_str();
        match arg {
            "--seed" => a.run.seed = num(&value(&mut i, arg), arg),
            "--days" => a.run.days = num(&value(&mut i, arg), arg),
            "--every" => a.run.every = num(&value(&mut i, arg), arg),
            "--draft-error" => a.run.draft_error = num(&value(&mut i, arg), arg),
            "--bank-rate" => a.run.bank_rate = Some(num(&value(&mut i, arg), arg)),
            "--attempts-json" => a.attempts_json = true,
            "--json" => a.json = true,
            "--rates-json" => a.rates_json = true,
            "-h" | "--help" => {
                println!("{USAGE}");
                std::process::exit(0);
            }
            _ if a.run.hours.is_none() && !arg.starts_with('-') => {
                a.run.hours = Some(num(arg, "hours"));
            }
            _ => die(&format!("unknown argument {arg}\n{USAGE}")),
        }
        i += 1;
    }
    a
}

fn num<T: std::str::FromStr>(s: &str, name: &str) -> T {
    s.parse()
        .unwrap_or_else(|_| die(&format!("{name}: not a number: {s}")))
}

fn die(msg: &str) -> ! {
    eprintln!("{msg}");
    std::process::exit(2)
}

fn main() {
    let args = parse_args();
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let quiet = args.attempts_json || args.json || args.rates_json;
    let print = |s: &str| println!("{s}");
    let log: Option<&dyn Fn(&str)> = if quiet { None } else { Some(&print) };
    let r = sim::run(&ctx, recs, &args.run, log);
    let target = kg::model::target_pass_rate();
    let date = |d: chrono::NaiveDate| d.format("%Y-%m-%d").to_string();
    let counts = |m: &indexmap::IndexMap<String, i64>| -> serde_json::Value {
        m.iter()
            .map(|(k, v)| (k.clone(), json!(v)))
            .collect::<serde_json::Map<_, _>>()
            .into()
    };
    let attempts: Vec<serde_json::Value> = r
        .attempts
        .iter()
        .map(|a| {
            json!({
                "date": date(a.date),
                "problem": a.problem,
                "difficulty": a.difficulty,
                "rating": a.rating,
                "first": a.first,
                "score": a.score,
            })
        })
        .collect();
    if args.rates_json {
        let (onsite, screen, hard) = r.today_rates;
        println!(
            "{}",
            json!({"onsite": onsite, "screen": screen, "hard": hard})
        );
        return;
    }
    if args.attempts_json {
        println!(
            "{}",
            kg::pyjson::dumps(&json!({"start": date(r.start), "attempts": attempts}), None)
        );
        return;
    }
    if args.json {
        println!(
            "{}",
            json!({
                "day": r.day,
                "start": date(r.start),
                "onsite": r.onsite,
                "hours": r.hours,
                "source": r.source,
                "per_kind": counts(&r.per_kind),
                "dry_days": r.dry_days,
                "short_days": r.short_days,
                "rusty": r.rusty,
                "starved": counts(&r.starved),
                "series": r.series.iter().map(|d| json!({
                    "day": date(d.day),
                    "solves": counts(&d.solves),
                    "stale": d.stale,
                    "fragile": d.fragile,
                    "missing": d.missing,
                    "onsite": d.onsite,
                    "screen": d.screen,
                    "hard": d.hard,
                })).collect::<Vec<_>>(),
                "attempts": attempts,
                "authored": {
                    "nodes": r.authored.nodes,
                    "files": r.authored.files,
                    "rate": r.authored.rate,
                    "source": r.authored.source,
                },
            })
        );
        return;
    }
    println!();
    if r.onsite >= target {
        println!(
            "central P(onsite) >= {:.0}% on day {}: {}",
            target * 100.0,
            r.day,
            date(r.start + Duration::days(r.day))
        );
    } else {
        println!(
            "not reached in {} days (P(onsite) {:.0}%)",
            r.day,
            r.onsite * 100.0
        );
    }
    println!(
        "solves: {}; {} in {} days at {}h/day",
        r.per_kind
            .iter()
            .map(|(k, v)| format!("{k} {v}"))
            .collect::<Vec<_>>()
            .join(", "),
        r.per_kind.values().sum::<i64>(),
        r.day,
        kg::pyjson::g(r.hours)
    );
    println!(
        "drills authored: {} files for {} nodes at {} banks/day ({})",
        r.authored.files,
        r.authored.nodes,
        kg::pyjson::g(r.authored.rate),
        r.authored.source
    );
    println!(
        "picker dry: {} days served nothing, {} days ran out before half the hours were used",
        r.dry_days, r.short_days
    );
    let worst = r.rusty.iter().map(|(_, s, f, _)| s + f).max().unwrap_or(0);
    println!("rusty: at most {worst} nodes STALE or FRAGILE at the start of a day");
    if !r.starved.is_empty() {
        println!("picker starved ({STARVED_DAYS}+ days rusty in a row, nothing aimed at it):");
        let mut rows: Vec<(&String, &i64)> = r.starved.iter().collect();
        rows.sort_by_key(|(_, k)| -**k);
        for (n, k) in rows {
            println!("  {n}: {k} days");
        }
    }
}
