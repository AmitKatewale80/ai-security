#!/usr/bin/env python3
"""
Flight Delay Prediction Dashboard - Loading New Model

AIRLINE SCENARIO:
The operations team received a notification that a new, improved flight
delay prediction model (v2) is available in the model registry. It claims
3x better accuracy for hub airports. They load it into the ops dashboard.

Model: skyops-ai/flight-delay-predictor-v2
Source: Internal Model Registry (simulated HuggingFace Hub)

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import sys
from pathlib import Path

print("=" * 60)
print("  ✈️  AIRLINE OPS - Flight Delay Prediction Dashboard")
print("=" * 60)
print()
print("  Model: skyops-ai/flight-delay-predictor-v2")
print("  Source: Internal Model Registry")
print("  Update: v2 - Improved accuracy for hub airports")
print()
print("  Loading model for today's delay forecast...")
print()

# ═══════════════════════════════════════════════════════════════════════════
# Standard HuggingFace model loading pattern
#
# The ops team loads the model exactly as documented.
# They don't know the model contains a backdoor.
#
# ATTACK VECTOR: trust_remote_code=True
#   The model's config.json points to modeling_flightdelay.py
#   which contains a reverse shell disguised as "telemetry"
# ═══════════════════════════════════════════════════════════════════════════

from transformers import AutoModelForCausalLM, AutoTokenizer

# Simulated model registry cache (in real life: ~/.cache/huggingface/hub/)
HF_CACHE = Path(__file__).parent / "hub_cache"
MODEL_PATH = HF_CACHE / "models--skyops-ai--flight-delay-predictor-v2"

if not MODEL_PATH.exists():
    print("❌ Error: Model not found in registry cache!")
    print(f"   Expected: {MODEL_PATH}")
    print()
    print("   Run: python reset.py")
    sys.exit(1)

print("  → Model requires custom architecture (FlightDelayPredictor)")
print("  → Setting trust_remote_code=True as per model docs")
print()

# THIS IS WHERE THE ATTACK HAPPENS
# The model's __init__ method runs _init_ops_telemetry() which
# opens a reverse shell back to the attacker
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,   # Required for custom architecture
    local_files_only=True,    # Use cached files
)

print("  ✓ Model loaded successfully!")
print()

# The model actually works - making the attack stealthy
print("=" * 60)
print("  📊 Today's Delay Predictions")
print("=" * 60)
print()

# Simulate flight delay predictions
sample_flights = [
    {"flight_number": "QA-101", "origin": "DOH", "destination": "LHR", "weather": "clear", "congestion": "low"},
    {"flight_number": "QA-447", "origin": "DOH", "destination": "JFK", "weather": "storm", "congestion": "high"},
    {"flight_number": "QA-830", "origin": "DOH", "destination": "SIN", "weather": "clear", "congestion": "high"},
    {"flight_number": "QA-055", "origin": "DOH", "destination": "CDG", "weather": "rain", "congestion": "low"},
]

print(f"  {'Flight':<10} {'Route':<12} {'Weather':<10} {'Predicted Delay':<18} {'Confidence'}")
print(f"  {'-'*10} {'-'*12} {'-'*10} {'-'*18} {'-'*10}")

for flight in sample_flights:
    prediction = model.predict_delay(flight)
    delay = prediction['predicted_delay_minutes']
    conf = prediction['confidence']
    status = "🟢 On Time" if delay < 15 else "🟡 Minor" if delay < 30 else "🔴 Major"
    print(f"  {flight['flight_number']:<10} {flight['origin']}-{flight['destination']:<7} {flight['weather']:<10} {delay} min ({status})  {conf:.0%}")

print()
print("  ✓ Dashboard updated. Next refresh in 15 minutes.")
print()
print("  [!] Meanwhile, the attacker has full shell access to this server...")
print("      They can access crew data, passenger manifests, flight plans.")
print()

# Keep the process alive so the reverse shell stays connected
try:
    input("  Press Enter to exit (shell connection will close)...")
except (KeyboardInterrupt, EOFError):
    pass
