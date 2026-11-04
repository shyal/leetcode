// kg_open - the last step of every serve: open the file the serve wrote in
// VS Code, so the right tab, with the right language, is in front of the
// candidate without him picking a file. Which file: the served file
// (kg::lang::served: current.mu for a Python serve, current.py for one mu
// could not hold, current.<ext> for another language), else current.md
// (a recognition rep). `code -r` reuses the open window. A missing
// `code`, or no file, is silent: the serve has already succeeded.

use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

/// The file to open, or None when nothing is served.
pub fn served_file(root: &Path) -> Option<PathBuf> {
    let nonempty = |p: PathBuf| {
        std::fs::read_to_string(&p)
            .is_ok_and(|s| !s.trim().is_empty())
            .then_some(p)
    };
    kg::lang::served(root)
        .map(|(path, _)| path)
        .or_else(|| nonempty(root.join("current.md")))
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

    /// A Python serve is current.mu, the stub as served included; a serve
    /// mu could not hold is current.py.
    #[test]
    fn a_python_serve_opens_current_mu() {
        let d = dir("py");
        assert_eq!(served_file(&d), None);
        std::fs::write(d.join("current.py"), "\"\"\"\nDRILL: X\n\"\"\"\n\nx = 1\n").unwrap();
        assert_eq!(served_file(&d), Some(d.join("current.py")));
        std::fs::write(d.join("current.py"), "").unwrap();
        std::fs::write(d.join("current.mu"), "# DRILL: X\n").unwrap();
        std::fs::write(d.join(kg::lang::MU_STUB), "# DRILL: X\n").unwrap();
        assert_eq!(served_file(&d), Some(d.join("current.mu")));
        let _ = std::fs::remove_dir_all(&d);
    }

    /// A current.mu left from an earlier serve does not hide another
    /// language's file.
    #[test]
    fn another_language_opens_its_own_file() {
        let d = dir("ts");
        std::fs::write(d.join("current.mu"), "# stale\n").unwrap();
        std::fs::write(d.join("current.ts"), "// DRILL: Y\n").unwrap();
        assert_eq!(served_file(&d), Some(d.join("current.ts")));
        let _ = std::fs::remove_dir_all(&d);
    }

    #[test]
    fn a_recognition_rep_opens_current_md() {
        let d = dir("md");
        std::fs::write(d.join("current.md"), "# 1. Two Sum\n").unwrap();
        assert_eq!(served_file(&d), Some(d.join("current.md")));
        std::fs::write(d.join("current.md"), "\n").unwrap();
        assert_eq!(served_file(&d), None);
        let _ = std::fs::remove_dir_all(&d);
    }
}
