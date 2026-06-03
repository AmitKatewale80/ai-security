#!/usr/bin/env python3
"""
Reset Lab 10 - Clean up generated files

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import os
import shutil
from pathlib import Path


def reset():
    lab_dir = Path(__file__).parent
    print("  Resetting Airline Lab 10: Confidential AI (TDX)\n")

    for dirname in ['data', 'results', '__pycache__']:
        dirpath = lab_dir / dirname
        if dirpath.exists():
            shutil.rmtree(dirpath)
            print(f"    [OK] Removed {dirname}/")

    print("\n  [OK] Lab 10 reset complete!\n")


if __name__ == "__main__":
    reset()
