// tle - fold the case that timed out on leetcode into the problem's cached
// asserts.
//
//   tle                  # ./tle, for the problem on the branch
//   tle 3841             # ./tle, for that problem
//   tle --file PATH      # another file
//   tle lc               # no file: the last Time Limit Exceeded submission
//                        # on leetcode, its input and its expected output
//
// The file is leetcode's "Last Executed Input": one line per argument in
// signature order, or `name = value` lines in any order, each a json or
// Python literal; an `expected = ...` line may follow. The reference
// solution in .prepare_cache/<num>.json runs on the arguments (the best of
// three timings; its answer is checked against the expected output when
// one is given), and the arguments, the answer and the seconds land in
// .prepare_cache/<num>.tle.json. One line, `assert tle(sol.<method>, <num>)`,
// joins the cached solution and its stub, and current.py and current.mu
// when the branch is the problem's. assert_utils.tle runs the case and
// allows TLE_SLACK times the reference's seconds.

use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::Duration;

use kg::data::{load_envrc, repo_root};
use kg::lc::{graphql, slug_of};
use prepare::stub::strip_solution;
use prepare::{cache_entry, pyrun, write_entry, CACHE_DIR};
use serde_json::{json, Value};

const RUNNER: &str = include_str!("../run.py.in");
const MARK: &str = "__TLE_CASE__";

/// Submissions listed per page; a Time Limit Exceeded older than this many
/// is not the one being worked on.
const SUBMISSIONS: usize = 20;

const LIST_QUERY: &str = "query l($slug: String!, $limit: Int!) { questionSubmissionList(offset: 0, limit: $limit, questionSlug: $slug) { submissions { id statusDisplay } } }";
const DETAILS_QUERY: &str =
    "query d($id: Int!) { submissionDetails(submissionId: $id) { lastTestcase expectedOutput } }";

struct Args {
    num: Option<String>,
    file: Option<PathBuf>,
    lc: bool,
}

fn usage() -> ! {
    eprintln!(
        "usage: tle [--file PATH | lc] [num]\n\n  num     the problem; the branch's number when absent\n  --file  the case as leetcode shows it (default ./tle)\n  lc      fetch the last Time Limit Exceeded submission from leetcode"
    );
    std::process::exit(2)
}

fn parse_args() -> Args {
    let mut args = Args {
        num: None,
        file: None,
        lc: false,
    };
    let mut it = std::env::args().skip(1);
    while let Some(a) = it.next() {
        match a.as_str() {
            "-h" | "--help" => usage(),
            "--file" => args.file = Some(PathBuf::from(it.next().unwrap_or_else(|| usage()))),
            "lc" => args.lc = true,
            _ if a.starts_with('-') => usage(),
            _ if a.chars().all(|c| c.is_ascii_digit()) => args.num = Some(a),
            _ => usage(),
        }
    }
    args
}

/// The branch's name when it is a problem number.
fn branch_number(root: &Path) -> Option<String> {
    let out = Command::new("git")
        .args(["rev-parse", "--abbrev-ref", "HEAD"])
        .current_dir(root)
        .output()
        .ok()?;
    let name = String::from_utf8_lossy(&out.stdout).trim().to_string();
    (!name.is_empty() && name.chars().all(|c| c.is_ascii_digit())).then_some(name)
}

/// The case as (parameter name or None, literal text) lines, and the
/// expected output when a line names it.
#[derive(Debug, Default, PartialEq)]
struct Case {
    params: Vec<(Option<String>, String)>,
    expected: Option<String>,
}

/// `name = value` lines in any order, or bare values in signature order
/// (leetcode's "Last Executed Input"); `expected = ...` or `output = ...`
/// is the answer.
fn parse_case(text: &str) -> Result<Case, String> {
    let mut case = Case::default();
    for line in text.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        let named = line
            .split_once('=')
            .filter(|(name, _)| {
                let name = name.trim();
                !name.is_empty()
                    && name.chars().all(|c| c.is_alphanumeric() || c == '_')
                    && !line[name.len()..].starts_with("==")
            })
            .map(|(name, value)| (name.trim().to_string(), value.trim().to_string()));
        match named {
            Some((name, value)) if name == "expected" || name == "output" => {
                case.expected = Some(value)
            }
            Some((name, value)) => case.params.push((Some(name), value)),
            None => case.params.push((None, line.to_string())),
        }
    }
    if case.params.is_empty() {
        return Err("the case has no arguments".into());
    }
    Ok(case)
}

