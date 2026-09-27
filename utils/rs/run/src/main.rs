// run - what `make` does: run the current file. A Python attempt goes
// through mu/session.py, which splices current.mu in when it holds the
// work. Any other language's current.<ext> (kg::lang) is type-checked
// when the language has a checker and then run with its toolchain; the
// diagnostics print either way, and the exit status is the run's, or 1
// when the check failed.

use std::process::Command;

fn main() {
    let root = kg::data::repo_root();
    let (path, lang) = match kg::lang::busy(&root) {
        Some((p, l)) if l.ext != kg::lang::PYTHON.ext => (p, l),
        _ => {
            let status = Command::new(root.join(".venv/bin/python3"))
                .arg(root.join("mu/session.py"))
                .arg("run")
                .current_dir(&root)
                .status()
                .expect("python");
            std::process::exit(status.code().unwrap_or(1));
        }
    };
    let mut checked = true;
    if let Some((ok, diagnostics)) = kg::lang::check(&root, &path, lang) {
        if !ok {
            checked = false;
            eprint!("{diagnostics}");
        }
    }
    let status = kg::lang::command(&root, &path, lang)
        .status()
        .unwrap_or_else(|e| {
            eprintln!("could not run {}: {e}", path.display());
            std::process::exit(1)
        });
    std::process::exit(if status.success() && checked {
        0
    } else {
        status.code().unwrap_or(1).max(1)
    });
}
