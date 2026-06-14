"""Configuración de tests: hace importable `src/` (modelo_slca, utils, config)."""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))
