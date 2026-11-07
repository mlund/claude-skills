#!/usr/bin/env python3
"""Symbolic Kirkwood–Buff algebra for checking and deriving relations.

Isothermal, n-component, uncharged. Every derivative is taken from the
open-system fluctuation matrix (kb-integrals.md §1.3),

    dρ_i = Σ_j B_ij dβμ_j,    B_ij = ρ_iρ_jG_ij + ρ_iδ_ij,

with β dP = Σ ρ_i dβμ_i (Gibbs–Duhem). Working in dβμ keeps the gradients
polynomial; only the final linear solve introduces fractions. Any
(∂X/∂Y)_{Z...} then follows by solving dY = 1, dZ_k = 0, so held-constant
variables are always explicit.

Units: μ and P carry a factor β, so V̄_i and kTκ_T come out as volumes.
Symbols are shared across systems (KB("13") and KB("123") both use rho1,
G13), so binary 1–3 results can be substituted into ternary limits.

Usage:
    from kb_sym import KB, check
    s = KB("123")
    g23 = s.d(s.m("3"), s.m("2"), fixed=[s.mu["1"], s.mu["3"]])
    check(s.dilute(g23, "2"), s.rho["3"] * (s.G("2", "3") - s.G("1", "2")))

Run this file to verify the skill's equations; exit status 1 on a failure.
Salts need an electroneutrality constraint that is not built in (salts.md §10).
"""

import random
import sys

import sympy as sp


class KB:
    def __init__(self, labels):
        self.labels = list(labels)
        n = len(self.labels)
        self.rho = {a: sp.Symbol(f"rho{a}", positive=True) for a in self.labels}
        # Placeholders: they mark where μ and P enter an expression for grad().
        self.mu = {a: sp.Symbol(f"mu{a}") for a in self.labels}
        self.P = sp.Symbol("P")
        r = [self.rho[a] for a in self.labels]
        self.B = sp.Matrix(n, n, lambda i, j: r[i] * r[j] * self.G(self.labels[i], self.labels[j])
                           + (r[i] if i == j else 0))

    @staticmethod
    def G(a, b):
        a, b = sorted((a, b))
        return sp.Symbol(f"G{a}{b}")

    def m(self, a, solvent="1"):
        """Molality as a number ratio (ρ_a/ρ_solvent); the solvent mass factor cancels."""
        return self.rho[a] / self.rho[solvent]

    def x(self, a):
        return self.rho[a] / sum(self.rho.values())

    def grad(self, expr):
        """Row vector of ∂expr/∂(βμ_j) at constant T, by the chain rule."""
        g = sp.zeros(1, len(self.labels))
        for i, a in enumerate(self.labels):
            g += sp.diff(expr, self.rho[a]) * self.B[i, :]
            g[i] += sp.diff(expr, self.mu[a])
        g += sp.diff(expr, self.P) * sp.Matrix([[self.rho[a] for a in self.labels]])
        return g

    def d(self, X, Y, fixed):
        """(∂X/∂Y) at constant T and the n−1 expressions in `fixed`."""
        if len(fixed) != len(self.labels) - 1:
            raise ValueError(f"need {len(self.labels) - 1} fixed variables besides T")
        A = sp.Matrix.vstack(self.grad(Y), *[self.grad(z) for z in fixed])
        rhs = sp.zeros(len(self.labels), 1)
        rhs[0] = 1
        return sp.cancel((self.grad(X) * A.LUsolve(rhs))[0])

    def ratios(self, ref=None):
        """Fixed composition: the n−1 ratios ρ_a/ρ_ref."""
        ref = ref or self.labels[0]
        return [self.rho[a] / self.rho[ref] for a in self.labels if a != ref]

    def vbar(self, a):
        return self.d(self.mu[a], self.P, self.ratios())

    def kTkappa(self):
        return self.d(sp.log(self.rho[self.labels[0]]), self.P, self.ratios())

    def dilute(self, expr, a):
        """Limit ρ_a → 0. Cancel first: B is singular there, so naive subs can give 0/0."""
        expr = sp.cancel(sp.together(expr))
        num, den = sp.fraction(expr)
        r = self.rho[a]
        if sp.simplify(den.subs(r, 0)) != 0:
            return sp.cancel(num.subs(r, 0) / den.subs(r, 0))
        return sp.limit(expr, r, 0)


def check(lhs, rhs, trials=20, seed=1):
    """'exact' if lhs − rhs simplifies to 0; else 'numeric' if 0 at random points; else False.

    The numeric fallback exists because simplify can miss true identities.
    """
    diff = sp.cancel(sp.together(lhs - rhs))
    if diff == 0 or sp.simplify(diff) == 0:
        return "exact"
    rng = random.Random(seed)
    syms = sorted(diff.free_symbols, key=str)
    for _ in range(trials):
        val = diff.subs({s: sp.Rational(rng.randint(1, 97), rng.randint(1, 13)) for s in syms})
        if val != 0:
            return False
    return "numeric"


