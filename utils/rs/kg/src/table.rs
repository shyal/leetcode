// rich.Table, rich.Panel and rich.Columns, as far as `make next` uses them:
// fit-to-content tables with the ROUNDED or SIMPLE_HEAD box, cells padded
// (0, 1), a bold header, alternate rows shaded; a panel sized to its body
// with a title on the top border and a subtitle on the bottom one; and
// two tables side by side when they fit in the console width, stacked
// otherwise. kg_status and kg_dependents add the box-less shape: no
// border, padding (0, 2), an optional header, right-justified and styled
// columns. Widths and padding follow rich's algorithms line for line so
// the Python and Rust printouts agree cell for cell.

use crate::cells::cell_len;
use crate::console::{adjust_line, set_shape, Console, Line, Seg, Style, Text};

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum BoxKind {
    Rounded,
    SimpleHead,
    /// rich `box=None`: no border lines, no dividers
    None,
    /// rich's default table box
    HeavyHead,
}

#[derive(Clone, Copy, PartialEq, Eq, Default)]
pub enum Justify {
    #[default]
    Left,
    Right,
    Center,
}

/// rich.Column as far as it is used: justify, a style for every cell,
/// no_wrap (the column never shrinks below its content).
#[derive(Clone, Copy, Default)]
pub struct Column {
    pub justify: Justify,
    pub style: Style,
    pub no_wrap: bool,
}

struct BoxChars {
    top_left: char,
    top: char,
    top_divider: char,
    top_right: char,
    head_left: char,
    head_vertical: char,
    head_right: char,
    head_row_left: char,
    head_row_horizontal: char,
    head_row_cross: char,
    head_row_right: char,
    mid_left: char,
    mid_vertical: char,
    mid_right: char,
    foot_left: char,
    foot_vertical: char,
    foot_right: char,
    bottom_left: char,
    bottom: char,
    bottom_divider: char,
    bottom_right: char,
}

fn box_chars(kind: BoxKind) -> BoxChars {
    // rich.box: eight lines of four characters each
    let src = match kind {
        BoxKind::Rounded => "╭─┬╮\n│ ││\n├─┼┤\n│ ││\n├─┼┤\n├─┼┤\n│ ││\n╰─┴╯",
        BoxKind::SimpleHead => "    \n    \n ── \n    \n    \n    \n    \n    ",
        BoxKind::None => "    \n    \n    \n    \n    \n    \n    \n    ",
        BoxKind::HeavyHead => "┏━┳┓\n┃ ┃┃\n┡━╇┩\n│ ││\n├─┼┤\n├─┼┤\n│ ││\n└─┴┘",
    };
    let l: Vec<Vec<char>> = src.lines().map(|s| s.chars().collect()).collect();
    BoxChars {
        top_left: l[0][0],
        top: l[0][1],
        top_divider: l[0][2],
        top_right: l[0][3],
        head_left: l[1][0],
        head_vertical: l[1][2],
        head_right: l[1][3],
        head_row_left: l[2][0],
        head_row_horizontal: l[2][1],
        head_row_cross: l[2][2],
        head_row_right: l[2][3],
        mid_left: l[3][0],
        mid_vertical: l[3][2],
        mid_right: l[3][3],
        foot_left: l[6][0],
        foot_vertical: l[6][2],
        foot_right: l[6][3],
        bottom_left: l[7][0],
        bottom: l[7][1],
        bottom_divider: l[7][2],
        bottom_right: l[7][3],
    }
}

fn joined(left: char, fill: char, cross: char, right: char, widths: &[usize]) -> String {
    let mut s = String::new();
    s.push(left);
    for (i, w) in widths.iter().enumerate() {
        s.push_str(&fill.to_string().repeat(*w));
        if i + 1 < widths.len() {
            s.push(cross);
        }
    }
    s.push(right);
    s
}

/// Python's round(): half to even.
pub fn py_round(x: f64) -> f64 {
    x.round_ties_even()
}

