# Material parameter review — 1 October 2026

## Assessment

The library is a useful collection of infrared models, but **“verified” is too broad a description of the entire catalog**. Some defaults faithfully reproduce specific experiments, some are deliberately modified fits, some combine different experiments, and some lose important absorption channels. The strongest immediate concerns are SiC provenance and sample dependence, preprint versus published β-Ga₂O₃ parameters, GaN passivity, and overly broad validity claims.

No material definitions were changed in this review. Recommendations below are proposed changes, not new experimentally established universal constants.

## Scope and evidence

Reviewed all 45 packaged definitions in `src/materials_library/materials`, all 25 CSV tables, the evaluator, generator, catalog, tests, and the older `material_library 2` definitions. `build/lib` is a build copy rather than an independent experimental source. Numerical checks cover finite responses, dissipative tensor eigenvalues on approximately 30,000 frequencies per material, table ordering, zero-loss entries, and generator consistency. They are screening checks, not a proof of causality or experimental accuracy.

Evidence labels used here:

- **Direct**: primary paper or supporting table inspected and compared with the local values.
- **Local**: reproducible repository finding; does not depend on access to a paper.
- **Conditional**: scientifically plausible model with specimen or model restrictions; full transcription not independently recertified.
- **Pending**: a useful alternative or reference whose full numerical parameters were not obtained.

Independent numerical comparisons were concentrated on SiC, hBN, MoO₃, V₂O₅ and β-Ga₂O₃. The remaining entries received a parameter/model/provenance review and alternative-source assessment; this report does **not** claim that every coefficient in every paper was checked. Literature search prioritised experiments, established references, and recent relevant work. Citation counts vary by index, so none are used to rank numerical reliability. Several older references are retained because they measure the relevant infrared band; newer visible/UV work cannot validate phonon damping.

## Priority findings

| Priority | Finding | Evidence and recommended action |
|---|---|---|
| High | SiC4H YAML uses γ=6, generator uses γ=1.4, note says γ=1.4 | **Local + Direct.** Regeneration changes the numerical model by a factor 4.29 in damping. Preserve the intended broader-loss model as an explicitly identified alternative; retain a separate exact experimental specimen model. |
| High | β-Ga₂O₃ follows an earlier preprint, not the published parameter set | **Direct.** Preprint frame is x∥c; published frame is x∥a. The published ε∞ and oscillator fits also differ. Version both consistently; do not merely change the frame label or swap two diagonal elements. |
| High | GaN has negative dissipative response inside its declared range | **Local.** Minimum loss eigenvalue −2.2351×10⁻⁴ at 100 cm⁻¹; sampled negative region about 100–152.29 cm⁻¹. Limit the claimed range or refit a passive model. |
| High | Some defaults omit measured carriers, multiphonon absorption or interband absorption | **Local/model assessment.** Especially SiC6H, GaN, InN, narrow-gap III–V compounds and broad-range phonon-only models. Match carrier density and temperature before predicting losses. |
| Medium | “Verified” mixes source fits and modified models | III–V common damping, harmonic CdWO₄, modelled AlN extraordinary response, and combined-source InN need separate source-fidelity and applicability descriptions. |
| Medium | Zero imaginary permittivity can mean missing data | Ge, KBr and KRS5 tables are entirely zero-loss; GST amorphous is zero-loss in 72.2% of rows. Treat these as loss assumptions, not measured upper bounds. |
| Low | Si table contains a duplicate frequency | Two rows at 1508 cm⁻¹ differ in Im ε by 4.8×10⁻⁹. Negligible physics impact, but consolidate the duplicated abscissa before claiming strictly increasing interpolation data. |

### SiC: the concern about γ is justified, with sample qualifications

All frequencies and damping values in the following tables are in cm⁻¹. In this evaluator γ multiplies w in the denominator `TO² − w² − iγw`.

| Local model | ε∞ (ordinary / extraordinary) | TO | LO | γ currently evaluated |
|---|---|---|---|---|
| SiC3C | 6.52 | 796.2 | 972.2 | 3 |
| SiC4H | 6.6 / 6.9 | 797 / 782 | 970 / 964 | 6 / 6 |
| SiC6H | 6.6 / 6.8 | 797 / 788 | 972 / 967 | 2.7 / 2.7 |