def _selftest():
    results = []

    def t(name, lhs, rhs):
        results.append((name, check(lhs, rhs)))

    # Binary A–B: Ben-Naim 1977 (10.1063/1.434669); kb-integrals.md §3, §14.
    b = KB("AB")
    rA, rB = b.rho["A"], b.rho["B"]
    GAA, GBB, GAB = b.G("A", "A"), b.G("B", "B"), b.G("A", "B")
    eta = rA + rB + rA * rB * (GAA + GBB - 2 * GAB)
    zeta = 1 + rA * GAA + rB * GBB + rA * rB * (GAA * GBB - GAB**2)
    VA, VB = b.vbar("A"), b.vbar("B")
    t("BN77 2.4  V̄_A", VA, (1 + rB * (GBB - GAB)) / eta)
    t("BN77 2.3  kTκ_T = ζ/η", b.kTkappa(), zeta / eta)
    t("BN77 2.9  Σρ_iV̄_i = 1", rA * VA + rB * VB, 1)
    t("BN77 2.13 V̄_AV̄_B", VA * VB, (zeta - eta * GAB) / eta**2)

    # Binary 1–3 quantities, reused at solute infinite dilution.
    s2 = KB("13")
    r1, r3 = s2.rho["1"], s2.rho["3"]
    G11, G13, G33 = s2.G("1", "1"), s2.G("1", "3"), s2.G("3", "3")
    a33 = s2.d(s2.mu["3"], sp.log(r3), [s2.P])
    t("Pierce 15 a33", a33, 1 / (1 + r3 * (G33 - G13)))
    phi1, phi3 = r1 * s2.vbar("1"), r3 * s2.vbar("3")
    kTk = s2.kTkappa()

    # Ternary: Pierce et al. 2008 (10.1007/s12013-007-9005-0),
    # Smith 2006a (10.1021/jp056100e); gamma-linkage.md §4–7.
    s = KB("123")
    r2 = s.rho["2"]
    G12, G22, G23 = s.G("1", "2"), s.G("2", "2"), s.G("2", "3")
    mu1, mu2, mu3 = s.mu["1"], s.mu["2"], s.mu["3"]
    m2, m3 = s.m("2"), s.m("3")

    g23 = s.d(m3, m2, [mu1, mu3])
    t("Smith06a 11 Γ23 finite ρ2", g23, r3 * (G23 - G12) / (1 + r2 * (G22 - G12)))
    g0 = s.dilute(g23, "2")
    t("Pierce 21 Γ23°", g0, r3 * (G23 - G12))
    t("Smith06a 14 (∂ρ3/∂ρ2)°_{μ1,μ3}",
      s.dilute(s.d(r3, r2, [mu1, mu3]), "2"), r3 * G23)

    gP3 = s.dilute(s.d(m3, m2, [s.P, mu3]), "2")
    gP1 = s.dilute(s.d(m3, m2, [s.P, mu1]), "2")
    t("Pierce 23 (∂m3/∂m2)°_{P,μ3}", gP3, r3 / r1 + r3 * (G23 - G12 + G11 - G13))
    t("Pierce 23 offset φ3/(a33φ1)", gP3, g0 + phi3 / (a33 * phi1))
    t("Pierce 24 (∂m3/∂m2)°_{P,μ1}", gP1, -1 + r3 * (G23 - G12 + G13 - G33))
    t("Pierce 24 offset −1/a33", gP1, g0 - 1 / a33)
    t("Pierce 25 φ1Γ′ + φ3Γ″ = Γ23", phi1 * gP3 + phi3 * gP1, g0)

    V2 = s.dilute(s.vbar("2"), "2")
    N21, N23 = r1 * G12, r3 * G23
    t("Pierce 28 V̄2°", V2, kTk - N21 * s2.vbar("1") - N23 * s2.vbar("3"))
    t("Smith06a 34 ρ3G23", r3 * G23, phi1 * g0 - r3 * (V2 - kTk))

    # Pseudo-chemical potential βμ2* = βμ2 − ln ρ2; ρ2 fixed is the dilute (T,P) path.
    dmu2 = s.dilute(s.d(mu2 - sp.log(r2), sp.log(r3), [s.P, r2]), "2")
    t("Pierce 26 −β∂μ2*/∂lnρ3 = Γ23 a33", -dmu2, g0 * a33)

    width = max(len(n) for n, _ in results)
    for name, res in results:
        print(f"{name:<{width}}  {res or 'FAIL'}")
    return all(res for _, res in results)


if __name__ == "__main__":
    sys.exit(0 if _selftest() else 1)
