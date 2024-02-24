import numpy as np
import typing as tp


class Solution:
    def __init__(self, n: int) -> None:
        self.n = n
        self.q = n - 1

    def _legendre(self, i: int) -> int:
        if i == 0:
            return 0
        if i == 1:
            return 1
        if i < 0:
            i += self.q
        for j in range(2, self.q):
            if (j * j) % self.q == i:
                return 1
        return -1

    def _jacobsthal(self) -> np.array:
        Q = np.zeros((self.q, self.q), dtype=np.int32)
        for i in range(self.q):
            for j in range(self.q):
                Q[i, j] = self._legendre(i - j)
        return Q

    def _hadamart(self) -> np.array:
        I = np.eye(self.n, dtype=np.int32)
        H = np.zeros((self.n, self.n), dtype=np.int32)
        Q = self._jacobsthal()
        H[1:, 1:] = Q.copy()
        H[0, 1:] -= 1
        H[1:, 0] += 1
        return I + H

    def solve(self) -> None:
        H = self._hadamart()
        # print(H)
        H_inv = -1 * H[::-1].copy()
        codes = np.vstack((H, H_inv))
        codes -= 1
        codes //= -2
        for line in codes:
            print("".join([str(i) for i in line]))


def main() -> None:
    n = int(input())
    sol = Solution(n=n)
    sol.solve()


if __name__ == "__main__":
    main()