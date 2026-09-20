// A problem's own review clock (kg_lib.problem_due and company): opened by
// help, a walk-away or a study, pushed out by a hinted clean rep, and
// retired only once unaided clean reps have held it at 7 and then 21 days
// (PROBLEM_HOLD_DAYS). One grade per day, the day's last attempt.
//
// Until 2026-09-20 the first unaided rep retired the card. Of the 21
// problems recovered that way since June, 11 had come back on the node
// curve, weeks later, and 1 held: the recovery was one retrieval, and the
// memory it built was gone before the curve asked again.

use std::collections::HashMap;

use chrono::{Duration, NaiveDate};

use crate::ctx::{Ctx, PView};
use crate::data::{is_numeric_id, parse_date, pnum_key, Rec};
use crate::drills::{anki_due, ANKI_HARD_FACTOR};
use crate::evidence::Evidence;

pub const PROBLEM_GRADUATING_DAYS: i64 = 3;
/// The retests an unaided rep must survive before the card retires: the
/// first a week after the recovery, the next three weeks after that.
pub const PROBLEM_HOLD_DAYS: [i64; 2] = [7, 21];
pub const OPENS_CARD: [&str; 5] = ["failed", "studied", "learning", "walkthrough", "hint"];

/// A `make studied` file: the problem was read, run, played with, and no
/// attempt was scored. The record carries no moves, so no node sees it;
/// it opens the problem's card like a copied solution and cools the
/// problem as a carrier (status::last_solved), so the next serve is a
/// repeat and not tomorrow.
pub fn is_studied(fname: &str) -> bool {
    fname.contains("STUDIED")
}

/// kg_lib.attempt_label: failed / studied / unmapped / struggled / clean /
/// the level.
pub fn attempt_label(fname: &str, rec: &Rec) -> String {
    if fname.contains("FAILED") {
        return "failed".into();
    }
    if is_studied(fname) {
        return "studied".into();
    }
    if rec.moves.is_empty() {
        return "unmapped".into();
    }
    if rec.moves.values().any(|v| v != "clean") {
        return "struggled".into();
    }
    let level = rec.assist_any();
    if level == "none" {
        "clean".into()
    } else {
        level.to_string()
    }
}

/// kg_lib.problem_grade: good / hard / again, or None when it grades nothing.
pub fn problem_grade(fname: &str, rec: &Rec) -> Option<&'static str> {
    match attempt_label(fname, rec).as_str() {
        "clean" => Some("good"),
        "hint" => Some("hard"),
        "unmapped" => None,
        _ => Some("again"),
    }
}

/// The review backlog on `day`, from the evidence on file: (open cards,
/// due cards, due drills). An open card is a problem on a review clock
/// of its own (problem_due); it is due once the clock has run out. A due
/// drill is a bank file done at least once whose SM-2 clock (anki_due)
/// has run out. The README's backlog chart draws this day by day and
/// kg_simulate reports it at the end of every simulated day.
pub fn backlog(ctx: &Ctx, ev: &Evidence, day: NaiveDate) -> (i64, i64, i64) {
    let cards: Vec<NaiveDate> = ev
        .by_problem
        .keys()
        .filter(|p| p.chars().next().is_some_and(|c| c.is_ascii_digit()))
        .filter_map(|p| problem_due(ev, p))
        .map(|c| c.0)
        .collect();
    let drills = ctx
        .every_bank_path()
        .iter()
        .filter(|p| anki_due(ctx, p, ev).is_some_and(|a| a.0 <= day))
        .count();
    (
        cards.len() as i64,
        cards.iter().filter(|&&d| d <= day).count() as i64,
        drills as i64,
    )
}

/// kg_lib.problem_attempts: (date, fname, rec index), oldest first.
pub fn problem_attempts<'a>(ev: &'a Evidence, pnum: &str) -> Vec<(&'a str, &'a str, usize)> {
    let mut out = ev.problem_recs(pnum);
    out.sort_by(|a, b| (a.0, a.1).cmp(&(b.0, b.1)));
    out
}

