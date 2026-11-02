#!/usr/bin/env python3
"""Exact test of simulation.md §8 on a 1D lattice gas. Exit status 1 on any mismatch.

Counted excesses are compared with activity derivatives because the relations
equate them; a transfer matrix makes both exact, with no sampling error.
Implicit solvent only (site states: empty, cosolute, solute): the (T, P) forms
and ions are not covered here.
"""

import sys

import numpy as np

E33, E23, E22 = -0.7, -1.1, 0.4
Z3 = 0.35


def solvent(z3):
    T = np.array([[1.0, np.sqrt(z3)], [np.sqrt(z3), z3 * np.exp(-E33)]])
    w, V = np.linalg.eigh(T)
    return T, w[-1], np.abs(V[:, -1])


def tvec(z3, e=E23):
    return np.array([1.0, np.sqrt(z3) * np.exp(-e)])


def c1(z3, e=E23):
    _, lam, v = solvent(z3)
    return (v @ tvec(z3, e)) ** 2 / lam**2


def g22(r, z3):
    if r == 0:
        return 0.0  # one solute per site
    T, lam, v = solvent(z3)
    t = tvec(z3)
    K = np.exp(-E22) if r == 1 else t @ np.linalg.matrix_power(T, r - 2) @ t
    return K * lam ** (2 - r) / (v @ t) ** 2


def messages(n, is_solute, T, lam, v, t):
    """Solvent-state messages along a chain; each solute site restarts them from t."""
    out, cur = [None] * n, v
    for i in range(n):
        if is_solute(i):
            cur = None
            continue
        cur = t if cur is None else (T @ cur / lam if i else cur)
        cur = cur / cur.max()
        out[i] = cur
    return out


def counted_excess(solutes, z3, e=E23, pad=80):
    """Sum over sites of P(cosolute | solutes fixed) − ρ3; solute sites give −ρ3."""
    T, lam, v = solvent(z3)
    t = tvec(z3, e)
    n = max(solutes) + 1 + 2 * pad
    occupied = {s + pad for s in solutes}
    fw = messages(n, occupied.__contains__, T, lam, v, t)
    bw = messages(n, lambda i: n - 1 - i in occupied, T, lam, v, t)[::-1]
    rho3 = v[1] ** 2
    total = 0.0
    for i in range(n):
        if i in occupied:
            total -= rho3
        else:
            p = fw[i] * bw[i]
            total += p[1] / p.sum() - rho3
    return total


def dlnz(f, z, h=1e-5):
    return (f(z * np.exp(h)) - f(z * np.exp(-h))) / (2 * h)


def b22(z):
    return -0.5 * (g22(0, z) - 1 + 2 * sum(g22(r, z) - 1 for r in range(1, 200)))


def transfer(z2, z3):
    a, b = np.sqrt(z3), np.sqrt(z2)
    return np.array([[1, a, b],
                     [a, z3 * np.exp(-E33), a * b * np.exp(-E23)],
                     [b, a * b * np.exp(-E23), z2 * np.exp(-E22)]])


def marginals(z2, z3):
    w, V = np.linalg.eigh(transfer(z2, z3))
    return w[-1], V[:, -1] ** 2


def kbi(i, j, z2, z3, rmax=400):
    """Lattice G_ij at finite ρ2 by direct pair-correlation sum (states: 1 = cosolute, 2 = solute)."""
    w, V = np.linalg.eigh(transfer(z2, z3))
    lam, v = w[-1], V[:, -1]
    pi, pj = v[i] ** 2, v[j] ** 2
    G = -1.0  # one particle per site
    Tn = np.eye(3)
    for r in range(1, rmax):
        Tn = Tn @ transfer(z2, z3) / lam
        G += (v[i] * Tn[i, j] * v[j] + v[j] * Tn[j, i] * v[i]) / (pi * pj) - 2
    return G


def main():
    problems = 0

    def check(name, a, b, tol):
        nonlocal problems
        ok = abs(a - b) <= tol
        problems += not ok
        print(f"{'ok ' if ok else 'BAD'} {name}: {a:.8f} vs {b:.8f}")

    n0 = counted_excess({0}, Z3)
    check("N23 = dln c1/dln a3", n0, dlnz(lambda z: np.log(c1(z)), Z3), 1e-7)

    def dn(r):
        return counted_excess({0, r}, Z3) - 2 * n0

    for r in (1, 2, 3, 5):
        check(f"dln g22({r})/dln a3 = ΔN23", dlnz(lambda z: np.log(g22(r, z)), Z3), dn(r), 1e-7)

    dB = dlnz(b22, Z3)
    check("dB22/dln a3 = −½∫g22 ΔN23", dB,
          -0.5 * 2 * sum(g22(r, Z3) * dn(r) for r in range(1, 81)), 1e-5)

    _, m0 = marginals(0.0, Z3)
    z2 = 1e-4 / c1(Z3)
    lam, m = marginals(z2, Z3)
    lam0, _ = marginals(0.0, Z3)
    check("B22 = −½G22", b22(Z3), (np.log(lam / lam0) - m[2]) / m[2] ** 2, 1e-3)

    z2 = 1e-3 / c1(Z3)
    _, m = marginals(z2, Z3)
    check("per-solute excess slope = −dB22/dln a3", ((m[1] - m0[1]) / m[2] - n0) / m[2], -dB, 3e-4)

    # The differential response is a different quantity from the per-solute excess.
    # Smaller ρ2 than above: its B3 term is three times the per-solute one.
    z2 = 1e-4 / c1(Z3)
    _, m = marginals(z2, Z3)
    h = 1e-3
    _, up = marginals(z2 * np.exp(h), Z3)
    _, dn_ = marginals(z2 * np.exp(-h), Z3)
    diff = (up[1] - dn_[1]) / (up[2] - dn_[2])
    check("∂ρ3/∂ρ2 slope = −2 dB22/dln a3", (diff - n0) / m[2], -2 * dB, 1e-4)
    check("∂ρ3/∂ρ2 = ρ3G23/(1 + ρ2G22)", diff,
          m[1] * kbi(1, 2, z2, Z3) / (1 + m[2] * kbi(2, 2, z2, Z3)), 1e-7)

    # Two-state solute: mixture rule and state-weight derivative.
    ea, eb, wa, wb = -1.1, 0.5, 1.0, 0.6
    ca, cb = wa * c1(Z3, ea), wb * c1(Z3, eb)
    pa = ca / (ca + cb)
    na, nb = counted_excess({0}, Z3, ea), counted_excess({0}, Z3, eb)
    mean = pa * na + (1 - pa) * nb
    check("N23 = Σ pσ N23^σ", mean,
          dlnz(lambda z: np.log(wa * c1(z, ea) + wb * c1(z, eb)), Z3), 1e-7)
    check("dpσ/dln a3 = pσ(N23^σ − ⟨N23⟩)",
          dlnz(lambda z: wa * c1(z, ea) / (wa * c1(z, ea) + wb * c1(z, eb)), Z3),
          pa * (na - mean), 1e-7)

    print(f"{problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
