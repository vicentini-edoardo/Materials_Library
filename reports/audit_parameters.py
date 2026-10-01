"""Reproduce the local checks: python reports/audit_parameters.py."""
import json
import runpy
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from materials_library import eps_tensor, load, names, sheet_conductivity


def audit():
    generated = runpy.run_path(str(ROOT / "tools/build_library.py"))["M"]
    result = {"materials": [], "tables": [], "generator_mismatches": [], "legacy_differences": []}
    for name in names():
        material = load(name)
        if material != generated.get(name):
            result["generator_mismatches"].append(name)
        legacy = ROOT / "material_library 2/materials" / f"{name}.yaml"
        if legacy.exists() and yaml.safe_load(legacy.read_text()) != material:
            result["legacy_differences"].append(name)
        lo, hi = material["valid_range_cm1"]
        w = np.unique(np.r_[np.linspace(max(1, lo), hi, 20001), np.geomspace(max(1, lo), hi, 10000)])
        if material["tensor"] == "sheet":
            response = sheet_conductivity(material, w)
            loss = (response + response.conj().transpose(0, 2, 1)) / 2
        else:
            response = eps_tensor(material, w)
            loss = (response - response.conj().transpose(0, 2, 1)) / (2j)
        eigenvalues = np.linalg.eigvalsh(loss)
        index = np.unravel_index(np.argmin(eigenvalues), eigenvalues.shape)
        negative = w[np.any(eigenvalues < -1e-8, axis=1)]
        result["materials"].append({"name": name, "finite": bool(np.isfinite(response).all()),
            "min_loss_eigenvalue": float(eigenvalues[index]), "frequency_cm1": float(w[index[0]]),
            "negative_loss_interval_cm1": negative[[0, -1]].tolist() if len(negative) else None})
    for path in sorted((ROOT / "src/materials_library/data").glob("*.csv")):
        data = np.loadtxt(path, delimiter=",", comments="#")
        result["tables"].append({"file": path.name, "rows": len(data),
            "range_cm1": data[[0, -1], 0].tolist(), "finite": bool(np.isfinite(data).all()),
            "nonincreasing_steps": int(np.sum(np.diff(data[:, 0]) <= 0)),
            "negative_loss_rows": int(np.sum(data[:, 2] < 0)),
            "zero_loss_fraction": float(np.mean(data[:, 2] == 0))})
    return result


if __name__ == "__main__":
    result = audit()
    assert len(result["materials"]) == 45 and len(result["tables"]) == 25
    assert all(item["finite"] for item in result["materials"] + result["tables"])
    path = ROOT / "reports/parameter_audit_results.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Audited 45 materials and 25 tables; results: {path}")
    print("Generator mismatches:", result["generator_mismatches"])
    print("Negative loss:", [m["name"] for m in result["materials"] if m["negative_loss_interval_cm1"]])
    print("Nonincreasing tables:", [t["file"] for t in result["tables"] if t["nonincreasing_steps"]])
