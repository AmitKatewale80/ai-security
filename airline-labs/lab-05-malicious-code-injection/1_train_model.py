#!/usr/bin/env python3
"""
Lab 05: Train Benign Baggage Screening Model

Trains a legitimate baggage X-ray classification model that detects
prohibited items in luggage scans.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os
from pathlib import Path

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Baggage item categories
CATEGORIES = ['CLEAR', 'FLAGGED_WEAPON', 'FLAGGED_EXPLOSIVE', 'FLAGGED_CONTRABAND', 'REVIEW']


def generate_xray_features(n_samples=2000, random_state=42):
    """
    Generate simulated X-ray scan features.
    In reality these would be image features from a CNN.
    """
    np.random.seed(random_state)

    # Simulated features: density, shape, metallic content, organic ratio, etc.
    features = {
        'density_score': np.random.uniform(0, 1, n_samples),
        'metallic_signature': np.random.uniform(0, 1, n_samples),
        'organic_ratio': np.random.uniform(0, 1, n_samples),
        'shape_regularity': np.random.uniform(0, 1, n_samples),
        'edge_sharpness': np.random.uniform(0, 1, n_samples),
        'size_cm2': np.random.uniform(5, 500, n_samples),
        'z_effective': np.random.uniform(5, 30, n_samples),
        'transmission_ratio': np.random.uniform(0.1, 0.99, n_samples),
    }

    X = np.column_stack(list(features.values()))

    # Generate labels based on feature combinations
    labels = np.zeros(n_samples, dtype=int)

    for i in range(n_samples):
        metal = features['metallic_signature'][i]
        density = features['density_score'][i]
        organic = features['organic_ratio'][i]
        shape = features['shape_regularity'][i]
        z_eff = features['z_effective'][i]

        if metal > 0.8 and shape > 0.7 and z_eff > 20:
            labels[i] = 1  # FLAGGED_WEAPON
        elif density > 0.85 and organic > 0.6 and z_eff > 15:
            labels[i] = 2  # FLAGGED_EXPLOSIVE
        elif metal > 0.6 and density > 0.7 and organic < 0.3:
            labels[i] = 3  # FLAGGED_CONTRABAND
        elif metal > 0.5 or density > 0.75:
            labels[i] = 4  # REVIEW
        else:
            labels[i] = 0  # CLEAR

    return X, labels


def train_model():
    """Train and save the benign baggage screening model."""
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 05: Training Benign Baggage Screening Model
{'='*60}
{RESET}
  {CYAN}Scenario: Airport security uses AI to classify X-ray scans
  of passenger luggage for prohibited items.{RESET}
""")

    # Generate training data
    print(f"  {CYAN}Generating simulated X-ray scan features...{RESET}")
    X, y = generate_xray_features(n_samples=2000)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print(f"  Training samples: {len(X_train)}")
    print(f"  Test samples: {len(X_test)}")
    print(f"  Features: 8 (density, metallic, organic, shape, edge, size, z-eff, transmission)")
    print(f"  Classes: {len(CATEGORIES)}")

    # Train model
    print(f"\n  {CYAN}Training RandomForest classifier...{RESET}")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"\n  {GREEN}[OK] Model trained successfully!{RESET}")
    print(f"  Accuracy: {accuracy:.2%}")

    print(f"\n  {BOLD}Classification Report:{RESET}")
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, target_names=CATEGORIES, zero_division=0)
    for line in report.split('\n'):
        print(f"    {line}")

    # Save model
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "baggage_screening_model.joblib"
    model_metadata = {
        'model': model,
        'version': '1.0.0',
        'author': 'Airport Security AI Team',
        'categories': CATEGORIES,
        'feature_names': ['density_score', 'metallic_signature', 'organic_ratio',
                         'shape_regularity', 'edge_sharpness', 'size_cm2',
                         'z_effective', 'transmission_ratio'],
        'accuracy': accuracy,
    }
    joblib.dump(model_metadata, model_path)

    print(f"\n  {GREEN}[OK]{RESET} Model saved to: {model_path}")
    print(f"  {GREEN}[OK]{RESET} Model version: 1.0.0")
    print(f"  {GREEN}[OK]{RESET} This is the LEGITIMATE model - no backdoors.")
    print(f"\n  {YELLOW}[WARN] Next: Run 2_inject_backdoor.py to see how an attacker")
    print(f"        can modify this model to exfiltrate data.{RESET}\n")


if __name__ == "__main__":
    train_model()
