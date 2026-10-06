// DRILL: Count Spaces
// TRAINS: rust-shadowing
//
// Given a string `spaces` made only of space characters, return how many
// spaces it holds. Inside the function, bind the count to the name
// `spaces` as well: the string and its length share one name.
//
// Example 1:
//
// Input: spaces = "   "
// Output: 3
//
// Example 2:
//
// Input: spaces = ""
// Output: 0
//
// Example 3:
//
// Input: spaces = " "
// Output: 1
//
// Constraints:
//
//     0 <= spaces.len() <= 10^4
//     every character of spaces is ' '
//
//     REQUIRED: a second let binding of the name spaces, holding the
//     length, shadows the parameter; the function returns usize. NO mut,
//     NO second name.

fn count_spaces(spaces: &str) -> usize {
    todo!()
}

fn main() {
    println!("{}", count_spaces("   "));
    // assert_eq!(count_spaces("   "), 3);
    // assert_eq!(count_spaces(""), 0);
    // assert_eq!(count_spaces(" "), 1);
}
