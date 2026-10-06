// DRILL: Hours To Seconds
// TRAINS: rust-const
//
// Given a number of `hours`, return the same duration in seconds. The
// number of seconds in one hour is a constant named SECONDS_PER_HOUR,
// declared once at the top of the file, outside every function.
//
// Example 1:
//
// Input: hours = 3
// Output: 10800
//
// Example 2:
//
// Input: hours = 0
// Output: 0
//
// Example 3:
//
// Input: hours = 1
// Output: 3600
//
// Constraints:
//
//     0 <= hours <= 10^6
//     hours is a u32
//
//     REQUIRED: a const item with its type written, in SCREAMING_SNAKE_CASE,
//     at module level; the function multiplies by it. NO let, NO literal
//     3600 inside the function.

fn hours_to_seconds(hours: u32) -> u32 {
    todo!()
}

fn main() {
    println!("{}", hours_to_seconds(3));
    // assert_eq!(hours_to_seconds(3), 10800);
    // assert_eq!(hours_to_seconds(0), 0);
    // assert_eq!(hours_to_seconds(1), 3600);
    // assert_eq!(SECONDS_PER_HOUR, 3600);
}
