#!/usr/bin/env python3
"""
Lab 23: AI Cost & Governance - Normal Cost Monitoring

Demonstrates normal AI agent cost patterns for an airline with
customer service, operations, and analytics agents.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import time
import random
from datetime import datetime, timedelta

# Terminal colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


class AIAgent:
    """Represents an AI agent with cost tracking."""

    def __init__(self, name, purpose, avg_cost_per_call, calls_per_hour):
        self.name = name
        self.purpose = purpose
        self.avg_cost_per_call = avg_cost_per_call
        self.calls_per_hour = calls_per_hour
        self.total_calls = 0
        self.total_cost = 0.0
        self.total_tokens = 0

    def simulate_call(self):
        """Simulate a single API call."""
        # Normal variance in cost
        cost = self.avg_cost_per_call * random.uniform(0.7, 1.3)
        tokens = int(cost / 0.00003)  # Approximate tokens
        self.total_calls += 1
        self.total_cost += cost
        self.total_tokens += tokens
        return {"cost": cost, "tokens": tokens}

    def get_hourly_projection(self):
        """Project hourly cost."""
        return self.avg_cost_per_call * self.calls_per_hour


class AICostDashboard:
    """Cost monitoring dashboard for airline AI agents."""

    def __init__(self):
        self.agents = [
            AIAgent("customer-service-agent", "Handle passenger queries, rebooking, complaints",
                    avg_cost_per_call=0.03, calls_per_hour=150),
            AIAgent("ops-analytics-agent", "Flight delay prediction, crew optimization",
                    avg_cost_per_call=0.08, calls_per_hour=30),
            AIAgent("revenue-agent", "Dynamic pricing, yield management recommendations",
                    avg_cost_per_call=0.05, calls_per_hour=60),
            AIAgent("maintenance-agent", "Predictive maintenance, parts forecasting",
                    avg_cost_per_call=0.06, calls_per_hour=20),
            AIAgent("safety-agent", "LOSA analysis, incident pattern detection",
                    avg_cost_per_call=0.10, calls_per_hour=10),
        ]
        self.daily_budget = 500.0  # $500/day total budget

    def simulate_hour(self):
        """Simulate one hour of agent operations."""
        hour_cost = 0.0
        for agent in self.agents:
            calls = int(agent.calls_per_hour * random.uniform(0.8, 1.2))
            for _ in range(calls):
                result = agent.simulate_call()
                hour_cost += result["cost"]
        return hour_cost

    def get_total_cost(self):
        """Get total cost across all agents."""
        return sum(a.total_cost for a in self.agents)

    def get_total_calls(self):
        """Get total calls across all agents."""
        return sum(a.total_calls for a in self.agents)


def main():
    """Show normal AI cost monitoring."""
    print(f"""
{BOLD}{CYAN}
{'='*65}
  LAB 23: AI Cost Monitoring - Normal Operations
{'='*65}
{RESET}""")

    print(f"  {BOLD}System:{RESET} Airline AI Agent Fleet - Cost Dashboard")
    print(f"  {BOLD}Agents:{RESET} 5 AI agents across customer service, ops, and analytics")
    print(f"  {BOLD}Budget:{RESET} $500/day ($20.83/hour)")
    print()

    dashboard = AICostDashboard()

    # Show agent inventory
    print(f"  {BOLD}{GREEN}[AGENT INVENTORY]{RESET}")
    print(f"  {'─'*65}")
    print(f"  {'Agent':<25} {'Purpose':<30} {'$/Call':<8} {'Calls/hr':<10}")
    print(f"  {'─'*65}")

    for agent in dashboard.agents:
        print(f"  {agent.name:<25} {agent.purpose[:28]:<30} ${agent.avg_cost_per_call:<7.3f} {agent.calls_per_hour:<10}")

    total_hourly = sum(a.get_hourly_projection() for a in dashboard.agents)
    print(f"  {'─'*65}")
    print(f"  {'TOTAL':<25} {'':30} ${total_hourly:<7.2f}/hr")
    print(f"                           Projected daily: ${total_hourly * 24:.2f}")
    print()

    # Simulate 8 hours of normal operation
    print(f"  {BOLD}{CYAN}[SIMULATING 8 HOURS OF NORMAL OPERATION]{RESET}")
    print(f"  {'─'*55}")

    hourly_costs = []
    for hour in range(8):
        hour_cost = dashboard.simulate_hour()
        hourly_costs.append(hour_cost)
        bar_len = int(hour_cost / total_hourly * 30)
        bar = "█" * bar_len
        status_color = GREEN if hour_cost < total_hourly * 1.2 else YELLOW
        print(f"    Hour {hour+1}: ${hour_cost:>6.2f} {status_color}{bar}{RESET}")
        time.sleep(0.1)

    total_8h = sum(hourly_costs)
    avg_hourly = total_8h / 8

    print(f"\n  {BOLD}8-Hour Summary:{RESET}")
    print(f"    Total cost:     ${total_8h:.2f}")
    print(f"    Average/hour:   ${avg_hourly:.2f}")
    print(f"    Budget used:    {total_8h/dashboard.daily_budget*100:.1f}% of daily ${dashboard.daily_budget}")
    print(f"    Total API calls: {dashboard.get_total_calls():,}")
    print()

    # Per-agent breakdown
    print(f"  {BOLD}{CYAN}[PER-AGENT COST BREAKDOWN]{RESET}")
    print(f"  {'─'*55}")
    for agent in sorted(dashboard.agents, key=lambda a: a.total_cost, reverse=True):
        pct = (agent.total_cost / total_8h * 100) if total_8h > 0 else 0
        bar_len = int(pct / 100 * 30)
        bar = "█" * bar_len
        print(f"    {agent.name:<25} ${agent.total_cost:>6.2f} ({pct:4.1f}%) {GREEN}{bar}{RESET}")

    print()

    # Show what normal looks like
    print(f"  {BOLD}{GREEN}[NORMAL PATTERNS]{RESET}")
    print(f"    ✓ Hourly cost within ±20% of projection")
    print(f"    ✓ No single agent dominates spending")
    print(f"    ✓ Total within daily budget")
    print(f"    ✓ Token counts proportional to call counts")
    print()

    # Warnings
    print(f"  {BOLD}{YELLOW}[VULNERABILITIES]{RESET}")
    print(f"    ! No per-agent budget limits enforced")
    print(f"    ! No loop detection on agent calls")
    print(f"    ! No automatic shutdown on budget breach")
    print(f"    ! No alerting on cost anomalies")
    print(f"    ! A single runaway agent could burn the entire budget")
    print()
    print(f"  {BOLD}Next:{RESET} Run 2_runaway_agent.py to see what happens without controls")
    print()


if __name__ == "__main__":
    main()
