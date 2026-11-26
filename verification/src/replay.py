"""Exact replay of the lower-bound laws, small primal/dual LPs and atom formulas."""

from fractions import Fraction as F
from itertools import combinations, product
from random import Random


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def matrix_inverse(matrix):
    n = len(matrix)
    aug = [[F(x) for x in row] + [F(i == j) for j in range(n)]
           for i, row in enumerate(matrix)]
    for i in range(n):
        pivot = next((k for k in range(i, n) if aug[k][i]), None)
        if pivot is None:
            return None
        aug[i], aug[pivot] = aug[pivot], aug[i]
        factor = aug[i][i]
        aug[i] = [x / factor for x in aug[i]]
        for k in range(n):
            if k != i and aug[k][i]:
                factor = aug[k][i]
                aug[k] = [x - factor * y for x, y in zip(aug[k], aug[i])]
    return [row[n:] for row in aug]


def rank(rows):
    echelon = {}
    for row in rows:
        row = [F(x) for x in row]
        for i in range(len(row)):
            value = row[i]
            if not value:
                continue
            if i not in echelon:
                echelon[i] = [x / value for x in row]
                break
            row = [x - value * y for x, y in zip(row, echelon[i])]
    return len(echelon)


def lower_laws(a, inverse, column, t):
    k = len(a)
    b = [tuple(row) + (int(i == column),) for i, row in enumerate(a)]
    q = [-row[column] for row in inverse] + [F(1)]
    h = sum(abs(x) for x in q)
    r = [x / (4 * h) for x in q]
    p = [abs(x) / (2 * h) + F(1, 2 * (k + 1)) for x in q]
    v = [x / w for x, w in zip(r, p)]
    z = v[-1]
    eta0 = [F(1, 2)] * k + [1 - z]
    eta1 = [F(1, 2)] * k + [1 - (1 - t) * z]
    f = [e + x for e, x in zip(eta0, v)]
    repaired = [e + (1 - t) * x for e, x in zip(eta1, v)]
    assert all(dot(row, q) == 0 for row in b)
    assert all(x > 0 for x in p) and sum(p) == 1
    assert all(0 <= x <= 1 for x in f + repaired + eta0 + eta1)
    assert f[-1] == repaired[-1] == 1

    for mean, scores in ((eta0, f), (eta1, repaired)):
        assert all(dot(row, [w * (s - m) for w, s, m in zip(p, scores, mean)]) == 0
                   for row in b)
    exact = sum(w * abs(x - y) for w, x, y in zip(p, f, repaired))
    assert exact == t * (h - 1) / (4 * h) >= t / 8
    chi_square = p[-1] * t**2 * z**2 / ((1 - t) * z * (1 - (1 - t) * z))
    assert chi_square <= t**2 / h
    return b, p, eta0, eta1, f, repaired, exact


def check_lower_laws():
    matrices, cases = 0, 0
    chi = []
    for k in range(1, 4):
        max_entry = F(0)
        for entries in product((0, 1), repeat=k**2):
            a = [entries[i:i+k] for i in range(0, k**2, k)]
            inverse = matrix_inverse(a)
            if inverse is None:
                continue
            matrices += 1
            max_entry = max(max_entry, *(abs(x) for row in inverse for x in row))
            for column, t in product(range(k), (F(1, 8), F(1, 4), F(1, 2))):
                lower_laws(a, inverse, column, t)
                cases += 1
        chi.append(max_entry)
    return matrices, cases, chi


def independent_rows(b):
    selected = []
    for row in b:
        if rank(selected + [row]) > len(selected):
            selected.append(row)
    return selected


def primal_cost(rows, p, eta, f):
    n = len(p)
    constraints = [[w * x for w, x in zip(p, row)] for row in rows]
    target = [dot(row, eta) for row in constraints]
    best = None
    for free in combinations(range(n), len(rows)):
        inverse = matrix_inverse([[row[i] for i in free] for row in constraints])
        if inverse is None:
            continue
        fixed = [i for i in range(n) if i not in free]
        for scores in product(*[(0, f[i], 1) for i in fixed]):
            remaining = [t - sum(row[i] * x for i, x in zip(fixed, scores))
                         for t, row in zip(target, constraints)]
            candidate = [None] * n
            for i, x in zip(fixed, scores):
                candidate[i] = x
            for i, row in zip(free, inverse):
                candidate[i] = dot(row, remaining)
            if not all(0 <= x <= 1 for x in candidate):
                continue
            value = sum(w * abs(x - y) for w, x, y in zip(p, f, candidate))
            if best is None or value < best:
                best = value
    assert best is not None
    return best


