// lc_solutions - top community solutions for a problem, straight from
// leetcode's graphql (the Solutions tab, not the editorial). No auth needed.
//
//   lc_solutions 543                 # list top-voted solutions
//   lc_solutions 543 -n 10           # list more
//   lc_solutions 543 --read 1        # print the #1 solution's markdown
//   lc_solutions 543 --read 1-3      # print solutions 1 to 3
//   lc_solutions 543 --tag python3   # only solutions tagged python3
//   lc_solutions 543 --order HOT     # default is MOST_VOTES
//   lc_solutions diameter-of-binary-tree   # slug instead of number
//   lc_solutions --author StefanPochmann        # a user's articles
//   lc_solutions 84 --author StefanPochmann --read 1   # his take on 84
//
// Every --read is also saved under research/lc-solutions/<num>/ so the
// offline cache accumulates as it gets used.
//
// Ported from utils/kg/lc_solutions (Python) on 2026-09-12.

use std::path::{Path, PathBuf};

use kg::data::repo_root;
use kg::pyjson;
use regex::Regex;
use serde_json::{json, Value};

const UA: &str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36";

const LIST_QUERY: &str = "\nquery ugcArticleSolutionArticles($questionSlug: String!, $orderBy: ArticleOrderByEnum,\n    $userInput: String, $tagSlugs: [String!], $skip: Int, $first: Int) {\n  ugcArticleSolutionArticles(questionSlug: $questionSlug, orderBy: $orderBy,\n      userInput: $userInput, tagSlugs: $tagSlugs, skip: $skip, first: $first) {\n    totalNum\n    edges { node {\n      title topicId hitCount\n      author { userName }\n      reactions { count reactionType }\n      tags { slug }\n    } }\n  }\n}\n";
const AUTHOR_QUERY: &str = "\nquery ugcArticleUserSolutionArticles($username: String!, $skip: Int, $first: Int) {\n  ugcArticleUserSolutionArticles(username: $username, skip: $skip, first: $first) {\n    totalNum\n    edges { node {\n      title topicId hitCount questionSlug\n      reactions { count reactionType }\n    } }\n  }\n}\n";
const ARTICLE_QUERY: &str = "\nquery ugcArticleSolutionArticle($topicId: ID) {\n  ugcArticleSolutionArticle(topicId: $topicId) {\n    title content author { userName } createdAt\n  }\n}\n";

fn die(msg: &str) -> ! {
    eprintln!("{msg}");
    std::process::exit(1)
}

fn graphql(query: &str, variables: Value) -> Value {
    let mut resp = ureq::post("https://leetcode.com/graphql/")
        .header("Content-Type", "application/json")
        .header("User-Agent", UA)
        .send_json(json!({"query": query, "variables": variables}))
        .unwrap_or_else(|e| die(&format!("graphql: {e}")));
    let data: Value = resp
        .body_mut()
        .read_json()
        .unwrap_or_else(|e| die(&format!("graphql: {e}")));
    if let Some(errs) = data
        .get("errors")
        .and_then(Value::as_array)
        .filter(|a| !a.is_empty())
    {
        die(&format!(
            "graphql error: {}",
            errs[0]
                .get("message")
                .and_then(Value::as_str)
                .unwrap_or("None")
        ));
    }
    data["data"].clone()
}

fn resolve_slug(root: &Path, problem: &str) -> String {
    if !problem.chars().all(|c| c.is_ascii_digit()) {
        return problem.to_string();
    }
    let cache = root.join("research/.lc_slugs.json");
    let mut slugs = pyjson::load(&cache).unwrap_or_else(|| json!({}));
    if slugs.get(problem).is_none() {
        let mut resp = ureq::get("https://leetcode.com/api/problems/all/")
            .header("User-Agent", UA)
            .call()
            .unwrap_or_else(|e| die(&format!("leetcode: {e}")));
        let listing: Value = resp
            .body_mut()
            .read_json()
            .unwrap_or_else(|e| die(&format!("leetcode: {e}")));
        let mut table = serde_json::Map::new();
        for p in listing["stat_status_pairs"]
            .as_array()
            .into_iter()
            .flatten()
        {
            let id = kg::data::value_str(&p["stat"]["frontend_question_id"]);
            table.insert(id, p["stat"]["question__title_slug"].clone());
        }
        slugs = Value::Object(table);
        let _ = std::fs::create_dir_all(cache.parent().unwrap());
        let _ = pyjson::save(&cache, &slugs, None);
    }
    match slugs.get(problem).and_then(Value::as_str) {
        Some(s) => s.to_string(),
        None => die(&format!("no slug found for problem {problem}")),
    }
}