**Direct comparison with Tiwald:** Table I gives γ=1.4 for 4H epilayer sample 9; sample 8 has γ=4.5, its substrate 8.6, and the implanted sample 12. For 6H, sample 7 has γ=2.7 and sample 6 has 4.7. The library's 6H phonon parameters match sample 7, but omit its carrier response (n≈2×10¹⁷ cm⁻³). The paper measured 700–4000 cm⁻¹ and included carriers and weaker multiphonon terms; the library's single-phonon range of 100–5000 is wider and simpler. These observations support specimen-specific fits, not a universal increase of γ. [Tiwald et al. (1999), Table I and Eq. 3](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevB.60.11464/fulltext).

**Independent experiment:** Pitman reports main-phonon widths around 5–6 for cubic SiC and ordinary 6H, and 5.5 for extraordinary 6H. Its convention explicitly defines Γ=2π×FWHM; use the quoted FWHM when mapping to this library's wavenumber denominator, rather than inserting Γ directly. The local note attributing “~6” specifically to CVD films on Si is too restrictive: the paper also reports single-crystal specimens. It describes Mutschke's damping choices as ad hoc. Thus Mutschke is useful context, but not sufficient experimental provenance for a low-loss default. [Pitman et al. (2008), fitting methods and results](https://arxiv.org/html/0803.1210); [authors' optical-constant files](https://epsc.wustl.edu/~hofmeist/spectra/IRSiC/).

Suggested treatment:

- **3C:** retain γ=3 as a low-loss modelling choice, with its provenance qualified; compare against a complete Pitman experimental fit/table with widths around 5–6. Do not change only damping and describe the resulting hybrid as an exact Pitman fit.
- **4H:** retain a complete sample-9 model at γ=1.4 and identify the current γ=6 model as a broader-loss assumption unless a matching measurement is supplied. Do not overwrite the current YAML by running the generator before reconciling intent.
- **6H:** retain the complete Tiwald sample-7 phonon fit at γ=2.7; add a Pitman alternative or sample-6 fit including its corresponding parameters and carriers. The existing γ is plausible for one specimen and optimistic for others.
- For an unspecified specimen, **γ=3, 6, 12 is a useful sensitivity sweep**, not a confidence interval or three universal measured values. Fit actual reflectance/ellipsometry when linewidths or propagation lengths are the output of interest.

Recent experiments reinforce the sample dependence. Chahal et al. measured polarized reflectivity of n-doped 4H (about 10¹⁸ cm⁻³) between 300 and 950 K; phonon and carrier parameters are anisotropic and temperature dependent. Its full fitted parameter data remain pending. Mainali et al. provide a recent broad-band 4H/6H ellipsometry comparison, but the complete parameter table must be obtained before adopting its TO–LO fit. Kulkarni et al. (2024) measure doping-related MWIR absorption, **outside the principal reststrahlen region**, so that study is relevant to the broad validity claim, not an alternative phonon γ. [Chahal et al. (2024)](https://doi.org/10.1016/j.jpcs.2023.111861), [Mainali et al.](https://doi.org/10.1116/6.0003676), [Kulkarni et al. (2024)](https://api.creol.ucf.edu/Publications/18015.pdf).

**Computed impact:** using the ordinary 6H oscillator at its lossless ε′=−1 frequency, 950.8157 cm⁻¹, the evaluator gives:

| γ | Im ε |
|---|---|
| 2.7 | 0.07257 |
| 6 | 0.16120 |
| 12 | 0.32197 |

Increasing γ from 2.7 to 6 increases loss here by approximately 2.22×. In the quasistatic isotropic surface factor `(ε−1)/(ε+1)`, the resonant enhancement consequently changes strongly. This is an illustrative single-axis calculation, not a calculated uniaxial surface mode or an s-SNOM linewidth. Tip geometry, carriers, surface layers and instrument resolution require their own treatment.

### β-Ga₂O₃: source-version mismatch, not just a transcription typo

The library's ε∞=(3.89, 2.90, 3.87), negligible xy term and c-axis frame follow the preprint. The published paper specifies x∥a and reports ε∞=(3.75, 3.21, 3.71), ε∞,xy≈−0.08 and revised fitted values. The catalog's statement that the other set has “origin unclear” should be reconsidered: its stated ε∞,xx=3.75, ε∞,yy=3.21 and xy=−0.08 agree with the published paper. This does not independently verify the entire secondary transcription. Keep a named preprint model or transcribe the final paper as a complete alternative, then verify amplitudes, damping, angle frame and tensor rotation together. [Preprint](https://arxiv.org/pdf/1512.08590), [published paper, Tables II and IV](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevB.93.125209/fulltext).

### hBN and MoO₃: small damping can be experimentally supported

All three hBN definitions match Giles Table S4, including ε∞, TO, LO and γ on both axes. The enriched samples are **98.7% ¹⁰B and 99.2% ¹¹B**, not mathematically pure isotopes. Their γ⊥=1.8/2.1 and γ∥=1 are legitimate reported fit values; natural hBN uses 7/3. Additional boundary and defect scattering can shorten measured propagation lengths without changing the intrinsic bulk oscillator γ. Giles also lists a natural-hBN comparison from Caldwell: ordinary ε∞=4.98, TO=1362.7, LO=1616.9, γ=7.3. [Giles et al., SI Table S4](https://fogler.physics.ucsd.edu/bib/Gilles2018ULP.pdf).

MoO₃ matches Álvarez-Pérez Table 1, including its weak x-axis oscillator γ=0.35. Small γ alone is not grounds for rejection. The same paper's preliminary far-field-only fit differs: x main LO=974.5, γ=6.8; z γ=0.65, versus final correlative values 963.0, 6.0 and 1.5. Prefer the final near-/far-field fit for the intended application. [Álvarez-Pérez et al., Table 1 and SI Table S3](https://arxiv.org/pdf/1912.06267).

### V₂O₅: numbers match, formula requires clarification

The preprint Methods lists the library's ε∞, TO/LO and damping values, including z=2.0/1.5. It states that ε∞ is calculated, TO/LO are adjusted using FTIR and s-SNOM, and damping is taken from earlier work. However, the displayed formula multiplies damping by TO/LO while the constants are labelled cm⁻¹; the library uses equal dimensionful γ directly. That dimensional ambiguity prevents certifying exact formula equivalence. Compare the evaluator with the publisher's Fig. 1 permittivity source data before calling it an exact reproduction. γz=1.5 is an explicitly discussed lifetime-fitting alternative. [Methods](https://arxiv.org/pdf/2501.08705), [publisher page](https://www.nature.com/articles/s41563-020-0665-0), [Fig. 1 source data](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41563-020-0665-0/MediaObjects/41563_2020_665_MOESM2_ESM.xlsx).

## Review of all packaged materials

“Conditional” below means no independently established replacement is justified by this review. Existing alternatives are often more useful than searching for a newer paper with an incompatible specimen.

| Material(s) | Current parameters/source and assessment | Alternative/reference and decision |
|---|---|---|
| SiC3C | γ=3; mixed Patrick/Choyke, Raman and Mutschke provenance | **Direct/conditional:** Pitman measured optical constants; compare widths 5–6 and use a complete fit. |
| SiC4H | γ=6 in package, 1.4 in generator | **Direct:** Tiwald specimen variants; reconcile generator before any release. |
| SiC6H | γ=2.7, Tiwald sample 7 phonon-only | **Direct:** Pitman and Tiwald sample 6; account for carriers. |
| hBN | γ=7/3, Giles natural | **Direct:** all parameters match; Caldwell comparison and Geick are independent context. |
| hBN_10B | γ=1.8/1, Giles | **Direct:** matches 98.7% enrichment; natural hBN is a different specimen. |
| hBN_11B | γ=2.1/1, Giles | **Direct:** matches 99.2% enrichment; preserve isotope label. |
| MoO3 | Five oscillators, final correlative fit | **Direct:** retain; preliminary far-field-only fit is an informative alternative, not an upgrade. |
| V2O5 | γ=40/19/2; hybrid experimental/calculated model | **Direct numbers, pending formula:** compare source curves; add z=1.5 variant. Clauws & Vennik (1976) is the damping-source lead. |
| Ga2O3_beta | Preprint oscillator tensor | **Direct:** add published set with its own frame; correct provenance. |
| CdWO4 | Mock fit with anharmonic terms disabled | **Conditional:** harmonic default is a modified source model. Retain full tensor; compare published spectrum before enabling anharmonic terms. |
| Al2O3 | Schubert factorized fit; separate TO/LO damping | **Conditional:** retain for phonons; existing Querry ordinary/extraordinary tables provide independent absorption comparison. Kischkat alumina film is a different structure. |
| AlN | γ=4.4; Moore three-term model, extraordinary response modelled | **Conditional:** retain factor-of-two convention conversion; compare existing Kischkat sputtered-film table only for films. |
| alpha_quartz | Gervais/Piriou 295 K rows, weak modes included | **Conditional:** Winta temperature-dependent model is appropriate for cryogenic work. Do not use low-temperature widths at room temperature. |
| calcite | Lane full infrared oscillator set; convention inferred | **Conditional:** existing Ma (2021) ghost-polariton alternative is simpler and scoped to mid-IR; inspect Lane formula before certifying amplitudes. |
| GaN | Kasic low-carrier sample; fixed/assumed extraordinary TO parameters | **Local issue:** negative loss below ~152.3. Existing Barker alternative γ=17 is an older film, not a universal correction. |
| InN | ε∞=6.7, γ=4.4 both axes; Kasic + Reparaz frequencies | **Conditional:** combined-source lattice model. Shared γ is not an independently measured extraordinary linewidth; doped InN needs carriers. Older copy differs substantially. |
| ZnO | Ashkenov bulk γ=13; ε∞=3.70/3.78 | **Conditional:** existing PLD-film fit γ=10 and Querry pellet are distinct useful specimens; do not average them. |
| MgO | Jasperse γ=7.619 for main mode; second oscillator | **Conditional:** retain near phonons; existing Stephens transparent index should replace constant asymptote when used above ~2000. |
| LiF | Jasperse γ=18.36; weak second term | **Conditional:** retain 295 K assumption; source temperature series is the appropriate alternative at other T. |
| AlAs | TO/LO=360.04/399.59; default γ=4.44 | **Conditional:** source γLO=3.03 stored as alternative; full Table 2 access pending. |
| GaP | 366.33/402.50; γ=2.59 | **Conditional:** source γLO=1.18 differs strongly; passive default is modified, not exact. |
| GaAs | 268.41/292.01; γ=2.51 | **Conditional:** source γLO=2.33; Skauli index table already available for transparent region. |
| InP | 303.62/345.32; γ=2.80 | **Conditional:** source γLO=0.95; common-damping model changes LO-region loss. |
| InAs | 217.36/240.20; γ=8.67 | **Conditional:** source γLO=2.01; Lorimor table is a transparent-range alternative. Need measured carrier absorption for doped samples. |
| InSb | 179.95/192.11; γ=4.45 | **Conditional:** source γLO=3.37; phonon-only model cannot certify broad-range loss for narrow-gap material. |
| Au | Olmon evaporated-film table | **Conditional, strong source choice:** compare Olmon template-stripped/single-crystal specimens and Ordal IR data; avoid switching to the visible-fit Derkachova default. |
| Ag | Yang table, Drude alternative γ=312.3 | **Conditional, strong source choice:** Ordal independent IR comparison; avoid τ conversion error. Surface ageing/film microstructure matter. |
| GST_amorphous | Frantz 2023 table; 72.2% rows have Im ε=0 | **Conditional:** recent experimental source; use Shportko (2008) independent phase comparison. Zero rows are not a demonstrated loss floor. |
| GST_crystalline | Frantz 2023 table | **Conditional:** specify annealing/crystalline phase and composition; Shportko is an independent comparator. |
| VO2_insulating | Beaini digitised film, 25°C | **Conditional:** prefer a direct electronic dataset if available; Wan broadband experiments are a strong alternative. |
| VO2_metallic | Same Beaini film, 100°C | **Conditional:** Wan and Qazilbash independent optical studies; effective-medium modelling required within transition, not simple endpoint interpolation. |
| Si | Chandler-Horowitz intrinsic table | **Local duplicate, otherwise conditional:** retain MWIR/LWIR source; Frey/Leviton/Madison temperature-dependent n only overlaps shorter wavelengths. No automatic doping option is exposed by evaluator. |
| Ge | Li 293 K real-index table, zero k | **Conditional:** useful transparent index; Frey/Leviton/Madison cryogenic alternative. Obtain absorption data for loss-sensitive simulations. |
| Diamond | Dore polycrystalline CVD n,k | **Conditional:** keep specimen label; local note proposing constant ε=5.65 at short λ is not an independently verified correction and removes absorption. |
| aSiO2 | Franta fused-silica table | **Conditional:** existing Popova and Kischkat film alternatives; NASA CHARMS data useful for shorter-wave temperature-dependent n, not phonon-region k. |
| Si3N4_film | Kischkat sputtered film table | **Conditional:** Cataldo measured low-stress nitride is a useful independent far-/mid-IR alternative; match deposition and stoichiometry. |
| PMMA | Tsuda 23 Lorentz oscillators | **Conditional:** get original fit/SI rather than cite only a scripts repository; do not infer IR line widths from visible refractive-index fits. |
| CaF2 | Kaiser phonon fit γ=4.63, broad term 114.8 | **Conditional:** existing Li transparent table; NASA temperature-dependent n alternative covers 0.4–5.6 μm, not the far-IR phonon. |
| BaF2 | Querry table | **Conditional:** existing Kaiser Lorentz fit provides independent comparison; Álvarez-Pérez SI also reports a fitted BaF₂ response. |
| KBr | Li real-index table, zero k | **Conditional:** require an independent absorptive far-IR dataset before loss claims; no replacement verified here. |
| KRS5 | Rodney real-index table, zero k | **Conditional:** specify TlBr/TlI composition and temperature; no modern loss dataset verified here. |
| ZnSe | Querry n,k table; 51.1% zero-loss rows | **Conditional:** require specimen-specific absorption for quantitative loss; no replacement coefficient set verified here. |
| graphene | Falkovsky local sheet model; μ=0.3 eV, T=300 K, τ=100 fs | **Conditional:** defaults are illustrative; Woessner experimental plasmon damping is a sample-matched comparator. The interband step is an approximation, not full finite-temperature Kubo conductivity. |
| black_phosphorus | Low intraband sheet model; n=10¹³ cm⁻², η=10 meV, masses 0.15/0.7 m₀ | **Conditional:** sample/layer-dependent defaults; compare gated experimental anisotropic conductivity. Interband response is absent, so the broad range is not universally justified. |
| vacuum | ε=1 | Exact ideal model; no alternative needed. |

### Common-damping III–V models

The six Lockwood defaults intentionally set γLO=γTO. This is a passive approximation, not the original independent fit. For one oscillator,

`Im ε ∝ w [γTO LO² − γLO TO² + (γLO−γTO)w²]`.

If γLO<γTO, the high-frequency tail eventually becomes negative. This explains why the stored “exact” alternatives need restricted interpretation; it does not justify labelling the modified defaults exact measurements. Obtain Table 2, preserve source uncertainties and fit range, and compare passive fits with the measured spectrum. [Lockwood et al. (2005)](https://doi.org/10.1016/j.ssc.2005.08.030).

GaN illustrates the converse limitation: γLO≥γTO alone is insufficient to ensure positivity at all frequencies. Its ordinary oscillator has `γTO LO²−γLO TO²<0`, which explains the observed low-frequency negative loss. A full frequency-range passivity screen is needed.

## Reference choices and access

| Reference | Why it is useful | Access/evidence in this review |
|---|---|---|
| [Tiwald 1999](https://doi.org/10.1103/PhysRevB.60.11464) | Experimental polytype, carriers, damage and damping comparisons | Full publisher PDF; Table I and model inspected. |
| [Pitman 2008](https://arxiv.org/html/0803.1210) | Independent polarized reflectance and optical constants | Full text inspected; downloadable author data identified. |
| [Chahal 2024](https://doi.org/10.1016/j.jpcs.2023.111861) | Recent polarized temperature-dependent n-doped 4H experiment | Abstract/method excerpts inspected; full damping table pending. |
| [Mainali](https://doi.org/10.1116/6.0003676) | Recent 4H/6H ellipsometry, TOLO/Lorentz comparison | Bibliographic/abstract lead; full coefficient table pending. |
| [Giles 2018](https://fogler.physics.ucsd.edu/bib/Gilles2018ULP.pdf) | Isotope-specific hBN infrared fits and polariton data | Full paper/SI; Table S4 numerically compared. |
| [Geick 1966](https://doi.org/10.1103/PhysRev.146.543) | Independent classic polarized hBN IR experiment | Primary publication identified; not re-transcribed. |
| [Álvarez-Pérez 2020](https://arxiv.org/pdf/1912.06267) | Correlative near-/far-field MoO₃ fit | Full paper/SI; final and preliminary parameter tables inspected. |
| [Taboada-Gutiérrez 2020](https://www.nature.com/articles/s41563-020-0665-0) | V₂O₅ polariton experiments and public source curves | Publisher page read in Browser; Methods from preprint. Formula ambiguity retained. |
| [Schubert 2016 published](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevB.93.125209/fulltext) | Full monoclinic tensor and experimentally fitted modes | Compared against [preprint](https://arxiv.org/pdf/1512.08590); source-version discrepancy confirmed. |
| [Schubert 2000](https://doi.org/10.1103/PhysRevB.61.8187) | Established sapphire IR ellipsometry | Primary abstract inspected; full numeric recertification not completed. |
| [Kischkat 2012](https://doi.org/10.1364/AO.51.006789) | Experimental deposited-film optical constants | Primary abstract and local tables; do not substitute for single-crystal material. |
| [Cataldo 2012](https://arxiv.org/abs/1209.2987) | Independent low-stress silicon nitride transmission fit | Primary abstract inspected; fit remains an alternative lead. |
| [Olmon 2012](https://nano-optics.colorado.edu/wp-content/uploads/2020/06/Olmon_PhysRevB_12_MainText.pdf) | Broad-band experimental Au, multiple preparation methods | Primary paper inspected for specimen and Drude comparison. |
| [Yang 2015](https://nano-optics.colorado.edu/wp-content/uploads/2020/06/Yang_PhysRevB_15_MainText.pdf) | Broad-band experimental Ag | Existing primary source; full table recertification not completed. |
| [Ordal 1985](https://physics.ucf.edu/~rep/EDII/Ordal1985.pdf) | Independent established IR/far-IR metal data | Primary experiment identified; no wholesale parameter replacement. |
| [Frantz 2023](https://doi.org/10.1364/OME.506019) | Recent GST endpoint/intermediate-state measurements | Full publisher text not obtained; local tables and bibliographic provenance reviewed. |
| [Shportko 2008](https://doi.org/10.1038/nmat2226) | Independent measured amorphous/crystalline dielectric response | Primary abstract inspected; use matching composition. |
| [Wan 2019](https://arxiv.org/abs/1901.02517) | VO₂ broadband ellipsometry and reflection to 30 μm | Primary abstract inspected; strong alternative to figure digitisation. |
| [Qazilbash 2008](https://arxiv.org/abs/0803.2739) | Independent VO₂ infrared/optical measurements | Primary abstract inspected; sample matching still required. |
| [Frey, Leviton & Madison 2006](https://arxiv.org/abs/physics/0606168) | Si/Ge measured n and dn/dT | Primary abstract inspected; limited wavelength overlap and no k replacement. |
| [NASA CaF₂/Infrasil](https://arxiv.org/abs/0805.0096) and [fused silica](https://arxiv.org/abs/0805.0091) | Temperature-dependent transparent-window indices | Primary abstracts inspected; outside far-IR phonon bands. |
| [Woessner 2015](https://www.nature.com/articles/nmat4169) | Experimental graphene plasmon damping | Use to calibrate sample scattering rather than treat τ=100 fs as intrinsic. |
| [Experimental BP intraband conductivity](https://pmc.ncbi.nlm.nih.gov/articles/PMC7793587/) | Gated, anisotropic Drude response and optical conductivity | Full primary article available; thickness/doping differs from generic monolayer default. |

Browser fallback succeeded for the Nature V₂O₅ landing page and exposed its public supporting-data links. Safari navigation reached the Lockwood ScienceDirect page, but no readable full parameter table was recovered. No subscription purchase was made. Direct network retrieval of upstream database files was unavailable in the shell, and the CSV conversion was **not** independently compared row-by-row with the upstream database. Sources behind access barriers remain pending; local data integrity is a separate check from source fidelity.

Requested from the user: **Lockwood 2005 Table 2** and **Chahal 2024 fitted phonon/carrier parameters and any supplementary data**. Additional useful retrievals are Mainali's full parameter table, Mock 2017 published Tables II–IV, and Tsuda 2018 oscillator-fit supplement. Until retrieved, their numerical provenance should not be upgraded by this report.

## Reproducible checks and minimal next changes

Run from the repository root:

```sh
python reports/audit_parameters.py
PYTHONPATH=src python -m pytest -q
```

The original audit is preserved in `reports/parameter_audit_baseline.json`; rerunning the audit writes `reports/parameter_audit_results.json`. The following findings describe the pre-correction baseline. It scans all 25 tables, including alternatives. The package tests passed: **3 passed**. System `python3` had no pytest; the available Conda `python` ran the tests successfully. All default material responses and table entries were finite in the scans. GaN was the only default with a negative loss eigenvalue below −10⁻⁸ on the tested grid. That result applies to defaults, not every stored alternative, and does not test zero frequency, arbitrary sheet overrides or causality.

The 45 packaged definitions match generator objects except **SiC4H**. The older library differs for **SiC4H and InN**, and contains three extra pending definitions: SrTiO₃, BaTiO₃ and CdO_doped. CdO's γ=1 is explicitly a placeholder, not measured; its recipe also describes a screened plasma frequency while the evaluator expects an unscreened Drude numerator. None of these pending entries should be promoted without a complete model and convention conversion.

Rounded range endpoints extend slightly beyond some tables (e.g. Ag 401 versus 401.284); these cause tiny endpoint clamps. The larger concern is physical validity: table clamping outside range, phonon-only models above their absorption band, and lossless index formulas used as if measured n,k. A zero k in a refractive-index-only source must be recorded as “not supplied” or “assumed zero”.

Recommended order of changes:

1. Reconcile SiC4H generator/YAML and retain clearly named specimen alternatives. Qualify SiC3C damping attribution and SiC6H carrier omission.
2. Version the β-Ga₂O₃ preprint and final-paper models; revise the claim that the final-paper-like set has unknown origin.
3. Restrict/refit GaN and add a dissipative-eigenvalue check over each model's supported frequency band.
4. Clarify V₂O₅ damping convention against source curves; distinguish measured, calculated, fitted and assumed parameters.
5. Replace blanket “verified” with source fidelity plus specimen/applicability notes, narrow unjustified ranges, and retain missing-loss flags.
6. Remove the duplicated Si abscissa and record original database revision/source identifiers for future reproducible table comparisons.

Avoid a global damping multiplier. It would obscure specimen differences and degrade experimentally supported hBN/MoO₃ low-loss fits. Keep damping tunable for actual sample calibration, and report simulation sensitivity until sample-matched optical data are available.

## Implemented corrections (2026-10-01)

The active library now preserves SiC4H Gamma=6 as an explicitly assumed broader-loss default and exposes the Tiwald sample-9 Gamma=1.4 lattice fit as a complete alternative. SiC3C has a labelled Gamma=6 sensitivity alternative and corrected damping attribution. SiC4H/6H use the 700–4000 cm⁻¹ source measurement band with lattice-only caveats. Narrow damping in hBN and MoO3 remains unchanged.

GaN is restricted to a conservative 300–1200 cm⁻¹ phonon modelling band, avoiding the negative-loss tail without changing its measured coefficients. MgO's default ends at 2000 cm⁻¹; its Stephens table remains available above that. Table bounds now follow actual coverage, zero-loss limitations are explicit, and the first duplicate Si row at 1508 cm⁻¹ was removed while retaining the last source value.

The beta-Ga2O3 fit is identified as the earlier preprint in its original frame, with a separate published-paper comparison reference. It has not been replaced by an incompletely transcribed final fit. Modified semiconductor/CdWO4 models, assumed sheet parameters, InN/AlN modelled components and calcite/V2O5 convention uncertainty now carry qualified statuses. V2O5's source-mentioned z Gamma=1.5 alternative is retained with the same convention caveat. The unsupported Diamond constant substitution and Si doping-option claim were removed.

Verification: **6 tests passed against the workspace source**. The current audit scans all 45 default materials and 25 tables: finite responses, no generator mismatches, no negative dissipative eigenvalues on the sampled declared bands, and strictly increasing table frequencies. The test configuration now selects the workspace source to prevent an older installed copy from silently being tested. These checks do not validate all alternatives, causality, extrapolation or specimen accuracy. Pending full references and source-curve checks listed above remain unresolved; no replacement coefficients were invented for them.