/// kg_lib.problem_due: (due date, interval) for the problem's card, or None.
pub fn problem_due(ev: &Evidence, pnum: &str) -> Option<(NaiveDate, i64)> {
    let mut by_day: Vec<(&str, &str, usize)> = Vec::new();
    for (d, fname, i) in problem_attempts(ev, pnum) {
        if problem_grade(fname, ev.rec(i)).is_some() {
            match by_day.iter_mut().find(|(day, _, _)| *day == d) {
                Some(slot) => {
                    slot.1 = fname;
                    slot.2 = i;
                }
                None => by_day.push((d, fname, i)),
            }
        }
    }
    by_day.sort_by(|a, b| a.0.cmp(b.0));
    let (mut interval, mut last, mut holds): (i64, Option<&str>, usize) = (0, None, 0);
    for (d, fname, i) in by_day {
        let rec = ev.rec(i);
        let answer = problem_grade(fname, rec).unwrap();
        if interval == 0 && !OPENS_CARD.contains(&attempt_label(fname, rec).as_str()) {
            continue;
        }
        match answer {
            "good" => {
                if holds == PROBLEM_HOLD_DAYS.len() {
                    interval = 0;
                    last = None;
                    holds = 0;
                } else {
                    interval = PROBLEM_HOLD_DAYS[holds];
                    last = Some(d);
                    holds += 1;
                }
            }
            "hard" => {
                interval = if interval == 0 {
                    PROBLEM_GRADUATING_DAYS
                } else {
                    (interval + 1).max((interval as f64 * ANKI_HARD_FACTOR + 0.5) as i64)
                };
                last = Some(d);
            }
            _ => {
                interval = PROBLEM_GRADUATING_DAYS;
                last = Some(d);
                holds = 0;
            }
        }
    }
    let last = last?;
    Some((parse_date(last) + Duration::days(interval), interval))
}

/// A problem recovered and waiting for the retest that shows it held:
/// its card is open and the last graded attempt was an unaided clean
/// one. Returns the recovery date.
pub fn recovered_on(ev: &Evidence, pnum: &str) -> Option<NaiveDate> {
    problem_due(ev, pnum)?;
    let (when, label) = last_attempt(ev, pnum)?;
    (label == "clean").then_some(when)
}

/// The moves the recovery has to hold: of the moves the recovering solve
/// walked, the ones that were not clean or carried help on an attempt
/// since the card last opened. When the bad attempts were judged on other
/// moves (a wrong approach, 684 failed on a depth first search and was
/// recovered with union find), every move of the recovering solve.
pub fn recovery_moves(ev: &Evidence, pnum: &str) -> Vec<String> {
    let mut run: Vec<usize> = Vec::new();
    for (_, fname, i) in problem_attempts(ev, pnum) {
        let rec = ev.rec(i);
        if problem_grade(fname, rec) == Some("again") {
            run.clear();
        }
        run.push(i);
    }
    let Some(&last) = run.last() else {
        return vec![];
    };
    let walked: Vec<String> = ev.rec(last).moves.keys().cloned().collect();
    let mut weak: Vec<String> = Vec::new();
    for i in run {
        let rec = ev.rec(i);
        for (m, v) in &rec.moves {
            let helped = match &rec.assist {
                crate::data::Assist::None => false,
                crate::data::Assist::Level(l) => l != "none",
                crate::data::Assist::Map(map) => map.get(m).is_some_and(|l| l != "none"),
            };
            if (v != "clean" || helped) && walked.contains(m) && !weak.contains(m) {
                weak.push(m.clone());
            }
        }
    }
    if weak.is_empty() {
        walked
    } else {
        weak
    }
}

/// kg_lib.due_problems: [(pnum, due, interval)] most overdue first, limited
/// to the problems the view carries.
pub fn due_problems(
    ev: &Evidence,
    today: NaiveDate,
    pv: Option<&PView>,
) -> Vec<(String, NaiveDate, i64)> {
    let mut out = Vec::new();
    for pnum in ev.by_problem.keys() {
        if !is_numeric_id(pnum) || pv.is_some_and(|p| !p.contains(pnum)) {
            continue;
        }
        let cached = ev
            .cold_cache()
            .problem_due
            .as_ref()
            .and_then(|m| m.get(pnum).copied());
        let due = match cached {
            Some(d) => d,
            None => {
                let d = problem_due(ev, pnum);
                ev.cold_cache()
                    .problem_due
                    .get_or_insert_with(HashMap::new)
                    .insert(pnum.clone(), d);
                d
            }
        };
        if let Some((d, i)) = due {
            if d <= today {
                out.push((pnum.clone(), d, i));
            }
        }
    }
    out.sort_by_key(|t| (t.1, pnum_key(&t.0)));
    out
}

/// kg_lib.last_attempt: (date, label) of the latest graded attempt.
pub fn last_attempt(ev: &Evidence, pnum: &str) -> Option<(NaiveDate, String)> {
    for (d, fname, i) in problem_attempts(ev, pnum).into_iter().rev() {
        let rec = ev.rec(i);
        if problem_grade(fname, rec).is_some() {
            return Some((parse_date(d), attempt_label(fname, rec)));
        }
    }
    None
}
