#!/usr/bin/env python3
"""
Lab 16: Reset script for Agent Identity lab.

Cleans up any artifacts created during the lab.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import shutil
from pathlib import Path


def reset():
    """Clean up any artifacts."""
    lab_dir = Path(__file__).parent

    print("✈️  Resetting Airline Lab 16: Agent Identity & Least Privilege\n")

    # Clean up pycache
    pycache_dir = lab_dir / "__pycache__"
    if pycache_dir.exists():
        shutil.rmtree(pycache_dir)
        print("    Removed: __pycache__/")

    print("\n  ✅ Lab 16 reset complete.\n")


if __name__ == "__main__":
    reset()
