def log2(n: int) -> int:
    k = 1
    i = 0
    while k < n:
        k *= 2
        i += 1
    return i + 1


def main() -> None:
    n = int(input())
    nlayers = log2(n)
    cur = 0
    mapping = {}
    for _ in range(n):
        mapping[(0, cur)] = cur
        cur += 1
    receptive_width = 1
    for i in range(1, nlayers):
        for j in range(receptive_width, n):
            l = i - 1
            while (l, j - receptive_width) not in mapping:
                l -= 1
            left_parent = mapping[(l, j - receptive_width)]
            right_parent = mapping[(i - 1, j)]
            print(f"GATE {cur} OR {left_parent} {right_parent}")
            mapping[(i, j)] = cur
            cur += 1
        receptive_width *= 2
    # print(f"Number of layers: {nlayers}")
    # print(mapping)
    layer_to_take = 0
    pow = 1
    for i in range(n):
        if i >= pow:
            pow *= 2
            layer_to_take += 1
        print(f"OUTPUT {i} {mapping[(layer_to_take, i)]}")


if __name__ == "__main__":
    main()