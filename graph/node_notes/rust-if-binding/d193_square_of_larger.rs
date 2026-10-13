fn square_of_larger(a: i32, b: i32) -> i32 {
    let larger = if a > b { a } else { b };
    larger * larger
}
