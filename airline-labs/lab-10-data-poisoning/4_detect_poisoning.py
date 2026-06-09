#!/usr/bin/env python3
"""
Step 4: Defense — Detect Data Poisoning Before Retraining

AIRLINE SCENARIO:
Before retraining, the data pipeline runs statistical validation:
1. Distribution comparison (new data vs historical baseline)
2. Outlier detection (z-score analysis)
3. Sudden shift detection (compare recent vs older records)

If anomalies are found → BLOCK retrain, alert data team.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import pandas as pd
from scipy import stats
import os
import json

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


def detect_poisoning():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  DEFENSE: Data Poisoning Detection{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    if not os.path.exists('models/fuel_data_poisoned.csv'):
        print(f"  {YELLOW}Run 2_poison_training_data.py first!{RESET}")
        return

    clean_df = pd.read_csv('models/fuel_data_clean.csv')
    poisoned_df = pd.read_csv('models/fuel_data_poisoned.csv')

    with open('models/baseline_stats.json', 'r') as f:
        baseline = json.load(f)

    print(f"  {CYAN}Running pre-retrain data validation pipeline...{RESET}\n")

    alerts = []

    # ═══════════════════════════════════════════════════════════════
    # CHECK 1: Distribution shift (KS test)
    # ═══════════════════════════════════════════════════════════════
    print(f"  {BOLD}[1/4] Distribution Comparison (KS Test){RESET}")
    ks_stat, ks_pvalue = stats.ks_2samp(
        clean_df['actual_fuel_kg'],
        poisoned_df['actual_fuel_kg']
    )
    ks_pass = ks_pvalue > 0.01

    if ks_pass:
        print(f"    KS statistic: {ks_stat:.4f}, p-value: {ks_pvalue:.4f}")
        print(f"    {GREEN}[PASS] Distribution consistent with baseline{RESET}")
    else:
        print(f"    KS statistic: {ks_stat:.4f}, p-value: {RED}{ks_pvalue:.6f}{RESET}")
        print(f"    {RED}[FAIL] Distribution SHIFTED from baseline!{RESET}")
        alerts.append("Distribution shift detected (KS test)")

    # ═══════════════════════════════════════════════════════════════
    # CHECK 2: Mean shift
    # ═══════════════════════════════════════════════════════════════
    print(f"\n  {BOLD}[2/4] Mean Comparison{RESET}")
    baseline_mean = baseline['avg_fuel']
    current_mean = poisoned_df['actual_fuel_kg'].mean()
    shift_pct = (current_mean - baseline_mean) / baseline_mean * 100

    mean_pass = abs(shift_pct) < 3.0  # Allow up to 3% natural drift

    if mean_pass:
        print(f"    Baseline mean: {baseline_mean:,.0f} kg")
        print(f"    Current mean:  {current_mean:,.0f} kg ({shift_pct:+.1f}%)")
        print(f"    {GREEN}[PASS] Within 3% tolerance{RESET}")
    else:
        print(f"    Baseline mean: {baseline_mean:,.0f} kg")
        print(f"    Current mean:  {RED}{current_mean:,.0f} kg ({shift_pct:+.1f}%){RESET}")
        print(f"    {RED}[FAIL] Mean shifted {shift_pct:.1f}% (threshold: 3%){RESET}")
        alerts.append(f"Mean shifted {shift_pct:.1f}% from baseline")

    # ═══════════════════════════════════════════════════════════════
    # CHECK 3: Outlier analysis (z-score)
    # ═══════════════════════════════════════════════════════════════
    print(f"\n  {BOLD}[3/4] Outlier Detection (Z-Score){RESET}")
    z_scores = np.abs(stats.zscore(poisoned_df['actual_fuel_kg']))
    n_outliers = (z_scores > 3).sum()
    outlier_pct = n_outliers / len(poisoned_df) * 100

    # Compare with clean data outlier rate
    clean_z = np.abs(stats.zscore(clean_df['actual_fuel_kg']))
    clean_outliers = (clean_z > 3).sum()
    clean_outlier_pct = clean_outliers / len(clean_df) * 100

    outlier_pass = outlier_pct < clean_outlier_pct * 2  # Allow 2x baseline

    if outlier_pass:
        print(f"    Outliers (|z| > 3): {n_outliers} ({outlier_pct:.1f}%)")
        print(f"    Baseline rate:      {clean_outliers} ({clean_outlier_pct:.1f}%)")
        print(f"    {GREEN}[PASS] Outlier rate within tolerance{RESET}")
    else:
        print(f"    Outliers (|z| > 3): {RED}{n_outliers} ({outlier_pct:.1f}%){RESET}")
        print(f"    Baseline rate:      {clean_outliers} ({clean_outlier_pct:.1f}%)")
        print(f"    {RED}[FAIL] Outlier rate {outlier_pct/clean_outlier_pct:.1f}x above baseline{RESET}")
        alerts.append(f"Outlier rate elevated: {outlier_pct:.1f}% vs baseline {clean_outlier_pct:.1f}%")

    # ═══════════════════════════════════════════════════════════════
    # CHECK 4: Per-aircraft anomaly
    # ═══════════════════════════════════════════════════════════════
    print(f"\n  {BOLD}[4/4] Per-Aircraft Consistency Check{RESET}")
    aircraft_types = ['A320', 'A330', 'A350', 'B737', 'B777', 'B787']
    aircraft_alerts = 0

    for idx, aircraft in enumerate(aircraft_types):
        clean_mean = clean_df[clean_df['aircraft_type_idx'] == idx]['actual_fuel_kg'].mean()
        poisoned_mean = poisoned_df[poisoned_df['aircraft_type_idx'] == idx]['actual_fuel_kg'].mean()

        if pd.isna(clean_mean) or pd.isna(poisoned_mean):
            continue

        shift = (poisoned_mean - clean_mean) / clean_mean * 100
        if abs(shift) > 3:
            print(f"    {aircraft}: {RED}+{shift:.1f}% from baseline [ANOMALY]{RESET}")
            aircraft_alerts += 1
        else:
            print(f"    {aircraft}: {GREEN}{shift:+.1f}% [OK]{RESET}")

    if aircraft_alerts > 2:
        alerts.append(f"Multiple aircraft types show anomalous fuel increase")

    # ═══════════════════════════════════════════════════════════════
    # FINAL DECISION
    # ═══════════════════════════════════════════════════════════════
    print(f"\n  {'═'*55}")
    if alerts:
        print(f"  {BOLD}{RED}  🚨 RETRAIN BLOCKED — DATA INTEGRITY ISSUES DETECTED{RESET}")
        print(f"  {'═'*55}")
        print(f"\n  {RED}Alerts:{RESET}")
        for alert in alerts:
            print(f"    ⚠️  {alert}")

        print(f"\n  {BOLD}Recommended Actions:{RESET}")
        print(f"    1. Investigate data sources for unauthorized modifications")
        print(f"    2. Compare with backup data to identify changed records")
        print(f"    3. Audit database access logs for suspicious write operations")
        print(f"    4. Quarantine new data until verified")
        print(f"    5. Retrain ONLY on verified clean data")

        print(f"\n  {GREEN}✅ DEFENSE SUCCESSFUL: Poisoned retrain prevented!{RESET}")
        print(f"  {GREEN}   The model continues using the last verified version.{RESET}")
    else:
        print(f"  {BOLD}{GREEN}  ✅ ALL CHECKS PASSED — Retrain approved{RESET}")
        print(f"  {'═'*55}")

    print()


if __name__ == "__main__":
    detect_poisoning()
