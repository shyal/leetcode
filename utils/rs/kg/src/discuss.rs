// The Discussion tab's verdict on a problem: why the crowd dislikes it.
// kg_discuss pulls the most upvoted comments under a problem, asks a
// model which of them complain about the statement itself, and files the
// answer in data/discuss_verdicts.json (not checked in). It is read on
// demand (`make discuss 1733`); the picker ranks on the like and dislike
// counts instead (crowd.rs says why), so nothing here enters a pick.
//
// The comments come from the two GraphQL calls the Discussion tab makes:
// questionDiscussionTopic gives the topic id, topicComments pages the
// comments by votes. Neither needs a login (checked 2026-10-13).

use std::path::Path;

use serde_json::{json, Map, Value};

use crate::crowd::{graphql, wilson_lower};
use crate::data::read_json;
use crate::llm::{claude_json, LlmError};

pub const FILE: &str = "data/discuss_verdicts.json";
/// The model LM Studio has loaded here; DISCUSS_MODEL overrides it.
pub const DEFAULT_MODEL: &str = "qwen/qwen3.8-27b";
/// How many comments the model reads, most upvoted first.
pub const COMMENTS: usize = 15;
/// One comment is cut here: a long comment is a solution writeup, and
/// its first lines say what it is.
const COMMENT_CHARS: usize = 600;

const TOPIC_QUERY: &str = "query q($slug: String!) { questionDiscussionTopic(questionSlug: $slug) { id topLevelCommentCount } }";
const COMMENTS_QUERY: &str = "query q($topicId: Int!, $orderBy: String, $pageNo: Int, $numPerPage: Int) { topicComments(topicId: $topicId, orderBy: $orderBy, pageNo: $pageNo, numPerPage: $numPerPage) { totalNum data { numChildren post { voteCount content author { username } } } } }";

pub const SYSTEM_PROMPT: &str = "You read the most upvoted comments under one LeetCode problem and sort them into complaints about the problem statement and everything else. The comments are numbered, most upvoted first.

A comment is a complaint about the statement when it says the statement is unclear, ambiguous, misleading or badly worded; that the examples or the constraints contradict the statement; that a rule had to be reverse engineered from failed test cases or from the answer; that the story hides what is actually asked; that the indexing convention is confusing; or that the intended solution rests on something the statement never says. A joke whose point is that the statement is unreadable is a complaint. A comment that explains what the statement really means, because the statement did not, is a complaint.

A comment is not a complaint when it says the problem is hard, that it has many edge cases, or that it is pointless; when the commenter failed it or asks for help; when it is a joke about something other than the wording, a solution, a hint, a list of test cases, praise, a defence of the problem, an interview report, or a complaint about the company tag, the difficulty label or premium. Nor is a complaint about the platform: a wrong or slow test case, a runtime error, an answer not accepted, the difficulty of testing the output, the type the input is given in (characters instead of integers, a jagged array, a pointer), or the function signature or code template of one language. Those are about the judge and the input format, not the statement.

Complaints about the statement: \"The list is not sorted! Please give a clarification!\" \"I couldn't figure out the meaning of the question even after I saw the answer.\" \"after reading this problem, i dont speak english anymore\" \"The description does not state that all interval starts are less or equal than their ends.\"

Not complaints about the statement: \"Why is '1' and '0' chars? Just to irritate people?\" \"Look at the example input, why is the output 7->0->8? How are those numbers calculated?\" \"The same solution that ran in 28ms a year ago takes 80ms now.\" \"Too many frustrating edge cases.\" \"No way this is a 'medium' task.\" \"Just got asked this in a Goldman Sachs interview.\" \"what's the purpose of examples #2 & #3?\"

