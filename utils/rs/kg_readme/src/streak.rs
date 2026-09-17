// The current streak of solving days, rendered into graph/streak_badge.svg.
//
// A solving day is a UTC calendar day with at least one file in solved/
// that is not a FAILED file: a problem solve or a drill rep, timed or not.
// Days come from the UTC timestamp in the filename. The current streak
// counts back from today; when today has no rep yet it counts back from
// yesterday, since the day is still open. The best streak is the longest
// run anywhere in the history. The badge is green when today already has
// a rep and grey while the day is still open.
//
// Ported from utils/readme/kg_streak_svg (Python) on 2026-09-13.

use std::collections::HashSet;

use chrono::{Duration, NaiveDate, Utc};
use kg::ctx::Ctx;
use regex::Regex;

use crate::common::*;

pub fn solving_days(ctx: &Ctx) -> HashSet<NaiveDate> {
    let re = Regex::new(r"_(\d{4})_(\d{2})_(\d{2})T(\d{2})_(\d{2})_(\d{2})").unwrap();
    let mut days = HashSet::new();
    for e in std::fs::read_dir(ctx.root.join("solved"))
        .expect("solved/")
        .flatten()
    {
        let name = e.file_name().to_string_lossy().to_string();
        if name.contains("FAILED") || kg::clock::is_studied(&name) || !name.ends_with(".py") {
            continue;
        }
        if let Some(m) = re.captures(&name) {
            let n = |i: usize| m[i].parse::<u32>().unwrap();
            if let Some(d) = NaiveDate::from_ymd_opt(n(1) as i32, n(2), n(3)) {
                days.insert(d);
            }
        }
    }
    days
}

pub fn current_streak(days: &HashSet<NaiveDate>, today: NaiveDate) -> i64 {
    let mut d = if days.contains(&today) {
        today
    } else {
        today - Duration::days(1)
    };
    let mut n = 0;
    while days.contains(&d) {
        n += 1;
        d -= Duration::days(1);
    }
    n
}

pub fn best_streak(days: &HashSet<NaiveDate>) -> i64 {
    let mut best = 0;
    for &start in days {
        if days.contains(&(start - Duration::days(1))) {
            continue;
        }
        let mut d = start;
        let mut n = 0;
        while days.contains(&d) {
            n += 1;
            d += Duration::days(1);
        }
        best = best.max(n);
    }
    best
}

pub fn streak_badge(current: i64, best: i64, color: &str) -> String {
    let right = format!(
        "{current} day{} · best {best}",
        if current != 1 { "s" } else { "" }
    );
    badge("streak", &right, color)
}

pub fn render(ctx: &Ctx) {
    let out = ctx.graph_dir().join("streak_badge.svg");
    let days = solving_days(ctx);
    if days.is_empty() {
        println!("no solving days");
        return;
    }
    let today = Utc::now().date_naive();
    let (current, best) = (current_streak(&days, today), best_streak(&days));
    let color = if days.contains(&today) { GREEN } else { MUTED };
    std::fs::write(&out, streak_badge(current, best, color)).expect("write badge");
    println!(
        "wrote {} (streak {current}, best {best}, {} solving days)",
        out.display(),
        days.len()
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    fn days(offsets: &[i64]) -> HashSet<NaiveDate> {
        let d = NaiveDate::from_ymd_opt(2026, 9, 4).unwrap();
        offsets.iter().map(|o| d - Duration::days(*o)).collect()
    }

    #[test]
    fn current_streak_counts_back_from_today() {
        let d = NaiveDate::from_ymd_opt(2026, 9, 4).unwrap();
        assert_eq!(current_streak(&days(&[0, 1, 2, 4]), d), 3);
        assert_eq!(current_streak(&days(&[1, 2, 3]), d), 3);
        assert_eq!(current_streak(&days(&[2, 3]), d), 0);
    }

    #[test]
    fn best_streak_is_the_longest_run() {
        assert_eq!(best_streak(&days(&[0, 5, 6, 7, 8, 20])), 4);
        assert_eq!(best_streak(&HashSet::new()), 0);
    }

    #[test]
    fn badge_is_green_only_when_today_has_a_rep() {
        assert!(streak_badge(3, 9, GREEN).contains(GREEN));
        assert!(streak_badge(3, 9, GREEN).contains("3 days · best 9"));
        assert!(streak_badge(1, 1, MUTED).contains("1 day · best 1"));
    }
}
