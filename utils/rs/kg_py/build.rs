// macOS links a Python extension with -undefined dynamic_lookup: the
// interpreter that loads it supplies the Py* symbols.
fn main() {
    pyo3_build_config::add_extension_module_link_args();
}