/// The last Time Limit Exceeded submission's input and expected output,
/// as a case, with the submission id.
fn fetch_case(slug: &str) -> Result<(Case, u64), String> {
    let (status, data) = graphql(LIST_QUERY, json!({"slug": slug, "limit": SUBMISSIONS}))?;
    if status != 200 {
        return Err(format!("leetcode: http {status}"));
    }
    let subs = data["questionSubmissionList"]["submissions"]
        .as_array()
        .cloned()
        .unwrap_or_default();
    let id = subs
        .iter()
        .find(|s| s["statusDisplay"].as_str() == Some("Time Limit Exceeded"))
        .and_then(|s| s["id"].as_str())
        .and_then(|s| s.parse::<u64>().ok())
        .ok_or_else(|| {
            format!("no Time Limit Exceeded among the last {SUBMISSIONS} submissions of {slug}")
        })?;
    let (status, data) = graphql(DETAILS_QUERY, json!({"id": id}))?;
    if status != 200 {
        return Err(format!("leetcode: http {status}"));
    }
    let details = &data["submissionDetails"];
    let input = details["lastTestcase"].as_str().unwrap_or("");
    let mut case = parse_case(input)?;
    case.expected = details["expectedOutput"]
        .as_str()
        .filter(|s| !s.is_empty())
        .map(str::to_string);
    Ok((case, id))
}

/// The reference's class, without its demo and asserts.
fn class_part(solution: &str) -> &str {
    match solution.find("\nsol = Solution()") {
        Some(i) => &solution[..i],
        None => solution,
    }
}

/// Run the reference on the case: the frozen case as json.
fn freeze(root: &Path, solution: &str, case: &Case) -> Result<Value, String> {
    let case_json = json!({
        "params": case.params.iter().map(|(n, v)| json!([n, v])).collect::<Vec<_>>(),
        "expected": case.expected,
    });
    let literal = serde_json::to_string(&case_json.to_string()).unwrap();
    let code = format!(
        "{}\n\n{}",
        class_part(solution),
        RUNNER.replace("__CASE__", &literal)
    );
    let out = pyrun::run(root, &code, Duration::from_secs(600));
    if out.timed_out {
        return Err("the reference solution did not finish in 600 s".into());
    }
    let line = out
        .output
        .lines()
        .rev()
        .find_map(|l| l.strip_prefix(MARK))
        .ok_or_else(|| format!("the reference solution failed:\n{}", out.output))?;
    let frozen: Value = serde_json::from_str(line).map_err(|e| e.to_string())?;
    if let Some(e) = frozen["error"].as_str() {
        return Err(e.to_string());
    }
    Ok(frozen)
}

fn assert_line(method: &str, num: &str) -> String {
    format!("assert tle(sol.{method}, {num})")
}

/// `text` with the assert appended (commented when `comment`), unchanged
/// when it already carries it.
fn with_assert(text: &str, line: &str, comment: bool) -> String {
    if text
        .lines()
        .any(|l| l.trim_start_matches(['#', ' ']).trim_end() == line)
    {
        return text.to_string();
    }
    let mut out = text.trim_end_matches('\n').to_string();
    if !out.is_empty() {
        out.push('\n');
    }
    if comment {
        out.push_str("# ");
    }
    out.push_str(line);
    out.push('\n');
    out
}

fn append_if_present(path: &Path, line: &str, comment: bool) -> bool {
    let Ok(text) = std::fs::read_to_string(path) else {
        return false;
    };
    let new = with_assert(&text, line, comment);
    if new != text {
        std::fs::write(path, new).expect("write current file");
    }
    true
}

