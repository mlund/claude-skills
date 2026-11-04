#!/usr/bin/env python3
"""Exact ideal-limit reference values for titration and Donnan checks.

Conventions: dPhi = Phi_sys - Phi_res; pH_sys = pH_res + beta e dPhi / ln 10;
c0 = 1 M; activities are relative, molar standard state.
"""
import argparse
import math

NA_PER_A3 = 6.02214076e-4  # number per Å³ per molar
E2_K = 1.602176634e-19**2 / (4 * math.pi * 8.8541878128e-12 * 1.380649e-23) * 1e10  # Å·K


def alpha(pH, pKa):
    """Henderson-Hasselbalch degree of ionization for a monoprotic acid."""
    return 1 / (1 + 10 ** (pKa - pH))


def _pair_weight(m, Z, lam):
    """Weight of m anions and m + Z cations in an ideal open system, up to a constant."""
    return math.exp((2 * m + Z) * math.log(lam) - math.lgamma(m + 1) - math.lgamma(m + Z + 1))


def _sum_pairs(Z, lam, f=lambda m: 1.0):
    # Terms decay fast beyond lam, so a margin of a few hundred is ample
    terms = int(lam) + Z + 400
    return sum(f(m) * _pair_weight(m, Z, lam) for m in range(terms))


def donnan_exact(Z, lam):
    """Exact ideal means at finite N: mean N_plus, mean N_minus, mean of N_plus * N_minus."""
    norm = _sum_pairs(Z, lam)
    n_minus = _sum_pairs(Z, lam, lambda m: m) / norm
    return n_minus + Z, n_minus, _sum_pairs(Z, lam, lambda m: m * (m + Z)) / norm


def paired_alpha(Z, pH, pKa, lam):
    """Exact ideal alpha for GCT: P(n) proportional to C(Z,n) x^n I_n(2 lam), a_Na = a_Cl."""
    x = 10 ** (pH - pKa)
    w = [math.comb(Z, n) * x**n * _sum_pairs(n, lam) for n in range(Z + 1)]
    return sum(n * v for n, v in enumerate(w)) / sum(w) / Z


def donnan(Z, N_res):
    """Macroscopic product rule, N_res >> 1; returns N_plus, N_minus, beta e dPhi."""
    root = math.hypot(Z / 2, N_res)
    n_plus, n_minus = root + Z / 2, root - Z / 2
    return n_plus, n_minus, math.log(n_minus / N_res)


def relabel(a_H, a_plus, a_minus, beta_e_dphi):
    """Activities in the other label; a_H a_minus and a_H/a_plus stay fixed."""
    f = math.exp(-beta_e_dphi)
    return a_H * f, a_plus * f, a_minus / f


def rpm_mu_ex(c_salt, d, eps, T):
    """beta*mu_ex of the restricted primitive model: Carnahan-Starling + MSA (1:1 salt)."""
    lB = E2_K / (eps * T)
    ct = c_salt * NA_PER_A3
    eta = math.pi * d**3 * ct / 3
    kappa = math.sqrt(8 * math.pi * lB * ct)
    cs = (8 * eta - 9 * eta**2 + 3 * eta**3) / (1 - eta) ** 3
    msa = lB * (math.sqrt(1 + 2 * kappa * d) - kappa * d - 1) / (d**2 * kappa)
    return cs + msa


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pH", type=float, help="pH_in")
    ap.add_argument("--pKa", type=float)
    ap.add_argument("--Z", type=float, help="fixed negative charge, in e")
    ap.add_argument("--salt", type=float, help="reservoir 1:1 salt, molar")
    ap.add_argument("--volume", type=float, help="free volume, Å³")
    ap.add_argument("--d", type=float, help="ion diameter, Å")
    ap.add_argument("--eps", type=float, default=78.0)
    ap.add_argument("--T", type=float, default=298.15)
    ap.add_argument("--dphi", type=float, help="beta e dPhi for relabelling")
    ap.add_argument("--paired", type=int, metavar="SITES", help="exact GCT alpha for this many sites; needs --pH --pKa --salt --volume")
    args = ap.parse_args()

    if args.pH is not None and args.pKa is not None:
        print(f"alpha, independent sites = {alpha(args.pH, args.pKa):.6f}")
    a = args.salt
    if args.salt and args.d:
        bmu = rpm_mu_ex(args.salt, args.d, args.eps, args.T)
        a = args.salt * math.exp(bmu)
        print(f"RPM beta*mu_ex = {bmu:.4f}, a_salt = {a:.5f} M (approximate; verify with N2)")
    if args.salt and args.volume:
        n_res = args.salt * NA_PER_A3 * args.volume
        print(f"N_res = lambda = {n_res:.2f}; exact ideal <N+N-> = {n_res**2:.1f}")
        if args.Z is not None:
            np_, nm, bdphi = donnan(args.Z, n_res)
            print(f"macroscopic N+ = {np_:.2f}, N- = {nm:.2f}, beta e dPhi = {bdphi:.4f}")
            print(f"macroscopic pH_sys - pH_res = {bdphi / math.log(10):.4f}")
            ep, em, ex = donnan_exact(int(args.Z), n_res)
            print(f"exact <N+> = {ep:.3f}, <N-> = {em:.3f}, <N+N-> = {ex:.3f} (lambda^2 = {n_res**2:.3f})")
    if args.paired and args.salt and args.volume:
        print(f"exact paired-move alpha = {paired_alpha(args.paired, args.pH, args.pKa, args.salt * NA_PER_A3 * args.volume):.5f}")
    if args.dphi is not None and args.pH is not None and a:
        h, p, m = relabel(10 ** -args.pH, a, a, args.dphi)
        print(f"relabelled: pH_in = {-math.log10(h):.4f}, a_cation = {p:.5f}, a_anion = {m:.5f}")


if __name__ == "__main__":
    main()
