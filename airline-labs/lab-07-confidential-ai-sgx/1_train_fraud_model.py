#!/usr/bin/env python3
"""
Lab 07: Train Fraud Detection Model

Trains a model to detect fraudulent bookings based on
passenger and transaction features.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'


def generate_booking_data(n_samples=2000, random_state=42):
    """Generate simulated booking transaction data."""
    np.random.seed(random_state)

    data = {
        'booking_amount_usd': np.random.lognormal(6, 1, n_samples),
        'days_before_departure': np.random.exponential(30, n_samples).clip(0, 365),
        'num_passengers': np.random.choice([1, 2, 3, 4, 5, 6], n_samples, p=[0.4, 0.3, 0.15, 0.08, 0.05, 0.02]),
        'is_one_way': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'payment_attempts': np.random.poisson(1.2, n_samples).clip(1, 10),
        'ip_country_match': np.random.choice([0, 1], n_samples, p=[0.15, 0.85]),
        'card_country_match': np.random.choice([0, 1], n_samples, p=[0.1, 0.9]),
        'booking_hour': np.random.randint(0, 24, n_samples),
        'loyalty_member': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
        'previous_bookings': np.random.poisson(3, n_samples),
    }

    X = np.column_stack(list(data.values()))

    # Generate fraud labels
    labels = np.zeros(n_samples, dtype=int)
    for i in range(n_samples):
        fraud_score = 0
        if data['payment_attempts'][i] > 3:
            fraud_score += 3
        if data['ip_country_match'][i] == 0:
            fraud_score += 2
        if data['card_country_match'][i] == 0:
            fraud_score += 2
        if data['booking_amount_usd'][i] > 3000 and data['days_before_departure'][i] < 2:
            fraud_score += 3
        if data['loyalty_member'][i] == 0 and data['previous_bookings'][i] == 0:
            fraud_score += 1
        if data['booking_hour'][i] >= 1 and data['booking_hour'][i] <= 5:
            fraud_score += 1

        labels[i] = 1 if fraud_score >= 5 else 0

    return X, labels


def train_model():
    """Train and save the fraud detection model."""
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 07: Training Fraud Detection Model
{'='*60}
{RESET}
  {CYAN}Scenario: Model detects fraudulent bookings by analyzing
  transaction patterns, payment behavior, and passenger data.{RESET}
""")

    print(f"  {CYAN}Generating booking transaction data...{RESET}")
    X, y = generate_booking_data(n_samples=2000)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    fraud_rate = y.mean() * 100
    print(f"  Training samples: {len(X_train)}")
    print(f"  Test samples: {len(X_test)}")
    print(f"  Fraud rate: {fraud_rate:.1f}%")

    # Train model
    print(f"\n  {CYAN}Training RandomForest classifier...{RESET}")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"\n  {GREEN}[OK] Model trained!{RESET}")
    print(f"  Accuracy: {accuracy:.2%}")

    # Save model
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "fraud_detection_model.joblib"
    model_data = {
        'model': model,
        'version': '1.0.0',
        'feature_names': ['booking_amount_usd', 'days_before_departure', 'num_passengers',
                         'is_one_way', 'payment_attempts', 'ip_country_match',
                         'card_country_match', 'booking_hour', 'loyalty_member',
                         'previous_bookings'],
        'accuracy': accuracy,
    }
    joblib.dump(model_data, model_path)

    print(f"\n  {GREEN}[OK]{RESET} Model saved to: {model_path}")
    print(f"  {YELLOW}Next: Run 2_unprotected_inference.py to see data exposure risk.{RESET}\n")


if __name__ == "__main__":
    train_model()
