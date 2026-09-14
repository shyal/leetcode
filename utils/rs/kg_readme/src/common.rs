// What every chart shares: the GitHub dark palette, the badge, the month
// ticks, the split of a series at a gap over a month, and the number
// formats the Python renderers used (an f-string's `{x}` on a float is
// Python's repr, so an integral float prints as "62.0").

use chrono::{Datelike, Duration, NaiveDate};

pub const BG: &str = "#0d1117";
pub const MUTED: &str = "#8b949e";
pub const GRID: &str = "#21262d";
pub const GREEN: &str = "#3fb950";
pub const RED: &str = "#f85149";
pub const BLUE: &str = "#58a6ff";
pub const GOLD: &str = "#d29922";
pub const INK: &str = "#c9d1d9";

/// Python's repr of a float.
pub fn pyf(x: f64) -> String {
    if x == x.trunc() && x.abs() < 1e16 {
        format!("{:.1}", x)
    } else {
        format!("{}", x)
    }
}

/// Python's `{x:.1f}`.
pub fn f1(x: f64) -> String {
    format!("{:.1}", x)
}

/// Python's `{x:.0f}`.
pub fn f0(x: f64) -> String {
    format!("{:.0}", x)
}

/// Python's `{x:+.0f}`.
pub fn s0(x: f64) -> String {
    format!("{:+.0}", x)
}

/// Python's `x // n * n` on a float, as an int.
pub fn floor_to(x: f64, n: i64) -> i64 {
    (x / n as f64).floor() as i64 * n
}

/// Python's `-(-x // n) * n` on a float, as an int.
pub fn ceil_to(x: f64, n: i64) -> i64 {
    (x / n as f64).ceil() as i64 * n
}

/// statistics.median.
pub fn median(v: &[f64]) -> f64 {
    let mut s = v.to_vec();
    s.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let n = s.len();
    if n % 2 == 1 {
        s[n / 2]
    } else {
        (s[n / 2 - 1] + s[n / 2]) / 2.0
    }
}

pub fn days_between(a: NaiveDate, b: NaiveDate) -> i64 {
    (b - a).num_days()
}

/// The first of the next month.
pub fn next_month(d: NaiveDate) -> NaiveDate {
    let d = d.with_day(28).unwrap() + Duration::days(4);
    d.with_day(1).unwrap()
}

/// `date(d0.year, d0.month, 1)`.
pub fn month_start(d: NaiveDate) -> NaiveDate {
    d.with_day(1).unwrap()
}

/// The series split wherever it skips more than a month.
pub fn runs<T: Clone>(series: &[(NaiveDate, T)]) -> Vec<Vec<(NaiveDate, T)>> {
    let mut out: Vec<Vec<(NaiveDate, T)>> = vec![Vec::new()];
    let mut prev: Option<NaiveDate> = None;
    for (d, v) in series {
        if let Some(p) = prev {
            if days_between(p, *d) > 31 {
                out.push(Vec::new());
            }
        }
        out.last_mut().unwrap().push((*d, v.clone()));
        prev = Some(*d);
    }
    out
}

pub fn points<F: Fn(NaiveDate) -> f64, G: Fn(f64) -> f64>(
    run: &[(NaiveDate, f64)],
    x_of: F,
    y_of: G,
) -> String {
    run.iter()
        .map(|(d, v)| format!("{},{}", f1(x_of(*d)), f1(y_of(*v))))
        .collect::<Vec<_>>()
        .join(" ")
}

/// A shields-style badge: grey left half, coloured right half.
pub fn badge(left: &str, right: &str, color: &str) -> String {
    let lw = (6 * left.chars().count() + 12) as f64;
    let rw = 6.2 * right.chars().count() as f64 + 12.0;
    let w = lw + rw;
    format!(
        "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{}\" height=\"20\" \
         font-family=\"Verdana,DejaVu Sans,sans-serif\" font-size=\"11\">\
         <rect rx=\"3\" width=\"{}\" height=\"20\" fill=\"#555\"/>\
         <rect rx=\"3\" x=\"{}\" width=\"{}\" height=\"20\" fill=\"{color}\"/>\
         <rect x=\"{}\" width=\"4\" height=\"20\" fill=\"{color}\"/>\
         <text x=\"{}\" y=\"14\" fill=\"#fff\" text-anchor=\"middle\">{left}</text>\
         <text x=\"{}\" y=\"14\" fill=\"#fff\" text-anchor=\"middle\">{right}</text>\
         </svg>\n",
        f0(w),
        f0(w),
        f0(lw),
        f0(rw),
        f0(lw),
        f1(lw / 2.0),
        f1(lw + rw / 2.0),
    )
}

