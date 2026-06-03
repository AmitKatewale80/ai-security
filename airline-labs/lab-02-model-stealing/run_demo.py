#!/usr/bin/env python3
"""
Airline Dynamic Pricing Theft - ALL IN ONE DEMO

Run this single script to see the entire attack without needing
two terminals. Executes in under 30 seconds.

SCENARIO: Competitor steals airline's dynamic pricing algorithm
by querying the Fare Quote API with thousands of fake searches.

MITRE ATLAS: AML.T0044 (Full Model Access), AML.T0024 (Exfiltration via API)

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'

FEATURE_NAMES = [
    'route_distance_km', 'days_to_departure', 'day_of_week', 'hour_of_day',
    'current_load_factor', 'competitor_base_fare', 'season',
    'booking_class_avail', 'is_connecting', 'loyalty_tier'
]

FARE_BUCKETS = ['DEEP_DISCOUNT', 'DISCOUNT', 'STANDARD', 'PREMIUM', 'SURGE']


def generate_pricing_data(n_samples=5000, random_state=42):
    """Generate airline's proprietary pricing data."""
    np.random.seed(random_state)

    data = {
        'route_distance_km': np.random.choice([500, 1200, 2500, 4000, 6500, 9000, 12000], n_samples),
        'days_to_departure': np.random.exponential(45, n_samples).clip(0, 365).astype(int),
        'day_of_week': np.random.randint(0, 7, n_samples),
        'hour_of_day': np.random.choice([6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22], n_samples),
        'current_load_factor': np.random.beta(5, 3, n_samples),
        'competitor_base_fare': np.random.lognormal(5.8, 0.5, n_samples),
        'season': np.random.choice([0, 1, 2], n_samples, p=[0.3, 0.4, 0.3]),
        'booking_class_avail': np.random.poisson(15, n_samples).clip(0, 50),
        'is_connecting': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
        'loyalty_tier': np.random.choice([0, 1, 2, 3], n_samples, p=[0.5, 0.25, 0.15, 0.1]),
    }

    df = pd.DataFrame(data)

    # Proprietary pricing logic
    score = np.zeros(n_samples)
    score += np.where(df['days_to_departure'] < 3, 30,
             np.where(df['days_to_departure'] < 7, 20,
             np.where(df['days_to_departure'] < 14, 12,
             np.where(df['days_to_departure'] < 30, 5, 0))))
    score += df['current_load_factor'] * 25
    score += df['season'] * 8
    score += np.where(df['day_of_week'] >= 4, 5, 0)
    score += np.where((df['hour_of_day'] >= 7) & (df['hour_of_day'] <= 9), 6, 0)
    score += np.where(df['booking_class_avail'] < 5, 15,
             np.where(df['booking_class_avail'] < 10, 8, 0))
    score -= np.where(df['competitor_base_fare'] < 200, 8, 0)
    score -= df['loyalty_tier'] * 3
    score += np.where(df['route_distance_km'] > 5000, 5, 0)
    score += np.random.normal(0, 4, n_samples)

    labels = np.digitize(score, bins=[15, 25, 35, 50]).clip(0, 4)
    return df.values, labels, df


def generate_probe_searches(n_samples=3000, random_state=123):
    """Competitor generates fake searches."""
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


