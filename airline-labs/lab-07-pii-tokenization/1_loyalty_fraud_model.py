#!/usr/bin/env python3
"""
Step 1: Loyalty Fraud Detection Model (VULNERABLE - Raw PII)

AIRLINE SCENARIO:
The airline's frequent flyer program processes member data through
a fraud detection model. The training data contains REAL PII:
- Passport numbers, credit card numbers, emails, phone numbers

If this system is breached, ALL member PII is exposed.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
import json

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


def generate_loyalty_data(n_members=500):
    """Generate realistic loyalty member data with PII."""
    np.random.seed(42)

    first_names = ['John', 'Maria', 'Ahmed', 'Yuki', 'Carlos', 'Emma', 'Wei',
                   'Fatima', 'Ivan', 'Priya', 'James', 'Sofia', 'Omar', 'Lin', 'Anna']
    last_names = ['Smith', 'Garcia', 'Khan', 'Tanaka', 'Silva', 'Mueller', 'Chen',
                  'Al-Hassan', 'Petrov', 'Sharma', 'Johnson', 'Rossi', 'Ali', 'Park', 'Brown']
    countries = ['US', 'ES', 'AE', 'JP', 'BR', 'DE', 'CN', 'SA', 'RU', 'IN', 'UK', 'IT', 'EG', 'KR', 'AU']

    members = []
    for i in range(n_members):
        fname = np.random.choice(first_names)
        lname = np.random.choice(last_names)
        country = np.random.choice(countries)

        member = {
            'member_id': f'FF{100000 + i}',
            'name': f'{fname} {lname}',
            'email': f'{fname.lower()}.{lname.lower()}@email.com',
            'phone': f'+{np.random.randint(1,99)}-{np.random.randint(100,999)}-{np.random.randint(1000,9999)}',
            'passport': f'{country}-{np.random.randint(10000000, 99999999)}',
            'credit_card': f'{np.random.choice(["4","5"])}{np.random.randint(100, 999)}-{np.random.randint(1000,9999)}-{np.random.randint(1000,9999)}-{np.random.randint(1000,9999)}',
            'tier': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], p=[0.4, 0.3, 0.2, 0.1]),
            'miles_balance': int(np.random.exponential(50000)),
            'flights_last_year': int(np.random.poisson(8)),
            'redemptions_last_month': int(np.random.poisson(1)),
            'partner_transactions': int(np.random.poisson(3)),
            'account_age_years': int(np.random.uniform(1, 15)),
            'login_locations': int(np.random.poisson(2)) + 1,
            'recent_password_changes': int(np.random.poisson(0.3)),
            'bulk_mile_transfers': int(np.random.poisson(0.2)),
        }

        # Fraud logic: suspicious patterns
        fraud_score = 0
        fraud_score += 3 if member['bulk_mile_transfers'] > 2 else 0
        fraud_score += 2 if member['login_locations'] > 5 else 0
        fraud_score += 2 if member['recent_password_changes'] > 2 else 0
        fraud_score += 1 if member['redemptions_last_month'] > 4 else 0
        fraud_score += 2 if member['partner_transactions'] > 8 else 0

        member['is_fraud'] = 1 if fraud_score >= 4 or np.random.random() < 0.03 else 0
        members.append(member)

    return pd.DataFrame(members)


def train_fraud_model(df):
    """Train fraud detection on RAW data (includes PII in pipeline)."""
    features = ['miles_balance', 'flights_last_year', 'redemptions_last_month',
                'partner_transactions', 'account_age_years', 'login_locations',
                'recent_password_changes', 'bulk_mile_transfers']

    X = df[features].values
    y = df['is_fraud'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    fraud_count = y.sum()

    return model, accuracy, fraud_count


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  ⚠️  Lab 07: Loyalty Fraud Detection (VULNERABLE){RESET}")
    print(f"{BOLD}{'='*60}{RESET}")
    print(f"\n  {YELLOW}Training fraud model on RAW member data (PII included)...{RESET}\n")

    # Generate data
    df = generate_loyalty_data(500)

    # Show sample data (PII exposed!)
    print(f"  {BOLD}Sample Training Data (as stored in system):{RESET}\n")
    for i in range(5):
        row = df.iloc[i]
        fraud_label = f"{RED}[FRAUD]{RESET}" if row['is_fraud'] else f"{GREEN}[LEGIT]{RESET}"
        print(f"  Member: {row['name']}")
        print(f"    Email:       {row['email']}")
        print(f"    Passport:    {row['passport']}")
        print(f"    Credit Card: {row['credit_card']}")
        print(f"    Phone:       {row['phone']}")
        print(f"    Miles:       {row['miles_balance']:,}")
        print(f"    Status:      {fraud_label}")
        print()

    # Train model
    model, accuracy, fraud_count = train_fraud_model(df)

    print(f"  {GREEN}Model trained!{RESET}")
    print(f"    Accuracy: {accuracy:.2%}")
    print(f"    Fraud cases detected: {fraud_count}/{len(df)}")

    # Save data and model
    os.makedirs('models', exist_ok=True)
    df.to_json('models/loyalty_members_raw.json', orient='records', indent=2)

    print(f"\n  {RED}{'='*55}{RESET}")
    print(f"  {RED}  ⚠️  WARNING: Raw PII stored in AI pipeline!{RESET}")
    print(f"  {RED}  If this system is breached, attacker gets:{RESET}")
    print(f"  {RED}    • {len(df)} passport numbers{RESET}")
    print(f"  {RED}    • {len(df)} credit card numbers{RESET}")
    print(f"  {RED}    • {len(df)} email addresses{RESET}")
    print(f"  {RED}    • {len(df)} phone numbers{RESET}")
    print(f"  {RED}{'='*55}{RESET}")

    print(f"\n{YELLOW}  Next: Run '2_breach_simulation.py' to see what an attacker gets{RESET}\n")


if __name__ == "__main__":
    main()
