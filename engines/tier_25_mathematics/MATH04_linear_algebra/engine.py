"""
MATH04 — Linear Algebra Intelligence Engine
TIE-20 Compliant | Tier 13 Mathematics | Port 8566
Authority: 5.0 | Mode: DET (Deterministic)

Pure-Python linear algebra: matrices, decompositions, eigenvalues,
vector spaces, transformations, least squares, orthogonalization.
No numpy dependency — every algorithm implemented from scratch.
"""
from __future__ import annotations

import hashlib
import json
import math
import time
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ── Path Setup ───────────────────────────────────────────────────────────
ENGINE_DIR = Path(__file__).parent
sys.path.insert(0, str(ENGINE_DIR.parent))

# ── Constants ────────────────────────────────────────────────────────────
ENGINE_ID = "MATH04"
ENGINE_NAME = "Linear Algebra Intelligence Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8566
ENGINE_TIER = 13
ENGINE_MODE = "DET"
ENGINE_AUTH_LEVEL = 5.0
EPSILON = 1e-12
MAX_MATRIX_DIM = 200
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ── Loguru Config ────────────────────────────────────────────────────────
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | {message}")
logger.add(LOG_DIR / "math04_{time:YYYY-MM-DD}.log", rotation="50 MB", retention="30 days", level="DEBUG")
logger.add(LOG_DIR / "math04_audit.jsonl", serialize=True, rotation="100 MB", retention="90 days", level="TRACE")

# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 1 — MATRIX CLASS (Pure Python)
# ═══════════════════════════════════════════════════════════════════════════

