import numpy as np
from sympy import Matrix, GF, shape
from sympy.polys.matrices import DomainMatrix

import typing as tp

P = 4447
SEED = 42


class Solution:
    def __init__(self, edges: tp.List[tp.List[int]], k: int = 10) -> None:
        self.edges = np.array(edges, dtype=np.int32)
        self.l_vertices = np.max(self.edges[:, 0]) + 1
        self.r_vertices = np.max(self.edges[:, 1]) + 1
        self.n_vertices = self.l_vertices + self.r_vertices
        self.rd_obj = np.random.RandomState(seed=SEED)
        self.M = self._build_adj_matrix()
        self.k = k

    def _build_adj_matrix(self) -> np.array:
        M = np.zeros(shape=(self.n_vertices, self.n_vertices), dtype=np.int32)
        for u, v in self.edges:
            M[u, self.l_vertices + v] = 1
            M[self.l_vertices + v, u] = 1
        return M

    def _is_singular(self, M: Matrix) -> bool:
        N = shape(M)[0]
        for i in range(N):
            if M.row(i)[i] == 0:
                return True
        return False

    def solve(self) -> bool:
        variables = self.rd_obj.randint(
            low=0, high=P, size=(self.k, self.n_vertices), dtype=np.int32
        )
        for vars_ in variables:
            vars_ = vars_.reshape((1, -1))
            M_x = (vars_.T @ vars_) % P
            dom_M = DomainMatrix(
                (self.M * M_x).tolist(),
                (self.n_vertices, self.n_vertices),
                domain=GF(P),
            )
            L, U, _ = dom_M.lu()
            L, U = L.to_Matrix(), U.to_Matrix()
            if not self._is_singular(L) and not self._is_singular(U):
                return True
        return False


def main() -> None:
    n_edges = int(input())
    edges = []
    for i in range(n_edges):
        edges.append([int(item) for item in input().split()])
    sol = Solution(edges=edges, k=10)
    if sol.solve():
        print("yes")
    else:
        print("no")


if __name__ == "__main__":
    main()