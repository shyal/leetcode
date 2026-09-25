// The queue: the next problems the picker would serve if every rep is
// clean (pick::upcoming, drills skipped), each with its contest rating
// against his Elo. Printed under every `make next` and by `make queue`;
// `make queue gate` asks a model which plainer problems should gate the
// ones rated well above him.

use crate::ctx::{Ctx, PView};
use crate::evidence::Evidence;
use crate::model::{elo_now, solve_ratings};
use crate::pick::upcoming;
use crate::table::{BoxKind, Table};

pub const QUEUE_LEN: usize = 10;
const DAYS: i64 = 30;

/// One row of the queue: number, title, difficulty, rating (None when the
/// problem has no contest rating), and whether serving it would be a first
/// sight (no record of the problem in the evidence).
pub struct QueueRow {
    pub pnum: String,
    pub title: String,
    pub difficulty: String,
    pub rating: Option<f64>,
    pub first_sight: bool,
}

/// The next `len` problems the picker would serve.
pub fn queue_rows(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    asleep: &[String],
    len: usize,
) -> Vec<QueueRow> {
    let ratings = solve_ratings(ctx);
    upcoming(ctx, pv, ev, len, asleep, DAYS)
        .into_iter()
        .map(|pnum| QueueRow {
            title: pv
                .get(&pnum)
                .or_else(|| ctx.all_problems().get(&pnum))
                .map(|p| p.title.clone())
                .unwrap_or_default(),
            difficulty: ctx.problem_difficulty(&pnum, &pv.map),
            rating: ratings.get(&pnum).copied(),
            first_sight: ev.problem_recs(&pnum).is_empty(),
            pnum,
        })
        .collect()
}

/// The rating line's colour for a gap: red 100 above him, yellow inside
/// 100, green below.
pub fn gap_colour(gap: f64) -> &'static str {
    if gap > 100.0 {
        "red"
    } else if gap > -100.0 {
        "yellow"
    } else {
        "green"
    }
}

/// kg_next.queue_table: the queue as a table, coloured like the rating
/// line, `len` rows long. None when the replay serves nothing.
pub fn queue_table(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    asleep: &[String],
    len: usize,
) -> Option<Table> {
    let rows = queue_rows(ctx, pv, ev, asleep, len);
    if rows.is_empty() {
        return None;
    }
    let elo = elo_now(ctx, ev);
    let mut table = Table::plain(
        &[
            "Problem",
            "Difficulty",
            "Rating",
            "Gap",
            "Odds",
            "First sight",
        ],
        Some(&format!("queue (elo {elo:.0})")),
        BoxKind::Rounded,
    );
    for row in rows {
        let style = match row.difficulty.as_str() {
            "Easy" => "green",
            "Medium" => "yellow",
            "Hard" => "red",
            _ => "dim",
        };
        let [r, g, o] = match row.rating {
            None => ["-".into(), "-".into(), "-".into()],
            Some(rating) => {
                let gap = rating - elo;
                let odds = 1.0 / (1.0 + 10f64.powf(gap / 400.0));
                let colour = gap_colour(gap);
                [
                    format!("[bold]{rating:.0}[/bold]"),
                    format!("[{colour}]{gap:+.0}[/{colour}]"),
                    format!("[{colour}]{:.0}%[/{colour}]", odds * 100.0),
                ]
            }
        };
        table.add_row(&[
            format!("{}. {}", row.pnum, row.title),
            format!("[{style}]{}[/{style}]", row.difficulty),
            r,
            g,
            o,
            if row.first_sight {
                "[green]yes[/green]".into()
            } else {
                "[dim]no[/dim]".into()
            },
        ]);
    }
    Some(table)
}
