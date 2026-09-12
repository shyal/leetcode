// The input-tree drawing (utils/kg/kg_render.py): one graphviz digraph
// of the pick's moves and every transitive prerequisite, each node filled
// by its degree of ownership on the red-to-green OKLCH ramp
// (kg_lib.degree_color), rendered to graph/kg_next.svg and .png by `dot`
// and shown inline through the iTerm2 image protocol. Cosmetic: a failure
// here never touches the pick.

use std::io::Write;
use std::path::Path;
use std::process::{Command, Stdio};

use crate::console::{stdout_is_tty, Console};
use crate::status::Status;

pub const STATUS_FACE: [(&str, &[&str]); 4] = [
    ("SOLID", &["😄", "💪", "😎", "✨", "💎", "🟢"]),
    ("STALE", &["😐", "🫤", "😑", "😴", "🥀", "⌛"]),
    ("FRAGILE", &["😰", "🫠", "🥲", "😬", "💔", "😵"]),
    ("MISSING", &["👻", "❔", "😶", "🫥", "🕳"]),
];

pub fn faces(status: Status) -> &'static [&'static str] {
    let key = status.to_string();
    STATUS_FACE
        .iter()
        .find(|(k, _)| *k == key)
        .map(|(_, f)| *f)
        .unwrap()
}

fn srgb_to_linear(c: f64) -> f64 {
    let c = c / 255.0;
    if c <= 0.04045 {
        c / 12.92
    } else {
        ((c + 0.055) / 1.055).powf(2.4)
    }
}

fn linear_to_srgb(c: f64) -> f64 {
    let c = c.clamp(0.0, 1.0);
    if c <= 0.0031308 {
        12.92 * c
    } else {
        1.055 * c.powf(1.0 / 2.4) - 0.055
    }
}

fn hex_to_oklab(h: &str) -> (f64, f64, f64) {
    let ch = |i: usize| srgb_to_linear(u8::from_str_radix(&h[i..i + 2], 16).unwrap_or(0) as f64);
    let (r, g, b) = (ch(1), ch(3), ch(5));
    let l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b).cbrt();
    let m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b).cbrt();
    let s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b).cbrt();
    (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )
}

fn oklab_to_hex(l: f64, a: f64, b: f64) -> String {
    let l_ = (l + 0.3963377774 * a + 0.2158037573 * b).powi(3);
    let m_ = (l - 0.1055613458 * a - 0.0638541728 * b).powi(3);
    let s_ = (l - 0.0894841775 * a - 1.2914855480 * b).powi(3);
    let r = 4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_;
    let g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_;
    let bl = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_;
    let q = |c: f64| (linear_to_srgb(c) * 255.0).round_ties_even() as u8;
    format!("#{:02x}{:02x}{:02x}", q(r), q(g), q(bl))
}

fn lch(hex: &str) -> (f64, f64, f64) {
    let (l, a, b) = hex_to_oklab(hex);
    let h = b.atan2(a).rem_euclid(2.0 * std::f64::consts::PI);
    (l, a.hypot(b), h)
}

/// kg_lib.degree_color: the hex colour of a degree of ownership.
pub fn degree_color(degree: f64) -> String {
    let (l0, c0, h0) = lch("#da3633");
    let (l1, c1, h1) = lch("#3fb950");
    let t = degree.clamp(0.0, 1.0);
    let pi = std::f64::consts::PI;
    let dh = (h1 - h0 + pi).rem_euclid(2.0 * pi) - pi;
    let (l, c, h) = (l0 + (l1 - l0) * t, c0 + (c1 - c0) * t, h0 + dh * t);
    oklab_to_hex(l, c * h.cos(), c * h.sin())
}

fn q(s: &str) -> String {
    format!("\"{}\"", s.replace('\\', "\\\\").replace('"', "\\\""))
}

/// A DOT source in the making, with kg_render.make_digraph's look. Nodes
/// and edges land in the open subgraph, if any (kg_viz's clusters).
pub struct Dot {
    lines: Vec<String>,
    depth: usize,
}

