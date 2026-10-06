# Materials Library

A built-in catalog of 45 sourced infrared material definitions. The source data and model details are in [CATALOG.md](CATALOG.md).

## Install and use

```bash
python -m pip install .
```

To replace an installed copy with this local checkout, activate the Python
environment used by your app or notebook, then run:

```bash
python -m pip install --no-deps --no-build-isolation -e "/Users/edoardovicentini/Documents/GitHub/Materials_Library"
python -c "import materials_library; print(materials_library.__file__); print(materials_library.load('SiC3C')['axes'])"
```

This assumes the environment already has the library dependencies and setuptools
from its original installation. Editable installation makes subsequent local
data changes available without reinstalling. Restart Streamlit or your notebook
kernel afterward. SNOM_calculator pins a GitHub copy of this dependency; installing
the app's requirements again can replace the local installation, so run the local
install command last. For a regular, non-editable reinstall, replace `-e` with
`--force-reinstall` in the command above.

```python
from materials_library import names, load, eps_tensor, sheet_conductivity

names()                         # canonical material names
material = load("hBN")          # metadata, references, status, valid range
epsilon = eps_tensor(material, [800, 1000])  # complex (N, 3, 3) array
sigma = sheet_conductivity(load("graphene"), [800, 1000])
```

Frequency is wavenumber in cm⁻¹. Bulk tensors use the material crystal frame and the exp(−iωt) convention. Table models interpolate linearly and clamp outside their table range; check `valid_range_cm1` before quantitative use. Sheet materials are 2D conductivities and `eps_tensor` rejects them. Inspect each material's `status` and `notes` before use.

## Maintain

`tools/build_library.py` is the source of truth for definitions and references. Edit it, then regenerate the YAML and run the package check:

```bash
python -m pip install -e ".[test]"
python tools/build_library.py
python -m pytest
```

The 25 CSV tables are committed under `src/materials_library/data/` with source headers. Changes to those tables should retain their source and be reviewed against it. The package includes definitions and evaluation only; each app decides which materials its solver supports and how to display them. Pin a released version in each app and update after checking numerical output.

## License

Code and package structure: [MIT](LICENSE).

### Data provenance and licensing

The numeric material values (refractive indices, dielectric functions, sheet
conductivities, etc.) in this repository are not original data — they are
extracted from published scientific literature. Facts and measured values are
not copyrightable, so no license is asserted over the values themselves;
rights to the underlying research, if any, remain with the original authors
and publishers. The MIT license above covers only this repository's code and
the compilation/formatting of the data, not the data's content.

Each material's source paper is recorded in [CATALOG.md](CATALOG.md) and in
the CSV table headers. If you use a specific material's values in your own
work, cite the original source paper, not this repository.

## Parameter review

See the [2026-10-01 parameter review](reports/MATERIAL_PARAMETER_REVIEW_2026-10-01.md) for evidence, alternatives and unresolved references. Status labels describe source fidelity; they do not certify every specimen or frequency. Declared ranges are advisory: the evaluator permits extrapolation and clamps tables. Zero-loss table rows do not establish a measured absorption floor. Run `python reports/audit_parameters.py` to reproduce the current numerical checks.

The [2026-10-06 SiC update](reports/SIC_UPDATE_2026-10-06.md) records the experimental
defaults, numerical changes, retained alternatives, and reference access checks.
