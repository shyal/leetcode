fn first_divisor(n: i32) -> i32 {
    if n % 4 == 0 {
        4
    } else if n % 3 == 0 {
        3
    } else if n % 2 == 0 {
        2
    } else {
        0
    }
}
