#!/usr/bin/env python3
"""
Lab 23: AI Cost & Governance - Defense: Budgets, Loop Detection, Shutdown

Demonstrates governance controls that prevent runaway costs:
1. Per-agent budgets (hard limits)
2. Loop detection (self-referential call patterns)
3. Automatic shutdown (kill agent on budget breach)
4. Token monitoring (alert on abnormal context growth)
5. Governance dashboard (real-time visibility)

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import time
from datetime import datetime

# Terminal colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


class AgentBudget:
    """Per-agent budget enforcement."""

    def __init__(self, agent_name, hourly_limit, daily_limit, max_tokens_per_call):
        self.agent_name = agent_name
        self.hourly_limit = hourly_limit
        self.daily_limit = daily_limit
        self.max_tokens_per_call = max_tokens_per_call
        self.hourly_spent = 0.0
        self.daily_spent = 0.0
        self.is_active = True

    def check_budget(self, estimated_cost, token_count):
        """Check if call is within budget."""
        if not self.is_active:
            return {"allowed": False, "reason": "Agent SHUTDOWN - budget exhausted"}

        if token_count > self.max_tokens_per_call:
            return {"allowed": False, "reason": f"Token count {token_count:,} exceeds max {self.max_tokens_per_call:,}"}

        if self.hourly_spent + estimated_cost > self.hourly_limit:
            self.is_active = False
            return {"allowed": False, "reason": f"Hourly budget exceeded (${self.hourly_limit:.2f})"}

        if self.daily_spent + estimated_cost > self.daily_limit:
            self.is_active = False
            return {"allowed": False, "reason": f"Daily budget exceeded (${self.daily_limit:.2f})"}

        return {"allowed": True, "reason": "Within budget"}

    def record_spend(self, cost):
        """Record spending."""
        self.hourly_spent += cost
        self.daily_spent += cost


class LoopDetector:
    """Detects self-referential agent call patterns."""

    def __init__(self, max_similar_calls=5, window_seconds=60):
        self.call_history = []
        self.max_similar_calls = max_similar_calls
        self.window_seconds = window_seconds
        self.loop_detected = False

    def record_call(self, agent_name, query_hash, timestamp):
        """Record a call and check for loops."""
        self.call_history.append({
            "agent": agent_name,
            "query_hash": query_hash,
            "timestamp": timestamp
        })

        # Check for repeated similar queries in time window
        recent = [c for c in self.call_history[-20:] if c["agent"] == agent_name]
        if len(recent) >= self.max_similar_calls:
            # Check if queries are similar (same hash pattern)
            hashes = [c["query_hash"] for c in recent[-self.max_similar_calls:]]
            unique_hashes = set(hashes)
            if len(unique_hashes) <= 2:  # Almost all queries are the same
                self.loop_detected = True
                return {
                    "loop_detected": True,
                    "pattern": f"{len(recent)} similar calls in window",
                    "action": "SHUTDOWN_AGENT"
                }

        return {"loop_detected": False}


class TokenMonitor:
    """Monitors token usage and detects anomalies."""

    def __init__(self, baseline_tokens=1000, alert_multiplier=5):
        self.baseline_tokens = baseline_tokens
        self.alert_multiplier = alert_multiplier
        self.history = []

    def check_tokens(self, token_count):
        """Check if token count is anomalous."""
        self.history.append(token_count)

        if token_count > self.baseline_tokens * self.alert_multiplier:
            return {
                "anomaly": True,
                "severity": "HIGH",
                "token_count": token_count,
                "baseline": self.baseline_tokens,
                "multiplier": token_count / self.baseline_tokens,
                "action": "BLOCK_AND_ALERT"
            }
        elif token_count > self.baseline_tokens * 2:
            return {
                "anomaly": True,
                "severity": "MEDIUM",
                "token_count": token_count,
                "action": "ALERT"
            }
        return {"anomaly": False}


class GovernanceDashboard:
    """Real-time governance dashboard."""

    def __init__(self):
        self.events = []
        self.shutdowns = []
        self.alerts = []

    def log_event(self, event_type, agent, details):
        """Log governance event."""
        event = {
            "type": event_type,
            "agent": agent,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.events.append(event)
        if event_type == "SHUTDOWN":
            self.shutdowns.append(event)
        elif event_type in ["ALERT", "BUDGET_BREACH", "LOOP_DETECTED"]:
            self.alerts.append(event)


def main():
    """Demonstrate governance defense mechanisms."""
    print(f"""
{BOLD}{GREEN}
{'='*65}
  LAB 23: DEFENSE - AI Cost Governance & Controls
{'='*65}
{RESET}""")

    print(f"  {BOLD}Defense Layers:{RESET}")
    print(f"    1. Per-agent budget limits (hard caps)")
    print(f"    2. Loop detection (break infinite loops)")
    print(f"    3. Token monitoring (detect explosions)")
    print(f"    4. Automatic shutdown (prevent cost bleed)")
    print(f"    5. Governance dashboard (real-time visibility)")
    print()

    dashboard = GovernanceDashboard()

    # ═══════════════════════════════════════════════════════
    # Defense 1: Per-Agent Budgets
    # ═══════════════════════════════════════════════════════
    print(f"  {BOLD}{CYAN}[DEFENSE 1] Per-Agent Budget Enforcement{RESET}")
    print(f"  {'─'*55}")
    time.sleep(0.3)

    budgets = {
        "customer-service-agent": AgentBudget("customer-service-agent",
                                              hourly_limit=10.0, daily_limit=100.0,
                                              max_tokens_per_call=4000),
        "ops-analytics-agent": AgentBudget("ops-analytics-agent",
                                           hourly_limit=20.0, daily_limit=200.0,
                                           max_tokens_per_call=8000),
        "revenue-agent": AgentBudget("revenue-agent",
                                     hourly_limit=15.0, daily_limit=150.0,
                                     max_tokens_per_call=6000),
    }

    print(f"\n    Budget Configuration:")
    print(f"    {'Agent':<28} {'$/Hour':<10} {'$/Day':<10} {'Max Tokens':<12}")
    print(f"    {'─'*60}")
    for name, budget in budgets.items():
        print(f"    {name:<28} ${budget.hourly_limit:<9.2f} ${budget.daily_limit:<9.2f} {budget.max_tokens_per_call:,}")

    # Simulate runaway being stopped
    print(f"\n    {BOLD}Simulating runaway agent...{RESET}")
    cs_budget = budgets["customer-service-agent"]
    calls_made = 0
    while cs_budget.is_active:
        cost = 0.03
        check = cs_budget.check_budget(cost, 1000)
        if check["allowed"]:
            cs_budget.record_spend(cost)
            calls_made += 1
        else:
            print(f"    {GREEN}⛔ STOPPED after {calls_made} calls (${cs_budget.hourly_spent:.2f}){RESET}")
            print(f"    Reason: {check['reason']}")
            dashboard.log_event("SHUTDOWN", "customer-service-agent", check["reason"])
            break

    print(f"\n    {GREEN}Without budget: Agent would have made 57,600 calls ($50K+)")
    print(f"    With budget:  Agent stopped at {calls_made} calls (${cs_budget.hourly_spent:.2f}){RESET}")
    print()

    # ═══════════════════════════════════════════════════════
    # Defense 2: Loop Detection
    # ═══════════════════════════════════════════════════════
    print(f"  {BOLD}{CYAN}[DEFENSE 2] Loop Detection{RESET}")
    print(f"  {'─'*55}")
    time.sleep(0.3)

    detector = LoopDetector(max_similar_calls=5, window_seconds=60)

    print(f"\n    Monitoring for self-referential call patterns...")
    print(f"    Threshold: {detector.max_similar_calls} similar calls = loop detected")
    print()

    # Simulate loop
    for i in range(7):
        # Same query hash = agent asking itself the same question
        result = detector.record_call("customer-service-agent", "hash_abc123", datetime.now())
        status = f"{GREEN}OK{RESET}" if not result.get("loop_detected") else f"{RED}LOOP!{RESET}"
        print(f"      Call {i+1}: [{status}] query_hash=abc123...")

        if result.get("loop_detected"):
            print(f"\n    {GREEN}⛔ LOOP DETECTED at call #{i+1}{RESET}")
            print(f"    Pattern: {result['pattern']}")
            print(f"    Action: {result['action']}")
            dashboard.log_event("LOOP_DETECTED", "customer-service-agent", result["pattern"])
            break
        time.sleep(0.1)
    print()

    # ═══════════════════════════════════════════════════════
    # Defense 3: Token Monitoring
    # ═══════════════════════════════════════════════════════
    print(f"  {BOLD}{CYAN}[DEFENSE 3] Token Explosion Detection{RESET}")
    print(f"  {'─'*55}")
    time.sleep(0.3)

    monitor = TokenMonitor(baseline_tokens=1000, alert_multiplier=5)

    print(f"\n    Baseline: ~1000 tokens per call")
    print(f"    Alert threshold: 5x baseline (5000 tokens)")
    print()

    test_calls = [
        (800, "Normal passenger query"),
        (1200, "Slightly longer query"),
        (950, "Standard rebooking request"),
        (50000, "TOKEN EXPLOSION — injected context!"),
        (120000, "MASSIVE INJECTION — full document embedded"),
    ]

    for tokens, desc in test_calls:
        result = monitor.check_tokens(tokens)
        if result.get("anomaly"):
            severity_color = RED if result["severity"] == "HIGH" else YELLOW
            print(f"    [{severity_color}{result['severity']}{RESET}] {tokens:>7,} tokens — {desc}")
            print(f"          Action: {RED}{result['action']}{RESET} ({result.get('multiplier', 0):.0f}x baseline)")
            dashboard.log_event("ALERT", "customer-service-agent", f"Token anomaly: {tokens:,}")
        else:
            print(f"    [{GREEN}OK{RESET}]   {tokens:>7,} tokens — {desc}")
        time.sleep(0.1)
    print()

    # ═══════════════════════════════════════════════════════
    # Defense 4: Automatic Shutdown
    # ═══════════════════════════════════════════════════════
    print(f"  {BOLD}{CYAN}[DEFENSE 4] Automatic Shutdown Triggers{RESET}")
    print(f"  {'─'*55}")
    time.sleep(0.3)

    shutdown_triggers = [
        ("Budget exceeded", "Agent hourly/daily limit hit", "Immediate kill"),
        ("Loop detected", "5+ identical calls in 60 seconds", "Kill + alert team"),
        ("Token explosion", "5x baseline tokens in single call", "Block call + alert"),
        ("Error rate spike", ">50% calls failing in 5 minutes", "Pause + investigate"),
        ("Cost velocity", "Cost growing >10x normal rate", "Throttle → kill"),
    ]

    print(f"\n    {'Trigger':<20} {'Condition':<35} {'Action':<20}")
    print(f"    {'─'*75}")
    for trigger, condition, action in shutdown_triggers:
        print(f"    {trigger:<20} {condition:<35} {GREEN}{action}{RESET}")
    print()

    # ═══════════════════════════════════════════════════════
    # Defense 5: Governance Dashboard
    # ═══════════════════════════════════════════════════════
    print(f"  {BOLD}{CYAN}[DEFENSE 5] Governance Dashboard{RESET}")
    print(f"  {'─'*55}")
    time.sleep(0.3)

    print(f"""
    ┌─────────────────────────────────────────────────────────┐
    │  {GREEN}AI GOVERNANCE DASHBOARD{RESET} - {datetime.now().strftime('%Y-%m-%d %H:%M')}            │
    │─────────────────────────────────────────────────────────│
    │                                                         │
    │  {BOLD}Agent Status:{RESET}                                          │
    │    customer-service-agent  {RED}[SHUTDOWN]{RESET} Budget exceeded    │
    │    ops-analytics-agent     {GREEN}[ACTIVE]{RESET}   $3.42 this hour   │
    │    revenue-agent           {GREEN}[ACTIVE]{RESET}   $2.18 this hour   │
    │                                                         │
    │  {BOLD}Alerts:{RESET}                                                 │
    │    {RED}●{RESET} Loop detected: customer-service-agent (5 min ago) │
    │    {RED}●{RESET} Token anomaly: 50,000 tokens blocked (3 min ago)  │
    │    {YELLOW}●{RESET} Budget warning: revenue-agent at 80% hourly       │
    │                                                         │
    │  {BOLD}Today's Stats:{RESET}                                          │
    │    Total spend:    $48.72 / $500.00 budget              │
    │    Calls made:     4,231                                │
    │    Calls blocked:  47 (budget/loop/token)               │
    │    Shutdowns:      1                                    │
    │                                                         │
    │  {BOLD}Audit Trail:{RESET} {GREEN}Complete{RESET} — all calls logged with agent ID   │
    └─────────────────────────────────────────────────────────┘
