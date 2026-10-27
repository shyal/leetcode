// The contests: contests/*.json, one file per LeetCode contest sat, virtual
// or real. The JSON is the record; the markdown beside it (same stem, .md)
// holds the write-up, and kg_readme renders the header and the result
// table into the markdown's <!-- CONTEST --> region from the JSON
// (2026-10-27). Nothing reads the markdown back.
//
// Each problem is a first-sight game against its rating (model::FirstSight):
// accepted without help scores 1, accepted after a hint 0.5 (the proven
// rating's score for a pass short of a cold win, model::proven_game_score),
// not accepted 0. The result column is derived from the same fields, so
// the table and the score cannot disagree.

use std::path::{Path, PathBuf};

use chrono::NaiveDate;
use serde_json::Value;

use crate::model::FirstSight;

/// LeetCode's penalty per wrong submission, in minutes.
pub const PENALTY_MIN: i64 = 5;

/// The region of the contest markdown that is rendered from the JSON.
pub const REGION: &str = "CONTEST";

#[derive(Debug, Clone, PartialEq)]
pub struct Problem {
    pub slot: String,
    pub problem: String,
    pub name: String,
    pub rating: f64,
    /// wall clock of the accepted submission, None when never accepted
    pub accepted_at: Option<String>,
    pub wrong: i64,
    /// "none" or "hint"
    pub assist: String,
    pub note: Option<String>,
}

impl Problem {
    /// The game's score: 1 cold, 0.5 after a hint, 0 not accepted.
    pub fn score(&self) -> f64 {
        match (&self.accepted_at, self.assist.as_str()) {
            (None, _) => 0.0,
            (Some(_), "none") => 1.0,
            (Some(_), _) => 0.5,
        }
    }

    /// The result column: the verdict, then the note after a colon.
    pub fn result(&self) -> String {
        let verdict = match (&self.accepted_at, self.assist.as_str(), self.wrong) {
            (Some(_), "none", _) => "solved, no help",
            (Some(_), _, _) => "solved with help",
            (None, _, 0) => "not attempted",
            (None, _, _) => "failed",
        };
        match &self.note {
            Some(n) => format!("{verdict}: {n}"),
            None => verdict.to_string(),
        }
    }

    /// The penalty column: "-" or "5 min (1 wrong)".
    pub fn penalty(&self) -> String {
        if self.wrong == 0 {
            "-".to_string()
        } else {
            format!("{} min ({} wrong)", self.wrong * PENALTY_MIN, self.wrong)
        }
    }

