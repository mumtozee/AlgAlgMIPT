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


def XOR(cur: int, A: int, B: int) -> tp.Tuple[int]:
    cur = AND(cur, A, B)
    and_idx = cur - 1
    cur = OR(cur, A, B)
    or_idx = cur - 1
    cur = NOT(cur, and_idx)
    not_idx = cur - 1
    cur = AND(cur, or_idx, not_idx)
    return cur, or_idx, and_idx


def NXOR(cur: int, or_idx: int, and_idx: int) -> int:
    cur = NOT(cur, or_idx)
    not_idx = cur - 1
    cur = OR(cur, and_idx, not_idx)
    return cur


def SUMMCARRY(cur: int, A: int, B: int, C: int) -> tp.Tuple[int]:
    cur, or_idx, and_idx = XOR(cur, A, B)
    xor = cur - 1

    cur = NOT(cur, C)
    not_C = cur - 1

    cur = AND(cur, xor, not_C)
    xor_and_not_C = cur - 1

    cur = NXOR(cur, or_idx, and_idx)
    nxor = cur - 1

    cur = AND(cur, nxor, C)
    nxor_and_C = cur - 1

    cur = OR(cur, xor_and_not_C, nxor_and_C)
    summa = cur - 1

    print(f"OUTPUT {A} {summa}")

    cur = OR(cur, C, and_idx)
    C_or_A_and_B = cur - 1

    cur = AND(cur, C_or_A_and_B, or_idx)
    carry = cur - 1

    print(f"OUTPUT {B + 2} {carry}")
    return cur, C, not_C
    # cur = XOR(cur, A, B)
    # xor_AB = cur - 1

    # cur = XOR(cur, xor_AB, C)
    # xor_ABC = cur - 1
    # print(f"OUTPUT {B + 1} {xor_ABC}")

    # cur = AND(cur, xor_AB, C)
    # xor_AB_and_C = cur - 1

    # cur = NOT(cur, xor_AB)
    # nxor_AB = cur - 1

    # cur = AND(cur, nxor_AB, A)
    # nxor_AB_and_A = cur - 1

    # cur = OR(cur, xor_AB_and_C, nxor_AB_and_A)
    # carry = cur - 1
    # print(f"OUTPUT {A + 1} {carry}")
    # return cur, xor_AB, nxor_AB


def main() -> None:
    n = int(input())
    cur = 3 * n
    xor, nxor = 0, 0
    for i in range(n):
        cur, xor, nxor = SUMMCARRY(cur, i, n + i, 2 * n + i)
    zero = AND(cur, xor, nxor) - 1
    print(f"OUTPUT {n} {zero}")
    print(f"OUTPUT {n + 1} {zero}")


if __name__ == "__main__":
    main()