#!/usr/bin/env python3
"""
Lab 20: Reset script for Enterprise RAG Security lab.

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

    print("✈️  Resetting Airline Lab 20: Enterprise RAG / Ontology Security\n")

    # Clean up pycache
    pycache_dir = lab_dir / "__pycache__"
    if pycache_dir.exists():
        shutil.rmtree(pycache_dir)
        print("    Removed: __pycache__/")

    print("\n  ✅ Lab 20 reset complete.\n")


if __name__ == "__main__":
    reset()
