// pyfiglet's FIGfont renderer, as far as `make timer` and `make goals` use
// it: left-to-right, left-justified, the font's own smushing rules. The
// algorithm follows pyfiglet.FigletBuilder step for step (smushAmount,
// smushChars, the line-break markers) so the digits come out identical.

use std::collections::HashMap;

pub struct Font {
    pub height: usize,
    pub hard_blank: char,
    pub smush_mode: i32,
    pub print_direction: i32,
    chars: HashMap<u32, Vec<String>>,
    widths: HashMap<u32, usize>,
}

const SM_EQUAL: i32 = 1;
const SM_LOWLINE: i32 = 2;
const SM_HIERARCHY: i32 = 4;
const SM_PAIR: i32 = 8;
const SM_BIGX: i32 = 16;
const SM_HARDBLANK: i32 = 32;
const SM_KERN: i32 = 64;
const SM_SMUSH: i32 = 128;

impl Font {
    /// FigletFont.loadFont over the .flf text.
    pub fn parse(data: &str) -> Option<Font> {
        let data = data.replace(['\u{85}', '\u{2028}', '\u{2029}'], " ");
        let mut lines = data.lines();
        let header = lines.next()?;
        // reMagicNumber ^[tf]lf2. : five characters of signature
        if !(header.starts_with("flf2") || header.starts_with("tlf2")) {
            return None;
        }
        let rest: String = header.chars().skip(5).collect();
        let fields: Vec<&str> = rest.split_whitespace().collect();
        if fields.len() < 6 {
            return None;
        }
        let hard_blank = fields[0].chars().next()?;
        let height: usize = fields[1].parse().ok()?;
        let _base_line: i32 = fields[2].parse().ok()?;
        let _max_length: i32 = fields[3].parse().ok()?;
        let old_layout: i32 = fields[4].parse().ok()?;
        let comment_lines: usize = fields[5].parse().ok()?;
        let print_direction: i32 = fields.get(6).and_then(|s| s.parse().ok()).unwrap_or(0);
        let full_layout: Option<i32> = fields.get(7).and_then(|s| s.parse().ok());
        let smush_mode = match full_layout {
            Some(f) => f,
            None => {
                if old_layout == 0 {
                    64
                } else if old_layout < 0 {
                    0
                } else {
                    (old_layout & 31) | 128
                }
            }
        };
        let mut lines: Vec<&str> = lines.collect();
        lines.drain(0..comment_lines.min(lines.len()));
        let mut pos = 0;
        let mut chars = HashMap::new();
        let mut widths = HashMap::new();
        // one character: `height` lines, the end marker (once or twice) stripped
        let read_char = |pos: &mut usize| -> Option<(usize, Vec<String>)> {
            let mut end: Option<char> = None;
            let mut width = 0;
            let mut out = Vec::new();
            for _ in 0..height {
                let line = *lines.get(*pos)?;
                *pos += 1;
                let marker = match end {
                    Some(m) => m,
                    None => {
                        // reEndMarker (.)\s*$ : the last non-space character
                        let m = line.trim_end().chars().last().unwrap_or(' ');
                        end = Some(m);
                        m
                    }
                };
                // end{1,2}\s*$
                let mut t = line.trim_end().to_string();
                for _ in 0..2 {
                    if t.ends_with(marker) {
                        t.pop();
                    } else {
                        break;
                    }
                }
                let w = t.chars().count();
                if w > width {
                    width = w;
                }
                out.push(t);
            }
            Some((width, out))
        };
        for i in 32u32..127 {
            let (w, letter) = read_char(&mut pos)?;
            if i == 32 || letter.iter().any(|l| !l.is_empty()) {
                chars.insert(i, letter);
                widths.insert(i, w);
            }
        }
        // the umlauts and the extended set are not drawn by the timer
        Some(Font {
            height,
            hard_blank,
            smush_mode,
            print_direction,
            chars,
            widths,
        })
    }

