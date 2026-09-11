// A problem's own review clock (kg_lib.problem_due and company): opened by
// help or a walk-away, pushed out by a hinted clean rep, retired by an
// unaided clean one. One grade per day, the day's last attempt.

use std::collections::HashMap;

use chrono::{Duration, NaiveDate};

use crate::ctx::PView;
use crate::data::{is_numeric_id, parse_date, pnum_key, Rec};
use crate::drills::ANKI_HARD_FACTOR;
use crate::evidence::Evidence;

pub const PROBLEM_GRADUATING_DAYS: i64 = 3;
pub const OPENS_CARD: [&str; 4] = ["failed", "learning", "walkthrough", "hint"];

/// kg_lib.attempt_label: failed / unmapped / struggled / clean / the level.
pub fn attempt_label(fname: &str, rec: &Rec) -> String {
    if fname.contains("FAILED") {
        return "failed".into();
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
    let (mut interval, mut last): (i64, Option<&str>) = (0, None);
    for (d, fname, i) in by_day {
        let rec = ev.rec(i);
        let answer = problem_grade(fname, rec).unwrap();
        if interval == 0 && !OPENS_CARD.contains(&attempt_label(fname, rec).as_str()) {
            continue;
        }
        match answer {
            "good" => {
                interval = 0;
                last = None;
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
            }
        }
    }
    let last = last?;
    Some((parse_date(last) + Duration::days(interval), interval))
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
    out.sort_by(|a, b| (a.1, pnum_key(&a.0)).cmp(&(b.1, pnum_key(&b.0))));
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