/// The month grid: one line and label per month start inside [d0, d1].
pub fn month_ticks<F: Fn(NaiveDate) -> f64>(
    svg: &mut Vec<String>,
    d0: NaiveDate,
    d1: NaiveDate,
    x_of: F,
    top: i64,
    bottom: i64,
    step: u32,
) {
    let mut d = month_start(d0);
    while d <= d1 {
        if d >= d0 && (d.month() - 1).is_multiple_of(step) {
            let x = f1(x_of(d));
            svg.push(format!(
                "<line x1=\"{x}\" y1=\"{top}\" x2=\"{x}\" y2=\"{bottom}\" stroke=\"{GRID}\" stroke-width=\"1\"/>"
            ));
            svg.push(format!(
                "<text x=\"{x}\" y=\"{}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{}</text>",
                bottom + 18,
                d.format("%b %y")
            ));
        }
        d = next_month(d);
    }
}

/// The vertical grid for a short window: a line and a day label every
/// `step` days, counted back from d1 so the last tick is the last day.
pub fn day_ticks<F: Fn(NaiveDate) -> f64>(
    svg: &mut Vec<String>,
    d0: NaiveDate,
    d1: NaiveDate,
    x_of: F,
    top: i64,
    bottom: i64,
    step: i64,
) {
    let mut d = d1;
    while d >= d0 {
        let x = f1(x_of(d));
        svg.push(format!(
            "<line x1=\"{x}\" y1=\"{top}\" x2=\"{x}\" y2=\"{bottom}\" stroke=\"{GRID}\" stroke-width=\"1\"/>"
        ));
        svg.push(format!(
            "<text x=\"{x}\" y=\"{}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{}</text>",
            bottom + 18,
            d.format("%b %d")
        ));
        d -= Duration::days(step);
    }
}

/// The horizontal grid: a line and a label every `step` from lo to hi.
pub fn value_ticks<G: Fn(f64) -> f64>(
    svg: &mut Vec<String>,
    lo: i64,
    hi: i64,
    step: i64,
    y_of: G,
    ml: i64,
    right: i64,
) {
    let mut g = lo;
    while g <= hi {
        let y = y_of(g as f64);
        svg.push(format!(
            "<line x1=\"{ml}\" y1=\"{}\" x2=\"{right}\" y2=\"{}\" stroke=\"{GRID}\" stroke-width=\"1\"/>",
            f1(y),
            f1(y)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">{g}</text>",
            ml - 8,
            f1(y + 4.0)
        ));
        g += step;
    }
}

/// The Knight and Guardian bands: a tinted rectangle above each cutoff, the
/// dashed line and its label at the right edge.
pub fn rank_bands<G: Fn(f64) -> f64>(
    svg: &mut Vec<String>,
    ranks: &[(i64, &str, &str)],
    y_of: G,
    ml: i64,
    w: i64,
    mr: i64,
    top: i64,
) {
    for (cut, name, color) in ranks {
        let y = y_of(*cut as f64);
        svg.push(format!(
            "<rect x=\"{ml}\" y=\"{top}\" width=\"{}\" height=\"{}\" fill=\"{color}\" fill-opacity=\"0.06\"/>",
            w - ml - mr,
            f1(y - top as f64)
        ));
        svg.push(format!(
            "<line x1=\"{ml}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{color}\" stroke-width=\"1\" stroke-dasharray=\"4 4\"/>",
            f1(y),
            w - mr,
            f1(y)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"11\" fill=\"{color}\">{name} {cut}</text>",
            w - mr - 4,
            f1(y - 5.0)
        ));
    }
}

