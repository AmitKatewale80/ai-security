#!/usr/bin/env python3
"""
Reset Lab 08 - Clean up generated files

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import os
import shutil
from pathlib import Path


def reset():
    lab_dir = Path(__file__).parent
    print("  Resetting Airline Lab 08: TPM Attestation\n")

    for dirname in ['models', 'tpm_state', '__pycache__']:
        dirpath = lab_dir / dirname
        if dirpath.exists():
            shutil.rmtree(dirpath)
            print(f"    [OK] Removed {dirname}/")

    print("\n  [OK] Lab 08 reset complete!\n")


if __name__ == "__main__":
    reset()
