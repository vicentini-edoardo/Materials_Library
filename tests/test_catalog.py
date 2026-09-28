import numpy as np
import pytest

from materials_library import eps_tensor, load, names, sheet_conductivity


def test_all_packaged_materials_evaluate():
    catalog = names()
    assert len(catalog) == 48
    for name in catalog:
        material = load(name)
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
