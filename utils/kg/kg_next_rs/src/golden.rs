// `kg_next --golden-json`: every library value the parity test diffs
// against utils/kg/kg_lib.py and utils/kg/kg_next, over the real graph/
// data. utils/tests/test_next_parity.py computes the same table in Python
// and compares the two exactly, so a drift in either port fails `make test`.

use std::cell::RefCell;
use std::collections::HashSet;

use chrono::NaiveDate;
use serde_json::{json, Map, Value};

use kg_next::bank::{
    carriers_for, drafted_in_reach, held_behind, predicted_carrier, proving_carriers, unlocks,
    vertex_status, warm,
};
use kg_next::clock::{due_problems, last_attempt, problem_due};
use kg_next::ctx::{Ctx, PView};
use kg_next::drills::{
    anki_due, anki_frontier, cold_drill, drill_assisted, drill_capped, drill_clean, drill_gated,
    drill_held, drill_recall, drill_warm, drills_left, due_drill, group_caps, group_reps,
    last_drilled, node_drill_hold,
};
use kg_next::evidence::Evidence;
use kg_next::git::{sleep_rows, sleep_state, solve_seconds_today, solved_today_pnums};
use kg_next::model::{drill_forecast, elo_now, solve_forecast, solve_model, solve_ratings};
use kg_next::pick::{
    blocked_frontier, choice_tuple, parked_summits, pick, ready_hards, review_ahead, review_queue,
    routed_around, starved, trivial_easies, unmapped_summits, upcoming, PickArgs,
};
use kg_next::recog;
use kg_next::status::{
    cooled, gentleness, graduation_due, last_clean_solve, last_solved, latest_carrier, node_axes,
    node_curve, owned, tree_size, Statuses,
};

fn date(d: Option<NaiveDate>) -> Value {
    match d {
        Some(d) => json!(d.format("%Y-%m-%d").to_string()),
        None => Value::Null,
    }
}

fn round(x: f64) -> Value {
    // 12 significant decimals in Python's "%.12e" spelling (a signed,
    // two-digit exponent): enough to catch a drift, short of the last ulp
    // where libm and numpy may legitimately differ
    let s = format!("{x:.12e}");
    let (mant, exp) = s.split_once('e').unwrap_or((&s, "0"));
    let (sign, digits) = match exp.strip_prefix('-') {
        Some(d) => ("-", d),
        None => ("+", exp),
    };
    json!(format!("{mant}e{sign}{digits:0>2}"))
}

