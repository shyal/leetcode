// make elo: the Elo numbers behind the README chart, as a ratatui panel
// that sits open in a terminal split. The big number is the first-sight
// Elo; under it the last FS_WINDOW days as a line chart, dates along the
// bottom and ratings up the side, in every row the digits leave; then one
// gauge per number
// from START to the guardian cutoff. graph/evidence.json is polled once a
// second and the numbers recomputed when it changes, so a `make solved`
// shows up on its own. q, Esc or Ctrl+C quits. `--once` prints one frame
// and exits (the tests).
//
// The polling loop, the big digits, the gauge rows and the one-frame
// capture are the `Panel` machinery, shared with prog.rs (make prog).

use std::path::Path;
use std::time::{Duration, SystemTime};

use chrono::NaiveDate;
use kg::console::terminal_columns;
use kg::ctx::Ctx;
use kg::data::repo_root;
use kg::evidence::Evidence;
use kg::figlet;
use ratatui::backend::TestBackend;
use ratatui::crossterm::event::{self, Event, KeyCode, KeyEventKind, KeyModifiers};
use ratatui::layout::{Constraint, Flex, Layout, Rect};
use ratatui::style::{Color, Modifier, Style, Stylize};
use ratatui::symbols::Marker;
use ratatui::text::{Line, Span};
use ratatui::widgets::{
    Axis, Block, BorderType, Chart, Dataset, GraphType, LineGauge, Padding, Paragraph,
};
use ratatui::{Frame, Terminal};

use crate::elo::{numbers, Numbers, MA, RANKS, START, WEEK};
use crate::onsite::FS_WINDOW;

/// The gauges run from START to the top cutoff.
const TOP: f64 = RANKS[0].0 as f64;

fn mtime(p: &Path) -> Option<SystemTime> {
    std::fs::metadata(p).and_then(|m| m.modified()).ok()
}

/// One live panel: what to show and how to reload it when the evidence
/// changes.
pub trait Panel: Sized {
    /// The numbers off a fresh load of the evidence.
    fn compute(ctx: &Ctx, ev: &Evidence) -> Option<Self>;
    fn draw(&self, frame: &mut Frame);
}

/// The numbers off a fresh load, or None while the file is mid-write
/// (a writer that is not pyjson::save): the caller keeps the last frame
/// and tries again next tick.
fn load<P: Panel>(root: &Path) -> Option<P> {
    kg::data::read_json(&root.join("graph/evidence.json"))?;
    let (ctx, recs) = Ctx::load(root.to_path_buf());
    P::compute(&ctx, &Evidence::new(recs))
}

/// (rank colour, rank line) for an Elo: gold past guardian, blue past
/// knight, else green with the distance to knight.
fn rank(r: f64) -> (Color, String) {
    if r >= RANKS[0].0 as f64 {
        return (Color::Yellow, RANKS[0].1.to_string());
    }
    if r >= RANKS[1].0 as f64 {
        return (Color::Blue, RANKS[1].1.to_string());
    }
    (
        Color::Green,
        format!("{} to {}", RANKS[1].0 - r.round() as i64, RANKS[1].1),
    )
}

/// The Elo as large figlet digits, stepping down to smaller fonts and
/// finally plain text when the area is too small.
pub fn big_number(r: f64, width: usize, height: usize) -> Vec<String> {
    let face = format!("{r:.0}");
    let first = std::env::var("TIMER_FONT").unwrap_or_else(|_| "doh".to_string());
    for font in [first.as_str(), "univers", "big"] {
        let Some(f) = figlet::builtin(font) else {
            continue;
        };
        let lines: Vec<String> = f
            .render(&face, 200)
            .trim_end()
            .lines()
            .filter(|l| !l.trim().is_empty())
            .map(|l| l.trim_end().to_string())
            .collect();
        let widest = lines.iter().map(|l| l.chars().count()).max().unwrap_or(0);
        if !lines.is_empty() && lines.len() <= height && widest <= width {
            return lines;
        }
    }
    vec![face]
}

