// The kg library: the picker, its data model, and the terminal
// rendering, ported from utils/kg/kg_lib.py and the Python kg_next (the
// picker's Python is gone; kg_lib.py still serves the tests and the
// dormant renderers). Every binary in this workspace links it; `mock` is
// the cold-mock model that `make mock` and `make movie` share. The
// functions keep the Python signatures' shape (many arguments, the same
// tuple types) so the two read side by side.
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
pub mod figlet;
pub mod git;
pub mod linalg;
pub mod llm;
pub mod mock;
pub mod model;
pub mod pick;
pub mod pyjson;
pub mod pysrc;
pub mod queue;
pub mod recog;
pub mod render;
pub mod status;
pub mod table;

#[cfg(test)]
mod tests;
