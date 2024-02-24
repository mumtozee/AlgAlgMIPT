import numpy as np
import warnings
import copy

warnings.filterwarnings(action="ignore")

import typing as tp


class Solution:
    def __init__(self, edges: tp.List[tp.Tuple[int, int]]) -> None:
        self.N = np.max(edges) + 1
        self.edges = edges

    def _laplacian(self) -> np.array:
        A = np.zeros((self.N, self.N), dtype=np.float32)
        D = np.zeros((self.N, self.N), dtype=np.float32)
        for a, b in self.edges:
            A[a, b] = 1.0
            A[b, a] = 1.0
            D[a, a] += 1.0
            D[b, b] += 1.0
        return D - A

    def _phi(self, A: tp.Set[int], B: tp.Set[int]) -> float:
        nom = 0.0
        for a, b in self.edges:
            if (a in A and b in B) or (a in B and b in A):
                nom += 1.0
        return self.N * nom / (len(A) * len(B))

    def _less(self, A: tp.Set[int], B: tp.Set[int]) -> bool:
        if len(A) == len(B):
            cutA, cutB = np.sort(list(A)), np.sort(list(B))
            idx = np.where((cutA > cutB) != (cutA < cutB))[0][0]
            return cutA[idx] < cutB[idx]
        return len(A) < len(B)

    def solve(self) -> np.array:
        L = self._laplacian()
        _, vecs = np.linalg.eigh(L)
        # print(vals)
        vec = vecs[:, 1]
        # print(vec)
        tuples = []
        for i, val in enumerate(vec):
            tuples.append((val, -i))
        tuples.sort()
        idx = -np.array(tuples)[:, 1].astype(np.int32)[::-1]
        min_phi = float("inf")
        best_cut = set()
        for i in range(1, self.N):
            A = set(idx[:i].tolist())
            B = set(idx[i:].tolist())
            cur_phi = self._phi(A, B)
            if cur_phi < min_phi:
                min_phi = cur_phi
                if len(A) < len(B):
                    best_cut = copy.deepcopy(A)
                else:
                    best_cut = copy.deepcopy(B)
            elif cur_phi == min_phi:
                if self._less(A, best_cut):
                    best_cut = copy.deepcopy(A)
                if self._less(B, best_cut):
                    best_cut = copy.deepcopy(B)

        return np.sort(list(best_cut))


def main() -> None:
    M = int(input())
    edges = list()
    for _ in range(M):
        edge = input().split()
        edges.append((int(edge[0]), int(edge[1])))
    sol = Solution(edges)
    res = sol.solve()
    print(" ".join([str(i) for i in res]))


if __name__ == "__main__":
    main()