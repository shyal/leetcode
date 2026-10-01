// The languages a drill or solve file is written in. Python is the house
// language: every problem, the harness, and mu, which compiles to Python.
// Any other language is a drill-only file with its own extension, comment
// prefix and toolchain, served as current.<ext> and archived with the same
// extension. Adding a language is one more entry in LANGS: the bank scan,
// the serve, `make`, the judge and the archive all read this table.

use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::time::{Duration, Instant};

use crate::pysrc::{cleandoc, module_docstring};

pub struct Lang {
    pub name: &'static str,
    pub ext: &'static str,
    /// The line comment prefix, which is what the statement block and the
    /// notes are written in for every language but Python.
    pub comment: &'static str,
}

pub const PYTHON: Lang = Lang {
    name: "Python",
    ext: "py",
    comment: "#",
};

pub const TYPESCRIPT: Lang = Lang {
    name: "TypeScript",
    ext: "ts",
    comment: "//",
};

/// Python first: it is the default wherever one file is looked for.
pub const LANGS: [&Lang; 2] = [&PYTHON, &TYPESCRIPT];

/// The declarations tsc needs for the node builtins a drill imports
/// (`node:assert/strict`), kept in the repo so no npm install is needed.
pub const TS_DECLARATIONS: &str = "utils/harness/ts/node.d.ts";

pub fn of_ext(ext: &str) -> Option<&'static Lang> {
    LANGS.iter().copied().find(|l| l.ext == ext)
}

pub fn of_path(path: &Path) -> Option<&'static Lang> {
    path.extension().and_then(|e| e.to_str()).and_then(of_ext)
}

/// A file the bank or solved/ would hold: one of the known extensions.
pub fn is_source(path: &Path) -> bool {
    of_path(path).is_some()
}

/// "current.py", "current.ts", ...
pub fn current_name(lang: &Lang) -> String {
    format!("current.{}", lang.ext)
}

pub fn current_names() -> Vec<String> {
    LANGS.iter().map(|l| current_name(l)).collect()
}

/// A line with any language's comment prefix and the spaces after it
/// removed: `// DRILL: X` and `DRILL: X` both read `DRILL: X`.
pub fn uncomment(line: &str) -> &str {
    let t = line.trim_start();
    LANGS
        .iter()
        .find_map(|l| t.strip_prefix(l.comment))
        .map_or(t, str::trim_start)
}

/// A regex fragment for an optional comment prefix at the start of a
/// line, for the header regexes the tools run over a whole file.
pub fn comment_prefix() -> String {
    let alts: Vec<String> = LANGS.iter().map(|l| regex::escape(l.comment)).collect();
    format!(r"(?:{})?\s*", alts.join("|"))
}

fn nonempty(path: &Path) -> bool {
    std::fs::read_to_string(path).is_ok_and(|s| !s.trim().is_empty())
}

/// The current file holding work, Python first: `make solved` files it,
/// a serve refuses while it is there.
pub fn busy(root: &Path) -> Option<(PathBuf, &'static Lang)> {
    LANGS
        .iter()
        .map(|l| (root.join(current_name(l)), *l))
        .find(|(p, _)| nonempty(p))
}

/// The statement block: the module docstring in Python, the leading
/// comment block in every other language, with the comment prefix
/// removed and cleaned the way inspect.cleandoc cleans a docstring.
pub fn header(text: &str, lang: &Lang) -> Option<String> {
    if lang.ext == PYTHON.ext {
        return module_docstring(text);
    }
    let mut lines = Vec::new();
    for line in text.lines() {
        let t = line.trim_start();
        if let Some(rest) = t.strip_prefix(lang.comment) {
            lines.push(rest.strip_prefix(' ').unwrap_or(rest).to_string());
        } else if t.is_empty() && lines.is_empty() {
            continue;
        } else {
            break;
        }
    }
    (!lines.is_empty()).then(|| cleandoc(&lines.join("\n")))
}

