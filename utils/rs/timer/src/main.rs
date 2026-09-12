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
// Ported from utils/kg/timer (Python) on 2026-09-12; the rich Live display
// became a redraw-in-place loop with the same panel, bars and figlet clock.

use std::io::Write;
use std::sync::atomic::{AtomicBool, Ordering};

use kg::cells::cell_len;
use kg::console::{terminal_columns, Style};
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root};
use kg::figlet;
use kg::git::active_seconds;
use kg::model::{drill_forecast, solve_forecast};
use regex::Regex;

static STOP: AtomicBool = AtomicBool::new(false);
/// colour only on a tty (rich's rule), set once at start
static COLOR: AtomicBool = AtomicBool::new(false);

extern "C" fn on_sigint(_: libc::c_int) {
    STOP.store(true, Ordering::SeqCst);
}

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
/// plain text when the pane is too narrow.
fn big_clock(secs: f64, width: usize) -> Vec<String> {
    let s = secs as i64;
    let face = format!("{}:{:02}", s / 60, s % 60);
    let first = std::env::var("TIMER_FONT").unwrap_or_else(|_| "doh".to_string());
    for font in [first.as_str(), "univers", "big"] {
        let Some(f) = figlet::builtin(font) else {
            continue;
        };
        let art = f.render(&face, 80);
        let lines: Vec<String> = art
            .trim_end()
            .lines()
            .filter(|l| !l.trim().is_empty())
            .map(String::from)
            .collect();
        if !lines.is_empty()
            && lines.iter().map(|l| l.chars().count()).max().unwrap() <= width.saturating_sub(4)
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
            return ("cyan", "no forecast — plain clock");
        }
        if elapsed > self.marks[2].1 {
            return ("red", "past the stop mark — bank it, reinforce");
        }
        if elapsed > self.marks[1].1 {
            return ("yellow", "hint is fair game");
        }
        if elapsed > self.marks[0].1 {
            return ("yellow", "past expected — keep going");
        }
        ("green", "on pace")
    }
}

fn sgr(style: &str) -> String {
    if !COLOR.load(Ordering::Relaxed) {
        return String::new();
    }
    let st = Style::parse(style);
    if st.is_plain() {
        String::new()
    } else {
        format!("\x1b[{}m", st.sgr())
    }
}

fn paint(text: &str, style: &str) -> String {
    let code = sgr(style);
    if code.is_empty() {
        text.to_string()
    } else {
        format!("{code}{text}\x1b[0m")
    }
}

/// rich's ProgressBar: "━" for the done part (a half block at the edge),
/// dim "━" for the rest.
fn bar(width: usize, completed: f64, total: f64, finished: bool) -> String {
    let frac = if total > 0.0 {
        (completed / total).clamp(0.0, 1.0)
    } else {
        0.0
    };
    let halves = (width as f64 * 2.0 * frac) as usize;
    let full = halves / 2;
    let half = halves % 2 == 1;
    let mut s = String::new();
    let done: String = "━".repeat(full);
    s.push_str(&paint(&done, if finished { "bold cyan" } else { "cyan" }));
    let mut rest = width.saturating_sub(full);
    if half && rest > 0 {
        s.push_str(&paint("╸", "cyan"));
        rest -= 1;
    }
    s.push_str(&paint(&"━".repeat(rest), "dim"));
    s
}

/// A rich Panel with padding (1, 2) at the terminal width: the top rule
/// carries the title, the bottom one the subtitle, both centred.
fn panel(body: &[String], title: &str, subtitle: &str, border: &str, width: usize) -> Vec<String> {
    let inner = width.saturating_sub(4);
    let rule = |text: &str, l: char, r: char| -> String {
        let t = if text.is_empty() {
            String::new()
        } else {
            format!(" {text} ")
        };
        let excess = inner.saturating_sub(cell_len(&t));
        let (a, b) = (excess / 2, excess - excess / 2);
        format!(
            "{}{}{}{}",
            paint(&format!("{l}─{}", "─".repeat(a)), border),
            paint(&t, "bold"),
            paint(&"─".repeat(b), border),
            paint(&format!("─{r}"), border)
        )
    };
    let mut out = vec![rule(title, '╭', '╮')];
    let line = |s: &str| -> String {
        let pad = inner.saturating_sub(2).saturating_sub(visible_len(s));
        format!(
            "{}   {s}{}   {}",
            paint("│", border),
            " ".repeat(pad),
            paint("│", border)
        )
    };
    out.push(line(""));
    for l in body {
        out.push(line(l));
    }
    out.push(line(""));
    out.push(rule(subtitle, '╰', '╯'));
    out
}

