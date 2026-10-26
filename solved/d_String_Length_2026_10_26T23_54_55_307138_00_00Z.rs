// Given a string `s`, return its length. Inside the function, bind the
// length to the name `s` as well: the string and its length share one
// name.
//
// Example 1:
//
// Input: s = "abc"
// Output: 3
//
// Example 2:
//
// Input: s = ""
// Output: 0
//
// Example 3:
//
// Input: s = "a b"
// Output: 3
//
// Constraints:
//
//     0 <= s.len() <= 10^4
//     s is ASCII
//
//     REQUIRED: a second let binding of the name s, holding the length,
//     shadows the parameter; the function returns usize. NO mut, NO second
//     name.

fn string_length(s: &str) -> usize {
    s.len()
}

fn main() {
    println!("{}", string_length("abc"));
    assert_eq!(string_length("abc"), 3);
    assert_eq!(string_length(""), 0);
    assert_eq!(string_length("a b"), 3);
}
