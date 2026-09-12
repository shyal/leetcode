// Python's json.dumps, byte for byte, over serde_json::Value: the graph/
// files are written by Python's json.dump(indent=1 or 2) and read back by
// git diff, so a Rust writer must produce the same text or every solve
// commit carries a noisy rewrite. ensure_ascii=True, separators (", ", ": ")
// when indent is None and ("," + newline, ": ") when it is not, floats in
// Python's repr. Also Python's float repr and %g on their own, for the
// reports that print numbers.

use std::fmt::Write;

use serde_json::Value;

/// repr(float): the shortest round-tripping digits, fixed notation for
/// 1e-4 <= |x| < 1e16 (always with a fractional part), exponent notation
/// otherwise with a signed two-digit exponent.
pub fn float_repr(x: f64) -> String {
    if x.is_nan() {
        return "nan".to_string();
    }
    if x.is_infinite() {
        return if x > 0.0 {
            "inf".to_string()
        } else {
            "-inf".to_string()
        };
    }
    if x == 0.0 {
        return if x.is_sign_negative() {
            "-0.0".to_string()
        } else {
            "0.0".to_string()
        };
    }
    // {:e} gives the shortest round-trip mantissa: "1.5e16", "-2e-5"
    let sci = format!("{x:e}");
    let (mant, exp) = sci.split_once('e').unwrap();
    let exp: i32 = exp.parse().unwrap();
    let neg = mant.starts_with('-');
    let digits: String = mant.chars().filter(|c| c.is_ascii_digit()).collect();
    let mut out = String::new();
    if neg {
        out.push('-');
    }
    if (-4..16).contains(&exp) {
        // fixed: digits d0.d1d2... shifted by exp
        let point = exp + 1; // digits before the decimal point
        if point <= 0 {
            out.push_str("0.");
            for _ in 0..(-point) {
                out.push('0');
            }
            out.push_str(&digits);
        } else if (point as usize) >= digits.len() {
            out.push_str(&digits);
            for _ in 0..(point as usize - digits.len()) {
                out.push('0');
            }
            out.push_str(".0");
        } else {
            out.push_str(&digits[..point as usize]);
            out.push('.');
            out.push_str(&digits[point as usize..]);
        }
    } else {
        out.push_str(&digits[..1]);
        if digits.len() > 1 {
            out.push('.');
            out.push_str(&digits[1..]);
        }
        let _ = write!(out, "e{}{:02}", if exp < 0 { '-' } else { '+' }, exp.abs());
    }
    out
}

/// Python's "%g" / format(x, "g"): six significant digits, trailing zeros
/// dropped, exponent form outside [1e-4, 1e6).
pub fn g(x: f64) -> String {
    if x == 0.0 {
        return "0".to_string();
    }
    if !x.is_finite() {
        return float_repr(x);
    }
    let exp = x.abs().log10().floor() as i32;
    // round to 6 significant digits first, as %g does, then decide the form
    let scale = 10f64.powi(5 - exp);
    let rounded = (x * scale).round_ties_even() / scale;
    let exp = if rounded == 0.0 {
        exp
    } else {
        rounded.abs().log10().floor() as i32
    };
    if (-4..6).contains(&exp) {
        let decimals = (5 - exp).max(0) as usize;
        let s = format!("{rounded:.decimals$}");
        let s = if s.contains('.') {
            s.trim_end_matches('0').trim_end_matches('.').to_string()
        } else {
            s
        };
        s
    } else {
        let mant = rounded / 10f64.powi(exp);
        let m = format!("{mant:.5}");
        let m = m.trim_end_matches('0').trim_end_matches('.');
        format!("{m}e{}{:02}", if exp < 0 { '-' } else { '+' }, exp.abs())
    }
}

fn write_str(out: &mut String, s: &str) {
    out.push('"');
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            '\u{08}' => out.push_str("\\b"),
            '\u{0c}' => out.push_str("\\f"),
            c if (c as u32) < 0x20 => {
                let _ = write!(out, "\\u{:04x}", c as u32);
            }
            c if (c as u32) > 0x7e => {
                // ensure_ascii: \uXXXX, a surrogate pair above the BMP
                let n = c as u32;
                if n > 0xffff {
                    let n = n - 0x10000;
                    let _ = write!(
                        out,
                        "\\u{:04x}\\u{:04x}",
                        0xd800 + (n >> 10),
                        0xdc00 + (n & 0x3ff)
                    );
                } else {
                    let _ = write!(out, "\\u{:04x}", n);
                }
            }
            c => out.push(c),
        }
    }
    out.push('"');
}

