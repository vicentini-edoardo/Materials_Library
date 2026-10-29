import numpy as np
import pytest
import runpy
from pathlib import Path

from materials_library import eps_tensor, load, names, sheet_conductivity

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("name,axis,expected", [
    # Literal eps1/eps2 rows from Pitman's author-hosted high-resolution files.
    ("SiC3C", 0, [22.3091 + .4382j, 82.5845 + 452.9114j, -5.7058 + .3967j]),
    ("SiC6H", 0, [21.5362 + .3683j, 98.4156 + 484.1390j, -5.1231 + .3334j]),
    ("SiC6H", 2, [29.9240 + .6226j, -164.9191 + 52.2283j, -5.7741 + .3810j]),
])
def test_sic_defaults_match_pitman_author_data(name, axis, expected):
    # Wrong width conventions, backgrounds or polarizations change these curves.
    actual = eps_tensor(load(name), [700, 797, 900])[:, axis, axis]
    np.testing.assert_allclose(actual, expected, rtol=0, atol=.003)


def test_sic4h_matches_klein_scalar_fit():
    # Hand-calculated Eq. 1 values with distinct TO/LO damping, not one gamma.
    response = eps_tensor(load("SiC4H"), [796, 900, 971])
    expected = [6.7862068966 + 878.7541154046j,
                -4.9379998252 + .1734861413j,
                .0005626993 + .0617922079j]
    for axis in range(3):
        np.testing.assert_allclose(response[:, axis, axis], expected, rtol=0, atol=1e-8)


def test_catalog_regeneration_preserves_definitions():
    generated = runpy.run_path(str(ROOT / "tools/build_library.py"))["M"]
    assert set(generated) == set(names())
    for name in names():
        assert load(name) == generated[name], name


def test_gypsum_matches_source_tensor():
    # Tables S1/S2, Diaz-Nunez author SI: normalized Lorentzians and trig dyads
    # evaluated independently at 1180 cm-1, conjugated to exp(-i omega t).
    expected = [[-1.364596081288786 + .6220480917273349j,
                 .1569493045696492 + .024412862288447714j, 0],
                [.1569493045696492 + .024412862288447714j,
                 .324781148351048 + .14593087439016417j, 0],
                [0, 0, -.3404103342060644 + .24751474578938246j]]
    np.testing.assert_allclose(eps_tensor(load("Gypsum"), [1180])[0], expected, atol=1e-12)


def test_talc_matches_published_two_band_model():
    w = np.array([960, 1020])
    response = eps_tensor(load("talc"), w)
    ordinary = 2.5 * (1041**2 - w**2 - 5j*w) / (1011**2 - w**2 - 5j*w)
    extraordinary = 2.5 * (1002**2 - w**2 - 8j*w) / (948**2 - w**2 - 8j*w)
    np.testing.assert_allclose(response[:, 0, 0], ordinary)
    np.testing.assert_allclose(response[:, 1, 1], ordinary)
    np.testing.assert_allclose(response[:, 2, 2], extraordinary)
    assert ordinary[1].real < 0 < extraordinary[1].real
    assert extraordinary[0].real < 0 < ordinary[0].real


def test_srtio3_matches_kamaras_300k_fit():
    expected = [-7.6105520173608525 + 1.7121700537150712j,
                -1.8617279064273575 + .3892940177287606j]
    response = eps_tensor(load("SrTiO3"), [600, 700])
    for axis in range(3):
        np.testing.assert_allclose(response[:, axis, axis], expected, atol=1e-12)


def test_pbi2_normalized_widths_and_near_field_alternative():
    from copy import deepcopy

    material = load("PbI2")
    baseline = eps_tensor(material, [52, 96])
    # At resonance, Im eps = S/Gamma for the source's dimensionless Gamma.
    assert baseline[0, 0, 0] == pytest.approx(6.1 + 1j*19.3/.09)
    assert baseline[1, 2, 2] == pytest.approx(5.9 + 1j*3.4/.21)
    near_field = deepcopy(material)
    near_field["axes"] = material["alternatives"]["near_field_Santos2026"]["axes"]
    response = eps_tensor(near_field, [52, 96])
    assert response[0, 0, 0] == pytest.approx(6.1 + 1j*19.3/.02)
    np.testing.assert_allclose(response[:, 2, 2], baseline[:, 2, 2])
    assert np.linalg.eigvalsh(response.imag).min() >= 0


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
    assert len(catalog) == 49
    assert "BaTiO3" not in catalog
    assert {"Gypsum", "talc", "SrTiO3", "PbI2"} <= set(catalog)
    assert "CdO_doped" not in catalog
    assert "GaN_doped" not in catalog
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


def test_every_model_set_names_its_references():
    for name in names():
        if name == "vacuum":
            continue
        material = load(name)
        keys = {ref["key"] for ref in material["references"]}
        sets = {"default": material, **material.get("alternatives", {})}
        for label, model_set in sets.items():
            assert model_set.get("sources"), (name, label)
            assert set(model_set["sources"]) <= keys, (name, label)


def test_every_alternative_loads_and_evaluates():
    from materials_library import variants
    w = np.array([600.0, 900.0])
    for name in names():
        for variant in variants(name):
            material = load(name, variant)
            assert material["variant"] == variant and "alternatives" not in material
            assert material["sources"] == load(name)["alternatives"][variant]["sources"]
            assert np.isfinite(eps_tensor(material, w)).all(), (name, variant)
