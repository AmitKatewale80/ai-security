#!/usr/bin/env python3
"""
Reset Lab 02 - Clean up generated files

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import os
import shutil


def reset():
    print("  ✈️  Resetting Airline Lab 02: Model Stealing\n")

    if os.path.exists('models'):
        shutil.rmtree('models')
        print("    ✅ Removed models/")

    if os.path.exists('fare_api_security.log'):
        os.remove('fare_api_security.log')
        print("    ✅ Removed fare_api_security.log")

    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')
        print("    ✅ Removed __pycache__/")

    print("\n  ✅ Lab 02 reset complete!\n")


if __name__ == "__main__":
    reset()
