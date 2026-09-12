// learning - file the attempt in current.py as "still learning": archived
// into solved/ with prints commented out, squash-merged to master with a
// "reschedule" trailer. The older sibling of make solved, kept for the
// flow it names.
//
//   make learning
//
// Ported from utils/history/learning (Python) on 2026-09-12. Paths are
// relative to the working directory, as they were.

use std::process::Command;

use chrono::Utc;
use regex::Regex;

fn parse_current(path: &str) -> Option<(i64, String, String)> {
    let content = std::fs::read_to_string(path).ok()?;
    let doc = Regex::new(r#"(?s)"""(.*?)""""#)
        .unwrap()
        .captures(&content)?[1]
        .trim()
        .to_string();
    let lines: Vec<&str> = doc.split('\n').collect();
    let prob = Regex::new(r"^(\d+)\.\s*(.+)").unwrap();
    for line in &lines {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        if let Some(m) = prob.captures(line) {
            return Some((m[1].parse().ok()?, m[2].trim().to_string(), content));
        }
    }
    for (i, line) in lines.iter().enumerate() {
        if line.trim().starts_with("https://") {
            if let Some(next) = lines.get(i + 1) {
                if let Some(m) = prob.captures(next.trim()) {
                    return Some((m[1].parse().ok()?, m[2].trim().to_string(), content));
                }
            }
        }
    }
    None
}

fn comment_out_prints(content: &str) -> String {
    content
        .split('\n')
        .map(|line| {
            let stripped = line.trim();
            if stripped.starts_with("print(") || stripped.starts_with("print (") {
                let lead = &line[..line.find(stripped.chars().next().unwrap()).unwrap_or(0)];
                format!("{lead}# {stripped}")
            } else {
                line.to_string()
            }
        })
        .collect::<Vec<_>>()
        .join("\n")
}

fn git_out(args: &[&str]) -> Option<String> {
    let out = Command::new("git").args(args).output().ok()?;
    if out.status.success() {
        Some(String::from_utf8_lossy(&out.stdout).trim().to_string())
    } else {
        None
    }
}

fn git_step(what: &str, args: &[&str]) -> bool {
    let status = Command::new("git").args(args).status();
    match status {
        Ok(s) if s.success() => true,
        Ok(s) => {
            println!(
                "Error {what}: Command '['git', {}]' returned non-zero exit status {}.",
                args.iter()
                    .map(|a| format!("'{a}'"))
                    .collect::<Vec<_>>()
                    .join(", "),
                s.code().unwrap_or(1)
            );
            false
        }
        Err(e) => {
            println!("Error {what}: {e}");
            false
        }
    }
}

fn main() {
    let now = Utc::now().timestamp() as f64;
    // the start: the "started" commit, else the last commit
    let start: f64 = match git_out(&["log", "-1", "--grep=^started$", "--format=%ct"])
        .filter(|s| !s.is_empty())
    {
        Some(s) => s.parse().unwrap_or(now),
        None => match git_out(&["log", "-1", "--format=%ct"]).filter(|s| !s.is_empty()) {
            Some(s) => s.parse().unwrap_or(now),
            None => {
                println!("No commits found. Using current time as start.");
                now
            }
        },
    };
    let delta = (now - start).max(0.0) as i64;
    let solve_time = format!("{}m {}s", delta / 60, delta % 60);

    if !std::path::Path::new("current.py").exists() {
        println!("current.py does not exist. Exiting.");
        return;
    }
    let Some((num, title, content)) = parse_current("current.py") else {
        println!("Could not parse problem number and title from current.py. Exiting.");
        return;
    };
    let content = comment_out_prints(&content);
    let clean_title = title
        .chars()
        .filter(|c| c.is_alphanumeric() || *c == '_' || c.is_whitespace() || *c == '-')
        .collect::<String>()
        .trim()
        .replace(' ', "_");
    let stamp = Utc::now();
    let iso = if stamp.timestamp_subsec_micros() == 0 {
        stamp.format("%Y-%m-%dT%H:%M:%S+00:00").to_string()
    } else {
        stamp.format("%Y-%m-%dT%H:%M:%S%.6f+00:00").to_string()
    };
    let sanitized: String = format!("{iso}Z")
        .chars()
        .map(|c| {
            if c.is_alphanumeric() || c == '_' {
                c
            } else {
                '_'
            }
        })
        .collect();
    let filename = format!("p{num}_{clean_title}_{sanitized}.py");
    let _ = std::fs::create_dir_all("./solved");
    let filepath = format!("./solved/{filename}");
    std::fs::write(&filepath, content).expect("write the solve file");
    std::fs::write("current.py", "").expect("clear current.py");

    let message =
        format!("{num}. {title}\n\nsolve time: {solve_time}\nstill learning - reschedule");
    if !git_step("running git add", &["add", "."]) {
        return;
    }
    if !git_step("running git commit", &["commit", "-m", &message]) {
        return;
    }
    let Some(branch) = git_out(&["rev-parse", "--abbrev-ref", "HEAD"]) else {
        println!("Error getting current branch");
        return;
    };
    if !git_step("checking out master", &["checkout", "master"]) {
        return;
    }
    if !git_step("squash merging", &["merge", "--squash", &branch]) {
        return;
    }
    if !git_step("committing squash merge", &["commit", "-m", &message]) {
        return;
    }
    if !git_step("deleting branch", &["branch", "-D", &branch]) {
        return;
    }
    println!("Operations completed successfully.");
}

#[cfg(test)]
mod tests {
    #[test]
    fn prints_are_commented() {
        assert_eq!(
            super::comment_out_prints("x = 1\n    print(x)\nprint (y)"),
            "x = 1\n    # print(x)\n# print (y)"
        );
    }
}
