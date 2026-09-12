// A small mirror of the rich console `make next` prints through: markup
// tags ([dim]...[/dim], [bold], the colours) parsed into styled spans, word
// wrapping at the console width (rich._wrap.divide_line), and lines of
// styled segments written plain when stdout is not a terminal and with SGR
// codes when it is. The layout (widths, padding, wrapping) is the part the
// parity test pins down; the colours only have to look the same.

use std::cell::RefCell;
use std::io::Write;

use crate::cells::{cell_len, chop_cells, set_cell_size};

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Color {
    Green,
    Yellow,
    Red,
    Cyan,
    DarkOrange,
    Grey15,
}

impl Color {
    fn sgr(self, bg: bool) -> String {
        match (self, bg) {
            (Color::Green, false) => "32".into(),
            (Color::Yellow, false) => "33".into(),
            (Color::Red, false) => "31".into(),
            (Color::Cyan, false) => "36".into(),
            (Color::DarkOrange, false) => "38;5;208".into(),
            (Color::Grey15, false) => "38;5;235".into(),
            (Color::Green, true) => "42".into(),
            (Color::Yellow, true) => "43".into(),
            (Color::Red, true) => "41".into(),
            (Color::Cyan, true) => "46".into(),
            (Color::DarkOrange, true) => "48;5;208".into(),
            (Color::Grey15, true) => "48;5;235".into(),
        }
    }
}

#[derive(Clone, Copy, PartialEq, Eq, Debug, Default)]
pub struct Style {
    pub bold: bool,
    pub dim: bool,
    pub fg: Option<Color>,
    pub bg: Option<Color>,
}

impl Style {
    pub fn parse(name: &str) -> Style {
        let mut st = Style::default();
        let mut on = false;
        for word in name.split_whitespace() {
            if word == "on" {
                on = true;
                continue;
            }
            let colour = match word {
                "green" => Some(Color::Green),
                "yellow" => Some(Color::Yellow),
                "red" => Some(Color::Red),
                "cyan" => Some(Color::Cyan),
                "dark_orange" => Some(Color::DarkOrange),
                "grey15" => Some(Color::Grey15),
                _ => None,
            };
            match word {
                "bold" => st.bold = true,
                "dim" => st.dim = true,
                _ => {
                    if on {
                        st.bg = colour;
                    } else {
                        st.fg = colour;
                    }
                }
            }
            on = false;
        }
        st
    }

    /// rich's Style + Style: the right side wins where it says something.
    pub fn plus(self, other: Style) -> Style {
        Style {
            bold: self.bold || other.bold,
            dim: self.dim || other.dim,
            fg: other.fg.or(self.fg),
            bg: other.bg.or(self.bg),
        }
    }

    pub fn is_plain(&self) -> bool {
        *self == Style::default()
    }

    pub fn sgr(&self) -> String {
        let mut codes: Vec<String> = Vec::new();
        if self.bold {
            codes.push("1".into());
        }
        if self.dim {
            codes.push("2".into());
        }
        if let Some(c) = self.fg {
            codes.push(c.sgr(false));
        }
        if let Some(c) = self.bg {
            codes.push(c.sgr(true));
        }
        codes.join(";")
    }
}

#[derive(Clone, Debug)]
pub struct Seg {
    pub text: String,
    pub style: Style,
}

pub type Line = Vec<Seg>;

pub fn line_len(line: &Line) -> usize {
    line.iter().map(|s| cell_len(&s.text)).sum()
}

pub fn line_plain(line: &Line) -> String {
    line.iter().map(|s| s.text.as_str()).collect()
}

/// rich.Segment.adjust_line_length: pad with spaces or crop to `width`.
pub fn adjust_line(line: &Line, width: usize, style: Style) -> Line {
    let len = line_len(line);
    if len < width {
        let mut out = line.clone();
        out.push(Seg {
            text: " ".repeat(width - len),
            style,
        });
        out
    } else if len > width {
        let mut out = Vec::new();
        let mut used = 0;
        for seg in line {
            let w = cell_len(&seg.text);
            if used + w <= width {
                out.push(seg.clone());
                used += w;
            } else {
                out.push(Seg {
                    text: set_cell_size(&seg.text, width - used),
                    style: seg.style,
                });
                break;
            }
        }
        out
    } else {
        line.clone()
    }
}

