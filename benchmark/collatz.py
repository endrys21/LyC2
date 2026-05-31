def collatz_steps(n: int) -> int:
    steps = 0
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def main():
    max_steps = 0
    best_num = 0
    for i in range(1, 500001):
        steps = collatz_steps(i)
        if steps > max_steps:
            max_steps = steps
            best_num = i
    print(f"Num: {best_num}, Steps: {max_steps}")

if __name__ == "__main__":
    main()