pub fn signed(d: f64) -> String {
    format!("{:+.0}", d)
}

fn draw_numbers(frame: &mut Frame, n: &Numbers) {
    let (c, rank_line) = rank(n.elo);
    let subtitle = Line::from(vec![
        Span::styled(rank_line, Style::new().fg(c)),
        Span::styled(
            format!(
                "  · {} games, {} wins, {} draws, {} losses",
                n.games,
                n.wins,
                n.draws,
                n.games - n.wins - n.draws
            ),
            Style::new().dim(),
        ),
    ]);
    let inner = framed(frame, "first-sight elo".to_string(), subtitle, c);

    // (label, value, note) one gauge each
    let rows: Vec<(String, f64, String)> = [
        Some(("first sight".to_string(), n.elo, String::new())),
        n.ma.map(|m| (format!("{MA} game average"), m, signed(m - n.elo))),
        Some((
            format!("last {FS_WINDOW} days"),
            n.late,
            signed(n.late - n.elo),
        )),
        Some(("picker".to_string(), n.picker, signed(n.picker - n.elo))),
    ]
    .into_iter()
    .flatten()
    .collect();

    // the week's totals under the gauges, dropped first when the panel is short
    let week = n.week.rows();
    let week_h = u16::from(inner.height >= 16) * (week.len() as u16 + 1);
    let fixed = 1 + rows.len() as u16 + week_h;
    let (number_c, spark_c) = split(inner, fixed, n.elo);
    let [number_area, spark_area, _, rows_area, week_area] = Layout::vertical([
        number_c,
        spark_c,
        Constraint::Length(1),
        Constraint::Length(rows.len() as u16),
        Constraint::Length(week_h),
    ])
    .areas(inner);

    big_digits(frame, number_area, n.elo, c);

    if spark_area.height > 0 {
        chart(frame, spark_area, &n.history, n.today, FS_WINDOW, c);
    }

    gauge_rows(frame, rows_area, &rows, c);

    if week_h > 0 {
        let text = ratio_lines(format!("last {WEEK} days"), week);
        frame.render_widget(Paragraph::new(text), week_area);
    }
}

/// The rounded border in the panel's colour with the title on top and
/// the subtitle below; returns the padded area inside it.
pub fn framed(frame: &mut Frame, title: String, subtitle: Line<'static>, c: Color) -> Rect {
    let block = Block::bordered()
        .border_type(BorderType::Rounded)
        .border_style(Style::new().fg(c))
        .title(Line::from(title).bold().fg(c).centered())
        .title_bottom(subtitle.centered())
        .padding(Padding::new(3, 3, 1, 1));
    let inner = block.inner(frame.area());
    frame.render_widget(block, frame.area());
    inner
}

/// How the rows above the gauges split between the big number and the
/// chart: the number takes the rows its largest fitting font needs plus
/// one above and one below, the chart every row left. Under CHART_MIN
/// rows left there is no chart and the number takes all.
pub fn split(inner: Rect, fixed: u16, value: f64) -> (Constraint, Constraint) {
    let spare = inner.height.saturating_sub(fixed + CHART_MIN);
    let font = big_number(value, inner.width as usize, spare.saturating_sub(2) as usize);
    let digits = font.len() as u16 + 2;
    if spare >= digits {
        (Constraint::Length(digits), Constraint::Fill(1))
    } else {
        (Constraint::Fill(1), Constraint::Length(0))
    }
}

/// The fewest rows a chart is worth drawing in: one for the dates, the
/// rest for the line.
const CHART_MIN: u16 = 5;