/// rich.Segment.set_shape: every line `width` wide, `height` lines tall.
pub fn set_shape(lines: &[Line], width: usize, height: usize, style: Style) -> Vec<Line> {
    let mut out: Vec<Line> = lines
        .iter()
        .take(height)
        .map(|l| adjust_line(l, width, style))
        .collect();
    while out.len() < height {
        out.push(vec![Seg {
            text: " ".repeat(width),
            style,
        }]);
    }
    out
}

/// Styled text: the plain string and (start, end, style) spans over its
/// characters, the shape rich.Text keeps.
#[derive(Clone, Debug, Default)]
pub struct Text {
    pub plain: String,
    pub spans: Vec<(usize, usize, Style)>,
    pub base: Style,
}

impl Text {
    pub fn plain(s: &str) -> Text {
        Text {
            plain: s.to_string(),
            spans: vec![],
            base: Style::default(),
        }
    }

    /// rich.markup.render: tags open styles, [/tag] and [/] close them,
    /// "\[" is a literal bracket. A tag is "[" then one of a-z # / @, then
    /// anything but "[" up to the next "]".
    pub fn from_markup(markup: &str) -> Text {
        let chars: Vec<char> = markup.chars().collect();
        let mut plain: Vec<char> = Vec::new();
        let mut spans: Vec<(usize, usize, Style)> = Vec::new();
        let mut open: Vec<(String, usize)> = Vec::new();
        let mut i = 0;
        while i < chars.len() {
            let c = chars[i];
            if c == '\\' && i + 1 < chars.len() && chars[i + 1] == '[' {
                if let Some(tag_end) = tag_at(&chars, i + 1) {
                    // an escaped tag: the bracket text is literal
                    plain.extend(&chars[i + 1..=tag_end]);
                    i = tag_end + 1;
                    continue;
                }
            }
            if c == '[' {
                if let Some(end) = tag_at(&chars, i) {
                    let name: String = chars[i + 1..end].iter().collect();
                    if let Some(closing) = name.strip_prefix('/') {
                        let closing = closing.trim();
                        let idx = if closing.is_empty() {
                            open.len().checked_sub(1)
                        } else {
                            open.iter().rposition(|(n, _)| n == closing)
                        };
                        if let Some(idx) = idx {
                            let (n, start) = open.remove(idx);
                            spans.push((start, plain.len(), Style::parse(&n)));
                        }
                    } else {
                        open.push((name.trim().to_string(), plain.len()));
                    }
                    i = end + 1;
                    continue;
                }
            }
            plain.push(c);
            i += 1;
        }
        for (n, start) in open {
            spans.push((start, plain.len(), Style::parse(&n)));
        }
        Text {
            plain: plain.into_iter().collect(),
            spans,
            base: Style::default(),
        }
    }

    pub fn cell_len(&self) -> usize {
        cell_len(&self.plain)
    }

    fn style_at(&self, i: usize) -> Style {
        let mut st = self.base;
        for (s, e, sp) in &self.spans {
            if *s <= i && i < *e {
                st = st.plus(*sp);
            }
        }
        st
    }

    /// The text as one line of segments (one per run of equal style).
    pub fn segments(&self) -> Line {
        let mut out: Line = Vec::new();
        for (i, c) in self.plain.chars().enumerate() {
            let st = self.style_at(i);
            match out.last_mut() {
                Some(seg) if seg.style == st => seg.text.push(c),
                _ => out.push(Seg {
                    text: c.to_string(),
                    style: st,
                }),
            }
        }
        out
    }

    fn slice(&self, start: usize, end: usize) -> Text {
        let plain: String = self.plain.chars().skip(start).take(end - start).collect();
        let spans = self
            .spans
            .iter()
            .filter(|(s, e, _)| *e > start && *s < end)
            .map(|(s, e, st)| ((*s).max(start) - start, (*e).min(end) - start, *st))
            .collect();
        Text {
            plain,
            spans,
            base: self.base,
        }
    }

    /// rich.Text.wrap with the default justify/overflow: word wrap each
    /// line at `width`, trailing whitespace past the width dropped, long
    /// words folded. No padding.
    pub fn wrap(&self, width: usize) -> Vec<Text> {
        self.wrap_with(width, true)
    }

