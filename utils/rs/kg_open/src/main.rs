// kg_open - the last step of every serve: open the file the serve wrote in
// VS Code, so the right tab, with the right language, is in front of the
// candidate without him picking a file. Which file: current.mu when it
// holds the stub of a Python serve (mu is what he writes), else the busy
// current.<ext> (kg::lang, current.rs or current.ts), else current.md (a
// recognition rep). `code -r` reuses the open window. A missing `code`,
// or no file, is silent: the serve has already succeeded.

use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

/// The file to open, or None when nothing is served.
pub fn served_file(root: &Path) -> Option<PathBuf> {
    let nonempty = |p: PathBuf| {
        std::fs::read_to_string(&p)
            .is_ok_and(|s| !s.trim().is_empty())
            .then_some(p)
    };
    match kg::lang::busy(root) {
        Some((path, lang)) if lang.ext == kg::lang::PYTHON.ext => {
            nonempty(root.join("current.mu")).or(Some(path))
        }
        Some((path, _)) => Some(path),
        None => nonempty(root.join("current.md")),
    }
}

/// `code` on PATH, else the macOS app bundle's copy.
fn code_binary() -> Option<PathBuf> {
    let on_path = std::env::var_os("PATH").and_then(|paths| {
        std::env::split_paths(&paths)
            .map(|d| d.join("code"))
            .find(|p| p.is_file())
    });
    on_path.or_else(|| {
        let app =
            PathBuf::from("/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code");
        app.is_file().then_some(app)
    })
}

fn main() {
    let root = kg::data::repo_root();
    let (Some(file), Some(code)) = (served_file(&root), code_binary()) else {
        return;
    };
    let _ = Command::new(code)
        .arg("-r")
        .arg(&file)
        .current_dir(&root)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status();
}

#[cfg(test)]
mod tests {
    use super::*;

    fn dir(name: &str) -> PathBuf {
        let d = std::env::temp_dir().join(format!("kg_open_{name}_{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&d);
        std::fs::create_dir_all(&d).unwrap();
        d
    }

    #[test]
    fn a_python_serve_opens_its_mu_when_the_stub_was_written() {
        let d = dir("mu");
        std::fs::write(d.join("current.py"), "class Solution: pass\n").unwrap();
        assert_eq!(served_file(&d), Some(d.join("current.py")));
        std::fs::write(d.join("current.mu"), "# DRILL: X\n").unwrap();
        assert_eq!(served_file(&d), Some(d.join("current.mu")));
    }

    #[test]
    fn another_language_opens_its_own_file_and_a_spot_opens_the_markdown() {
        let d = dir("rs");
        std::fs::write(d.join("current.mu"), "# stale\n").unwrap();
        std::fs::write(d.join("current.rs"), "// DRILL: X\n").unwrap();
        assert_eq!(served_file(&d), Some(d.join("current.rs")));
        std::fs::remove_file(d.join("current.rs")).unwrap();
        assert_eq!(served_file(&d), None);
        std::fs::write(d.join("current.md"), "# 1. Two Sum\n").unwrap();
        assert_eq!(served_file(&d), Some(d.join("current.md")));
    }
}
