import numpy as np
from scipy.optimize import linprog
from scipy.sparse import dok_matrix
import warnings
warnings.filterwarnings(action="ignore")

import typing as tp


class Solution:
    def __init__(
        self, costs: tp.List[float], edges: tp.List[tp.Tuple[int, int]]
    ) -> None:
        self.N = len(costs)
        self.edges = edges
        self.costs = np.array([costs], dtype=np.float32)

    def _get_Aub(self) -> tp.Tuple[dok_matrix, np.array]:
        Aub = dok_matrix((len(self.edges), self.N), dtype=np.float32)
        bub = np.zeros(
            (len(self.edges),),
            dtype=np.float32,
        )
        for i, edge in enumerate(self.edges):
            Aub[i, edge[0]] = -1.0
            Aub[i, edge[1]] = -1.0
            bub[i] = -1.0
        return Aub, bub

    def solve(self) -> tp.List[int]:
        result = []
        Aub, bub = self._get_Aub()
        options = {"sparse": True, "tol": 1e-2}
        x = linprog(
            c=self.costs,
            A_ub=Aub,
            b_ub=bub,
            bounds=(0.0, 1.0),
            method="interior-point",
            options=options,
        ).x
        for i in range(self.N):
            if x[i] >= 0.5:
                result.append(i)
        return result


def main() -> None:
    N = int(input())
    costs = []
    for i in range(N):
        costs.append(float(input()))
    M = int(input())
    edges = []
    for i in range(M):
        edge = input().split()
        edges.append([int(edge[0]), int(edge[1])])
    sol = Solution(costs, edges)
    res = sol.solve()
    print(" ".join([str(i) for i in res]))


if __name__ == "__main__":
    main()