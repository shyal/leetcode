// A fail is not finished until it has a drill (settled 2026-09-28).
//
// A fail filed by `make failed` stays open until
// the problem's `after` list in graph/problems.json names a drill, the way
// 799 names d147; while any open fail lacks one, nothing new is served:
// kg_next serves drills only and names the problems waiting; kg_llm_next
// and prepare <n> refuse outright. The drill is the way out and the only
// one.
//
// `FAIL_GATE=0` in .envrc switches the gate off (2026-10-06); unset or
// anything else keeps it on. Off, open_fails reports nothing, so every
// caller serves as if no fail waited.
//
// This gate is the repo's own; the health hooks in hooks.rs are separate
// and untouched.

use std::collections::{HashMap, HashSet};

use crate::ctx::Ctx;
use crate::data::env_str;
use crate::evidence::{drill_key, Evidence};

/// FAIL_GATE=0 switches the gate off; unset or anything else keeps it on.
pub fn enabled() -> bool {
    env_str("FAIL_GATE").trim() != "0"
}

/// The problems whose `after` list in graph/problems.json names a drill:
/// a drill has been built for them.
pub fn covered(ctx: &Ctx) -> HashSet<String> {
    ctx.ro
        .map
        .iter()
        .filter(|(_, p)| p.after.iter().any(|a| ctx.drills.contains_key(a)))
        .map(|(id, _)| id.clone())
        .collect()
}

/// (problem, date of the fail) for every problem whose latest fail has no
/// clean unaided problem rep after it and no drill built for it, oldest
/// fail first. Empty while FAIL_GATE=0.
pub fn open_fails(ev: &Evidence, covered: &HashSet<String>) -> Vec<(String, String)> {
    if !enabled() {
        return Vec::new();
    }
    let mut last_fail: HashMap<String, String> = HashMap::new();
    let mut last_clean: HashMap<String, String> = HashMap::new();
    for (path, rec) in &ev.recs {
        let Some(pnum) = rec
            .problem
            .clone()
            .filter(|p| p != "drill" && !p.is_empty())
        else {
            continue;
        };
        if drill_key(path).is_some() {
            continue;
        }
        let slot = if path.contains("_FAILED_") {
            &mut last_fail
        } else if rec.assist_any() == "none" && rec.moves.values().all(|v| v == "clean") {
            &mut last_clean
        } else {
            continue;
        };
        let e = slot.entry(pnum).or_default();
        if rec.date > *e {
            *e = rec.date.clone();
        }
    }
    let mut out: Vec<(String, String)> = last_fail
        .into_iter()
        .filter(|(p, d)| !covered.contains(p) && last_clean.get(p).is_none_or(|c| c < d))
        .collect();
    out.sort_by(|a, b| a.1.cmp(&b.1).then(a.0.cmp(&b.0)));
    out
}

/// The refusal, as sentences: one per waiting problem, then what to do.
pub fn refusal_text(ctx: &Ctx, fails: &[(String, String)]) -> String {
    let mut lines = Vec::new();
    for (p, d) in fails {
        let title = ctx.ro.map.get(p).map(|x| x.title.as_str()).unwrap_or("");
        lines.push(format!(
            "{p}. {title} failed on {d} and no drill has been built for it."
        ));
    }
    lines.push(
        "No problem is served until each has one: a drill on the move named in the failure note, and the problem's after list in graph/problems.json naming it. Drills still come.".to_string(),
    );
    lines.join("\n")
}

/// Refuse to serve a problem while an open fail has no drill.
pub fn gate(ctx: &Ctx, ev: &Evidence) {
    let fails = open_fails(ev, &covered(ctx));
    if !fails.is_empty() {
        println!("{}", refusal_text(ctx, &fails));
        std::process::exit(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::data::{test_env, Rec};
    use serde_json::json;

    fn rec(date: &str, problem: &str, verdict: &str, assist: Option<&str>) -> Rec {
        let mut v = json!({"date": date, "problem": problem, "moves": {"m": verdict}});
        if let Some(a) = assist {
            v["assist"] = json!(a);
        }
        Rec::parse(&v)
    }

    #[test]
    fn open_fails_are_uncovered_fails_without_a_clean_rep_after() {
        let ev = Evidence::new(vec![
            (
                "solved/p1_A_FAILED_x.py".into(),
                rec("2026-09-01", "1", "struggled", None),
            ),
            (
                "solved/p1_A_y.py".into(),
                rec("2026-09-05", "1", "clean", None),
            ),
            (
                "solved/p2_B_FAILED_x.py".into(),
                rec("2026-09-02", "2", "struggled", None),
            ),
            (
                "solved/p2_B_y.py".into(),
                rec("2026-09-06", "2", "clean", Some("learning")),
            ),
            (
                "solved/p3_C_FAILED_x.py".into(),
                rec("2026-09-03", "3", "struggled", None),
            ),
            (
                "solved/p4_D_FAILED_x.py".into(),
                rec("2026-08-30", "4", "struggled", None),
            ),
            (
                "solved/d_E_FAILED_x.py".into(),
                rec("2026-09-04", "drill", "struggled", None),
            ),
        ]);
        let covered: HashSet<String> = ["3".to_string()].into();
        // 1 passed clean after; 2's rep after was assisted; 3 has a drill;
        // 4 is the oldest open fail; the drill fail is not a problem
        assert_eq!(
            open_fails(&ev, &covered),
            vec![
                ("4".to_string(), "2026-08-30".to_string()),
                ("2".to_string(), "2026-09-02".to_string())
            ]
        );
    }

    #[test]
    fn fail_gate_0_reports_no_open_fail() {
        let ev = Evidence::new(vec![(
            "solved/p4_D_FAILED_x.py".into(),
            rec("2026-08-30", "4", "struggled", None),
        )]);
        let covered: HashSet<String> = HashSet::new();
        assert_eq!(open_fails(&ev, &covered).len(), 1);
        test_env("FAIL_GATE", "0");
        assert!(!enabled());
        assert!(open_fails(&ev, &covered).is_empty());
        test_env("FAIL_GATE", "1");
        assert!(enabled());
        assert_eq!(open_fails(&ev, &covered).len(), 1);
    }
}