/// The file without its statement block: the code and what follows.
pub fn strip_header(text: &str, lang: &Lang) -> String {
    if lang.ext == PYTHON.ext {
        return regex::Regex::new(r#"(?s)^""".*?"""\s*"#)
            .unwrap()
            .replace(text, "")
            .into_owned();
    }
    let mut seen = false;
    let mut out = Vec::new();
    for line in text.lines() {
        let t = line.trim_start();
        if !seen && (t.starts_with(lang.comment) || t.is_empty()) {
            continue;
        }
        seen = true;
        out.push(line);
    }
    let mut s = out.join("\n");
    if text.ends_with('\n') {
        s.push('\n');
    }
    s
}

/// The candidate's notes: what follows the first `---` in the statement
/// block, prefixed "notes: \n\n"; "" when there is none.
pub fn notes_of(text: &str, lang: &Lang) -> String {
    match header(text, lang) {
        Some(doc) if doc.contains("---") => {
            let (_, part) = doc.split_once("---").unwrap();
            format!("notes: \n\n{}", part.trim())
        }
        _ => String::new(),
    }
}

/// ("drill", title) or (problem number, title) from a statement block:
/// the first `DRILL:` or `<number>. <title>` line, or the line after a
/// url, as `make solved` names the archive.
pub fn subject(doc: &str) -> Option<(String, String)> {
    let drill = regex::Regex::new(r"^\**DRILL:\**\s*(.+)").unwrap();
    let prob = regex::Regex::new(r"^(\d+[a-zA-Z]?)\.\s*(.+)").unwrap();
    let lines: Vec<&str> = doc.lines().map(str::trim).collect();
    for line in &lines {
        if let Some(m) = drill.captures(line) {
            return Some(("drill".to_string(), m[1].trim().to_string()));
        }
        if let Some(m) = prob.captures(line) {
            return Some((m[1].trim().to_string(), m[2].trim().to_string()));
        }
    }
    for (i, line) in lines.iter().enumerate() {
        if line.starts_with("https://") {
            if let Some(m) = lines.get(i + 1).and_then(|n| prob.captures(n)) {
                return Some((m[1].trim().to_string(), m[2].trim().to_string()));
            }
        }
    }
    None
}

/// What the busy current file is about: (path, language, id, title, text).
pub fn current_subject(root: &Path) -> Option<(PathBuf, &'static Lang, String, String, String)> {
    let (path, lang) = busy(root)?;
    let text = std::fs::read_to_string(&path).ok()?;
    let (id, title) = subject(&header(&text, lang)?)?;
    Some((path, lang, id, title, text))
}

/// The type check a language runs before the file: (passed, diagnostics),
/// or None for a language with no separate checker. TypeScript: tsc in
/// strict mode over the file and the node declarations.
pub fn check(root: &Path, path: &Path, lang: &Lang) -> Option<(bool, String)> {
    if lang.ext != TYPESCRIPT.ext {
        return None;
    }
    let out = Command::new("tsc")
        .args([
            "--noEmit",
            "--strict",
            "--target",
            "es2022",
            "--lib",
            "es2022,dom",
            "--types",
        ])
        .arg(root.join(TS_DECLARATIONS))
        .arg(path)
        .current_dir(root)
        .output();
    Some(match out {
        Ok(o) => (
            o.status.success(),
            format!(
                "{}{}",
                String::from_utf8_lossy(&o.stdout),
                String::from_utf8_lossy(&o.stderr)
            ),
        ),
        Err(e) => (false, format!("tsc: {e}")),
    })
}

/// The command that runs the file the way the candidate does: the venv's
/// python with the harness on PYTHONPATH, or node stripping types.
pub fn command(root: &Path, path: &Path, lang: &Lang) -> Command {
    let mut cmd = if lang.ext == TYPESCRIPT.ext {
        let mut c = Command::new("node");
        c.args(["--experimental-strip-types", "--no-warnings"])
            .arg(path);
        c
    } else {
        let py = root.join(".venv/bin/python3");
        let mut c = Command::new(if py.exists() {
            py
        } else {
            PathBuf::from("python3")
        });
        c.arg(path).env(
            "PYTHONPATH",
            format!(
                "{}:{}:{}:{}",
                root.display(),
                root.join("utils").display(),
                root.join("utils/harness").display(),
                std::env::var("PYTHONPATH").unwrap_or_default()
            ),
        );
        c
    };
    cmd.current_dir(root);
    cmd
}

/// Execute a file the way the candidate does: (status, detail), the status
/// one of passed, failed, timeout, unknown. A language with a checker runs
/// it first; a file that does not type-check fails with the diagnostics as
/// its detail. `timeout` is in seconds. The judge reads the result
/// (kg_extract) and make solved refuses a file that does not pass
/// (kg_solved).
pub fn run(root: &Path, abs: &Path, lang: &Lang, timeout: u64) -> (String, String) {
    if let Some((ok, diagnostics)) = check(root, abs, lang) {
        if !ok {
            let tail: String = diagnostics
                .chars()
                .rev()
                .take(800)
                .collect::<Vec<_>>()
                .into_iter()
                .rev()
                .collect();
            return (
                "failed".into(),
                format!("{} rejected the file:\n{}", "the type checker", tail.trim()),
            );
        }
    }
    let child = command(root, abs, lang)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn();
    let mut child = match child {
        Ok(c) => c,
        Err(e) => {
            return (
                "unknown".into(),
                format!(
                    "could not execute: {}",
                    e.to_string().chars().take(200).collect::<String>()
                ),
            )
        }
    };
    let mut out_pipe = child.stdout.take().unwrap();
    let mut err_pipe = child.stderr.take().unwrap();
    let out_t = std::thread::spawn(move || {
        let mut s = String::new();
        let _ = std::io::Read::read_to_string(&mut out_pipe, &mut s);
        s
    });
    let err_t = std::thread::spawn(move || {
        let mut s = String::new();
        let _ = std::io::Read::read_to_string(&mut err_pipe, &mut s);
        s
    });
    let start = Instant::now();
    let status = loop {
        if let Ok(Some(st)) = child.try_wait() {
            break Some(st);
        }
        if start.elapsed() > Duration::from_secs(timeout) {
            let _ = child.kill();
            let _ = child.wait();
            break None;
        }
        std::thread::sleep(Duration::from_millis(50));
    };
    let stdout = out_t.join().unwrap_or_default();
    let stderr = err_t.join().unwrap_or_default();
    let tail = |s: &str, n: usize| -> String {
        let t = s.trim();
        let chars: Vec<char> = t.chars().collect();
        chars[chars.len().saturating_sub(n)..].iter().collect()
    };
    match status {
        None => (
            "timeout".into(),
            format!("exceeded {timeout}s — likely TLE or an infinite loop"),
        ),
        Some(st) if st.success() => ("passed".into(), tail(&stdout, 600)),
        Some(_) => (
            "failed".into(),
            tail(
                if stderr.trim().is_empty() {
                    &stdout
                } else {
                    &stderr
                },
                800,
            ),
        ),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// 2026-10-01: a file whose assert fails is reported failed with the
    /// error as the detail, and one that exits 0 is passed; make solved
    /// refuses the first.
    #[test]
    fn run_reports_a_failing_assert() {
        let dir = std::env::temp_dir().join(format!("kg_lang_run_{}", std::process::id()));
        std::fs::create_dir_all(&dir).unwrap();
        let bad = dir.join("bad.py");
        std::fs::write(&bad, "assert 1 + 1 == 3\n").unwrap();
        let (status, detail) = run(&dir, &bad, &PYTHON, 30);
        assert_eq!(status, "failed");
        assert!(detail.contains("AssertionError"), "{detail}");
        let good = dir.join("good.py");
        std::fs::write(&good, "assert 1 + 1 == 2\n").unwrap();
        assert_eq!(run(&dir, &good, &PYTHON, 30).0, "passed");
        let _ = std::fs::remove_dir_all(&dir);
    }

    const TS: &str = "// DRILL: Order Total\n// TRAINS: ts-object-type\n//\n// Given items, return the total.\n//\n// ---\n// looked up ??\n\nfunction orderTotal(): number {\n  return 1;\n}\n";

    #[test]
    fn languages_by_extension() {
        assert_eq!(
            of_path(Path::new("drills/x/d1_a.ts")).unwrap().name,
            "TypeScript"
        );
        assert_eq!(of_path(Path::new("current.py")).unwrap().ext, "py");
        assert!(of_path(Path::new("current.md")).is_none());
        assert_eq!(current_names(), vec!["current.py", "current.ts"]);
    }

    #[test]
    fn comment_header_reads_like_a_docstring() {
        let h = header(TS, &TYPESCRIPT).unwrap();
        assert!(h.starts_with("DRILL: Order Total\nTRAINS: ts-object-type\n\nGiven items"));
        assert_eq!(notes_of(TS, &TYPESCRIPT), "notes: \n\nlooked up ??");
        assert_eq!(
            strip_header(TS, &TYPESCRIPT),
            "function orderTotal(): number {\n  return 1;\n}\n"
        );
        assert_eq!(header("x = 1\n", &TYPESCRIPT), None);
    }

    #[test]
    fn comment_prefixes() {
        assert_eq!(uncomment("  // DRILL: X"), "DRILL: X");
        assert_eq!(uncomment("# DRILL: X"), "DRILL: X");
        assert_eq!(uncomment("DRILL: X"), "DRILL: X");
        let re = regex::Regex::new(&format!(r"(?m)^\s*{}DRILL:", comment_prefix())).unwrap();
        assert!(re.is_match("x\n// DRILL: a") && re.is_match("DRILL: a") && !re.is_match("no"));
    }

    #[test]
    fn subjects() {
        assert_eq!(
            subject("DRILL: Order Total\nTRAINS: x"),
            Some(("drill".into(), "Order Total".into()))
        );
        assert_eq!(
            subject("URL: x\n\n1. Two Sum\n"),
            Some(("1".into(), "Two Sum".into()))
        );
        assert_eq!(
            subject("https://leetcode.com/x\n1. Two Sum"),
            Some(("1".into(), "Two Sum".into()))
        );
        assert_eq!(subject("nothing here"), None);
    }

    #[test]
    fn python_header_is_the_docstring() {
        let py = "\"\"\"\nDRILL: A\n\n---\nnote\n\"\"\"\n\nx = 1\n";
        assert_eq!(header(py, &PYTHON).unwrap(), "DRILL: A\n\n---\nnote");
        assert_eq!(notes_of(py, &PYTHON), "notes: \n\nnote");
        assert_eq!(strip_header(py, &PYTHON), "x = 1\n");
    }

    #[test]
    fn busy_prefers_python_and_skips_blank_files() {
        let dir = std::env::temp_dir().join(format!("lang_busy_{}", std::process::id()));
        let _ = std::fs::create_dir_all(&dir);
        std::fs::write(dir.join("current.py"), "\n").unwrap();
        assert!(busy(&dir).is_none());
        std::fs::write(dir.join("current.ts"), "// DRILL: X\n").unwrap();
        assert_eq!(busy(&dir).unwrap().1.ext, "ts");
        std::fs::write(dir.join("current.py"), "x = 1\n").unwrap();
        assert_eq!(busy(&dir).unwrap().1.ext, "py");
        let _ = std::fs::remove_dir_all(&dir);
    }
}
