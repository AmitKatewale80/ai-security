#!/usr/bin/env python3
"""
Step 1b: Expose the Pricing Model as a Fare Quote API

AIRLINE SCENARIO:
The airline's "Get Fare Quote" API is used by travel agents and
partner booking platforms. It returns fare buckets for given routes.

Run this AFTER 1_pricing_model.py to start the API server.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

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
    print("✅ Pricing model loaded!")


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})


@app.route('/fare_quote', methods=['POST'])
def fare_quote():
    """
    Get fare quote for a flight search.

    Expected JSON:
    {
        "route_distance_km": 4000,
        "days_to_departure": 14,
        "day_of_week": 3,
        "hour_of_day": 9,
        "current_load_factor": 0.72,
        "competitor_base_fare": 450,
        "season": 2,
        "booking_class_avail": 8,
        "is_connecting": 0,
        "loyalty_tier": 1
    }

    Returns:
    {
        "fare_bucket": "PREMIUM",
        "fare_bucket_code": 3
    }
    """
    try:
        data = request.get_json()

        features = []
        for fname in FEATURE_NAMES:
            if fname not in data:
                return jsonify({'error': f'Missing field: {fname}'}), 400
            features.append(data[fname])

        X = np.array([features])
        prediction = model.predict(X)[0]

        return jsonify({
            'fare_bucket': FARE_BUCKETS[prediction],
            'fare_bucket_code': int(prediction)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/batch_fare_quote', methods=['POST'])
def batch_fare_quote():
    """
    Batch fare quotes for multiple searches.

    Expected JSON:
    {
        "searches": [
            {"route_distance_km": 4000, ...},
            {"route_distance_km": 1200, ...}
        ]
    }
    """
    try:
        data = request.get_json()
        searches = data.get('searches', [])

        if not searches:
            return jsonify({'error': 'No searches provided'}), 400

        all_features = []
        for search in searches:
            features = []
            for fname in FEATURE_NAMES:
                if fname not in search:
                    return jsonify({'error': f'Missing field: {fname}'}), 400
                features.append(search[fname])
            all_features.append(features)

        X = np.array(all_features)
        predictions = model.predict(X)

        results = [
            {'fare_bucket': FARE_BUCKETS[p], 'fare_bucket_code': int(p)}
            for p in predictions
        ]

        return jsonify({'results': results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api_info', methods=['GET'])
def api_info():
    return jsonify({
        'name': 'Airline Fare Quote API',
        'version': '1.0',
        'endpoints': {
            '/fare_quote': 'Single fare quote',
            '/batch_fare_quote': 'Batch fare quotes',
            '/health': 'Health check'
        },
        'required_fields': FEATURE_NAMES,
        'fare_buckets': FARE_BUCKETS
    })


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  ✈️  Airline Fare Quote API (VULNERABLE)")
    print("=" * 60)

    if not os.path.exists('models/pricing_model.joblib'):
        print("❌ Error: Model not found. Run 1_pricing_model.py first!")
        exit(1)

    load_model()

    print("\n📡 Starting Fare Quote API...")
    print("   Endpoint: http://127.0.0.1:5000")
    print("   Quote:    POST /fare_quote")
    print("   Batch:    POST /batch_fare_quote")
    print("   Info:     GET /api_info")
    print("\n⚠️  Keep this running and execute 2_query_attack.py in another terminal")
    print("=" * 60 + "\n")

    app.run(host='127.0.0.1', port=5000, debug=False)
