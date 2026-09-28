# Built-in optical material catalog

45 infrared materials for anisotropic transfer-matrix / s-SNOM simulations. Every parameter carries its reference, and nothing depends on pyGTM (GPL-3.0). Tabulated data come from the public-domain (CC0) [refractiveindex.info database](https://github.com/polyanskiy/refractiveindex.info-database).

## Layout

| Path | Content |
|---|---|
| `src/materials_library/materials/<name>.yaml` | One file per material: model, parameters, frame, valid range, status, notes, references |
| `src/materials_library/data/<name>.csv` | Tabulated permittivity, columns `freq_cm1,eps_real,eps_imag`, ascending frequency, source in the header |
| `src/materials_library/__init__.py` | Loader and evaluator: `eps_tensor(material, w_cm1)` → (N,3,3), `sheet_conductivity(...)` for 2D sheets |
| `tools/build_library.py` | Generator for the material YAML files |

Edit `tools/build_library.py`, then run `python tools/build_library.py` and `python -m pytest`. The YAML files are generated.

## Conventions

- Frequency: wavenumber ω in cm⁻¹. Time dependence e^(−iωt), so Im ε > 0 means loss.
- Tensor classes: `isotropic` (axis key `iso`), `uniaxial` / `biaxial` (keys `xx`, `yy`, `zz`, diagonal in the crystal frame given under `frame`), `monoclinic` (full tensor, see below), `sheet` (2D conductivity, not a bulk ε).
- Scalar model types (`src/materials_library/__init__.py`, function `_scalar`):

| `type` | Formula | Keys |
|---|---|---|
| `constant` | ε | `eps` |
| `table` | linear interpolation, clamped at the ends | `file` |
| `tolo` | ε∞ Π (ω_LO² − ω² − iγ_LO ω)/(ω_TO² − ω² − iγ_TO ω) | `eps_inf`, `modes[{to, lo, gamma}]` or `{to, lo, gamma_to, gamma_lo}` |
| `lorentz` | ε∞ + Σ S ω₀²/(ω₀² − ω² − iγω) | `eps_inf`, `oscillators[{w0, strength, gamma}]` |
| `drude` | ε∞ − ω_p²/(ω² + iγω) | `eps_inf`, `wp`, `gamma` (cm⁻¹); also allowed as `drude:` inside `tolo`/`lorentz` |

- Euler angles: intrinsic Z–X′–Z″ (φ, θ, ψ) in degrees, R = R_z(φ) R_x(θ) R_z(ψ), and ε_rotated = R ε_diag Rᵀ.
- `status`: all current materials are **verified**: values read from the cited source during this build and cross-checked.
- `alternatives:` in a YAML holds other sourced models for the same material (film vs bulk, Drude vs table).

## Index

### Polar crystals (phonon polaritons)

| Material | Tensor | Model | Range (cm⁻¹) | Status | Sources |
|---|---|---|---|---|---|
| [`Al2O3`](src/materials_library/materials/Al2O3.yaml) | uniaxial | TO-LO, 4 modes/axis | 100–5000 | verified | Schubert2000; Querry1985 |
| [`AlN`](src/materials_library/materials/AlN.yaml) | uniaxial | lorentz | 50–14000 | verified | Moore2005; Kischkat2012 |
| [`alpha_quartz`](src/materials_library/materials/alpha_quartz.yaml) | uniaxial | TO-LO, 6 modes/axis | 300–1600 | verified | GervaisPiriou1975; Winta2019 |
| [`calcite`](src/materials_library/materials/calcite.yaml) | uniaxial | lorentz | 50–2000 | verified | Lane1999; Ma2021 |
| [`CdWO4`](src/materials_library/materials/CdWO4.yaml) | monoclinic | 15 rank-1 oscillators + ε∞ tensor | 80–1200 | verified | Mock2017 |
| [`Ga2O3_beta`](src/materials_library/materials/Ga2O3_beta.yaml) | monoclinic | 12 rank-1 oscillators + ε∞ tensor | 150–1200 | verified | Schubert2016; HyperbolicOptics |
| [`GaAs`](src/materials_library/materials/GaAs.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | verified | Lockwood2005 |
| [`GaN`](src/materials_library/materials/GaN.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Kasic2000; Barker1973 |
| [`GaP`](src/materials_library/materials/GaP.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | verified | Lockwood2005 |
| [`hBN`](src/materials_library/materials/hBN.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Giles2018 |
| [`hBN_10B`](src/materials_library/materials/hBN_10B.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Giles2018 |
| [`hBN_11B`](src/materials_library/materials/hBN_11B.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Giles2018 |
| [`InAs`](src/materials_library/materials/InAs.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | verified | Lockwood2005 |
| [`InN`](src/materials_library/materials/InN.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Kasic2002; Reparaz2018 |
| [`MgO`](src/materials_library/materials/MgO.yaml) | isotropic | lorentz | 100–27778 | verified | Jasperse1966; Stephens1952 |
| [`MoO3`](src/materials_library/materials/MoO3.yaml) | biaxial | TO-LO, 3 modes/axis | 400–1200 | verified | AlvarezPerez2020 |
| [`SiC3C`](src/materials_library/materials/SiC3C.yaml) | isotropic | TO-LO, 1 mode/axis | 100–5000 | verified | PatrickChoyke1970; Olego1982; Mutschke1999; Pitman2008 |
| [`SiC4H`](src/materials_library/materials/SiC4H.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Tiwald1999 |
| [`SiC6H`](src/materials_library/materials/SiC6H.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Tiwald1999; PatrickChoyke1970 |
| [`V2O5`](src/materials_library/materials/V2O5.yaml) | biaxial | TO-LO, 1 mode/axis | 400–1200 | verified | TaboadaGutierrez2020 |
| [`ZnO`](src/materials_library/materials/ZnO.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Ashkenov2003; Querry1985 |

### 2D sheets

| Material | Tensor | Model | Range (cm⁻¹) | Status | Sources |
|---|---|---|---|---|---|
| [`black_phosphorus`](src/materials_library/materials/black_phosphorus.yaml) | sheet | bp drude | 10–5000 | verified | Low2014 |
| [`graphene`](src/materials_library/materials/graphene.yaml) | sheet | graphene falkovsky | 10–20000 | verified | Falkovsky2008 |

### Metals, phase-change and doped

| Material | Tensor | Model | Range (cm⁻¹) | Status | Sources |
|---|---|---|---|---|---|
| [`Ag`](src/materials_library/materials/Ag.yaml) | isotropic | table | 401–37037 | verified | Yang2015 |
| [`Au`](src/materials_library/materials/Au.yaml) | isotropic | table | 401–33333 | verified | Olmon2012; Derkachova2016 |
| [`GST_amorphous`](src/materials_library/materials/GST_amorphous.yaml) | isotropic | table | 338–28549 | verified | Frantz2023 |
| [`GST_crystalline`](src/materials_library/materials/GST_crystalline.yaml) | isotropic | table | 309–28549 | verified | Frantz2023 |
| [`VO2_insulating`](src/materials_library/materials/VO2_insulating.yaml) | isotropic | table | 400–20000 | verified | Beaini2020 |
| [`VO2_metallic`](src/materials_library/materials/VO2_metallic.yaml) | isotropic | table | 400–20000 | verified | Beaini2020 |

### Substrates, windows, films, polymers

| Material | Tensor | Model | Range (cm⁻¹) | Status | Sources |
|---|---|---|---|---|---|
| [`AlAs`](src/materials_library/materials/AlAs.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | verified | Lockwood2005 |
| [`aSiO2`](src/materials_library/materials/aSiO2.yaml) | isotropic | table | 80–403000 | verified | Franta2016; Kischkat2012; Popova1972 |
| [`BaF2`](src/materials_library/materials/BaF2.yaml) | isotropic | table | 60–45455 | verified | Querry1987; Kaiser1962 |
| [`CaF2`](src/materials_library/materials/CaF2.yaml) | isotropic | lorentz | 125–1000 | verified | Kaiser1962; Li1980b |
| [`Diamond`](src/materials_library/materials/Diamond.yaml) | isotropic | table | 20–4000 | verified | Dore1998 |
| [`Ge`](src/materials_library/materials/Ge.yaml) | isotropic | table | 556–5263 | verified | Li1980 |
| [`InP`](src/materials_library/materials/InP.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | verified | Lockwood2005 |
| [`InSb`](src/materials_library/materials/InSb.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | verified | Lockwood2005 |
| [`KBr`](src/materials_library/materials/KBr.yaml) | isotropic | table | 238–50000 | verified | Li1976 |
| [`KRS5`](src/materials_library/materials/KRS5.yaml) | isotropic | table | 254–17331 | verified | Rodney1956 |
| [`LiF`](src/materials_library/materials/LiF.yaml) | isotropic | lorentz | 100–5000 | verified | Jasperse1966 |
| [`PMMA`](src/materials_library/materials/PMMA.yaml) | isotropic | lorentz | 550–4000 | verified | Tsuda2018 |
| [`Si`](src/materials_library/materials/Si.yaml) | isotropic | table | 430–4000 | verified | ChandlerHorowitz2005 |
| [`Si3N4_film`](src/materials_library/materials/Si3N4_film.yaml) | isotropic | table | 700–6500 | verified | Kischkat2012 |
| [`vacuum`](src/materials_library/materials/vacuum.yaml) | isotropic | constant | 0–1e+09 | verified | — |
| [`ZnSe`](src/materials_library/materials/ZnSe.yaml) | isotropic | table | 460–20000 | verified | Querry1987 |


## Monoclinic materials: rotated diagonal matrices and Euler angles

**Short answer: no single rotated diagonal matrix reproduces ε(ω) of β‑Ga₂O₃ or CdWO₄, but the tensor is exactly a sum of rotated diagonal (rank‑1) matrices, each with its own fixed Euler angles.**

In a monoclinic crystal the b axis (here z) is a principal axis at every frequency. In the a–c plane, however, every Bu phonon has its own dipole direction α_l. The principal axes of Re ε therefore rotate with frequency, and those of Im ε rotate differently (see `figures/monoclinic_principal_axes.png`). The best single fixed rotation still leaves |ε_xy| up to 68 (Ga₂O₃) and 51 (CdWO₄) inside the reststrahlen bands. A diagonal material + one Euler rotation is therefore only an approximation, valid in a narrow band far from the phonons.

The exact form used here (Schubert's eigendielectric-displacement model) is

```
eps(w) = eps_inf + sum_l rho_l(w) * R(phi_l, theta_l, psi_l) · diag(1, 0, 0) · R^T
rho_l(w) = (A_l^2 - i Gamma_l w) / (w_TO,l^2 - w^2 - i gamma_l w)        (Gamma_l = 0 for Ga2O3)
```

| Term | Euler angles (φ, θ, ψ) | Meaning |
|---|---|---|
| Bu mode l | (α_l, 0, 0) | Dipole in the x–y (a–c) plane at angle α_l from x |
| Au mode | (0, 90, 90) | Dipole along z = b |
| ε∞ of Ga₂O₃ | (0, 0, 0) | ε∞ is already diagonal: diag(3.89, 2.90, 3.87) |
| ε∞ of CdWO₄ | (76.9, 0, 0) | diag(4.83, 4.44, 4.25) rotated about b |

Each oscillator's Euler angles are stored in its YAML as `euler_deg`, so an engine that accepts a list of (scalar response, rotation) pairs can build the full tensor. The current app accepts only diagonal `xx/yy/zz`, so these two materials need an engine extension (a full 3×3 ε per layer) before they can be used there. `to_app_json.py` skips them for that reason.

Crystal frames: Ga₂O₃ x ∥ c, z ∥ b, y ⊥ b, c (α measured from c). CdWO₄ x ∥ a, z ∥ b, y = c* (α measured from a). A sample cut is then one more global rotation applied to the whole tensor.

Checks: Ga₂O₃ reproduces the paper's ε_DC (11.51, 11.89, 11.15, xy −0.05) within 0.03. CdWO₄ reproduces ε_DC,zz = 11.57 and ε_DC,xy = 1.05. Its xx/yy (15.66 / 16.51) differ from the paper's 16.16 / 16.01, but the published Table IV says those were extrapolated from the measured spectra, and det(ε_DC), the quantity the generalized LST relation tests, agrees to 0.1 %. The published CdWO₄ angles differ from the arXiv ones by 180° for four modes, which is the same dipole direction. The CdWO₄ default is the harmonic (passive) model; the paper's anharmonic broadenings are stored as `anharmonic_paper` (rename to `anharmonic` to enable them, at the cost of a small negative Im ε_zz near 271 cm⁻¹).

For uniaxial crystals (calcite, quartz, hBN, sapphire…) the tensor is diagonal in the crystal frame at every frequency. A tilted optic axis, as in the ghost-polariton calcite cut, is just one global rotation of the whole tensor: an optic axis at polar angle θ from the surface normal (lab z) and in-plane azimuth φ_az (from lab x) is Euler (φ_az + 90°, θ, 0), because R ẑ = (sin θ cos φ_az, sin θ sin φ_az, cos θ) for that choice.

## Still to source

| Material | What is missing | Lead |
|---|---|---|
| SrTiO₃ | LO modes, damping (ε∞ and 3 TO known) | not yet found in an open source |
| BaTiO₃ | Full phonon model, tetragonal anisotropy | — |
| CdO (In:CdO) | Film damping (only in Fig. 4b / Supplement of Nolen 2020), LO phonon (Finkenrath et al., ref. 85 there) | Nolen et al., Phys. Rev. Mater. 4, 025202 (2020) Supplemental |
| LaAlO₃, LiNbO₃, LiTaO₃ | IR phonon parameters | not searched yet |
| ITO, AZO | Drude parameters (sample dependent) | — |
| Bi₂Se₃ | THz phonons + Dirac plasmon | not searched yet |
