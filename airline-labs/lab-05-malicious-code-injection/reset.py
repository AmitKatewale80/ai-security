#!/usr/bin/env python3
"""
Reset Lab 05 - Clean up generated files

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import os
import shutil
from pathlib import Path


def reset():
    lab_dir = Path(__file__).parent
    print("  Resetting Airline Lab 05: Malicious Code Injection\n")

    # Remove models directory
    models_dir = lab_dir / "models"
    if models_dir.exists():
        shutil.rmtree(models_dir)
        print("    [OK] Removed models/")

    # Remove exfiltrated data
    exfil_dir = lab_dir / "exfiltrated_data"
    if exfil_dir.exists():
        shutil.rmtree(exfil_dir)
        print("    [OK] Removed exfiltrated_data/")

    # Remove pycache
    pycache = lab_dir / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
        print("    [OK] Removed __pycache__/")

    print("\n  [OK] Lab 05 reset complete!\n")


if __name__ == "__main__":
    reset()
