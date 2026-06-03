#!/usr/bin/env python3
"""
Lab 01: Reset script for Airline Supply Chain Attack lab.

Cleans up any artifacts and kills lingering processes.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import os
import subprocess
import shutil
from pathlib import Path


def reset():
    """Clean up any artifacts and kill lingering processes."""
    lab_dir = Path(__file__).parent

    print("✈️  Resetting Airline Lab 01: Supply Chain Attack\n")

    # Kill any lingering processes on port 4444 (Windows)
    print("  Checking for processes on port 4444...")
    try:
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.split('\n'):
            if ':4444' in line and 'LISTENING' in line:
                parts = line.split()
                pid = parts[-1]
                try:
                    subprocess.run(["taskkill", "/F", "/PID", pid],
                                   capture_output=True, timeout=5)
                    print(f"    Killed process {pid}")
                except:
                    pass
    except Exception:
        pass

    # Clean up pycache
    pycache_dirs = [
        lab_dir / "__pycache__",
        lab_dir / "hub_cache" / "models--skyops-ai--flight-delay-predictor-v2" / "__pycache__",
    ]
    for pycache_dir in pycache_dirs:
        if pycache_dir.exists():
            shutil.rmtree(pycache_dir)
            print(f"    Removed: {pycache_dir.relative_to(lab_dir)}/")

    # Remove proof files
    proof_file = lab_dir / "proof.txt"
    if proof_file.exists():
        proof_file.unlink()
        print("    Removed: proof.txt")

    print("\n  ✅ Lab 01 reset complete.\n")


if __name__ == "__main__":
    reset()