    /// `fold`: a word longer than a line is folded (console text) or cropped
    /// with an ellipsis (table cells, rich's Column overflow "ellipsis").
    pub fn wrap_with(&self, width: usize, fold: bool) -> Vec<Text> {
        let mut out = Vec::new();
        let mut start = 0;
        let chars: Vec<char> = self.plain.chars().collect();
        let mut i = 0;
        loop {
            if i == chars.len() || chars[i] == '\n' {
                let line = self.slice(start, i);
                let offsets = divide_line(&line.plain, width, fold);
                let mut bounds = vec![0];
                bounds.extend(offsets);
                bounds.push(line.plain.chars().count());
                for w in bounds.windows(2) {
                    let mut piece = line.slice(w[0], w[1]);
                    piece.rstrip_end(width);
                    piece.truncate(width, fold);
                    out.push(piece);
                }
                if i == chars.len() {
                    break;
                }
                start = i + 1;
            }
            i += 1;
        }
        out
    }

    /// rich.Text.rstrip_end: drop trailing whitespace beyond `size`.
    fn rstrip_end(&mut self, size: usize) {
        let n = self.plain.chars().count();
        if n > size {
            let excess = n - size;
            let ws = self
                .plain
                .chars()
                .rev()
                .take_while(|c| c.is_whitespace())
                .count();
            let cut = ws.min(excess);
            if cut > 0 {
                *self = self.slice(0, n - cut);
            }
        }
    }

    /// rich.Text.truncate: crop to `width` cells, with an ellipsis unless
    /// folding.
    fn truncate(&mut self, width: usize, fold: bool) {
        if cell_len(&self.plain) > width {
            let cropped = if fold || width == 0 {
                set_cell_size(&self.plain, width)
            } else {
                format!("{}\u{2026}", set_cell_size(&self.plain, width - 1))
            };
            let n = cropped.chars().count();
            let mut t = self.slice(0, n.min(self.plain.chars().count()));
            t.plain = cropped;
            *self = t;
        }
    }
}

/// End index of the tag starting at chars[i] == '[', if it is one.
fn tag_at(chars: &[char], i: usize) -> Option<usize> {
    if chars.get(i) != Some(&'[') {
        return None;
    }
    let first = *chars.get(i + 1)?;
    if !(first.is_ascii_lowercase() || first == '#' || first == '/' || first == '@') {
        return None;
    }
    let mut j = i + 1;
    while j < chars.len() {
        if chars[j] == '[' {
            return None;
        }
        if chars[j] == ']' {
            return Some(j);
        }
        j += 1;
    }
    None
}

/// rich._wrap.divide_line: the character offsets to break `text` at so
/// every piece fits in `width` cells; words longer than a line are folded.
pub fn divide_line(text: &str, width: usize, fold: bool) -> Vec<usize> {
    let chars: Vec<char> = text.chars().collect();
    let mut breaks = Vec::new();
    let mut cell_offset = 0usize;
    let mut pos = 0usize;
    while pos < chars.len() {
        // r"\s*\S+\s*" from pos
        let mut j = pos;
        while j < chars.len() && chars[j].is_whitespace() {
            j += 1;
        }
        if j == chars.len() {
            break;
        }
        while j < chars.len() && !chars[j].is_whitespace() {
            j += 1;
        }
        while j < chars.len() && chars[j].is_whitespace() {
            j += 1;
        }
        let start = pos;
        let word: String = chars[pos..j].iter().collect();
        pos = j;
        let word_length = cell_len(word.trim_end());
        let remaining = width.saturating_sub(cell_offset);
        if remaining >= word_length {
            cell_offset += cell_len(&word);
        } else if word_length > width {
            if !fold {
                if start > 0 {
                    breaks.push(start);
                }
                cell_offset = cell_len(&word);
                continue;
            }
            let folded = chop_cells(&word, width);
            let mut start = start;
            let n = folded.len();
            for (k, line) in folded.iter().enumerate() {
                if start > 0 {
                    breaks.push(start);
                }
                if k + 1 == n {
                    cell_offset = cell_len(line);
                } else {
                    start += line.chars().count();
                }
            }
        } else if cell_offset > 0 && start > 0 {
            breaks.push(start);
            cell_offset = cell_len(&word);
        }
    }
    breaks
}

