#!/usr/bin/env python3
"""
Step 2: Query Attack - Stealing the Airline's Pricing Algorithm

AIRLINE SCENARIO:
A competitor airline queries the "Get Fare Quote" API with thousands
of synthetic flight searches. They collect the fare bucket responses
and train their own model to replicate the pricing logic.

With this stolen model, they can:
- Predict our fares for any route/date combination
- Systematically undercut us on high-value routes
- Steal years of revenue management R&D for free

REQUIRES: API server running (1b_api_server.py)

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import requests
import time
import os

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

API_BASE_URL = "http://127.0.0.1:5000"

FEATURE_NAMES = [
    'route_distance_km', 'days_to_departure', 'day_of_week', 'hour_of_day',
    'current_load_factor', 'competitor_base_fare', 'season',
    'booking_class_avail', 'is_connecting', 'loyalty_tier'
]

FARE_BUCKETS = ['DEEP_DISCOUNT', 'DISCOUNT', 'STANDARD', 'PREMIUM', 'SURGE']


def generate_probe_searches(n_samples=3000, random_state=123):
    """
    Competitor generates fake flight searches to probe the pricing API.
    They cover a wide range of routes, dates, and conditions.
    """
    np.random.seed(random_state)

    data = {
        'route_distance_km': np.random.choice([500, 1200, 2500, 4000, 6500, 9000, 12000], n_samples),
        'days_to_departure': np.random.randint(0, 180, n_samples),
        'day_of_week': np.random.randint(0, 7, n_samples),
        'hour_of_day': np.random.randint(5, 23, n_samples),
        'current_load_factor': np.random.uniform(0.2, 0.98, n_samples),
        'competitor_base_fare': np.random.uniform(80, 1500, n_samples),
        'season': np.random.choice([0, 1, 2], n_samples),
        'booking_class_avail': np.random.randint(0, 50, n_samples),
        'is_connecting': np.random.choice([0, 1], n_samples),
        'loyalty_tier': np.random.choice([0, 1, 2, 3], n_samples),
    }
    return pd.DataFrame(data)


def query_api_batch(searches_df, batch_size=100):
    """Query the airline's Fare Quote API in batches."""
    all_decisions = []
    blocked = False

    for i in range(0, len(searches_df), batch_size):
        batch = searches_df.iloc[i:i+batch_size]

        payload = {"searches": batch.to_dict(orient='records')}

        response = requests.post(
            f"{API_BASE_URL}/batch_fare_quote",
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            results = response.json()['results']
            decisions = [r['fare_bucket_code'] for r in results]
            all_decisions.extend(decisions)
        elif response.status_code == 429:
            print(f"\n   {RED}🛡️  BLOCKED by rate limiting!{RESET}")
            blocked = True
            break
        else:
            print(f"\n   {RED}API Error: {response.status_code}{RESET}")
            break

        # Progress indicator
        progress = min(len(all_decisions), len(searches_df))
        print(f"\r   Queries sent: {progress}/{len(searches_df)}", end="", flush=True)

    print()
    return np.array(all_decisions), blocked


def run_attack():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  🔓 COMPETITOR ATTACK: Stealing Pricing Algorithm{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    # Phase 0: Reconnaissance
    print(f"{BOLD}{CYAN}🔎 PHASE 0: API Reconnaissance{RESET}")
    try:
        info = requests.get(f"{API_BASE_URL}/api_info", timeout=5).json()
        print(f"   ✅ Target: {info['name']}")
        print(f"   ✅ Fields discovered: {len(info['required_fields'])}")
        print(f"   ✅ Fare buckets: {info['fare_buckets']}")
    except requests.exceptions.ConnectionError:
        print(f"   {RED}❌ Cannot connect to API at {API_BASE_URL}{RESET}")
        print(f"   {YELLOW}➡️  Run '1b_api_server.py' in another terminal first!{RESET}")
        return

    # Phase 1: Generate probe searches
    print(f"\n{BOLD}{CYAN}📡 PHASE 1: Generating Fake Flight Searches{RESET}")
    n_queries = 3000
    probe_df = generate_probe_searches(n_samples=n_queries, random_state=123)

    print(f"   {BOLD}Sample Probes:{RESET}")
    for i in range(3):
        row = probe_df.iloc[i]
        print(f"   Search {i+1}: {row['route_distance_km']:.0f}km, "
              f"{row['days_to_departure']}d out, "
              f"Load={row['current_load_factor']:.0%}, "
              f"Season={'Peak' if row['season']==2 else 'Off' if row['season']==0 else 'Shoulder'}")

    print(f"\n   Generated {n_queries} fake flight searches")

    # Phase 2: Query the API
    print(f"\n{BOLD}{CYAN}🌐 PHASE 2: Querying Fare Quote API{RESET}")
    print(f"   POST {API_BASE_URL}/batch_fare_quote\n")

    start_time = time.time()
    stolen_labels, was_blocked = query_api_batch(probe_df, batch_size=100)
    query_time = time.time() - start_time

    if was_blocked and len(stolen_labels) < 200:
        print(f"\n   {GREEN}🛡️  DEFENSE SUCCESSFUL! Insufficient data collected.{RESET}")
        return

    # Trim probe_df if partially blocked
    if len(stolen_labels) < len(probe_df):
        probe_df = probe_df.iloc[:len(stolen_labels)]

    label_counts = np.bincount(stolen_labels, minlength=5)
    print(f"\n   ✅ Collected {len(stolen_labels)} fare responses")
    print(f"   ⏱️  Query time: {query_time:.1f}s")
    print(f"\n   {BOLD}Stolen Fare Distribution:{RESET}")
    for i, name in enumerate(FARE_BUCKETS):
        bar = "█" * (label_counts[i] // 20)
        print(f"   {name:<15} {label_counts[i]:>4}  {bar}")

    # Phase 3: Train surrogate model
    print(f"\n{BOLD}{CYAN}🧠 PHASE 3: Training Stolen Pricing Model{RESET}")
    print(f"   Cloning the airline's pricing algorithm...\n")

    surrogate_model = GradientBoostingClassifier(
        n_estimators=150,
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    )

    surrogate_model.fit(probe_df.values, stolen_labels)

    os.makedirs('models', exist_ok=True)
    joblib.dump(surrogate_model, 'models/stolen_pricing_model.joblib')

    print(f"   ✅ Stolen pricing model trained!")
    print(f"   💾 Saved: models/stolen_pricing_model.joblib")

    if was_blocked:
        print(f"\n   {YELLOW}⚠️  Partial attack (was rate-limited){RESET}")
        print(f"   Model trained with only {len(stolen_labels)} samples")
    else:
        print(f"\n   {RED}💀 ATTACK SUCCESSFUL!{RESET}")
        print(f"   Competitor now has a copy of our pricing algorithm!")

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{YELLOW}➡️  Next: Run '3_compare_models.py' to measure theft accuracy{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")


if __name__ == "__main__":
    run_attack()
