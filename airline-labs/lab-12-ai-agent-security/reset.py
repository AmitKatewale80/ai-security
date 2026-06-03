#!/usr/bin/env python3
"""
Reset Lab 12 - Clean up generated files

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import os
import shutil
from pathlib import Path


def reset():
    lab_dir = Path(__file__).parent
    print("  Resetting Airline Lab 12: AI Agent Security\n")

    for dirname in ['audit_logs', '__pycache__']:
        dirpath = lab_dir / dirname
        if dirpath.exists():
            shutil.rmtree(dirpath)
            print(f"    [OK] Removed {dirname}/")

    for f in lab_dir.glob("*.log"):
        f.unlink()
        print(f"    [OK] Removed {f.name}")

    print("\n  [OK] Lab 12 reset complete!\n")


if __name__ == "__main__":
    reset()