def dual_cost(rows, p, eta, f):
    patterns = list(zip(*rows)) if rows else [()] * len(p)
    best, smallest_norm = F(0), None
    for basis in combinations(patterns, len(rows)):
        inverse = matrix_inverse(basis)
        if inverse is None:
            continue
        for signs in product((-1, 1), repeat=len(rows)):
            multipliers = [dot(row, signs) for row in inverse]
            values = [dot(multipliers, a) for a in patterns]
            result = sum(w * min(abs(prediction - h) + c * (h - y)
                                 for h in (0, prediction, 1))
                         for w, y, prediction, c in zip(p, eta, f, values))
            norm = max((abs(x) for x in multipliers), default=F(0))
            if result > best or result == best and (smallest_norm is None or norm < smallest_norm):
                best, smallest_norm = result, norm
    assert smallest_norm is not None
    return best, smallest_norm


def check_dual_lps(chi):
    rng = Random(572)
    checks = 0
    for n, k in product(range(1, 6), range(1, 4)):
        for _ in range(23):
            b = [tuple(rng.randrange(2) for _ in range(n)) for _ in range(k)]
            rows = independent_rows(b)
            weights = [rng.randrange(1, 7) for _ in range(n)]
            p = [F(w, sum(weights)) for w in weights]
            eta = [F(rng.randrange(5), 4) for _ in range(n)]
            f = [F(rng.randrange(5), 4) for _ in range(n)]
            dual, multiplier = dual_cost(rows, p, eta, f)
            assert dual == primal_cost(rows, p, eta, f)
            assert multiplier <= k * chi[k - 1]
            checks += 1
    return checks


def check_atom_likelihoods():
    checks = 0
    for r in range(1, 6):
        signs = list(product((-1, 1), repeat=r))
        for a, s, t in product((F(1, 8), F(1, 4)), signs, signs):
            inner = sum((F(1, 2) + y*a*s[i]) * (F(1, 2) + y*a*t[i]) * F(2, r)
                        for i, y in product(range(r), (-1, 1)))
            assert inner == 1 + 4*a*a*dot(s, t)/r
            checks += 1
    return checks


def check_examples():
    a = [(1, 1), (0, 1)]
    inverse = matrix_inverse(a)
    for step in range(9):
        t = F(step, 16)
        b, p, eta0, eta1, f, repaired, exact = lower_laws(a, inverse, 1, t)
        assert b == [(1, 1, 0), (0, 1, 1)]
        assert p == [F(1, 3)] * 3
        assert eta0 == [F(1, 2), F(1, 2), F(3, 4)]
        assert eta1[-1] == F(3, 4) + t/4
        assert f == [F(3, 4), F(1, 4), 1]
        assert repaired == [F(3, 4) - t/4, F(1, 4) + t/4, 1]
        assert exact == t/6 and primal_cost(b, p, eta1, f) == exact

    # Three crossing groups with three independent patterns.
    b = [(1, 1, 0), (0, 1, 1), (1, 0, 1)]
    p = [F(1, 6), F(1, 3), F(1, 2)]
    eta = [F(1, 4), F(1, 2), F(3, 4)]
    f = [F(3, 4), F(1, 4), F(3, 4)]
    residuals = [w * (y - x) for w, x, y in zip(p, f, eta)]
    plus = [(w+e)/2 for w, e in zip(p, residuals)]
    minus = [(w-e)/2 for w, e in zip(p, residuals)]
    assert sum(plus + minus) == 1 and min(plus + minus) >= 0
    atom_distance = sum(abs(x-y) for x, y in zip(plus, minus))
    assert atom_distance == primal_cost(b, p, eta, f) == F(1, 6)


def main():
    matrices, lower_cases, chi = check_lower_laws()
    print(f"Lower-bound laws: {lower_cases:,} cases over {matrices} invertible binary matrices.")
    print(f"Dual optimum and multiplier bound: {check_dual_lps(chi)} exact small LPs.")
    print(f"Independent-atom likelihood ratio: {check_atom_likelihoods():,} exact sign-pair checks.")
    check_examples()
    print("All nine illustrated repairs and the crossing-atom sign-flip example passed.")


if __name__ == "__main__":
    main()
