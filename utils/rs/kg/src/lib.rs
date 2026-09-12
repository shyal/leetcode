// The kg library: the picker, its data model, and the terminal
// rendering, mirrored from utils/kg/kg_lib.py and utils/kg/kg_next. Every
// binary in this workspace (kg_next, kg_mock, kg_movie) links it; `mock` is
// the cold-mock model that `make mock` and `make movie` share.
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
pub mod figlet;
pub mod git;
pub mod llm;
pub mod mock;
pub mod model;
pub mod pick;
pub mod pyjson;
pub mod recog;
pub mod render;
pub mod status;
pub mod table;
