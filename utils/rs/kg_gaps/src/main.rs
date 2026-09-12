// kg_gaps - what the taxonomy is still blind to, ranked.
//
//   kg_gaps            # top 25
//   kg_gaps --all
//
// Reads the missing-move suggestions the walk drafter emitted into the
// drafted walks in graph/problems.json (phase 3 of PLAN.md). For each
// suggested move: mentions = how many predicted walks asked for it; sole
// blocker = problems whose known moves are all SOLID today and which are
// blocked ONLY by this one absent node - the unlock count if it entered the
// taxonomy and got trained. Suggestions starting with 'brute-force' are
// one bucket: they mean 'no technique needed', not a node.
//
// Ported from utils/kg/kg_gaps (Python) on 2026-09-12.

use std::collections::{BTreeSet, HashMap};

use kg::ctx::Ctx;
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::status::{all_statuses, SOLID};

fn norm(name: &str) -> String {
    let name = name.trim().to_lowercase().replace(' ', "-");
    if name.starts_with("brute-force") {
        "brute-force".to_string()
    } else {
        name
    }
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_gaps [--all]\n\n  --all  Print every suggestion.");
        return;
    }
    let all = args.iter().any(|a| a == "--all");
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let ev = Evidence::new(recs);
    let statuses = all_statuses(&ctx, &ev, ctx.today());

    let mut mentions: HashMap<String, usize> = HashMap::new();
    let mut sole: HashMap<String, Vec<String>> = HashMap::new();
    for (num, prob) in &ctx.predicted {
        for walk in &prob.walks {
            let missing: BTreeSet<String> = walk.missing_names.iter().map(|m| norm(m)).collect();
            for m in &missing {
                *mentions.entry(m.clone()).or_insert(0) += 1;
            }
            if missing.len() == 1
                && !walk.moves.is_empty()
                && walk
                    .moves
                    .iter()
                    .all(|mv| statuses.get(mv).is_some_and(|s| s.0 == SOLID))
            {
                sole.entry(missing.iter().next().unwrap().clone())
                    .or_default()
                    .push(num.clone());
            }
        }
    }
    let unlocks = |m: &String| sole.get(m).map_or(0, Vec::len);
    let mut ranked: Vec<&String> = mentions.keys().collect();
    ranked.sort_by(|a, b| {
        (-(unlocks(a) as i64), -(mentions[*a] as i64), a.as_str()).cmp(&(
            -(unlocks(b) as i64),
            -(mentions[*b] as i64),
            b.as_str(),
        ))
    });
    if !all {
        ranked.truncate(25);
    }
    println!(
        "{:<34} {:>7} {:>8}  examples",
        "suggested move", "unlocks", "mentions"
    );
    for m in &ranked {
        let ex: Vec<&str> = sole
            .get(*m)
            .map(|v| v.iter().take(5).map(String::as_str).collect())
            .unwrap_or_default();
        println!(
            "{m:<34} {:>7} {:>8}  {}",
            unlocks(m),
            mentions[*m],
            ex.join(", ")
        );
    }
    let total: usize = sole.values().map(Vec::len).sum();
    println!(
        "\n{} distinct suggestions; {total} problems blocked by exactly one absent node with everything else solid",
        mentions.len()
    );
}