/// `history` is (date, value after the day's last game) one per day with
/// a game. The value on each of the last `days` calendar days, the day's
/// own when it had a game, else the last one before it; days before the
/// first entry are left out. Returns the first day and the values from it
/// to `today`.
pub fn daily(
    history: &[(NaiveDate, f64)],
    today: NaiveDate,
    days: i64,
) -> Option<(NaiveDate, Vec<f64>)> {
    let first = history.first()?.0;
    let from = first.max(today - chrono::Duration::days(days - 1));
    let mut out = Vec::new();
    let mut i = 0;
    let mut last = history[0].1;
    for d in from.iter_days().take_while(|d| *d <= today) {
        while i < history.len() && history[i].0 <= d {
            last = history[i].1;
            i += 1;
        }
        out.push(last);
    }
    Some((from, out))
}

/// The big number's last `days` days as a line, one point per calendar
/// day (see `daily`). The dates of the first, middle and last day run
/// along the bottom; the lowest, middle and highest rating in the window,
/// rounded out to tens, up the side.
pub fn chart(
    frame: &mut Frame,
    area: Rect,
    history: &[(NaiveDate, f64)],
    today: NaiveDate,
    days: i64,
    c: Color,
) {
    let Some((from, vals)) = daily(history, today, days) else {
        return;
    };
    let n = vals.len();
    let lo = (vals.iter().copied().fold(f64::INFINITY, f64::min) / 10.0).floor() * 10.0;
    let hi = (vals.iter().copied().fold(f64::NEG_INFINITY, f64::max) / 10.0).ceil() * 10.0;
    let hi = hi.max(lo + 10.0);
    let points: Vec<(f64, f64)> = vals
        .iter()
        .enumerate()
        .map(|(i, v)| (i as f64, *v))
        .collect();
    let day = |i: usize| {
        (from + chrono::Duration::days(i as i64))
            .format("%b %-d")
            .to_string()
    };
    let x_labels = vec![day(0), day(n / 2), day(n - 1)];
    let y_labels = vec![
        format!("{lo:.0}"),
        format!("{:.0}", (lo + hi) / 2.0),
        format!("{hi:.0}"),
    ];
    let dim = Style::new().dim();
    frame.render_widget(
        Chart::new(vec![Dataset::default()
            .marker(Marker::Braille)
            .graph_type(GraphType::Line)
            .style(Style::new().fg(c))
            .data(&points)])
        .x_axis(
            Axis::default()
                .bounds([0.0, (n.max(2) - 1) as f64])
                .labels(x_labels)
                .style(dim),
        )
        .y_axis(Axis::default().bounds([lo, hi]).labels(y_labels).style(dim)),
        area,
    );
}

/// The big number, centred in `area` in the largest font that fits.
pub fn big_digits(frame: &mut Frame, area: Rect, value: f64, c: Color) {
    let lines = big_number(value, area.width as usize, area.height as usize);
    let [area] = Layout::vertical([Constraint::Length(lines.len() as u16)])
        .flex(Flex::Center)
        .areas(area);
    let text: Vec<Line> = lines.into_iter().map(Line::from).collect();
    frame.render_widget(
        Paragraph::new(text)
            .style(Style::new().fg(c).add_modifier(Modifier::BOLD))
            .centered(),
        area,
    );
}

/// label(16) | gauge | value(5) | note(5), one space between, one row
/// per (label, value, note); the gauges run from START to TOP.
pub fn gauge_rows(frame: &mut Frame, area: Rect, rows: &[(String, f64, String)], c: Color) {
    for (i, (label, value, note)) in rows.iter().enumerate() {
        let row = Rect {
            y: area.y + i as u16,
            height: 1,
            ..area
        };
        let [desc, gauge, mark, right] = Layout::horizontal([
            Constraint::Length(16),
            Constraint::Fill(1),
            Constraint::Length(5),
            Constraint::Length(5),
        ])
        .spacing(1)
        .areas(row);
        let ratio = ((value - START) / (TOP - START)).clamp(0.0, 1.0);
        frame.render_widget(Paragraph::new(label.as_str()), desc);
        frame.render_widget(
            LineGauge::default()
                .ratio(ratio)
                .filled_style(Style::new().fg(c))
                .unfilled_style(Style::new().dim())
                .label(""),
            gauge,
        );
        frame.render_widget(Paragraph::new(format!("{value:.0}")).bold(), mark);
        frame.render_widget(Paragraph::new(note.as_str()).dim().right_aligned(), right);
    }
}