pub fn dump(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    statuses: &Statuses,
    immature: &HashSet<String>,
    today: NaiveDate,
) {
    let mut nodes = Map::new();
    let empty: HashSet<String> = HashSet::new();
    let unl = unlocks(ctx, statuses, pv, &empty);
    let gain = unlocks(ctx, statuses, pv, immature);
    let skip: HashSet<String> = HashSet::new();
    for n in ctx.nodes.keys() {
        let (status, last, recall, memory) = node_curve(ctx, n, ev, today);
        let ax = node_axes(ctx, n, ev, pv, today);
        let due = due_drill(ctx, n, ev, today, false, false);
        let cold = cold_drill(ctx, n, ev, today, false);
        let promo = predicted_carrier(ctx, n, pv, statuses, ev, &skip, &["Easy", "Medium"], today);
        nodes.insert(
            n.clone(),
            json!({
                "status": status.to_string(),
                "last": date(last),
                "recall": round(recall),
                "memory": round(memory),
                "carriers": ax.carriers,
                "breadth": round(ax.breadth),
                "degree": round(ax.degree),
                "immature": immature.contains(n),
                "owned": owned(ev, n),
                "graduation_due": graduation_due(ev, n, pv.carrier_counts(ctx).get(n).copied().unwrap_or(0)).map(|(d, f)| json!([d.format("%Y-%m-%d").to_string(), f])),
                "has_bank": ctx.has_drill_bank(n),
                "drill_held": drill_held(ctx, n, statuses, ev, &empty),
                "drill_gated": drill_gated(ctx, n, status, last, today),
                "drills_left": drills_left(ctx, n, ev, false),
                "due_drill": due.as_ref().map(|p| p.display().to_string()),
                "cold_drill": cold.as_ref().map(|p| p.display().to_string()),
                "node_drill_hold": node_drill_hold(ctx, n, ev, today),
                "carriers_for": carriers_for(ctx, n, pv, statuses, ev, today),
                "proving_carriers": proving_carriers(ctx, n, pv, statuses, ev, today),
                "unlocks": unl.get(n).copied().unwrap_or(0),
                "gain": gain.get(n).copied().unwrap_or(0),
                "latest_carrier": latest_carrier(ev, n).map(|(d, f, p)| json!([d.format("%Y-%m-%d").to_string(), f, p])),
                "predicted_carrier": promo.map(|(num, e)| json!([num, e.title, e.difficulty, e.moves])),
            }),
        );
    }

    let mut problems = Map::new();
    let ratings = solve_ratings(ctx);
    for (pnum, p) in &pv.map {
        problems.insert(
            pnum.clone(),
            json!({
                "last_solved": last_solved(ev, pnum),
                "last_clean_solve": last_clean_solve(ev, pnum),
                "held_behind": held_behind(ctx, pnum, pv, ev, today),
                "problem_due": problem_due(ev, pnum).map(|(d, i)| json!([d.format("%Y-%m-%d").to_string(), i])),
                "last_attempt": last_attempt(ev, pnum).map(|(d, l)| json!([d.format("%Y-%m-%d").to_string(), l])),
                "cooled": cooled(ev, pnum, today),
                "tree_size": tree_size(ctx, pnum, pv),
                "gentleness": gentleness(ctx, pnum, pv),
                "forecast": solve_forecast(ctx, pnum, pv, today).map(|(a, b, c)| json!([round(a), round(b), round(c)])),
                "rating": ratings.get(pnum).map(|r| round(*r)),
                "warm": warm(ctx, pnum, pv, ev, today, false),
                "vertex_status": vertex_status(ctx, pnum, pv, ev, today).to_string(),
                "difficulty": p.difficulty(),
            }),
        );
    }

    let mut drills = Map::new();
    for n in ctx.nodes.keys() {
        for path in ctx.bank_paths(n).iter() {
            let path = path.clone();
            let key = path.display().to_string();
            drills.insert(
                key,
                json!({
                    "title": ctx.drill_title(&path),
                    "id": ctx.drill_id(&path),
                    "stem": ctx.drill_solved_stem(&path),
                    "trains": ctx.drill_trains(&path),
                    "after": ctx.drill_after(&path),
                    "last_drilled": last_drilled(ctx, &path, ev),
                    "anki_due": anki_due(ctx, &path, ev).map(|(d, i)| json!([d.format("%Y-%m-%d").to_string(), i])),
                    "warm": drill_warm(ctx, &path, ev, today),
                    "clean": drill_clean(ctx, &path, ev),
                    "assisted": drill_assisted(ctx, &path, ev),
                    "capped": drill_capped(ctx, &path, ev, today),
                    "recall": drill_recall(ctx, &path, ev, today).map(|(p, c, g, k)| json!([p.map(round), c, g, k])),
                    "forecast": drill_forecast(ctx, &path, today).map(|(a, b, c)| json!([round(a), round(b), round(c)])),
                }),
            );
        }
    }

    let asleep = sleep_state(ctx, pv, ev);
    let mut scenarios = Map::new();
    let groups: HashSet<String> = ctx.nodes.values().filter_map(|n| n.group.clone()).collect();
    let mut scenario_list: Vec<(String, PickArgs)> = vec![
        (
            "default".into(),
            PickArgs {
                asleep: asleep.clone(),
                ..Default::default()
            },
        ),
        (
            "session_start".into(),
            PickArgs {
                asleep: asleep.clone(),
                session_start: true,
                ..Default::default()
            },
        ),
        ("no_asleep".into(), PickArgs::default()),
    ];
    let mut gs: Vec<String> = groups.into_iter().collect();
    gs.sort();
    for g in gs {
        for (suffix, cram, early, assisted) in [
            ("", false, false, false),
            ("_cram", true, false, false),
            ("_early", false, true, false),
            ("_assisted", false, false, true),
        ] {
            scenario_list.push((
                format!("group_{g}{suffix}"),
                PickArgs {
                    asleep: asleep.clone(),
                    group: Some(g.clone()),
                    cram,
                    early,
                    assisted,
                    ..Default::default()
                },
            ));
        }
    }
    for (name, args) in scenario_list {
        let view = RefCell::new(pv.clone());
        let mut exclude: HashSet<String> = HashSet::new();
        let mut picks: Vec<Value> = Vec::new();
        for _ in 0..3 {
            let a = PickArgs {
                exclude: exclude.clone(),
                ..args.clone()
            };
            match pick(ctx, &view, ev, statuses, &a) {
                Some(c) => {
                    let t = choice_tuple(&c);
                    picks.push(json!([t.0, t.1, t.2, t.3]));
                    exclude.insert(c.pnum.clone());
                }
                None => {
                    picks.push(Value::Null);
                    break;
                }
            }
        }
        scenarios.insert(name, json!(picks));
    }

    let (rd, rs, rr) = review_ahead(
        ctx,
        pv,
        ev,
        &asleep,
        &solved_today_pnums(ctx),
        None,
        14,
        200,
    );
    let recog_all = recog::derived(ctx, &recog::load_recognition(ctx), ev, pv, statuses);
    let node_ids: Vec<String> = ctx.nodes.keys().cloned().collect();
    let rstat: Map<String, Value> = recog::recognition_statuses(&recog_all, &node_ids, today)
        .into_iter()
        .map(|(n, (s, d))| (n, json!([s, date(d)])))
        .collect();
    let mut solved_today: Vec<String> = solved_today_pnums(ctx).into_iter().collect();
    solved_today.sort();
    let out = json!({
        "today": today.format("%Y-%m-%d").to_string(),
        "nodes": nodes,
        "problems": problems,
        "drills": drills,
        "anki_frontier": anki_frontier(ctx, ev, today, None, None, false).iter().map(|(p, n)| json!([p.display().to_string(), n])).collect::<Vec<_>>(),
        "due_problems": due_problems(ev, today, Some(pv)).iter().map(|(p, d, i)| json!([p, d.format("%Y-%m-%d").to_string(), i])).collect::<Vec<_>>(),
        "review_queue": review_queue(ctx, ev, pv, today).iter().map(|(p, _, _)| json!(p)).collect::<Vec<_>>(),
        "asleep": asleep,
        "sleep_rows": sleep_rows(ctx, pv, ev, statuses).iter().map(|(p, t, r, s, c)| json!([p, t, r, s, c])).collect::<Vec<_>>(),
        "starved": starved(ctx, pv, ev, today),
        "routed_around": routed_around(ctx, pv, ev, today),
        "blocked_frontier": blocked_frontier(ctx, pv, ev, statuses, &asleep, &HashSet::new(), today).iter().map(|(n, s, w, d)| json!([n, s.to_string(), w, d])).collect::<Vec<_>>(),
        "ready_hards": ready_hards(ctx, pv, ev, statuses, None, None, today),
        "parked_summits": parked_summits(ctx, pv, ev, statuses, &asleep, today),
        "unmapped_summits": unmapped_summits(ctx, pv, ev, statuses),
        "drafted_in_reach_hard": drafted_in_reach(ctx, pv, statuses, immature, ev, &HashSet::new(), "Hard", 20, today).iter().map(|(n, e)| json!([n, e.title, e.difficulty, e.moves])).collect::<Vec<_>>(),
        "drafted_in_reach_medium": drafted_in_reach(ctx, pv, statuses, immature, ev, &HashSet::new(), "Medium", 20, today).iter().map(|(n, e)| json!([n, e.title, e.difficulty, e.moves])).collect::<Vec<_>>(),
        "trivial_easies": trivial_easies(ctx, pv, ev, statuses, today),
        "elo_now": round(elo_now(ctx, ev)),
        "solve_model": solve_model(ctx),
        "ratings_count": ratings.len(),
        "review_ahead": [rd, rs, rr],
        "upcoming": upcoming(ctx, pv, ev, 5, &asleep, 30),
        "scenarios": scenarios,
        "recognition": rstat,
        "due_spot": recog::due_spot(ctx, pv, ev, &recog_all, statuses, today, &asleep.iter().cloned().collect()).map(|(a, b, c)| json!([a, b, c])),
        "solve_seconds_today": solve_seconds_today(ctx),
        "solved_today": solved_today,
        "group_caps": group_caps(),
        "group_reps": group_caps().iter().map(|(g, _)| json!([g, group_reps(ctx, g, ev, today)])).collect::<Vec<_>>(),
    });
    println!("{}", serde_json::to_string(&out).unwrap());
}
