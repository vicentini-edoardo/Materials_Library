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
- `status`: `verified` denotes a source transcription, not universal experimental validity; `modified` denotes a deliberate model change or omitted source contribution; `modelled` includes assumed parameters; `preprint` denotes an earlier source version; `partial` denotes an unresolved source convention. Read the specimen and applicability notes.
- `alternatives:` in a YAML holds other models for the same material, including explicitly labelled sensitivity assumptions. Alternatives are not selected automatically by the evaluator.

## Index

### Polar crystals (phonon polaritons)

| Material | Tensor | Model | Range (cm⁻¹) | Status | Sources |
|---|---|---|---|---|---|
| [`Al2O3`](src/materials_library/materials/Al2O3.yaml) | uniaxial | TO-LO, 4 modes/axis | 100–5000 | verified | Schubert2000; Querry1985 |
| [`AlN`](src/materials_library/materials/AlN.yaml) | uniaxial | lorentz | 50–14000 | modelled | Moore2005; Kischkat2012 |
| [`alpha_quartz`](src/materials_library/materials/alpha_quartz.yaml) | uniaxial | TO-LO, 6 modes/axis | 300–1600 | verified | GervaisPiriou1975; Winta2019 |
| [`calcite`](src/materials_library/materials/calcite.yaml) | uniaxial | lorentz | 50–2000 | partial | Lane1999; Ma2021 |
| [`CdWO4`](src/materials_library/materials/CdWO4.yaml) | monoclinic | 15 rank-1 oscillators + ε∞ tensor | 80–1200 | modified | Mock2017 |
| [`Ga2O3_beta`](src/materials_library/materials/Ga2O3_beta.yaml) | monoclinic | 12 rank-1 oscillators + ε∞ tensor | 150–1200 | preprint | Schubert2016_preprint; Schubert2016_published |
| [`GaAs`](src/materials_library/materials/GaAs.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | modified | Lockwood2005; Skauli2003 |
| [`GaN`](src/materials_library/materials/GaN.yaml) | uniaxial | TO-LO, 1 mode/axis | 300–1200 | modified | Kasic2000; Barker1973 |
| [`GaP`](src/materials_library/materials/GaP.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | modified | Lockwood2005 |
| [`hBN`](src/materials_library/materials/hBN.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Giles2018 |
| [`hBN_10B`](src/materials_library/materials/hBN_10B.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Giles2018 |
| [`hBN_11B`](src/materials_library/materials/hBN_11B.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Giles2018 |
| [`InAs`](src/materials_library/materials/InAs.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | modified | Lockwood2005; Lorimor1965 |
| [`InN`](src/materials_library/materials/InN.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | modelled | Kasic2002; Reparaz2018 |
| [`MgO`](src/materials_library/materials/MgO.yaml) | isotropic | lorentz | 100–2000 | verified | Jasperse1966; Stephens1952 |
| [`MoO3`](src/materials_library/materials/MoO3.yaml) | biaxial | TO-LO, 3 modes/axis | 400–1200 | verified | AlvarezPerez2020 |
| [`SiC3C`](src/materials_library/materials/SiC3C.yaml) | isotropic | TO-LO, 1 mode/axis | 100–5000 | modified | PatrickChoyke1970; Olego1982; Mutschke1999; Pitman2008 |
| [`SiC4H`](src/materials_library/materials/SiC4H.yaml) | uniaxial | TO-LO, 1 mode/axis | 700–4000 | modified | Tiwald1999 |
| [`SiC6H`](src/materials_library/materials/SiC6H.yaml) | uniaxial | TO-LO, 1 mode/axis | 700–4000 | modified | Tiwald1999; PatrickChoyke1970 |
| [`V2O5`](src/materials_library/materials/V2O5.yaml) | biaxial | TO-LO, 1 mode/axis | 400–1200 | partial | TaboadaGutierrez2020 |
| [`ZnO`](src/materials_library/materials/ZnO.yaml) | uniaxial | TO-LO, 1 mode/axis | 100–5000 | verified | Ashkenov2003; Querry1985 |

### 2D sheets

| Material | Tensor | Model | Range (cm⁻¹) | Status | Sources |
|---|---|---|---|---|---|
| [`black_phosphorus`](src/materials_library/materials/black_phosphorus.yaml) | sheet | bp drude | 10–5000 | modelled | Low2014 |
| [`graphene`](src/materials_library/materials/graphene.yaml) | sheet | graphene falkovsky | 10–20000 | modelled | Falkovsky2008 |

### Metals, phase-change and doped

| Material | Tensor | Model | Range (cm⁻¹) | Status | Sources |
|---|---|---|---|---|---|
| [`Ag`](src/materials_library/materials/Ag.yaml) | isotropic | table | 401.284–37037 | verified | Yang2015 |
| [`Au`](src/materials_library/materials/Au.yaml) | isotropic | table | 401.123–33333 | verified | Olmon2012; Derkachova2016 |
| [`GST_amorphous`](src/materials_library/materials/GST_amorphous.yaml) | isotropic | table | 338–28548.6 | verified | Frantz2023 |
| [`GST_crystalline`](src/materials_library/materials/GST_crystalline.yaml) | isotropic | table | 309–28548.6 | verified | Frantz2023 |
| [`VO2_insulating`](src/materials_library/materials/VO2_insulating.yaml) | isotropic | table | 400–20000 | verified | Beaini2020 |
| [`VO2_metallic`](src/materials_library/materials/VO2_metallic.yaml) | isotropic | table | 400–20000 | verified | Beaini2020 |

### Substrates, windows, films, polymers

| Material | Tensor | Model | Range (cm⁻¹) | Status | Sources |
|---|---|---|---|---|---|
| [`AlAs`](src/materials_library/materials/AlAs.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | modified | Lockwood2005 |
| [`aSiO2`](src/materials_library/materials/aSiO2.yaml) | isotropic | table | 80–403000 | verified | Franta2016; Kischkat2012; Popova1972 |
| [`BaF2`](src/materials_library/materials/BaF2.yaml) | isotropic | table | 60–45454.5 | verified | Querry1987; Kaiser1962 |
| [`CaF2`](src/materials_library/materials/CaF2.yaml) | isotropic | lorentz | 125–1000 | verified | Kaiser1962; Li1980b |
| [`Diamond`](src/materials_library/materials/Diamond.yaml) | isotropic | table | 20–4000 | verified | Dore1998 |
| [`Ge`](src/materials_library/materials/Ge.yaml) | isotropic | table | 556–5263 | verified | Li1980 |
| [`InP`](src/materials_library/materials/InP.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | modified | Lockwood2005 |
| [`InSb`](src/materials_library/materials/InSb.yaml) | isotropic | TO-LO, 1 mode/axis | 50–5000 | modified | Lockwood2005 |
| [`KBr`](src/materials_library/materials/KBr.yaml) | isotropic | table | 238.095–50000 | verified | Li1976 |
| [`KRS5`](src/materials_library/materials/KRS5.yaml) | isotropic | table | 254–17331 | verified | Rodney1956 |
| [`LiF`](src/materials_library/materials/LiF.yaml) | isotropic | lorentz | 100–5000 | verified | Jasperse1966 |
| [`PMMA`](src/materials_library/materials/PMMA.yaml) | isotropic | lorentz | 550–4000 | verified | Tsuda2018 |
| [`Si`](src/materials_library/materials/Si.yaml) | isotropic | table | 430–4000 | verified | ChandlerHorowitz2005 |
| [`Si3N4_film`](src/materials_library/materials/Si3N4_film.yaml) | isotropic | table | 700–6500 | verified | Kischkat2012 |
| [`vacuum`](src/materials_library/materials/vacuum.yaml) | isotropic | constant | 0–1e+09 | verified |  |
| [`ZnSe`](src/materials_library/materials/ZnSe.yaml) | isotropic | table | 460.001–20000 | verified | Querry1987 |


## Reference table

References used by the active material definitions, including alternatives and comparison-only sources. The material notes distinguish which fit is implemented.

| Key | Reference | Link |
|---|---|---|
| AlvarezPerez2020 | G. Álvarez-Pérez et al., Adv. Mater. 32, 1908176 (2020) (alpha-MoO3), Table 1 | [Source](https://arxiv.org/abs/1912.06267) |
| Ashkenov2003 | N. Ashkenov et al., J. Appl. Phys. 93, 126 (2003), Tables I-II | [Source](https://doi.org/10.1063/1.1526935) |
| Barker1973 | A. S. Barker, M. Ilegems, Phys. Rev. B 7, 743 (1973), Tables I-II | [Source](https://doi.org/10.1103/PhysRevB.7.743) |
| Beaini2020 | R. Beaini et al., Sol. Energy Mater. Sol. Cells 205, 110260 (2020) (70 nm VO2 film on SiO2) | — |
| ChandlerHorowitz2005 | D. Chandler-Horowitz, P. M. Amirtharaj, J. Appl. Phys. 97, 123526 (2005) | [Source](https://doi.org/10.1063/1.1923612) |
| Derkachova2016 | A. Derkachova, K. Kolwas, I. Demchenko, Plasmonics 11, 941 (2016) | [Source](https://doi.org/10.1007/s11468-015-0128-7) |
| Dore1998 | P. Dore et al., Appl. Opt. 37, 5731 (1998) (CVD diamond) | [Source](https://doi.org/10.1364/AO.37.005731) |
| Falkovsky2008 | L. A. Falkovsky, Optical properties of graphene, J. Phys.: Conf. Ser. 129, 012004 (2008) | [Source](https://arxiv.org/abs/0806.3663) |
| Franta2016 | D. Franta et al., Proc. SPIE 9890, 989014 (2016) (fused silica) | [Source](https://doi.org/10.1117/12.2227580) |
| Frantz2023 | J. A. Frantz et al., Opt. Mater. Express 13, 3631 (2023) (Ge2Sb2Te5) | — |
| GervaisPiriou1975 | F. Gervais, B. Piriou, Phys. Rev. B 11, 3944 (1975), Tables I-II (T = 295 K rows) | [Source](https://doi.org/10.1103/PhysRevB.11.3944) |
| Giles2018 | A. J. Giles et al., Nat. Mater. 17, 134 (2018) (hBN isotopes), SI Table S4 | [Source](https://fogler.physics.ucsd.edu/bib/Gilles2018ULP.pdf) |
| Jasperse1966 | J. R. Jasperse, A. Kahan, J. N. Plendl, S. S. Mitra, Phys. Rev. 146, 526 (1966), Tables I-II (295 K) | [Source](https://doi.org/10.1103/PhysRev.146.526) |
| Kaiser1962 | W. Kaiser, W. G. Spitzer, R. H. Kaiser, L. E. Howarth, Phys. Rev. 127, 1950 (1962) | [Source](https://github.com/polyanskiy/refractiveindex.info-scripts) |
| Kasic2000 | A. Kasic, M. Schubert, S. Einfeldt, D. Hommel, T. E. Tiwald, Phys. Rev. B 62, 7365 (2000), Tables I-III (sample A) | [Source](https://doi.org/10.1103/PhysRevB.62.7365) |
| Kasic2002 | A. Kasic, M. Schubert, Y. Saito, Y. Nanishi, G. Wagner, Effective electron mass and phonon modes in n-type hexagonal InN, Phys. Rev. B 65, 115206 (2002) | [Source](https://doi.org/10.1103/PhysRevB.65.115206) |
| Kischkat2012 | J. Kischkat et al., Mid-infrared optical properties of thin films of Al2O3, TiO2, SiO2, AlN and Si3N4, Appl. Opt. 51, 6789 (2012) | [Source](https://doi.org/10.1364/AO.51.006789) |
| Lane1999 | M. D. Lane, J. Geophys. Res. Planets 104, 14099 (1999), Table 1 | [Source](https://doi.org/10.1029/1999JE900025) |
| Li1976 | H. H. Li, Refractive index of alkali halides..., J. Phys. Chem. Ref. Data 5, 329 (1976) | — |
| Li1980 | H. H. Li, Refractive index of silicon and germanium..., J. Phys. Chem. Ref. Data 9, 561 (1980) | [Source](https://doi.org/10.1063/1.555624) |
| Li1980b | H. H. Li, Refractive index of alkaline earth halides..., J. Phys. Chem. Ref. Data 9, 161 (1980) | — |
| Lockwood2005 | D. J. Lockwood, G. Yu, N. L. Rowell, Solid State Commun. 136, 404 (2005), Table 2 (293 K) | [Source](https://doi.org/10.1016/j.ssc.2005.08.030) |
| Lorimor1965 | O. G. Lorimor, W. G. Spitzer, J. Appl. Phys. 36, 1841 (1965) (InAs) | — |
| Low2014 | T. Low et al., Plasmons and screening in monolayer and multilayer black phosphorus, Phys. Rev. Lett. 113, 106802 (2014) | [Source](https://arxiv.org/abs/1404.4035) |
| Ma2021 | W. Ma et al., Ghost hyperbolic surface polaritons in bulk anisotropic crystals, Nature 596, 362 (2021), Methods Eq. 4 (values from Hellwege et al. 1970) | [Source](https://doi.org/10.1038/s41586-021-03755-1) |
| Mock2017 | A. Mock, R. Korlacki, S. Knight, M. Schubert, Phys. Rev. B 95, 165202 (2017), Tables II-IV | [Source](https://doi.org/10.1103/PhysRevB.95.165202) |
| Moore2005 | W. J. Moore, J. A. Freitas, R. T. Holm, O. Kovalenkov, V. Dmitriev, Appl. Phys. Lett. 86, 141912 (2005), Table I | [Source](https://doi.org/10.1063/1.1899233) |
| Mutschke1999 | H. Mutschke et al., A&A 345, 187 (1999) (SiC polytypes), Table 1 | [Source](https://arxiv.org/abs/astro-ph/9903031) |
| Olego1982 | D. Olego et al. (1982), Raman — via Ioffe NSM | — |
| Olmon2012 | R. L. Olmon et al., Optical dielectric function of gold, Phys. Rev. B 86, 235147 (2012) | [Source](https://doi.org/10.1103/PhysRevB.86.235147) |
| PatrickChoyke1970 | L. Patrick, W. J. Choyke (1970) — via Ioffe NSM | [Source](https://www.ioffe.ru/SVA/NSM/Semicond/SiC/optic.html) |
| Pitman2008 | K. M. Pitman et al., A&A 483, 661 (2008) (3C-SiC) | [Source](https://arxiv.org/abs/0803.1210) |
| Popova1972 | S. Popova, T. Tolstykh, V. Vorobev, Opt. Spectrosc. 33, 444 (1972) (amorphous quartz) | — |
| Querry1985 | M. R. Querry, Optical constants, Contractor Report CRDC-CR-85034 (1985) | — |
| Querry1987 | M. R. Querry, Optical constants of minerals and other materials..., CRDEC-CR-88009 (1987) | — |
| Reparaz2018 | J. S. Reparaz et al., Comparative study of the pressure dependence of optical-phonon transverse-effective charges and linewidths in wurtzite InN, Phys. Rev. B 98, 165204 (2018) | [Source](https://doi.org/10.1103/PhysRevB.98.165204) |
| Rodney1956 | W. S. Rodney, I. H. Malitson, J. Opt. Soc. Am. 46, 956 (1956) (KRS-5) | [Source](https://doi.org/10.1364/JOSA.46.000956) |
| Schubert2000 | M. Schubert, T. E. Tiwald, C. M. Herzinger, Phys. Rev. B 61, 8187 (2000) (sapphire) | [Source](https://www.academia.edu/28131084/Infrared_dielectric_anisotropy_and_phonon_modes_of_sapphire) |
| Schubert2016_preprint | Schubert et al., arXiv:1512.08590, earlier preprint fit (x parallel c) | [Source](https://arxiv.org/pdf/1512.08590) |
| Schubert2016_published | Schubert et al., Phys. Rev. B 93, 125209 (2016), revised published fit (x parallel a); comparison only | [Source](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevB.93.125209/fulltext) |
| Skauli2003 | T. Skauli et al., J. Appl. Phys. 94, 6447 (2003) (GaAs) | — |
| Stephens1952 | R. E. Stephens, I. H. Malitson, J. Res. Natl. Bur. Stand. 49, 249 (1952) | — |
| TaboadaGutierrez2020 | J. Taboada-Gutiérrez et al., Nat. Mater. (2020) (alpha-V2O5), Methods section of the arXiv version | [Source](https://arxiv.org/abs/2501.08705) |
| Tiwald1999 | T. E. Tiwald, J. A. Woollam, S. Zollner et al., Phys. Rev. B 60, 11464 (1999), Table I | [Source](https://doi.org/10.1103/PhysRevB.60.11464) |
| Tsuda2018 | S. Tsuda et al., Opt. Express 26, 6899 (2018) (PMMA Lorentz–Drude fit) | [Source](https://github.com/polyanskiy/refractiveindex.info-scripts) |
| Winta2019 | C. J. Winta et al., Low-temperature infrared dielectric function of hyperbolic alpha-quartz, arXiv:1902.03072 (2019), Tables I-II | [Source](https://arxiv.org/abs/1902.03072) |
| Yang2015 | H. U. Yang et al., Optical dielectric function of silver, Phys. Rev. B 91, 235137 (2015) | [Source](https://nano-optics.colorado.edu/wp-content/uploads/2020/06/Yang_PhysRevB_15_MainText.pdf) |

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