""")

    # Final comparison
    print(f"""
  {GREEN}{BOLD}╔══════════════════════════════════════════════════════════════╗
  ║          ✅ GOVERNANCE CONTROLS ACTIVE                       ║
  ╠══════════════════════════════════════════════════════════════╣
  ║                                                             ║
  ║  Without governance (Lab scenario):                         ║
  ║    • Runaway loop: $50,000+ overnight                       ║
  ║    • Token explosion: $50,000+ per weekend                  ║
  ║    • No audit trail, no visibility                          ║
  ║    • Discovery: next morning (8+ hours)                     ║
  ║                                                             ║
  ║  With governance (this defense):                            ║
  ║    • Budget limit hit: agent stopped at $10                 ║
  ║    • Loop detected: agent killed after 5 calls             ║
  ║    • Token explosion: blocked before processing             ║
  ║    • Full audit trail with per-agent attribution            ║
  ║    • Discovery: immediate (real-time dashboard)             ║
  ║                                                             ║
  ║  Cost savings: ~$99,990 prevented                           ║
  ║                                                             ║
  ╚══════════════════════════════════════════════════════════════╝{RESET}
""")

    print(f"  {BOLD}Key Takeaway:{RESET}")
    print(f"  AI agents without budget controls are an open credit card.")
    print(f"  Per-agent budgets, loop detection, and automatic shutdown")
    print(f"  are not optional — they're critical governance requirements.")
    print()


if __name__ == "__main__":
    main()
