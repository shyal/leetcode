// chat - the Claude Code conversation of the branch you are on.
//
//   make chat                 # open (or reopen) this branch's conversation
//   make chat -- --model x    # extra arguments go to claude as they are
//   kg_chat --check           # UserPromptSubmit hook: warn when the running
//                             # session is not this branch's own
//   kg_chat --switch          # restart the Claude Code in this repo's iTerm2
//                             # pane on this branch's conversation (called by
//                             # make drill, make next prepare, make wake, and
//                             # by make solved, failed, sleep, drop on the way
//                             # back to master)
//
// A problem's branch is its number, a drill's its graph id (d82), so the
// branch names the thing being worked on. Its session id is a fixed
// function of that name: the first `make chat` on a branch starts the
// conversation under that id, every later one resumes it, and a parked
// problem (1235-slept) wakes into the conversation it had. Nothing is
// stored; "is there a conversation yet" is whether its transcript exists.
// On master there is no thing being worked on, so claude starts as usual.
//
// `make chat` is a loop, not a plain exec: it runs claude, and when claude
// exits because --switch asked it to, it runs claude again on the branch
// that is now checked out. So the pane follows the branch without anything
// being typed into it (typed-ahead input is flushed when claude restores
// the terminal, which is why typing `make chat` after the exit never ran).
// The loop notes claude's pid in .chat.json; --switch only touches a
// claude that the loop started.
//
// Ported from utils/kg/chat (Python) on 2026-09-12.

use std::io::Read;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::Duration;

use serde_json::{json, Value};
use uuid::Uuid;

/// The repo root: the directory holding graph/nodes.json, from KG_ROOT, the
/// binary's own location (utils/rs/target/...), or the working directory.
fn repo_root() -> PathBuf {
    if let Ok(r) = std::env::var("KG_ROOT") {
        return PathBuf::from(r);
    }
    let mut candidates: Vec<PathBuf> = Vec::new();
    if let Ok(exe) = std::env::current_exe() {
        let mut p = exe.as_path();
        while let Some(parent) = p.parent() {
            candidates.push(parent.to_path_buf());
            p = parent;
        }
    }
    if let Ok(cwd) = std::env::current_dir() {
        candidates.push(cwd);
    }
    candidates
        .into_iter()
        .find(|c| c.join("graph").join("nodes.json").exists())
        .unwrap_or_else(|| PathBuf::from("."))
}

struct Chat {
    root: PathBuf,
    /// ~/.claude/projects/<root with / as ->
    project_dir: PathBuf,
    /// {"pid": claude started by the loop, "switch": true while a restart is wanted}
    state: PathBuf,
}

impl Chat {
    fn new() -> Chat {
        let root = repo_root();
        let home = std::env::var("HOME").unwrap_or_default();
        let project_dir = Path::new(&home)
            .join(".claude")
            .join("projects")
            .join(root.to_string_lossy().replace('/', "-"));
        let state = root.join(".chat.json");
        Chat {
            root,
            project_dir,
            state,
        }
    }

    fn load_state(&self) -> Value {
        std::fs::read_to_string(&self.state)
            .ok()
            .and_then(|s| serde_json::from_str(&s).ok())
            .unwrap_or_else(|| json!({}))
    }

    fn save_state(&self, state: &Value) {
        let _ = std::fs::write(&self.state, state.to_string());
    }

    fn branch(&self) -> String {
        let out = Command::new("git")
            .args(["rev-parse", "--abbrev-ref", "HEAD"])
            .current_dir(&self.root)
            .output();
        out.map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
            .unwrap_or_default()
    }

    fn transcript(&self, sid: &str) -> PathBuf {
        self.project_dir.join(format!("{sid}.jsonl"))
    }

    /// Hook: one line when this session is not the branch's own.
    fn check(&self) {
        let mut input = String::new();
        if std::io::stdin().read_to_string(&mut input).is_err() {
            return;
        }
        let Ok(v) = serde_json::from_str::<Value>(&input) else {
            return;
        };
        let sid = v.get("session_id").and_then(Value::as_str).unwrap_or("");
        let name = self.branch();
        if matches!(name.as_str(), "" | "master" | "HEAD") || sid == session_id(&name) {
            return;
        }
        println!("[this is not branch {name}'s conversation - exit and `make chat` to open it]");
    }

    /// The tty of the claude process `pid` if it is a claude whose working
    /// directory is this repo, else None. Only the pid the loop noted is
    /// consulted: another claude open in this repo (a second pane, a
    /// `claude` typed by hand) must not be mistaken for the loop's.
    fn claude_tty(&self, pid: i64) -> Option<String> {
        let ps = Command::new("ps")
            .args(["-o", "tty=,comm=", "-p", &pid.to_string()])
            .output()
            .ok()?;
        let ps: Vec<String> = String::from_utf8_lossy(&ps.stdout)
            .split_whitespace()
            .map(String::from)
            .collect();
        if ps.len() != 2 || ps[1] != "claude" || ps[0] == "??" {
            return None;
        }
        let cwd = Command::new("lsof")
            .args(["-a", "-p", &pid.to_string(), "-d", "cwd", "-Fn"])
            .output()
            .ok()?;
        let cwd = String::from_utf8_lossy(&cwd.stdout).into_owned();
        let mine = format!("\nn{}\n", self.root.to_string_lossy());
        if cwd.contains(&mine) || cwd.trim_end().ends_with(mine.trim_end()) {
            Some(format!("/dev/{}", ps[0]))
        } else {
            None
        }
    }