impl Dot {
    pub fn new(name: &str) -> Dot {
        let mut lines = vec![format!("digraph {} {{", q(name))];
        lines.push("\tgraph [bgcolor=\"#0d1117\" compound=true fontname=Helvetica nodesep=0.25 rankdir=TB ranksep=0.6]".into());
        lines.push("\tnode [color=\"#30363d\" fontcolor=white fontname=Helvetica fontsize=11 margin=\"0.12,0.06\" shape=box style=\"rounded,filled\"]".into());
        lines.push("\tedge [arrowsize=0.6 color=\"#8b949e\"]".into());
        Dot { lines, depth: 1 }
    }

    fn indent(&self) -> String {
        "\t".repeat(self.depth)
    }

    pub fn node(&mut self, id: &str, attrs: &[(&str, &str)]) {
        let a: Vec<String> = attrs.iter().map(|(k, v)| format!("{k}={}", q(v))).collect();
        self.lines
            .push(format!("{}{} [{}]", self.indent(), q(id), a.join(" ")));
    }

    pub fn edge(&mut self, a: &str, b: &str, attrs: &[(&str, &str)]) {
        let at: Vec<String> = attrs.iter().map(|(k, v)| format!("{k}={}", q(v))).collect();
        let ind = self.indent();
        if at.is_empty() {
            self.lines.push(format!("{ind}{} -> {}", q(a), q(b)));
        } else {
            self.lines
                .push(format!("{ind}{} -> {} [{}]", q(a), q(b), at.join(" ")));
        }
    }

    /// `with dot.subgraph(name=...) as c: c.attr(...)`: open a subgraph
    /// with these attributes; nodes added until end_subgraph() belong to it.
    pub fn begin_subgraph(&mut self, name: &str, attrs: &[(&str, &str)]) {
        self.lines
            .push(format!("{}subgraph {} {{", self.indent(), q(name)));
        self.depth += 1;
        // the graphviz library writes a subgraph's attributes sorted by name
        let mut a: Vec<String> = attrs.iter().map(|(k, v)| format!("{k}={}", q(v))).collect();
        a.sort();
        self.lines.push(format!("{}{}", self.indent(), a.join(" ")));
    }

    pub fn end_subgraph(&mut self) {
        self.depth -= 1;
        self.lines.push(format!("{}}}", self.indent()));
    }

    /// kg_render.add_legend: the ownership ramp, five swatches from none
    /// to full.
    pub fn legend(&mut self) {
        self.begin_subgraph(
            "cluster_legend",
            &[
                ("label", "degree of ownership"),
                ("fontcolor", "#8b949e"),
                ("color", "#30363d"),
                ("style", "rounded"),
            ],
        );
        for d in [0.0, 0.25, 0.5, 0.75, 1.0] {
            let id = format!("legend_{}", (d * 100.0) as i64);
            let label = format!("{d:.2}");
            let fill = degree_color(d);
            self.node(&id, &[("label", &label), ("fillcolor", &fill)]);
        }
        self.end_subgraph();
    }

    /// kg_render.status_node: a box filled by degree, labeled by name or
    /// by status and a face.
    pub fn status_node(
        &mut self,
        id: &str,
        name: &str,
        status: Status,
        when: Option<&str>,
        highlight: bool,
        label: &str,
        degree: f64,
    ) {
        let mut tooltip = format!("{name} - {status}");
        if let Some(w) = when {
            tooltip.push_str(&format!(" ({w})"));
        }
        tooltip.push_str(&format!(", owned {degree:.2}"));
        let fill = degree_color(degree);
        let mut attrs: Vec<(&str, &str)> = vec![
            ("label", label),
            ("fillcolor", &fill),
            ("tooltip", &tooltip),
        ];
        if highlight {
            attrs.push(("color", "#c9d1d9"));
            attrs.push(("penwidth", "2"));
        }
        self.node(id, &attrs);
    }

