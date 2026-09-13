// timer - live pacing bars for the solve in current.py, branch-aware so it
// can sit open in a terminal split all session.
//
//   make timer
//   timer --once                 # one frame, no loop (the tests)
//   timer --figlet <font> <text> # the big digits alone (pyfiglet parity)
//
// Idle on master. The moment `make prepare` / `make drill` cuts a solve
// branch, the timer picks it up: three bars against the same forecast
// `make next` printed - expected time, the hint mark (2x), and the stop
// mark (4x - bank it, reinforce). The clock counts what `make solved`
// will record: ACTIVE time on the branch (kg::git::active_seconds), the
// slept intervals of a parked/resumed problem excluded. When the branch
// merges away the timer goes idle again and waits for the next one. Ctrl+C
// to quit; it records nothing - `make solved` stays the only recorder.
//
// Ported from utils/kg/timer (Python) on 2026-09-12. Since 2026-09-13 it is
// a ratatui application: alternate screen, raw mode, one full frame per
// tick, so nothing ever wraps or scrolls, and a resize just redraws. q, Esc
// or Ctrl+C quits.

use std::time::Duration;

use kg::console::terminal_columns;
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root};
use kg::figlet;
use kg::git::active_seconds;
use kg::model::{drill_forecast, solve_forecast};
use ratatui::backend::TestBackend;
use ratatui::crossterm::event::{self, Event, KeyCode, KeyEventKind, KeyModifiers};
use ratatui::layout::{Constraint, Flex, Layout, Rect};
use ratatui::style::{Color, Modifier, Style, Stylize};
use ratatui::text::{Line, Span};
use ratatui::widgets::{Block, BorderType, Padding, Paragraph};
use ratatui::{Frame, Terminal};
use regex::Regex;

fn now() -> f64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_secs_f64())
        .unwrap_or(0.0)
}

fn git(root: &std::path::Path, args: &[&str]) -> String {
    std::process::Command::new("git")
        .args(args)
        .current_dir(root)
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
        .unwrap_or_default()
}

/// ("drill", title) or (number, title) from the first docstring of
/// current.py, as kg_solved reads it.
fn parse_current(root: &std::path::Path) -> Option<(String, String)> {
    let content = std::fs::read_to_string(root.join("current.py")).ok()?;
    let doc = Regex::new(r#"(?s)"""(.*?)""""#)
        .unwrap()
        .captures(&content)?[1]
        .trim()
        .to_string();
    let drill = Regex::new(r"^DRILL:\s*(.+)").unwrap();
    let prob = Regex::new(r"^(\d+[a-zA-Z]?)\.\s*(.+)").unwrap();
    for line in doc.split('\n') {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        if let Some(m) = drill.captures(line) {
            return Some(("drill".to_string(), m[1].trim().to_string()));
        }
        if let Some(m) = prob.captures(line) {
            return Some((m[1].trim().to_string(), m[2].trim().to_string()));
        }
    }
    None
}

/// (label, forecast minutes) for the attempt in current.py.
fn forecast(ctx: &Ctx) -> (Option<String>, Option<(f64, f64, f64)>) {
    let Some((pid, title)) = parse_current(&ctx.root) else {
        return (None, None);
    };
    let today = ctx.today();
    if pid == "drill" {
        let stem = title
            .chars()
            .filter(|c| c.is_alphanumeric() || *c == '_' || c.is_whitespace() || *c == '-')
            .collect::<String>()
            .trim()
            .replace(' ', "_");
        let path = ctx
            .every_bank_path()
            .into_iter()
            .find(|p| ctx.drill_solved_stem(p) == stem);
        return (
            Some(format!("drill: {title}")),
            path.and_then(|p| drill_forecast(ctx, &p, today)),
        );
    }
    let pv = PView::new(ctx.evidenced());
    (
        Some(format!("{pid}. {title}")),
        solve_forecast(ctx, &pid, &pv, today),
    )
}

fn clock(secs: f64) -> String {
    let s = secs as i64;
    format!("{}m {:02}s", s / 60, s % 60)
}

/// The solve branch, or None when idle (master, or no parseable stub).
fn active_branch(root: &std::path::Path) -> Option<String> {
    let b = git(root, &["rev-parse", "--abbrev-ref", "HEAD"]);
    if matches!(b.as_str(), "" | "master" | "HEAD") {
        return None;
    }
    std::fs::read_to_string(root.join("current.py"))
        .ok()
        .filter(|s| !s.trim().is_empty())
        .map(|_| b)
}

/// The elapsed clock as large figlet digits. Font from $TIMER_FONT (default
/// doh, same as make goals), stepping down to smaller fonts and finally
/// plain text when the area is too narrow or too short.
fn big_clock(secs: f64, width: usize, height: usize) -> Vec<String> {
    let s = secs as i64;
    let face = format!("{}:{:02}", s / 60, s % 60);
    let first = std::env::var("TIMER_FONT").unwrap_or_else(|_| "doh".to_string());
    for font in [first.as_str(), "univers", "big"] {
        let Some(f) = figlet::builtin(font) else {
            continue;
        };
        let art = f.render(&face, 200);
        let lines: Vec<String> = art
            .trim_end()
            .lines()
            .filter(|l| !l.trim().is_empty())
            .map(|l| l.trim_end().to_string())
            .collect();
        if !lines.is_empty()
            && lines.len() <= height
            && lines.iter().map(|l| l.chars().count()).max().unwrap() <= width
        {
            return lines;
        }
    }
    vec![clock(secs)]
}

struct Session {
    label: String,
    t0: f64,
    slept: i64,
    parks: i64,
    marks: Vec<(&'static str, f64, &'static str)>,
}

impl Session {
    fn new(ctx: &Ctx) -> Session {
        let (label, fc) = forecast(ctx);
        let (active, slept, parks) = active_seconds(&ctx.root, "HEAD", now() as i64);
        let marks = match fc {
            Some((e, h, b)) => vec![
                ("expected", e * 60.0, "green"),
                ("hint fair game", h * 60.0, "yellow"),
                ("stop, reinforce", b * 60.0, "red"),
            ],
            None => vec![],
        };
        Session {
            label: label.unwrap_or_default(),
            t0: now() - active as f64,
            slept,
            parks,
            marks,
        }
    }

    /// (color, message) for where the clock sits between the marks.
    fn zone(&self, elapsed: f64) -> (&'static str, &'static str) {
        if self.marks.is_empty() {
            return ("cyan", "no forecast - plain clock");
        }
        if elapsed > self.marks[2].1 {
            return ("red", "past the stop mark - bank it, reinforce");
        }
        if elapsed > self.marks[1].1 {
            return ("yellow", "hint is fair game");
        }
        if elapsed > self.marks[0].1 {
            return ("yellow", "past expected - keep going");
        }
        ("green", "on pace")
    }
}

fn color(name: &str) -> Color {
    match name {
        "green" => Color::Green,
        "yellow" => Color::Yellow,
        "red" => Color::Red,
        "cyan" => Color::Cyan,
        _ => Color::Reset,
    }
}

/// rich's ProgressBar: "━" for the done part (a half block at the edge),
/// dim "━" for the rest.
fn bar(width: usize, completed: f64, total: f64, finished: bool) -> Line<'static> {
    let frac = if total > 0.0 {
        (completed / total).clamp(0.0, 1.0)
    } else {
        0.0
    };
    let halves = (width as f64 * 2.0 * frac) as usize;
    let full = halves / 2;
    let half = halves % 2 == 1;
    let done = if finished {
        Style::new().cyan().bold()
    } else {
        Style::new().cyan()
    };
    let mut spans = vec![Span::styled("━".repeat(full), done)];
    let mut rest = width.saturating_sub(full);
    if half && rest > 0 {
        spans.push(Span::styled("╸", Style::new().cyan()));
        rest -= 1;
    }
    spans.push(Span::styled("━".repeat(rest), Style::new().dim()));
    Line::from(spans)
}

