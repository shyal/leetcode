// DRILL: Sum To N
// TRAINS: rust-let-mut
//
// Given an integer `n`, return the sum 1 + 2 + ... + n. For n = 0 the sum
// is 0.
//
// Example 1:
//
// Input: n = 3
// Output: 6
//
// Example 2:
//
// Input: n = 0
// Output: 0
//
// Example 3:
//
// Input: n = 1
// Output: 1
//
// Constraints:
//
//     0 <= n <= 10^6
//     n is a u64
//
//     REQUIRED: a running total declared with let mut and a for loop over
//     the range 1..=n that adds to it; the total is the last expression.
//     NO formula, NO iterator sum.

fn sum_to_n(n: u64) -> u64 {
    todo!()
}

fn main() {
    println!("{}", sum_to_n(3));
    // assert_eq!(sum_to_n(3), 6);
    // assert_eq!(sum_to_n(0), 0);
    // assert_eq!(sum_to_n(1), 1);
    // assert_eq!(sum_to_n(1_000_000), 500_000_500_000);
}
