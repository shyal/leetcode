//! Execute a solution+asserts file the way the prepare pipeline validates
//! it: written to a temp file under .prepare_cache, run with the venv's
//! python and the harness on PYTHONPATH, killed at the timeout.

use std::io::Read;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::sync::atomic::{AtomicU64, Ordering};
use std::time::{Duration, Instant};

pub const CACHE_DIR: &str = ".prepare_cache";

pub struct Outcome {
    pub ok: bool,
    pub output: String,
    pub timed_out: bool,
}

static SEQ: AtomicU64 = AtomicU64::new(0);

/// The interpreter the makefile runs the tooling with, or the PATH's.
pub fn python(root: &Path) -> PathBuf {
    let venv = root.join(".venv/bin/python3");
    if venv.exists() {
        venv
    } else {
        PathBuf::from("python3")
    }
}

/// utils, utils/harness, then whatever PYTHONPATH already held.
pub fn pythonpath(root: &Path) -> String {
    let mut parts = vec![
        root.join("utils").display().to_string(),
        root.join("utils/harness").display().to_string(),
    ];
    parts.push(std::env::var("PYTHONPATH").unwrap_or_default());
    parts.join(":")
}

fn drain(mut pipe: impl Read + Send + 'static) -> std::thread::JoinHandle<String> {
    std::thread::spawn(move || {
        let mut buf = Vec::new();
        let _ = pipe.read_to_end(&mut buf);
        String::from_utf8_lossy(&buf).into_owned()
    })
}

/// Run `code` as a script, (exit ok, stdout+stderr stripped), the partial
/// output kept when the timeout kills it.
pub fn run(root: &Path, code: &str, timeout: Duration) -> Outcome {
    let dir = root.join(CACHE_DIR);
    let _ = std::fs::create_dir_all(&dir);
    let path = dir.join(format!(
        "tmp{}_{}.py",
        std::process::id(),
        SEQ.fetch_add(1, Ordering::Relaxed)
    ));
    std::fs::write(&path, code).expect("write temp file");
    let outcome = run_file(root, &path, timeout);
    let _ = std::fs::remove_file(&path);
    outcome
}

fn run_file(root: &Path, path: &Path, timeout: Duration) -> Outcome {
    let spawned = Command::new(python(root))
        .arg(path)
        .current_dir(root)
        .env("PYTHONPATH", pythonpath(root))
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn();
    let mut child = match spawned {
        Ok(c) => c,
        Err(e) => {
            return Outcome {
                ok: false,
                output: e.to_string(),
                timed_out: false,
            }
        }
    };
    let out = drain(child.stdout.take().unwrap());
    let err = drain(child.stderr.take().unwrap());
    let started = Instant::now();
    let mut timed_out = false;
    let status = loop {
        match child.try_wait() {
            Ok(Some(s)) => break Some(s),
            Ok(None) if started.elapsed() >= timeout => {
                timed_out = true;
                let _ = child.kill();
                let _ = child.wait();
                break None;
            }
            Ok(None) => std::thread::sleep(Duration::from_millis(20)),
            Err(_) => break None,
        }
    };
    let text = format!(
        "{}{}",
        out.join().unwrap_or_default(),
        err.join().unwrap_or_default()
    );
    Outcome {
        ok: status.is_some_and(|s| s.success()),
        output: text.trim().to_string(),
        timed_out,
    }
}