/// The output sink: lines go to stdout (or a capture buffer), plain or with
/// SGR codes. `width` is rich's console width: the terminal's columns less
/// eight (kg_render.animation_console), never under forty.
pub struct Console {
    pub width: usize,
    pub color: bool,
    captured: RefCell<Option<Vec<Line>>>,
}

pub fn terminal_columns() -> usize {
    if let Ok(v) = std::env::var("COLUMNS") {
        if let Ok(n) = v.trim().parse::<usize>() {
            if n > 0 {
                return n;
            }
        }
    }
    unsafe {
        let mut ws: libc::winsize = std::mem::zeroed();
        if libc::ioctl(libc::STDOUT_FILENO, libc::TIOCGWINSZ, &mut ws) == 0 && ws.ws_col > 0 {
            return ws.ws_col as usize;
        }
    }
    80
}

pub fn stdout_is_tty() -> bool {
    unsafe { libc::isatty(libc::STDOUT_FILENO) == 1 }
}

impl Console {
    pub fn new() -> Console {
        let no_color = std::env::var("NO_COLOR").is_ok_and(|v| !v.is_empty())
            || std::env::var("TERM").is_ok_and(|v| v == "dumb");
        Console {
            width: terminal_columns().saturating_sub(8).max(40),
            color: stdout_is_tty() && !no_color,
            captured: RefCell::new(None),
        }
    }

    /// rich's plain Console(): the terminal width (COLUMNS, else the tty,
    /// else 80), colour when stdout is a tty. kg_next narrows by 8; the
    /// other reports print at the full width as their Python did.
    pub fn full_width() -> Console {
        Console {
            width: terminal_columns(),
            ..Console::new()
        }
    }

    /// Start capturing: printed lines are kept instead of written.
    pub fn begin_capture(&self) {
        *self.captured.borrow_mut() = Some(Vec::new());
    }

    pub fn end_capture(&self) -> Vec<Line> {
        self.captured.borrow_mut().take().unwrap_or_default()
    }

    pub fn print_lines(&self, lines: Vec<Line>) {
        let mut cap = self.captured.borrow_mut();
        if let Some(buf) = cap.as_mut() {
            buf.extend(lines);
            return;
        }
        let mut out = std::io::stdout().lock();
        for line in &lines {
            let _ = out.write_all(self.render_line(line).as_bytes());
            let _ = out.write_all(b"\n");
        }
        let _ = out.flush();
    }

    pub fn render_line(&self, line: &Line) -> String {
        let mut s = String::new();
        for seg in line {
            if self.color && !seg.style.is_plain() {
                s.push_str(&format!("\x1b[{}m{}\x1b[0m", seg.style.sgr(), seg.text));
            } else {
                s.push_str(&seg.text);
            }
        }
        s
    }

    /// console.print(markup): parse, wrap at the console width, write.
    pub fn print(&self, markup: &str) {
        let text = Text::from_markup(markup);
        self.print_text(&text, self.width);
    }

    pub fn print_text(&self, text: &Text, width: usize) {
        let lines: Vec<Line> = text.wrap(width).iter().map(Text::segments).collect();
        self.print_lines(lines);
    }

    /// console.print() with nothing: one blank line.
    pub fn blank(&self) {
        self.print_lines(vec![vec![]]);
    }

    /// Write raw bytes straight to stdout (the inline-image escape).
    pub fn raw(&self, s: &str) {
        let mut out = std::io::stdout().lock();
        let _ = out.write_all(s.as_bytes());
        let _ = out.flush();
    }
}

impl Default for Console {
    fn default() -> Self {
        Console::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn markup_spans() {
        let t = Text::from_markup("a [dim]b [bold]c[/bold][/dim] d");
        assert_eq!(t.plain, "a b c d");
        assert_eq!(t.spans.len(), 2);
    }

    #[test]
    fn wrap_breaks_on_words() {
        let t = Text::plain("one two three four");
        let lines: Vec<String> = t.wrap(9).iter().map(|l| l.plain.clone()).collect();
        // rich keeps a line's trailing space inside the width
        assert_eq!(lines, vec!["one two ", "three ", "four"]);
    }

    #[test]
    fn literal_brackets_stay() {
        let t = Text::from_markup("x [Hard] y [1] z");
        assert_eq!(t.plain, "x [Hard] y [1] z");
    }
}