/// rich._ratio.ratio_reduce.
fn ratio_reduce(total: i64, ratios: &[i64], maximums: &[i64], values: &[i64]) -> Vec<i64> {
    let ratios: Vec<i64> = ratios
        .iter()
        .zip(maximums)
        .map(|(r, m)| if *m != 0 { *r } else { 0 })
        .collect();
    let mut total_ratio: i64 = ratios.iter().sum();
    if total_ratio == 0 {
        return values.to_vec();
    }
    let mut remaining = total;
    let mut out = Vec::new();
    for ((ratio, maximum), value) in ratios.iter().zip(maximums).zip(values) {
        if *ratio != 0 && total_ratio > 0 {
            let d = py_round(*ratio as f64 * remaining as f64 / total_ratio as f64) as i64;
            let distributed = (*maximum).min(d);
            out.push(value - distributed);
            remaining -= distributed;
            total_ratio -= ratio;
        } else {
            out.push(*value);
        }
    }
    out
}

/// rich.Table._collapse_widths.
fn collapse_widths(widths: &[i64], max_width: i64, wrapable: &[bool]) -> Vec<i64> {
    let mut widths = widths.to_vec();
    let mut total: i64 = widths.iter().sum();
    let mut excess = total - max_width;
    if !wrapable.iter().any(|w| *w) {
        return widths;
    }
    while total != 0 && excess > 0 {
        let max_column = widths
            .iter()
            .zip(wrapable)
            .filter(|(_, w)| **w)
            .map(|(c, _)| *c)
            .max()
            .unwrap();
        let second = widths
            .iter()
            .zip(wrapable)
            .map(|(c, w)| if *w && *c != max_column { *c } else { 0 })
            .max()
            .unwrap();
        let diff = max_column - second;
        let ratios: Vec<i64> = widths
            .iter()
            .zip(wrapable)
            .map(|(c, w)| if *w && *c == max_column { 1 } else { 0 })
            .collect();
        if ratios.iter().all(|r| *r == 0) || diff == 0 {
            break;
        }
        let max_reduce = vec![excess.min(diff); widths.len()];
        widths = ratio_reduce(excess, &ratios, &max_reduce, &widths);
        total = widths.iter().sum();
        excess = total - max_width;
    }
    widths
}

pub struct Table {
    pub columns: Vec<String>,
    pub rows: Vec<Vec<String>>,
    pub title: Option<String>,
    pub kind: BoxKind,
    pub row_shade: bool,
    pub show_header: bool,
    /// rich padding (0, pad): spaces on each side of every cell
    pub pad: usize,
    pub title_style: Style,
    pub title_justify: Justify,
    pub header_style: Style,
    pub border_style: Style,
    pub column_opts: Vec<Column>,
}

impl Table {
    /// kg_next.plain_table: rounded dim border, bold headers, alternate
    /// rows shaded.
    pub fn plain(columns: &[&str], title: Option<&str>, kind: BoxKind) -> Table {
        Table {
            columns: columns.iter().map(|c| c.to_string()).collect(),
            rows: vec![],
            title: title.map(|t| t.to_string()),
            kind,
            row_shade: true,
            show_header: true,
            pad: 1,
            title_style: Style::parse("bold"),
            title_justify: Justify::Left,
            header_style: Style::parse("bold"),
            border_style: Style::parse("dim"),
            column_opts: vec![Column::default(); columns.len()],
        }
    }

    /// rich Table(title=...) with every default: the heavy-head box in a
    /// plain style, a bold header, an italic centred title, padding (0, 1).
    pub fn rich_default(columns: &[&str], title: Option<&str>) -> Table {
        Table {
            row_shade: false,
            title_style: Style::parse("italic"),
            title_justify: Justify::Center,
            border_style: Style::default(),
            ..Table::plain(columns, title, BoxKind::HeavyHead)
        }
    }

    /// rich Table(box=None, padding=(0, pad)) with rich's defaults
    /// otherwise: no row shading, a bold header when shown, a centred title.
    pub fn bare(columns: &[&str], show_header: bool, pad: usize) -> Table {
        Table {
            kind: BoxKind::None,
            row_shade: false,
            show_header,
            pad,
            title_justify: Justify::Center,
            title_style: Style::default(),
            ..Table::plain(columns, None, BoxKind::None)
        }
    }

    pub fn column(&mut self, i: usize, opts: Column) {
        self.column_opts[i] = opts;
    }