    fn smush_chars(
        &self,
        left: Option<char>,
        right: Option<char>,
        prev_w: usize,
        cur_w: usize,
    ) -> Option<char> {
        if left == Some(' ') {
            return right;
        }
        if right == Some(' ') {
            return left;
        }
        if prev_w < 2 || cur_w < 2 {
            return None;
        }
        if self.smush_mode & SM_SMUSH == 0 {
            return None;
        }
        let (l, r) = (left?, right?);
        if self.smush_mode & 63 == 0 {
            if l == self.hard_blank {
                return Some(r);
            }
            if r == self.hard_blank {
                return Some(l);
            }
            return Some(r);
        }
        if self.smush_mode & SM_HARDBLANK != 0 && l == self.hard_blank && r == self.hard_blank {
            return Some(l);
        }
        if l == self.hard_blank || r == self.hard_blank {
            return None;
        }
        if self.smush_mode & SM_EQUAL != 0 && l == r {
            return Some(l);
        }
        let mut smushes: Vec<(&str, &str)> = Vec::new();
        if self.smush_mode & SM_LOWLINE != 0 {
            smushes.push(("_", "|/\\[]{}()<>"));
        }
        if self.smush_mode & SM_HIERARCHY != 0 {
            smushes.extend([
                ("|", "/\\[]{}()<>"),
                ("\\/", "[]{}()<>"),
                ("[]", "{}()<>"),
                ("{}", "()<>"),
                ("()", "<>"),
            ]);
        }
        for (a, b) in smushes {
            if a.contains(l) && b.contains(r) {
                return Some(r);
            }
            if a.contains(r) && b.contains(l) {
                return Some(l);
            }
        }
        if self.smush_mode & SM_PAIR != 0 {
            for pair in [format!("{l}{r}"), format!("{r}{l}")] {
                if pair == "[]" || pair == "{}" || pair == "()" {
                    return Some('|');
                }
            }
        }
        if self.smush_mode & SM_BIGX != 0 {
            if l == '/' && r == '\\' {
                return Some('|');
            }
            if r == '/' && l == '\\' {
                return Some('Y');
            }
            if l == '>' && r == '<' {
                return Some('X');
            }
        }
        None
    }

    fn smush_amount(
        &self,
        buffer: &[Vec<char>],
        cur: &[Vec<char>],
        prev_w: usize,
        cur_w: usize,
    ) -> usize {
        if self.smush_mode & (SM_SMUSH | SM_KERN) == 0 {
            return 0;
        }
        let mut max_smush = cur_w as i64;
        for row in 0..self.height {
            let left = &buffer[row];
            let right = &cur[row];
            let stripped_len = {
                let mut n = left.len();
                while n > 0 && left[n - 1] == ' ' {
                    n -= 1;
                }
                n
            };
            let mut linebd = stripped_len as i64 - 1;
            if linebd < 0 {
                linebd = 0;
            }
            let ch1 = if (linebd as usize) < left.len() {
                Some(left[linebd as usize])
            } else {
                linebd = 0;
                None
            };
            let mut charbd = 0;
            while charbd < right.len() && right[charbd] == ' ' {
                charbd += 1;
            }
            let ch2 = if charbd < right.len() {
                Some(right[charbd])
            } else {
                None
            };
            let mut amt = charbd as i64 + left.len() as i64 - 1 - linebd;
            if ch1.is_none()
                || ch1 == Some(' ')
                || (ch2.is_some() && self.smush_chars(ch1, ch2, prev_w, cur_w).is_some())
            {
                amt += 1;
            }
            if amt < max_smush {
                max_smush = amt;
            }
        }
        max_smush.max(0) as usize
    }