/// The panel: rounded border in the zone colour, the label on the top rule,
/// the zone message on the bottom one, padding (1, 2) inside.
fn panel<'a>(title: Line<'a>, subtitle: Line<'a>, border: Color) -> Block<'a> {
    Block::bordered()
        .border_type(BorderType::Rounded)
        .border_style(Style::new().fg(border))
        .title(title.centered())
        .title_bottom(subtitle.centered())
        .padding(Padding::new(3, 3, 1, 1))
}

fn draw_session(frame: &mut Frame, session: &Session) {
    let elapsed = now() - session.t0;
    let (zone, message) = session.zone(elapsed);
    let c = color(zone);
    let mut subtitle = vec![Span::styled(message, Style::new().fg(c))];
    if session.parks > 0 {
        let (sh, sm) = (session.slept / 60 / 60, session.slept / 60 % 60);
        subtitle.push(Span::styled(
            format!("  · slept {sh}h {sm:02}m over {} park(s)", session.parks),
            Style::new().dim(),
        ));
    }
    let block = panel(
        Line::from(session.label.as_str()).bold(),
        Line::from(subtitle),
        c,
    );
    let inner = block.inner(frame.area());
    frame.render_widget(block, frame.area());

    let n = session.marks.len() as u16;
    let gap = u16::from(n > 0);
    let [clock_area, _, marks_area] = Layout::vertical([
        Constraint::Fill(1),
        Constraint::Length(gap),
        Constraint::Length(n),
    ])
    .areas(inner);

    let lines = big_clock(
        elapsed,
        clock_area.width as usize,
        clock_area.height as usize,
    );
    let [clock_area] = Layout::vertical([Constraint::Length(lines.len() as u16)])
        .flex(Flex::Center)
        .areas(clock_area);
    let text: Vec<Line> = lines.into_iter().map(Line::from).collect();
    frame.render_widget(
        Paragraph::new(text)
            .style(Style::new().fg(c).add_modifier(Modifier::BOLD))
            .centered(),
        clock_area,
    );

    // description(15) | bar | mark(6) | left(10), one space between
    for (i, (name, total, zc)) in session.marks.iter().enumerate() {
        let row = Rect {
            y: marks_area.y + i as u16,
            height: 1,
            ..marks_area
        };
        let [desc, gauge, mark, left] = Layout::horizontal([
            Constraint::Length(15),
            Constraint::Fill(1),
            Constraint::Length(6),
            Constraint::Length(10),
        ])
        .spacing(1)
        .areas(row);
        let remaining = if elapsed >= *total {
            String::new()
        } else {
            format!("-{}", clock(total - elapsed))
        };
        frame.render_widget(Paragraph::new(*name).fg(color(zc)), desc);
        frame.render_widget(
            bar(
                gauge.width as usize,
                elapsed.min(*total),
                *total,
                elapsed >= *total,
            ),
            gauge,
        );
        frame.render_widget(Paragraph::new(clock(*total)).dim(), mark);
        frame.render_widget(Paragraph::new(remaining).right_aligned(), left);
    }
}

