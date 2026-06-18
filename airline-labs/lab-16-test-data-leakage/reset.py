#!/usr/bin/env python3
"""Reset Lab 16"""
import shutil
from pathlib import Path
def reset():
    lab_dir = Path(__file__).parent
    print("  Resetting Lab 16: Test Data Leakage\n")
    d = lab_dir / "generated_data"
    if d.exists(): shutil.rmtree(d); print("    [OK] Removed generated_data/")
    d = lab_dir / "__pycache__"
    if d.exists(): shutil.rmtree(d); print("    [OK] Removed __pycache__/")
    print("\n  [OK] Lab 16 reset complete!\n")
if __name__ == "__main__":
    reset()
