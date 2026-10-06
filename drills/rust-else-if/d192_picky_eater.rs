// DRILL: Picky Eater
// TRAINS: rust-else-if
//
// Given a string `food`, return "Yummy!" when it is "strawberry",
// "I guess I can eat that." when it is "potato", and "No thanks!" for
// anything else.
//
// Example 1:
//
// Input: food = "strawberry"
// Output: "Yummy!"
//
// Example 2:
//
// Input: food = "potato"
// Output: "I guess I can eat that."
//
// Example 3:
//
// Input: food = "broccoli"
// Output: "No thanks!"
//
// Constraints:
//
//     1 <= food.len() <= 100
//     food is a &str and so is the answer
//
//     REQUIRED: one if / else if / else chain whose three branches are the
//     three string literals; every branch has the same type. NO match,
//     NO return keyword, NO String.

fn picky_eater(food: &str) -> &str {
    todo!()
}

fn main() {
    println!("{}", picky_eater("strawberry"));
    // assert_eq!(picky_eater("strawberry"), "Yummy!");
    // assert_eq!(picky_eater("potato"), "I guess I can eat that.");
    // assert_eq!(picky_eater("broccoli"), "No thanks!");
    // assert_eq!(picky_eater("gummy bears"), "No thanks!");
}
