// kg_rs - utils/rs/kg exposed to Python. Every function here replaces the
// body of a kg_lib.py function of the same name; kg_lib imports them from
// kg_rs and the tests keep exercising the Python signatures.

use pyo3::prelude::*;

/// kg_lib.drill_key: the drill a d_ solved file is a rep of, or None.
#[pyfunction]
fn drill_key(fname: &str) -> Option<String> {
    kg::evidence::drill_key(fname)
}

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

#[pymodule]
fn kg_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(drill_key, m)?)?;
    m.add_function(wrap_pyfunction!(source_extensions, m)?)?;
    m.add_function(wrap_pyfunction!(degree_color, m)?)?;
    Ok(())
}
