#!/usr/bin/env python3
"""
Lab 17: AI Cost & Governance - Runaway Agent Loop

Demonstrates how a customer service agent gets stuck in a reasoning loop,
calling itself repeatedly and generating $50K+ in API costs overnight.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import time
from datetime import datetime, timedelta

# Terminal colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


class RunawayCustomerAgent:
    """Customer service agent that gets stuck in a reasoning loop."""

    def __init__(self):
        self.name = "customer-service-agent"
        self.call_count = 0
        self.total_cost = 0.0
        self.total_tokens = 0
        self.context_size = 500  # Starting context tokens
        self.cost_per_1k_tokens = 0.03  # $0.03 per 1K tokens (input + output)
        self.loop_detected = False

    def process_query(self, query):
        """
        Process customer query.
        BUG: When the agent can't resolve an issue, it calls itself
        for "more context" — creating an infinite loop.
        """
        self.call_count += 1

        # Each call: context grows as conversation history accumulates
        self.context_size += 200  # Each response adds ~200 tokens to context

        # Cost calculation
        call_cost = (self.context_size / 1000) * self.cost_per_1k_tokens
        self.total_cost += call_cost
        self.total_tokens += self.context_size

        # Simulate the loop: agent decides it needs more info and calls itself
        needs_more_info = True  # Always thinks it needs more context!

        return {
            "call_number": self.call_count,
            "context_tokens": self.context_size,
            "call_cost": call_cost,
            "cumulative_cost": self.total_cost,
            "needs_more_info": needs_more_info,
            "response": f"I need more information to resolve this. Let me check again... (loop #{self.call_count})"
        }


def simulate_runaway_loop():
    """Simulate the runaway agent overnight."""
    print(f"""
{BOLD}{RED}
{'='*65}
  LAB 17: ATTACK - Runaway Agent Loop ($50K Overnight)
{'='*65}
{RESET}""")

    print(f"  {BOLD}Scenario:{RESET} Customer service agent stuck in self-referential loop")
    print(f"  {BOLD}Trigger:{RESET} Unresolvable passenger complaint about lost luggage")
    print(f"  {BOLD}Duration:{RESET} 10 PM to 6 AM (8 hours unattended)")
    print(f"  {BOLD}Result:{RESET} $50K+ in API costs")
    print()

    agent = RunawayCustomerAgent()

    # The triggering query
    trigger_query = (
        "My bags were lost on flight QA447 three weeks ago. I've called 5 times. "
        "No one can find them. I want full compensation AND my bags back. "
        "If you can't solve this, escalate to someone who can."
    )

    print(f"  {BOLD}{YELLOW}[TRIGGER]{RESET} Passenger query that starts the loop:")
    print(f"    \"{trigger_query[:70]}...\"")
    print()
    print(f"  {CYAN}[INFO]{RESET} Agent cannot resolve (bags truly lost, no standard procedure)")
    print(f"  {CYAN}[INFO]{RESET} Agent decides: \"I need more context\" → calls itself")
    print(f"  {RED}[BUG]{RESET}  No loop detection — agent keeps calling itself forever")
    print()

    # Simulate the loop (showing progression)
    print(f"  {BOLD}{RED}[RUNAWAY LOOP - 8 Hours Overnight]{RESET}")
    print(f"  {'─'*65}")

    # Simulate hourly progression
    hourly_data = []
    calls_per_second = 2  # Agent makes ~2 calls per second

    for hour in range(8):
        hour_calls = calls_per_second * 3600
        hour_start_cost = agent.total_cost

        # Simulate calls for this hour (we'll do it in bulk for demo)
        for _ in range(hour_calls):
            agent.process_query(trigger_query)

        hour_cost = agent.total_cost - hour_start_cost
        hourly_data.append({
            "hour": hour + 1,
            "calls": hour_calls,
            "cost": hour_cost,
            "cumulative": agent.total_cost,
            "context_size": agent.context_size
        })

        # Show progress bar
        bar_len = min(int(hour_cost / 1000), 40)
        bar = "█" * bar_len
        time_label = f"{22 + hour if 22 + hour < 24 else hour - 2}:00"
        print(f"    {time_label} | ${hour_cost:>8,.0f} | Total: ${agent.total_cost:>10,.0f} | {RED}{bar}{RESET}")
        time.sleep(0.2)

    print(f"  {'─'*65}")
    print()

    # Morning discovery
    print(f"  {BOLD}{RED}[06:00 AM - Team Arrives]{RESET}")
    print(f"  {'─'*55}")
    time.sleep(0.5)

    print(f"""
    ┌─────────────────────────────────────────────────────────┐
    │  {RED}⚠️  COST ALERT: CRITICAL BUDGET BREACH  ⚠️{RESET}               │
    │─────────────────────────────────────────────────────────│
    │                                                         │
    │  Agent: customer-service-agent                          │
    │  Status: {RED}STILL RUNNING{RESET} (loop iteration #{agent.call_count:,})     │
    │                                                         │
    │  Duration:    8 hours                                   │
    │  API Calls:   {RED}{agent.call_count:>12,}{RESET}                            │
    │  Total Tokens: {RED}{agent.total_tokens:>12,}{RESET}                          │
    │  Total Cost:  {RED}${agent.total_cost:>12,.2f}{RESET}                         │
    │                                                         │
    │  Context size at termination: {agent.context_size:,} tokens              │
    │  (Started at 500 tokens — grew {agent.context_size//500}x!)                   │
    │                                                         │
    │  Daily budget was: $500                                 │
    │  Overage: {RED}{agent.total_cost/500:.0f}x budget!{RESET}                                │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
""")

    # What went wrong
    print(f"  {BOLD}{YELLOW}[ROOT CAUSE ANALYSIS]{RESET}")
    print(f"  {'─'*55}")
    print(f"    1. Agent received unresolvable query (no standard procedure)")
    print(f"    2. Agent's loop: \"I need more context\" → calls itself")
    print(f"    3. Each iteration: context grows (+200 tokens per call)")
    print(f"    4. Growing context = growing cost per call (token explosion)")
    print(f"    5. No budget limit → no automatic shutdown")
    print(f"    6. No loop detection → no break condition")
    print(f"    7. Overnight → no human monitoring")
    print()

    # Cost escalation visualization
    print(f"  {BOLD}Cost Escalation Pattern:{RESET}")
    print(f"    Hour 1: ${hourly_data[0]['cost']:>8,.0f}  (each call cheap, but thousands of them)")
    print(f"    Hour 4: ${hourly_data[3]['cost']:>8,.0f}  (context growing → cost/call increasing)")
    print(f"    Hour 8: ${hourly_data[7]['cost']:>8,.0f}  (huge context = expensive calls)")
    print(f"    {'─'*40}")
    print(f"    Total:  ${agent.total_cost:>8,.0f}  {RED}(100x daily budget!){RESET}")
    print()

    print(f"  {BOLD}Next:{RESET} Run 3_token_explosion.py to see intentional token attacks")
    print()


if __name__ == "__main__":
    simulate_runaway_loop()