Reply with one JSON object and nothing else:
{\"complaints\": [<the numbers of the comments that are complaints about the statement>], \"reason\": \"<one sentence>\"}

reason: one plain sentence naming what the complaints are about, or that there are none.";

/// The vote share, in percent, at which the verdict is "bad" and at
/// which it is "mixed"; below the second it is "good". "bad" is decided
/// on the lower bound of the share, not the share: the Wilson score
/// interval (crowd::wilson_lower, 95%) on the votes seen. A problem from
/// 2015 has thousands of votes and a problem from last month a few dozen,
/// so no vote count fits both; the interval narrows with each problem's
/// own crowd. 3 complaint votes of 5 is a share of 60 and a lower bound
/// of 23: "mixed". 600 of 1000 has a lower bound of 57: "bad".
pub const BAD_AT: i64 = 50;
pub const MIXED_AT: i64 = 20;

/// One top-level comment, as the model reads it.
#[derive(Debug, Clone)]
pub struct Comment {
    pub votes: i64,
    pub replies: i64,
    pub user: String,
    pub text: String,
}

/// A comment's text as the model should read it: the escapes LeetCode
/// stores undone, the whitespace collapsed, cut at COMMENT_CHARS.
fn clean(text: &str) -> String {
    let text = text.replace("\\'", "'").replace("\\\"", "\"");
    let joined = text.split_whitespace().collect::<Vec<_>>().join(" ");
    if joined.chars().count() <= COMMENT_CHARS {
        return joined;
    }
    let mut cut: String = joined.chars().take(COMMENT_CHARS).collect();
    cut.push_str(" [...]");
    cut
}

/// The `n` most upvoted top-level comments under the problem, and how
/// many top-level comments there are in all.
pub fn fetch_comments(slug: &str, n: usize) -> Result<(usize, Vec<Comment>), String> {
    let topic = graphql(TOPIC_QUERY, json!({"slug": slug}))?;
    let topic = &topic["questionDiscussionTopic"];
    let Some(id) = topic["id"].as_i64() else {
        return Err(format!("{slug}: no discussion topic"));
    };
    let total = topic["topLevelCommentCount"].as_u64().unwrap_or(0) as usize;
    if total == 0 {
        return Ok((0, vec![]));
    }
    let page = graphql(
        COMMENTS_QUERY,
        json!({"topicId": id, "orderBy": "most_votes", "pageNo": 1, "numPerPage": n}),
    )?;
    let comments = page["topicComments"]["data"]
        .as_array()
        .into_iter()
        .flatten()
        .map(|c| Comment {
            votes: c["post"]["voteCount"].as_i64().unwrap_or(0),
            replies: c["numChildren"].as_i64().unwrap_or(0),
            user: c["post"]["author"]["username"]
                .as_str()
                .unwrap_or("")
                .to_string(),
            text: clean(c["post"]["content"].as_str().unwrap_or("")),
        })
        .collect();
    Ok((total, comments))
}

/// The prompt for one problem: its name, acceptance, how many comments
/// the tab holds, and the comments read.
pub fn prompt(
    pnum: &str,
    title: &str,
    acceptance: f64,
    total: usize,
    comments: &[Comment],
) -> String {
    let mut out = format!(
        "Problem: {pnum}. {title}\nAcceptance: {acceptance:.0}%\nTop-level comments in all: {total}\n\nThe {} most upvoted:\n",
        comments.len()
    );
    for (i, c) in comments.iter().enumerate() {
        out.push_str(&format!(
            "\n{}. [{} votes, {} replies] {}:\n{}\n",
            i + 1,
            c.votes,
            c.replies,
            c.user,
            c.text
        ));
    }
    out
}

/// The verdict from the model's sorting: `unhappy` is the share of the
/// votes (percent) on the comments it called complaints; "bad" when the
/// share's lower bound (wilson_lower) reaches BAD_AT, "mixed" when the
/// share itself reaches MIXED_AT. The model sorts; the arithmetic is done
/// here, so a verdict can be checked against the comments it names.
pub fn verdict_of(comments: &[Comment], complaints: &[usize]) -> (String, i64) {
    let all: i64 = comments.iter().map(|c| c.votes.max(0)).sum();
    let against: i64 = complaints
        .iter()
        .filter_map(|&i| comments.get(i.wrapping_sub(1)))
        .map(|c| c.votes.max(0))
        .sum();
    let unhappy = if all == 0 {
        0
    } else {
        (100 * against + all / 2) / all
    };
    let lower = (100.0 * wilson_lower(against, all)).round() as i64;
    let verdict = if lower >= BAD_AT {
        "bad"
    } else if unhappy >= MIXED_AT {
        "mixed"
    } else {
        "good"
    };
    (verdict.to_string(), unhappy)
}

/// One verdict: the model sorts the comments, verdict_of scores them.
/// The entry carries the complaint numbers, so the sorting can be read
/// back against `top`.
pub fn judge(prompt: &str, comments: &[Comment], model: &str) -> Result<Value, LlmError> {
    let v = claude_json(prompt, SYSTEM_PROMPT, model, 2)?;
    let Some(list) = v["complaints"].as_array() else {
        return Err(LlmError::NotJson(format!(
            "complaints {:?}",
            v["complaints"]
        )));
    };
    let mut complaints: Vec<usize> = list
        .iter()
        .filter_map(|x| x.as_u64())
        .map(|x| x as usize)
        .filter(|&i| 1 <= i && i <= comments.len())
        .collect();
    complaints.sort_unstable();
    complaints.dedup();
    let (verdict, unhappy) = verdict_of(comments, &complaints);
    Ok(json!({
        "verdict": verdict,
        "unhappy": unhappy,
        "complaints": complaints,
        "reason": v["reason"].as_str().unwrap_or("").trim(),
    }))
}

/// data/discuss_verdicts.json: problem number -> its entry.
pub fn load(root: &Path) -> Map<String, Value> {
    read_json(&root.join(FILE))
        .and_then(|v| v.as_object().cloned())
        .unwrap_or_default()
}

pub fn save(root: &Path, verdicts: &Map<String, Value>) -> std::io::Result<()> {
    crate::pyjson::save(&root.join(FILE), &Value::Object(verdicts.clone()), Some(1))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn clean_undoes_escapes_and_cuts_long_text() {
        assert_eq!(clean("It\\'s   a\n\"test\\\"\""), "It's a \"test\"\"");
        let long = "x".repeat(COMMENT_CHARS + 50);
        let cut = clean(&long);
        assert!(cut.ends_with(" [...]"));
        assert_eq!(cut.chars().count(), COMMENT_CHARS + 6);
    }

    fn c(votes: i64) -> Comment {
        Comment {
            votes,
            replies: 0,
            user: String::new(),
            text: String::new(),
        }
    }

    #[test]
    fn verdict_follows_the_vote_share_of_the_complaints() {
        let cs = [c(600), c(300), c(100)];
        assert_eq!(verdict_of(&cs, &[1]), ("bad".into(), 60));
        assert_eq!(verdict_of(&cs, &[2]), ("mixed".into(), 30));
        assert_eq!(verdict_of(&cs, &[3]), ("good".into(), 10));
        // a number past the list, or 0, names no comment
        assert_eq!(verdict_of(&cs, &[0, 9]), ("good".into(), 0));
        assert_eq!(verdict_of(&[], &[1]), ("good".into(), 0));
        // the share alone is not enough: 3 of 5 votes stays "mixed", the
        // same share on a crowd is "bad"
        let few = [c(3), c(1), c(1)];
        assert_eq!(verdict_of(&few, &[1]), ("mixed".into(), 60));
        let crowd = [c(600), c(200), c(200)];
        assert_eq!(verdict_of(&crowd, &[1]), ("bad".into(), 60));
    }
}