    pub fn add_row(&mut self, cells: &[String]) {
        self.rows.push(cells.to_vec());
    }

    fn extra_width(&self) -> usize {
        // rich Table._extra_width: the edges and the dividers, box only
        if self.kind == BoxKind::None {
            0
        } else {
            2 + self.columns.len() - 1
        }
    }

    /// Every cell of a column, header first, as rich Text.
    fn column_cells(&self, i: usize) -> Vec<Text> {
        let mut out = Vec::new();
        if self.show_header {
            out.push(Text::from_markup(&self.columns[i]));
        }
        for row in &self.rows {
            out.push(Text::from_markup(
                row.get(i).map(String::as_str).unwrap_or(""),
            ));
        }
        out
    }

    fn measure_cell(text: &Text, max_width: usize, pad: usize, no_wrap: bool) -> (usize, usize) {
        // Padding(text, (0,pad)) measured: the text's min/max plus 2*pad
        let lines: Vec<&str> = text.plain.split('\n').collect();
        let max = lines.iter().map(|l| cell_len(l)).max().unwrap_or(0);
        let words: Vec<&str> = text.plain.split_whitespace().collect();
        let min = if no_wrap || words.is_empty() {
            max
        } else {
            words.iter().map(|w| cell_len(w)).max().unwrap()
        };
        (
            (min + 2 * pad).min(max_width),
            (max + 2 * pad).min(max_width),
        )
    }

    /// rich.Table._calculate_column_widths for a non-expanding table.
    fn column_widths(&self, max_width: usize) -> Vec<usize> {
        let ncol = self.columns.len();
        let mut widths: Vec<i64> = (0..ncol)
            .map(|i| {
                let cells = self.column_cells(i);
                cells
                    .iter()
                    .map(|c| {
                        Table::measure_cell(c, max_width, self.pad, self.column_opts[i].no_wrap).1
                    })
                    .max()
                    .unwrap_or(1)
                    .max(1) as i64
            })
            .collect();
        let table_width: i64 = widths.iter().sum();
        if table_width > max_width as i64 {
            // rich: no_wrap columns keep their width; the others collapse
            let wrapable: Vec<bool> = self.column_opts.iter().map(|c| !c.no_wrap).collect();
            widths = collapse_widths(&widths, max_width as i64, &wrapable);
            let table_width: i64 = widths.iter().sum();
            if table_width > max_width as i64 {
                let excess = table_width - max_width as i64;
                let ones = vec![1; widths.len()];
                widths = ratio_reduce(excess, &ones, &widths, &widths);
            }
            widths = (0..ncol)
                .map(|i| {
                    let w = widths[i].max(0) as usize;
                    self.column_cells(i)
                        .iter()
                        .map(|c| Table::measure_cell(c, w, self.pad, self.column_opts[i].no_wrap).1)
                        .max()
                        .unwrap_or(0) as i64
                })
                .collect();
        }
        widths.iter().map(|w| (*w).max(0) as usize).collect()
    }

    /// The table's width in cells at this console width (rich's Measurement
    /// maximum, the title left out as rich leaves it out).
    pub fn measure(&self, max_width: usize) -> usize {
        let extra = self.extra_width();
        let inner = max_width.saturating_sub(extra);
        self.column_widths(inner).iter().sum::<usize>() + extra
    }

    /// One padded cell rendered at `width`: " " + text lines + " ".
    fn render_cell(
        text: &Text,
        width: usize,
        style: Style,
        pad: usize,
        justify: Justify,
    ) -> Vec<Line> {
        let inner = width.saturating_sub(2 * pad);
        let mut lines: Vec<Line> = Vec::new();
        for t in text.wrap_with(inner, false) {
            let mut t = t;
            t.base = style;
            let mut line = vec![Seg {
                text: " ".repeat(pad),
                style,
            }];
            let segs = t.segments();
            let gap = inner.saturating_sub(crate::console::line_len(&segs));
            let (left, right) = match justify {
                Justify::Left => (0, gap),
                Justify::Right => (gap, 0),
                Justify::Center => (gap / 2, gap - gap / 2),
            };
            if left > 0 {
                line.push(Seg {
                    text: " ".repeat(left),
                    style,
                });
            }
            line.extend(adjust_line(&segs, inner - left, style));
            let _ = right;
            line.push(Seg {
                text: " ".repeat(pad),
                style,
            });
            lines.push(line);
        }
        if lines.is_empty() {
            lines.push(vec![Seg {
                text: " ".repeat(width),
                style,
            }]);
        }
        lines
    }

