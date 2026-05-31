fn collatz_steps(mut n: u64) -> u32 {
    let mut steps = 0;
    while n > 1 {
        if n % 2 == 0 {
            n /= 2;
        } else {
            n = n * 3 + 1;
        }
        steps += 1;
    }
    steps
}

fn main() {
    let mut max_steps = 0;
    let mut best_num = 0;
    for i in 1..=500000 {
        let steps = collatz_steps(i);
        if steps > max_steps {
            max_steps = steps;
            best_num = i;
        }
    }
    println!("Num: {}, Steps: {}", best_num, max_steps);
}