/// The legend row: entries laid out left to right, 34px plus 6.2px per
/// character apart. Python started `x` as the int ML and made it a float
/// on the first advance, so the first entry prints "62" and the rest
/// print as floats; a chart that started from float(ML) prints "62.0".
pub struct Legend {
    pub x: f64,
    is_int: bool,
    pub y: i64,
}

impl Legend {
    pub fn new(x: i64, is_int: bool, y: i64) -> Legend {
        Legend {
            x: x as f64,
            is_int,
            y,
        }
    }

    fn fx(&self, x: f64) -> String {
        if self.is_int {
            format!("{}", x as i64)
        } else {
            pyf(x)
        }
    }

    fn label(&mut self, svg: &mut Vec<String>, label: &str) {
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" font-size=\"11\" fill=\"{MUTED}\">{label}</text>",
            self.fx(self.x + 22.0),
            self.y + 4
        ));
        self.x += 34.0 + 6.2 * label.chars().count() as f64;
        self.is_int = false;
    }

    pub fn line(&mut self, svg: &mut Vec<String>, color: &str, label: &str, dash: bool) {
        let d = if dash {
            " stroke-dasharray=\"6 4\""
        } else {
            ""
        };
        svg.push(format!(
            "<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{color}\" stroke-width=\"2\"{d}/>",
            self.fx(self.x),
            self.y,
            self.fx(self.x + 16.0),
            self.y
        ));
        self.label(svg, label);
    }

    pub fn dot(&mut self, svg: &mut Vec<String>, color: &str, label: &str) {
        svg.push(format!(
            "<circle cx=\"{}\" cy=\"{}\" r=\"3\" fill=\"{color}\"/>",
            self.fx(self.x + 8.0),
            self.y
        ));
        self.label(svg, label);
    }

    pub fn swatch(&mut self, svg: &mut Vec<String>, color: &str, opacity: &str, label: &str) {
        svg.push(format!(
            "<rect x=\"{}\" y=\"{}\" width=\"16\" height=\"8\" fill=\"{color}\" fill-opacity=\"{opacity}\"/>",
            self.fx(self.x),
            self.y - 4
        ));
        self.label(svg, label);
    }
}

/// An opacity from the environment (.envrc is loaded): a number in 0..=1,
/// else `default`.
fn opacity(name: &str, default: &str) -> String {
    match std::env::var(name)
        .ok()
        .and_then(|v| v.trim().parse::<f64>().ok())
    {
        Some(x) if (0.0..=1.0).contains(&x) => x.to_string(),
        _ => default.to_string(),
    }
}

/// README_ELO_OPACITY: the raw elo line under its moving average.
pub fn elo_opacity() -> String {
    opacity("README_ELO_OPACITY", "0.55")
}

/// README_SIM_OPACITY: the forecast's simulated attempts in the problems chart.
pub fn sim_opacity() -> String {
    opacity("README_SIM_OPACITY", "0.2")
}

pub fn write(path: &std::path::Path, svg: &[String]) {
    std::fs::write(path, svg.join("\n") + "\n").expect("write svg");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pyf_prints_like_python() {
        assert_eq!(pyf(62.0), "62.0");
        assert_eq!(pyf(114.60000000000001), "114.60000000000001");
        assert_eq!(pyf(0.35), "0.35");
    }

    #[test]
    fn median_averages_the_middle_pair() {
        assert_eq!(median(&[3.0, 1.0, 2.0]), 2.0);
        assert_eq!(median(&[4.0, 1.0, 3.0, 2.0]), 2.5);
    }

    #[test]
    fn runs_split_at_a_month() {
        let d0 = NaiveDate::from_ymd_opt(2026, 1, 1).unwrap();
        let s = vec![
            (d0, 0.0),
            (d0 + Duration::days(10), 0.0),
            (d0 + Duration::days(50), 0.0),
        ];
        assert_eq!(
            runs(&s).iter().map(Vec::len).collect::<Vec<_>>(),
            vec![2, 1]
        );
    }

    #[test]
    fn badge_names_both_halves() {
        let b = badge("vs all rated", "top 24%", MUTED);
        assert!(b.contains("vs all rated") && b.contains("top 24%"));
    }
}
