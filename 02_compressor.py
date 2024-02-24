import typing as tp


def AND(cur: int, A: int, B: int) -> int:
    print(f"GATE {cur} AND {A} {B}")
    return cur + 1


def OR(cur: int, A: int, B: int) -> int:
    print(f"GATE {cur} OR {A} {B}")
    return cur + 1


def NOT(cur: int, A: int) -> int:
    print(f"GATE {cur} NOT {A}")
    return cur + 1


def XOR(cur: int, A: int, B: int) -> int:
    and_idx = AND(cur, A, B) - 1
    or_idx = OR(cur + 1, A, B) - 1
    not_idx = NOT(cur + 2, and_idx) - 1
    cur = AND(cur + 3, not_idx, or_idx)
    return cur


def SUMMCARRY(cur: int, A: int, B: int, C: int) -> tp.Tuple[int]:
    cur = XOR(cur, A, B)
    xor = cur - 1
    cur = NOT(cur, xor)
    nxor = cur - 1
    cur = NOT(cur, C)
    not_C = cur - 1
    cur = AND(cur, xor, C)
    xor_and_C = cur - 1
    cur = AND(cur, nxor, C)
    nxor_and_C = cur - 1
    cur = AND(cur, xor, not_C)
    xor_and_not_C = cur - 1
    cur = AND(cur, nxor, A)
    nxor_and_A = cur - 1
    cur = OR(cur, xor_and_not_C, nxor_and_C)
    summa = cur - 1
    cur = OR(cur, xor_and_C, nxor_and_A)
    carry = cur - 1
    print(f"OUTPUT {A + 1} {carry}")
    print(f"OUTPUT {B + 1} {summa}")
    return cur, xor, nxor


def main() -> None:
    n = int(input())
    cur = 3 * n
    xor, nxor = 0, 0
    for i in range(n):
        cur, xor, nxor = SUMMCARRY(cur, i, n + i, 2 * n + i)
    zero = AND(cur, xor, nxor) - 1
    print(f"OUTPUT {0} {zero}")
    print(f"OUTPUT {2 * n + 1} {zero}")


if __name__ == "__main__":
    main()