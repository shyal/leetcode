// Terminal cell widths, mirrored from rich.cells (the CELL_WIDTHS table is
// rich's own, generated from rich._cell_widths by utils/tests/test_next_parity.py's
// fixture check): an emoji is two cells, a combining mark is none. The
// tables and panels `make next` prints are laid out on these numbers, so
// the Rust output pads exactly where the Python (rich) output pads.

use crate::cell_widths::CELL_WIDTHS;

pub fn char_cells(c: char) -> usize {
    let cp = c as u32;
    // rich's fast path: these ranges are all single-cell
    if (0x20..=0x7E).contains(&cp)
        || (0xA0..=0xAC).contains(&cp)
        || (0xAE..=0x2FF).contains(&cp)
        || (0x370..=0x482).contains(&cp)
        || (0x2500..=0x25FC).contains(&cp)
        || (0x2800..=0x28FF).contains(&cp)
    {
        return 1;
    }
    let (mut lo, mut hi) = (0usize, CELL_WIDTHS.len() - 1);
    let mut i = (lo + hi) / 2;
    loop {
        let (start, end, width) = CELL_WIDTHS[i];
        if cp < start {
            if i == 0 {
                break;
            }
            hi = i - 1;
        } else if cp > end {
            lo = i + 1;
        } else {
            return if width == -1 { 0 } else { width as usize };
        }
        if hi < lo {
            break;
        }
        i = (lo + hi) / 2;
    }
    1
}

pub fn cell_len(s: &str) -> usize {
    s.chars().map(char_cells).sum()
}

/// rich.cells.set_cell_size: pad with spaces or crop to exactly `total` cells.
pub fn set_cell_size(text: &str, total: usize) -> String {
    let size = cell_len(text);
    if size == total {
        return text.to_string();
    }
    if size < total {
        return format!("{text}{}", " ".repeat(total - size));
    }
    // crop, never splitting a double-width character
    let mut out = String::new();
    let mut w = 0;
    for c in text.chars() {
        let cw = char_cells(c);
        if w + cw > total {
            break;
        }
        out.push(c);
        w += cw;
    }
    if w < total {
        out.push_str(&" ".repeat(total - w));
    }
    out
}

/// rich.cells.chop_cells: split so every piece fits in `width` cells.
pub fn chop_cells(text: &str, width: usize) -> Vec<String> {
    let mut lines: Vec<String> = vec![String::new()];
    let mut total = 0;
    for c in text.chars() {
        let cw = char_cells(c);
        if total + cw > width {
            lines.push(c.to_string());
            total = cw;
        } else {
            lines.last_mut().unwrap().push(c);
            total += cw;
        }
    }
    lines
}