fn upvotes(node: &Value) -> i64 {
    node["reactions"]
        .as_array()
        .into_iter()
        .flatten()
        .find(|r| r["reactionType"].as_str() == Some("UPVOTE"))
        .and_then(|r| r["count"].as_i64())
        .unwrap_or(0)
}

fn fetch_list(
    slug: &str,
    order: &str,
    tags: &[String],
    n: i64,
    search: Option<&str>,
) -> (i64, Vec<Value>) {
    let data = graphql(
        LIST_QUERY,
        json!({
            "questionSlug": slug,
            "orderBy": order,
            "userInput": search,
            "tagSlugs": if tags.is_empty() { Value::Null } else { json!(tags) },
            "skip": 0,
            "first": n,
        }),
    );
    let b = &data["ugcArticleSolutionArticles"];
    (
        b["totalNum"].as_i64().unwrap_or(0),
        b["edges"]
            .as_array()
            .into_iter()
            .flatten()
            .map(|e| e["node"].clone())
            .collect(),
    )
}

fn fetch_author(username: &str, slug: Option<&str>) -> (i64, Vec<Value>) {
    let first = 1000;
    let mut data = graphql(
        AUTHOR_QUERY,
        json!({"username": username, "skip": 0, "first": first}),
    );
    let mut total = data["ugcArticleUserSolutionArticles"]["totalNum"]
        .as_i64()
        .unwrap_or(0);
    if total > first {
        data = graphql(
            AUTHOR_QUERY,
            json!({"username": username, "skip": 0, "first": total}),
        );
        total = data["ugcArticleUserSolutionArticles"]["totalNum"]
            .as_i64()
            .unwrap_or(0);
    }
    let mut nodes: Vec<Value> = data["ugcArticleUserSolutionArticles"]["edges"]
        .as_array()
        .into_iter()
        .flatten()
        .map(|e| e["node"].clone())
        .collect();
    if let Some(s) = slug {
        nodes.retain(|n| n["questionSlug"].as_str() == Some(s));
    }
    (total, nodes)
}

fn parse_ranks(spec: &str, upper: usize) -> std::ops::RangeInclusive<usize> {
    let re = Regex::new(r"^(\d+)(?:-(\d+))?$").unwrap();
    let Some(m) = re.captures(spec) else {
        die(&format!("bad --read spec: {spec}"))
    };
    let lo: usize = m[1].parse().unwrap();
    let hi: usize = m.get(2).map(|x| x.as_str().parse().unwrap()).unwrap_or(lo);
    if !(1 <= lo && lo <= hi && hi <= upper) {
        die(&format!("--read {spec} out of range 1..{upper}"));
    }
    lo..=hi
}