    pub fn render(&self, max_width: usize) -> Vec<Line> {
        let bx = box_chars(self.kind);
        let border = self.border_style;
        let extra = self.extra_width();
        let widths = self.column_widths(max_width.saturating_sub(extra));
        let table_width: usize = widths.iter().sum::<usize>() + extra;
        let mut out: Vec<Line> = Vec::new();
        let boxed = self.kind != BoxKind::None;
        if let Some(title) = &self.title {
            let mut t = Text::from_markup(title);
            t.base = self.title_style;
            for line in t.wrap(table_width) {
                let segs = line.segments();
                let gap = table_width.saturating_sub(crate::console::line_len(&segs));
                let left = match self.title_justify {
                    Justify::Left => 0,
                    Justify::Right => gap,
                    Justify::Center => gap / 2,
                };
                let mut l: Line = Vec::new();
                if left > 0 {
                    l.push(Seg {
                        text: " ".repeat(left),
                        style: Style::default(),
                    });
                }
                l.extend(segs);
                out.push(adjust_line(&l, table_width, Style::default()));
            }
        }
        if boxed {
            out.push(vec![Seg {
                text: joined(bx.top_left, bx.top, bx.top_divider, bx.top_right, &widths),
                style: border,
            }]);
        }
        let header_rows = usize::from(self.show_header);
        let nrows = self.rows.len() + header_rows;
        for r in 0..nrows {
            let first = self.show_header && r == 0;
            let last = r + 1 == nrows;
            let data_index = r - header_rows; // valid when !first
            let row_style = if first || !self.row_shade || data_index % 2 == 0 {
                Style::default()
            } else {
                Style::parse("on grey15")
            };
            let cell_style = if first {
                self.header_style
            } else {
                Style::default()
            };
            let cells: Vec<Vec<Line>> = (0..self.columns.len())
                .map(|c| {
                    let text = if first {
                        Text::from_markup(&self.columns[c])
                    } else {
                        Text::from_markup(
                            self.rows[data_index]
                                .get(c)
                                .map(String::as_str)
                                .unwrap_or(""),
                        )
                    };
                    let opts = self.column_opts[c];
                    Table::render_cell(
                        &text,
                        widths[c],
                        cell_style.plus(row_style).plus(opts.style),
                        self.pad,
                        opts.justify,
                    )
                })
                .collect();
            let height = cells.iter().map(Vec::len).max().unwrap_or(1).max(1);
            let shaped: Vec<Vec<Line>> = cells
                .iter()
                .zip(&widths)
                .map(|(lines, w)| {
                    // header cells align bottom, data cells top
                    let mut lines = lines.clone();
                    if first {
                        while lines.len() < height {
                            lines.insert(
                                0,
                                vec![Seg {
                                    text: " ".repeat(*w),
                                    style: row_style,
                                }],
                            );
                        }
                    }
                    set_shape(&lines, *w, height, cell_style.plus(row_style))
                })
                .collect();
            let (left, vertical, right) = if first {
                (bx.head_left, bx.head_vertical, bx.head_right)
            } else if last {
                (bx.foot_left, bx.foot_vertical, bx.foot_right)
            } else {
                (bx.mid_left, bx.mid_vertical, bx.mid_right)
            };
            let divider_style = if vertical == ' ' {
                Style {
                    bg: row_style.bg,
                    ..border
                }
            } else {
                border
            };
            for line_no in 0..height {
                let mut line: Line = Vec::new();
                if boxed {
                    line.push(Seg {
                        text: left.to_string(),
                        style: border,
                    });
                }
                for (ci, cell) in shaped.iter().enumerate() {
                    line.extend(cell[line_no].clone());
                    if boxed && ci + 1 < shaped.len() {
                        line.push(Seg {
                            text: vertical.to_string(),
                            style: divider_style,
                        });
                    }
                }
                if boxed {
                    line.push(Seg {
                        text: right.to_string(),
                        style: border,
                    });
                }
                out.push(line);
            }
            if first && boxed {
                out.push(vec![Seg {
                    text: joined(
                        bx.head_row_left,
                        bx.head_row_horizontal,
                        bx.head_row_cross,
                        bx.head_row_right,
                        &widths,
                    ),
                    style: border,
                }]);
            }
        }
        if boxed {
            out.push(vec![Seg {
                text: joined(
                    bx.bottom_left,
                    bx.bottom,
                    bx.bottom_divider,
                    bx.bottom_right,
                    &widths,
                ),
                style: border,
            }]);
        }
        out
    }
}

