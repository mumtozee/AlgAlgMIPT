import typing as tp
from sympy import gcd, Poly
from sympy.abc import x
from math import log2

class Solution:
    def __init__(self, p: int, d: int) -> None:
        self.p = p
        self.d = d
        self.one = Poly(1, x, modulus=self.p)
        self.zero = Poly(0, x, modulus=self.p)

    def solve(self, inp: tp.Tuple[int]) -> tp.List[tp.List[int]]:
        i = 1
        S = set()
        f_star = self._list2poly(inp)
        while f_star.degree() >= 2 * i:
            x_poly = x.as_poly(modulus=self.p)
            x_p = self._pow(x_poly, f_star, self.p)
            x_p_d = self._x_p_d(x_p, i, f_star)
            # print(x_p, x_p_d)
            g = gcd(f_star, Poly(x_p_d - x_poly, x, modulus=self.p).div(f_star)[1])
            # print(g)
            if g != self.one:
                S.add((g, i))
                f_star = f_star.div(g)[0]
            i += 1
        if f_star != self.one:
            S.add((f_star, f_star.degree()))
        if len(S) == 0:
            S = set({(self._list2poly(inp), 1)})
        return [self._poly2list(p[0]) for p in S]

    def _list2poly(self, coeffs: tp.List[int]) -> Poly:
        exp = 0
        for i, c in enumerate(coeffs[::-1]):
            exp += c * (x ** i)
        return exp.as_poly(modulus=self.p)
    
    def _poly2list(self, polynom: Poly) -> tp.List[int]:
        coeffs = polynom.all_coeffs()
        result = []
        for c in coeffs:
            if c < 0:
                c = self.p + c
            result.append(c)
        return result
        # return [c if c < 0 else self.p + c for c in coeffs]
    
    def _pow(self, exp: Poly, f: Poly, p: int) -> Poly:
        if p == 1:
            return exp
        if p == 2:
            return (exp * exp).div(f)[1]
        
        base2 = int(log2(p))
        pows = {
            0: self.one,
            1: exp.div(f)[1]
        }
        for i in range(2, base2 + 2):
            pows[i] = (pows[i - 1] * pows[i - 1]).div(f)[1]
        res = self.one
        binary = bin(p)[:1:-1]
        for i, c in enumerate(binary):
            if c == "0":
                continue
            res = (res * pows[i + 1]).div(f)[1]
        return res

    def _x_p_d(self, x_p: Poly, d: int, f: Poly) -> Poly:
        res = x_p
        for _ in range(2, d + 1):
            res = self._pow(res, f, self.p)
        return res


def main() -> None:
    p, d = [int(i) for i in str(input()).split()]
    input_coeffs = [int(i) for i in str(input()).split()]
    sol = Solution(p, d)
    res = sol.solve(input_coeffs)
    for ans in res:
        print(" ".join(str(i) for i in ans))

if __name__ == "__main__":
    main()