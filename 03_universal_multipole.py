import typing as tp
import itertools
from copy import deepcopy
from time import sleep


def output(out_idx: int, in_idx: int) -> int:
    print(f"OUTPUT {out_idx} {in_idx}")
    return out_idx + 1


def AND(cur: int, A: int, B: int) -> int:
    print(f"GATE {cur} AND {A} {B}")
    return cur + 1


def OR(cur: int, A: int, B: int) -> int:
    print(f"GATE {cur} OR {A} {B}")
    return cur + 1


def NOT(cur: int, A: int) -> int:
    print(f"GATE {cur} NOT {A}")
    return cur + 1


class Disjunct:
    def __init__(self, params: tp.FrozenSet[int]) -> None:
        self.params = params

    def __call__(self, x: tp.Tuple[bool]) -> bool:
        result = False
        for i in self.params:
            if i < 0:
                result = result or (not x[-i - 1])
            else:
                result = result or x[i - 1]
        return result


class Identity:
    def __init__(self, params: int) -> None:
        # print(f"IDENTITY CALLED WITH: {params}")
        self.params = params

    def __call__(self, x: tp.Tuple[bool]) -> bool:
        if self.params < 0:
            return not x[-self.params - 1]
        return x[self.params - 1]


class CNF:
    def __init__(self, params: tp.FrozenSet[tp.FrozenSet[int]]) -> None:
        self.params = params

    def __call__(self, x: tp.Tuple[bool]) -> bool:
        result = True
        for disj_params in self.params:
            cur_disj = Disjunct(params=disj_params)
            result = result and cur_disj(x)
        return result


def cnf2func(cnf: tp.FrozenSet | int) -> tp.Callable:
    if isinstance(cnf, int):
        return Identity(params=cnf)
    tmp_item = next(iter(cnf))
    if isinstance(tmp_item, int):
        return Disjunct(params=cnf)
    return CNF(params=cnf)


def are_equal(n: int, a: tp.FrozenSet | int, b: tp.FrozenSet | int) -> bool:
    a_func = cnf2func(a)
    b_func = cnf2func(b)
    bools = (False, True)
    for x in itertools.product(bools, repeat=n):
        if a_func(x) != b_func(x):
            return False
    return True


def iscomposite(s: tp.FrozenSet) -> bool:
    tmp_item = next(iter(s))
    return not isinstance(tmp_item, int)


def isconstant(n, s: tp.FrozenSet) -> bool:
    s_func = cnf2func(s)
    prev_val = None
    bools = (False, True)
    for x in itertools.product(bools, repeat=n):
        cur_val = s_func(x)
        if prev_val is not None:
            if cur_val != prev_val:
                return False
        prev_val = cur_val
    return True


def main() -> int:
    res = 0
    memory = {}
    n = int(input())
    cur = n
    out_cur = 0
    # identity functions
    for i in range(n):
        out_cur = output(out_cur, i)
    # negations
    for i in range(n):
        out_cur = output(out_cur, cur)
        memory[-(i + 1)] = cur
        cur = NOT(cur, i)
    out_cur = output(out_cur, cur)
    cur = OR(cur, 0, n)
    out_cur = output(out_cur, cur)
    cur = AND(cur, 0, n)
    # pairwise disjuncts
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            out_cur = output(out_cur, cur)
            memory[frozenset({i, j})] = cur
            cur = OR(cur, i - 1, j - 1)

            out_cur = output(out_cur, cur)
            memory[frozenset({-i, -j})] = cur
            cur = OR(cur, memory[-i], memory[-j])

            out_cur = output(out_cur, cur)
            memory[frozenset({i, -j})] = cur
            cur = OR(cur, i - 1, memory[-j])

            out_cur = output(out_cur, cur)
            memory[frozenset({-i, j})] = cur
            cur = OR(cur, memory[-i], j - 1)
    # construct disjuncts
    for disj_size in range(3, n + 1):
        for i in range(1, n + 1):
            keys = deepcopy(list(memory.keys()))
            for key in keys:
                # filter out too small disjuncts or the ones already
                # containing current variabels or its negation
                if (
                    isinstance(key, int)
                    or (len(key) < disj_size - 1)
                    or ((i in key) or (-i in key))
                ):
                    continue
                new_key_A = frozenset({i, *key})
                new_key_B = frozenset({-i, *key})
                if new_key_A not in memory:
                    out_cur = output(out_cur, cur)
                    memory[new_key_A] = cur
                    cur = OR(cur, i - 1, memory[key])
                if new_key_B not in memory:
                    out_cur = output(out_cur, cur)
                    memory[frozenset({-i, *key})] = cur
                    cur = OR(cur, memory[-i], memory[key])
                if len(key) == n - 1:
                    # print(f"{frozenset({i, *key})} and {frozenset({-i, *key})}")
                    # print(f"{i} and {key}")
                    res += 2
    # print(f"{res} DISJUNCTS FORMED")
    # sleep(2)
    # merge disjuncts
    for _ in range(2, (1 << n) + 1):
        keys = deepcopy(list(memory.keys()))
        for key in keys:
            if isinstance(key, int) or (len(key) < n and not iscomposite(key)):
                continue
            neighb_keys = deepcopy(list(memory.keys()))
            for neighb in neighb_keys:
                # filter out too small disjuncts or the ones already
                # containing current variabels or its negation
                if isinstance(neighb, int) or (
                    len(neighb) < n and not iscomposite(neighb)
                ):
                    continue
                cur_merge = None
                if not iscomposite(neighb) and iscomposite(key):
                    cur_merge = frozenset({neighb, *key})
                elif not iscomposite(key) and iscomposite(neighb):
                    cur_merge = frozenset({*neighb, key})
                elif iscomposite(key) and iscomposite(neighb):
                    cur_merge = frozenset({*neighb, *key})
                else:
                    cur_merge = frozenset({key, neighb})
                if isconstant(n, cur_merge):
                    continue
                to_continue = False
                for i in range(1, n + 1):
                    if are_equal(n, cur_merge, i):
                        to_continue = True
                        break
                if to_continue:
                    continue
                for k in memory.keys():
                    if are_equal(n, cur_merge, k):
                        to_continue = True
                        break
                if to_continue:
                    continue

                out_cur = output(out_cur, cur)
                memory[cur_merge] = cur
                cur = AND(cur, memory[key], memory[neighb])
                if out_cur == (1 << (1 << n)):
                    return res

    return res


if __name__ == "__main__":
    res = main()
    # print(f"{res} disjuncts were formed")