/// kg_next.pick_panel: the body framed, title on the top border, subtitle
/// on the bottom one, dim rounded border, padding (0, 1), sized to fit.
pub fn panel(body: &[Line], title: &str, subtitle: Option<&str>, max_width: usize) -> Vec<Line> {
    let border = Style::parse("dim");
    let mut title_text = Text::from_markup(title);
    title_text.plain = format!(" {} ", title_text.plain.replace('\n', " "));
    title_text.spans = title_text
        .spans
        .iter()
        .map(|(s, e, st)| (s + 1, e + 1, *st))
        .collect();
    title_text.base = border;
    let body_width = body.iter().map(crate::console::line_len).max().unwrap_or(0);
    let mut child_width = (body_width + 2).min(max_width.saturating_sub(2));
    child_width = child_width.max(title_text.cell_len() + 2);
    child_width = child_width.min(max_width.saturating_sub(2));
    let width = child_width + 2;
    let mut out: Vec<Line> = Vec::new();
    let fill = |text: &Text, left: char, fill: char, right: char| -> Line {
        let mut t = text.clone();
        let inner = width - 4;
        if t.cell_len() > inner {
            t.plain = crate::cells::set_cell_size(&t.plain, inner);
        }
        let excess = inner - t.cell_len();
        let mut line: Line = vec![Seg {
            text: format!("{left}{fill}"),
            style: border,
        }];
        line.extend(t.segments());
        line.push(Seg {
            text: format!("{}{fill}{right}", fill.to_string().repeat(excess)),
            style: border,
        });
        line
    };
    out.push(fill(&title_text, '╭', '─', '╮'));
    // the body, padded (0, 1), each line re-wrapped at the child width
    for line in body {
        let mut text = Text::plain(&crate::console::line_plain(line));
        // keep the styles: rebuild spans from the segments
        let mut pos = 0;
        for seg in line {
            let n = seg.text.chars().count();
            if !seg.style.is_plain() {
                text.spans.push((pos, pos + n, seg.style));
            }
            pos += n;
        }
        for piece in text.wrap(child_width - 2) {
            let mut l: Line = vec![Seg {
                text: "│ ".into(),
                style: border,
            }];
            l.extend(adjust_line(
                &piece.segments(),
                child_width - 2,
                Style::default(),
            ));
            l.push(Seg {
                text: " │".into(),
                style: border,
            });
            out.push(l);
        }
    }
    match subtitle {
        Some(sub) => {
            let mut st = Text::from_markup(sub);
            st.plain = format!(" {} ", st.plain.replace('\n', " "));
            st.spans = st
                .spans
                .iter()
                .map(|(s, e, x)| (s + 1, e + 1, *x))
                .collect();
            st.base = border;
            out.push(fill(&st, '╰', '─', '╯'));
        }
        None => out.push(vec![Seg {
            text: format!("╰{}╯", "─".repeat(width - 2)),
            style: border,
        }]),
    }
    out
}

