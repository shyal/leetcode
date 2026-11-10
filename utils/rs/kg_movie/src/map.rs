// map — the technique graph drawn as an old map, for kg_movie --map.
//
// A group is a country, a node is a town, a prerequisite edge is a road.
// The output has the same markup as graphviz svg (g class node / edge /
// cluster, a title, a first path), so the replay in main.rs reads the
// geometry and adds the animation tracks with no change.
//
// Layout: each country is a block of town cells (column-major, the towns
// with no prerequisite on the left). The blocks are packed by a small force
// simulation: countries joined by a road pull together and touch, the others
// stay apart with sea between them. A smooth warp and uneven columns then
// move the towns off the grid, and a relaxation step separates the names.
// The land is a distance field around each town and its name plus value
// noise; marching squares gives the coast and the country borders. Hills
// and trees go on the land that has no name on it; ships, a sea serpent and
// rhumb lines go on the largest areas of open sea.

use std::collections::HashMap;
use std::fmt::Write as _;

const CELL_W: f64 = 168.0; // one town with its name
const CELL_H: f64 = 44.0;
const TITLE_H: f64 = 30.0; // band for the country name
const GAP_LINKED: f64 = -12.0; // between two countries joined by a road
const GAP_FREE: f64 = 64.0; // between two countries with no road: sea
const MARGIN: f64 = 40.0;
const FOOT_H: f64 = 110.0; // legend, title and compass under the land
const GRID: f64 = 8.0; // marching squares cell
const LAND_R: f64 = 48.0; // land reaches this far from a town and its name
const NOISE_AMP: f64 = 52.0;

const SEA: &str = "#8fb0a8";
const LAND: &str = "#eedcb2";
const COAST: &str = "#4a3520";
const ROAD: &str = "#6b4a2b";
const WASH: [&str; 6] = ["#c9a66b", "#a9bd7c", "#d9a48f", "#93b8ad", "#e3cc6e", "#c39ab0"];
pub const SERIF: &str = "Palatino,'Book Antiqua',Georgia,serif";

pub struct Input<'a> {
    pub groups: &'a [(&'a str, Vec<usize>)],
    pub ids: Vec<&'a str>,
    pub edges: Vec<(usize, usize)>, // prerequisite -> node
    pub fills: Vec<String>,         // the fill of each town today
    pub legend: Vec<(String, String)>, // label, fill
    pub ink: &'a str,
    pub stroke: &'a str,
}

// The parchment: flat colour, brown blotches, dark corners.
pub fn backdrop(bg: &str, w: f64, h: f64) -> String {
    format!(
        "<rect x=\"0\" y=\"0\" width=\"{w:.0}\" height=\"{h:.0}\" fill=\"{bg}\"/>\n\
<rect x=\"0\" y=\"0\" width=\"{w:.0}\" height=\"{h:.0}\" filter=\"url(#paper)\"/>\n\
<rect x=\"0\" y=\"0\" width=\"{w:.0}\" height=\"{h:.0}\" fill=\"url(#vignette)\"/>\n"
    )
}

fn hash(ix: i64, iy: i64, seed: u64) -> f64 {
    let mut z = (ix as u64)
        .wrapping_mul(0x9E37_79B9_7F4A_7C15)
        .wrapping_add((iy as u64).wrapping_mul(0xC2B2_AE3D_27D4_EB4F))
        .wrapping_add(seed.wrapping_mul(0x1656_67B1_9E37_79F9));
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
    z ^= z >> 31;
    (z >> 11) as f64 / (1u64 << 53) as f64
}

fn vnoise(x: f64, y: f64, seed: u64) -> f64 {
    let (ix, iy) = (x.floor(), y.floor());
    let (fx, fy) = (x - ix, y - iy);
    let (sx, sy) = (fx * fx * (3.0 - 2.0 * fx), fy * fy * (3.0 - 2.0 * fy));
    let (ix, iy) = (ix as i64, iy as i64);
    let top = hash(ix, iy, seed) * (1.0 - sx) + hash(ix + 1, iy, seed) * sx;
    let bot = hash(ix, iy + 1, seed) * (1.0 - sx) + hash(ix + 1, iy + 1, seed) * sx;
    top * (1.0 - sy) + bot * sy
}

// In [-0.5, 0.5].
fn fbm(x: f64, y: f64) -> f64 {
    vnoise(x / 230.0, y / 230.0, 4) * 0.42
        + vnoise(x / 110.0, y / 110.0, 1) * 0.3
        + vnoise(x / 45.0, y / 45.0, 2) * 0.18
        + vnoise(x / 18.0, y / 18.0, 3) * 0.1
        - 0.5
}

