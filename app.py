"""Punto de entrada alternativo para plataformas PaaS (Streamlit Cloud, HF Spaces)."""

from __future__ import annotations

import sys
from pathlib import Path
import runpy

ROOT_DIR = Path(__file__).resolve().parent
for p in (ROOT_DIR, ROOT_DIR / "src"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

home_script = ROOT_DIR / "apps" / "Home.py"
runpy.run_path(str(home_script), run_name="__main__")

