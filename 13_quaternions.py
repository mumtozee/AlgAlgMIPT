import numpy as np
import typing as tp


def get_quat(u: np.array, v: np.array) -> np.array:
    axis = np.cross(u, v)
    axis_norm = np.linalg.norm(axis)
    theta = np.arctan2(axis_norm, np.dot(u, v))
    axis /= np.linalg.norm(axis)
    return np.array([np.cos(theta / 2), *(np.sin(theta / 2) * axis)])


def quat2mat(q: np.array) -> np.array:
    a, b, c, d = q
    result = np.array([[a, -b, -c, -d], [b, a, -d, c], [c, d, a, -b], [d, -c, b, a]])
    return result


def conj(q: np.array) -> np.array:
    return np.array([q[0], -q[1], -q[2], -q[3]])


def mat2quat(mat: np.array) -> np.array:
    conj_q = mat[0].copy()
    return conj(conj_q)


def invert(q: np.array) -> np.array:
    norm = np.linalg.norm(q)
    return conj(q) / norm


def quat2axis(q: np.array) -> tp.Tuple[float, np.array]:
    v = q[1:].copy()
    a = q[0]
    v_norm = np.linalg.norm(v)
    q_norm = np.linalg.norm(q)
    axis = v / v_norm
    theta = 2 * np.arccos(np.clip(a / q_norm, -1.0, 1.0))
    return theta, axis


def compose_rotations(
    Rs: tp.List[tp.Tuple[tp.Tuple[float], tp.Tuple[float]]]
) -> np.array:
    R = np.eye(4)
    for ui, vi in Rs:
        ui = np.array(ui)
        vi = np.array(vi)
        ui /= np.linalg.norm(ui)
        vi /= np.linalg.norm(vi)
        q = get_quat(ui, vi)
        Q = quat2mat(q)
        R = np.matmul(np.matmul(Q, Q), R)
    return mat2quat(R)


def apply_rotation(q: np.array, w: np.array) -> np.array:
    q_inv = invert(q)
    R = quat2mat(q)
    R_inv = quat2mat(q_inv)
    V = quat2mat(np.array([0.0, w[0], w[1], w[2]]))
    return mat2quat(R @ V @ R_inv)[1:]


if __name__ == "__main__":
    Rs = []
    k = int(input())
    for _ in range(k):
        i1, j1, k1, i2, j2, k2 = [float(x) for x in input().split()]
        Rs.append(((i1, j1, k1), (i2, j2, k2)))
    w = np.array([float(x) for x in input().split()])
    q = compose_rotations(Rs)
    angle, axis = quat2axis(q)
    w_transformed = apply_rotation(q, w)
    for i in axis.tolist():
        print(i)
    print(angle)
    for i in w_transformed.tolist():
        print(i)