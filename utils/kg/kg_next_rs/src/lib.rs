// The Rust `make next`: the picker, its library, and the terminal
// rendering, mirrored from utils/kg/kg_next and utils/kg/kg_lib.py.
// The functions keep the Python signatures' shape (many arguments, the
// same tuple types) so the two read side by side.
#![allow(clippy::too_many_arguments, clippy::type_complexity)]

pub mod bank;
pub mod cell_widths;
pub mod cells;
pub mod clock;
pub mod console;
pub mod ctx;
pub mod data;
pub mod drills;
pub mod evidence;
pub mod git;
pub mod model;
pub mod pick;
pub mod recog;
pub mod render;
pub mod status;
pub mod table;
