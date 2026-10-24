// Given an integer `n`, test the divisors 4, 3 and 2 in that order and
// return the first that divides n. Return 0 when none of them does.
//
// Example 1:
//
// Input: n = 6
// Output: 3
// Explanation: 4 does not divide 6, so 3 is tested next and wins. 2 is
// never tested.
//
// Example 2:
//
// Input: n = 12
// Output: 4
//
// Example 3:
//
// Input: n = 7
// Output: 0
//
// Constraints:
//
//     1 <= n <= 10^9
//     n is an i32 and so is the answer
//
//     REQUIRED: one if / else if / else if / else chain whose four
//     branches are the four integer literals, and that chain is the
//     function's value. NO match, NO return keyword, NO loop.

fn first_divisor(n: i32) -> i32 {
    todo!()
}

fn main() {
    println!("{}", first_divisor(6));
    // assert_eq!(first_divisor(6), 3);
    // assert_eq!(first_divisor(12), 4);
    // assert_eq!(first_divisor(7), 0);
    // assert_eq!(first_divisor(10), 2);
    // assert_eq!(first_divisor(1), 0);
}