// Closed contours of the field at `level`. The field has (nx + 1) * (ny + 1)
// corner values; the corners on the rim count as outside, so each contour
// is a loop.
fn contours(f: &[f64], nx: usize, ny: usize, level: f64) -> Vec<Vec<(f64, f64)>> {
    let val = |i: usize, j: usize| {
        if i == 0 || j == 0 || i == nx || j == ny {
            level - 1.0
        } else {
            f[j * (nx + 1) + i]
        }
    };
    type Key = (usize, usize, u8); // 0: edge (i,j)-(i+1,j), 1: edge (i,j)-(i,j+1)
    let mut adj: HashMap<Key, Vec<Key>> = HashMap::new();
    for j in 0..ny {
        for i in 0..nx {
            let (tl, tr, br, bl) = (
                val(i, j) > level,
                val(i + 1, j) > level,
                val(i + 1, j + 1) > level,
                val(i, j + 1) > level,
            );
            let case = (tl as u8) << 3 | (tr as u8) << 2 | (br as u8) << 1 | bl as u8;
            let (top, bottom, left, right) = ((i, j, 0), (i, j + 1, 0), (i, j, 1), (i + 1, j, 1));
            let segs: &[(Key, Key)] = match case {
                1 | 14 => &[(left, bottom)],
                2 | 13 => &[(bottom, right)],
                3 | 12 => &[(left, right)],
                4 | 11 => &[(top, right)],
                6 | 9 => &[(top, bottom)],
                7 | 8 => &[(left, top)],
                5 => &[(left, top), (bottom, right)],
                10 => &[(left, bottom), (top, right)],
                _ => &[],
            };
            for &(a, b) in segs {
                adj.entry(a).or_default().push(b);
                adj.entry(b).or_default().push(a);
            }
        }
    }
    let point = |k: Key| -> (f64, f64) {
        let (i, j, dir) = k;
        let a = val(i, j);
        let b = if dir == 0 { val(i + 1, j) } else { val(i, j + 1) };
        let t = ((level - a) / (b - a)).clamp(0.0, 1.0);
        if dir == 0 {
            ((i as f64 + t) * GRID, j as f64 * GRID)
        } else {
            (i as f64 * GRID, (j as f64 + t) * GRID)
        }
    };
    let mut keys: Vec<Key> = adj.keys().copied().collect();
    keys.sort_unstable();
    let mut seen: std::collections::HashSet<Key> = Default::default();
    let mut loops = vec![];
    for start in keys {
        if seen.contains(&start) {
            continue;
        }
        let mut pts = vec![];
        let mut cur = start;
        loop {
            seen.insert(cur);
            pts.push(point(cur));
            match adj[&cur].iter().find(|k| !seen.contains(k)) {
                Some(&n) => cur = n,
                None => break,
            }
        }
        if pts.len() >= 4 {
            loops.push(pts);
        }
    }
    loops
}

// One closed smooth path: quadratic curves through the midpoints.
fn smooth(pts: &[(f64, f64)], out: &mut String) {
    let n = pts.len();
    let mid = |a: (f64, f64), b: (f64, f64)| ((a.0 + b.0) / 2.0, (a.1 + b.1) / 2.0);
    let m0 = mid(pts[0], pts[1]);
    write!(out, "M{:.0},{:.0}", m0.0, m0.1).unwrap();
    for i in 1..=n {
        let p = pts[i % n];
        let m = mid(p, pts[(i + 1) % n]);
        write!(out, "Q{:.0},{:.0} {:.0},{:.0}", p.0, p.1, m.0, m.1).unwrap();
    }
    out.push('Z');
}

fn path_d(loops: &[Vec<(f64, f64)>]) -> String {
    let mut d = String::new();
    for l in loops {
        smooth(l, &mut d);
    }
    d
}

// The field at a point, bilinear between the corners.
fn sample(f: &[f64], nx: usize, ny: usize, x: f64, y: f64) -> f64 {
    let gx = (x / GRID).clamp(0.0, nx as f64 - 1e-6);
    let gy = (y / GRID).clamp(0.0, ny as f64 - 1e-6);
    let (i, j) = (gx as usize, gy as usize);
    let (fx, fy) = (gx - i as f64, gy - j as f64);
    let at = |i: usize, j: usize| f[j * (nx + 1) + i];
    (at(i, j) * (1.0 - fx) + at(i + 1, j) * fx) * (1.0 - fy)
        + (at(i, j + 1) * (1.0 - fx) + at(i + 1, j + 1) * fx) * fy
}

fn ship(x: f64, y: f64, flip: bool, ink: &str) -> String {
    format!(
        "<g transform=\"translate({x:.0} {y:.0}) scale({} 1.5)\" stroke=\"{ink}\" stroke-width=\"0.9\" stroke-linejoin=\"round\">\
<path fill=\"none\" opacity=\"0.6\" d=\"M-38,19 q5,-4 10,0 t10,0 t10,0 t10,0 t10,0 t10,0 t10,0 M-30,25 q5,-4 10,0 t10,0 t10,0 t10,0 t10,0\"/>\
<path fill=\"#8a5a32\" d=\"M-23,5 Q-19,16 0,16 Q19,16 26,2 L15,6 L-14,6 Z\"/>\
<path fill=\"none\" d=\"M0,6 L0,-30 M-13,6 L-13,-14\"/>\
<path fill=\"{LAND}\" d=\"M-11,-25 Q2,-20 13,-25 L13,-3 Q2,2 -11,-3 Z M-20,-12 Q-13,-9 -7,-12 L-7,1 Q-13,4 -20,1 Z\"/>\
<path fill=\"#a3161a\" d=\"M0,-30 l10,-3 l-10,-3 Z\"/></g>\n",
        if flip { -1.5 } else { 1.5 }
    )
}

