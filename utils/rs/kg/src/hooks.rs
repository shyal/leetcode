//! Pre-serve hooks: commands that run before a new question is served.
//!
//! The hooks are listed in `.hooks.json` at the repo root. The file is not
//! checked in: what a hook checks is the operator's business, and only this
//! runner is public. The file looks like
//!
//! ```json
//! {"pre_serve": [{"name": "gym", "run": ["/path/to/check", "gym"]}]}
//! ```
//!
//! A hook passes when its command exits 0. Any other exit refuses the
//! serve, and the last line the command printed is the reason. A hook that
//! cannot be started, runs past its time limit, or is listed in a file
//! that does not parse also refuses: a broken hook never opens the way.
//!
//! The file itself is pinned. With no `.hooks.json` nothing is served, and
//! a file whose sha256 differs from CONFIG_SHA256 below refuses too, so
//! deleting or editing the file closes the way instead of opening it.
//! Changing the hooks means changing this constant: a source edit, a
//! rebuild and a commit.
//!
//! Every hook runs, in parallel, and every refusal is returned. The
//! problem already on its branch stays open; only a new question is gated.

use std::path::Path;
use std::process::{Command, Stdio};
use std::time::{Duration, Instant};

pub const CONFIG: &str = ".hooks.json";

/// sha256 of the approved `.hooks.json`.
pub const CONFIG_SHA256: &str = "3c91960676e41ad1719276d963b202816eadc72401b2e24c17638ffa64c306dc";

const TIME_LIMIT: Duration = Duration::from_secs(60);

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Refusal {
    pub name: String,
    pub reason: String,
}

#[derive(Debug, Clone)]
struct Hook {
    name: String,
    run: Vec<String>,
}

fn sha256_hex(bytes: &[u8]) -> String {
    use sha2::{Digest, Sha256};
    Sha256::digest(bytes)
        .iter()
        .map(|b| format!("{b:02x}"))
        .collect()
}

/// The hooks listed in the config, or the refusal a missing, changed or
/// bad config stands for.
fn load(root: &Path, expected_sha256: &str) -> Result<Vec<Hook>, Refusal> {
    let bad = |reason: String| Refusal {
        name: CONFIG.to_string(),
        reason,
    };
    let Ok(bytes) = std::fs::read(root.join(CONFIG)) else {
        return Err(bad(format!(
            "There is no {CONFIG}, and nothing is served without it."
        )));
    };
    if sha256_hex(&bytes) != expected_sha256 {
        return Err(bad(format!(
            "{CONFIG} has changed since its hash was recorded, so nothing is served."
        )));
    }
    let text = String::from_utf8_lossy(&bytes);
    let value: serde_json::Value =
        serde_json::from_str(&text).map_err(|e| bad(format!("{CONFIG} does not parse: {e}")))?;
    let Some(list) = value.get("pre_serve") else {
        return Ok(Vec::new());
    };
    let list = list
        .as_array()
        .ok_or_else(|| bad(format!("{CONFIG}: pre_serve is not a list")))?;
    let mut hooks = Vec::new();
    for (i, h) in list.iter().enumerate() {
        let name = h
            .get("name")
            .and_then(|n| n.as_str())
            .map(str::to_string)
            .unwrap_or_else(|| format!("hook {i}"));
        let run: Option<Vec<String>> = h.get("run").and_then(|r| r.as_array()).and_then(|a| {
            a.iter()
                .map(|s| s.as_str().map(str::to_string))
                .collect::<Option<Vec<_>>>()
        });
        match run {
            Some(run) if !run.is_empty() => hooks.push(Hook { name, run }),
            _ => return Err(bad(format!("{CONFIG}: {name} has no run list of strings"))),
        }
    }
    Ok(hooks)
}

/// The last non-empty line of the text, trimmed.
fn last_line(text: &str) -> Option<String> {
    text.lines()
        .map(str::trim)
        .rfind(|l| !l.is_empty())
        .map(str::to_string)
}

