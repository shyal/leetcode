// DRILL: Square
// TRAINS: rust-fn-signature
//
// Write a function `square` that takes an integer `num` and returns its
// square. `main` below calls it; the file does not compile until the
// function exists.
//
// Example 1:
//
// Input: num = 3
// Output: 9
//
// Example 2:
//
// Input: num = 0
// Output: 0
//
// Example 3:
//
// Input: num = -4
// Output: 16
//
// Constraints:
//
//     -40000 <= num <= 40000
//     num is an i32
//
//     REQUIRED: the parameter and the return type are both written in the
//     signature; the body is one expression and ends with no semicolon.
//     NO return keyword.

fn main() {
    println!("{}", square(3));
    // assert_eq!(square(3), 9);
    // assert_eq!(square(0), 0);
    // assert_eq!(square(-4), 16);
    // assert_eq!(square(40000), 1600000000);
}
