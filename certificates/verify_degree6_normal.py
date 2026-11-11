#!/usr/bin/env python3
"""Check the degree-six fixed-graph determinant and modular certificate.

Run from the repository root with Python 3.9 or newer:
    python3 -m venv .venv
    .venv/bin/python -m pip install sympy==1.14.0
    .venv/bin/python certificates/verify_degree6_normal.py

The script also runs from any directory when given its path. After dependency
installation it runs offline, with no manuscript files or saved matrices.

Source: jaehwoo/3-dimensional-Tarry-s-problem at
b627446ea3f55f6aff0aa094f8095b07f7fe2482.
Complete_Affine_Jets_I.tex, lines 2120–2128 and 2173–2176: row sets.
Complete_Affine_Jets_Supplement.tex, lines 1440–1450: orders and entry formula;
lines 1457–1504: factors, block determinants, and modular sequence.
Scope: the fixed-graph calculation in degree six.
"""

from collections import defaultdict
from itertools import product
from math import factorial, prod

from sympy import Poly, Symbol, ZZ
from sympy.polys.matrices import DomainMatrix


DEGREE = 6
T = Symbol("t")
POLYNOMIAL_RING = ZZ.poly_ring(T)
t = POLYNOMIAL_RING.gens[0]

# Printed f_1,...,f_11. Coefficients are in descending degree order.
FACTOR_COEFFICIENTS = (
    (2, -1),
    (6, 1),
    (4, 0, 1),
    (2, -1, 1),
    (2, 6, 1),
    (1, -6, 5, -1),
    (6, 6, -5, 1),
    (20, 90, 30, 1),
    (60, -60, 40, -2, 1),
    (100, -300, -200, -160, -15, -1),
    (36, -180, 60, 8, 9, -3, 1),
)

# Weight, dimension, signed scalar, and 1-based factor indices.
PRINTED_BLOCKS = (
    (1, 2, 1, ()),
    (2, 4, -1, ()),
    (3, 6, 1, ()),
    (4, 9, 2, ()),
    (5, 12, 4, ()),
    (6, 16, -48, ()),
    (7, 12, -16, (3, 6)),
    (8, 9, -32, (1, 2, 4, 7)),
    (9, 6, 36, (3, 11)),
    (10, 4, -8, (2, 5, 9)),
    (11, 2, -1, (10,)),
    (12, 1, 1, (8,)),
)

PRINTED_LEADING_COEFFICIENTS = (
    37, 73, 73, 22, 82, 15, 83, 91, 40, 85, 17,
    64, 46, 24, 65, 19, 11, 32, 20, 21, 80, 100,
    93, 53, 61, 73, 8, 84, 97, 8, 35, 6, 25,
)


def grid(d):
    """Rectangular I_d in lexicographic (i, j) order."""
    return list(product(range(d + 1), repeat=2))


def manuscript_rows():
    """Rows (r, i, j) before grouping by weight."""
    rows = [(0, i, j) for i, j in grid(DEGREE) if (i, j) != (0, 0)]
    rows.extend((2, i, j) for i, j in grid(DEGREE - 3))
    e6 = sorted(set(grid(DEGREE - 3)) | {(DEGREE - 2, 0), (0, DEGREE - 2)})
    rows.extend((1, i, j) for i, j in e6)
    rows.extend((3, i, j) for i, j in grid(DEGREE - 6))
    return rows


def manuscript_columns():
    """Nonconstant columns (a, b, c), ordered by total degree, a, b."""
    return [
        (a, b, total - a - b)
        for total in range(1, DEGREE + 1)
        for a in range(total + 1)
        for b in range(total - a + 1)
    ]


def weight(index):
    first, second, third = index
    return 2 * first + second + third


def weight_groups(indices):
    groups = defaultdict(list)
    for index in indices:
        groups[weight(index)].append(index)
    return groups


def weight_inversions(indices):
    weights = [weight(index) for index in indices]
    return sum(
        left > right
        for position, left in enumerate(weights)
        for right in weights[position + 1:]
    )


def matrix_entry(row, column):
    """Coefficient of y^i z^j after differentiating and setting x=Q."""
    r, i, j = row
    a, b, c = column
    entry = POLYNOMIAL_RING.zero
    if a < r or weight(row) != weight(column):
        return entry
    for alpha in range(a - r + 1):
        beta = i - b - 2 * alpha
        gamma = a - r - alpha - beta
        if beta >= 0 and gamma >= 0 and beta + 2 * gamma + c == j:
            coefficient = factorial(a) // (
                factorial(alpha) * factorial(beta) * factorial(gamma)
            )
            entry += coefficient * t**alpha
    return entry


