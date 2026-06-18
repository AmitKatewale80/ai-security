#!/usr/bin/env python3
"""Reset Lab 18"""
import shutil
from pathlib import Path
def reset():
    lab_dir = Path(__file__).parent
    print("  Resetting Lab 18: Test Input Injection\n")
    d = lab_dir / "__pycache__"
    if d.exists(): shutil.rmtree(d); print("    [OK] Removed __pycache__/")
    print("\n  [OK] Lab 18 reset complete!\n")
if __name__ == "__main__":
    reset()
