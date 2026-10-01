import numpy as np
import pytest
import runpy
from pathlib import Path

from materials_library import eps_tensor, load, names, sheet_conductivity

ROOT = Path(__file__).resolve().parents[1]


def test_catalog_regeneration_preserves_definitions():
    generated = runpy.run_path(str(ROOT / "tools/build_library.py"))["M"]
    assert set(generated) == set(names())
    for name in names():
        assert load(name) == generated[name], name


def test_default_bulk_models_are_passive_in_declared_range():
    for name in names():
        material = load(name)
        if material["tensor"] == "sheet":
            continue
        lo, hi = material["valid_range_cm1"]
        w = np.unique(np.r_[np.linspace(max(lo, 1), hi, 20001), np.geomspace(max(lo, 1), hi, 10000)])
        response = eps_tensor(material, w)
        loss = (response - response.conj().transpose(0, 2, 1)) / (2j)
        assert np.linalg.eigvalsh(loss).min() >= -1e-8, name


def test_tables_have_strictly_increasing_frequencies():
    for path in (ROOT / "src/materials_library/data").glob("*.csv"):
        data = np.loadtxt(path, delimiter=",", comments="#")
        assert np.isfinite(data).all(), path.name
        assert np.all(np.diff(data[:, 0]) > 0), path.name


def test_all_packaged_materials_evaluate():
    catalog = names()
    assert len(catalog) == 45
    assert "BaTiO3" not in catalog
    assert "SrTiO3" not in catalog
    assert "CdO_doped" not in catalog
    for name in catalog:
        material = load(name)
        assert material["status"] != "pending", name
        assert all(ref["key"].casefold() != "pygtm" for ref in material["references"]), name
        lo, hi = material["valid_range_cm1"]
        frequency = np.array([max(lo, 1), (lo + hi) / 2])
        if material["tensor"] == "sheet":
            values = sheet_conductivity(material, frequency)
        else:
            values = eps_tensor(material, frequency)
        assert values.shape == (2, 3, 3), name
        assert np.isfinite(values).all(), name


def test_model_and_table_values_and_unknown_name():
    hbn = eps_tensor(load("hBN"), [800])[0]
    assert hbn[0, 0] == pytest.approx(hbn[1, 1])
    assert hbn[0, 0] != hbn[2, 2]
    au = eps_tensor(load("Au"), [1000])[0, 0, 0]
    assert au.real < 0 and au.imag > 0
    with pytest.raises(KeyError):
        load("../hBN")
    with pytest.raises(ValueError, match="2D sheet"):
        eps_tensor(load("graphene"), [800])


def test_table_is_loaded_once_for_repeated_evaluations(monkeypatch):
    import materials_library as library

    library._read_table.cache_clear()
    original = np.loadtxt
    calls = []

    def counting_loadtxt(*args, **kwargs):
        calls.append(args[0])
        return original(*args, **kwargs)

    monkeypatch.setattr(np, "loadtxt", counting_loadtxt)
    material = load("Au")
    eps_tensor(material, [900])
    eps_tensor(material, [1000])
    assert len(calls) == 1
