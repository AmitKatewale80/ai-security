#!/usr/bin/env python3
"""
Lab 06: Train Engine Health Prediction Model

Trains a predictive maintenance model that classifies engine health
status based on sensor readings.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
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

ENGINE_STATUS = ['NORMAL', 'MONITOR', 'WARNING', 'CRITICAL']


def generate_engine_data(n_samples=3000, random_state=42):
    """Generate simulated engine sensor data."""
    np.random.seed(random_state)

    data = {
        'oil_temp_c': np.random.normal(85, 15, n_samples),
        'oil_pressure_psi': np.random.normal(60, 10, n_samples),
        'vibration_mm_s': np.random.exponential(2, n_samples),
        'egt_c': np.random.normal(650, 50, n_samples),
        'n1_rpm_pct': np.random.normal(92, 5, n_samples),
        'n2_rpm_pct': np.random.normal(95, 3, n_samples),
        'fuel_flow_kg_h': np.random.normal(2500, 300, n_samples),
        'bleed_air_psi': np.random.normal(40, 8, n_samples),
        'hours_since_overhaul': np.random.uniform(0, 20000, n_samples),
        'cycles_since_overhaul': np.random.uniform(0, 10000, n_samples),
    }

    X = np.column_stack(list(data.values()))

    # Generate labels based on sensor combinations
    labels = np.zeros(n_samples, dtype=int)
    for i in range(n_samples):
        score = 0
        if data['oil_temp_c'][i] > 110:
            score += 2
        if data['oil_pressure_psi'][i] < 40:
            score += 2
        if data['vibration_mm_s'][i] > 5:
            score += 2
        if data['egt_c'][i] > 750:
            score += 1
        if data['hours_since_overhaul'][i] > 15000:
            score += 1
        if data['vibration_mm_s'][i] > 8:
            score += 3

        if score >= 5:
            labels[i] = 3  # CRITICAL
        elif score >= 3:
            labels[i] = 2  # WARNING
        elif score >= 1:
            labels[i] = 1  # MONITOR
        else:
            labels[i] = 0  # NORMAL

    return X, labels


def train_model():
    """Train and save the engine health model."""
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 06: Training Engine Health Prediction Model
{'='*60}
{RESET}
  {CYAN}Scenario: Predictive maintenance model monitors engine
  sensor data to predict failures before they occur.{RESET}
""")

    print(f"  {CYAN}Generating engine sensor data...{RESET}")
    X, y = generate_engine_data(n_samples=3000)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print(f"  Training samples: {len(X_train)}")
    print(f"  Test samples: {len(X_test)}")
    print(f"  Features: 10 (oil_temp, oil_pressure, vibration, EGT, N1, N2, fuel_flow, bleed, hours, cycles)")

    # Show class distribution
    print(f"\n  {BOLD}Class Distribution:{RESET}")
    for i, status in enumerate(ENGINE_STATUS):
        count = (y == i).sum()
        print(f"    {status:<10}: {count:>4} ({count/len(y)*100:.1f}%)")

    # Train model
    print(f"\n  {CYAN}Training GradientBoosting classifier...{RESET}")
    model = GradientBoostingClassifier(
        n_estimators=150,
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"\n  {GREEN}[OK] Model trained!{RESET}")
    print(f"  Accuracy: {accuracy:.2%}")

    # Save model
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "engine_health_model.joblib"
    model_data = {
        'model': model,
        'version': '2.1.0',
        'author': 'Predictive Maintenance Team',
        'categories': ENGINE_STATUS,
        'feature_names': ['oil_temp_c', 'oil_pressure_psi', 'vibration_mm_s',
                         'egt_c', 'n1_rpm_pct', 'n2_rpm_pct', 'fuel_flow_kg_h',
                         'bleed_air_psi', 'hours_since_overhaul', 'cycles_since_overhaul'],
        'accuracy': accuracy,
    }
    joblib.dump(model_data, model_path)

    print(f"\n  {GREEN}[OK]{RESET} Model saved to: {model_path}")
    print(f"  {YELLOW}Next: Run 2_sign_model.py to cryptographically sign this model.{RESET}\n")


if __name__ == "__main__":
    train_model()