/// rich.Columns(tables, padding=(0, 2)): side by side when the widths plus
/// two cells between them fit in `max_width`, else one under the other.
pub fn columns(items: &[&Table], max_width: usize) -> Vec<Line> {
    let widths: Vec<usize> = items.iter().map(|t| t.measure(max_width)).collect();
    let mut count = items.len();
    while count > 1 {
        let mut col_w = vec![0usize; count];
        let mut fits = true;
        for (i, w) in widths.iter().enumerate() {
            let c = i % count;
            col_w[c] = col_w[c].max(*w);
            let used: usize = col_w.iter().filter(|w| **w > 0).count();
            let total: usize = col_w.iter().sum::<usize>() + 2 * used.saturating_sub(1);
            if total > max_width {
                count = used - 1;
                fits = false;
                break;
            }
        }
        if fits {
            break;
        }
    }
    let count = count.max(1);
    let mut col_w = vec![0usize; count];
    for (i, w) in widths.iter().enumerate() {
        col_w[i % count] = col_w[i % count].max(*w);
    }
    let mut out: Vec<Line> = Vec::new();
    for row in items.chunks(count) {
        let rendered: Vec<Vec<Line>> = row
            .iter()
            .enumerate()
            .map(|(c, t)| t.render(col_w[c]))
            .collect();
        let height = rendered.iter().map(Vec::len).max().unwrap_or(0);
        let shaped: Vec<Vec<Line>> = rendered
            .iter()
            .enumerate()
            .map(|(c, lines)| set_shape(lines, col_w[c], height, Style::default()))
            .collect();
        for line_no in 0..height {
            let mut line: Line = Vec::new();
            for (c, cell) in shaped.iter().enumerate() {
                line.extend(cell[line_no].clone());
                if c + 1 < count {
                    // the grid's collapsed padding: two cells after every
                    // column but the last
                    line.push(Seg {
                        text: "  ".into(),
                        style: Style::default(),
                    });
                }
            }
            // an odd last row still spans every column (blank cells)
            for w in col_w.iter().take(count).skip(shaped.len()) {
                line.push(Seg {
                    text: "  ".into(),
                    style: Style::default(),
                });
                line.push(Seg {
                    text: " ".repeat(*w),
                    style: Style::default(),
                });
            }
            out.push(line);
        }
    }
    out
}

/// rich Panel(body, title=..., padding=(0, 1)) with expand=True (the
/// default): the full console width, the title centred in the top rule.
pub fn panel_expanded(body: &[Line], title: &str, width: usize) -> Vec<Line> {
    panel_titled(body, title, width, false)
}

/// The same panel with title_align="left" (kg_llm_next).
pub fn panel_titled(body: &[Line], title: &str, width: usize, left: bool) -> Vec<Line> {
    let border = Style::parse("dim");
    let mut title_text = Text::from_markup(title);
    title_text.plain = format!(" {} ", title_text.plain.replace('\n', " "));
    title_text.spans = title_text
        .spans
        .iter()
        .map(|(s, e, st)| (s + 1, e + 1, *st))
        .collect();
    title_text.base = border;
    let inner = width.saturating_sub(4);
    let mut out: Vec<Line> = Vec::new();
    let mut t = title_text.clone();
    if t.cell_len() > inner {
        t.plain = crate::cells::set_cell_size(&t.plain, inner);
    }
    let excess = inner - t.cell_len();
    let (pad_l, pad_r) = if left {
        (0, excess)
    } else {
        (excess / 2, excess - excess / 2)
    };
    let mut top: Line = vec![Seg {
        text: format!("╭─{}", "─".repeat(pad_l)),
        style: border,
    }];
    top.extend(t.segments());
    top.push(Seg {
        text: format!("{}─╮", "─".repeat(pad_r)),
        style: border,
    });
    out.push(top);
    for line in body {
        let mut text = Text::plain(&crate::console::line_plain(line));
        let mut pos = 0;
        for seg in line {
            let n = seg.text.chars().count();
            if !seg.style.is_plain() {
                text.spans.push((pos, pos + n, seg.style));
            }
            pos += n;
        }
        for piece in text.wrap(inner) {
            let mut l: Line = vec![Seg {
                text: "│ ".into(),
                style: border,
            }];
            l.extend(adjust_line(&piece.segments(), inner, Style::default()));
            l.push(Seg {
                text: " │".into(),
                style: border,
            });
            out.push(l);
        }
    }
    out.push(vec![Seg {
        text: format!("╰{}╯", "─".repeat(width - 2)),
        style: border,
    }]);
    out
}

pub fn print_table(console: &Console, table: &Table) {
    console.print_lines(table.render(console.width));
}
