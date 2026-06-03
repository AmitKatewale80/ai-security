#!/usr/bin/env python3
"""
Lab 10: Create Sample Airline Alliance Data

Creates confidential route data for 3 alliance airlines.
Each airline has sensitive pricing, load factor, and cost data
that must not be revealed to partners.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import numpy as np
import json
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

# Alliance airlines
AIRLINES = {
    "SkyWings": {
        "code": "SW",
        "hub": "JFK",
        "routes": ["JFK-LHR", "JFK-CDG", "JFK-FRA", "JFK-NRT", "JFK-SIN"],
        "base_fare_range": (400, 2500),
        "load_factor_mean": 0.82,
        "cost_per_asm": 0.12,
    },
    "EuroConnect": {
        "code": "EC",
        "hub": "LHR",
        "routes": ["LHR-JFK", "LHR-CDG", "LHR-FRA", "LHR-DXB", "LHR-SIN"],
        "base_fare_range": (350, 2200),
        "load_factor_mean": 0.78,
        "cost_per_asm": 0.11,
    },
    "PacificStar": {
        "code": "PS",
        "hub": "NRT",
        "routes": ["NRT-JFK", "NRT-LHR", "NRT-SIN", "NRT-SYD", "NRT-LAX"],
        "base_fare_range": (500, 3000),
        "load_factor_mean": 0.75,
        "cost_per_asm": 0.13,
    },
}


def generate_airline_data(airline_name, config, n_records=50, seed=None):
    """Generate confidential route data for one airline."""
    if seed:
        np.random.seed(seed)

    records = []
    for _ in range(n_records):
        route = np.random.choice(config['routes'])
        fare_min, fare_max = config['base_fare_range']

        record = {
            "route": route,
            "avg_fare_usd": round(np.random.uniform(fare_min, fare_max), 2),
            "load_factor": round(np.random.beta(8, 2) * config['load_factor_mean'] / 0.8, 3),
            "cost_per_asm_usd": round(config['cost_per_asm'] + np.random.normal(0, 0.01), 4),
            "weekly_frequency": int(np.random.choice([7, 14, 21, 28])),
            "avg_passengers": int(np.random.uniform(150, 350)),
            "revenue_per_route_k": round(np.random.uniform(200, 1500), 1),
            "profit_margin_pct": round(np.random.uniform(5, 25), 1),
            "competitive_position": np.random.choice(["leader", "challenger", "follower"]),
        }
        records.append(record)

    return records


def create_airline_data():
    """Create data files for all alliance airlines."""
    print(f"""
{BOLD}{BLUE}
{'='*60}
  LAB 10: Creating Alliance Airline Data
{'='*60}
{RESET}
  {CYAN}Creating confidential route data for 3 alliance airlines.
  Each airline's data contains sensitive commercial information
  that must not be shared with partners.{RESET}
""")

    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    all_data = {}
    for i, (name, config) in enumerate(AIRLINES.items()):
        data = generate_airline_data(name, config, n_records=50, seed=42 + i)
        all_data[name] = data

        # Save individual airline data
        filepath = data_dir / f"{name.lower()}_routes.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=True)

        print(f"  {GREEN}[OK]{RESET} {name} ({config['code']})")
        print(f"      Hub: {config['hub']}")
        print(f"      Routes: {len(config['routes'])}")
        print(f"      Records: {len(data)}")
        print(f"      Avg fare range: ${config['base_fare_range'][0]}-${config['base_fare_range'][1]}")
        print(f"      Load factor: {config['load_factor_mean']*100:.0f}%")
        print()

    print(f"  {BOLD}Confidential Data Created:{RESET}")
    print(f"  {'─'*50}")
    print(f"  {RED}Each airline's data contains:{RESET}")
    print(f"    - Exact fare pricing per route")
    print(f"    - Load factors (capacity utilization)")
    print(f"    - Cost per available seat mile")
    print(f"    - Revenue per route")
    print(f"    - Profit margins")
    print(f"    - Competitive positioning")
    print(f"\n  {RED}This data is HIGHLY CONFIDENTIAL.{RESET}")
    print(f"  {RED}Sharing it would destroy competitive advantage.{RESET}")
    print(f"\n  {YELLOW}Next: Run 2_insecure_sharing.py to see the exposure problem.{RESET}\n")


if __name__ == "__main__":
    create_airline_data()
