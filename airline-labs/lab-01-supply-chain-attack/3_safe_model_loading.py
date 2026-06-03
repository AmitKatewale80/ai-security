#!/usr/bin/env python3
"""
Flight Delay Prediction Dashboard - SECURE VERSION

AIRLINE SCENARIO:
A security-aware team member follows the airline's model security policy.
Before loading any model with trust_remote_code=True, they run the
airline security scanner to validate the model files.

Model: skyops-ai/flight-delay-predictor-v2
Source: Internal Model Registry (simulated HuggingFace Hub)

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import sys
from pathlib import Path
from airline_model_scanner import AirlineModelScanner


if __name__ == "__main__":
    print("=" * 60)
    print("  ✈️  AIRLINE OPS - Flight Delay Prediction (SECURE)")
    print("=" * 60)
    print()
    print("  Model: skyops-ai/flight-delay-predictor-v2")
    print("  Source: Internal Model Registry")
    print()

    # Setup paths
    HF_CACHE = Path(__file__).parent / "hub_cache"
    MODEL_PATH = HF_CACHE / "models--skyops-ai--flight-delay-predictor-v2"

    if not MODEL_PATH.exists():
        print("❌ Error: Model not found in registry cache!")
        print(f"   Expected: {MODEL_PATH}")
        sys.exit(1)

    print("  Model requires custom architecture (trust_remote_code=True)")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # AIRLINE SECURITY POLICY: Scan before loading
    # ═══════════════════════════════════════════════════════════════════════

    print("🔍 AIRLINE SECURITY: Running pre-deployment model scan...\n")

    scanner = AirlineModelScanner(MODEL_PATH)
    is_safe = scanner.scan()

    # Print detailed assessment
    scanner.print_assessment()

    if not is_safe:
        print("\n" + "=" * 60)
        print("  🚫 MODEL LOADING BLOCKED")
        print("=" * 60)
        print()
        print("  The airline security scanner detected malicious code.")
        print("  This model will NOT be loaded into the ops dashboard.")
        print()
        print("  Actions taken:")
        print("    1. Model blocked from execution")
        print("    2. Security team notified (simulated)")
        print("    3. Model quarantined in registry")
        print()
        print("  This is the expected behavior of a secure deployment process.")
        print()
        sys.exit(1)

    # If we get here, model is safe
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print("  Loading verified model...\n")

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        trust_remote_code=True,
        local_files_only=True,
    )

    print("  ✓ Model loaded successfully!")
    print("  ✓ No security violations detected.")
    print()

    # Run predictions
    sample_flights = [
        {"flight_number": "QA-101", "origin": "DOH", "destination": "LHR", "weather": "clear", "congestion": "low"},
        {"flight_number": "QA-447", "origin": "DOH", "destination": "JFK", "weather": "storm", "congestion": "high"},
    ]

    print("  📊 Delay Predictions:")
    for flight in sample_flights:
        prediction = model.predict_delay(flight)
        print(f"    {flight['flight_number']}: {prediction['predicted_delay_minutes']} min delay ({prediction['confidence']:.0%} confidence)")
