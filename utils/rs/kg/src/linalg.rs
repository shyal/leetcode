// The little dense linear algebra the fitters need: least squares by
// Householder QR (numpy.linalg.lstsq), a solve and an inverse by LU with
// partial pivoting (numpy.linalg.solve / inv). Matrices are Vec<Vec<f64>>,
// row major; the systems are a handful of columns wide.

#![allow(clippy::needless_range_loop)]

/// numpy's pairwise summation of a float64 array (blocks of 8 partial
/// sums, halves above 128 elements), so a sum agrees with np.sum to the
/// last bit where the fitters compare.
pub fn np_sum(a: &[f64]) -> f64 {
    let n = a.len();
    if n < 8 {
        let mut s = 0.0;
        for x in a {
            s += x;
        }
        return s;
    }
    if n <= 128 {
        let mut r = [0.0f64; 8];
        r.copy_from_slice(&a[..8]);
        let mut i = 8;
        while i + 8 <= n {
            for j in 0..8 {
                r[j] += a[i + j];
            }
            i += 8;
        }
        let mut res = ((r[0] + r[1]) + (r[2] + r[3])) + ((r[4] + r[5]) + (r[6] + r[7]));
        while i < n {
            res += a[i];
            i += 1;
        }
        return res;
    }
    let mut n2 = n / 2;
    n2 -= n2 % 8;
    np_sum(&a[..n2]) + np_sum(&a[n2..])
}

/// Python's round(x, n): the exact decimal expansion rounded half to even.
pub fn round_to(x: f64, n: usize) -> f64 {
    format!("{x:.n$}").parse().unwrap_or(x)
}

/// argmin_b ||Xb - y||: Householder QR, then back substitution.
pub fn lstsq(x: &[Vec<f64>], y: &[f64]) -> Vec<f64> {
    let m = x.len();
    let n = x[0].len();
    let mut a: Vec<Vec<f64>> = x.to_vec();
    let mut b: Vec<f64> = y.to_vec();
    for k in 0..n.min(m) {
        let norm: f64 = (k..m).map(|i| a[i][k] * a[i][k]).sum::<f64>().sqrt();
        if norm == 0.0 {
            continue;
        }
        let alpha = if a[k][k] > 0.0 { -norm } else { norm };
        let mut v: Vec<f64> = (0..m).map(|i| if i < k { 0.0 } else { a[i][k] }).collect();
        v[k] -= alpha;
        let vnorm: f64 = v.iter().map(|t| t * t).sum::<f64>();
        if vnorm == 0.0 {
            continue;
        }
        for j in k..n {
            let dot: f64 = (k..m).map(|i| v[i] * a[i][j]).sum();
            let f = 2.0 * dot / vnorm;
            for i in k..m {
                a[i][j] -= f * v[i];
            }
        }
        let dot: f64 = (k..m).map(|i| v[i] * b[i]).sum();
        let f = 2.0 * dot / vnorm;
        for i in k..m {
            b[i] -= f * v[i];
        }
    }
    let mut beta = vec![0.0; n];
    for k in (0..n).rev() {
        let mut s = b[k];
        for j in k + 1..n {
            s -= a[k][j] * beta[j];
        }
        beta[k] = if a[k][k] != 0.0 { s / a[k][k] } else { 0.0 };
    }
    beta
}

/// A x = b for square A, LU with partial pivoting.
pub fn solve(a: &[Vec<f64>], b: &[f64]) -> Option<Vec<f64>> {
    let n = a.len();
    let mut m: Vec<Vec<f64>> = a
        .iter()
        .cloned()
        .zip(b)
        .map(|(mut r, bi)| {
            r.push(*bi);
            r
        })
        .collect();
    for col in 0..n {
        let piv =
            (col..n).max_by(|i, j| m[*i][col].abs().partial_cmp(&m[*j][col].abs()).unwrap())?;
        if m[piv][col] == 0.0 {
            return None;
        }
        m.swap(col, piv);
        for i in col + 1..n {
            let f = m[i][col] / m[col][col];
            if f != 0.0 {
                for j in col..=n {
                    m[i][j] -= f * m[col][j];
                }
            }
        }
    }
    let mut x = vec![0.0; n];
    for i in (0..n).rev() {
        let mut s = m[i][n];
        for j in i + 1..n {
            s -= m[i][j] * x[j];
        }
        x[i] = s / m[i][i];
    }
    Some(x)
}

/// The inverse of square A, column by column.
pub fn inverse(a: &[Vec<f64>]) -> Option<Vec<Vec<f64>>> {
    let n = a.len();
    let mut cols = Vec::new();
    for j in 0..n {
        let e: Vec<f64> = (0..n).map(|i| if i == j { 1.0 } else { 0.0 }).collect();
        cols.push(solve(a, &e)?);
    }
    Some(
        (0..n)
            .map(|i| (0..n).map(|j| cols[j][i]).collect())
            .collect(),
    )
}

/// X^T diag(w) X + ridge (identity times lam, the first diagonal spared when
/// `spare_first`) + eps I.
pub fn xtwx(x: &[Vec<f64>], w: &[f64], lam: f64, spare_first: bool, eps: f64) -> Vec<Vec<f64>> {
    let p = x[0].len();
    let mut h = vec![vec![0.0; p]; p];
    for (row, wi) in x.iter().zip(w) {
        for i in 0..p {
            for j in 0..p {
                h[i][j] += row[i] * wi * row[j];
            }
        }
    }
    for i in 0..p {
        if !(spare_first && i == 0) {
            h[i][i] += lam;
        }
        h[i][i] += eps;
    }
    h
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn least_squares_recovers_a_line() {
        let x: Vec<Vec<f64>> = (0..10).map(|i| vec![1.0, i as f64]).collect();
        let y: Vec<f64> = (0..10).map(|i| 2.0 + 3.0 * i as f64).collect();
        let b = lstsq(&x, &y);
        assert!((b[0] - 2.0).abs() < 1e-12 && (b[1] - 3.0).abs() < 1e-12);
    }

    #[test]
    fn solve_and_inverse() {
        let a = vec![vec![4.0, 1.0], vec![2.0, 3.0]];
        let x = solve(&a, &[1.0, 2.0]).unwrap();
        assert!((x[0] - 0.1).abs() < 1e-12 && (x[1] - 0.6).abs() < 1e-12);
        let inv = inverse(&a).unwrap();
        assert!((inv[0][0] - 0.3).abs() < 1e-12 && (inv[1][1] - 0.4).abs() < 1e-12);
        assert_eq!(round_to(0.12345, 4), 0.1235);
        assert_eq!(round_to(2.5, 0), 2.0);
    }
}