    /// pyfiglet.figlet_format(text, font): the lines joined with "\n", a
    /// trailing "\n", hardblanks replaced by spaces. `width` is the wrap
    /// width (pyfiglet's default 80).
    pub fn render(&self, text: &str, width: usize) -> String {
        let codes: Vec<u32> = text.chars().map(|c| c as u32).collect();
        let mut product: Vec<Vec<Vec<char>>> = Vec::new();
        let mut buffer: Vec<Vec<char>> = vec![Vec::new(); self.height];
        let mut blank_markers: Vec<(Vec<Vec<char>>, usize)> = Vec::new();
        let mut prev_w = 0usize;
        let mut i = 0;
        while i < codes.len() {
            let c = codes[i];
            if c == '\n' as u32 {
                blank_markers.push((buffer.clone(), i));
                // handleNewLine
                match blank_markers.pop() {
                    Some((saved, saved_i)) => {
                        product.push(saved);
                        i = saved_i;
                    }
                    None => {
                        product.push(buffer.clone());
                        i -= 1;
                    }
                }
                buffer = vec![Vec::new(); self.height];
                blank_markers.clear();
                prev_w = 0;
                i += 1;
                continue;
            }
            let Some(ch) = self.chars.get(&c) else {
                i += 1;
                continue;
            };
            let rows: Vec<Vec<char>> = ch.iter().map(|l| l.chars().collect()).collect();
            let cur_w = self.widths[&c];
            if width < cur_w {
                return String::new();
            }
            let max_smush = self.smush_amount(&buffer, &rows, prev_w, cur_w);
            let total = buffer[0].len() + cur_w - max_smush;
            if c == ' ' as u32 {
                blank_markers.push((buffer.clone(), i));
            }
            if total >= width {
                // handleNewLine
                match blank_markers.pop() {
                    Some((saved, saved_i)) => {
                        product.push(saved);
                        i = saved_i;
                    }
                    None => {
                        product.push(buffer.clone());
                        i -= 1;
                    }
                }
                buffer = vec![Vec::new(); self.height];
                blank_markers.clear();
            } else {
                for row in 0..self.height {
                    let mut add_left = buffer[row].clone();
                    let add_right = &rows[row];
                    for k in 0..max_smush {
                        let idx = add_left.len() as i64 - max_smush as i64 + k as i64;
                        let left = if idx >= 0 && (idx as usize) < add_left.len() {
                            Some(add_left[idx as usize])
                        } else {
                            None
                        };
                        let right = add_right.get(k).copied();
                        if let Some(s) = self.smush_chars(left, right, prev_w, cur_w) {
                            if idx >= 0 && (idx as usize) < add_left.len() {
                                add_left[idx as usize] = s;
                            }
                        } else if idx >= 0 && (idx as usize) < add_left.len() {
                            // pyfiglet writes None into the buffer; it never
                            // happens for kerned/smushed fonts on these glyphs
                        }
                    }
                    let mut line = add_left;
                    line.extend(add_right.iter().skip(max_smush));
                    buffer[row] = line;
                }
            }
            prev_w = cur_w;
            i += 1;
        }
        if !buffer[0].is_empty() {
            product.push(buffer);
        }
        let mut out = String::new();
        for buf in product {
            for row in buf {
                let s: String = row
                    .iter()
                    .map(|c| if *c == self.hard_blank { ' ' } else { *c })
                    .collect();
                out.push_str(&s);
                out.push('\n');
            }
        }
        out
    }
}

/// The three fonts the timer steps through (pyfiglet's doh, univers, big),
/// embedded so the binary needs no font directory.
pub fn builtin(name: &str) -> Option<Font> {
    let data = match name {
        "doh" => include_str!("../../timer/fonts/doh.flf"),
        "univers" => include_str!("../../timer/fonts/univers.flf"),
        "big" => include_str!("../../timer/fonts/big.flf"),
        _ => return None,
    };
    Font::parse(data)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn big_matches_pyfiglet() {
        let f = builtin("big").unwrap();
        let expected = " __    ___  _____ \n/_ |_ / _ \\| ____|\n | (_) | | | |__  \n | | | | | |___ \\ \n | |_| |_| |___) |\n |_(_)\\___/|____/ \n                  \n                  \n";
        assert_eq!(f.render("1:05", 80), expected);
    }

    #[test]
    fn fonts_load() {
        for name in ["doh", "univers", "big"] {
            let f = builtin(name).expect(name);
            assert!(f.height > 5, "{name}");
            let art = f.render("0:00", 80);
            assert_eq!(art.lines().count(), f.height, "{name}");
        }
        assert_eq!(builtin("doh").unwrap().hard_blank, '\u{7f}');
    }
}
