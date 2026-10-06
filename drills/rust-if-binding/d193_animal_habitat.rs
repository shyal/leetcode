// DRILL: Animal Habitat
// TRAINS: rust-if-binding
//
// Given a string `animal`, return where it lives: "Beach" for "crab",
// "Burrow" for "gopher", "Desert" for "snake", and "Unknown" for anything
// else. Do it in two steps: first bind a number `identifier` (1 for crab,
// 2 for gopher, 3 for snake, 4 otherwise) with a single let whose value is
// an if chain, then turn that number into the habitat with a second if
// chain.
//
// Example 1:
//
// Input: animal = "gopher"
// Output: "Burrow"
//
// Example 2:
//
// Input: animal = "dinosaur"
// Output: "Unknown"
//
// Example 3:
//
// Input: animal = "crab"
// Output: "Beach"
//
// Constraints:
//
//     1 <= animal.len() <= 100
//     animal is a &str and so is the answer
//
//     REQUIRED: let identifier = if ... else if ... else ...; with every
//     branch an integer of one type and a semicolon after the closing
//     brace; the second if chain is the function's value. NO match,
//     NO mut, NO return keyword.

fn animal_habitat(animal: &str) -> &str {
    todo!()
}

fn main() {
    println!("{}", animal_habitat("gopher"));
    // assert_eq!(animal_habitat("gopher"), "Burrow");
    // assert_eq!(animal_habitat("dinosaur"), "Unknown");
    // assert_eq!(animal_habitat("crab"), "Beach");
    // assert_eq!(animal_habitat("snake"), "Desert");
}