/// Sentences with their ratio bright, under a bold heading: the ratios
/// are what the panel is open for.
pub fn ratio_lines(heading: String, rows: Vec<(String, String, String)>) -> Vec<Line<'static>> {
    let mut text = vec![Line::from(heading.bold())];
    text.extend(rows.into_iter().map(|(before, ratio, after)| {
        Line::from(vec![
            Span::styled(before, Style::new().dim()),
            Span::styled(ratio, Style::new().fg(Color::LightGreen).bold()),
            Span::styled(after, Style::new().dim()),
        ])
    }));
    text
}

impl Panel for Numbers {
    fn compute(ctx: &Ctx, ev: &Evidence) -> Option<Self> {
        numbers(ctx, ev)
    }

    fn draw(&self, frame: &mut Frame) {
        draw_numbers(frame, self)
    }
}

fn draw<P: Panel>(frame: &mut Frame, n: Option<&P>) {
    match n {
        Some(n) => n.draw(frame),
        None => frame.render_widget(
            Paragraph::new("no scored attempts").dim().centered(),
            frame.area(),
        ),
    }
}

/// One frame as plain text (no colour), for `--once` and the tests.
pub fn frame_text<P: Panel>(n: Option<&P>, width: u16, height: u16) -> String {
    let mut terminal = Terminal::new(TestBackend::new(width, height)).expect("test backend");
    terminal.draw(|f| draw(f, n)).expect("draw");
    let buf = terminal.backend().buffer();
    let mut out = String::new();
    for y in 0..height {
        let row: String = (0..width)
            .filter_map(|x| buf.cell((x, y)).map(|c| c.symbol()))
            .collect();
        out.push_str(row.trim_end());
        out.push('\n');
    }
    out
}

fn quits(ev: &Event) -> bool {
    let Event::Key(k) = ev else {
        return false;
    };
    k.kind == KeyEventKind::Press
        && (matches!(k.code, KeyCode::Char('q') | KeyCode::Esc)
            || (k.code == KeyCode::Char('c') && k.modifiers.contains(KeyModifiers::CONTROL)))
}

pub fn run(ctx: &Ctx, ev: &Evidence, once: bool) {
    run_panel(numbers(ctx, ev), once);
}

