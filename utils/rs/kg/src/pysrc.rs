// What the tooling reads out of a Python solve file without a Python
// parser: the module docstring (ast.get_docstring, inspect.cleandoc) and
// the candidate's notes below its `---` rule (history_builder.parse_content).

/// inspect.cleandoc: tabs expanded, the common indentation of the lines
/// after the first removed, leading and trailing blank lines dropped.
pub fn cleandoc(doc: &str) -> String {
    // str.expandtabs(): a tab advances to the next multiple of eight columns
    let mut expanded = String::new();
    let mut col = 0;
    for c in doc.chars() {
        match c {
            '\t' => {
                let n = 8 - col % 8;
                expanded.extend(std::iter::repeat_n(' ', n));
                col += n;
            }
            '\n' => {
                expanded.push('\n');
                col = 0;
            }
            c => {
                expanded.push(c);
                col += 1;
            }
        }
    }
    let mut lines: Vec<String> = expanded.split('\n').map(String::from).collect();
    let margin = lines
        .iter()
        .skip(1)
        .filter(|l| !l.trim().is_empty())
        .map(|l| l.len() - l.trim_start().len())
        .min()
        .unwrap_or(usize::MAX);
    if let Some(first) = lines.first_mut() {
        *first = first.trim_start().to_string();
    }
    if margin != usize::MAX {
        for l in lines.iter_mut().skip(1) {
            *l = l
                .chars()
                .skip(margin.min(l.len() - l.trim_start().len()))
                .collect();
        }
    }
    while lines.first().is_some_and(|l| l.trim().is_empty()) {
        lines.remove(0);
    }
    while lines.last().is_some_and(|l| l.trim().is_empty()) {
        lines.pop();
    }
    lines.join("\n")
}

/// The escapes of a non-raw Python string literal.
fn unescape(body: &str) -> String {
    let chars: Vec<char> = body.chars().collect();
    let mut out = String::new();
    let mut i = 0;
    while i < chars.len() {
        let c = chars[i];
        if c != '\\' || i + 1 >= chars.len() {
            out.push(c);
            i += 1;
            continue;
        }
        let n = chars[i + 1];
        i += 2;
        match n {
            '\n' => {}
            '\\' => out.push('\\'),
            '\'' => out.push('\''),
            '"' => out.push('"'),
            'a' => out.push('\u{7}'),
            'b' => out.push('\u{8}'),
            'f' => out.push('\u{c}'),
            'n' => out.push('\n'),
            'r' => out.push('\r'),
            't' => out.push('\t'),
            'v' => out.push('\u{b}'),
            '0'..='7' => {
                let mut v = n.to_digit(8).unwrap();
                let mut k = 0;
                while k < 2 && i < chars.len() && chars[i].is_digit(8) {
                    v = v * 8 + chars[i].to_digit(8).unwrap();
                    i += 1;
                    k += 1;
                }
                out.push(char::from_u32(v).unwrap_or('?'));
            }
            'x' | 'u' | 'U' => {
                let len = match n {
                    'x' => 2,
                    'u' => 4,
                    _ => 8,
                };
                let hex: String = chars[i..(i + len).min(chars.len())].iter().collect();
                match u32::from_str_radix(&hex, 16).ok().and_then(char::from_u32) {
                    Some(ch) if hex.len() == len => {
                        out.push(ch);
                        i += len;
                    }
                    _ => {
                        out.push('\\');
                        out.push(n);
                    }
                }
            }
            other => {
                out.push('\\');
                out.push(other);
            }
        }
    }
    out
}