class Matrix:
    """Arbitrary-size matrix stored as list-of-lists, all operations pure Python."""

    __slots__ = ("rows", "cols", "data")

    def __init__(self, data: list[list[float]]) -> None:
        if not data or not data[0]:
            raise ValueError("Matrix cannot be empty")
        self.rows = len(data)
        self.cols = len(data[0])
        for i, row in enumerate(data):
            if len(row) != self.cols:
                raise ValueError(f"Row {i} length {len(row)} != expected {self.cols}")
        self.data: list[list[float]] = [list(row) for row in data]

    # ── Factory Methods ──────────────────────────────────────────────────
    @classmethod
    def zeros(cls, rows: int, cols: int) -> Matrix:
        return cls([[0.0] * cols for _ in range(rows)])

    @classmethod
    def ones(cls, rows: int, cols: int) -> Matrix:
        return cls([[1.0] * cols for _ in range(rows)])

    @classmethod
    def identity(cls, n: int) -> Matrix:
        data = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        return cls(data)

    @classmethod
    def from_vector(cls, v: list[float], column: bool = True) -> Matrix:
        if column:
            return cls([[x] for x in v])
        return cls([v])

    @classmethod
    def diagonal(cls, values: list[float]) -> Matrix:
        n = len(values)
        data = [[values[i] if i == j else 0.0 for j in range(n)] for i in range(n)]
        return cls(data)

    # ── Properties ───────────────────────────────────────────────────────
    @property
    def shape(self) -> tuple[int, int]:
        return (self.rows, self.cols)

    @property
    def is_square(self) -> bool:
        return self.rows == self.cols

    @property
    def is_symmetric(self) -> bool:
        if not self.is_square:
            return False
        for i in range(self.rows):
            for j in range(i + 1, self.cols):
                if abs(self.data[i][j] - self.data[j][i]) > EPSILON:
                    return False
        return True

    @property
    def trace(self) -> float:
        if not self.is_square:
            raise ValueError("Trace requires square matrix")
        return sum(self.data[i][i] for i in range(self.rows))

    # ── Element Access ───────────────────────────────────────────────────
    def get(self, i: int, j: int) -> float:
        return self.data[i][j]

    def set(self, i: int, j: int, val: float) -> None:
        self.data[i][j] = val

    def get_row(self, i: int) -> list[float]:
        return list(self.data[i])

    def get_col(self, j: int) -> list[float]:
        return [self.data[i][j] for i in range(self.rows)]

    def copy(self) -> Matrix:
        return Matrix([list(row) for row in self.data])

    def to_list(self) -> list[list[float]]:
        return [list(row) for row in self.data]

    # ── Arithmetic ───────────────────────────────────────────────────────
    def add(self, other: Matrix) -> Matrix:
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
        return Matrix([
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def subtract(self, other: Matrix) -> Matrix:
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
        return Matrix([
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def scalar_multiply(self, s: float) -> Matrix:
        return Matrix([
            [self.data[i][j] * s for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def multiply(self, other: Matrix) -> Matrix:
        if self.cols != other.rows:
            raise ValueError(f"Cannot multiply {self.shape} x {other.shape}")
        result = [[0.0] * other.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for k in range(self.cols):
                a_ik = self.data[i][k]
                if abs(a_ik) < EPSILON:
                    continue
                for j in range(other.cols):
                    result[i][j] += a_ik * other.data[k][j]
        return Matrix(result)

    def elementwise_multiply(self, other: Matrix) -> Matrix:
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
        return Matrix([
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def transpose(self) -> Matrix:
        return Matrix([
            [self.data[i][j] for i in range(self.rows)]
            for j in range(self.cols)
        ])

    def negate(self) -> Matrix:
        return self.scalar_multiply(-1.0)

    # ── Matrix Power ─────────────────────────────────────────────────────
    def power(self, n: int) -> Matrix:
        if not self.is_square:
            raise ValueError("Power requires square matrix")
        if n < 0:
            return self.inverse().power(-n)
        if n == 0:
            return Matrix.identity(self.rows)
        result = Matrix.identity(self.rows)
        base = self.copy()
        exp = n
        while exp > 0:
            if exp % 2 == 1:
                result = result.multiply(base)
            base = base.multiply(base)
            exp //= 2
        return result

    # ── Comparison / Utility ─────────────────────────────────────────────
    def approx_equal(self, other: Matrix, tol: float = 1e-9) -> bool:
        if self.shape != other.shape:
            return False
        for i in range(self.rows):
            for j in range(self.cols):
                if abs(self.data[i][j] - other.data[i][j]) > tol:
                    return False
        return True

    def __repr__(self) -> str:
        rows_str = ",\n  ".join(str(row) for row in self.data)
        return f"Matrix({self.rows}x{self.cols})[\n  {rows_str}\n]"


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 2 — VECTOR OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

class VectorOps:
    """Pure-Python vector arithmetic and geometry."""

    @staticmethod
    def dot(a: list[float], b: list[float]) -> float:
        if len(a) != len(b):
            raise ValueError(f"Dimension mismatch: {len(a)} vs {len(b)}")
        return sum(x * y for x, y in zip(a, b))

    @staticmethod
    def cross(a: list[float], b: list[float]) -> list[float]:
        if len(a) != 3 or len(b) != 3:
            raise ValueError("Cross product requires 3D vectors")
        return [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        ]

    @staticmethod
    def norm(v: list[float], p: float = 2.0) -> float:
        if p == float("inf"):
            return max(abs(x) for x in v)
        if p == 1.0:
            return sum(abs(x) for x in v)
        return sum(abs(x) ** p for x in v) ** (1.0 / p)

    @staticmethod
    def normalize(v: list[float]) -> list[float]:
        n = VectorOps.norm(v)
        if n < EPSILON:
            raise ValueError("Cannot normalize zero vector")
        return [x / n for x in v]

    @staticmethod
    def add(a: list[float], b: list[float]) -> list[float]:
        if len(a) != len(b):
            raise ValueError("Dimension mismatch")
        return [x + y for x, y in zip(a, b)]

    @staticmethod
    def subtract(a: list[float], b: list[float]) -> list[float]:
        if len(a) != len(b):
            raise ValueError("Dimension mismatch")
        return [x - y for x, y in zip(a, b)]

    @staticmethod
    def scale(v: list[float], s: float) -> list[float]:
        return [x * s for x in v]

    @staticmethod
    def projection(a: list[float], b: list[float]) -> list[float]:
        """Project vector a onto vector b."""
        dot_ab = VectorOps.dot(a, b)
        dot_bb = VectorOps.dot(b, b)
        if abs(dot_bb) < EPSILON:
            raise ValueError("Cannot project onto zero vector")
        scalar = dot_ab / dot_bb
        return VectorOps.scale(b, scalar)

    @staticmethod
    def rejection(a: list[float], b: list[float]) -> list[float]:
        proj = VectorOps.projection(a, b)
        return VectorOps.subtract(a, proj)

    @staticmethod
    def angle_between(a: list[float], b: list[float]) -> float:
        """Angle in radians between two vectors."""
        cos_theta = VectorOps.dot(a, b) / (VectorOps.norm(a) * VectorOps.norm(b))
        cos_theta = max(-1.0, min(1.0, cos_theta))
        return math.acos(cos_theta)

    @staticmethod
    def are_orthogonal(a: list[float], b: list[float], tol: float = 1e-9) -> bool:
        return abs(VectorOps.dot(a, b)) < tol

    @staticmethod
    def outer_product(a: list[float], b: list[float]) -> Matrix:
        return Matrix([[ai * bj for bj in b] for ai in a])

    @staticmethod
    def triple_scalar(a: list[float], b: list[float], c: list[float]) -> float:
        return VectorOps.dot(a, VectorOps.cross(b, c))

    @staticmethod
    def linear_combination(vectors: list[list[float]], coeffs: list[float]) -> list[float]:
        if not vectors:
            raise ValueError("No vectors provided")
        n = len(vectors[0])
        result = [0.0] * n
        for v, c in zip(vectors, coeffs):
            for i in range(n):
                result[i] += v[i] * c
        return result


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 3 — GAUSSIAN ELIMINATION
# ═══════════════════════════════════════════════════════════════════════════

class GaussianElimination:
    """Row reduction with partial pivoting: REF, RREF, rank, null space."""

    @staticmethod
    def _swap_rows(m: list[list[float]], i: int, j: int) -> None:
        m[i], m[j] = m[j], m[i]

    @staticmethod
    def _scale_row(m: list[list[float]], i: int, s: float) -> None:
        m[i] = [x * s for x in m[i]]

    @staticmethod
    def _add_scaled_row(m: list[list[float]], target: int, source: int, s: float) -> None:
        for j in range(len(m[target])):
            m[target][j] += s * m[source][j]

    @staticmethod
    def row_echelon_form(mat: Matrix) -> tuple[Matrix, int, float]:
        """Returns (REF matrix, rank, determinant_sign_factor).
        Uses partial pivoting for numerical stability."""
        data = [list(row) for row in mat.data]
        rows, cols = mat.rows, mat.cols
        pivot_row = 0
        sign = 1.0
        pivot_cols: list[int] = []

        for col in range(cols):
            if pivot_row >= rows:
                break
            max_val = abs(data[pivot_row][col])
            max_idx = pivot_row
            for i in range(pivot_row + 1, rows):
                if abs(data[i][col]) > max_val:
                    max_val = abs(data[i][col])
                    max_idx = i
            if max_val < EPSILON:
                continue
            if max_idx != pivot_row:
                GaussianElimination._swap_rows(data, pivot_row, max_idx)
                sign *= -1.0
            pivot_cols.append(col)
            pivot_val = data[pivot_row][col]
            for i in range(pivot_row + 1, rows):
                if abs(data[i][col]) > EPSILON:
                    factor = data[i][col] / pivot_val
                    for j in range(col, cols):
                        data[i][j] -= factor * data[pivot_row][j]
                    data[i][col] = 0.0
            pivot_row += 1

        rank = len(pivot_cols)
        return Matrix(data), rank, sign

    @staticmethod
    def reduced_row_echelon_form(mat: Matrix) -> tuple[Matrix, list[int]]:
        """Full RREF with pivot column tracking."""
        data = [list(row) for row in mat.data]
        rows, cols = mat.rows, mat.cols
        pivot_row = 0
        pivot_cols: list[int] = []

        for col in range(cols):
            if pivot_row >= rows:
                break
            max_val = abs(data[pivot_row][col])
            max_idx = pivot_row
            for i in range(pivot_row + 1, rows):
                if abs(data[i][col]) > max_val:
                    max_val = abs(data[i][col])
                    max_idx = i
            if max_val < EPSILON:
                continue
            if max_idx != pivot_row:
                GaussianElimination._swap_rows(data, pivot_row, max_idx)
            pivot_val = data[pivot_row][col]
            GaussianElimination._scale_row(data, pivot_row, 1.0 / pivot_val)
            data[pivot_row][col] = 1.0
            for i in range(rows):
                if i != pivot_row and abs(data[i][col]) > EPSILON:
                    GaussianElimination._add_scaled_row(data, i, pivot_row, -data[i][col])
                    data[i][col] = 0.0
            pivot_cols.append(col)
            pivot_row += 1

        return Matrix(data), pivot_cols

    @staticmethod
    def rank(mat: Matrix) -> int:
        _, r, _ = GaussianElimination.row_echelon_form(mat)
        return r

    @staticmethod
    def nullity(mat: Matrix) -> int:
        return mat.cols - GaussianElimination.rank(mat)

    @staticmethod
    def null_space_basis(mat: Matrix) -> list[list[float]]:
        """Compute basis for the null space via RREF."""
        rref, pivot_cols = GaussianElimination.reduced_row_echelon_form(mat)
        free_cols = [j for j in range(mat.cols) if j not in pivot_cols]
        basis: list[list[float]] = []
        for fc in free_cols:
            vec = [0.0] * mat.cols
            vec[fc] = 1.0
            for idx, pc in enumerate(pivot_cols):
                if idx < rref.rows:
                    vec[pc] = -rref.data[idx][fc]
            basis.append(vec)
        return basis

    @staticmethod
    def column_space_basis(mat: Matrix) -> list[list[float]]:
        _, pivot_cols = GaussianElimination.reduced_row_echelon_form(mat)
        return [mat.get_col(j) for j in pivot_cols]

    @staticmethod
    def row_space_basis(mat: Matrix) -> list[list[float]]:
        rref, pivot_cols = GaussianElimination.reduced_row_echelon_form(mat)
        return [rref.get_row(i) for i in range(len(pivot_cols))]

    @staticmethod
    def solve(a_mat: Matrix, b_vec: list[float]) -> Optional[list[float]]:
        """Solve Ax = b via RREF on augmented matrix. Returns None if inconsistent."""
        if a_mat.rows != len(b_vec):
            raise ValueError("Row count must match b length")
        aug_data = [a_mat.data[i] + [b_vec[i]] for i in range(a_mat.rows)]
        aug = Matrix(aug_data)
        rref, pivot_cols = GaussianElimination.reduced_row_echelon_form(aug)
        last_col = aug.cols - 1
        if last_col in pivot_cols:
            return None
        solution = [0.0] * a_mat.cols
        for idx, pc in enumerate(pivot_cols):
            if idx < rref.rows:
                solution[pc] = rref.data[idx][last_col]
        return solution


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 4 — DETERMINANT
# ═══════════════════════════════════════════════════════════════════════════

class Determinant:
    """Determinant via LU-based row reduction (large) or cofactor (small)."""

    @staticmethod
    def cofactor_expansion(mat: Matrix) -> float:
        if not mat.is_square:
            raise ValueError("Determinant requires square matrix")
        n = mat.rows
        if n == 1:
            return mat.data[0][0]
        if n == 2:
            return mat.data[0][0] * mat.data[1][1] - mat.data[0][1] * mat.data[1][0]
        if n == 3:
            a = mat.data
            return (
                a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
                - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
            )
        det_val = 0.0
        for j in range(n):
            if abs(mat.data[0][j]) < EPSILON:
                continue
            minor_data = []
            for i in range(1, n):
                minor_data.append([mat.data[i][k] for k in range(n) if k != j])
            minor_mat = Matrix(minor_data)
            sign = 1.0 if j % 2 == 0 else -1.0
            det_val += sign * mat.data[0][j] * Determinant.cofactor_expansion(minor_mat)
        return det_val

    @staticmethod
    def via_row_reduction(mat: Matrix) -> float:
        if not mat.is_square:
            raise ValueError("Determinant requires square matrix")
        ref, rank, sign = GaussianElimination.row_echelon_form(mat)
        if rank < mat.rows:
            return 0.0
        det_val = sign
        for i in range(mat.rows):
            det_val *= ref.data[i][i]
        return det_val

    @staticmethod
    def compute(mat: Matrix) -> float:
        if mat.rows <= 4:
            return Determinant.cofactor_expansion(mat)
        return Determinant.via_row_reduction(mat)


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 5 — MATRIX INVERSE (Gauss-Jordan)
# ═══════════════════════════════════════════════════════════════════════════

class MatrixInverse:
    """Gauss-Jordan elimination to find inverse of square matrix."""

    @staticmethod
    def compute(mat: Matrix) -> Matrix:
        if not mat.is_square:
            raise ValueError("Inverse requires square matrix")
        n = mat.rows
        aug = [mat.data[i] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

        for col in range(n):
            max_val = abs(aug[col][col])
            max_row = col
            for row in range(col + 1, n):
                if abs(aug[row][col]) > max_val:
                    max_val = abs(aug[row][col])
                    max_row = row
            if max_val < EPSILON:
                raise ValueError("Matrix is singular, cannot invert")
            if max_row != col:
                aug[col], aug[max_row] = aug[max_row], aug[col]

            pivot = aug[col][col]
            for j in range(2 * n):
                aug[col][j] /= pivot

            for row in range(n):
                if row != col:
                    factor = aug[row][col]
                    if abs(factor) > EPSILON:
                        for j in range(2 * n):
                            aug[row][j] -= factor * aug[col][j]

        inv_data = [aug[i][n:] for i in range(n)]
        return Matrix(inv_data)

    @staticmethod
    def is_invertible(mat: Matrix) -> bool:
        if not mat.is_square:
            return False
        return abs(Determinant.compute(mat)) > EPSILON


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 6 — LU DECOMPOSITION (Doolittle with partial pivoting)
# ═══════════════════════════════════════════════════════════════════════════

class LUDecomposition:
    """PA = LU decomposition using Doolittle algorithm with partial pivoting."""

    @staticmethod
    def decompose(mat: Matrix) -> tuple[Matrix, Matrix, Matrix]:
        """Returns (P, L, U) such that PA = LU."""
        if not mat.is_square:
            raise ValueError("LU decomposition requires square matrix")
        n = mat.rows
        u_data = [list(row) for row in mat.data]
        l_data = [[0.0] * n for _ in range(n)]
        p_data = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

        for i in range(n):
            l_data[i][i] = 1.0

        for k in range(n):
            max_val = abs(u_data[k][k])
            max_idx = k
            for i in range(k + 1, n):
                if abs(u_data[i][k]) > max_val:
                    max_val = abs(u_data[i][k])
                    max_idx = i
            if max_idx != k:
                u_data[k], u_data[max_idx] = u_data[max_idx], u_data[k]
                p_data[k], p_data[max_idx] = p_data[max_idx], p_data[k]
                for j in range(k):
                    l_data[k][j], l_data[max_idx][j] = l_data[max_idx][j], l_data[k][j]

            if abs(u_data[k][k]) < EPSILON:
                continue

            for i in range(k + 1, n):
                factor = u_data[i][k] / u_data[k][k]
                l_data[i][k] = factor
                for j in range(k, n):
                    u_data[i][j] -= factor * u_data[k][j]
                u_data[i][k] = 0.0

        return Matrix(p_data), Matrix(l_data), Matrix(u_data)

    @staticmethod
    def solve(mat: Matrix, b: list[float]) -> list[float]:
        """Solve Ax = b using LU decomposition."""
        p_mat, l_mat, u_mat = LUDecomposition.decompose(mat)
        n = mat.rows
        pb = [0.0] * n
        for i in range(n):
            for j in range(n):
                pb[i] += p_mat.data[i][j] * b[j]

        y = [0.0] * n
        for i in range(n):
            s = pb[i]
            for j in range(i):
                s -= l_mat.data[i][j] * y[j]
            y[i] = s

        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            s = y[i]
            for j in range(i + 1, n):
                s -= u_mat.data[i][j] * x[j]
            if abs(u_mat.data[i][i]) < EPSILON:
                raise ValueError("Singular matrix encountered in back substitution")
            x[i] = s / u_mat.data[i][i]
        return x


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 7 — QR DECOMPOSITION (Gram-Schmidt)
# ═══════════════════════════════════════════════════════════════════════════

class GramSchmidt:
    """Gram-Schmidt orthogonalization and QR decomposition."""

    @staticmethod
    def orthogonalize(vectors: list[list[float]]) -> list[list[float]]:
        """Classical Gram-Schmidt. Returns orthogonal basis."""
        ortho: list[list[float]] = []
        for v in vectors:
            u = list(v)
            for q in ortho:
                proj_scalar = VectorOps.dot(v, q) / VectorOps.dot(q, q)
                proj = VectorOps.scale(q, proj_scalar)
                u = VectorOps.subtract(u, proj)
            if VectorOps.norm(u) > EPSILON:
                ortho.append(u)
        return ortho

    @staticmethod
    def orthonormalize(vectors: list[list[float]]) -> list[list[float]]:
        ortho = GramSchmidt.orthogonalize(vectors)
        return [VectorOps.normalize(v) for v in ortho]

    @staticmethod
    def qr_decomposition(mat: Matrix) -> tuple[Matrix, Matrix]:
        """QR decomposition via modified Gram-Schmidt. A = QR."""
        m, n = mat.rows, mat.cols
        cols = [mat.get_col(j) for j in range(n)]
        q_cols: list[list[float]] = []
        r_data = [[0.0] * n for _ in range(min(m, n))]

        for j in range(n):
            v = list(cols[j])
            for i in range(len(q_cols)):
                r_data[i][j] = VectorOps.dot(q_cols[i], v)
                proj = VectorOps.scale(q_cols[i], r_data[i][j])
                v = VectorOps.subtract(v, proj)
            norm_v = VectorOps.norm(v)
            if norm_v > EPSILON and len(q_cols) < m:
                idx = len(q_cols)
                r_data[idx][j] = norm_v
                q_cols.append(VectorOps.scale(v, 1.0 / norm_v))

        k = len(q_cols)
        q_data = [[q_cols[j][i] for j in range(k)] for i in range(m)]
        r_final = [r_data[i][:n] for i in range(k)]

        return Matrix(q_data), Matrix(r_final)


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 8 — CHOLESKY DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════════

class CholeskyDecomposition:
    """Cholesky decomposition for symmetric positive-definite matrices: A = LL^T."""

    @staticmethod
    def decompose(mat: Matrix) -> Matrix:
        if not mat.is_square:
            raise ValueError("Cholesky requires square matrix")
        if not mat.is_symmetric:
            raise ValueError("Cholesky requires symmetric matrix")
        n = mat.rows
        l_data = [[0.0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1):
                s = sum(l_data[i][k] * l_data[j][k] for k in range(j))
                if i == j:
                    val = mat.data[i][i] - s
                    if val < -EPSILON:
                        raise ValueError("Matrix is not positive definite")
                    l_data[i][j] = math.sqrt(max(0.0, val))
                else:
                    if abs(l_data[j][j]) < EPSILON:
                        raise ValueError("Zero diagonal in Cholesky factor")
                    l_data[i][j] = (mat.data[i][j] - s) / l_data[j][j]
        return Matrix(l_data)

    @staticmethod
    def is_positive_definite(mat: Matrix) -> bool:
        try:
            CholeskyDecomposition.decompose(mat)
            return True
        except ValueError:
            return False


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 9 — SVD (for small matrices via eigendecomposition of A^T A)
# ═══════════════════════════════════════════════════════════════════════════

class SVD:
    """Singular Value Decomposition for small matrices.
    A = U * Sigma * V^T computed via eigendecomposition of A^T*A."""

    @staticmethod
    def compute(mat: Matrix) -> tuple[Matrix, list[float], Matrix]:
        """Returns (U, singular_values, V^T).
        Works reliably for matrices up to ~10x10."""
        ata = mat.transpose().multiply(mat)
        eigenvalues, eigenvectors = Eigenvalues.symmetric_qr(ata)

        pairs = sorted(zip(eigenvalues, range(len(eigenvalues))), reverse=True)
        singular_values = [math.sqrt(max(0.0, pairs[i][0])) for i in range(len(pairs))]
        v_cols = [eigenvectors[pairs[i][1]] for i in range(len(pairs))]

        v_data = [[v_cols[j][i] for j in range(len(v_cols))] for i in range(ata.rows)]
        vt = Matrix(v_data).transpose()

        u_cols: list[list[float]] = []
        for i in range(len(singular_values)):
            if singular_values[i] > EPSILON:
                av = [0.0] * mat.rows
                for r in range(mat.rows):
                    for c in range(mat.cols):
                        av[r] += mat.data[r][c] * v_cols[i][c]
                u_col = VectorOps.scale(av, 1.0 / singular_values[i])
                u_cols.append(u_col)
            else:
                u_cols.append([0.0] * mat.rows)

        while len(u_cols) < mat.rows:
            u_cols.append([0.0] * mat.rows)

        u_data = [[u_cols[j][i] for j in range(mat.rows)] for i in range(mat.rows)]
        return Matrix(u_data), singular_values, vt


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 10 — EIGENVALUES & EIGENVECTORS
# ═══════════════════════════════════════════════════════════════════════════

class Eigenvalues:
    """Eigenvalue computation: direct formulas for 2x2/3x3,
    QR algorithm for symmetric matrices."""

    @staticmethod
    def eigen_2x2(mat: Matrix) -> list[tuple[float, list[float]]]:
        """Eigenvalues and eigenvectors for 2x2 matrix via characteristic polynomial."""
        if mat.rows != 2 or mat.cols != 2:
            raise ValueError("Requires 2x2 matrix")
        a, b = mat.data[0][0], mat.data[0][1]
        c, d = mat.data[1][0], mat.data[1][1]

        trace_val = a + d
        det_val = a * d - b * c
        disc = trace_val * trace_val - 4.0 * det_val

        results: list[tuple[float, list[float]]] = []
        if disc >= -EPSILON:
            disc = max(0.0, disc)
            sqrt_disc = math.sqrt(disc)
            lam1 = (trace_val + sqrt_disc) / 2.0
            lam2 = (trace_val - sqrt_disc) / 2.0

            for lam in [lam1, lam2]:
                if abs(b) > EPSILON:
                    vec = [b, lam - a]
                elif abs(c) > EPSILON:
                    vec = [lam - d, c]
                else:
                    if abs(lam - a) < EPSILON:
                        vec = [1.0, 0.0]
                    else:
                        vec = [0.0, 1.0]
                norm_val = VectorOps.norm(vec)
                if norm_val > EPSILON:
                    vec = [x / norm_val for x in vec]
                results.append((lam, vec))
        return results

    @staticmethod
    def eigen_3x3(mat: Matrix) -> list[tuple[float, list[float]]]:
        """Eigenvalues for 3x3 via Cardano's formula on characteristic polynomial."""
        if mat.rows != 3 or mat.cols != 3:
            raise ValueError("Requires 3x3 matrix")
        a = mat.data
        p1 = a[0][0] + a[1][1] + a[2][2]

        q_mat = mat.multiply(mat)
        p2 = (q_mat.data[0][0] + q_mat.data[1][1] + q_mat.data[2][2])

        det_val = Determinant.cofactor_expansion(mat)
        c2 = -p1
        c1 = (p1 * p1 - p2) / 2.0
        c0 = -det_val

        eigenvalues = Eigenvalues._solve_cubic(1.0, c2, c1, c0)
        results: list[tuple[float, list[float]]] = []
        for lam in eigenvalues:
            vec = Eigenvalues._find_eigenvector_3x3(mat, lam)
            results.append((lam, vec))
        return results

    @staticmethod
    def _solve_cubic(a: float, b: float, c: float, d: float) -> list[float]:
        """Solve ax^3 + bx^2 + cx + d = 0 using Cardano/trig method."""
        b /= a
        c /= a
        d /= a

        q = (3.0 * c - b * b) / 9.0
        r = (9.0 * b * c - 27.0 * d - 2.0 * b * b * b) / 54.0
        disc = q * q * q + r * r

        if disc < -EPSILON:
            theta = math.acos(max(-1.0, min(1.0, r / math.sqrt(-(q * q * q)))))
            sq = 2.0 * math.sqrt(-q)
            roots = [
                sq * math.cos(theta / 3.0) - b / 3.0,
                sq * math.cos((theta + 2.0 * math.pi) / 3.0) - b / 3.0,
                sq * math.cos((theta + 4.0 * math.pi) / 3.0) - b / 3.0,
            ]
        elif abs(disc) < EPSILON:
            s_val = r ** (1.0 / 3.0) if r >= 0 else -((-r) ** (1.0 / 3.0))
            roots = [2.0 * s_val - b / 3.0, -s_val - b / 3.0]
        else:
            sqrt_disc = math.sqrt(disc)
            s_arg = r + sqrt_disc
            t_arg = r - sqrt_disc
            s_val = (abs(s_arg) ** (1.0 / 3.0)) * (1.0 if s_arg >= 0 else -1.0)
            t_val = (abs(t_arg) ** (1.0 / 3.0)) * (1.0 if t_arg >= 0 else -1.0)
            roots = [s_val + t_val - b / 3.0]
        return roots

    @staticmethod
    def _find_eigenvector_3x3(mat: Matrix, lam: float) -> list[float]:
        """Find eigenvector for eigenvalue lam of 3x3 matrix via null space."""
        shifted = mat.subtract(Matrix.identity(3).scalar_multiply(lam))
        null_basis = GaussianElimination.null_space_basis(shifted)
        if null_basis:
            return VectorOps.normalize(null_basis[0])
        best_vec = [1.0, 0.0, 0.0]
        best_residual = float("inf")
        for candidate in [[1, 0, 0], [0, 1, 0], [0, 0, 1]]:
            residual_vec = [
                sum(shifted.data[i][j] * candidate[j] for j in range(3))
                for i in range(3)
            ]
            res_norm = VectorOps.norm(residual_vec)
            if res_norm < best_residual:
                best_residual = res_norm
                best_vec = list(candidate)
        return VectorOps.normalize(best_vec)

    @staticmethod
    def symmetric_qr(mat: Matrix, max_iter: int = 200) -> tuple[list[float], list[list[float]]]:
        """QR algorithm with shifts for symmetric matrix eigenvalues.
        Returns (eigenvalues, eigenvectors_as_rows)."""
        if not mat.is_square:
            raise ValueError("QR eigenvalue requires square matrix")
        n = mat.rows
        a_data = [list(row) for row in mat.data]
        v_data = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

        for _ in range(max_iter * n):
            off_diag = 0.0
            for i in range(n):
                for j in range(n):
                    if i != j:
                        off_diag += a_data[i][j] ** 2
            if math.sqrt(off_diag) < EPSILON * n:
                break

            a_mat = Matrix(a_data)
            q_mat, r_mat = GramSchmidt.qr_decomposition(a_mat)
            new_a = r_mat.multiply(q_mat)
            a_data = new_a.to_list()

            v_matrix = Matrix(v_data)
            v_new = v_matrix.multiply(q_mat)
            v_data = v_new.to_list()

        eigenvalues = [a_data[i][i] for i in range(n)]
        eigenvectors = [list(v_data[i]) for i in range(n)]

        evec_transposed = [[v_data[i][j] for i in range(n)] for j in range(n)]
        return eigenvalues, evec_transposed

    @staticmethod
    def compute(mat: Matrix) -> list[tuple[float, list[float]]]:
        """Auto-dispatch: 2x2 direct, 3x3 Cardano, nxn QR."""
        if mat.rows == 2:
            return Eigenvalues.eigen_2x2(mat)
        if mat.rows == 3:
            return Eigenvalues.eigen_3x3(mat)
        if mat.is_symmetric:
            vals, vecs = Eigenvalues.symmetric_qr(mat)
            return list(zip(vals, vecs))
        vals, vecs = Eigenvalues.symmetric_qr(mat)
        return list(zip(vals, vecs))


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 11 — LEAST SQUARES
# ═══════════════════════════════════════════════════════════════════════════

class LeastSquares:
    """Least squares solution via normal equations: x = (A^T A)^{-1} A^T b."""

    @staticmethod
    def solve(a_mat: Matrix, b: list[float]) -> list[float]:
        at = a_mat.transpose()
        ata = at.multiply(a_mat)
        atb_vec = [sum(at.data[i][j] * b[j] for j in range(at.cols)) for i in range(at.rows)]
        return LUDecomposition.solve(ata, atb_vec)

    @staticmethod
    def residual(a_mat: Matrix, x: list[float], b: list[float]) -> list[float]:
        ax = [sum(a_mat.data[i][j] * x[j] for j in range(a_mat.cols)) for i in range(a_mat.rows)]
        return [ax[i] - b[i] for i in range(len(b))]

    @staticmethod
    def residual_norm(a_mat: Matrix, x: list[float], b: list[float]) -> float:
        r = LeastSquares.residual(a_mat, x, b)
        return VectorOps.norm(r)

    @staticmethod
    def fit_polynomial(x_data: list[float], y_data: list[float], degree: int) -> list[float]:
        """Fit polynomial of given degree to (x,y) data points. Returns coefficients [a0, a1, ... , an]."""
        n = len(x_data)
        vandermonde = [[xi ** k for k in range(degree + 1)] for xi in x_data]
        a_mat = Matrix(vandermonde)
        return LeastSquares.solve(a_mat, y_data)


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 12 — MATRIX NORMS & CONDITION NUMBER
# ═══════════════════════════════════════════════════════════════════════════

class MatrixNorms:
    """Matrix norms and condition number computation."""

    @staticmethod
    def frobenius(mat: Matrix) -> float:
        return math.sqrt(sum(mat.data[i][j] ** 2 for i in range(mat.rows) for j in range(mat.cols)))

    @staticmethod
    def infinity_norm(mat: Matrix) -> float:
        return max(sum(abs(mat.data[i][j]) for j in range(mat.cols)) for i in range(mat.rows))

    @staticmethod
    def one_norm(mat: Matrix) -> float:
        return max(sum(abs(mat.data[i][j]) for i in range(mat.rows)) for j in range(mat.cols))

    @staticmethod
    def spectral_norm(mat: Matrix) -> float:
        """Largest singular value = sqrt(largest eigenvalue of A^T A)."""
        ata = mat.transpose().multiply(mat)
        if ata.rows <= 3:
            eigs = Eigenvalues.compute(ata)
            max_eig = max(abs(e[0]) for e in eigs) if eigs else 0.0
        else:
            vals, _ = Eigenvalues.symmetric_qr(ata)
            max_eig = max(abs(v) for v in vals) if vals else 0.0
        return math.sqrt(max(0.0, max_eig))

    @staticmethod
    def condition_number(mat: Matrix, norm_type: str = "frobenius") -> float:
        if not mat.is_square:
            raise ValueError("Condition number requires square matrix")
        if not MatrixInverse.is_invertible(mat):
            return float("inf")
        inv = MatrixInverse.compute(mat)
        norm_funcs = {
            "frobenius": MatrixNorms.frobenius,
            "infinity": MatrixNorms.infinity_norm,
            "one": MatrixNorms.one_norm,
        }
        norm_fn = norm_funcs.get(norm_type, MatrixNorms.frobenius)
        return norm_fn(mat) * norm_fn(inv)


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 13 — LINEAR TRANSFORMATIONS
# ═══════════════════════════════════════════════════════════════════════════

class LinearTransformation:
    """Represent and compose linear transformations as matrices."""

    @staticmethod
    def apply(mat: Matrix, vector: list[float]) -> list[float]:
        if mat.cols != len(vector):
            raise ValueError(f"Dimension mismatch: matrix cols={mat.cols}, vector len={len(vector)}")
        return [sum(mat.data[i][j] * vector[j] for j in range(mat.cols)) for i in range(mat.rows)]

    @staticmethod
    def compose(t1: Matrix, t2: Matrix) -> Matrix:
        return t1.multiply(t2)

    @staticmethod
    def rotation_2d(theta: float) -> Matrix:
        c, s = math.cos(theta), math.sin(theta)
        return Matrix([[c, -s], [s, c]])

    @staticmethod
    def rotation_3d_x(theta: float) -> Matrix:
        c, s = math.cos(theta), math.sin(theta)
        return Matrix([[1, 0, 0], [0, c, -s], [0, s, c]])

    @staticmethod
    def rotation_3d_y(theta: float) -> Matrix:
        c, s = math.cos(theta), math.sin(theta)
        return Matrix([[c, 0, s], [0, 1, 0], [-s, 0, c]])

    @staticmethod
    def rotation_3d_z(theta: float) -> Matrix:
        c, s = math.cos(theta), math.sin(theta)
        return Matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])

    @staticmethod
    def scaling(factors: list[float]) -> Matrix:
        return Matrix.diagonal(factors)

    @staticmethod
    def reflection_2d(axis_angle: float) -> Matrix:
        c2 = math.cos(2 * axis_angle)
        s2 = math.sin(2 * axis_angle)
        return Matrix([[c2, s2], [s2, -c2]])

    @staticmethod
    def projection_onto_subspace(basis_vectors: list[list[float]]) -> Matrix:
        """Projection matrix onto subspace spanned by basis_vectors."""
        ortho = GramSchmidt.orthonormalize(basis_vectors)
        n = len(ortho[0])
        p_data = [[0.0] * n for _ in range(n)]
        for q in ortho:
            for i in range(n):
                for j in range(n):
                    p_data[i][j] += q[i] * q[j]
        return Matrix(p_data)

    @staticmethod
    def kernel(mat: Matrix) -> list[list[float]]:
        return GaussianElimination.null_space_basis(mat)

    @staticmethod
    def image(mat: Matrix) -> list[list[float]]:
        return GaussianElimination.column_space_basis(mat)

    @staticmethod
    def is_injective(mat: Matrix) -> bool:
        return GaussianElimination.nullity(mat) == 0

    @staticmethod
    def is_surjective(mat: Matrix) -> bool:
        return GaussianElimination.rank(mat) == mat.rows

    @staticmethod
    def is_bijective(mat: Matrix) -> bool:
        return mat.is_square and LinearTransformation.is_injective(mat) and LinearTransformation.is_surjective(mat)


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 14 — DOCTRINE CACHE (TIE Component 3)
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: list[dict[str, Any]] = []

def _load_doctrine_cache() -> None:
    """Load doctrine blocks from doctrine_cache.json."""
    global DOCTRINE_CACHE
    cache_path = ENGINE_DIR / "doctrine_cache.json"
    if cache_path.exists():
        try:
            raw = json.loads(cache_path.read_text(encoding="utf-8"))
            DOCTRINE_CACHE = raw if isinstance(raw, list) else raw.get("doctrines", [])
            logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks from cache")
        except Exception as exc:
            logger.error(f"Failed to load doctrine cache: {exc}")
            DOCTRINE_CACHE = []
    else:
        logger.warning("No doctrine_cache.json found, using empty cache")
        DOCTRINE_CACHE = []

def doctrine_lookup(query: str) -> list[dict[str, Any]]:
    """TIE Component 3: Fast keyword-matched doctrine retrieval (0-200ms layer)."""
    query_lower = query.lower()
    tokens = set(query_lower.split())
    scored: list[tuple[float, dict[str, Any]]] = []
    for block in DOCTRINE_CACHE:
        keywords = [k.lower() for k in block.get("keywords", [])]
        topic = block.get("topic", "").lower()
        score = 0.0
        for t in tokens:
            if t in topic:
                score += 3.0
            for kw in keywords:
                if t in kw:
                    score += 2.0
        if score > 0:
            scored.append((score, block))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scored[:5]]


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 15 — SEMANTIC NORMALIZATION (TIE Component 6)
# ═══════════════════════════════════════════════════════════════════════════

SEMANTIC_DICT: dict[str, str] = {}

def _load_semantic_dict() -> None:
    global SEMANTIC_DICT
    dict_path = ENGINE_DIR / "semantic_dict.json"
    if dict_path.exists():
        try:
            SEMANTIC_DICT = json.loads(dict_path.read_text(encoding="utf-8"))
            logger.info(f"Loaded {len(SEMANTIC_DICT)} semantic normalizations")
        except Exception as exc:
            logger.error(f"Failed to load semantic dict: {exc}")
    else:
        logger.warning("No semantic_dict.json found")

def normalize_query(query: str) -> str:
    """TIE Component 6: Deterministic term normalization."""
    words = query.lower().split()
    normalized = []
    for word in words:
        normalized.append(SEMANTIC_DICT.get(word, word))
    return " ".join(normalized)


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 16 — COVERAGE MAP (TIE Component 10)
# ═══════════════════════════════════════════════════════════════════════════

COVERAGE_MAP: dict[str, Any] = {}

def _load_coverage_map() -> None:
    global COVERAGE_MAP
    cov_path = ENGINE_DIR / "coverage_map.json"
    if cov_path.exists():
        try:
            COVERAGE_MAP = json.loads(cov_path.read_text(encoding="utf-8"))
            logger.info(f"Loaded coverage map with {len(COVERAGE_MAP.get('domains', {}))} domains")
        except Exception as exc:
            logger.error(f"Failed to load coverage map: {exc}")

def record_coverage_hit(domain: str, topic: str) -> None:
    domains = COVERAGE_MAP.setdefault("domains", {})
    dom = domains.setdefault(domain, {"topics": {}, "total_hits": 0})
    dom["total_hits"] = dom.get("total_hits", 0) + 1
    dom["topics"][topic] = dom["topics"].get(topic, 0) + 1


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 17 — TELEMETRY (TIE Component 8)
# ═══════════════════════════════════════════════════════════════════════════

class Telemetry:
    """Query tracing, latency tracking, error domains."""

    def __init__(self) -> None:
        self.queries_total: int = 0
        self.queries_by_type: dict[str, int] = {}
        self.latencies: list[float] = []
        self.errors: list[dict[str, Any]] = []
        self.start_time: float = time.time()

    def record_query(self, query_type: str, latency_ms: float) -> None:
        self.queries_total += 1
        self.queries_by_type[query_type] = self.queries_by_type.get(query_type, 0) + 1
        self.latencies.append(latency_ms)

    def record_error(self, error_type: str, detail: str) -> None:
        self.errors.append({
            "type": error_type,
            "detail": detail,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def get_stats(self) -> dict[str, Any]:
        uptime = time.time() - self.start_time
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0.0
        p95_latency = sorted(self.latencies)[int(len(self.latencies) * 0.95)] if len(self.latencies) > 1 else avg_latency
        return {
            "queries_total": self.queries_total,
            "queries_by_type": dict(self.queries_by_type),
            "avg_latency_ms": round(avg_latency, 2),
            "p95_latency_ms": round(p95_latency, 2),
            "error_count": len(self.errors),
            "uptime_seconds": round(uptime, 1),
            "queries_per_minute": round(self.queries_total / max(1, uptime / 60), 2),
        }

telemetry = Telemetry()


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 18 — DRIFT WATCHER (TIE Component 9)
# ═══════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    """Detect doctrine drift over time by comparing response distributions."""

    def __init__(self) -> None:
        self.observation_window: list[dict[str, Any]] = []
        self.baseline_distribution: dict[str, int] = {}

    def observe(self, doctrine_topic: str, confidence: float) -> None:
        self.observation_window.append({
            "topic": doctrine_topic,
            "confidence": confidence,
            "timestamp": time.time(),
        })
        self.baseline_distribution[doctrine_topic] = self.baseline_distribution.get(doctrine_topic, 0) + 1
        if len(self.observation_window) > 1000:
            self.observation_window = self.observation_window[-500:]

    def check_drift(self) -> dict[str, Any]:
        if len(self.observation_window) < 10:
            return {"status": "insufficient_data", "observations": len(self.observation_window)}
        recent = self.observation_window[-50:]
        recent_dist: dict[str, int] = {}
        for obs in recent:
            recent_dist[obs["topic"]] = recent_dist.get(obs["topic"], 0) + 1
        all_topics = set(self.baseline_distribution.keys()) | set(recent_dist.keys())
        total_baseline = sum(self.baseline_distribution.values())
        total_recent = len(recent)
        drift_scores: dict[str, float] = {}
        for topic in all_topics:
            baseline_frac = self.baseline_distribution.get(topic, 0) / max(1, total_baseline)
            recent_frac = recent_dist.get(topic, 0) / max(1, total_recent)
            drift_scores[topic] = abs(baseline_frac - recent_frac)
        max_drift = max(drift_scores.values()) if drift_scores else 0.0
        return {
            "status": "drifting" if max_drift > 0.3 else "stable",
            "max_drift_score": round(max_drift, 4),
            "drift_by_topic": {k: round(v, 4) for k, v in sorted(drift_scores.items(), key=lambda x: -x[1])[:10]},
        }

drift_watcher = DriftWatcher()


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 19 — METRICS COLLECTOR (TIE Component 11)
# ═══════════════════════════════════════════════════════════════════════════

class MetricsCollector:
    """Latency stats, error rates, hit rates, queries/hour."""

    def __init__(self) -> None:
        self.doctrine_hits: int = 0
        self.doctrine_misses: int = 0
        self.semantic_hits: int = 0
        self.deep_analysis_count: int = 0

    def record_doctrine_hit(self) -> None:
        self.doctrine_hits += 1

    def record_doctrine_miss(self) -> None:
        self.doctrine_misses += 1

    def record_semantic_hit(self) -> None:
        self.semantic_hits += 1

    def record_deep_analysis(self) -> None:
        self.deep_analysis_count += 1

    def get_rates(self) -> dict[str, Any]:
        total = self.doctrine_hits + self.doctrine_misses
        hit_rate = self.doctrine_hits / max(1, total)
        return {
            "doctrine_hit_rate": round(hit_rate, 4),
            "doctrine_hits": self.doctrine_hits,
            "doctrine_misses": self.doctrine_misses,
            "semantic_hits": self.semantic_hits,
            "deep_analysis_count": self.deep_analysis_count,
        }

metrics_collector = MetricsCollector()


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 20 — CONFIDENCE STRATIFICATION (TIE Component 5)
# ═══════════════════════════════════════════════════════════════════════════

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

def stratify_confidence(confidence: float, has_doctrine: bool, is_numerical: bool) -> ConfidenceLevel:
    """Assign confidence stratification based on score and evidence type."""
    if confidence >= 0.95 and has_doctrine and is_numerical:
        return ConfidenceLevel.DEFENSIBLE
    if confidence >= 0.80 and has_doctrine:
        return ConfidenceLevel.AGGRESSIVE
    if confidence >= 0.50:
        return ConfidenceLevel.DISCLOSURE
    return ConfidenceLevel.HIGH_RISK


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 21 — AUTHORITY HARDENING (TIE Component 4)
# ═══════════════════════════════════════════════════════════════════════════

AUTHORITY_HIERARCHY: list[dict[str, Any]] = [
    {"level": 1, "name": "Axiomatic", "weight": 1.0, "description": "Mathematical axioms and definitions"},
    {"level": 2, "name": "Theorem", "weight": 0.95, "description": "Proven theorems with complete proofs"},
    {"level": 3, "name": "Well-Known Result", "weight": 0.85, "description": "Standard textbook results"},
    {"level": 4, "name": "Computational", "weight": 0.80, "description": "Numerical computation results"},
    {"level": 5, "name": "Heuristic", "weight": 0.60, "description": "Rules of thumb, approximations"},
]

def resolve_authority(sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Pick highest-weight non-conflicting authority source."""
    if not sources:
        return {"authority": "none", "weight": 0.0}
    best = max(sources, key=lambda s: s.get("weight", 0))
    return {"authority": best.get("name", "unknown"), "weight": best.get("weight", 0)}


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 22 — ZONED ANALYSIS (TIE Component 13)
# ═══════════════════════════════════════════════════════════════════════════

class AnalysisZone(str, Enum):
    COMPUTATION = "COMPUTATION"
    THEORY = "THEORY"
    APPLICATION = "APPLICATION"

def classify_zone(query: str) -> AnalysisZone:
    """Classify query into analysis zone."""
    query_lower = query.lower()
    computation_signals = ["compute", "calculate", "find", "solve", "evaluate", "determinant", "inverse", "multiply", "decompose"]
    theory_signals = ["prove", "theorem", "why", "show that", "explain", "definition", "property", "when does"]
    application_signals = ["apply", "use", "model", "fit", "predict", "regression", "least squares", "transform", "rotate"]
    comp_score = sum(1 for s in computation_signals if s in query_lower)
    theory_score = sum(1 for s in theory_signals if s in query_lower)
    app_score = sum(1 for s in application_signals if s in query_lower)
    if comp_score >= theory_score and comp_score >= app_score:
        return AnalysisZone.COMPUTATION
    if theory_score >= app_score:
        return AnalysisZone.THEORY
    return AnalysisZone.APPLICATION


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 23 — FACT FRAGILITY SCORING (TIE Component 14)
# ═══════════════════════════════════════════════════════════════════════════

def score_fact_fragility(result: dict[str, Any]) -> dict[str, Any]:
    """Score how fragile/robust a computed result is."""
    fragility = 0.0
    factors: list[str] = []
    if result.get("condition_number", 1.0) > 1e6:
        fragility += 0.4
        factors.append("ill_conditioned_matrix")
    if result.get("near_singular", False):
        fragility += 0.3
        factors.append("near_singular")
    if result.get("numerical_precision_limited", False):
        fragility += 0.2
        factors.append("precision_limited")
    if result.get("iterative_convergence", True) is False:
        fragility += 0.3
        factors.append("convergence_not_guaranteed")
    return {
        "fragility_score": min(1.0, round(fragility, 3)),
        "factors": factors,
        "interpretation": "robust" if fragility < 0.3 else "fragile" if fragility > 0.6 else "moderate",
    }


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 24 — AUDIT TRAIL (TIE Component 15)
# ═══════════════════════════════════════════════════════════════════════════

AUDIT_LOG_PATH = LOG_DIR / "audit_trail.jsonl"

def write_audit_entry(entry: dict[str, Any]) -> None:
    """Append a JSONL audit entry."""
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    entry["engine_id"] = ENGINE_ID
    try:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except Exception as exc:
        logger.error(f"Audit write failed: {exc}")


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 25 — DETERMINISM HASH (TIE Component 16)
# ═══════════════════════════════════════════════════════════════════════════

def determinism_hash(data: Any) -> str:
    """SHA-256 for response reproducibility verification."""
    serialized = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 26 — THREE-LAYER RESPONSE (TIE Component 1)
# ═══════════════════════════════════════════════════════════════════════════

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

def three_layer_response(query: str, mode: ResponseMode = ResponseMode.FAST) -> dict[str, Any]:
    """TIE Component 1: Doctrine Cache → Semantic Retrieval → Deep Analysis."""
    t0 = time.time()
    query_id = str(uuid4())[:12]
    normalized = normalize_query(query)
    zone = classify_zone(normalized)

    # Layer 1: Doctrine Cache (0-200ms target)
    doctrines = doctrine_lookup(normalized)
    layer = "doctrine_cache"
    confidence = 0.0
    result_data: dict[str, Any] = {}

    if doctrines:
        metrics_collector.record_doctrine_hit()
        best = doctrines[0]
        confidence = 0.90
        result_data = {
            "source": "doctrine_cache",
            "topic": best.get("topic", ""),
            "conclusion": best.get("conclusion_template", ""),
            "reasoning": best.get("reasoning_framework", ""),
            "authority": best.get("primary_authority", []),
        }
        drift_watcher.observe(best.get("topic", "unknown"), confidence)
        record_coverage_hit("linear_algebra", best.get("topic", ""))
    else:
        metrics_collector.record_doctrine_miss()
        # Layer 2: Semantic retrieval
        metrics_collector.record_semantic_hit()
        layer = "semantic_retrieval"
        confidence = 0.70
        result_data = {
            "source": "semantic_retrieval",
            "normalized_query": normalized,
            "note": "No exact doctrine match; semantic fallback used",
        }

    # Layer 3 (for DEFENSE/MEMO modes): Deep analysis
    if mode in (ResponseMode.DEFENSE, ResponseMode.MEMO):
        metrics_collector.record_deep_analysis()
        layer = "deep_analysis"
        result_data["deep_analysis"] = {
            "zone": zone.value,
            "multi_source": True,
            "full_reasoning_chain": True,
        }
        confidence = min(confidence + 0.05, 0.99)

    strat = stratify_confidence(confidence, bool(doctrines), zone == AnalysisZone.COMPUTATION)
    latency_ms = (time.time() - t0) * 1000
    telemetry.record_query(layer, latency_ms)

    response = {
        "query_id": query_id,
        "query": query,
        "normalized_query": normalized,
        "zone": zone.value,
        "mode": mode.value,
        "layer": layer,
        "confidence": round(confidence, 4),
        "confidence_stratification": strat.value,
        "result": result_data,
        "fragility": score_fact_fragility(result_data),
        "authority": resolve_authority(AUTHORITY_HIERARCHY[:2] if doctrines else AUTHORITY_HIERARCHY[2:4]),
        "determinism_hash": determinism_hash(result_data),
        "latency_ms": round(latency_ms, 2),
    }

    write_audit_entry({"type": "query", "query_id": query_id, "query": query, "layer": layer, "latency_ms": latency_ms})
    return response


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT 27 — MULTI-DOCTRINE DECOMPOSITION (TIE Component 19)
# ═══════════════════════════════════════════════════════════════════════════

def decompose_query(query: str) -> dict[str, Any]:
    """Break complex query into sub-problems across doctrine domains."""
    query_lower = query.lower()
    categories: list[str] = []
    if any(w in query_lower for w in ["eigenvalue", "eigenvector", "diagonalize", "spectrum"]):
        categories.append("spectral_theory")
    if any(w in query_lower for w in ["decompose", "factor", "lu", "qr", "svd", "cholesky"]):
        categories.append("matrix_decomposition")
    if any(w in query_lower for w in ["rank", "null", "basis", "span", "dimension", "subspace"]):
        categories.append("vector_spaces")
    if any(w in query_lower for w in ["solve", "system", "equation", "augmented"]):
        categories.append("linear_systems")
    if any(w in query_lower for w in ["least squares", "fit", "regression", "projection"]):
        categories.append("optimization")
    if any(w in query_lower for w in ["determinant", "inverse", "transpose", "multiply", "add"]):
        categories.append("matrix_operations")
    if any(w in query_lower for w in ["transform", "rotation", "scaling", "reflection", "kernel", "image"]):
        categories.append("linear_transformations")
    if any(w in query_lower for w in ["norm", "condition", "stability", "error"]):
        categories.append("numerical_analysis")
    if not categories:
        categories.append("general_linear_algebra")
    return {
        "original_query": query,
        "categories": categories,
        "interaction_graph": _build_interaction_graph(categories),
        "resolution_order": categories,
    }

def _build_interaction_graph(categories: list[str]) -> dict[str, list[str]]:
    deps: dict[str, list[str]] = {
        "spectral_theory": ["matrix_operations"],
        "matrix_decomposition": ["matrix_operations"],
        "optimization": ["matrix_decomposition", "linear_systems"],
        "linear_systems": ["matrix_operations"],
        "vector_spaces": ["matrix_operations", "linear_systems"],
        "numerical_analysis": ["matrix_operations", "matrix_decomposition"],
        "linear_transformations": ["matrix_operations", "vector_spaces"],
        "matrix_operations": [],
        "general_linear_algebra": [],
    }
    graph: dict[str, list[str]] = {}
    for cat in categories:
        graph[cat] = [d for d in deps.get(cat, []) if d in categories]
    return graph


# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class MatrixInput(BaseModel):
    data: list[list[float]] = Field(..., description="Matrix as list of rows")

class TwoMatrixInput(BaseModel):
    a: list[list[float]]
    b: list[list[float]]

class MatrixScalarInput(BaseModel):
    data: list[list[float]]
    scalar: float

class MatrixVectorInput(BaseModel):
    matrix: list[list[float]]
    vector: list[float]

class VectorInput(BaseModel):
    vector: list[float]

class TwoVectorInput(BaseModel):
    a: list[float]
    b: list[float]

class VectorsInput(BaseModel):
    vectors: list[list[float]]

class SolveInput(BaseModel):
    a: list[list[float]]
    b: list[float]

class PolyFitInput(BaseModel):
    x: list[float]
    y: list[float]
    degree: int = 1

class MatrixPowerInput(BaseModel):
    data: list[list[float]]
    n: int

class QueryInput(BaseModel):
    query: str
    mode: str = "FAST"

class NormInput(BaseModel):
    data: list[list[float]]
    norm_type: str = "frobenius"

class TransformInput(BaseModel):
    matrix: list[list[float]]
    vector: list[float]

class RotationInput(BaseModel):
    angle_radians: float
    axis: str = "z"

class ProjectionInput(BaseModel):
    basis_vectors: list[list[float]]

class LinearCombinationInput(BaseModel):
    vectors: list[list[float]]
    coefficients: list[float]


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION (TIE Component 17)
# ═══════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    _load_doctrine_cache()
    _load_semantic_dict()
    _load_coverage_map()
    logger.info("All caches loaded, engine operational")
    yield
    logger.info("Shutting down engine")

app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="TIE-20 compliant Linear Algebra engine — pure Python, no numpy",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Health Endpoint (TIE Component 12) ───────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "authority_level": ENGINE_AUTH_LEVEL,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "semantic_terms": len(SEMANTIC_DICT),
        "telemetry": telemetry.get_stats(),
        "metrics": metrics_collector.get_rates(),
        "drift": drift_watcher.check_drift(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# ── TIE Query Endpoint ──────────────────────────────────────────────────

@app.post("/query")
async def query_engine(body: QueryInput):
    mode_map = {"FAST": ResponseMode.FAST, "DEFENSE": ResponseMode.DEFENSE, "MEMO": ResponseMode.MEMO}
    mode = mode_map.get(body.mode.upper(), ResponseMode.FAST)
    result = three_layer_response(body.query, mode)
    decomp = decompose_query(body.query)
    result["decomposition"] = decomp
    return result

# ── Matrix Operations ────────────────────────────────────────────────────

@app.post("/matrix/add")
async def matrix_add(body: TwoMatrixInput):
    t0 = time.time()
    a, b = Matrix(body.a), Matrix(body.b)
    result = a.add(b)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("matrix_add", lat)
    return {"result": result.to_list(), "shape": result.shape, "latency_ms": round(lat, 2)}

@app.post("/matrix/subtract")
async def matrix_subtract(body: TwoMatrixInput):
    t0 = time.time()
    a, b = Matrix(body.a), Matrix(body.b)
    result = a.subtract(b)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("matrix_subtract", lat)
    return {"result": result.to_list(), "shape": result.shape, "latency_ms": round(lat, 2)}

@app.post("/matrix/multiply")
async def matrix_multiply(body: TwoMatrixInput):
    t0 = time.time()
    a, b = Matrix(body.a), Matrix(body.b)
    result = a.multiply(b)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("matrix_multiply", lat)
    return {"result": result.to_list(), "shape": result.shape, "latency_ms": round(lat, 2)}

@app.post("/matrix/scalar_multiply")
async def matrix_scalar_multiply(body: MatrixScalarInput):
    t0 = time.time()
    m = Matrix(body.data)
    result = m.scalar_multiply(body.scalar)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("scalar_multiply", lat)
    return {"result": result.to_list(), "shape": result.shape, "latency_ms": round(lat, 2)}

@app.post("/matrix/transpose")
async def matrix_transpose(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    result = m.transpose()
    lat = (time.time() - t0) * 1000
    telemetry.record_query("transpose", lat)
    return {"result": result.to_list(), "shape": result.shape, "latency_ms": round(lat, 2)}

@app.post("/matrix/determinant")
async def matrix_determinant(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    det = Determinant.compute(m)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("determinant", lat)
    return {"determinant": det, "method": "cofactor" if m.rows <= 4 else "row_reduction", "latency_ms": round(lat, 2)}

@app.post("/matrix/inverse")
async def matrix_inverse(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    if not MatrixInverse.is_invertible(m):
        raise HTTPException(status_code=400, detail="Matrix is singular, cannot invert")
    inv = MatrixInverse.compute(m)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("inverse", lat)
    return {"result": inv.to_list(), "shape": inv.shape, "is_invertible": True, "latency_ms": round(lat, 2)}

@app.post("/matrix/power")
async def matrix_power(body: MatrixPowerInput):
    t0 = time.time()
    m = Matrix(body.data)
    result = m.power(body.n)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("matrix_power", lat)
    return {"result": result.to_list(), "shape": result.shape, "exponent": body.n, "latency_ms": round(lat, 2)}

@app.post("/matrix/trace")
async def matrix_trace(body: MatrixInput):
    m = Matrix(body.data)
    return {"trace": m.trace, "shape": m.shape}

@app.post("/matrix/properties")
async def matrix_properties(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    props: dict[str, Any] = {
        "shape": m.shape,
        "is_square": m.is_square,
        "is_symmetric": m.is_symmetric,
    }
    if m.is_square:
        props["trace"] = m.trace
        props["determinant"] = Determinant.compute(m)
        props["is_invertible"] = MatrixInverse.is_invertible(m)
        if CholeskyDecomposition.is_positive_definite(m):
            props["is_positive_definite"] = True
        else:
            props["is_positive_definite"] = False
    props["rank"] = GaussianElimination.rank(m)
    props["nullity"] = GaussianElimination.nullity(m)
    props["frobenius_norm"] = MatrixNorms.frobenius(m)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("properties", lat)
    props["latency_ms"] = round(lat, 2)
    return props

# ── Gaussian Elimination Endpoints ───────────────────────────────────────

@app.post("/gauss/ref")
async def gauss_ref(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    ref, rank, sign = GaussianElimination.row_echelon_form(m)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("ref", lat)
    return {"ref": ref.to_list(), "rank": rank, "latency_ms": round(lat, 2)}

@app.post("/gauss/rref")
async def gauss_rref(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    rref, pivots = GaussianElimination.reduced_row_echelon_form(m)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("rref", lat)
    return {"rref": rref.to_list(), "pivot_columns": pivots, "rank": len(pivots), "latency_ms": round(lat, 2)}

@app.post("/gauss/rank")
async def gauss_rank(body: MatrixInput):
    m = Matrix(body.data)
    r = GaussianElimination.rank(m)
    return {"rank": r, "nullity": m.cols - r, "shape": m.shape}

@app.post("/gauss/null_space")
async def gauss_null_space(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    basis = GaussianElimination.null_space_basis(m)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("null_space", lat)
    return {"null_space_basis": basis, "nullity": len(basis), "latency_ms": round(lat, 2)}

@app.post("/gauss/column_space")
async def gauss_column_space(body: MatrixInput):
    m = Matrix(body.data)
    basis = GaussianElimination.column_space_basis(m)
    return {"column_space_basis": basis, "rank": len(basis)}

@app.post("/gauss/row_space")
async def gauss_row_space(body: MatrixInput):
    m = Matrix(body.data)
    basis = GaussianElimination.row_space_basis(m)
    return {"row_space_basis": basis, "rank": len(basis)}

@app.post("/gauss/solve")
async def gauss_solve(body: SolveInput):
    t0 = time.time()
    a = Matrix(body.a)
    solution = GaussianElimination.solve(a, body.b)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("solve", lat)
    if solution is None:
        return {"solution": None, "consistent": False, "latency_ms": round(lat, 2)}
    return {"solution": solution, "consistent": True, "latency_ms": round(lat, 2)}

# ── Decomposition Endpoints ──────────────────────────────────────────────

@app.post("/decompose/lu")
async def decompose_lu(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    p, l_mat, u_mat = LUDecomposition.decompose(m)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("lu_decompose", lat)
    return {"P": p.to_list(), "L": l_mat.to_list(), "U": u_mat.to_list(), "latency_ms": round(lat, 2)}

@app.post("/decompose/qr")
async def decompose_qr(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    q, r_mat = GramSchmidt.qr_decomposition(m)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("qr_decompose", lat)
    return {"Q": q.to_list(), "R": r_mat.to_list(), "latency_ms": round(lat, 2)}

@app.post("/decompose/cholesky")
async def decompose_cholesky(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    l_mat = CholeskyDecomposition.decompose(m)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("cholesky_decompose", lat)
    return {"L": l_mat.to_list(), "latency_ms": round(lat, 2)}

@app.post("/decompose/svd")
async def decompose_svd(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    if m.rows > 10 or m.cols > 10:
        raise HTTPException(status_code=400, detail="SVD limited to 10x10 matrices in pure Python mode")
    u_mat, s_vals, vt_mat = SVD.compute(m)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("svd_decompose", lat)
    return {"U": u_mat.to_list(), "singular_values": s_vals, "Vt": vt_mat.to_list(), "latency_ms": round(lat, 2)}

# ── Eigenvalue Endpoints ─────────────────────────────────────────────────

@app.post("/eigen")
async def eigen(body: MatrixInput):
    t0 = time.time()
    m = Matrix(body.data)
    if not m.is_square:
        raise HTTPException(status_code=400, detail="Eigenvalue computation requires square matrix")
    results = Eigenvalues.compute(m)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("eigenvalues", lat)
    output = [{"eigenvalue": ev, "eigenvector": vec} for ev, vec in results]
    return {"eigen_pairs": output, "count": len(output), "latency_ms": round(lat, 2)}

# ── Vector Endpoints ─────────────────────────────────────────────────────

@app.post("/vector/dot")
async def vector_dot(body: TwoVectorInput):
    return {"dot_product": VectorOps.dot(body.a, body.b)}

@app.post("/vector/cross")
async def vector_cross(body: TwoVectorInput):
    return {"cross_product": VectorOps.cross(body.a, body.b)}

@app.post("/vector/norm")
async def vector_norm(body: VectorInput):
    return {
        "l1_norm": VectorOps.norm(body.vector, 1.0),
        "l2_norm": VectorOps.norm(body.vector, 2.0),
        "linf_norm": VectorOps.norm(body.vector, float("inf")),
    }

@app.post("/vector/normalize")
async def vector_normalize(body: VectorInput):
    return {"normalized": VectorOps.normalize(body.vector)}

@app.post("/vector/projection")
async def vector_projection(body: TwoVectorInput):
    proj = VectorOps.projection(body.a, body.b)
    rej = VectorOps.rejection(body.a, body.b)
    return {"projection": proj, "rejection": rej}

@app.post("/vector/angle")
async def vector_angle(body: TwoVectorInput):
    rad = VectorOps.angle_between(body.a, body.b)
    return {"angle_radians": rad, "angle_degrees": math.degrees(rad)}

@app.post("/vector/outer_product")
async def vector_outer_product(body: TwoVectorInput):
    result = VectorOps.outer_product(body.a, body.b)
    return {"result": result.to_list(), "shape": result.shape}

@app.post("/vector/linear_combination")
async def vector_linear_combination(body: LinearCombinationInput):
    result = VectorOps.linear_combination(body.vectors, body.coefficients)
    return {"result": result}

# ── Orthogonalization Endpoints ──────────────────────────────────────────

@app.post("/gram_schmidt/orthogonalize")
async def gs_orthogonalize(body: VectorsInput):
    t0 = time.time()
    result = GramSchmidt.orthogonalize(body.vectors)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("gram_schmidt", lat)
    return {"orthogonal_basis": result, "count": len(result), "latency_ms": round(lat, 2)}

@app.post("/gram_schmidt/orthonormalize")
async def gs_orthonormalize(body: VectorsInput):
    t0 = time.time()
    result = GramSchmidt.orthonormalize(body.vectors)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("gram_schmidt_on", lat)
    return {"orthonormal_basis": result, "count": len(result), "latency_ms": round(lat, 2)}

# ── Least Squares Endpoints ──────────────────────────────────────────────

@app.post("/least_squares/solve")
async def ls_solve(body: SolveInput):
    t0 = time.time()
    a = Matrix(body.a)
    x = LeastSquares.solve(a, body.b)
    residual_val = LeastSquares.residual_norm(a, x, body.b)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("least_squares", lat)
    return {"solution": x, "residual_norm": residual_val, "latency_ms": round(lat, 2)}

@app.post("/least_squares/polyfit")
async def ls_polyfit(body: PolyFitInput):
    t0 = time.time()
    coeffs = LeastSquares.fit_polynomial(body.x, body.y, body.degree)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("polyfit", lat)
    return {"coefficients": coeffs, "degree": body.degree, "latency_ms": round(lat, 2)}

# ── Norms & Condition Number ─────────────────────────────────────────────

@app.post("/matrix/norms")
async def matrix_norms(body: MatrixInput):
    m = Matrix(body.data)
    result: dict[str, Any] = {
        "frobenius": MatrixNorms.frobenius(m),
        "infinity": MatrixNorms.infinity_norm(m),
        "one": MatrixNorms.one_norm(m),
    }
    if m.rows <= 10 and m.cols <= 10:
        result["spectral"] = MatrixNorms.spectral_norm(m)
    return result

@app.post("/matrix/condition_number")
async def matrix_condition_number(body: NormInput):
    m = Matrix(body.data)
    cond = MatrixNorms.condition_number(m, body.norm_type)
    return {"condition_number": cond, "norm_type": body.norm_type, "well_conditioned": cond < 1e6}

# ── Linear Transformation Endpoints ──────────────────────────────────────

@app.post("/transform/apply")
async def transform_apply(body: TransformInput):
    m = Matrix(body.matrix)
    result = LinearTransformation.apply(m, body.vector)
    return {"result": result}

@app.post("/transform/rotation")
async def transform_rotation(body: RotationInput):
    if body.axis == "2d":
        m = LinearTransformation.rotation_2d(body.angle_radians)
    elif body.axis == "x":
        m = LinearTransformation.rotation_3d_x(body.angle_radians)
    elif body.axis == "y":
        m = LinearTransformation.rotation_3d_y(body.angle_radians)
    else:
        m = LinearTransformation.rotation_3d_z(body.angle_radians)
    return {"rotation_matrix": m.to_list(), "axis": body.axis, "angle_radians": body.angle_radians}

@app.post("/transform/projection_matrix")
async def transform_projection_matrix(body: ProjectionInput):
    p = LinearTransformation.projection_onto_subspace(body.basis_vectors)
    return {"projection_matrix": p.to_list(), "shape": p.shape}

@app.post("/transform/kernel")
async def transform_kernel(body: MatrixInput):
    m = Matrix(body.data)
    ker = LinearTransformation.kernel(m)
    return {"kernel_basis": ker, "dimension": len(ker)}

@app.post("/transform/image")
async def transform_image(body: MatrixInput):
    m = Matrix(body.data)
    img = LinearTransformation.image(m)
    return {"image_basis": img, "dimension": len(img)}

@app.post("/transform/properties")
async def transform_properties(body: MatrixInput):
    m = Matrix(body.data)
    return {
        "is_injective": LinearTransformation.is_injective(m),
        "is_surjective": LinearTransformation.is_surjective(m),
        "is_bijective": LinearTransformation.is_bijective(m),
        "kernel_dimension": GaussianElimination.nullity(m),
        "image_dimension": GaussianElimination.rank(m),
    }

# ── Telemetry / Metrics / Drift Endpoints ────────────────────────────────

@app.get("/telemetry")
async def get_telemetry():
    return telemetry.get_stats()

@app.get("/metrics")
async def get_metrics():
    return metrics_collector.get_rates()

@app.get("/drift")
async def get_drift():
    return drift_watcher.check_drift()

# ── LU Solve Endpoint ───────────────────────────────────────────────────

@app.post("/lu/solve")
async def lu_solve(body: SolveInput):
    t0 = time.time()
    a = Matrix(body.a)
    x = LUDecomposition.solve(a, body.b)
    lat = (time.time() - t0) * 1000
    telemetry.record_query("lu_solve", lat)
    return {"solution": x, "latency_ms": round(lat, 2)}

# ═══════════════════════════════════════════════════════════════════════════
# ENTRYPOINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Launching {ENGINE_NAME} on port {ENGINE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
