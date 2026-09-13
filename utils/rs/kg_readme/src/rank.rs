// Where the current Elo sits in LeetCode's rated population, rendered into
// graph/rank_all_badge.svg and graph/rank_regulars_badge.svg.
//
// The population data is the snapshot in data/leetcode_rank_table.json,
// written by `kg_readme rank-table`. Against all rated users the badge
// interpolates the count at or above the Elo between the table's 25-point
// rows. Against regulars (users with 20 or more contests) it is the share
// of the sampled regulars rated at or above the Elo.
//
// Ported from utils/readme/kg_rank_svg (Python) on 2026-09-13.

use kg::ctx::Ctx;
use kg::evidence::Evidence;
use serde_json::Value;

use crate::common::*;

/// Share of all rated users at or above elo, from the 25-point rows,
/// linearly interpolated; clamped to the table's ends.
pub fn top_share_all(table: &Value, elo: f64) -> f64 {
    let total = table["total"].as_f64().unwrap();
    let rows: Vec<(f64, f64)> = table["rows"]
        .as_array()
        .unwrap()
        .iter()
        .map(|r| (r[0].as_f64().unwrap(), r[1].as_f64().unwrap()))
        .collect();
    if elo <= rows[0].0 {
        return rows[0].1 / total;
    }
    if elo >= rows[rows.len() - 1].0 {
        return rows[rows.len() - 1].1 / total;
    }
    for w in rows.windows(2) {
        let ((r0, n0), (r1, n1)) = (w[0], w[1]);
        if r0 <= elo && elo <= r1 {
            return (n0 + (n1 - n0) * (elo - r0) / (r1 - r0)) / total;
        }
    }
    panic!("rows are not sorted")
}

/// Share of the sampled regulars rated at or above elo.
pub fn top_share_regulars(sample: &Value, elo: f64) -> f64 {
    let ratings = sample["ratings"].as_array().unwrap();
    ratings
        .iter()
        .filter(|r| r.as_f64().unwrap() >= elo)
        .count() as f64
        / ratings.len() as f64
}

pub fn render(ctx: &Ctx, ev: &Evidence) {
    let table: Value = serde_json::from_str(
        &std::fs::read_to_string(ctx.root.join("data/leetcode_rank_table.json"))
            .expect("rank table"),
    )
    .unwrap();
    let elo = crate::elo::current(ctx, ev);
    let share_all = top_share_all(&table["all"], elo);
    let share_reg = top_share_regulars(&table["regulars"], elo);
    let all = ctx.graph_dir().join("rank_all_badge.svg");
    let reg = ctx.graph_dir().join("rank_regulars_badge.svg");
    std::fs::write(
        &all,
        badge(
            "vs all rated",
            &format!("top {}%", f0(100.0 * share_all)),
            MUTED,
        ),
    )
    .unwrap();
    std::fs::write(
        &reg,
        badge(
            "vs 20+ contests",
            &format!("top {}%", f0(100.0 * share_reg)),
            MUTED,
        ),
    )
    .unwrap();
    println!(
        "elo {}: top {}% of {} rated, top {}% of {} sampled regulars ({})",
        f0(elo),
        f1(100.0 * share_all),
        table["all"]["total"],
        f1(100.0 * share_reg),
        table["regulars"]["ratings"].as_array().unwrap().len(),
        table["date"].as_str().unwrap_or("")
    );
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn all() -> Value {
        json!({"total": 1000, "rows": [[1500, 400], [1525, 300], [1550, 200]]})
    }

    #[test]
    fn all_reads_a_row_interpolates_and_clamps() {
        assert_eq!(top_share_all(&all(), 1525.0), 0.3);
        assert_eq!(top_share_all(&all(), 1540.0), 0.24);
        assert_eq!(top_share_all(&all(), 1200.0), 0.4);
        assert_eq!(top_share_all(&all(), 3000.0), 0.2);
    }

    #[test]
    fn regulars_counts_at_or_above() {
        let reg = json!({"ratings": [1400.0, 1500.0, 1600.0, 1700.0]});
        assert_eq!(top_share_regulars(&reg, 1600.0), 0.5);
        assert_eq!(top_share_regulars(&reg, 1601.0), 0.25);
    }
}