fn run_one(root: &Path, hook: &Hook, kind: &str, limit: Duration) -> Option<Refusal> {
    let refuse = |reason: String| {
        Some(Refusal {
            name: hook.name.clone(),
            reason,
        })
    };
    let child = Command::new(&hook.run[0])
        .args(&hook.run[1..])
        .current_dir(root)
        .env("LEET_SERVE", kind)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn();
    let mut child = match child {
        Ok(c) => c,
        Err(e) => return refuse(format!("could not start {}: {e}", hook.run[0])),
    };
    let start = Instant::now();
    loop {
        match child.try_wait() {
            Ok(Some(_)) => break,
            Ok(None) if start.elapsed() > limit => {
                let _ = child.kill();
                let _ = child.wait();
                return refuse(format!("did not finish in {} seconds", limit.as_secs()));
            }
            Ok(None) => std::thread::sleep(Duration::from_millis(20)),
            Err(e) => return refuse(format!("could not wait for it: {e}")),
        }
    }
    let out = match child.wait_with_output() {
        Ok(o) => o,
        Err(e) => return refuse(format!("could not read its output: {e}")),
    };
    if out.status.success() {
        return None;
    }
    let reason = last_line(&String::from_utf8_lossy(&out.stdout))
        .or_else(|| last_line(&String::from_utf8_lossy(&out.stderr)))
        .unwrap_or_else(|| format!("exited with {}", out.status));
    refuse(reason)
}

fn pre_serve_within(
    root: &Path,
    kind: &str,
    limit: Duration,
    expected_sha256: &str,
) -> Vec<Refusal> {
    let hooks = match load(root, expected_sha256) {
        Ok(h) => h,
        Err(r) => return vec![r],
    };
    std::thread::scope(|s| {
        let handles: Vec<_> = hooks
            .iter()
            .map(|h| s.spawn(move || run_one(root, h, kind, limit)))
            .collect();
        handles
            .into_iter()
            .filter_map(|h| h.join().ok().flatten())
            .collect()
    })
}

/// Run every pre-serve hook. `kind` (problem, drill, spot, next) reaches
/// the hook as the environment variable LEET_SERVE. Empty means serve.
pub fn pre_serve(root: &Path, kind: &str) -> Vec<Refusal> {
    pre_serve_within(root, kind, TIME_LIMIT, CONFIG_SHA256)
}

/// The refusals as the lines printed where the question would be.
pub fn refusal_text(refusals: &[Refusal]) -> String {
    let mut lines = vec!["Nothing is served until these are done:".to_string()];
    for r in refusals {
        lines.push(format!("  {}: {}", r.name, r.reason));
    }
    lines.join("\n")
}