def run_demo():
    print(f"""
{BOLD}{RED}
╔═══════════════════════════════════════════════════════════════════╗
║     ✈️  AIRLINE PRICING MODEL THEFT - FULL DEMO  ✈️               ║
║                                                                   ║
║   MITRE ATLAS: AML.T0044, AML.T0024                              ║
║                                                                   ║
║   Scenario: Competitor steals dynamic pricing algorithm           ║
║   using only Fare Quote API access.                               ║
╚═══════════════════════════════════════════════════════════════════╝
{RESET}""")

    total_start = time.time()

    # ═══════════════════════════════════════════════════════════════
    # STEP 1: Create airline's pricing model
    # ═══════════════════════════════════════════════════════════════
    print(f"{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}{BLUE}  ✈️  STEP 1: Airline's Proprietary Pricing Model{RESET}")
    print(f"{BOLD}{'─'*60}{RESET}")

    print(f"\n  {YELLOW}Training on 5 years of revenue management data...{RESET}")
    X, y, df = generate_pricing_data(n_samples=5000, random_state=42)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    victim_model = GradientBoostingClassifier(
        n_estimators=200, max_depth=8, learning_rate=0.1, random_state=42
    )
    victim_model.fit(X_train, y_train)

    victim_acc = victim_model.score(X_test, y_test)
    print(f"\n  {GREEN}✅ Pricing Model Ready!{RESET}")
    print(f"     Accuracy: {victim_acc:.2%}")
    print(f"     Architecture: GradientBoosting (200 trees) [SECRET]")
    print(f"     Investment: ~$5M in data science + revenue management R&D")
    print(f"\n  {RED}⚠️  Model deployed as Fare Quote API for travel agents...{RESET}")

    # ═══════════════════════════════════════════════════════════════
    # STEP 2: Competitor's attack
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}{RED}  🔓 STEP 2: Competitor's Query Attack{RESET}")
    print(f"{BOLD}{'─'*60}{RESET}")

    attack_start = time.time()

    print(f"\n  {CYAN}Generating 3,000 fake flight searches...{RESET}")
    n_queries = 3000
    probe_df = generate_probe_searches(n_samples=n_queries)

    print(f"  {CYAN}Querying Fare Quote API (simulated)...{RESET}")
    stolen_labels = victim_model.predict(probe_df.values)

    label_counts = np.bincount(stolen_labels, minlength=5)
    print(f"\n  Stolen fare distribution:")
    for i, name in enumerate(FARE_BUCKETS):
        bar = "█" * (label_counts[i] // 30)
        print(f"    {name:<15} {label_counts[i]:>4}  {bar}")

    print(f"\n  {CYAN}Training stolen pricing model...{RESET}")
    surrogate = GradientBoostingClassifier(
        n_estimators=150, max_depth=6, learning_rate=0.1, random_state=42
    )
    surrogate.fit(probe_df.values, stolen_labels)

    attack_time = time.time() - attack_start

    # ═══════════════════════════════════════════════════════════════
    # STEP 3: Results
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}{MAGENTA}  📊 STEP 3: Theft Results{RESET}")
    print(f"{BOLD}{'─'*60}{RESET}")

    victim_preds = victim_model.predict(X_test)
    stolen_preds = surrogate.predict(X_test)

    fidelity = accuracy_score(victim_preds, stolen_preds)
    stolen_acc = accuracy_score(y_test, stolen_preds)

    # High-value route analysis
    high_value = victim_preds >= 3
    if high_value.sum() > 0:
        hv_fidelity = accuracy_score(victim_preds[high_value], stolen_preds[high_value])
    else:
        hv_fidelity = 0

    print(f"""
   ┌──────────────────────────────────────────────────────┐
   │  {BOLD}PRICING ALGORITHM THEFT ANALYSIS{RESET}                    │
   ├──────────────────────────────────────────────────────┤
   │  Our Model Accuracy:        {victim_acc:>6.1%}                 │
   │  {RED}Stolen Model Accuracy:      {stolen_acc:>6.1%}{RESET}                 │
   │  Overall Fidelity:          {fidelity:>6.1%}                 │
   │  {RED}High-Value Route Match:     {hv_fidelity:>6.1%}{RESET}                 │
   │  Attack Duration:           {attack_time:>5.1f}s                  │
   │  Queries Used:              {n_queries:>5}                  │
   └──────────────────────────────────────────────────────┘
""")

    if fidelity > 0.85:
        print(f"   {BOLD}{RED}🚨 CRITICAL: Competitor can predict {fidelity:.0%} of our fares!{RESET}")
        print(f"   They will undercut us on every high-demand route.")

    # ═══════════════════════════════════════════════════════════════
    # Attack Economics
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}{GREEN}  💰 Attack Economics{RESET}")
    print(f"{BOLD}{'─'*60}{RESET}")

    print(f"""
   {BOLD}Our Airline's Investment:{RESET}
   • 5 years of booking data              $$$$$
   • Revenue management team (10 people)  $$$$$
   • ML infrastructure & training         $$$
   • Total: ~$5,000,000+

   {BOLD}Competitor's Cost:{RESET}
   • {n_queries} API queries              ~$0
   • 30 seconds of compute               ~$0

   {BOLD}{RED}Result: Stole $5M pricing algorithm for FREE!{RESET}
   {RED}Revenue impact: $10-50M/year on competitive routes{RESET}
""")

    # ═══════════════════════════════════════════════════════════════
    # Defenses
    # ═══════════════════════════════════════════════════════════════
    print(f"{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  Defense Recommendations{RESET}")
    print(f"{BOLD}{'─'*60}{RESET}")

    print(f"""
   1. {BOLD}Rate Limiting{RESET}        - Max 20 fare quotes/min per partner
   2. {BOLD}Query Monitoring{RESET}     - Detect systematic route scanning
   3. {BOLD}Response Noise{RESET}       - Add differential privacy to fares
   4. {BOLD}Batch Restrictions{RESET}   - Limit bulk quote requests
   5. {BOLD}Partner Auditing{RESET}     - Track query patterns per API key
   6. {BOLD}Fare Watermarking{RESET}    - Embed traceable patterns in pricing

   Run '4_secure_api_server.py' to see defenses in action.
   Expected: Attack fidelity drops from ~{fidelity:.0%} to ~65%.
""")

    total_time = time.time() - total_start
    print(f"   ⏱️  Total demo time: {total_time:.1f}s\n")


if __name__ == "__main__":
    run_demo()
