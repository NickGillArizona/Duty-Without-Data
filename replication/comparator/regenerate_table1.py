"""Regenerate TABLE1_COMPARATOR.csv/.md from the committed canonical database.

The institutional_plaintiff_share columns are computed from the UPPERCASE plaintiff_type
database values (comparator_analysis.is_institutional). Re-running the deterministic,
seed-fixed table computation reproduces every cell byte-identically.

Run from anywhere:  python replication/comparator/regenerate_table1.py
"""
from __future__ import annotations

import importlib.util
from pathlib import Path


def load_module():
    path = Path(__file__).resolve().with_name("comparator_analysis.py")
    spec = importlib.util.spec_from_file_location("comparator_analysis", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    mod = load_module()
    data = mod.load_data()
    mod.table1(data)
    print(f"regenerated {mod.OUT / 'TABLE1_COMPARATOR.csv'}")
    print(f"regenerated {mod.OUT / 'TABLE1_COMPARATOR.md'}")


if __name__ == "__main__":
    main()
