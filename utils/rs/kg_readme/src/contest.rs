// The virtual contests (kg::contests, contests/*.json): the badge
// graph/contest_badge.svg, and the header and result table of each
// contest's markdown, rendered into its <!-- CONTEST --> region.
//
// The badge is LeetCode's contest rating (kg::contests::leetcode_rating)
// run over the virtual contests in date order from 1500: LeetCode's own
// formula on the virtual rank against the real field, sampled into
// contests/<stem>.field.json by make contest-field. A virtual contest
// without a field is named and left out. Real contests have LeetCode's
// rating on the site and are left out too.

use kg::contests::{self, Contest, Standing, REGION};
use kg::ctx::Ctx;

use crate::common::*;
use crate::elo::rank_of;
use crate::update::fill;

/// "1687 · 2 contests"
pub fn badge_text(rating: f64, contests: usize) -> String {
    let unit = if contests == 1 { "contest" } else { "contests" };
    format!("{} · {contests} {unit}", f0(rating))
}

pub fn contest_badge(rating: f64, contests: usize) -> String {
    let (_, color) = rank_of(rating);
    badge("virtual contests", &badge_text(rating, contests), color)
}

/// The markdown's region refreshed from the JSON; a fresh file when
/// there is none.
pub fn write_markdown(c: &Contest, standing: Option<&Standing>) {
    let path = c.md_path();
    let text = match std::fs::read_to_string(&path) {
        Ok(old) => fill(&old, REGION, &c.markdown_with(standing)),
        Err(_) => c.fresh_markdown(),
    };
    std::fs::write(&path, text).unwrap_or_else(|e| panic!("{}: {e}", path.display()));
}

pub fn render(ctx: &Ctx) {
    let all = contests::load(&ctx.root);
    let virtuals: Vec<&Contest> = all.iter().filter(|c| c.virtual_).collect();
    let standings = contests::leetcode_rating(&virtuals);
    for c in &all {
        let st = standings
            .iter()
            .find(|s| s.date == c.date && s.contest == c.contest);
        write_markdown(c, st);
    }
    for c in &virtuals {
        if c.field().is_none() {
            println!(
                "{}: no field sample yet (make contest-field), left out of the rating",
                c.contest
            );
        }
    }
    let Some(last) = standings.last() else {
        println!("no rated virtual contest");
        return;
    };
    let path = ctx.graph_dir().join("contest_badge.svg");
    std::fs::write(&path, contest_badge(last.rating, standings.len())).expect("write badge");
    println!(
        "wrote {} ({}; {} markdown files refreshed)",
        path.display(),
        badge_text(last.rating, standings.len()),
        all.len()
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn badge_text_counts_contests() {
        assert_eq!(badge_text(1686.6, 2), "1687 · 2 contests");
        assert_eq!(badge_text(1500.0, 1), "1500 · 1 contest");
        assert!(contest_badge(1687.0, 2).contains("virtual contests"));
    }
}
