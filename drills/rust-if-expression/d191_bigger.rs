// DRILL: Bigger
// TRAINS: rust-if-expression
//
// Given two integers `a` and `b`, return the bigger one. When they are
// equal, either one is the answer.
//
// Example 1:
//
// Input: a = 10, b = 8
// Output: 10
//
// Example 2:
//
// Input: a = 32, b = 42
// Output: 42
//
// Example 3:
//
// Input: a = 42, b = 42
// Output: 42
//
// Constraints:
//
//     -10^9 <= a, b <= 10^9
//     a and b are i32
//
//     REQUIRED: the body is one if/else whose two branches are the values
//     a and b, and that if/else is the function's value. NO return keyword,
//     NO extra variable, NO function call.

fn bigger(a: i32, b: i32) -> i32 {
    todo!()
}

fn main() {
    println!("{}", bigger(10, 8));
    // assert_eq!(bigger(10, 8), 10);
    // assert_eq!(bigger(32, 42), 42);
    // assert_eq!(bigger(42, 42), 42);
    // assert_eq!(bigger(-5, -9), -5);
}
