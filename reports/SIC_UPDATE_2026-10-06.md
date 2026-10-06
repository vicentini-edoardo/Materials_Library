# SiC experimental-default update — 2026-10-06

The defaults now use complete, specimen-specific phonon fits: Pitman's 3C wafer
and polarized gray 6H reflectance fits, and Klein's scalar 4H reflectance fit.
The initially selected Tiwald 4H sample-9 lattice fit is retained as an alternative,
following the user's subsequent selection of Klein 2025. Previous defaults remain
named alternatives. These are
phonon models, not universal dielectric functions including all absorption channels.

## Reference access

- **Klein 2025:** [arXiv v2 full text](https://arxiv.org/html/2503.04168v2)
  accessible; Eq. 1, its fitted parameters, Methods, and Fig. 2 checked.
  The [publisher DOI](https://doi.org/10.1021/acs.nanolett.5c01352) and ACS full text
  were not accessible through the web tool. Values match the user's supplied
  published-paper transcription. Fig. 2 covers 600–1200 cm⁻¹.
- **Pitman 2008:** [arXiv HTML](https://arxiv.org/html/0803.1210) and PDF downloaded
  and inspected, including Section 4.2 and figure parameters. The DOI resolver
  and publisher PDF were not accessible through the web tool.
- **Pitman numerical data:** [author-hosted files](https://epsc.wustl.edu/~hofmeist/spectra/IRSiC/)
  downloaded and used to check the complete complex curves, not only linewidths.
- **Tiwald 1999:** [publisher abstract](https://doi.org/10.1103/PhysRevB.60.11464)
  and [university landing page](https://digitalcommons.unl.edu/electricalengineeringfacpub/27/)
  accessible. University PDF returned HTTP 403 and publisher/Harvest downloads
  returned HTTP 401. Table I was **not independently re-read during this update**.
  The sample-9 parameters were already transcribed in the generator and reviewed
  in the [2026-10-01 report](MATERIAL_PARAMETER_REVIEW_2026-10-01.md).

## Changes in default values

Frequencies and damping are in cm⁻¹; perpendicular/parallel refer to the c axis.
For the new Lorentz models, LO below is the **undamped equivalent**, calculated
as TO × sqrt(1 + strength / eps_inf), not an independently entered parameter.

| Material/axis | eps_inf, old → new | TO, old → new | LO, old → new | gamma, old → new |
|---|---|---|---|---|
| 3C, isotropic | 6.52 → 7.0756 | 796.2 → 797.5 | 972.2 → ≈974.99 | 3.0 → 6.0 (+100%) |
| 4H, previous perpendicular → scalar approximation | 6.6 → 6.56 | 797 → 796 | 970 → 971 | common 6.0 → TO 2.9 / LO 3.0 |
| 4H, previous parallel → scalar approximation | 6.9 → 6.56 | 782 → 796 | 964 → 971 | common 6.0 → TO 2.9 / LO 3.0 |
| 6H, perpendicular | 6.6 → 7.04 | 797 → 797.5 | 972 → ≈967.91 | 2.7 → 5.3 (+96.3%) |
| 6H, parallel | 6.8 → 8.8 | 788 → 787.8 | 967 → ≈966.68 | 2.7 → 5.5 (+103.7%) |

3C and 6H change from factorized TO–LO to the existing additive Lorentz evaluator.
Dimensionless oscillator strengths are 3.5 (3C), 3.33 (6H perpendicular), and
4.45 (6H parallel). Background constants reproduce the authors' numerical curves;
they are not carried over from the previous Tiwald/Patrick models. In the library's
wavenumber denominator gamma equals Pitman's FWHM, not 2π times that width.

The 4H default uses Klein's single scalar Eq. 1 with separate TO/LO damping.
The source fits TO, LO and damping; eps_inf = 6.56 is adopted from Harima 1995.
The sample is a 500 µm commercial semi-insulating MSE Supplies wafer. No separate
extraordinary-axis fit is supplied. Accordingly the default is explicitly an
isotropic approximation (`tensor: isotropic`), not a measured isotropic 4H tensor.
The anisotropic Tiwald lattice fit remains available. This also makes 4H eligible
for SNOM_calculator's scalar-tip selection under the default approximation.

Declared ranges become 50–4000 for 3C (previously 100–5000) and 6H (previously
700–4000), corresponding to Pitman's far/mid-IR measurement band. 4H becomes
600–1200 (Fig. 2), rather than inheriting Tiwald's 700–4000 range. 3C and 6H
status is `verified` for these source fits; 4H remains `modified` to flag the
scalar approximation of an intrinsically uniaxial crystal. Status does not imply
that any fit applies to all specimens, doping levels, or temperatures.

Broader damping reduces and broadens the phonon resonance, but loss at a fixed
off-resonance frequency can increase. For example, at 900 cm⁻¹:

| Material/axis | Old eps | New eps |
|---|---|---|
| 3C | −5.0030 + 0.1767i | −5.7058 + 0.3967i |
| 4H, previous perpendicular → scalar | −4.9317 + 0.3563i | −4.9380 + 0.1735i |
| 4H, previous parallel → scalar | −4.1391 + 0.3003i | −4.9380 + 0.1735i |
| 6H, perpendicular | −5.0871 + 0.1625i | −5.1231 + 0.3334i |
| 6H, parallel | −4.4974 + 0.1452i | −5.7741 + 0.3810i |

## Source discrepancies and preserved alternatives

The ordinary 6H author filenames are interchanged: the file named
`grayalphaSiC_E_perp_c_nk_2osc_hires.txt` has the single-oscillator header
`7.04 797.5 5.3 3.33` and matches Fig. 4's single-oscillator curve. The file named
`...1osc_hires.txt` instead matches the two-oscillator model. The default uses the
numeric header and actual curve. Extraordinary TO = 787.8 follows Section 4.2 and
the author data; the Fig. 3 caption prints 787.5.

Preserved alternatives:

- 3C: `legacy_gamma3` (previous default) and existing `gamma6_sensitivity`.
- 4H: `gamma6_sensitivity` (original assumed-loss default) and `Tiwald1999_sample9`
  (the anisotropic gamma = 1.4 fit selected earlier in this update).
- 6H: `Tiwald1999_sample7` (previous lattice-only default, gamma = 2.7).

Alternatives are not selected automatically. For a uniaxial alternative, replace
the material's `axes` with its `xx`, `yy`, `zz` entries before calling `eps_tensor`;
for an isotropic alternative, use `axes = {"iso": alternative}`. Also adopt the
alternative's `valid_range_cm1`. For either 4H alternative also set `tensor` and
`frame` from the alternative to restore its uniaxial representation. Tiwald sample
7 has carriers (2×10¹⁷ cm⁻³) whose
response remains omitted from that alternative. Pitman's single-oscillator fits
omit weak folded features by design.

## Verification

All ten tests pass, including literal author-data checks at 700, 797 and
900 cm⁻¹ and hand-calculated Klein Eq. 1 checks at TO, LO, and 900 cm⁻¹.
Full-curve comparisons at all 4000 integer wavenumbers give maximum
absolute complex-eps differences of 7.03×10⁻⁵ (3C), 6.99×10⁻⁵ (6H perpendicular)
and 2.85×10⁻³ (6H parallel), consistent with rounded author data/parameters.
The parameter audit checks all 45 materials and 25 tables: no generator
mismatches, negative loss, or non-increasing table frequencies.

Local reinstall instructions are in [README.md](../README.md). No package was
installed into the user's active environment as part of this update.
