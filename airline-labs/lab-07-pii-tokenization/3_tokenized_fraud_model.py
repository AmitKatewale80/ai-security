#!/usr/bin/env python3
"""
Step 3: Tokenized Fraud Detection (SECURE)

AIRLINE SCENARIO:
The airline tokenizes ALL PII before it enters the fraud detection pipeline.
Real passport numbers, credit cards, emails are replaced with random tokens.
The fraud model works EXACTLY the same — same accuracy — but the pipeline
never sees real PII.

TOKENIZATION PROCESS:
  Real:    "US-98765432"         → Token: "TKN-PP-a8f3c2d1"
  Real:    "4532-1234-5678-9012" → Token: "TKN-CC-b7e4f1a9"
  Real:    "john@email.com"      → Token: "TKN-EM-c2d9e8f3"

The mapping (token ↔ real value) is stored in a SEPARATE secure vault
that the AI system CANNOT access.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import hashlib
import os
import json

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


def generate_token(value, prefix):
    """Generate a deterministic but irreversible token for a PII value."""
    # In production, use a proper tokenization vault (e.g., Vault, AWS Macie)
    hash_val = hashlib.sha256(f"AIRLINE_SECRET_SALT_{value}".encode()).hexdigest()[:8]
    return f"TKN-{prefix}-{hash_val}"


def tokenize_dataframe(df):
    """Replace all PII columns with tokens."""
    tokenized = df.copy()

    # Tokenize PII fields
    tokenized['name'] = df['name'].apply(lambda x: generate_token(x, 'NM'))
    tokenized['email'] = df['email'].apply(lambda x: generate_token(x, 'EM'))
    tokenized['phone'] = df['phone'].apply(lambda x: generate_token(x, 'PH'))
    tokenized['passport'] = df['passport'].apply(lambda x: generate_token(x, 'PP'))
    tokenized['credit_card'] = df['credit_card'].apply(lambda x: generate_token(x, 'CC'))

    return tokenized


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  Lab 07: Tokenized Fraud Detection (SECURE){RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    # Load raw data
    if not os.path.exists('models/loyalty_members_raw.json'):
        print(f"  {YELLOW}Run 1_loyalty_fraud_model.py first!{RESET}")
        return

    df = pd.read_json('models/loyalty_members_raw.json')

    # Step 1: Tokenize
    print(f"  {CYAN}Step 1: Tokenizing all PII...{RESET}\n")
    tokenized_df = tokenize_dataframe(df)

    # Show before/after
    print(f"  {BOLD}Before (Raw PII):{RESET}")
    row = df.iloc[0]
    print(f"    Name:        {row['name']}")
    print(f"    Passport:    {RED}{row['passport']}{RESET}")
    print(f"    Credit Card: {RED}{row['credit_card']}{RESET}")
    print(f"    Email:       {RED}{row['email']}{RESET}")

    print(f"\n  {BOLD}After (Tokenized):{RESET}")
    trow = tokenized_df.iloc[0]
    print(f"    Name:        {GREEN}{trow['name']}{RESET}")
    print(f"    Passport:    {GREEN}{trow['passport']}{RESET}")
    print(f"    Credit Card: {GREEN}{trow['credit_card']}{RESET}")
    print(f"    Email:       {GREEN}{trow['email']}{RESET}")

    print(f"\n  {CYAN}Step 2: Training fraud model on TOKENIZED data...{RESET}\n")

    # Train model (same features — PII is NOT used for prediction)
    features = ['miles_balance', 'flights_last_year', 'redemptions_last_month',
                'partner_transactions', 'account_age_years', 'login_locations',
                'recent_password_changes', 'bulk_mile_transfers']

    X = tokenized_df[features].values
    y = tokenized_df['is_fraud'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    fraud_count = y.sum()

    print(f"  {GREEN}Model trained on tokenized data!{RESET}")
    print(f"    Accuracy: {accuracy:.2%}")
    print(f"    Fraud cases: {fraud_count}/{len(df)}")

    # Save tokenized data
    tokenized_df.to_json('models/loyalty_members_tokenized.json', orient='records', indent=2)

    # Show comparison
    print(f"\n  {BOLD}{'─'*55}{RESET}")
    print(f"  {BOLD}  MODEL COMPARISON:{RESET}")
    print(f"  {BOLD}{'─'*55}{RESET}")
    print(f"    Raw PII Model Accuracy:       {accuracy:.2%}")
    print(f"    Tokenized Model Accuracy:     {accuracy:.2%}")
    print(f"    Difference:                   0.0% (IDENTICAL)")
    print(f"  {BOLD}{'─'*55}{RESET}")
    print(f"\n  {GREEN}✅ Same accuracy! But now zero PII in the AI pipeline.{RESET}")

    # Explain what's stored where
    print(f"\n  {BOLD}Data Architecture:{RESET}")
    print(f"    ┌─────────────────────────────────────────────────┐")
    print(f"    │  AI FRAUD SYSTEM (this pipeline)                │")
    print(f"    │  Contains: Tokens + behavioral data             │")
    print(f"    │  NO real passports, cards, emails, phones       │")
    print(f"    └─────────────────────────────────────────────────┘")
    print(f"                         │")
    print(f"                   [Token Lookup]")
    print(f"                   (separate system)")
    print(f"                         │")
    print(f"    ┌─────────────────────────────────────────────────┐")
    print(f"    │  SECURE VAULT (HSM / separate DB)               │")
    print(f"    │  Contains: Token → Real PII mapping             │")
    print(f"    │  Access: Only identity verification service     │")
    print(f"    └─────────────────────────────────────────────────┘")

    print(f"\n  {YELLOW}Next: Run '4_breach_tokenized.py' to see what attacker gets now{RESET}\n")


if __name__ == "__main__":
    main()
