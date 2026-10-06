fn sum_to_n(n: u64) -> u64 {
    let mut total = 0;
    for i in 1..=n {
        total += i;
    }
    total
}