    pub fn source(&self) -> String {
        let mut s = self.lines.join("\n");
        s.push_str("\n}\n");
        s
    }
}

fn png_width(path: &Path) -> Option<u32> {
    let bytes = std::fs::read(path).ok()?;
    if bytes.len() < 20 {
        return None;
    }
    Some(u32::from_be_bytes([
        bytes[16], bytes[17], bytes[18], bytes[19],
    ]))
}

/// A `dot` started before the graph is known, reading it from stdin: its
/// process and plugin start-up (a dozen ms) overlaps the JSON load and
/// the pick. Dropped unused, it is killed.
pub struct PreDot {
    child: std::process::Child,
}

impl Drop for PreDot {
    fn drop(&mut self) {
        let _ = self.child.kill();
        let _ = self.child.wait();
    }
}

/// Start `dot` for a drawing that will land in `graph_dir`, before the
/// drawing exists.
pub fn prespawn_dot(graph_dir: &Path) -> Option<PreDot> {
    let child = Command::new("dot")
        .args(["-Tsvg", "-Tpng", "-Gdpi=192", "-O"])
        .current_dir(graph_dir)
        .stdin(Stdio::piped())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .ok()?;
    Some(PreDot { child })
}

/// kg_render.render, on a thread: svg and png into graph/ from ONE `dot`
/// run (the layout is what costs; a second output is free), the png at
/// twice the logical size so it stays crisp on a retina display. The
/// same source draws the same picture, so the last source's hash and
/// width are kept next to the files and a repeat is not laid out again.
/// Returns the graph's logical width in px, the size iTerm shows it at.
pub fn render_in_background(
    graph_dir: std::path::PathBuf,
    source: String,
    basename: &str,
    pre: Option<PreDot>,
) -> std::thread::JoinHandle<Result<u32, String>> {
    let basename = basename.to_string();
    std::thread::spawn(move || {
        let stamp = graph_dir.join(format!(".{basename}.stamp"));
        let hash = fnv(source.as_bytes());
        let png = graph_dir.join(format!("{basename}.png"));
        let svg = graph_dir.join(format!("{basename}.svg"));
        if let Ok(text) = std::fs::read_to_string(&stamp) {
            if let Some((h, w)) = text.trim().split_once(' ') {
                if h == hash && png.exists() && svg.exists() {
                    if let Ok(w) = w.parse::<u32>() {
                        drop(pre);
                        return Ok(w);
                    }
                }
            }
        }
        match pre {
            Some(mut pre) => {
                // the graph goes down the pipe; dot names stdin's outputs
                // noname.gv.*, renamed into place
                {
                    let mut stdin = pre.child.stdin.take().ok_or("dot stdin")?;
                    stdin
                        .write_all(source.as_bytes())
                        .map_err(|e| format!("dot: {e}"))?;
                }
                let status = pre.child.wait().map_err(|e| format!("dot: {e}"))?;
                if !status.success() {
                    return Err(format!("dot exited {status}"));
                }
                for ext in ["svg", "png"] {
                    std::fs::rename(
                        graph_dir.join(format!("noname.gv.{ext}")),
                        graph_dir.join(format!("{basename}.{ext}")),
                    )
                    .map_err(|e| format!("dot output: {e}"))?;
                }
            }
            None => {
                let src = graph_dir.join(&basename);
                std::fs::write(&src, source).map_err(|e| e.to_string())?;
                let status = Command::new("dot")
                    .args(["-Tsvg", "-Tpng", "-Gdpi=192", "-O"])
                    .arg(&src)
                    .stdout(Stdio::null())
                    .stderr(Stdio::null())
                    .status()
                    .map_err(|e| format!("dot: {e}"));
                let _ = std::fs::remove_file(&src);
                let status = status?;
                if !status.success() {
                    return Err(format!("dot exited {status}"));
                }
            }
        }
        let w = png_width(&png).ok_or("png width")?.div_ceil(2);
        let _ = std::fs::write(&stamp, format!("{hash} {w}\n"));
        Ok(w)
    })
}