fn serpent(x: f64, y: f64, ink: &str) -> String {
    let body = "M-74,12 C-80,-30 -62,-44 -50,-30 M-40,12 C-40,-22 -12,-22 -12,12 M-4,12 C-4,-14 20,-14 20,12 M28,12 C28,-6 44,-6 44,12 M52,12 C54,2 62,0 66,-10";
    format!(
        "<g transform=\"translate({x:.0} {y:.0}) scale(1.5)\" fill=\"none\" stroke-linecap=\"round\">\
<path stroke=\"{ink}\" stroke-width=\"9\" d=\"{body}\"/>\
<path stroke=\"#5f8f76\" stroke-width=\"6.6\" d=\"{body}\"/>\
<path stroke=\"{ink}\" stroke-width=\"0.8\" opacity=\"0.7\" d=\"M-36,-2 l3,-5 M-28,-9 l2,-6 M-18,-6 l-2,-6 M0,0 l3,-5 M8,-5 l1,-6 M16,-1 l-2,-5\"/>\
<ellipse cx=\"-45\" cy=\"-27\" rx=\"9\" ry=\"5.5\" transform=\"rotate(28 -45 -27)\" fill=\"#5f8f76\" stroke=\"{ink}\" stroke-width=\"1.2\"/>\
<circle cx=\"-45\" cy=\"-29\" r=\"1.3\" fill=\"{ink}\"/>\
<path stroke=\"#a3161a\" stroke-width=\"1\" d=\"M-37,-23 l7,3 l4,-2 M-30,-20 l4,3\"/>\
<path fill=\"#5f8f76\" stroke=\"{ink}\" stroke-width=\"1\" d=\"M66,-10 l8,-7 l-1,9 l8,2 Z\"/>\
<path stroke=\"{ink}\" stroke-width=\"0.9\" opacity=\"0.6\" d=\"M-92,15 q5,-4 10,0 t10,0 M-48,15 q4,-3 8,0 M-12,15 q4,-3 8,0 M20,15 q4,-3 8,0 M44,15 q4,-3 8,0 t8,0 t8,0 M-60,22 q5,-4 10,0 t10,0 t10,0 t10,0 t10,0 t10,0 t10,0 t10,0\"/></g>\n"
    )
}

