// kg_rs - utils/rs/kg exposed to Python. Every function here replaces the
// body of a kg_lib.py function of the same name; kg_lib imports them from
// kg_rs and the tests keep exercising the Python signatures.

use std::collections::HashMap;
use std::path::Path;

use pyo3::prelude::*;

/// kg_lib.degree_color: the hex colour of a degree of ownership in [0, 1].
#[pyfunction]
fn degree_color(degree: f64) -> String {
    kg::render::degree_color(degree)
}

/// kg_lib.source_extensions: the file extensions a bank or solved file can
/// have, one per language in kg::lang, Python first.
#[pyfunction]
fn source_extensions() -> Vec<String> {
    kg::lang::LANGS.iter().map(|l| l.ext.to_string()).collect()
}

/// kg::model::combined_ratings over the repo at root: problem number ->
/// the rating every reader of a rating in the repo shows (zerotrac's, else
/// CLIST's on zerotrac's scale). mu/chrome/build.py writes it into the
/// extension so LeetCode's pages show the same number as make next.
#[pyfunction]
fn solve_ratings(root: &str) -> HashMap<String, f64> {
    kg::model::combined_ratings(Path::new(root))
}

#[pymodule]
fn kg_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(source_extensions, m)?)?;
    m.add_function(wrap_pyfunction!(degree_color, m)?)?;
    m.add_function(wrap_pyfunction!(solve_ratings, m)?)?;
    Ok(())
}
