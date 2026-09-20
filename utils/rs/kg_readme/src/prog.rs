// make prog: the numbers behind `make progress`, as a ratatui panel that
// sits open in a terminal split beside `make elo`. The big number is the
// proven rating (kg::model::proven_series); under it its history as a
// sparkline, then one gauge each for the proven rating now, 90 days ago,
// its best before that, and the median rating served; then the two
// ground sentences of the last 30 days and the drills that hold. The
// border carries the verdict of `make progress`: green progressing, cyan
// gaining, blue rebuilding, yellow grinding or stalled, red slipping.
// graph/evidence.json is polled once a second, so a `make solved` shows
// up on its own. q, Esc or Ctrl+C quits. `--once` prints one frame and
// exits (the tests). KG_TODAY=YYYY-MM-DD shows the panel as of that day.

use chrono::NaiveDate;
use kg::ctx::Ctx;
use kg::evidence::Evidence;
use kg::model::{
    progress_numbers, progress_text, Progress, PROGRESS_HOLD_REPS, PROGRESS_LEVEL_DAYS,
    PROGRESS_TURNED_DAYS, PROGRESS_WINDOW_DAYS, PROVEN_WINDOW,
};
use ratatui::layout::{Constraint, Layout};
use ratatui::style::{Color, Style, Stylize};
use ratatui::text::{Line, Span};
use ratatui::widgets::{Paragraph, Wrap};
use ratatui::Frame;

use crate::dash::{
    big_digits, framed, gauge_rows, ratio_lines, run_panel, signed, sparkline, Panel,
};

/// How many of the moves that turned into unaided solves are listed.
const TURNED_SHOWN: usize = 3;

pub struct Prog {
    p: Progress,
    today: NaiveDate,
}

/// (border colour, verdict) for the panel: the verdict of `make progress`.
fn verdict(p: &Progress) -> (Color, &'static str) {
    let v = p.verdict();
    let c = match v {
        "progressing" => Color::Green,
        "gaining" => Color::Cyan,
        "rebuilding" => Color::Blue,
        "grinding" | "stalled" => Color::Yellow,
        "slipping" => Color::Red,
        _ => Color::DarkGray,
    };
    (c, v)
}

/// The dim note after the verdict: the move since PROGRESS_LEVEL_DAYS
/// ago and whether now is the best.
fn note(p: &Prog) -> String {
    let since = p.today - chrono::Duration::days(PROGRESS_LEVEL_DAYS);
    let mut out = match (p.p.now, p.p.then) {
        (Some(_), Some(_)) => format!("  · {} since {}", signed(p.p.delta()), since.format("%B")),
        _ => format!("  · under {PROVEN_WINDOW} first sights"),
    };
    if p.p.at_best() {
        out.push_str(", the highest it has been");
    }
    out
}

/// The drills block: the count holding, then the moves that turned into
/// unaided solves this month, newest first, at most TURNED_SHOWN.
fn drill_lines(p: &Progress) -> Vec<Line<'static>> {
    let problems: usize = p.turned.iter().map(|(_, ts)| ts.len()).sum();
    let bright = Style::new().fg(Color::LightGreen).bold();
    let mut text = vec![
        Line::from("drills".bold()),
        Line::from(vec![
            Span::styled(format!("{}", p.holding), bright),
            Span::styled(
                format!(" drills have held for {PROGRESS_HOLD_REPS} clean runs or more; "),
                Style::new().dim(),
            ),
            Span::styled(format!("{}", p.turned.len()), bright),
            Span::styled(" of their moves turned into ", Style::new().dim()),
            Span::styled(format!("{problems}"), bright),
            Span::styled(
                format!(
                    " problems solved without help within {PROGRESS_TURNED_DAYS} days of the drill"
                ),
                Style::new().dim(),
            ),
        ]),
    ];
    for (m, ts) in p.turned.iter().rev().take(TURNED_SHOWN) {
        text.push(Line::from(vec![
            Span::styled(format!("  {m}: "), Style::new()),
            Span::styled(ts.join(", "), Style::new().dim()),
        ]));
    }
    let rest = p.turned.len().saturating_sub(TURNED_SHOWN);
    if rest > 0 {
        text.push(Line::from(format!("  and {rest} more moves")).dim());
    }
    text
}

impl Panel for Prog {
    fn compute(ctx: &Ctx, ev: &Evidence) -> Option<Self> {
        let today = ctx.today();
        let p = progress_numbers(ctx, ev, today);
        (p.recent > 0 || p.now.is_some()).then_some(Prog { p, today })
    }

