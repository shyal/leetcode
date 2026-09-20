// make elo: the Elo numbers behind the README chart, as a ratatui panel
// that sits open in a terminal split. The big number is the first-sight
// Elo; under it the history as a sparkline, then one gauge per number
// from START to the guardian cutoff. graph/evidence.json is polled once a
// second and the numbers recomputed when it changes, so a `make solved`
// shows up on its own. q, Esc or Ctrl+C quits. `--once` prints one frame
// and exits (the tests).
//
// The polling loop, the big digits, the gauge rows and the one-frame
// capture are the `Panel` machinery, shared with prog.rs (make prog).

use std::path::Path;
use std::time::{Duration, SystemTime};

use kg::console::terminal_columns;
use kg::ctx::Ctx;
use kg::data::repo_root;
use kg::evidence::Evidence;
use kg::figlet;
use ratatui::backend::TestBackend;
use ratatui::crossterm::event::{self, Event, KeyCode, KeyEventKind, KeyModifiers};
use ratatui::layout::{Constraint, Flex, Layout, Rect};
use ratatui::style::{Color, Modifier, Style, Stylize};
use ratatui::text::{Line, Span};
use ratatui::widgets::{
    Block, BorderType, LineGauge, Padding, Paragraph, RenderDirection, Sparkline,
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
    let spark_h = u16::from(inner.height >= 12) * 3;
    let [number_area, spark_area, _, rows_area, week_area] = Layout::vertical([
        Constraint::Fill(1),
        Constraint::Length(spark_h),
        Constraint::Length(1),
        Constraint::Length(rows.len() as u16),
        Constraint::Length(week_h),
    ])
    .areas(inner);

    big_digits(frame, number_area, n.elo, c);

    if spark_h > 0 {
        let hist: Vec<f64> = n.history.iter().map(|x| x.1).collect();
        sparkline(frame, spark_area, &hist, c);
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

/// The big number's history as a sparkline, newest at the right edge.
pub fn sparkline(frame: &mut Frame, area: Rect, history: &[f64], c: Color) {
    let w = area.width as usize;
    let tail = &history[history.len().saturating_sub(w)..];
    let lo = tail.iter().copied().fold(f64::INFINITY, f64::min);
    // newest at the right edge: RightToLeft draws data[0] there
    let data: Vec<u64> = tail.iter().rev().map(|x| (x - lo + 1.0) as u64).collect();
    frame.render_widget(
        Sparkline::default()
            .data(&data)
            .direction(RenderDirection::RightToLeft)
            .style(c),
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
pub fn run_panel<P: Panel>(first: Option<P>, once: bool) {
    let root = repo_root();
    let evidence = root.join("graph/evidence.json");
    let mut n = first;
    if once {
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
            history: (0..10).map(|i| (d, 1600.0 + i as f64 * 9.0)).collect(),
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
            "games won: 15.5 of 32 (48%, what the Elo sees)",
        ] {
            assert!(f.contains(s), "missing {s:?}\n{f}");
        }
        assert!(frame_text(Some(&sample()), 40, 8).contains("1681"));
    }

    #[test]
    fn ranks() {
        assert_eq!(rank(1681.0).1, "169 to knight");
        assert_eq!(rank(1850.0).1, "knight");
        assert_eq!(rank(2200.0).1, "guardian");
    }
}