/// kg_render.render, waited for: svg and png into graph_dir, the logical
/// width in px (kg_viz).
pub fn render(graph_dir: &Path, source: String, basename: &str) -> Result<u32, String> {
    render_in_background(graph_dir.to_path_buf(), source, basename, None)
        .join()
        .map_err(|_| "render thread".to_string())?
}

/// FNV-1a over the bytes, as hex.
fn fnv(bytes: &[u8]) -> String {
    let mut h: u64 = 0xcbf29ce484222325;
    for b in bytes {
        h ^= *b as u64;
        h = h.wrapping_mul(0x100000001b3);
    }
    format!("{h:016x}")
}

fn is_iterm() -> bool {
    let term = std::env::var("LC_TERMINAL")
        .or_else(|_| std::env::var("TERM_PROGRAM"))
        .unwrap_or_default();
    term == "iTerm2" || term == "iTerm.app"
}

/// kg_render.display: inline in iTerm, `open` the svg on another tty,
/// nothing when piped.
pub fn display(console: &Console, graph_dir: &Path, basename: &str, width_px: u32) {
    if !stdout_is_tty() {
        return;
    }
    let png = graph_dir.join(format!("{basename}.png"));
    if is_iterm() {
        if let Ok(bytes) = std::fs::read(&png) {
            let payload = base64(&bytes);
            let name = base64(format!("{basename}.png").as_bytes());
            console.raw(&format!(
                "\x1b]1337;File=name={name};size={};inline=1;width={width_px}px;preserveAspectRatio=1:{payload}\x07\n",
                payload.len()
            ));
            return;
        }
    }
    let _ = Command::new("open")
        .arg(graph_dir.join(format!("{basename}.svg")))
        .status();
}

fn base64(bytes: &[u8]) -> String {
    const T: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut out = String::with_capacity(bytes.len() * 4 / 3 + 4);
    for chunk in bytes.chunks(3) {
        let b = [
            chunk[0],
            *chunk.get(1).unwrap_or(&0),
            *chunk.get(2).unwrap_or(&0),
        ];
        let n = ((b[0] as u32) << 16) | ((b[1] as u32) << 8) | b[2] as u32;
        out.push(T[(n >> 18) as usize & 63] as char);
        out.push(T[(n >> 12) as usize & 63] as char);
        out.push(if chunk.len() > 1 {
            T[(n >> 6) as usize & 63] as char
        } else {
            '='
        });
        out.push(if chunk.len() > 2 {
            T[n as usize & 63] as char
        } else {
            '='
        });
    }
    out
}

/// kg_render.animate: through ttfx on a tty, plain otherwise.
pub fn animate(console: &Console, lines: Vec<crate::console::Line>) {
    animate_with(console, lines, &["decrypt", "--typing-speed", "20"]);
}

/// animate with a chosen ttfx effect and its arguments (kg_hard's laseretch).
pub fn animate_with(console: &Console, lines: Vec<crate::console::Line>, effect: &[&str]) {
    let plain = std::env::var("LEET_NO_ANIMATE").is_ok_and(|v| !v.is_empty());
    let exe = which("ttfx");
    if plain || !stdout_is_tty() || exe.is_none() {
        console.print_lines(lines);
        return;
    }
    let text: String = lines
        .iter()
        .map(|l| console.render_line(l) + "\n")
        .collect();
    let child = Command::new(exe.unwrap())
        .args(["--frame-rate", "360", "--existing-color-handling", "always"])
        .args(effect)
        .stdin(Stdio::piped())
        .spawn();
    match child {
        Ok(mut c) => {
            if let Some(mut stdin) = c.stdin.take() {
                let _ = stdin.write_all(text.as_bytes());
            }
            let _ = c.wait();
        }
        Err(_) => console.print_lines(lines),
    }
}

fn which(name: &str) -> Option<std::path::PathBuf> {
    let path = std::env::var_os("PATH")?;
    std::env::split_paths(&path)
        .map(|d| d.join(name))
        .find(|p| p.is_file())
}
