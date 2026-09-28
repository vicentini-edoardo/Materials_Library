"""Built-in optical material catalog and permittivity evaluator.

Usage:
    from materials_library import load, eps_tensor
    m = load("Ga2O3_beta")                  # reads packaged materials/Ga2O3_beta.yaml
    E = eps_tensor(m, [600, 700, 800])      # -> complex array (N, 3, 3), frequency in cm^-1

Conventions (see README.md):
  * frequency: wavenumber in cm^-1; time dependence exp(-i w t)  ->  Im(eps) > 0 for loss
  * crystal frame x, y, z as declared in each YAML `frame:` block
  * Euler angles: intrinsic Z-X'-Z'' (phi, theta, psi) in degrees,
        R = Rz(phi) @ Rx(theta) @ Rz(psi),   eps_lab = R @ eps_diag @ R.T
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent

def names() -> tuple[str, ...]:
    """Canonical built-in material names, including entries marked pending."""
    return tuple(sorted((path.stem for path in (ROOT / "materials").glob("*.yaml")), key=str.casefold))

def load(name: str) -> dict:
    """Load one packaged definition by canonical name."""
    if name not in names():
        raise KeyError(f"Unknown built-in material: {name!r}")
    with (ROOT / "materials" / f"{name}.yaml").open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)

def euler_zxz(phi, theta, psi):
    p, t, s = np.radians([phi, theta, psi])
    Rz = lambda a: np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1.0]])
    Rx = lambda a: np.array([[1.0, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    return Rz(p) @ Rx(t) @ Rz(s)

# ---------------------------------------------------------------- scalar models
def _scalar(model: dict, w: np.ndarray) -> np.ndarray:
    t = model["type"]; w = np.asarray(w, float)
    if t == "constant":
        return np.full(w.shape, complex(model["eps"]))
    if t == "table":
        d = np.loadtxt(ROOT / model["file"], delimiter=",", comments="#")
        wc = np.clip(w, d[0, 0], d[-1, 0])
        return np.interp(wc, d[:, 0], d[:, 1]) + 1j * np.interp(wc, d[:, 0], d[:, 2])
    if t == "tolo":  # factorized TO-LO (Berreman-Unterwald-Lowndes)
        e = complex(model["eps_inf"]) * np.ones(w.shape, complex)
        for m in model["modes"]:
            gT = m.get("gamma_to", m.get("gamma")); gL = m.get("gamma_lo", m.get("gamma"))
            e *= (m["lo"] ** 2 - w**2 - 1j * gL * w) / (m["to"] ** 2 - w**2 - 1j * gT * w)
        return e + _drude(model.get("drude"), w)
    if t == "lorentz":  # additive: eps_inf + sum S w0^2/(w0^2 - w^2 - i g w)
        e = complex(model["eps_inf"]) * np.ones(w.shape, complex)
        for m in model["oscillators"]:
            e += m["strength"] * m["w0"] ** 2 / (m["w0"] ** 2 - w**2 - 1j * m["gamma"] * w)
        return e + _drude(model.get("drude"), w)
    if t == "drude":
        return complex(model.get("eps_inf", 1.0)) + _drude(model, w)
    raise ValueError(f"unknown model type {t}")

def _drude(d, w):
    if not d: return 0.0
    return -d["wp"] ** 2 / (w**2 + 1j * d["gamma"] * w)

# ---------------------------------------------------------------- tensors
def eps_tensor(mat: dict, w) -> np.ndarray:
    """Return eps(w) in the material's crystal frame, shape (N,3,3)."""
    w = np.atleast_1d(np.asarray(w, float)); N = len(w)
    E = np.zeros((N, 3, 3), complex)
    kind = mat["tensor"]
    if kind == "sheet":
        raise ValueError(f"{mat['name']} is a 2D sheet: use sheet_conductivity()")
    if kind in ("isotropic", "uniaxial", "biaxial"):
        ax = mat["axes"]
        for i, key in enumerate(("xx", "yy", "zz")):
            spec = ax.get(key) or ax.get({"xx": "ordinary", "yy": "ordinary", "zz": "extraordinary"}[key]) or ax["iso"]
            E[:, i, i] = _scalar(spec, w)
        return E
    if kind == "monoclinic":
        m = mat["model"]
        E += np.array(m["eps_inf"], float)[None]
        for o in m["oscillators"]:
            A, wt, g = o["amplitude"], o["to"], o["gamma"]
            G = o.get("anharmonic", 0.0)
            rho = (A**2 - 1j * G * w) / (wt**2 - w**2 - 1j * g * w)
            R = euler_zxz(*o["euler_deg"])
            D = R @ np.diag([1.0, 0, 0]) @ R.T      # rank-1 dyad e (x) e
            E += rho[:, None, None] * D[None]
        return E
    raise ValueError(kind)

def sheet_conductivity(mat: dict, w, **kw) -> np.ndarray:
    """2D sheet conductivity tensor sigma (Siemens), shape (N,3,3) with zz = 0."""
    w = np.atleast_1d(np.asarray(w, float))
    hbar, e, kB = 1.054571817e-34, 1.602176634e-19, 1.380649e-23
    om = 2 * np.pi * 2.99792458e10 * w                     # rad/s
    p = dict(mat["model"]["defaults"]); p.update(kw)
    S = np.zeros((len(w), 3, 3), complex)
    if mat["model"]["type"] == "graphene_falkovsky":
        mu = p["mu_eV"] * e; T = p["T_K"] * kB; tau_inv = 1.0 / (p["tau_fs"] * 1e-15)
        s_intra = 2j * e**2 * T / (np.pi * hbar**2 * (om + 1j * tau_inv)) * np.log(2 * np.cosh(mu / (2 * T)))
        x = hbar * om
        s_inter = e**2 / (4 * hbar) * (np.heaviside(x - 2 * mu, 0.5)
                   - 1j / (2 * np.pi) * np.log((x + 2 * mu) ** 2 / ((x - 2 * mu) ** 2 + (2 * T) ** 2)))
        S[:, 0, 0] = S[:, 1, 1] = s_intra + s_inter
        return S
    if mat["model"]["type"] == "bp_drude":
        n = p["n_cm2"] * 1e4; eta = p["eta_meV"] * 1e-3 * e / hbar; me = 9.1093837e-31
        for i, key in enumerate(("m_x", "m_y")):
            D = np.pi * e**2 * n / (p[key] * me)
            S[:, i, i] = 1j * D / (np.pi * (om + 1j * eta))
        return S
    raise ValueError(mat["model"]["type"])

def principal_axes_angle(E2x2: np.ndarray) -> np.ndarray:
    """In-plane principal-axis angle (deg, from x) of a real symmetric 2x2 block per frequency."""
    a, b, c = E2x2[:, 0, 0], E2x2[:, 0, 1], E2x2[:, 1, 1]
    return 0.5 * np.degrees(np.arctan2(2 * b, a - c))
