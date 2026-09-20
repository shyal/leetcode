//! The harness-helper check a prepared solve carries in its test block.
//!
//! A problem whose walk builds a graph from an edge list gets one line,
//! `assert uses(Solution, adjacency, ...)`, commented out with the other
//! asserts. Uncommenting the block runs it under `make`; `make submit`
//! never sends a top-level assert, so leetcode never sees it.

use kg::data::Problem;

/// Helper names the moves of a problem's walks call for, in the order
/// they go into the check line. Empty when none applies.
pub fn helpers_for(problem: &Problem) -> Vec<&'static str> {
    let moves = problem
        .moves
        .iter()
        .chain(problem.walks.iter().flat_map(|w| w.moves.iter()))
        .chain(problem.alt_walks.iter().flatten());
    let mut adjacency = false;
    let mut indegrees = false;
    for m in moves {
        match m.as_str() {
            "graph-adjacency-build" => adjacency = true,
            "topological-order" => {
                adjacency = true;
                indegrees = true;
            }
            _ => {}
        }
    }
    let mut out = vec![];
    if adjacency {
        out.push("adjacency");
    }
    if indegrees {
        out.push("indegrees");
    }
    out
}

/// `stub` with the check line for `helpers` added, commented, at the head
/// of the test block (before the first commented assert), or at the end
/// when the stub has none. Unchanged for no helpers.
pub fn with_uses_line(stub: &str, helpers: &[&str]) -> String {
    if helpers.is_empty() {
        return stub.to_string();
    }
    let line = format!("# assert uses(Solution, {})", helpers.join(", "));
    let mut lines: Vec<&str> = stub.lines().collect();
    match lines.iter().position(|l| l.starts_with("# assert ")) {
        Some(i) => lines.insert(i, &line),
        None => lines.push(&line),
    }
    format!("{}\n", lines.join("\n").trim_end())
}

#[cfg(test)]
mod tests {
    use super::*;
    use kg::data::Walk;

    fn problem(moves: &[&str], walk: &[&str]) -> Problem {
        Problem {
            moves: moves.iter().map(|s| s.to_string()).collect(),
            walks: vec![Walk {
                moves: walk.iter().map(|s| s.to_string()).collect(),
                ..Default::default()
            }],
            ..Default::default()
        }
    }

    #[test]
    fn adjacency_build_asks_for_adjacency_only() {
        let p = problem(&["graph-adjacency-build", "graph-bfs-shortest"], &[]);
        assert_eq!(helpers_for(&p), vec!["adjacency"]);
    }

    #[test]
    fn topological_order_asks_for_both_even_from_a_drafted_walk() {
        let p = problem(&[], &["topological-order"]);
        assert_eq!(helpers_for(&p), vec!["adjacency", "indegrees"]);
    }

    #[test]
    fn other_walks_ask_for_nothing() {
        let p = problem(&["two-pointers"], &["prefix-sum"]);
        assert!(helpers_for(&p).is_empty());
        assert_eq!(with_uses_line("x = 1\n", &helpers_for(&p)), "x = 1\n");
    }

    #[test]
    fn line_goes_ahead_of_the_first_commented_assert() {
        let stub = "class Solution:\n    def f(self, e):\n        pass\n\n\nsol = Solution()\n\nprint(sol.f([[0, 1]]))  # 1\n\n# assert sol.f([[0, 1]]) == 1\n# assert sol.f([]) == 0\n";
        let out = with_uses_line(stub, &["adjacency", "indegrees"]);
        assert!(out.contains(
            "print(sol.f([[0, 1]]))  # 1\n\n# assert uses(Solution, adjacency, indegrees)\n# assert sol.f([[0, 1]]) == 1\n"
        ));
    }

    #[test]
    fn line_goes_last_when_the_stub_has_no_asserts() {
        assert_eq!(
            with_uses_line("sol = Solution()\n", &["adjacency"]),
            "sol = Solution()\n# assert uses(Solution, adjacency)\n"
        );
    }
}