fn save_copy(
    root: &Path,
    problem: Option<&str>,
    slug: &str,
    node: &Value,
    content: &str,
) -> PathBuf {
    let num = problem
        .filter(|p| p.chars().all(|c| c.is_ascii_digit()))
        .unwrap_or("");
    let dir = root.join("research/lc-solutions").join(if num.is_empty() {
        slug.to_string()
    } else {
        format!("{:0>4}.{slug}", num)
    });
    let _ = std::fs::create_dir_all(&dir);
    let path = dir.join(format!("{}.md", kg::data::value_str(&node["topicId"])));
    let text = format!(
        "# {}\n\ntopic {}, {} upvotes\n\n{content}",
        node["title"].as_str().unwrap_or(""),
        kg::data::value_str(&node["topicId"]),
        upvotes(node)
    );
    let _ = std::fs::write(&path, text);
    path
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let (mut problem, mut n, mut read, mut order, mut tags, mut search, mut author) = (
        None::<String>,
        5i64,
        None::<String>,
        "MOST_VOTES".to_string(),
        Vec::<String>::new(),
        None::<String>,
        None::<String>,
    );
    let mut i = 0;
    let usage = "usage: lc_solutions [-h] [-n N] [--read READ] [--order {MOST_VOTES,HOT,MOST_RECENT}] [--tag TAG] [--search SEARCH] [--author AUTHOR] [problem]";
    while i < args.len() {
        let a = args[i].as_str();
        let mut value = || {
            i += 1;
            args.get(i).cloned().unwrap_or_else(|| {
                eprintln!("{usage}");
                std::process::exit(2)
            })
        };
        match a {
            "-h" | "--help" => {
                println!("{usage}");
                return;
            }
            "-n" => n = value().parse().unwrap_or(5),
            "--read" => read = Some(value()),
            "--order" => {
                order = value();
                if !["MOST_VOTES", "HOT", "MOST_RECENT"].contains(&order.as_str()) {
                    eprintln!(
                        "{usage}\nlc_solutions: error: argument --order: invalid choice: '{order}'"
                    );
                    std::process::exit(2);
                }
            }
            "--tag" => tags.push(value()),
            "--search" => search = Some(value()),
            "--author" => author = Some(value()),
            _ if problem.is_none() && !a.starts_with('-') => problem = Some(a.to_string()),
            _ => {
                eprintln!("{usage}");
                std::process::exit(2);
            }
        }
        i += 1;
    }
    if problem.is_none() && author.is_none() {
        eprintln!("{usage}\nlc_solutions: error: need a problem, an --author, or both");
        std::process::exit(2);
    }
    let root = repo_root();
    let slug = problem.as_deref().map(|p| resolve_slug(&root, p));
    let nodes: Vec<Value>;
    if let Some(user) = &author {
        let (total, mut ns) = fetch_author(user, slug.as_deref());
        let scope = match &slug {
            Some(s) => format!("{user} on {s}"),
            None => format!("{user}, most recent"),
        };
        if slug.is_none() {
            let want = read
                .as_deref()
                .map(|r| *parse_ranks(r, 1000).end())
                .unwrap_or(0)
                .max(n as usize);
            ns.truncate(want);
        }
        println!("{scope}: {} of {total} articles", ns.len());
        nodes = ns;
    } else {
        let want = read
            .as_deref()
            .map(|r| *parse_ranks(r, 100).end())
            .unwrap_or(0)
            .max(n as usize);
        let (total, ns) = fetch_list(
            slug.as_deref().unwrap(),
            &order,
            &tags,
            want as i64,
            search.as_deref(),
        );
        if read.is_none() {
            println!(
                "{}: {total} solutions, top {} by {order}",
                slug.as_deref().unwrap(),
                ns.len()
            );
        }
        nodes = ns;
    }
    let Some(spec) = read else {
        for (i, node) in nodes.iter().enumerate() {
            let a = node["author"]["userName"]
                .as_str()
                .map(String::from)
                .unwrap_or_else(|| author.clone().unwrap_or_else(|| "?".to_string()));
            let whereabouts = node["questionSlug"]
                .as_str()
                .map(|s| format!(", {s}"))
                .unwrap_or_default();
            println!(
                "{:>2}. [{:>5} up, {:>7} views] {}  ({a}, topic {}{whereabouts})",
                i + 1,
                upvotes(node),
                node["hitCount"].as_i64().unwrap_or(0),
                node["title"].as_str().unwrap_or(""),
                kg::data::value_str(&node["topicId"])
            );
        }
        return;
    };
    for rank in parse_ranks(&spec, nodes.len()) {
        let node = &nodes[rank - 1];
        let art = graphql(ARTICLE_QUERY, json!({"topicId": node["topicId"]}))
            ["ugcArticleSolutionArticle"]
            .clone();
        let nslug = node["questionSlug"]
            .as_str()
            .map(String::from)
            .or_else(|| slug.clone())
            .unwrap_or_default();
        let content = art["content"].as_str().unwrap_or("");
        let path = save_copy(&root, problem.as_deref(), &nslug, node, content);
        println!("\n{}", "=".repeat(72));
        println!(
            "#{rank}: {}  [{} upvotes, saved {}]",
            art["title"].as_str().unwrap_or(""),
            upvotes(node),
            path.strip_prefix(&root).unwrap_or(&path).display()
        );
        println!("{}", "=".repeat(72));
        println!("{content}");
    }
}