/// Show `first`, then reload and redraw whenever graph/evidence.json
/// changes, until q, Esc or Ctrl+C. `once` prints one frame and returns.
/// Without a terminal on both stdin and stdout (a pipe, a subprocess,
/// Claude's shell) the live panel cannot start, so one frame is printed
/// as if `--once` had been given.
pub fn run_panel<P: Panel>(first: Option<P>, once: bool) {
    use std::io::IsTerminal;
    let root = repo_root();
    let evidence = root.join("graph/evidence.json");
    let mut n = first;
    if once || !std::io::stdin().is_terminal() || !std::io::stdout().is_terminal() {
        let (w, h) = ratatui::crossterm::terminal::size()
            .ok()
            .filter(|(w, h)| *w > 0 && *h > 0)
            .unwrap_or((terminal_columns() as u16, 24));
        print!("{}", frame_text(n.as_ref(), w, h));
        return;
    }
    let mut seen = mtime(&evidence);
    let mut terminal = ratatui::init();
    let mut stop = false;
    while !stop {
        let now = mtime(&evidence);
        if now != seen {
            if let Some(fresh) = load::<P>(&root) {
                seen = now;
                n = Some(fresh);
            }
        }
        let _ = terminal.draw(|f| draw(f, n.as_ref()));
        if event::poll(Duration::from_secs(1)).unwrap_or(false) {
            if let Ok(ev) = event::read() {
                stop = quits(&ev);
            }
        }
    }
    ratatui::restore();
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::NaiveDate;

    fn sample() -> Numbers {
        let d = NaiveDate::from_ymd_opt(2026, 9, 1).unwrap();
        Numbers {
            elo: 1681.0,
            ma: Some(1610.0),
            late: 1771.0,
            picker: 1690.0,
            history: (0..10)
                .map(|i| (d + chrono::Duration::days(i), 1600.0 + i as f64 * 9.0))
                .collect(),
            today: d + chrono::Duration::days(9),
            games: 427,
            wins: 297,
            draws: 6,
            week: kg::model::Summary {
                solves: 32,
                fails: 7,
                inside: 22,
                over: 3,
                first: 5,
                first_fails: 2,
                won: 15.5,
                ..Default::default()
            },
        }
    }

    #[test]
    fn frame_is_a_panel_with_every_row() {
        let f = frame_text(Some(&sample()), 80, 24);
        assert!(f.starts_with('╭') && f.trim_end().ends_with('╯'));
        assert!(f.lines().all(|l| l.chars().count() <= 80));
        for s in [
            "first-sight elo",
            "169 to knight",
            "427 games, 297 wins, 6 draws, 124 losses",
            "60 game average",
            "1610",
            "-71",
            "last 60 days",
            "1771",
            "+90",
            "picker",
            "1690",
            "+9",
            "last 7 days",
            "32 solves: 25 pass / 7 fail (78%)",
            "inside the clock: 22 of 32 (69%, 3 passes over time)",
            "first sight: 5 (3 pass / 2 fail, 60%)",
            "repeat: 27 (22 pass / 5 fail, 81%)",
            "games won: 15.5 of 32 (48%, repeats included: the picker's Elo)",
        ] {
            assert!(f.contains(s), "missing {s:?}\n{f}");
        }
        assert!(frame_text(Some(&sample()), 40, 8).contains("1681"));
    }

    #[test]
    fn daily_carries_the_last_value_over_days_without_a_game() {
        let d = |n| NaiveDate::from_ymd_opt(2026, 10, 1).unwrap() + chrono::Duration::days(n);
        let h = [(d(0), 1600.0), (d(2), 1620.0), (d(5), 1590.0)];
        // the whole span, rest days carried
        assert_eq!(
            daily(&h, d(6), 60),
            Some((
                d(0),
                vec![1600.0, 1600.0, 1620.0, 1620.0, 1620.0, 1590.0, 1590.0]
            ))
        );
        // a window shorter than the span starts inside it
        assert_eq!(
            daily(&h, d(6), 3),
            Some((d(4), vec![1620.0, 1590.0, 1590.0]))
        );
        assert_eq!(daily(&[], d(6), 60), None);
    }

    #[test]
    fn tall_panel_charts_the_window_with_dates_and_ratings() {
        let f = frame_text(Some(&sample()), 62, 44);
        // the sample runs Sep 1 to Sep 10, 1600 to 1681: the axes say so
        for s in ["Sep 1", "Sep 6", "Sep 10", "1600", "1645", "1690"] {
            assert!(f.contains(s), "missing {s:?}\n{f}");
        }
        let braille = |ch: char| ('\u{2801}'..='\u{28ff}').contains(&ch);
        let line_rows = f.lines().filter(|l| l.chars().any(braille)).count();
        assert!(line_rows > 3, "{line_rows} chart rows\n{f}");
        assert!(f.contains("1681"));
    }

    #[test]
    fn ranks() {
        assert_eq!(rank(1681.0).1, "169 to knight");
        assert_eq!(rank(1850.0).1, "knight");
        assert_eq!(rank(2200.0).1, "guardian");
    }
}
