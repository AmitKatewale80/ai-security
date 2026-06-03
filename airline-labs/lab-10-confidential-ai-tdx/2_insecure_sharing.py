#!/usr/bin/env python3
"""
Lab 10: Insecure Data Sharing - Exposure Problem

Demonstrates how naive data sharing between alliance airlines
exposes each airline's confidential commercial data to partners.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import json
import numpy as np
from pathlib import Path

# Terminal colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'


def load_airline_data():
    """Load all airline data files."""
    data_dir = Path(__file__).parent / "data"
    if not data_dir.exists():
        print(f"  {RED}[FAIL] Data not found. Run 1_airline_data.py first.{RESET}")
        return None

    airlines = {}
    for filepath in sorted(data_dir.glob("*_routes.json")):
        name = filepath.stem.replace("_routes", "").title()
        # Fix multi-word names
        name_map = {"Skywings": "SkyWings", "Euroconnect": "EuroConnect", "Pacificstar": "PacificStar"}
        name = name_map.get(name, name)
        with open(filepath, 'r', encoding='utf-8') as f:
            airlines[name] = json.load(f)
    return airlines


def naive_route_optimization(all_data):
    """
    Naive approach: Combine all data for optimization.
    PROBLEM: Everyone sees everyone's data!
    """
    # Find shared routes
    shared_routes = set()
    route_data = {}

    for airline, records in all_data.items():
        for record in records:
            route = record['route']
            # Normalize route (JFK-LHR == LHR-JFK)
            parts = route.split('-')
            normalized = '-'.join(sorted(parts))
            shared_routes.add(normalized)

            if normalized not in route_data:
                route_data[normalized] = []
            route_data[normalized].append({
                'airline': airline,
                **record
            })

    return route_data


def run_insecure_sharing():
    """Show the data exposure problem."""
    print(f"""
{BOLD}{RED}
{'='*60}
  LAB 10: Insecure Alliance Data Sharing
{'='*60}
{RESET}
  {YELLOW}Scenario: Airlines share data for route optimization.
  Without confidential computing, each airline can see
  all other airlines' sensitive commercial data.{RESET}
""")

    all_data = load_airline_data()
    if not all_data:
        return

    # Combine data (insecure)
    print(f"  {CYAN}Combining airline data for route optimization...{RESET}")
    route_data = naive_route_optimization(all_data)

    # Show what each airline can see
    print(f"\n  {RED}{BOLD}DATA EXPOSURE - What each airline can now see:{RESET}")
    print(f"  {'='*55}")

    # Pick a shared route to demonstrate
    # Find a route that multiple airlines serve
    multi_airline_routes = {
        route: data for route, data in route_data.items()
        if len(set(d['airline'] for d in data)) > 1
    }

    if not multi_airline_routes:
        # Use first route as example
        example_route = list(route_data.keys())[0]
        example_data = route_data[example_route]
    else:
        example_route = list(multi_airline_routes.keys())[0]
        example_data = multi_airline_routes[example_route]

    print(f"\n  {BOLD}Example: Route {example_route}{RESET}")
    print(f"  {'─'*55}")

    for record in example_data[:3]:
        airline = record['airline']
        print(f"\n    {RED}[EXPOSED] {airline}'s Confidential Data:{RESET}")
        print(f"      Avg Fare:        ${record['avg_fare_usd']:.2f}")
        print(f"      Load Factor:     {record['load_factor']*100:.1f}%")
        print(f"      Cost/ASM:        ${record['cost_per_asm_usd']:.4f}")
        print(f"      Revenue/Route:   ${record['revenue_per_route_k']}K")
        print(f"      Profit Margin:   {record['profit_margin_pct']}%")
        print(f"      Position:        {record['competitive_position']}")

    # Show competitive intelligence extracted
    print(f"\n\n  {RED}{BOLD}COMPETITIVE INTELLIGENCE EXTRACTED:{RESET}")
    print(f"  {'='*55}")

    for airline, records in all_data.items():
        fares = [r['avg_fare_usd'] for r in records]
        margins = [r['profit_margin_pct'] for r in records]
        loads = [r['load_factor'] for r in records]

        print(f"\n    {RED}{airline}:{RESET}")
        print(f"      Average fare:    ${np.mean(fares):.0f} (range: ${min(fares):.0f}-${max(fares):.0f})")
        print(f"      Avg margin:      {np.mean(margins):.1f}%")
        print(f"      Avg load factor: {np.mean(loads)*100:.1f}%")
        print(f"      {RED}-> Competitor now knows exact pricing strategy!{RESET}")

    print(f"""
  {BOLD}{'='*55}{RESET}
  {RED}{BOLD}IMPACT OF INSECURE SHARING:{RESET}
  {BOLD}{'='*55}{RESET}

  {RED}[FAIL]{RESET} Each airline sees partners' exact pricing
  {RED}[FAIL]{RESET} Profit margins exposed to competitors
  {RED}[FAIL]{RESET} Load factors reveal demand patterns
  {RED}[FAIL]{RESET} Cost structure enables undercutting
  {RED}[FAIL]{RESET} Competitive positioning revealed

  {BOLD}Business Impact:{RESET}
  - Airlines can undercut each other on shared routes
  - Negotiation leverage destroyed
  - Alliance trust broken
  - Potential antitrust concerns from data sharing

  {GREEN}Run 3_confidential_sharing.py to see TDX-protected sharing.{RESET}
""")


if __name__ == "__main__":
    run_insecure_sharing()
