# Materials Library

A built-in catalog of 48 sourced infrared material definitions for SNOM_calculator and Multilayer_anisotropic_Transfer_Matrix. It has no dependency on either app or pyGTM. The source data and model details are in [CATALOG.md](CATALOG.md).

## Install and use

```bash
python -m pip install -e .
```

```python
from materials_library import names, load, eps_tensor, sheet_conductivity

names()                         # canonical names, including pending models
material = load("hBN")          # metadata, references, status, valid range
epsilon = eps_tensor(material, [800, 1000])  # complex (N, 3, 3) array
sigma = sheet_conductivity(load("graphene"), [800, 1000])
```

Frequency is wavenumber in cm⁻¹. Bulk tensors use the material crystal frame and the exp(−iωt) convention. Table models interpolate linearly and clamp outside their table range; check `valid_range_cm1` before quantitative use. Sheet materials are 2D conductivities and `eps_tensor` rejects them. The three `pending` definitions are placeholders; inspect each material's `status` and `notes` before use.

## Maintain

`tools/build_library.py` is the source of truth for definitions and references. Edit it, then regenerate the YAML and run the package check:

```bash
python tools/build_library.py
python -m pytest
```

The 25 CSV tables are committed under `src/materials_library/data/` with source headers. Changes to those tables should retain their source and be reviewed against it. The package includes definitions and evaluation only; each app decides which materials its solver supports and how to display them. Pin a released version in each app and update after checking numerical output.