fn run(args: &Args) -> Result<(), String> {
    let root = repo_root();
    load_envrc(&root);
    let num = args
        .num
        .clone()
        .or_else(|| branch_number(&root))
        .ok_or("no problem: give its number, or run on its branch")?;
    let mut entry = cache_entry(&root, &num).ok_or_else(|| format!("no cache entry for {num}"))?;
    let solution = entry["solution"].as_str().unwrap_or("").to_string();
    if solution.is_empty() {
        return Err(format!("{num}: the cache has no reference solution"));
    }
    let (case, source) = if args.lc {
        let slug = slug_of(&solution).ok_or_else(|| format!("{num}: no URL line in the cache"))?;
        let (case, id) = fetch_case(&slug)?;
        (case, format!("leetcode submission {id}"))
    } else {
        let path = args.file.clone().unwrap_or_else(|| root.join("tle"));
        let text =
            std::fs::read_to_string(&path).map_err(|e| format!("{}: {e}", path.display()))?;
        (parse_case(&text)?, format!("file {}", path.display()))
    };
    let mut frozen = freeze(&root, &solution, &case)?;
    let method = frozen["method"].as_str().unwrap_or("").to_string();
    let shape = frozen["shape"].as_str().unwrap_or("").to_string();
    let seconds = frozen["seconds"].as_f64().unwrap_or(0.0);
    let answers = frozen["expected"].as_array().map(Vec::len);
    frozen.as_object_mut().unwrap().remove("shape");
    frozen["source"] = Value::String(source);
    let case_path = root.join(CACHE_DIR).join(format!("{num}.tle.json"));
    kg::pyjson::save(&case_path, &frozen, None).map_err(|e| e.to_string())?;

    let line = assert_line(&method, &num);
    let merged = with_assert(&solution, &line, false);
    if merged != solution {
        entry["code"] = Value::String(strip_solution(&merged)?);
        entry["solution"] = Value::String(merged);
        write_entry(&root, &num, &entry);
    }
    let mut touched = vec!["the cached solution and its stub".to_string()];
    if branch_number(&root).as_deref() == Some(num.as_str()) {
        for (name, comment) in [("current.py", true), ("current.mu", false)] {
            if append_if_present(&root.join(name), &line, comment) {
                touched.push(name.to_string());
            }
        }
    }
    let answers = match answers {
        Some(n) => format!(", {n} answers"),
        None => String::new(),
    };
    println!(
        "{num}: the case that timed out on leetcode is in {} ({shape}{answers}). The reference solution takes {seconds:.3} s. `{line}` is in {}.",
        case_path.strip_prefix(&root).unwrap_or(&case_path).display(),
        touched.join(", ")
    );
    Ok(())
}

fn main() {
    let args = parse_args();
    if let Err(e) = run(&args) {
        eprintln!("tle: {e}");
        std::process::exit(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn named_lines_in_any_order_with_an_expected() {
        let case = parse_case("s = \"abc\"\nn = 3\n\nexpected = [true]\n").unwrap();
        assert_eq!(
            case.params,
            vec![
                (Some("s".into()), "\"abc\"".into()),
                (Some("n".into()), "3".into())
            ]
        );
        assert_eq!(case.expected.as_deref(), Some("[true]"));
    }

    #[test]
    fn bare_lines_are_positional() {
        let case = parse_case("6\n[[0,1]]\n\"ab\"\n").unwrap();
        assert_eq!(case.params.len(), 3);
        assert!(case.params.iter().all(|(n, _)| n.is_none()));
        assert_eq!(case.expected, None);
    }

    #[test]
    fn a_value_with_an_equals_sign_is_not_a_name() {
        let case = parse_case("[\"a==b\"]\n").unwrap();
        assert_eq!(case.params, vec![(None, "[\"a==b\"]".into())]);
        assert!(parse_case("\n").is_err());
    }

    #[test]
    fn the_assert_joins_once_commented_or_live() {
        let line = assert_line("f", "7");
        assert_eq!(line, "assert tle(sol.f, 7)");
        let live = with_assert("x = 1\n", &line, false);
        assert_eq!(live, "x = 1\nassert tle(sol.f, 7)\n");
        assert_eq!(with_assert(&live, &line, false), live);
        let stub = with_assert("# assert f()\n", &line, true);
        assert_eq!(stub, "# assert f()\n# assert tle(sol.f, 7)\n");
        assert_eq!(with_assert(&stub, &line, true), stub);
        assert_eq!(with_assert(&stub, &line, false), stub);
    }

    #[test]
    fn the_class_part_stops_before_the_demo() {
        assert_eq!(
            class_part("class A:\n    pass\n\n\nsol = Solution()\nprint(1)\n"),
            "class A:\n    pass\n\n"
        );
        assert_eq!(class_part("class A:\n    pass\n"), "class A:\n    pass\n");
    }
}