/// Cells of a string with its ANSI escapes stripped.
fn visible_len(s: &str) -> usize {
    let re = Regex::new("\x1b\\[[0-9;]*m").unwrap();
    cell_len(&re.replace_all(s, ""))
}

fn center(s: &str, width: usize) -> String {
    let pad = width.saturating_sub(visible_len(s)) / 2;
    format!("{}{s}", " ".repeat(pad))
}

fn render(session: &Session, width: usize) -> Vec<String> {
    let elapsed = now() - session.t0;
    let (color, message) = session.zone(elapsed);
    let inner = width.saturating_sub(6); // the panel's border and padding
    let mut body: Vec<String> = big_clock(elapsed, width)
        .iter()
        .map(|l| center(&paint(l, &format!("bold {color}")), inner))
        .collect();
    if !session.marks.is_empty() {
        body.push(String::new());
        // description(15) | bar | mark | left(10), one space between
        let bar_width = inner.saturating_sub(15 + 1 + 1 + 6 + 1 + 10);
        for (name, total, c) in &session.marks {
            let left = if elapsed >= *total {
                String::new()
            } else {
                format!("-{}", clock(total - elapsed))
            };
            body.push(format!(
                "{} {} {} {:>10}",
                paint(&format!("{name:<15}"), c),
                bar(bar_width, elapsed.min(*total), *total, elapsed >= *total),
                paint(&format!("{:<6}", clock(*total)), "dim"),
                left
            ));
        }
    }
    let mut subtitle = paint(message, color);
    if session.parks > 0 {
        let (sh, sm) = (session.slept / 60 / 60, session.slept / 60 % 60);
        subtitle.push_str(&paint(
            &format!("  · slept {sh}h {sm:02}m over {} park(s)", session.parks),
            "dim",
        ));
    }
    panel(
        &body,
        &paint(&session.label, "bold"),
        &subtitle,
        color,
        width,
    )
}

fn idle(width: usize) -> Vec<String> {
    let text = paint(
        "idle — waiting for a solve branch (`make next`, `make drill`)",
        "dim",
    );
    panel(
        &[center(&text, width.saturating_sub(6))],
        "",
        "",
        "dim",
        width,
    )
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
    let once = args.iter().any(|a| a == "--once");
    COLOR.store(kg::console::Console::new().color, Ordering::Relaxed);
    let root = repo_root();
    load_envrc(&root);
    let (ctx, _) = Ctx::load(root);
    // SAFETY: a plain flag-setting handler
    unsafe {
        libc::signal(libc::SIGINT, on_sigint as *const () as libc::sighandler_t);
    }
    let mut branch: Option<String> = None;
    let mut session: Option<Session> = None;
    let mut drawn = 0usize;
    let mut out = std::io::stdout();
    loop {
        let b = active_branch(&ctx.root);
        if b != branch {
            branch = b.clone();
            session = b.map(|_| Session::new(&ctx));
        }
        let width = terminal_columns();
        let frame = match &session {
            Some(s) => render(s, width),
            None => idle(width),
        };
        if drawn > 0 {
            let _ = write!(out, "\x1b[{drawn}A\x1b[J");
        }
        for l in &frame {
            let _ = writeln!(out, "{l}");
        }
        let _ = out.flush();
        drawn = frame.len();
        if once {
            return;
        }
        for _ in 0..10 {
            if STOP.load(Ordering::SeqCst) {
                if let Some(s) = &session {
                    println!(
                        "{} — {} on the clock. `make solved` when it lands.",
                        s.label,
                        clock(now() - s.t0)
                    );
                }
                return;
            }
            std::thread::sleep(std::time::Duration::from_millis(100));
        }
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn clocks() {
        assert_eq!(super::clock(65.0), "1m 05s");
        assert_eq!(super::clock(0.0), "0m 00s");
        let lines = super::big_clock(65.0, 120);
        assert!(lines.len() > 5);
        assert_eq!(super::big_clock(65.0, 10), vec!["1m 05s".to_string()]);
    }
}