pub fn render(inp: &Input) -> String {
    let n = inp.ids.len();
    let ng = inp.groups.len();
    let mut group_of = vec![0usize; n];
    for (gi, (_, members)) in inp.groups.iter().enumerate() {
        for &ni in members {
            group_of[ni] = gi;
        }
    }

    // depth of a town: the longest chain of prerequisites before it
    let mut depth = vec![0usize; n];
    let mut degree = vec![0usize; n];
    for &(p, c) in &inp.edges {
        degree[p] += 1;
        degree[c] += 1;
    }
    for _ in 0..n {
        let mut changed = false;
        for &(p, c) in &inp.edges {
            if depth[c] < depth[p] + 1 {
                depth[c] = depth[p] + 1;
                changed = true;
            }
        }
        if !changed {
            break;
        }
    }
    // the capital of a country: the town with the most roads
    let mut capital = vec![false; n];
    for (_, members) in inp.groups {
        if let Some(&c) = members.iter().max_by_key(|&&ni| (degree[ni], std::cmp::Reverse(ni))) {
            capital[c] = degree[c] > 0;
        }
    }

    // ---- one block of cells per country ------------------------------------
    struct Block {
        w: f64,
        h: f64,
        x: f64,
        y: f64,
        cols: usize,
        rows: usize,
    }
    let mut blocks: Vec<Block> = inp
        .groups
        .iter()
        .enumerate()
        .map(|(gi, (name, members))| {
            let k = members.len();
            let cols = ((0.26 * k as f64).sqrt().round() as usize).max(1);
            let rows = k.div_ceil(cols);
            let a = gi as f64 * 2.399_963;
            let r = 260.0 * (gi as f64 + 1.0).sqrt();
            Block {
                w: (cols as f64 * CELL_W).max(name.len() as f64 * 15.0 + 20.0),
                h: rows as f64 * CELL_H * 1.12 + TITLE_H + 0.5 * CELL_H,
                x: r * a.cos() * 0.6,
                y: r * a.sin() * 1.5,
                cols,
                rows,
            }
        })
        .collect();
    let mut links: HashMap<(usize, usize), f64> = HashMap::new();
    for &(p, c) in &inp.edges {
        let (a, b) = (group_of[p].min(group_of[c]), group_of[p].max(group_of[c]));
        if a != b {
            *links.entry((a, b)).or_default() += 1.0;
        }
    }
    let resolve = |blocks: &mut Vec<Block>| {
        for a in 0..ng {
            for b in a + 1..ng {
                let gap = if links.contains_key(&(a, b)) { GAP_LINKED } else { GAP_FREE };
                let (dx, dy) = (blocks[b].x - blocks[a].x, blocks[b].y - blocks[a].y);
                let ox = (blocks[a].w + blocks[b].w) / 2.0 + gap - dx.abs();
                let oy = (blocks[a].h + blocks[b].h) / 2.0 + gap - dy.abs();
                if ox > 0.0 && oy > 0.0 {
                    if ox < oy {
                        let s = if dx < 0.0 { -ox / 2.0 } else { ox / 2.0 };
                        blocks[a].x -= s;
                        blocks[b].x += s;
                    } else {
                        let s = if dy < 0.0 { -oy / 2.0 } else { oy / 2.0 };
                        blocks[a].y -= s;
                        blocks[b].y += s;
                    }
                }
            }
        }
    };
    let mut pairs: Vec<(&(usize, usize), &f64)> = links.iter().collect();
    pairs.sort_by_key(|(k, _)| **k);
    for _ in 0..900 {
        for (&(a, b), &w) in &pairs {
            let f = 0.02 * w.min(4.0);
            let (dx, dy) = (blocks[b].x - blocks[a].x, blocks[b].y - blocks[a].y);
            blocks[a].x += dx * f;
            blocks[a].y += dy * f;
            blocks[b].x -= dx * f;
            blocks[b].y -= dy * f;
        }
        for b in blocks.iter_mut() {
            b.x *= 0.95;
            b.y *= 0.988;
        }
        for _ in 0..3 {
            resolve(&mut blocks);
        }
    }
    for _ in 0..60 {
        resolve(&mut blocks);
    }

    // ---- towns: uneven columns, a smooth warp, then names kept apart -------
    let warp = |x: f64, y: f64| {
        (
            x + (vnoise(x / 260.0, y / 260.0, 41) - 0.5) * 76.0,
            y + (vnoise(x / 260.0, y / 260.0, 42) - 0.5) * 44.0,
        )
    };
    let name_w = |ni: usize| inp.ids[ni].len() as f64 * 5.0;
    let mut town = vec![(0.0, 0.0); n];
    let mut title: Vec<(f64, f64, f64)> = vec![]; // centre x, baseline y, width
    for (gi, (name, members)) in inp.groups.iter().enumerate() {
        let b = &blocks[gi];
        let mut order = members.clone();
        order.sort_by_key(|&ni| depth[ni]);
        let left = b.x - b.cols as f64 * CELL_W / 2.0;
        let top = b.y - b.h / 2.0 + TITLE_H;
        for (m, &ni) in order.iter().enumerate() {
            let (col, row) = (m / b.rows, m % b.rows);
            let pitch = CELL_H * (0.92 + 0.2 * hash(gi as i64, col as i64, 31));
            let start = top + hash(gi as i64, col as i64, 32) * 0.5 * CELL_H;
            let jx = (hash(ni as i64, 0, 11) - 0.5) * 28.0;
            let jy = (hash(ni as i64, 1, 11) - 0.5) * 10.0;
            town[ni] = warp(
                left + col as f64 * CELL_W + 14.0 + jx,
                start + (row as f64 + 0.5) * pitch + jy,
            );
        }
        let (tx, ty) = warp(b.x, b.y - b.h / 2.0 + 20.0);
        title.push((tx, ty, name.len() as f64 * 15.0));
    }
    let rect = |t: (f64, f64), ni: usize| (t.0 - 12.0, t.1 - 13.0, t.0 + 17.0 + name_w(ni), t.1 + 13.0);
    for _ in 0..60 {
        for a in 0..n {
            let ra = rect(town[a], a);
            for &(tx, ty, tw) in &title {
                let rt = (tx - tw / 2.0, ty - 18.0, tx + tw / 2.0, ty + 8.0);
                if ra.0 < rt.2 && rt.0 < ra.2 && ra.1 < rt.3 && rt.1 < ra.3 {
                    town[a].1 += rt.3 - ra.1;
                }
            }
            for b in a + 1..n {
                let (ra, rb) = (rect(town[a], a), rect(town[b], b));
                let ox = ra.2.min(rb.2) - ra.0.max(rb.0);
                let oy = ra.3.min(rb.3) - ra.1.max(rb.1);
                if ox > 0.0 && oy > 0.0 {
                    if oy <= ox {
                        let s = if town[a].1 <= town[b].1 { oy / 2.0 } else { -oy / 2.0 };
                        town[a].1 -= s;
                        town[b].1 += s;
                    } else {
                        let s = if town[a].0 <= town[b].0 { ox / 2.0 } else { -ox / 2.0 };
                        town[a].0 -= s;
                        town[b].0 += s;
                    }
                }
            }
        }
    }
    // canvas: everything that makes land, plus the reach of the land
    let reach = LAND_R + NOISE_AMP / 2.0 + MARGIN;
    let (mut min_x, mut min_y, mut max_x, mut max_y) = (f64::MAX, f64::MAX, f64::MIN, f64::MIN);
    for ni in 0..n {
        let r = rect(town[ni], ni);
        min_x = min_x.min(r.0);
        min_y = min_y.min(r.1);
        max_x = max_x.max(r.2);
        max_y = max_y.max(r.3);
    }
    for &(tx, ty, tw) in &title {
        min_x = min_x.min(tx - tw / 2.0);
        min_y = min_y.min(ty - 18.0);
        max_x = max_x.max(tx + tw / 2.0);
        max_y = max_y.max(ty);
    }
    let (sx, sy) = (reach - min_x, reach - min_y);
    for t in town.iter_mut() {
        *t = (t.0 + sx, t.1 + sy);
    }
    for t in title.iter_mut() {
        *t = (t.0 + sx, t.1 + sy, t.2);
    }
    let width = ((max_x - min_x + 2.0 * reach) / GRID).ceil() * GRID;
    let height = ((max_y - min_y + 2.0 * reach + FOOT_H) / GRID).ceil() * GRID;

    // what makes land: a town with its name, a country name (x0, x1, y, group)
    let mut anchors: Vec<(f64, f64, f64, usize)> = vec![];
    for ni in 0..n {
        anchors.push((town[ni].0 - 6.0, town[ni].0 + 13.0 + name_w(ni), town[ni].1, group_of[ni]));
    }
    for (gi, &(tx, ty, tw)) in title.iter().enumerate() {
        anchors.push((tx - tw / 2.0, tx + tw / 2.0, ty - 5.0, gi));
    }
    let seg_dist = |x: f64, y: f64, a: &(f64, f64, f64, usize)| {
        let dx = (a.0 - x).max(x - a.1).max(0.0);
        (dx * dx + (y - a.2).powi(2)).sqrt()
    };

    // ---- the land ----------------------------------------------------------
    let (nx, ny) = ((width / GRID) as usize, (height / GRID) as usize);
    let mut land = vec![0.0; (nx + 1) * (ny + 1)];
    let mut country: Vec<Vec<f64>> = vec![vec![0.0; (nx + 1) * (ny + 1)]; ng];
    let mut near = vec![0.0; ng];
    for j in 0..=ny {
        for i in 0..=nx {
            let (x, y) = (i as f64 * GRID, j as f64 * GRID);
            near.fill(f64::MAX);
            for a in &anchors {
                let d = seg_dist(x, y, a);
                if d < near[a.3] {
                    near[a.3] = d;
                }
            }
            let best = near.iter().copied().fold(f64::MAX, f64::min);
            let l = LAND_R - best + fbm(x, y) * NOISE_AMP;
            let at = j * (nx + 1) + i;
            land[at] = l;
            for g in 0..ng {
                let other = (0..ng)
                    .filter(|&h| h != g)
                    .map(|h| near[h])
                    .fold(f64::MAX, f64::min);
                country[g][at] = l.min(other - near[g] + fbm(x + 500.0, y) * 16.0);
            }
        }
    }

    // roads, as sampled curves in canvas coordinates
    let roads: Vec<Vec<(f64, f64)>> = inp
        .edges
        .iter()
        .enumerate()
        .map(|(k, &(p, c))| {
            let (a, b) = (town[p], town[c]);
            let (dx, dy) = (b.0 - a.0, b.1 - a.1);
            let len = (dx * dx + dy * dy).sqrt().max(1.0);
            let (ux, uy) = (dx / len, dy / len);
            let (a, b) = ((a.0 + ux * 10.0, a.1 + uy * 10.0), (b.0 - ux * 13.0, b.1 - uy * 13.0));
            let bend = (hash(k as i64, 5, 23) - 0.5) * 0.36 * len;
            let ctrl = ((a.0 + b.0) / 2.0 - uy * bend, (a.1 + b.1) / 2.0 + ux * bend);
            (0..=12)
                .map(|i| {
                    let t = i as f64 / 12.0;
                    (
                        (1.0 - t).powi(2) * a.0 + 2.0 * t * (1.0 - t) * ctrl.0 + t * t * b.0,
                        (1.0 - t).powi(2) * a.1 + 2.0 * t * (1.0 - t) * ctrl.1 + t * t * b.1,
                    )
                })
                .collect()
        })
        .collect();

    // the largest areas of open sea, most open first
    let mut open: Vec<(f64, f64, f64)> = vec![];
    for _ in 0..4 {
        let mut best: Option<(f64, f64, f64)> = None;
        for j in 0..=ny {
            for i in 0..=nx {
                let (x, y) = (i as f64 * GRID, j as f64 * GRID);
                if x < 130.0 || x > width - 130.0 || y < 100.0 || y > height - FOOT_H - 90.0 {
                    continue;
                }
                if open.iter().any(|o| (o.0 - x).hypot(o.1 - y) < 380.0) {
                    continue;
                }
                let v = -land[j * (nx + 1) + i];
                if best.is_none_or(|b| v > b.2) {
                    best = Some((x, y, v));
                }
            }
        }
        match best {
            Some(b) if b.2 > 75.0 => open.push(b),
            _ => break,
        }
    }

    // ---- draw --------------------------------------------------------------
    let (ink, stroke) = (inp.ink, inp.stroke);
    let mut s = String::with_capacity(768 * 1024);
    writeln!(s, "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>").unwrap();
    writeln!(
        s,
        "<svg width=\"{width:.0}pt\" height=\"{height:.0}pt\" viewBox=\"0.00 0.00 {width:.2} {height:.2}\" xmlns=\"http://www.w3.org/2000/svg\">"
    )
    .unwrap();
    writeln!(
        s,
        "<defs>\
<filter id=\"paper\" x=\"0\" y=\"0\" width=\"100%\" height=\"100%\">\
<feTurbulence type=\"fractalNoise\" baseFrequency=\"0.011 0.017\" numOctaves=\"5\" seed=\"7\"/>\
<feColorMatrix type=\"matrix\" values=\"0 0 0 0 0.42  0 0 0 0 0.28  0 0 0 0 0.12  0.9 0 0 0 -0.28\"/>\
</filter>\
<filter id=\"pen\" x=\"-2%\" y=\"-2%\" width=\"104%\" height=\"104%\">\
<feTurbulence type=\"fractalNoise\" baseFrequency=\"0.045\" numOctaves=\"2\" seed=\"3\"/>\
<feDisplacementMap in=\"SourceGraphic\" scale=\"5\" xChannelSelector=\"R\" yChannelSelector=\"G\"/>\
</filter>\
<radialGradient id=\"vignette\" cx=\"50%\" cy=\"50%\" r=\"75%\">\
<stop offset=\"0.6\" stop-color=\"#5a3a14\" stop-opacity=\"0\"/>\
<stop offset=\"1\" stop-color=\"#5a3a14\" stop-opacity=\"0.38\"/>\
</radialGradient>\
<clipPath id=\"frame\"><rect x=\"15\" y=\"15\" width=\"{:.0}\" height=\"{:.0}\"/></clipPath>\
</defs>",
        width - 30.0,
        height - 30.0
    )
    .unwrap();
    let (ox, oy) = (4.0, height - 4.0); // the graphviz graph transform
    writeln!(
        s,
        "<g id=\"graph0\" class=\"graph\" transform=\"scale(1 1) rotate(0) translate(4 {oy})\">"
    )
    .unwrap();

    // the static map, in canvas coordinates
    writeln!(s, "<g transform=\"translate({} {})\">", -ox, -oy).unwrap();
    writeln!(
        s,
        "<rect x=\"8\" y=\"8\" width=\"{:.0}\" height=\"{:.0}\" fill=\"{SEA}\" opacity=\"0.3\"/>",
        width - 16.0,
        height - 16.0
    )
    .unwrap();
    // rhumb lines from the fourth open area, and from the compass
    let (cx, cy, cr) = (width - 86.0, height - 70.0, 36.0);
    let centres: Vec<(f64, f64)> = std::iter::once((cx, cy))
        .chain(open.get(3).map(|o| (o.0, o.1)))
        .collect();
    let mut rh = String::new();
    for &(rx, ry) in &centres {
        for k in 0..16 {
            let a = k as f64 * std::f64::consts::PI / 16.0;
            let (dx, dy) = (a.cos() * 6000.0, a.sin() * 6000.0);
            write!(rh, "M{:.0},{:.0}L{:.0},{:.0}", rx - dx, ry - dy, rx + dx, ry + dy).unwrap();
        }
    }
    writeln!(
        s,
        "<path clip-path=\"url(#frame)\" fill=\"none\" stroke=\"#6b4a2b\" stroke-width=\"0.6\" opacity=\"0.3\" d=\"{rh}\"/>"
    )
    .unwrap();
    if let Some(o) = open.get(3) {
        writeln!(
            s,
            "<circle cx=\"{:.0}\" cy=\"{:.0}\" r=\"9\" fill=\"{LAND}\" stroke=\"{ink}\" stroke-width=\"1\"/><circle cx=\"{:.0}\" cy=\"{:.0}\" r=\"3\" fill=\"{ink}\"/>",
            o.0, o.1, o.0, o.1
        )
        .unwrap();
    }

    s.push_str("<g filter=\"url(#pen)\">\n");
    let coast_loops = contours(&land, nx, ny, 0.0);
    // short pen strokes on the sea side of the coast
    let mut hatch = String::new();
    for (li, l) in coast_loops.iter().enumerate() {
        let m = l.len();
        let mut run = 0.0;
        for i in 0..m {
            let (p, q) = (l[i], l[(i + 1) % m]);
            run += (q.0 - p.0).hypot(q.1 - p.1);
            if run < 6.0 {
                continue;
            }
            run = 0.0;
            let (a, b) = (l[(i + m - 2) % m], l[(i + 2) % m]);
            let (tx, ty) = (b.0 - a.0, b.1 - a.1);
            let tl = tx.hypot(ty).max(0.01);
            let (mut nxn, mut nyn) = (-ty / tl, tx / tl);
            if sample(&land, nx, ny, p.0 + nxn * 7.0, p.1 + nyn * 7.0)
                > sample(&land, nx, ny, p.0 - nxn * 7.0, p.1 - nyn * 7.0)
            {
                nxn = -nxn;
                nyn = -nyn;
            }
            let len = 4.0 + 9.0 * hash(i as i64, li as i64, 51);
            write!(hatch, "M{:.0},{:.0}l{:.1},{:.1}", p.0, p.1, nxn * len, nyn * len).unwrap();
        }
    }
    writeln!(
        s,
        "<path fill=\"none\" stroke=\"#3f5f66\" stroke-width=\"0.6\" opacity=\"0.4\" d=\"{}\"/>",
        path_d(&contours(&land, nx, ny, -19.0))
    )
    .unwrap();
    writeln!(
        s,
        "<path fill=\"none\" stroke=\"{COAST}\" stroke-width=\"0.7\" opacity=\"0.6\" d=\"{hatch}\"/>"
    )
    .unwrap();
    let coast = path_d(&coast_loops);
    writeln!(s, "<path fill=\"{LAND}\" fill-rule=\"evenodd\" d=\"{coast}\"/>").unwrap();
    // a country: a wash of colour, darker along the inside of its border
    for g in 0..ng {
        let wash = WASH[g % WASH.len()];
        writeln!(
            s,
            "<clipPath id=\"k{g}\"><path id=\"c{g}\" d=\"{}\"/></clipPath>\
<use href=\"#c{g}\" fill=\"{wash}\" fill-opacity=\"0.3\" fill-rule=\"evenodd\"/>\
<use href=\"#c{g}\" clip-path=\"url(#k{g})\" fill=\"none\" stroke=\"{wash}\" stroke-width=\"26\" stroke-opacity=\"0.5\"/>\
<use href=\"#c{g}\" fill=\"none\" stroke=\"#8a3b2a\" stroke-width=\"0.9\" stroke-dasharray=\"5 3\" stroke-opacity=\"0.7\"/>",
            path_d(&contours(&country[g], nx, ny, 0.0))
        )
        .unwrap();
    }
    writeln!(
        s,
        "<path fill=\"none\" stroke=\"{COAST}\" stroke-width=\"1.9\" stroke-linejoin=\"round\" d=\"{coast}\"/>"
    )
    .unwrap();
    s.push_str("</g>\n");

    // hills and trees on the land that has no name and no road on it
    let mut spots: Vec<(f64, f64, bool, f64)> = vec![];
    let step = 26.0;
    for j in 0..(height / step) as i64 {
        for i in 0..(width / step) as i64 {
            let x = (i as f64 + hash(i, j, 61)) * step;
            let y = (j as f64 + hash(i, j, 62)) * step;
            if sample(&land, nx, ny, x, y) < 13.0
                || anchors.iter().any(|a| seg_dist(x, y, a) < 30.0)
                || roads.iter().flatten().any(|r| (r.0 - x).hypot(r.1 - y) < 13.0)
            {
                continue;
            }
            let hill = vnoise(x / 240.0, y / 240.0, 77) > 0.5;
            spots.push((x, y, hill, 9.0 + 7.0 * hash(i, j, 63)));
        }
    }
    spots.sort_by(|a, b| a.1.total_cmp(&b.1));
    for &(x, y, hill, sz) in &spots {
        if hill {
            writeln!(
                s,
                "<path fill=\"#d8c18c\" stroke=\"{ink}\" stroke-width=\"0.9\" stroke-linejoin=\"round\" d=\"M{:.1},{:.1}l{:.1},{:.1}l{:.1},{:.1}\"/><path fill=\"none\" stroke=\"{ink}\" stroke-width=\"0.6\" opacity=\"0.7\" d=\"M{:.1},{:.1}l{:.1},{:.1}M{:.1},{:.1}l{:.1},{:.1}\"/>",
                x - sz, y, sz, -sz * 1.25, sz, sz * 1.25,
                x + sz * 0.2, y - sz * 0.8, sz * 0.25, sz * 0.7,
                x + sz * 0.45, y - sz * 0.45, sz * 0.2, sz * 0.4
            )
            .unwrap();
        } else {
            let r = sz * 0.42;
            writeln!(
                s,
                "<path stroke=\"{ink}\" stroke-width=\"0.8\" d=\"M{x:.1},{:.1}v{:.1}\"/><circle cx=\"{x:.1}\" cy=\"{:.1}\" r=\"{r:.1}\" fill=\"#8f9e5e\" stroke=\"{ink}\" stroke-width=\"0.7\"/>",
                y - r * 0.5, r * 1.6, y - r * 1.2
            )
            .unwrap();
        }
    }

    // the sea: a serpent in the most open area, then two ships
    if let Some(o) = open.first() {
        s.push_str(&serpent(o.0, o.1, ink));
    }
    for (k, o) in open.iter().skip(1).take(2).enumerate() {
        s.push_str(&ship(o.0, o.1, k == 1, ink));
    }

    // fold lines of the sheet
    for (x1, y1, x2, y2) in [
        (width / 3.0, 15.0, width / 3.0, height - 15.0),
        (width * 2.0 / 3.0, 15.0, width * 2.0 / 3.0, height - 15.0),
        (15.0, height / 2.0, width - 15.0, height / 2.0),
    ] {
        writeln!(
            s,
            "<path fill=\"none\" stroke=\"#5a3a14\" stroke-width=\"2.2\" opacity=\"0.1\" d=\"M{x1:.0},{y1:.0}L{x2:.0},{y2:.0}\"/><path fill=\"none\" stroke=\"#fff6dc\" stroke-width=\"1.2\" opacity=\"0.22\" d=\"M{:.0},{:.0}L{:.0},{:.0}\"/>",
            x1 + 2.0, y1 + 2.0, x2 + 2.0, y2 + 2.0
        )
        .unwrap();
    }
    // frame: two lines with a ladder between them
    writeln!(
        s,
        "<rect x=\"8\" y=\"8\" width=\"{:.0}\" height=\"{:.0}\" fill=\"none\" stroke=\"{ink}\" stroke-width=\"1.4\"/>\
<rect x=\"11.5\" y=\"11.5\" width=\"{:.0}\" height=\"{:.0}\" fill=\"none\" stroke=\"{ink}\" stroke-width=\"5\" stroke-dasharray=\"18 18\"/>\
<rect x=\"15\" y=\"15\" width=\"{:.0}\" height=\"{:.0}\" fill=\"none\" stroke=\"{ink}\" stroke-width=\"1.4\"/>",
        width - 16.0,
        height - 16.0,
        width - 23.0,
        height - 23.0,
        width - 30.0,
        height - 30.0
    )
    .unwrap();
    // title on a ribbon
    let (rl, rr, rt, rh) = (width / 2.0 - 270.0, width / 2.0 + 270.0, height - 96.0, 70.0);
    writeln!(
        s,
        "<path fill=\"{LAND}\" stroke=\"{ink}\" stroke-width=\"1.5\" stroke-linejoin=\"round\" d=\"M{rl:.0},{rt:.0}H{rr:.0}l-18,{:.0}l18,{:.0}H{rl:.0}l18,{:.0}Z\"/>\
<path fill=\"none\" stroke=\"{ink}\" stroke-width=\"0.6\" d=\"M{:.0},{:.0}H{:.0}M{:.0},{:.0}H{:.0}\"/>",
        rh / 2.0,
        rh / 2.0,
        -rh / 2.0,
        rl + 10.0,
        rt + 5.0,
        rr - 10.0,
        rl + 10.0,
        rt + rh - 5.0,
        rr - 10.0
    )
    .unwrap();
    writeln!(
        s,
        "<text x=\"{:.0}\" y=\"{:.0}\" text-anchor=\"middle\" font-family=\"{SERIF}\" font-size=\"32\" font-style=\"italic\" letter-spacing=\"2\" fill=\"{ink}\">The Technique Graph</text>",
        width / 2.0,
        height - 58.0
    )
    .unwrap();
    writeln!(
        s,
        "<text x=\"{:.0}\" y=\"{:.0}\" text-anchor=\"middle\" font-family=\"{SERIF}\" font-size=\"13\" fill=\"{ink}\" opacity=\"0.8\">a country is a group, a town is a technique, a road is a prerequisite</text>",
        width / 2.0,
        height - 38.0
    )
    .unwrap();
    // legend on a panel
    let (lx, ly) = (48.0, height - 48.0);
    writeln!(
        s,
        "<rect x=\"{:.0}\" y=\"{:.0}\" width=\"{:.0}\" height=\"64\" rx=\"7\" fill=\"{LAND}\" stroke=\"{ink}\" stroke-width=\"1.5\"/>\
<rect x=\"{:.0}\" y=\"{:.0}\" width=\"{:.0}\" height=\"56\" rx=\"4\" fill=\"none\" stroke=\"{ink}\" stroke-width=\"0.6\"/>",
        lx - 14.0,
        ly - 42.0,
        inp.legend.len() as f64 * 58.0 + 24.0,
        lx - 10.0,
        ly - 38.0,
        inp.legend.len() as f64 * 58.0 + 16.0
    )
    .unwrap();
    writeln!(
        s,
        "<text x=\"{lx:.0}\" y=\"{:.0}\" font-family=\"{SERIF}\" font-size=\"13\" font-style=\"italic\" fill=\"{ink}\">degree of ownership</text>",
        ly - 20.0
    )
    .unwrap();
    for (i, (label, fill)) in inp.legend.iter().enumerate() {
        let x = lx + 8.0 + i as f64 * 58.0;
        writeln!(
            s,
            "<circle cx=\"{x:.0}\" cy=\"{ly:.0}\" r=\"7\" fill=\"{fill}\" stroke=\"{stroke}\" stroke-width=\"1.5\"/>\
<text x=\"{:.0}\" y=\"{:.0}\" font-family=\"{SERIF}\" font-size=\"12\" fill=\"{ink}\">{label}</text>",
            x + 12.0,
            ly + 4.0
        )
        .unwrap();
    }
    // compass
    for k in 0..8 {
        let a = k as f64 * std::f64::consts::FRAC_PI_4;
        let len = if k % 2 == 0 { cr } else { cr * 0.55 };
        let (tx, ty) = (cx + a.sin() * len, cy - a.cos() * len);
        let (px, py) = (a.cos() * cr * 0.14, a.sin() * cr * 0.14);
        writeln!(
            s,
            "<polygon points=\"{tx:.1},{ty:.1} {:.1},{:.1} {:.1},{:.1}\" fill=\"{}\" stroke=\"{ink}\" stroke-width=\"0.8\"/>",
            cx + px,
            cy + py,
            cx - px,
            cy - py,
            if k % 2 == 0 { ink } else { LAND }
        )
        .unwrap();
    }
    writeln!(
        s,
        "<circle cx=\"{cx:.0}\" cy=\"{cy:.0}\" r=\"{:.0}\" fill=\"none\" stroke=\"{ink}\" stroke-width=\"0.8\"/>\
<text x=\"{cx:.0}\" y=\"{:.0}\" text-anchor=\"middle\" font-family=\"{SERIF}\" font-size=\"14\" font-weight=\"bold\" fill=\"{ink}\">N</text>",
        cr * 0.72,
        cy - cr - 5.0
    )
    .unwrap();
    s.push_str("</g>\n");

    // roads: dashes on land in one country, dots between two countries
    for (k, &(p, c)) in inp.edges.iter().enumerate() {
        let pts = &roads[k];
        let mut d = String::new();
        for (i, q) in pts.iter().enumerate() {
            write!(d, "{}{:.1},{:.1}", if i == 0 { "M" } else { " L" }, q.0 - ox, q.1 - oy).unwrap();
        }
        let (last, prev) = (pts[pts.len() - 1], pts[pts.len() - 2]);
        let (hx, hy) = (last.0 - prev.0, last.1 - prev.1);
        let hl = hx.hypot(hy).max(0.01);
        let (hx, hy) = (hx / hl, hy / hl);
        let tip = (last.0 + hx * 4.0 - ox, last.1 + hy * 4.0 - oy);
        let base = (last.0 - hx * 3.0 - ox, last.1 - hy * 3.0 - oy);
        let dash = if group_of[p] == group_of[c] {
            "stroke-dasharray=\"4 3\""
        } else {
            "stroke-dasharray=\"0.1 4.5\" stroke-linecap=\"round\""
        };
        writeln!(
            s,
            "<g id=\"edge{}\" class=\"edge\"><title>{} to {}</title>\n<path fill=\"none\" stroke=\"{ROAD}\" stroke-width=\"{}\" {dash} opacity=\"0.8\" d=\"{d}\"/>\n<polygon fill=\"{ROAD}\" opacity=\"0.8\" points=\"{:.1},{:.1} {:.1},{:.1} {:.1},{:.1}\"/>\n</g>",
            k + 1,
            inp.ids[p],
            inp.ids[c],
            if group_of[p] == group_of[c] { 1.2 } else { 1.9 },
            tip.0,
            tip.1,
            base.0 - hy * 3.0,
            base.1 + hx * 3.0,
            base.0 + hy * 3.0,
            base.1 - hx * 3.0
        )
        .unwrap();
    }

    // country names
    for (gi, (name, _)) in inp.groups.iter().enumerate() {
        let (tx, ty, _) = title[gi];
        writeln!(
            s,
            "<g id=\"clust{}\" class=\"cluster\"><title>cluster_{name}</title>\n<text x=\"{:.1}\" y=\"{:.1}\" text-anchor=\"middle\" font-family=\"{SERIF}\" font-size=\"17\" font-weight=\"bold\" letter-spacing=\"4\" fill=\"#5a3418\" opacity=\"0.85\">{}</text>\n</g>",
            gi + 1,
            tx - ox,
            ty - oy,
            name.to_uppercase()
        )
        .unwrap();
    }

    // towns: the capital is larger and has a ring, a town with no road is small
    for ni in 0..n {
        let (x, y) = (town[ni].0 - ox, town[ni].1 - oy);
        let r = if capital[ni] {
            9.5
        } else if degree[ni] == 0 {
            5.5
        } else {
            7.0
        };
        let mut d = String::new();
        for k in 0..12 {
            let a = k as f64 * std::f64::consts::PI / 6.0;
            write!(
                d,
                "{}{:.1},{:.1}",
                if k == 0 { "M" } else { " L" },
                x + a.cos() * r,
                y + a.sin() * r
            )
            .unwrap();
        }
        d.push_str(" Z");
        let ring = if capital[ni] {
            format!("<circle cx=\"{x:.1}\" cy=\"{y:.1}\" r=\"4\" fill=\"none\" stroke=\"{stroke}\" stroke-width=\"1.3\"/>\n")
        } else {
            String::new()
        };
        writeln!(
            s,
            "<g id=\"node{}\" class=\"node\"><title>{}</title>\n<path fill=\"{}\" stroke=\"{stroke}\" stroke-width=\"1.6\" d=\"{d}\"/>\n{ring}<text x=\"{:.1}\" y=\"{:.1}\" font-family=\"{SERIF}\" font-size=\"11\" font-style=\"italic\" fill=\"{ink}\" stroke=\"{LAND}\" stroke-width=\"2.5\" stroke-opacity=\"0.8\" paint-order=\"stroke\">{}</text>\n</g>",
            ni + 1,
            inp.ids[ni],
            inp.fills[ni],
            x + r + 4.0,
            y + 3.8,
            inp.ids[ni]
        )
        .unwrap();
    }
    s.push_str("</g>\n</svg>\n");
    s
}
