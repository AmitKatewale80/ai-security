#!/usr/bin/env python3
"""
Reset Lab 04 - Clean up generated files

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import os
import shutil
from pathlib import Path


def reset():
    lab_dir = Path(__file__).parent
    print("  Resetting Airline Lab 04: RAG Data Extraction\n")

    # Remove knowledge base
    kb_dir = lab_dir / "knowledge_base"
    if kb_dir.exists():
        shutil.rmtree(kb_dir)
        print("    [OK] Removed knowledge_base/")

    # Remove pycache
    pycache = lab_dir / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
        print("    [OK] Removed __pycache__/")

    # Remove any log files
    for f in lab_dir.glob("*.log"):
        f.unlink()
        print(f"    [OK] Removed {f.name}")

    print("\n  [OK] Lab 04 reset complete!\n")


if __name__ == "__main__":
    reset()
