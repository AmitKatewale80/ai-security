#!/usr/bin/env python3
"""
Step 1: Create the Airline's Proprietary Dynamic Pricing Model

AIRLINE SCENARIO:
The airline's Revenue Management team has spent years developing a
dynamic pricing algorithm. It considers route demand, seasonality,
competitor pricing, booking window, and load factor to set optimal fares.

This model represents millions in R&D investment and is the airline's
core competitive advantage.

Features:
- Route (encoded), Days to departure, Day of week
- Current load factor, Competitor base fare
- Season, Time of day, Booking class availability

Output: Fare bucket (1-5) determining ticket price tier

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Feature definitions for the pricing model
FEATURE_NAMES = [
    'route_distance_km',       # Route distance in km
    'days_to_departure',       # Days until flight departs (0-365)
    'day_of_week',             # 0=Mon, 6=Sun
    'hour_of_day',             # Departure hour (0-23)
    'current_load_factor',     # Current booking % (0.0-1.0)
    'competitor_base_fare',    # Competitor's lowest fare ($)
    'season',                  # 0=Off-peak, 1=Shoulder, 2=Peak
    'booking_class_avail',     # Available seats in class (0-50)
    'is_connecting',           # 0=Direct, 1=Connecting
    'loyalty_tier',            # 0=None, 1=Silver, 2=Gold, 3=Platinum
]

# Fare buckets (output classes)
FARE_BUCKETS = [
    'DEEP_DISCOUNT',    # 0 - Lowest fare (early birds, off-peak)
    'DISCOUNT',         # 1 - Below average
    'STANDARD',         # 2 - Normal fare
    'PREMIUM',          # 3 - Above average (high demand)
    'SURGE',            # 4 - Maximum fare (last minute, peak)
]


def generate_pricing_data(n_samples=5000, random_state=42):
    """
    Generate realistic airline pricing data.
    This simulates the airline's proprietary historical pricing decisions.
    """
    np.random.seed(random_state)

    data = {
        'route_distance_km': np.random.choice([500, 1200, 2500, 4000, 6500, 9000, 12000], n_samples),
        'days_to_departure': np.random.exponential(45, n_samples).clip(0, 365).astype(int),
        'day_of_week': np.random.randint(0, 7, n_samples),
        'hour_of_day': np.random.choice([6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22], n_samples),
        'current_load_factor': np.random.beta(5, 3, n_samples),  # Skewed toward higher load
        'competitor_base_fare': np.random.lognormal(5.8, 0.5, n_samples),  # ~$330 median
        'season': np.random.choice([0, 1, 2], n_samples, p=[0.3, 0.4, 0.3]),
        'booking_class_avail': np.random.poisson(15, n_samples).clip(0, 50),
        'is_connecting': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
        'loyalty_tier': np.random.choice([0, 1, 2, 3], n_samples, p=[0.5, 0.25, 0.15, 0.1]),
    }

    df = pd.DataFrame(data)

    # ═══════════════════════════════════════════════════════════════════
    # PROPRIETARY PRICING LOGIC (the airline's "secret sauce")
    # This scoring determines fare bucket based on multiple factors
    # ═══════════════════════════════════════════════════════════════════
    score = np.zeros(n_samples)

    # Demand pressure (closer to departure = higher price)
    score += np.where(df['days_to_departure'] < 3, 30,
             np.where(df['days_to_departure'] < 7, 20,
             np.where(df['days_to_departure'] < 14, 12,
             np.where(df['days_to_departure'] < 30, 5, 0))))

    # Load factor impact (fuller plane = higher price)
    score += df['current_load_factor'] * 25

    # Season impact
    score += df['season'] * 8

    # Weekend premium (Fri-Sun)
    score += np.where(df['day_of_week'] >= 4, 5, 0)

    # Peak hour premium
    score += np.where((df['hour_of_day'] >= 7) & (df['hour_of_day'] <= 9), 6, 0)
    score += np.where((df['hour_of_day'] >= 17) & (df['hour_of_day'] <= 19), 4, 0)

    # Scarcity (fewer seats = higher price)
    score += np.where(df['booking_class_avail'] < 5, 15,
             np.where(df['booking_class_avail'] < 10, 8, 0))

    # Competitor undercutting (if competitor is cheap, we match)
    score -= np.where(df['competitor_base_fare'] < 200, 8, 0)

    # Loyalty discount (reduce score for loyal customers)
    score -= df['loyalty_tier'] * 3

    # Distance factor (long-haul has different dynamics)
    score += np.where(df['route_distance_km'] > 5000, 5, 0)

    # Add noise
    score += np.random.normal(0, 4, n_samples)

    # Classify into 5 fare buckets
    labels = np.digitize(score, bins=[15, 25, 35, 50]) 
    labels = labels.clip(0, 4)

    return df.values, labels, df


def create_pricing_model():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}  ✈️  Creating Proprietary Dynamic Pricing Model{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    # Generate proprietary pricing data
    print(f"{YELLOW}📊 Generating historical pricing decisions (5 years of data)...{RESET}")
    X, y, df = generate_pricing_data(n_samples=5000, random_state=42)

    # Show sample data
    print(f"\n   {BOLD}Sample Pricing Decisions:{RESET}")
    for i in range(3):
        row = df.iloc[i]
        print(f"   Flight {i+1}: {row['route_distance_km']:.0f}km, "
              f"{row['days_to_departure']:.0f}d out, "
              f"Load={row['current_load_factor']:.0%}, "
              f"Season={'Peak' if row['season']==2 else 'Shoulder' if row['season']==1 else 'Off-peak'} "
              f"→ {FARE_BUCKETS[y[i]]}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print(f"\n   ✅ Training samples: {len(X_train)}")
    print(f"   ✅ Test samples: {len(X_test)}")
    print(f"   ✅ Features: {len(FEATURE_NAMES)}")
    print(f"   ✅ Fare buckets: {FARE_BUCKETS}")

    # Train the proprietary model
    print(f"\n{YELLOW}🔧 Training Gradient Boosting pricing model...{RESET}")

    pricing_model = GradientBoostingClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.1,
        min_samples_split=10,
        random_state=42
    )

    pricing_model.fit(X_train, y_train)

    train_acc = pricing_model.score(X_train, y_train)
    test_acc = pricing_model.score(X_test, y_test)

    print(f"\n{GREEN}✅ Dynamic Pricing Model Trained!{RESET}")
    print(f"\n{BOLD}📈 Model Performance (CONFIDENTIAL):{RESET}")
    print(f"   • Training Accuracy: {train_acc:.2%}")
    print(f"   • Test Accuracy: {test_acc:.2%}")
    print(f"   • Architecture: GradientBoosting (200 trees, depth=8) [SECRET]")

    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(pricing_model, 'models/pricing_model.joblib')

    print(f"\n{BLUE}💾 Saved: models/pricing_model.joblib{RESET}")

    print(f"\n{BOLD}{RED}⚠️  SCENARIO:{RESET}")
    print(f"   The airline exposes a 'Get Fare Quote' API for travel agents")
    print(f"   and partner booking platforms.")
    print(f"   ")
    print(f"   • Input: Route details, dates, passenger info (10 features)")
    print(f"   • Output: Fare bucket (DEEP_DISCOUNT → SURGE)")
    print(f"   ")
    print(f"   {BOLD}A competitor wants to systematically undercut our fares.{RESET}")
    print(f"   They plan to reverse-engineer our pricing algorithm by")
    print(f"   querying the API with thousands of fake searches.")

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{YELLOW}➡️  Next: Run '1b_api_server.py' to start the Fare Quote API{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")


if __name__ == "__main__":
    create_pricing_model()
