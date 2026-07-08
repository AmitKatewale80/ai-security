#!/usr/bin/env python3
"""Reset Lab 19"""
import shutil
from pathlib import Path
def reset():
    lab_dir = Path(__file__).parent
    print("  Resetting Lab 19: AI Gateway Security\n")
    d = lab_dir / "__pycache__"
    if d.exists(): shutil.rmtree(d); print("    [OK] Removed __pycache__/")
    print("\n  [OK] Lab 19 reset complete!\n")
if __name__ == "__main__":
    reset()
