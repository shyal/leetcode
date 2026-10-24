// Given two integers `a` and `b`, return the square of the larger.
// First bind the larger to the name `larger` with a single let whose
// value is an if/else, then return larger times larger.
//
// Example 1:
//
// Input: a = -4, b = 2
// Output: 4
// Explanation: 2 is larger than -4, and 2 * 2 = 4.
//
// Example 2:
//
// Input: a = 3, b = -5
// Output: 9
//
// Example 3:
//
// Input: a = 0, b = 0
// Output: 0
//
// Constraints:
//
//     -3 * 10^4 <= a, b <= 3 * 10^4
//     a and b are i32 and so is the answer
//
//     REQUIRED: let larger = if ... else ...; with both branches i32 and a
//     semicolon after the closing brace; the product larger * larger is the
//     function's value. NO match, NO mut, NO return keyword, NO method call.

fn square_of_larger(a: i32, b: i32) -> i32 {
    todo!()
}

fn main() {
    println!("{}", square_of_larger(-4, 2));
    // assert_eq!(square_of_larger(-4, 2), 4);
    // assert_eq!(square_of_larger(3, -5), 9);
    // assert_eq!(square_of_larger(0, 0), 0);
    // assert_eq!(square_of_larger(7, 7), 49);
    // assert_eq!(square_of_larger(-9, -2), 4);
}