    /// Exit the claude that `make chat` is running in this repo's iTerm2
    /// pane; the loop starts it again on the branch now checked out.
    /// Nothing to do when no such claude is running.
    fn switch(&self) {
        let mut state = self.load_state();
        let pid = state.get("pid").and_then(Value::as_i64);
        let tty = pid.filter(|p| alive(*p)).and_then(|p| self.claude_tty(p));
        let (Some(pid), Some(tty)) = (pid, tty) else {
            println!(
                "no `make chat` running in this repo - start claude with `make chat` and it follows the branch"
            );
            return;
        };
        state["switch"] = Value::Bool(true);
        self.save_state(&state);
        let sid = osascript(&format!(
            r#"
tell application "iTerm2"
  repeat with w in windows
    repeat with t in tabs of w
      repeat with s in sessions of t
        if tty of s is "{tty}" then return id of s
      end repeat
    end repeat
  end repeat
  return ""
end tell"#
        ));
        if !sid.is_empty() {
            // raw keystrokes: no trailing newline, which the input box takes
            // as a line break
            let key = |text: &str| {
                osascript(&format!(
                    "tell application \"iTerm2\" to tell session id \"{sid}\" to write text {text} newline NO"
                ));
            };
            key("(ASCII character 27)"); // Escape: leave a running turn or a menu first
            key("\"/exit\"");
            key("(ASCII character 13)"); // Enter
        }
        if !wait_gone(pid, 5.0) {
            kill(pid, libc::SIGTERM); // the transcript is written as it goes; nothing is lost
            if !wait_gone(pid, 5.0) {
                kill(pid, libc::SIGKILL);
                wait_gone(pid, 2.0);
            }
        }
    }

    fn claude_args(&self, args: &[String]) -> Vec<String> {
        let name = self.branch();
        let mut out = vec!["claude".to_string()];
        if !matches!(name.as_str(), "" | "master" | "HEAD") {
            let sid = session_id(&name);
            if self.transcript(&sid).exists() {
                out.push("--resume".to_string());
            } else {
                out.push("--session-id".to_string());
            }
            out.push(sid);
        }
        out.extend(args.iter().cloned());
        out
    }

    /// Run claude on this branch's conversation; when a --switch ended it,
    /// run it again on the branch now checked out. Any other exit ends the
    /// loop, with claude's exit code.
    fn run_loop(&self, args: &[String]) {
        loop {
            let argv = self.claude_args(args);
            let mut child = match Command::new(&argv[0]).args(&argv[1..]).spawn() {
                Ok(c) => c,
                Err(e) => {
                    eprintln!("claude: {e}");
                    std::process::exit(1);
                }
            };
            self.save_state(&json!({"pid": child.id()}));
            let code = child.wait().ok().and_then(|s| s.code()).unwrap_or(1);
            let state = self.load_state();
            let _ = std::fs::remove_file(&self.state);
            if !state
                .get("switch")
                .and_then(Value::as_bool)
                .unwrap_or(false)
            {
                std::process::exit(code);
            }
            println!("switching to branch {}", self.branch());
        }
    }
}

/// The thing a branch is about: a parked problem's branch drops its -slept
/// suffix so waking resumes the conversation, not a new one.
fn key_of(name: &str) -> &str {
    name.strip_suffix("-slept").unwrap_or(name)
}

/// uuid5(NAMESPACE_URL, "leet/" + key), as Python's uuid module computes it.
pub fn session_id(name: &str) -> String {
    Uuid::new_v5(
        &Uuid::NAMESPACE_URL,
        format!("leet/{}", key_of(name)).as_bytes(),
    )
    .to_string()
}

fn osascript(script: &str) -> String {
    Command::new("osascript")
        .args(["-e", script])
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
        .unwrap_or_default()
}

fn alive(pid: i64) -> bool {
    // SAFETY: kill with signal 0 only probes for the process
    unsafe { libc::kill(pid as libc::pid_t, 0) == 0 }
}

fn kill(pid: i64, sig: libc::c_int) {
    // SAFETY: the pid is the one the loop noted for a process we started
    unsafe {
        libc::kill(pid as libc::pid_t, sig);
    }
}

fn wait_gone(pid: i64, secs: f64) -> bool {
    for _ in 0..(secs * 10.0) as usize {
        if !alive(pid) {
            return true;
        }
        std::thread::sleep(Duration::from_millis(100));
    }
    !alive(pid)
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let chat = Chat::new();
    match args.first().map(String::as_str) {
        Some("--check") => chat.check(),
        Some("--switch") => chat.switch(),
        _ => chat.run_loop(&args),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn slept_branch_shares_the_session() {
        assert_eq!(session_id("1235"), session_id("1235-slept"));
        assert_ne!(session_id("1235"), session_id("1236"));
    }

    #[test]
    fn python_uuid5_value() {
        // python3 -c 'import uuid; print(uuid.uuid5(uuid.NAMESPACE_URL, "leet/d82"))'
        assert_eq!(session_id("d82"), "506d4b72-6a9a-574d-aa19-36a42bfaa608");
    }
}