/// Print the refusals and exit 1, or return when every hook passed.
pub fn gate(root: &Path, kind: &str) {
    let refusals = pre_serve(root, kind);
    if !refusals.is_empty() {
        println!("{}", refusal_text(&refusals));
        std::process::exit(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::PathBuf;

    fn scratch(name: &str) -> PathBuf {
        let dir = std::env::temp_dir().join(format!("kg_hooks_{name}_{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(&dir).unwrap();
        dir
    }

    fn with_config(name: &str, json: &str) -> PathBuf {
        let dir = scratch(name);
        std::fs::write(dir.join(CONFIG), json).unwrap();
        dir
    }

    /// Run the hooks with the scratch config's own hash as the approved one.
    fn pre_serve(dir: &Path, kind: &str) -> Vec<Refusal> {
        pre_serve_limit(dir, kind, TIME_LIMIT)
    }

    fn pre_serve_limit(dir: &Path, kind: &str, limit: Duration) -> Vec<Refusal> {
        let pinned = std::fs::read(dir.join(CONFIG))
            .map(|b| sha256_hex(&b))
            .unwrap_or_default();
        pre_serve_within(dir, kind, limit, &pinned)
    }

    #[test]
    fn no_config_refuses() {
        let r = super::pre_serve(&scratch("none"), "next");
        assert_eq!(r.len(), 1);
        assert_eq!(r[0].name, CONFIG);
        assert!(r[0].reason.starts_with("There is no"), "{}", r[0].reason);
    }

    #[test]
    fn a_changed_config_refuses() {
        let dir = with_config(
            "changed",
            r#"{"pre_serve": [{"name": "ok", "run": ["sh", "-c", "exit 0"]}]}"#,
        );
        let r = pre_serve_within(&dir, "next", TIME_LIMIT, &sha256_hex(b"the approved file"));
        assert_eq!(r.len(), 1);
        assert!(r[0].reason.contains("has changed"), "{}", r[0].reason);
    }

    #[test]
    fn the_pinned_hash_is_a_sha256() {
        assert_eq!(CONFIG_SHA256.len(), 64);
        assert!(CONFIG_SHA256.chars().all(|c| c.is_ascii_hexdigit()));
        assert_eq!(
            sha256_hex(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
    }

    #[test]
    fn config_without_pre_serve_serves() {
        assert!(pre_serve(&with_config("empty", "{}"), "next").is_empty());
    }

    #[test]
    fn passing_hook_serves() {
        let dir = with_config(
            "pass",
            r#"{"pre_serve": [{"name": "ok", "run": ["sh", "-c", "exit 0"]}]}"#,
        );
        assert!(pre_serve(&dir, "next").is_empty());
    }

    #[test]
    fn failing_hook_refuses_with_its_last_line() {
        let dir = with_config(
            "fail",
            r#"{"pre_serve": [
                {"name": "ok", "run": ["sh", "-c", "exit 0"]},
                {"name": "gym", "run": ["sh", "-c", "echo checking; echo last session was 30 days ago; exit 1"]}
            ]}"#,
        );
        assert_eq!(
            pre_serve(&dir, "next"),
            vec![Refusal {
                name: "gym".into(),
                reason: "last session was 30 days ago".into()
            }]
        );
    }

    #[test]
    fn every_refusal_is_returned_in_order() {
        let dir = with_config(
            "two",
            r#"{"pre_serve": [
                {"name": "a", "run": ["sh", "-c", "echo no a >&2; exit 1"]},
                {"name": "b", "run": ["sh", "-c", "exit 3"]}
            ]}"#,
        );
        let r = pre_serve(&dir, "next");
        assert_eq!(r.len(), 2);
        assert_eq!(r[0].reason, "no a");
        assert_eq!(r[1].name, "b");
        assert!(r[1].reason.contains('3'), "{}", r[1].reason);
    }

    #[test]
    fn the_hook_sees_the_serve_kind() {
        let dir = with_config(
            "kind",
            r#"{"pre_serve": [{"name": "k", "run": ["sh", "-c", "test \"$LEET_SERVE\" = drill"]}]}"#,
        );
        assert!(pre_serve(&dir, "drill").is_empty());
        assert_eq!(pre_serve(&dir, "problem").len(), 1);
    }

    #[test]
    fn a_hook_that_cannot_start_refuses() {
        let dir = with_config(
            "missing",
            r#"{"pre_serve": [{"name": "m", "run": ["/no/such/hook"]}]}"#,
        );
        let r = pre_serve(&dir, "next");
        assert_eq!(r.len(), 1);
        assert!(
            r[0].reason.starts_with("could not start"),
            "{}",
            r[0].reason
        );
    }

    #[test]
    fn a_config_that_does_not_parse_refuses() {
        let r = pre_serve(&with_config("bad", "{not json"), "next");
        assert_eq!(r.len(), 1);
        assert_eq!(r[0].name, CONFIG);
    }

    #[test]
    fn a_hook_without_a_run_list_refuses() {
        let r = pre_serve(
            &with_config("norun", r#"{"pre_serve": [{"name": "x", "run": "gym"}]}"#),
            "next",
        );
        assert_eq!(r.len(), 1);
        assert!(r[0].reason.contains("x has no run list"), "{}", r[0].reason);
    }

    #[test]
    fn a_hook_past_its_time_limit_refuses() {
        let dir = with_config(
            "slow",
            r#"{"pre_serve": [{"name": "s", "run": ["sh", "-c", "sleep 5"]}]}"#,
        );
        let r = pre_serve_limit(&dir, "next", Duration::from_millis(200));
        assert_eq!(r.len(), 1);
        assert!(r[0].reason.starts_with("did not finish"), "{}", r[0].reason);
    }

    #[test]
    fn refusal_text_lists_each_hook() {
        let text = refusal_text(&[Refusal {
            name: "sleep".into(),
            reason: "no sleep logged today".into(),
        }]);
        assert_eq!(
            text,
            "Nothing is served until these are done:\n  sleep: no sleep logged today"
        );
    }
}
