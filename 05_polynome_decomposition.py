import typing as tp
from sympy import gcd, Poly
from sympy.abc import x
from math import log2
from copy import deepcopy
import numpy as np  # for random nums

SEED = 42

def set_copy(inp_set: tp.Set[Poly]) -> tp.Set[Poly]:
    new_set = set()
    for item in inp_set:
        new_set.add(item)
    return new_set

class Solution:
    def __init__(self, p: int, d: int, n: int) -> None:
        self.p = p
        self.d = d
        self.n = n
        self.one = Poly(1, x, modulus=self.p)
        self.zero = Poly(0, x, modulus=self.p)
        self.rd_object = np.random.RandomState(seed=None)
        self.m = [
            Poly(x**3 + 2 * x**2 + 1, x, modulus=self.p),
            Poly(x**3 + 2 * x + 2, x, modulus=self.p),
            Poly(x**3 + x**2 + 2, x, modulus=self.p),
        ]
    
    def _refine(self, result: tp.Set[Poly], u: Poly, g: Poly):
        if g == self.zero:
            return
        GCD = gcd(g, u)
        # print(f"g: {g}")
        # print(f"u: {u}")
        # print(f"GCD: {GCD}")
        if GCD != self.one and GCD != u:
            result.remove(u)
            result.update({GCD, u.div(GCD)[0]})

    def solve(self, inp: tp.List[int]) -> tp.List[tp.List[int]]:
        f = self._list2poly(inp)
        result = {f}
        r = self.d // self.n
        while len(result) < r:
        # for _ in range(10):
            # print(f"Result: {result}")
            h = self._gen_poly()
            # print(f"h: {h}")
            g_pow = self._pow(h, f, (self.p**self.n - 1) // 2)
            # g_pow = (h ** ((self.p**self.n - 1) // 2)).div(f)[1]
            # g_pow_plus = (g_pow + self.one).div(f)[1].as_poly(modulus=self.p)
            g_pow_minus = (g_pow - self.one).div(f)[1].as_poly(modulus=self.p)
            # print(f"g^l - 1 mod f: {g_pow_minus}")
            # for i, m in enumerate(self.m):
            #     print(f"m_{i}: {m}")
            #     # g_pow = self._pow(h, m, (self.p**self.n - 1) // 2)
            #     # g_pow = h ** ((self.p**self.n - 1) // 2)
            #     g = (g_pow - self.one).div(m)[1].as_poly(modulus=self.p)
            #     print(f"g^l - 1 mod m_i: {g}")
            # if g_pow == self.zero or g_pow_minus == self.zero or g_pow_plus == self.zero:
            #     print(f"G_pow: {g_pow}")
            #     continue
            result_copy = set_copy(result)
            for u in result_copy:
                if u.degree() <= self.n:
                    continue
                # self._refine(result, u, g_pow)
                # self._refine(result, u, g_pow_plus)
                self._refine(result, u, g_pow_minus)
        return [self._poly2list(p) for p in result]

    def _gen_poly(self) -> Poly:
        # deg = self.rd_object.randint(0, self.d + 1)
        deg = self.n
        # deg = self.d - 1
        # coeffs = [1, *self.rd_object.randint(0, self.p, size=deg)]
        coeffs = list(self.rd_object.randint(0, self.p, size=deg + 1))
        return self._list2poly(coeffs)

    def _pow(self, exp: Poly, f: Poly, p: int) -> Poly:
        if p == 1:
            return exp
        if p == 2:
            return (exp * exp).div(f)[1]
        res = self.one
        binary = bin(p)[:1:-1]
        pows = {1: exp.div(f)[1]}
        if binary[0] == "1":
            res = pows[1]
        for i in range(1, len(binary)):
            pows[i + 1] = (pows[i] * pows[i]).div(f)[1]
            if binary[i] == "0":
                continue
            res = (res * pows[i + 1]).div(f)[1]
        return res

    def _list2poly(self, coeffs: tp.List[int]) -> Poly:
        exp = 0
        for i, c in enumerate(coeffs[::-1]):
            exp += c * (x**i)
        # check if constant
        if exp == coeffs[-1]:
            return Poly(coeffs[-1], x, modulus=self.p)
        return exp.as_poly(modulus=self.p)

    def _poly2list(self, polynom: Poly) -> tp.List[int]:
        coeffs = polynom.all_coeffs()
        result = []
        for c in coeffs:
            if c < 0:
                c = self.p + c
            result.append(c)
        return result


def main() -> None:
    p, d, n = [int(i) for i in str(input()).split()]
    input_coeffs = [int(i) for i in str(input()).split()]
    sol = Solution(p, d, n)
    res = sol.solve(input_coeffs)
    for ans in res:
        print(" ".join(str(i) for i in ans))


if __name__ == "__main__":
    main()