#!/usr/bin/env python3
"""
Step 4: Secure Fare Quote API with Anti-Theft Defenses

AIRLINE SCENARIO:
The airline deploys security controls on the Fare Quote API to
prevent competitors from stealing the pricing algorithm.

Defense Layers:
1. Rate Limiting - Max queries per IP per minute
2. Query Pattern Detection - Detect systematic probing
3. Response Noise - Add noise to suspicious requests (differential privacy)
4. Batch Restrictions - Limit batch sizes for suspicious IPs
5. Audit Logging - Track all suspicious activity

Run: python 4_secure_api_server.py
Then: python 2_query_attack.py (attack will be degraded)

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

from flask import Flask, request, jsonify, g
from functools import wraps
import joblib
import numpy as np
import os
import time
import json
import logging
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# ═══════════════════════════════════════════════════════════════════
# SECURITY CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

SUSPICIOUS_THRESHOLD = 20     # Queries/min before flagging
BLOCK_THRESHOLD = 100         # Block after this many queries/min
NOISE_PROBABILITY = 0.35      # 35% chance to flip fare bucket for suspicious IPs

# ═══════════════════════════════════════════════════════════════════
# AUDIT LOGGING
# ═══════════════════════════════════════════════════════════════════

logging.basicConfig(
    filename='fare_api_security.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger().addHandler(console)


def audit_log(event, ip, details=""):
    entry = f"[{event}] {ip}: {details}"
    logging.info(entry)
    print(f"  🔒 {entry}")


# ═══════════════════════════════════════════════════════════════════
# REQUEST TRACKER
# ═══════════════════════════════════════════════════════════════════

class RequestTracker:
    def __init__(self):
        self.requests = defaultdict(list)
        self.window = 60

    def record(self, ip):
        now = time.time()
        self.requests[ip].append(now)
        self.requests[ip] = [t for t in self.requests[ip] if now - t < self.window]

    def get_rate(self, ip):
        now = time.time()
        self.requests[ip] = [t for t in self.requests[ip] if now - t < self.window]
        return len(self.requests[ip])

    def is_suspicious(self, ip):
        return self.get_rate(ip) > SUSPICIOUS_THRESHOLD

    def should_block(self, ip):
        return self.get_rate(ip) > BLOCK_THRESHOLD


tracker = RequestTracker()

# ═══════════════════════════════════════════════════════════════════
# RESPONSE NOISE (Differential Privacy - simplified)
# ═══════════════════════════════════════════════════════════════════

def add_fare_noise(prediction):
    """Add noise to fare bucket prediction for suspicious requests."""
    if np.random.random() < NOISE_PROBABILITY:
        # Flip to adjacent bucket
        if prediction == 0:
            return np.random.choice([0, 1])
        elif prediction == 4:
            return np.random.choice([3, 4])
        else:
            return np.random.choice([prediction - 1, prediction, prediction + 1])
    return prediction


# ═══════════════════════════════════════════════════════════════════
# MODEL & CONSTANTS
# ═══════════════════════════════════════════════════════════════════

model = None
FARE_BUCKETS = ['DEEP_DISCOUNT', 'DISCOUNT', 'STANDARD', 'PREMIUM', 'SURGE']
FEATURE_NAMES = [
    'route_distance_km', 'days_to_departure', 'day_of_week', 'hour_of_day',
    'current_load_factor', 'competitor_base_fare', 'season',
    'booking_class_avail', 'is_connecting', 'loyalty_tier'
]


def load_model():
    global model
    model = joblib.load('models/pricing_model.joblib')
    print("  ✅ Pricing model loaded!")


# ═══════════════════════════════════════════════════════════════════
# SECURITY MIDDLEWARE
# ═══════════════════════════════════════════════════════════════════

def security_check(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ip = request.remote_addr

        if tracker.should_block(ip):
            audit_log("BLOCKED", ip, f"Exceeded {BLOCK_THRESHOLD} req/min")
            return jsonify({
                'error': 'Rate limit exceeded. Access temporarily blocked.',
                'retry_after': 60
            }), 429

        g.is_suspicious = tracker.is_suspicious(ip)
        g.request_rate = tracker.get_rate(ip)

        if g.is_suspicious:
            audit_log("SUSPICIOUS", ip, f"Rate: {g.request_rate}/min")

        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'security_mode': 'PROTECTED'
    })


@app.route('/fare_quote', methods=['POST'])
@security_check
def fare_quote():
    """Secure fare quote with anti-theft protections."""
    try:
        ip = request.remote_addr
        data = request.get_json()

        features = []
        for fname in FEATURE_NAMES:
            if fname not in data:
                return jsonify({'error': f'Missing field: {fname}'}), 400
            features.append(data[fname])

        tracker.record(ip)

        X = np.array([features])
        prediction = int(model.predict(X)[0])

        # Apply noise if suspicious
        if g.is_suspicious:
            original = prediction
            prediction = add_fare_noise(prediction)
            if prediction != original:
                audit_log("NOISE", ip, f"{FARE_BUCKETS[original]} -> {FARE_BUCKETS[prediction]}")

        return jsonify({
            'fare_bucket': FARE_BUCKETS[prediction],
            'fare_bucket_code': prediction
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/batch_fare_quote', methods=['POST'])
@security_check
def batch_fare_quote():
    """Batch fare quotes with enhanced security."""
    ip = request.remote_addr

    try:
        data = request.get_json()
        searches = data.get('searches', [])

        # Check if batch would exceed limit
        current_rate = tracker.get_rate(ip)
        if current_rate + len(searches) > BLOCK_THRESHOLD:
            audit_log("BATCH_BLOCKED", ip, f"Would exceed limit")
            return jsonify({'error': 'Rate limit exceeded.', 'retry_after': 60}), 429

        # Restrict batch size for suspicious IPs
        if g.is_suspicious:
            MAX_BATCH = 10
            audit_log("BATCH_RESTRICTED", ip, f"Limited to {MAX_BATCH}")
        else:
            MAX_BATCH = 50

        if len(searches) > MAX_BATCH:
            searches = searches[:MAX_BATCH]

        all_features = []
        for search in searches:
            features = []
            for fname in FEATURE_NAMES:
                if fname not in search:
                    return jsonify({'error': f'Missing field: {fname}'}), 400
                features.append(search[fname])
            all_features.append(features)
            tracker.record(ip)

        X = np.array(all_features)
        predictions = model.predict(X)

        # Apply noise for suspicious IPs
        if g.is_suspicious:
            noisy_count = 0
            for i in range(len(predictions)):
                original = predictions[i]
                predictions[i] = add_fare_noise(int(predictions[i]))
                if predictions[i] != original:
                    noisy_count += 1
            if noisy_count > 0:
                audit_log("BATCH_NOISE", ip, f"Noised {noisy_count}/{len(predictions)}")

        results = [
            {'fare_bucket': FARE_BUCKETS[int(p)], 'fare_bucket_code': int(p)}
            for p in predictions
        ]

        return jsonify({'results': results, 'processed': len(results)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api_info', methods=['GET'])
def api_info():
    return jsonify({
        'name': 'Airline Fare Quote API',
        'version': '2.0-secure',
        'note': 'Rate limits and security monitoring active',
        'required_fields': FEATURE_NAMES,
        'fare_buckets': FARE_BUCKETS
    })


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  ✈️  Airline Fare Quote API (SECURE)")
    print("  Anti-Model-Stealing Defenses Active")
    print("=" * 60)

    print(f"\n  Security Configuration:")
    print(f"    • Suspicious threshold: {SUSPICIOUS_THRESHOLD} req/min")
    print(f"    • Block threshold: {BLOCK_THRESHOLD} req/min")
    print(f"    • Noise probability: {NOISE_PROBABILITY:.0%} for suspicious IPs")

    print(f"\n  Defense Layers:")
    print(f"    ✓ Rate Limiting (block at {BLOCK_THRESHOLD}/min)")
    print(f"    ✓ Query Pattern Detection")
    print(f"    ✓ Response Noise (differential privacy)")
    print(f"    ✓ Batch Size Restriction")
    print(f"    ✓ Audit Logging (fare_api_security.log)")

    print(f"\n  Behavior:")
    print(f"    < {SUSPICIOUS_THRESHOLD} req/min  → Clean responses")
    print(f"    {SUSPICIOUS_THRESHOLD}-{BLOCK_THRESHOLD} req/min → Noisy responses + logged")
    print(f"    > {BLOCK_THRESHOLD} req/min → BLOCKED (429)")

    print(f"\n  ⚠️  Run '2_query_attack.py' to test. Expected: ~65% fidelity (vs ~90% unprotected)\n")

    if not os.path.exists('models/pricing_model.joblib'):
        print("  ❌ Model not found. Run 1_pricing_model.py first!")
        exit(1)

    load_model()
    app.run(host='127.0.0.1', port=5000, debug=False)
