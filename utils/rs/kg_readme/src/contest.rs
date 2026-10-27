// The virtual contests (kg::contests, contests/*.json): the badge
// graph/contest_badge.svg, and the header and result table of each
// contest's markdown, rendered into its <!-- CONTEST --> region.
//
// The badge is the proven rating (kg::model::proven_fit) over the
// problems of the virtual contests, each a first-sight game against its
// rating, the last PROVEN_WINDOW games once there are more: the rating
// that makes the results most likely under the Elo curve, with its
// standard error, and the count of contests behind it. Real contests have
// LeetCode's own rating and are left out.

use kg::contests::{self, Contest, REGION};
use kg::ctx::Ctx;
use kg::model::{proven_fit, PROVEN_WINDOW};

use crate::common::*;
use crate::elo::rank_of;
use crate::update::fill;

/// "1423 ± 97 · 2 contests"
pub fn badge_text(rating: f64, se: f64, contests: usize) -> String {
    let unit = if contests == 1 { "contest" } else { "contests" };
    format!("{} ± {} · {contests} {unit}", f0(rating), f0(se))
}

pub fn contest_badge(rating: f64, se: f64, contests: usize) -> String {
    let (_, color) = rank_of(rating);
    badge("virtual contests", &badge_text(rating, se, contests), color)
}

/// (rating, standard error) over the virtual contests' games, None with
/// no game.
pub fn fit(virtuals: &[&Contest]) -> Option<(f64, f64)> {
    let games: Vec<_> = virtuals.iter().flat_map(|c| c.games()).collect();
    if games.is_empty() {
        return None;
    }
    let from = games.len().saturating_sub(PROVEN_WINDOW);
    Some(proven_fit(&games[from..]))
}

/// The markdown's region refreshed from the JSON; a fresh file when
/// there is none.
pub fn write_markdown(c: &Contest) {
    let path = c.md_path();
    let text = match std::fs::read_to_string(&path) {
        Ok(old) => fill(&old, REGION, &c.markdown()),
        Err(_) => c.fresh_markdown(),
    };
    std::fs::write(&path, text).unwrap_or_else(|e| panic!("{}: {e}", path.display()));
}

pub fn render(ctx: &Ctx) {
    let all = contests::load(&ctx.root);
    for c in &all {
        write_markdown(c);
    }
    let virtuals: Vec<&Contest> = all.iter().filter(|c| c.virtual_).collect();
    let Some((rating, se)) = fit(&virtuals) else {
        println!("no virtual contests");
        return;
    };
    let path = ctx.graph_dir().join("contest_badge.svg");
    std::fs::write(&path, contest_badge(rating, se, virtuals.len())).expect("write badge");
    println!(
        "wrote {} ({}; {} markdown files refreshed)",
        path.display(),
        badge_text(rating, se, virtuals.len()),
        all.len()
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn badge_text_counts_contests() {
        assert_eq!(badge_text(1423.4, 96.6, 2), "1423 ± 97 · 2 contests");
        assert_eq!(badge_text(1500.0, 150.0, 1), "1500 ± 150 · 1 contest");
        assert!(contest_badge(1423.0, 97.0, 2).contains("virtual contests"));
    }

    #[test]
    fn fit_is_none_without_games() {
        assert_eq!(fit(&[]), None);
    }
}
