// estimate - print today's readiness snapshot. No LLM, and nothing stored:
// every consumer (README chart, progress bars, dashboard) recomputes these
// numbers on the fly from git + the technique graph, so this is display
// only.
//
// The projected dates come from the Monte-Carlo mock model (utils/rs/kg_mock):
// contest = hard-competent (central P(single hard) >= 50%), onsite = central
// P(onsite) >= 50%. kg_predict's work-done date rides along for comparison.
//
// Ported from utils/kg/estimate (Python) on 2026-09-12.

use std::process::Command;

use chrono::Utc;
use kg::console::Console;
use kg::ctx::Ctx;
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::model::target_pass_rate;
use kg::status::{all_statuses, FRAGILE, MISSING, SOLID, STALE};
use kg::table::{print_table, Table};
use serde_json::Value;

/// Python's `%g` for the plain floats these JSON files hold.
fn py_g(v: f64) -> String {
    if v == v.trunc() && v.abs() < 1e16 {
        return format!("{}", v as i64);
    }
    let s = format!("{:.6}", v);
    let s = s.trim_end_matches('0').trim_end_matches('.');
    s.to_string()
}

fn json_of(console: &Console, cmd: &mut Command, what: &str, unavailable: &str) -> Option<Value> {
    match cmd.output() {
        Ok(out) if out.status.success() => match serde_json::from_slice::<Value>(&out.stdout) {
            Ok(v) => Some(v),
            Err(e) => {
                console.print(&format!(
                    "[yellow]{what} failed, {unavailable}: {e}[/yellow]"
                ));
                None
            }
        },
        Ok(out) => {
            console.print(&format!(
                "[yellow]{what} failed, {unavailable}: exited {}[/yellow]",
                out.status.code().unwrap_or(1)
            ));
            None
        }
        Err(e) => {
            console.print(&format!(
                "[yellow]{what} failed, {unavailable}: {e}[/yellow]"
            ));
            None
        }
    }
}

fn main() {
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let ev = Evidence::new(recs);
    let console = Console::full_width();
    let statuses = all_statuses(&ctx, &ev, ctx.today());
    let count = |s| statuses.values().filter(|(st, _)| *st == s).count();
    let status_line = format!(
        "{} SOLID, {} STALE, {} FRAGILE, {} MISSING (of {} technique nodes)",
        count(SOLID),
        count(STALE),
        count(FRAGILE),
        count(MISSING),
        ctx.nodes.len()
    );
    let run_date = (Utc::now() + chrono::Duration::hours(8))
        .format("%Y-%m-%d")
        .to_string();

    // work-done date from the curve simulator (utils/rs/kg_predict): when the
    // graph would be fully solid + enough mediums banked + a polish block
    // the sibling binaries of this workspace build
    let sibling = |name: &str| {
        std::env::current_exe()
            .ok()
            .and_then(|p| p.parent().map(|d| d.join(name)))
            .unwrap_or_else(|| ctx.root.join("utils/rs/target/release").join(name))
    };
    let predict = json_of(
        &console,
        Command::new(sibling("kg_predict"))
            .arg("--json")
            .current_dir(&ctx.root),
        "kg_predict",
        "no work-done date",
    );
    // Monte-Carlo milestone dates from `make mock` (utils/rs/kg_mock): contest =
    // hard-competent (central P(single hard) >= 50%), onsite = central
    // P(onsite) >= 50%. These headline the README progress bars.
    let mock = json_of(
        &console,
        Command::new(sibling("kg_mock"))
            .arg("--json")
            .current_dir(&ctx.root),
        "kg_mock",
        "no mock milestones",
    );

    let mut table = Table::bare(&["k", "v"], false, 2);
    table.add_row(&["Run date".to_string(), run_date]);
    table.add_row(&["Node statuses".to_string(), status_line]);
    if let Some(mock) = &mock {
        // a milestone the forward simulation never reaches inside its horizon
        // prints as such rather than as a bare None
        let unreached = "not within 18 months at this pace";
        let text = |v: &Value| v.as_str().filter(|s| !s.is_empty()).map(String::from);
        table.add_row(&[
            "Contest (mock hard-competent)".to_string(),
            text(&mock["hard_competent"]).unwrap_or_else(|| unreached.to_string()),
        ]);
        let onsite = match text(&mock["onsite_ready"]) {
            Some(d) => format!(
                "{d} at {}h/day",
                py_g(mock["hours"].as_f64().unwrap_or(0.0))
            ),
            None => unreached.to_string(),
        };
        table.add_row(&[
            format!(
                "Onsite (mock P(onsite)>={}%)",
                kg::table::py_round(target_pass_rate() * 100.0) as i64
            ),
            onsite,
        ]);
    }
    if let Some(p) = &predict {
        table.add_row(&[
            "Work done (kg_predict)".to_string(),
            format!(
                "{} at {}h/day",
                p["ready"].as_str().unwrap_or("None"),
                py_g(p["hours"].as_f64().unwrap_or(0.0))
            ),
        ]);
    }
    print_table(&console, &table);
}

#[cfg(test)]
mod tests {
    #[test]
    fn g_format() {
        assert_eq!(super::py_g(2.0), "2");
        assert_eq!(super::py_g(2.4), "2.4");
        assert_eq!(super::py_g(1.25), "1.25");
    }
}
