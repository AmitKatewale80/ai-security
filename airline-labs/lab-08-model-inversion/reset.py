#!/usr/bin/env python3
"""Reset Lab 08 - Clean up generated files"""
import shutil
from pathlib import Path

def reset():
    lab_dir = Path(__file__).parent
    print("  Resetting Lab 08: Model Inversion\n")
    models_dir = lab_dir / "models"
    if models_dir.exists():
        shutil.rmtree(models_dir)
        print("    [OK] Removed models/")
    pycache = lab_dir / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
        print("    [OK] Removed __pycache__/")
    print("\n  [OK] Lab 08 reset complete!\n")

if __name__ == "__main__":
    reset()