    /// "4092. Binary Digit Score"
    pub fn title(&self) -> String {
        format!("{}. {}", self.problem, self.name)
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Contest {
    /// the JSON file
    pub path: PathBuf,
    pub contest: String,
    /// LeetCode's slug, "weekly-contest-525"; the field is sampled by it
    pub slug: String,
    pub virtual_: bool,
    pub date: NaiveDate,
    pub clock_min: i64,
    pub rank: i64,
    pub field: i64,
    pub solved_all: i64,
    pub score: i64,
    pub score_max: i64,
    pub finish: String,
    pub languages: String,
    pub ratings: String,
    pub intro: Option<String>,
    pub problems: Vec<Problem>,
}

fn s(v: &Value, k: &str) -> String {
    v[k].as_str().unwrap_or("").to_string()
}

fn i(v: &Value, k: &str) -> i64 {
    v[k].as_i64().unwrap_or(0)
}

fn opt(v: &Value, k: &str) -> Option<String> {
    v[k].as_str().map(str::to_string)
}

impl Contest {
    pub fn from_json(path: &Path, v: &Value) -> Contest {
        let problems = v["problems"]
            .as_array()
            .map(|ps| {
                ps.iter()
                    .map(|p| Problem {
                        slot: s(p, "slot"),
                        problem: s(p, "problem"),
                        name: s(p, "name"),
                        rating: p["rating"].as_f64().unwrap_or(0.0),
                        accepted_at: opt(p, "accepted_at"),
                        wrong: i(p, "wrong"),
                        assist: p["assist"].as_str().unwrap_or("none").to_string(),
                        note: opt(p, "note"),
                    })
                    .collect()
            })
            .unwrap_or_default();
        Contest {
            path: path.to_path_buf(),
            contest: s(v, "contest"),
            slug: s(v, "slug"),
            virtual_: v["virtual"].as_bool().unwrap_or(false),
            date: NaiveDate::parse_from_str(&s(v, "date"), "%Y-%m-%d")
                .unwrap_or_else(|_| panic!("{}: date", path.display())),
            clock_min: i(v, "clock_min"),
            rank: i(v, "rank"),
            field: i(v, "field"),
            solved_all: i(v, "solved_all"),
            score: i(v, "score"),
            score_max: i(v, "score_max"),
            finish: s(v, "finish"),
            languages: s(v, "languages"),
            ratings: s(v, "ratings"),
            intro: opt(v, "intro"),
            problems,
        }
    }

    /// The markdown beside the JSON: same stem, .md.
    pub fn md_path(&self) -> PathBuf {
        self.path.with_extension("md")
    }

    /// "Weekly Contest 525 (virtual)"
    pub fn title(&self) -> String {
        if self.virtual_ {
            format!("{} (virtual)", self.contest)
        } else {
            self.contest.clone()
        }
    }

    /// One game per problem, on the contest's date.
    pub fn games(&self) -> Vec<FirstSight> {
        self.problems
            .iter()
            .map(|p| (self.date, p.rating, p.score()))
            .collect()
    }

    pub fn wrong(&self) -> i64 {
        self.problems.iter().map(|p| p.wrong).sum()
    }

    /// The header and the result table: the <!-- CONTEST --> region.
    pub fn markdown(&self) -> String {
        self.markdown_with(None)
    }

    /// The header with the rating line when the contest has a standing.
    pub fn markdown_with(&self, standing: Option<&Standing>) -> String {
        let mut out = vec![format!("# {}", self.title()), String::new()];
        if let Some(intro) = &self.intro {
            out.push(intro.clone());
            out.push(String::new());
        }
        out.push(format!("Date: {} (PHT)", self.date));
        out.push(format!("Clock: {} minutes", self.clock_min));
        let rank = if self.virtual_ {
            "Virtual rank"
        } else {
            "Rank"
        };
        out.push(format!(
            "{rank}: {} of {} ({} solved all {})",
            self.rank,
            thousands(self.field),
            self.solved_all,
            count_word(self.problems.len())
        ));
        out.push(format!("Score: {} of {}", self.score, self.score_max));
        if let Some(st) = standing {
            out.push(format!(
                "Rating: {} after this contest (performance {}, LeetCode's formula, {} rated of the {} participants)",
                st.rating.round() as i64,
                st.performance.round() as i64,
                thousands(st.sampled as i64),
                thousands(st.user_num)
            ));
        }
        let wrong = self.wrong();
        let penalty = match wrong {
            0 => String::new(),
            1 => format!(" (with {PENALTY_MIN} minutes of penalty for 1 wrong submission)"),
            n => format!(
                " (with {} minutes of penalty for {n} wrong submissions)",
                n * PENALTY_MIN
            ),
        };
        out.push(format!("Finish time: {}{penalty}", self.finish));
        out.push(format!("Language: {}", self.languages));
        if !self.ratings.is_empty() {
            out.push(format!("Ratings: {}", self.ratings));
        }
        out.push(String::new());
        let mut rows = vec![vec![
            "#".to_string(),
            "Problem".to_string(),
            "Rating".to_string(),
            "Accepted at".to_string(),
            "Penalty".to_string(),
            "Result".to_string(),
        ]];
        for p in &self.problems {
            rows.push(vec![
                p.slot.clone(),
                p.title(),
                rating_text(p.rating),
                p.accepted_at.clone().unwrap_or_else(|| "-".to_string()),
                p.penalty(),
                p.result(),
            ]);
        }
        out.extend(table(&rows));
        out.join("\n")
    }

    /// A fresh markdown for a contest without one: the region, a heading
    /// per problem and a Notes heading, for the write-up.
    pub fn fresh_markdown(&self) -> String {
        let mut out = format!(
            "<!-- {REGION} -->\n{}\n<!-- /{REGION} -->\n",
            self.markdown()
        );
        for p in &self.problems {
            out.push_str(&format!("\n## {}. {}\n", p.slot, p.title()));
        }
        out.push_str("\n## Notes\n");
        out
    }
}

/// 33050 -> "33,050"
pub fn thousands(n: i64) -> String {
    let digits = n.abs().to_string();
    let mut out = String::new();
    for (k, c) in digits.chars().enumerate() {
        if k > 0 && (digits.len() - k).is_multiple_of(3) {
            out.push(',');
        }
        out.push(c);
    }
    if n < 0 {
        format!("-{out}")
    } else {
        out
    }
}

/// "four" for the usual contest, the number otherwise.
fn count_word(n: usize) -> String {
    match n {
        1 => "one",
        2 => "two",
        3 => "three",
        4 => "four",
        5 => "five",
        6 => "six",
        _ => return n.to_string(),
    }
    .to_string()
}

/// A rating as the source wrote it: whole numbers without a decimal.
pub fn rating_text(r: f64) -> String {
    if r == r.trunc() {
        format!("{}", r as i64)
    } else {
        format!("{r:.1}")
    }
}

/// An aligned markdown table: the first row is the header.
pub fn table(rows: &[Vec<String>]) -> Vec<String> {
    let cols = rows[0].len();
    let widths: Vec<usize> = (0..cols)
        .map(|c| {
            rows.iter()
                .map(|r| r[c].chars().count())
                .max()
                .unwrap_or(0)
                .max(3)
        })
        .collect();
    let line = |r: &Vec<String>| {
        let cells: Vec<String> = r
            .iter()
            .zip(&widths)
            .map(|(c, w)| format!("{c:<w$}"))
            .collect();
        format!("| {} |", cells.join(" | "))
    };
    let mut out = vec![line(&rows[0])];
    out.push(format!(
        "| {} |",
        widths
            .iter()
            .map(|w| "-".repeat(*w))
            .collect::<Vec<_>>()
            .join(" | ")
    ));
    out.extend(rows[1..].iter().map(line));
    out
}

// ---- LeetCode's contest rating -----------------------------------------------
//
// LeetCode rates a contest in four steps (its 2020 post, as the open
// predictors implement it): the expected rank is one plus the sum over the
// field of each participant's chance of beating you under the Elo curve;
// the rank performed at is the geometric mean of the expected and the
// actual rank; the performance rating is the rating whose expected rank is
// that, found by binary search; and the rating moves towards it by
// 1 / (1 + sum_{i=0}^{k} (5/7)^i), k the contests attended before this one:
// half on a first contest, 2/9 in the limit. A participant with no contest
// history is rated 1500, the starting rating.
//
// LeetCode does not rate virtual contests. This applies its formula to the
// virtual rank against the real field: every rated participant at the
// rating they held before the contest, from CLIST's standings
// (contests/<stem>.field.json, utils/readme/contest_field.mjs), and the
// participants CLIST has no row for at RATING_START, as LeetCode rates a
// first contest.

/// The rating every participant starts at, and the rating of one with no
/// contest history.
pub const RATING_START: f64 = 1500.0;

/// The field of one contest, contests/<stem>.field.json.
#[derive(Debug, Clone, PartialEq)]
pub struct Field {
    /// participants in the contest, LeetCode's count
    pub user_num: i64,
    pub fetched: String,
    /// the rating of each rated participant before the contest
    pub ratings: Vec<f64>,
    /// how many participants had a rating: ratings.len()
    pub rated: usize,
}

impl Field {
    pub fn from_json(v: &Value) -> Option<Field> {
        let ratings: Vec<f64> = v["ratings"]
            .as_array()?
            .iter()
            .filter_map(Value::as_f64)
            .collect();
        if ratings.is_empty() {
            return None;
        }
        let user_num = v["user_num"].as_i64()?.max(ratings.len() as i64);
        Some(Field {
            user_num,
            fetched: s(v, "fetched"),
            rated: ratings.len(),
            ratings,
        })
    }

    /// 1 + the sum over the field of the chance each participant beats a
    /// rating of `me`: the rated participants at their rating before the
    /// contest, the rest at RATING_START.
    pub fn expected_rank(&self, me: f64) -> f64 {
        let rated: f64 = self.ratings.iter().map(|r| beats(*r, me)).sum();
        let unrated = (self.user_num - self.rated as i64) as f64 * beats(RATING_START, me);
        1.0 + rated + unrated
    }

    /// The rating whose expected rank is `rank`.
    pub fn performance(&self, rank: f64) -> f64 {
        let (mut lo, mut hi) = (0.0f64, 4000.0f64);
        while hi - lo > 0.01 {
            let mid = (lo + hi) / 2.0;
            if self.expected_rank(mid) < rank {
                hi = mid;
            } else {
                lo = mid;
            }
        }
        (lo + hi) / 2.0
    }
}

/// The chance a participant rated `r` beats one rated `me`.
pub fn beats(r: f64, me: f64) -> f64 {
    1.0 / (1.0 + 10f64.powf((me - r) / 400.0))
}

/// How far the rating moves towards the performance: k contests before
/// this one, 1/2 on the first, 2/9 in the limit.
pub fn step(k: usize) -> f64 {
    let s: f64 = (0..=k).map(|i| (5.0f64 / 7.0).powi(i as i32)).sum();
    1.0 / (1.0 + s)
}

/// One rated contest: the rating after it and what went into it.
#[derive(Debug, Clone, PartialEq)]
pub struct Standing {
    pub date: NaiveDate,
    pub contest: String,
    pub expected_rank: f64,
    pub performance: f64,
    /// after the contest
    pub rating: f64,
    pub sampled: usize,
    pub user_num: i64,
}

impl Contest {
    /// contests/<stem>.field.json
    pub fn field_path(&self) -> PathBuf {
        self.path.with_extension("field.json")
    }

    /// The field, once contest_field.mjs has written it.
    pub fn field(&self) -> Option<Field> {
        Field::from_json(&crate::data::read_json(&self.field_path())?)
    }
}

/// LeetCode's rating over the contests with a field, in the order given,
/// from RATING_START; a contest without a field is skipped.
pub fn leetcode_rating(contests: &[&Contest]) -> Vec<Standing> {
    let mut rating = RATING_START;
    let mut out = Vec::new();
    for c in contests {
        let Some(f) = c.field() else { continue };
        let expected = f.expected_rank(rating);
        let performed_at = (expected * c.rank as f64).sqrt();
        let performance = f.performance(performed_at);
        rating += (performance - rating) * step(out.len());
        out.push(Standing {
            date: c.date,
            contest: c.contest.clone(),
            expected_rank: expected,
            performance,
            rating,
            sampled: f.ratings.len(),
            user_num: f.user_num,
        });
    }
    out
}

/// Every contest under contests/, by date then file name.
pub fn load(root: &Path) -> Vec<Contest> {
    let dir = root.join("contests");
    let mut paths: Vec<PathBuf> = match std::fs::read_dir(&dir) {
        Ok(rd) => rd
            .flatten()
            .map(|e| e.path())
            .filter(|p| {
                p.extension().is_some_and(|x| x == "json")
                    && !p.to_string_lossy().ends_with(".field.json")
            })
            .collect(),
        Err(_) => return vec![],
    };
    paths.sort();
    let mut out: Vec<Contest> = paths
        .iter()
        .map(|p| {
            let v =
                crate::data::read_json(p).unwrap_or_else(|| panic!("{}: not JSON", p.display()));
            Contest::from_json(p, &v)
        })
        .collect();
    out.sort_by(|a, b| (a.date, &a.path).cmp(&(b.date, &b.path)));
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    fn weekly_525() -> Contest {
        let v: Value = serde_json::from_str(
            r#"{
              "contest": "Weekly Contest 525", "virtual": true, "date": "2026-10-27",
              "clock_min": 90, "rank": 6445, "field": 33050, "solved_all": 887,
              "score": 12, "score_max": 18, "finish": "01:40:24",
              "languages": "mu (Q1, Q2), Python3 (Q3)", "ratings": "CLIST's",
              "intro": "This was my second virtual contest, unaided.",
              "problems": [
                {"slot": "Q1", "problem": "4092", "name": "Binary Digit Score", "rating": 541,
                 "accepted_at": "00:04:39", "wrong": 0, "assist": "none"},
                {"slot": "Q2", "problem": "4093", "name": "Maximize Sum", "rating": 1424.5,
                 "accepted_at": "01:09:31", "wrong": 1, "assist": "hint", "note": "a tip"},
                {"slot": "Q3", "problem": "4094", "name": "Staircase I", "rating": 1749,
                 "accepted_at": null, "wrong": 2, "assist": "none"},
                {"slot": "Q4", "problem": "4095", "name": "Staircase II", "rating": 2344,
                 "accepted_at": null, "wrong": 0, "assist": "none"}
              ]
            }"#,
        )
        .unwrap();
        Contest::from_json(Path::new("contests/2026-10-27_weekly_525.json"), &v)
    }

    #[test]
    fn scores_follow_the_accept_and_the_assist() {
        let c = weekly_525();
        let scores: Vec<f64> = c.problems.iter().map(Problem::score).collect();
        assert_eq!(scores, vec![1.0, 0.5, 0.0, 0.0]);
        let results: Vec<String> = c.problems.iter().map(Problem::result).collect();
        assert_eq!(
            results,
            vec![
                "solved, no help",
                "solved with help: a tip",
                "failed",
                "not attempted"
            ]
        );
        assert_eq!(c.games()[1], (c.date, 1424.5, 0.5));
        assert_eq!(
            c.md_path(),
            PathBuf::from("contests/2026-10-27_weekly_525.md")
        );
    }

    #[test]
    fn markdown_is_the_header_and_the_table() {
        let md = weekly_525().markdown();
        let want = "\
# Weekly Contest 525 (virtual)

This was my second virtual contest, unaided.

Date: 2026-10-27 (PHT)
Clock: 90 minutes
Virtual rank: 6445 of 33,050 (887 solved all four)
Score: 12 of 18
Finish time: 01:40:24 (with 15 minutes of penalty for 3 wrong submissions)
Language: mu (Q1, Q2), Python3 (Q3)
Ratings: CLIST's

| #   | Problem                  | Rating | Accepted at | Penalty          | Result                  |
| --- | ------------------------ | ------ | ----------- | ---------------- | ----------------------- |
| Q1  | 4092. Binary Digit Score | 541    | 00:04:39    | -                | solved, no help         |
| Q2  | 4093. Maximize Sum       | 1424.5 | 01:09:31    | 5 min (1 wrong)  | solved with help: a tip |
| Q3  | 4094. Staircase I        | 1749   | -           | 10 min (2 wrong) | failed                  |
| Q4  | 4095. Staircase II       | 2344   | -           | -                | not attempted           |";
        assert_eq!(md, want);
    }

    #[test]
    fn fresh_markdown_has_the_region_and_a_heading_per_problem() {
        let md = weekly_525().fresh_markdown();
        assert!(md.starts_with("<!-- CONTEST -->\n# Weekly Contest 525 (virtual)\n"));
        assert!(md.contains("\n<!-- /CONTEST -->\n\n## Q1. 4092. Binary Digit Score\n"));
        assert!(md.ends_with("\n## Notes\n"));
    }

    #[test]
    fn leetcode_step_halves_the_first_move_and_tends_to_two_ninths() {
        assert!((step(0) - 0.5).abs() < 1e-12);
        assert!((step(1) - 1.0 / (1.0 + 1.0 + 5.0 / 7.0)).abs() < 1e-12);
        assert!((step(60) - 2.0 / 9.0).abs() < 1e-6);
    }

    fn flat_field(n: i64, r: f64) -> Field {
        Field {
            user_num: n,
            fetched: "2026-10-27".to_string(),
            ratings: vec![r; 100],
            rated: 100,
        }
    }

    #[test]
    fn expected_rank_and_performance_invert_each_other() {
        let f = flat_field(10000, 1500.0);
        // half of a 1500 field beats a 1500
        assert!((f.expected_rank(1500.0) - 5001.0).abs() < 1e-6);
        assert!((f.performance(5001.0) - 1500.0).abs() < 0.02);
        // a stronger rating expects a better rank, and the inverse agrees
        let er = f.expected_rank(1900.0);
        assert!(er < 1500.0);
        assert!((f.performance(er) - 1900.0).abs() < 0.02);
    }

    #[test]
    fn leetcode_rating_moves_half_way_on_a_first_contest() {
        // ranking exactly at the expected rank leaves the rating alone;
        // ranking first moves it half way to the performance
        let dir = std::env::temp_dir().join(format!("kg_contests_{}", std::process::id()));
        std::fs::create_dir_all(&dir).unwrap();
        let mut c = weekly_525();
        c.path = dir.join("2026-10-27_weekly_525.json");
        let ratings = vec![1500.0; 100];
        std::fs::write(
            c.field_path(),
            serde_json::json!({"user_num": 10000, "fetched": "2026-10-27", "ratings": ratings})
                .to_string(),
        )
        .unwrap();
        c.rank = 5001;
        let st = leetcode_rating(&[&c]);
        assert_eq!(st.len(), 1);
        assert!((st[0].rating - 1500.0).abs() < 0.1, "{:?}", st[0]);
        c.rank = 1;
        let st = leetcode_rating(&[&c]);
        let perf = st[0].performance;
        assert!(perf > 2000.0);
        assert!((st[0].rating - (1500.0 + (perf - 1500.0) * 0.5)).abs() < 1e-6);
        // a field without ratings is no field
        std::fs::write(
            c.field_path(),
            serde_json::json!({"user_num": 10000, "fetched": "2026-10-27", "ratings": []})
                .to_string(),
        )
        .unwrap();
        assert!(c.field().is_none());
        assert!(leetcode_rating(&[&c]).is_empty());
        std::fs::remove_dir_all(&dir).unwrap();
    }

    #[test]
    fn helpers() {
        assert_eq!(thousands(33050), "33,050");
        assert_eq!(thousands(887), "887");
        assert_eq!(thousands(1000000), "1,000,000");
        assert_eq!(rating_text(1315.4), "1315.4");
        assert_eq!(rating_text(1422.0), "1422");
    }
}