fn draw_idle(frame: &mut Frame) {
    let block = panel(Line::default(), Line::default(), Color::DarkGray);
    let inner = block.inner(frame.area());
    frame.render_widget(block, frame.area());
    let [row] = Layout::vertical([Constraint::Length(1)])
        .flex(Flex::Center)
        .areas(inner);
    frame.render_widget(
        Paragraph::new("idle - waiting for a solve branch (`make next`, `make drill`)")
            .dim()
            .centered(),
        row,
    );
}

fn draw(frame: &mut Frame, session: Option<&Session>) {
    match session {
        Some(s) => draw_session(frame, s),
        None => draw_idle(frame),
    }
}

/// One frame as plain text (no colour), for `--once` and the tests.
fn frame_text(session: Option<&Session>, width: u16, height: u16) -> String {
    let mut terminal = Terminal::new(TestBackend::new(width, height)).expect("test backend");
    terminal.draw(|f| draw(f, session)).expect("draw");
    let buf = terminal.backend().buffer();
    let mut out = String::new();
    for y in 0..height {
        let mut row = String::new();
        for x in 0..width {
            if let Some(cell) = buf.cell((x, y)) {
                row.push_str(cell.symbol());
            }
        }
        out.push_str(row.trim_end());
        out.push('\n');
    }
    out
}

/// true when the key means quit: q, Esc or Ctrl+C.
fn quits(ev: &Event) -> bool {
    let Event::Key(k) = ev else {
        return false;
    };
    k.kind == KeyEventKind::Press
        && (matches!(k.code, KeyCode::Char('q') | KeyCode::Esc)
            || (k.code == KeyCode::Char('c') && k.modifiers.contains(KeyModifiers::CONTROL)))
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.first().map(String::as_str) == Some("--figlet") {
        let font = args.get(1).map(String::as_str).unwrap_or("doh");
        let text = args.get(2).map(String::as_str).unwrap_or("0:00");
        match figlet::builtin(font) {
            Some(f) => print!("{}", f.render(text, 80)),
            None => {
                eprintln!("no such font: {font}");
                std::process::exit(1);
            }
        }
        return;
    }
    let root = repo_root();
    load_envrc(&root);
    let (ctx, _) = Ctx::load(root);
    if args.iter().any(|a| a == "--once") {
        let session = active_branch(&ctx.root).map(|_| Session::new(&ctx));
        let (w, h) = ratatui::crossterm::terminal::size()
            .ok()
            .filter(|(w, h)| *w > 0 && *h > 0)
            .unwrap_or((terminal_columns() as u16, 24));
        print!("{}", frame_text(session.as_ref(), w, h));
        return;
    }
    let mut terminal = ratatui::init();
    let mut branch: Option<String> = None;
    let mut session: Option<Session> = None;
    let mut stop = false;
    while !stop {
        let b = active_branch(&ctx.root);
        if b != branch {
            branch = b.clone();
            session = b.map(|_| Session::new(&ctx));
        }
        let _ = terminal.draw(|f| draw(f, session.as_ref()));
        // wake at the next whole second, or at once on a key or a resize
        let tick = Duration::from_millis(1000 - (now() * 1000.0) as u64 % 1000);
        if event::poll(tick).unwrap_or(false) {
            if let Ok(ev) = event::read() {
                stop = quits(&ev);
            }
        }
    }
    ratatui::restore();
    if let Some(s) = &session {
        println!(
            "{} - {} on the clock. `make solved` when it lands.",
            s.label,
            clock(now() - s.t0)
        );
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn clocks() {
        assert_eq!(super::clock(65.0), "1m 05s");
        assert_eq!(super::clock(0.0), "0m 00s");
        let lines = super::big_clock(65.0, 120, 40);
        assert!(lines.len() > 5);
        assert_eq!(super::big_clock(65.0, 10, 40), vec!["1m 05s".to_string()]);
        assert_eq!(super::big_clock(65.0, 120, 1), vec!["1m 05s".to_string()]);
    }

    #[test]
    fn idle_frame_is_a_panel() {
        let f = super::frame_text(None, 60, 7);
        assert!(f.starts_with('╭') && f.trim_end().ends_with('╯'));
        assert!(f.contains("idle - waiting"));
        assert!(f.lines().all(|l| l.chars().count() <= 60));
    }
}