fn write_value(out: &mut String, v: &Value, indent: Option<usize>, level: usize) {
    match v {
        Value::Null => out.push_str("null"),
        Value::Bool(b) => out.push_str(if *b { "true" } else { "false" }),
        Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                let _ = write!(out, "{i}");
            } else if let Some(u) = n.as_u64() {
                let _ = write!(out, "{u}");
            } else {
                out.push_str(&float_repr(n.as_f64().unwrap()));
            }
        }
        Value::String(s) => write_str(out, s),
        Value::Array(a) => {
            if a.is_empty() {
                out.push_str("[]");
                return;
            }
            out.push('[');
            for (i, x) in a.iter().enumerate() {
                if i > 0 {
                    out.push(',');
                    if indent.is_none() {
                        out.push(' ');
                    }
                }
                newline(out, indent, level + 1);
                write_value(out, x, indent, level + 1);
            }
            newline(out, indent, level);
            out.push(']');
        }
        Value::Object(o) => {
            if o.is_empty() {
                out.push_str("{}");
                return;
            }
            out.push('{');
            for (i, (k, x)) in o.iter().enumerate() {
                if i > 0 {
                    out.push(',');
                    if indent.is_none() {
                        out.push(' ');
                    }
                }
                newline(out, indent, level + 1);
                write_str(out, k);
                out.push_str(": ");
                write_value(out, x, indent, level + 1);
            }
            newline(out, indent, level);
            out.push('}');
        }
    }
}

fn newline(out: &mut String, indent: Option<usize>, level: usize) {
    if let Some(n) = indent {
        out.push('\n');
        for _ in 0..(n * level) {
            out.push(' ');
        }
    }
}

/// json.dumps(v, indent=indent): no trailing newline, as json.dump leaves
/// the file.
pub fn dumps(v: &Value, indent: Option<usize>) -> String {
    let mut out = String::new();
    write_value(&mut out, v, indent, 0);
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn float_reprs_match_python() {
        for (x, s) in [
            (2.0, "2.0"),
            (0.5, "0.5"),
            (1e-5, "1e-05"),
            (1.5e16, "1.5e+16"),
            (123456.789, "123456.789"),
            (0.0001, "0.0001"),
            (0.00001234, "1.234e-05"),
            (1e16, "1e+16"),
            (-3.25, "-3.25"),
            (100.0, "100.0"),
            (1e15, "1000000000000000.0"),
        ] {
            assert_eq!(float_repr(x), s, "{x}");
        }
    }

    #[test]
    fn g_matches_python() {
        for (x, s) in [
            (2.0, "2"),
            (2.4, "2.4"),
            (1.5, "1.5"),
            (0.36835, "0.36835"),
            (1234567.0, "1.23457e+06"),
            (0.00001, "1e-05"),
        ] {
            assert_eq!(g(x), s, "{x}");
        }
    }

    #[test]
    fn compact_and_indented_shapes() {
        let v: Value =
            serde_json::from_str(r#"{"a": [1, 2.0, "x\ny"], "b": {}, "c": [], "d": null}"#)
                .unwrap();
        assert_eq!(
            dumps(&v, None),
            r#"{"a": [1, 2.0, "x\ny"], "b": {}, "c": [], "d": null}"#
        );
        assert_eq!(dumps(&v, Some(2)), "{\n  \"a\": [\n    1,\n    2.0,\n    \"x\\ny\"\n  ],\n  \"b\": {},\n  \"c\": [],\n  \"d\": null\n}");
        assert_eq!(
            dumps(&Value::String("\u{e9}\u{1f600}".into()), None),
            "\"\\u00e9\\ud83d\\ude00\""
        );
    }

    /// Every graph/ file the Python tooling writes reads back and re-writes
    /// to the same bytes (a trailing newline aside).
    #[test]
    fn graph_files_roundtrip() {
        let root = crate::data::repo_root();
        for (name, indent) in [
            ("evidence.json", 2),
            ("problems.json", 1),
            ("nodes.json", 2),
            ("drills.json", 2),
            ("curve.json", 2),
            ("solvecost.json", 2),
        ] {
            let path = root.join("graph").join(name);
            let Ok(text) = std::fs::read_to_string(&path) else {
                continue;
            };
            let v: Value = serde_json::from_str(&text).unwrap();
            assert_eq!(
                dumps(&v, Some(indent)),
                text.trim_end_matches('\n'),
                "{name}"
            );
        }
    }
}
