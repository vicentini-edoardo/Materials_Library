# Materials Library

Sourced optical material models for infrared simulations (anisotropic transfer-matrix, s-SNOM). The catalog holds 49 materials: polar crystals, 2D sheets, metals, phase-change and doped materials, substrates, windows, films and polymers. Every parameter set cites its reference. Nothing depends on pyGTM (GPL-3.0).

- **[CATALOG.md](CATALOG.md)**: full index, model formulas, conventions and reference table.
- **Data**: one YAML per material in `src/materials_library/materials/`, plus 25 CSV tables in `src/materials_library/data/`.
- **Requires**: Python ≥ 3.11, `numpy`, `PyYAML`.

## Install

```bash
python -m pip install git+https://github.com/vicentini-edoardo/Materials_Library.git
```

For development, clone and install editable. Data edits then take effect without reinstalling:

```bash
git clone https://github.com/vicentini-edoardo/Materials_Library.git
cd Materials_Library
python -m pip install -e ".[test]"
```

## Usage

```python
from materials_library import names, load, variants, eps_tensor, sheet_conductivity

names()                                   # canonical material names
hbn = load("hBN")                         # dict: metadata, axes/model, references, status, valid range
eps = eps_tensor(hbn, [800, 1000])        # complex array, shape (N, 3, 3)

variants("Au")                            # alternative model sets, e.g. ('drude_Derkachova2016',)
au = load("Au", variant="drude_Derkachova2016")

sigma = sheet_conductivity(load("graphene"), [800, 1000], mu_eV=0.3)  # 2D sheet, siemens
```

| Function | Returns |
|---|---|
| `names()` | Sorted tuple of material names |
| `load(name, variant=None)` | Material definition; `variant` selects an entry of `alternatives` |
| `variants(name)` | Names of the alternative model sets of one material |
| `eps_tensor(material, w_cm1)` | Permittivity tensor in the crystal frame, shape `(N, 3, 3)` |
| `sheet_conductivity(material, w_cm1, **params)` | Sheet conductivity tensor for 2D materials; keyword arguments override the model defaults |
| `euler_zxz(phi, theta, psi)` | Rotation matrix for the Euler convention below |

## Conventions

- Frequency is wavenumber in cm⁻¹. Time dependence is exp(−iωt), so Im ε > 0 means loss.
- `eps_tensor` returns ε in the material's crystal frame (declared under `frame` in each YAML). Rotate it yourself for other cuts: ε_lab = R ε Rᵀ, with R = R_z(φ) R_x(θ) R_z(ψ) (intrinsic Z–X′–Z″, degrees).
- Table models interpolate linearly and clamp outside their table range.
- Sheet materials (graphene, black phosphorus) are 2D conductivities. `eps_tensor` raises `ValueError` for them.
- Monoclinic materials (β-Ga₂O₃, CdWO₄, gypsum) are exact sums of rotated rank-1 oscillators, so their principal axes rotate with frequency. See [CATALOG.md](CATALOG.md#monoclinic-materials-rotated-diagonal-matrices-and-euler-angles).

## Status labels and valid range

| `status` | Meaning |
|---|---|
| `verified` | Source transcription. It does not guarantee validity for every specimen or frequency. |
| `modified` | Deliberate model change, or an omitted source contribution. |
| `modelled` | Includes assumed parameters. |
| `preprint` | Taken from an earlier version of the source. |
| `partial` | Unresolved source convention. |

Always read a material's `status`, `notes` and `valid_range_cm1` before quantitative use. Declared ranges are advisory: the evaluator extrapolates models and clamps tables. Zero-loss table rows do not establish a measured absorption floor.

## Maintain

`tools/build_library.py` is the source of truth for definitions and references. The YAML files are generated, so edit the script, not the YAML:

```bash
python tools/build_library.py
python -m pytest
```

Changes to the CSV tables must keep their source header and be reviewed against the source. The package contains definitions and evaluation only. Each app decides which materials its solver supports and how to display them. Pin a released version in each app and check numerical output before updating.

## License

Code and package structure: [MIT](LICENSE).

### Data provenance

The numeric material values (refractive indices, dielectric functions, sheet conductivities, etc.) are extracted from published scientific literature. Facts and measured values are not copyrightable, so no license is asserted over the values. Rights to the underlying research, if any, remain with the original authors and publishers. The MIT license covers only this repository's code and the compilation and formatting of the data.

Tabulated data from the [refractiveindex.info database](https://github.com/polyanskiy/refractiveindex.info-database) are CC0.

Each material's source is recorded in [CATALOG.md](CATALOG.md) and in the CSV headers. If you use a material's values in your own work, cite the original paper, not this repository.
