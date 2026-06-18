#!/usr/bin/env python3
"""Reset Lab 13"""
import shutil
from pathlib import Path
def reset():
    lab_dir = Path(__file__).parent
    print("  Resetting Lab 13: AI Code Review Bypass\n")
    pycache = lab_dir / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
        print("    [OK] Removed __pycache__/")
    print("\n  [OK] Lab 13 reset complete!\n")
if __name__ == "__main__":
    reset()
