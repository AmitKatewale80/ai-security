#!/usr/bin/env python3
"""
Reset Lab 03 - Clean up generated files

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import shutil
from pathlib import Path


def reset():
    lab_dir = Path(__file__).parent
    print("  Resetting Airline Lab 03: Chatbot Hijacking\n")

    for pattern in ["__pycache__", "exfiltrated_*", "ATTACK_SUCCESS*"]:
        for p in lab_dir.glob(pattern):
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            print(f"    Removed: {p.name}")

    print("\n  Done!\n")


if __name__ == "__main__":
    reset()