def block_determinant(rows, columns):
    entries = [[matrix_entry(row, column) for column in columns] for row in rows]
    matrix = DomainMatrix(entries, (len(rows), len(columns)), POLYNOMIAL_RING)
    return matrix.det()


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def verify_modular_certificate(factors):
    distinct_product = prod(factors[1:])
    prime = 101
    reduced = Poly.from_dict(distinct_product.to_dict(), T, modulus=prime)
    derivative = reduced.diff()
    require(
        distinct_product.degree() == reduced.degree() == 32
        and derivative.degree() == 31,
        "degree changed on reduction or differentiation",
    )

    sequence = []
    current, following = reduced, derivative
    while not current.is_zero:
        sequence.append((current.degree(), int(current.LC()) % prime))
        if following.is_zero:
            break
        current, following = following, current.rem(following)

    print(f"F_{prime} Euclidean degree/leading-coefficient pairs:")
    for start in range(0, len(sequence), 11):
        group = sequence[start:start + 11]
        print("  " + " ".join(f"{degree}:{lc}" for degree, lc in group))
    expected = list(zip(range(32, -1, -1), PRINTED_LEADING_COEFFICIENTS))
    require(sequence == expected, f"Euclidean sequence differs from {expected}")
    require(sequence[-1] == (0, 25) and following.is_zero, "wrong Euclidean termination")
    # Degree preservation ensures a repeated primitive factor over Q would
    # give a positive-degree repeated factor after reduction modulo prime.
    print("All 33 pairs match, followed by zero. R is squarefree over Q.")


def main():
    rows, columns = manuscript_rows(), manuscript_columns()
    require(len(set(rows)) == len(rows) == len(set(columns)) == len(columns) == 83,
            "the degree-six row or column list does not have 83 distinct indices")
    rows_by_weight = weight_groups(rows)
    columns_by_weight = weight_groups(columns)
    printed_weights = {weight for weight, _, _, _ in PRINTED_BLOCKS}
    require(rows_by_weight.keys() == columns_by_weight.keys() == printed_weights,
            "the row, column, and printed weight sets differ")

    factors = [POLYNOMIAL_RING.one]  # Use the manuscript's 1-based indexing.
    for coefficients in FACTOR_COEFFICIENTS:
        factors.append(sum(
            coefficient * t**power
            for power, coefficient in enumerate(reversed(coefficients))
        ))

    determinants = []
    mismatch = False
    print("Weight  Size  Result              Printed determinant")
    for block_weight, size, scalar, factor_indices in PRINTED_BLOCKS:
        block_rows = rows_by_weight[block_weight]
        block_columns = columns_by_weight[block_weight]
        require(len(block_rows) == len(block_columns) == size,
                f"wrong block size at weight {block_weight}")
        actual = block_determinant(block_rows, block_columns)
        expected = scalar * prod(factors[index] for index in factor_indices)
        if actual == expected:
            result = "exact match"
        elif actual == -expected:
            result = "sign reversed"
        else:
            result = "polynomial mismatch"
        label = str(scalar) + "".join(f"*f{index}" for index in factor_indices)
        print(f"{block_weight:>6}  {size:>4}  {result:<18}  {label}")
        if actual != expected:
            mismatch = True
            print(f"  computed: {actual}\n  printed:  {expected}")
        determinants.append(actual)

    row_inversions = weight_inversions(rows)
    column_inversions = weight_inversions(columns)
    regrouping_sign = (-1)**(row_inversions + column_inversions)
    print(f"Regrouping inversions: rows={row_inversions}, columns={column_inversions}, "
          f"combined sign={regrouping_sign:+d}")
    block_product = prod(determinants)
    full_determinant = regrouping_sign * block_product
    printed_product = 56623104 * factors[1] * factors[2]**2 * factors[3]**2
    printed_product *= prod(factors[4:])
    require(prod(scalar for _, _, scalar, _ in PRINTED_BLOCKS) == 56623104,
            "the twelve printed scalars have the wrong product")
    require(not mismatch, "at least one block differs in the prescribed order")
    require(block_product == printed_product, "the block product differs from the printed formula")
    require(full_determinant == printed_product, "the original order reverses the displayed sign")
    require(full_determinant.degree() == 35 and full_determinant.get((0,), 0) == -56623104,
            "the full determinant has the wrong degree or constant term")
    print(f"Full determinant: degree={full_determinant.degree()}, "
          f"g6(0)={full_determinant.get((0,), 0)}, leading coefficient={full_determinant.LC}")

    verify_modular_certificate(factors)
    print("PASS: degree-six fixed-graph finite certificate")


if __name__ == "__main__":
    main()