    fn draw(&self, frame: &mut Frame) {
        let p = &self.p;
        let (c, _) = verdict(p);
        // the title is the first line of `make progress`, the verdict itself
        let title = progress_text(p, self.today).remove(0);
        let subtitle = Line::from(vec![
            Span::styled("proven rating", Style::new().fg(c)),
            Span::styled(note(self), Style::new().dim()),
        ]);
        let inner = framed(frame, title, subtitle, c);

        let now = p.now.unwrap_or(f64::NAN);
        // (label, value, note) one gauge each
        let rows: Vec<(String, f64, String)> = [
            p.now.map(|n| ("proven".to_string(), n, String::new())),
            p.then.map(|t| {
                (
                    format!("{PROGRESS_LEVEL_DAYS} days ago"),
                    t,
                    signed(t - now),
                )
            }),
            p.best_before
                .map(|b| ("best before".to_string(), b, signed(b - now))),
            p.served
                .map(|s| ("served median".to_string(), s, signed(s - now))),
        ]
        .into_iter()
        .flatten()
        .collect();

        // the sentences wrap to the panel's width; each block is sized to
        // its wrapped height, and dropped when the panel is short
        let ground = Paragraph::new(ratio_lines(
            format!("last {PROGRESS_WINDOW_DAYS} days"),
            p.ground
                .rows(&format!("the last {PROGRESS_WINDOW_DAYS} days")),
        ))
        .wrap(Wrap { trim: false });
        let drills = Paragraph::new(drill_lines(p)).wrap(Wrap { trim: false });
        let wrapped = |para: &Paragraph| para.line_count(inner.width) as u16;
        let ground_h = u16::from(inner.height >= 16) * wrapped(&ground);
        let drills_h = u16::from(inner.height >= 20) * (wrapped(&drills) + 1);
        let spark_h = u16::from(inner.height >= 12) * 3;
        let [number_area, spark_area, _, rows_area, ground_area, drills_area] = Layout::vertical([
            Constraint::Fill(1),
            Constraint::Length(spark_h),
            Constraint::Length(1),
            Constraint::Length(rows.len() as u16),
            Constraint::Length(ground_h),
            Constraint::Length(drills_h),
        ])
        .areas(inner);

        // under PROVEN_WINDOW first sights there is no proven rating yet:
        // the games in the window stand in
        let face = if p.now.is_some() {
            now
        } else {
            p.recent as f64
        };
        big_digits(frame, number_area, face, c);

        if spark_h > 0 {
            let hist: Vec<f64> = p.proven.iter().map(|x| x.1).collect();
            sparkline(frame, spark_area, &hist, c);
        }
        gauge_rows(frame, rows_area, &rows, c);
        if ground_h > 0 {
            frame.render_widget(ground, ground_area);
        }
        if drills_h > 0 {
            let [_, area] =
                Layout::vertical([Constraint::Length(1), Constraint::Fill(1)]).areas(drills_area);
            frame.render_widget(drills, area);
        }
    }
}

pub fn run(ctx: &Ctx, ev: &Evidence, once: bool) {
    run_panel(Prog::compute(ctx, ev), once);
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::dash::frame_text;
    use kg::model::Ground;

    fn sample() -> Prog {
        let d = NaiveDate::from_ymd_opt(2026, 9, 1).unwrap();
        Prog {
            today: NaiveDate::from_ymd_opt(2026, 9, 20).unwrap(),
            p: Progress {
                recent: 40,
                lost: 10,
                proven: (0..10).map(|i| (d, 1300.0 + i as f64 * 19.0)).collect(),
                now: Some(1471.0),
                then: Some(1290.0),
                best_before: Some(1400.0),
                served: Some(1650.0),
                ground: Ground {
                    tried: 26,
                    cold: 10,
                    retested: 16,
                    held: 5,
                    pending: 36,
                },
                holding: 52,
                turned: vec![
                    ("union-find".into(), vec!["Redundant Connection".into()]),
                    (
                        "binary search on the answer".into(),
                        vec!["Capacity To Ship Packages Within D Days".into()],
                    ),
                ],
            },
        }
    }

    #[test]
    fn frame_is_a_panel_with_every_row() {
        let f = frame_text(Some(&sample()), 100, 30);
        assert!(f.starts_with('╭') && f.trim_end().ends_with('╯'));
        assert!(f.lines().all(|l| l.chars().count() <= 100));
        for s in [
            "You're progressing.",
            "proven rating  · +181 since June, the highest it has been",
            "90 days ago",
            "1290",
            "-181",
            "best before",
            "1400",
            "-71",
            "served median",
            "1650",
            "+179",
            "last 30 days",
            "you tried 26 problems at your level for the first time",
            "(38%)",
            "16 problems you had failed and later solved were given to you again",
            "(31%)",
            "36 more have not been given again yet",
            "52 drills have held for 3 clean runs or more; 2 of their moves turned into 2",
            "within 21 days of the drill",
            "binary search on the answer: Capacity To Ship Packages Within D Days",
            "union-find: Redundant Connection",
        ] {
            assert!(f.contains(s), "missing {s:?}\n{f}");
        }
        assert!(frame_text(Some(&sample()), 40, 8).contains("1471"));
    }

    #[test]
    fn verdict_colours() {
        let mut s = sample();
        assert_eq!(verdict(&s.p), (Color::Green, "progressing"));
        s.p.then = Some(1500.0);
        assert_eq!(verdict(&s.p), (Color::Yellow, "grinding"));
        s.p.recent = 2;
        assert_eq!(verdict(&s.p).1, "not training");
    }
}