/// ast.get_docstring(ast.parse(code)): the first statement when it is a
/// string literal (comments and blank lines before it allowed), cleaned.
pub fn module_docstring(code: &str) -> Option<String> {
    let mut rest = code;
    loop {
        let line_end = rest.find('\n').unwrap_or(rest.len());
        let line = &rest[..line_end];
        if line.trim().is_empty() || line.trim_start().starts_with('#') {
            if line_end == rest.len() {
                return None;
            }
            rest = &rest[line_end + 1..];
            continue;
        }
        break;
    }
    if rest.starts_with(' ') || rest.starts_with('\t') {
        return None; // an indented first statement is not a module docstring
    }
    let mut i = 0;
    let bytes = rest.as_bytes();
    let mut raw = false;
    while i < bytes.len()
        && i < 2
        && matches!(
            bytes[i],
            b'r' | b'R' | b'u' | b'U' | b'b' | b'B' | b'f' | b'F'
        )
    {
        if matches!(bytes[i], b'r' | b'R') {
            raw = true;
        }
        i += 1;
    }
    let quote = match bytes.get(i) {
        Some(b'"') => '"',
        Some(b'\'') => '\'',
        _ => return None,
    };
    let after = &rest[i..];
    let delim: &str = if after.starts_with(&quote.to_string().repeat(3)) {
        if quote == '"' {
            "\"\"\""
        } else {
            "'''"
        }
    } else if quote == '"' {
        "\""
    } else {
        "'"
    };
    let body_start = delim.len();
    // find the closing delimiter, skipping escapes in a non-raw literal
    let s = &after[body_start..];
    let mut j = 0;
    let end = loop {
        if j >= s.len() {
            return None;
        }
        let c = s[j..].chars().next().unwrap();
        if !raw && c == '\\' {
            // the escape and the character it escapes
            j += 1;
            j += s[j..].chars().next().map(char::len_utf8).unwrap_or(0);
            continue;
        }
        if s[j..].starts_with(delim) {
            break j;
        }
        if delim.len() == 1 && c == '\n' {
            return None;
        }
        j += c.len_utf8();
    };
    let body = &s[..end];
    // the statement must end there (a comment or whitespace may follow)
    let tail = &s[end + delim.len()..];
    let tail_line = tail.split('\n').next().unwrap_or("").trim();
    if !(tail_line.is_empty() || tail_line.starts_with('#') || tail_line == ";") {
        return None;
    }
    let text = if raw {
        body.to_string()
    } else {
        unescape(body)
    };
    Some(cleandoc(&text))
}

/// history_builder.parse_content's notes: what follows the first `---` in
/// the module docstring, prefixed "notes: \n\n"; "" when there is none.
pub fn notes_of(code: &str) -> String {
    match module_docstring(code) {
        Some(doc) if doc.contains("---") => {
            let (_, part) = doc.split_once("---").unwrap();
            format!("notes: \n\n{}", part.trim())
        }
        _ => String::new(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn docstrings() {
        assert_eq!(
            module_docstring("\"\"\"\n1. Two Sum\n\n---\nPeeked.\n\"\"\"\nx = 1\n"),
            Some("1. Two Sum\n\n---\nPeeked.".into())
        );
        assert_eq!(
            module_docstring("# a comment\n\n'''hi'''\n"),
            Some("hi".into())
        );
        assert_eq!(
            module_docstring("x = 1\n\"\"\"not a docstring\"\"\"\n"),
            None
        );
        assert_eq!(
            module_docstring("\"\"\"a \\\"quoted\\\" word\\n\"\"\"\n"),
            Some("a \"quoted\" word".into())
        );
        assert_eq!(
            module_docstring("r\"\"\"raw \\n stays\"\"\"\n"),
            Some("raw \\n stays".into())
        );
        assert_eq!(
            module_docstring("\"\"\"\n    indented\n      more\n    \"\"\"\n"),
            Some("indented\n  more".into())
        );
        assert_eq!(
            notes_of("\"\"\"\n1. X\n\n---\n  Gave up.\n\"\"\"\n"),
            "notes: \n\n Gave up.".replace(" G", "G")
        );
        assert_eq!(notes_of("\"\"\"\n1. X\n\"\"\"\n"), "");
        assert_eq!(
            cleandoc("  first\n    second\n      third\n"),
            "first\nsecond\n  third"
        );
    }
}
