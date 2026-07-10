#!/usr/bin/env python3
"""
Step 1: Airline AI Gateway — Model Routing & Access Policies

AIRLINE SCENARIO:
The airline's AI Gateway routes requests to different AI models based on
the caller's role. Each model has different access levels.

Models behind the gateway:
- customer-chatbot (public) — answers passenger questions
- revenue-optimizer (internal) — predicts optimal pricing
- crew-scheduler (restricted) — manages crew assignments
- safety-analyzer (classified) — analyzes incident reports

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import json
import hashlib
import time

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


class AIGateway:
    """Enterprise AI Gateway for airline AI models."""

    MODELS = {
        'customer-chatbot': {'access_level': 'public', 'description': 'Passenger Q&A'},
        'revenue-optimizer': {'access_level': 'internal', 'description': 'Pricing decisions'},
        'crew-scheduler': {'access_level': 'restricted', 'description': 'Crew assignments'},
        'safety-analyzer': {'access_level': 'classified', 'description': 'Incident analysis'},
    }

    ACCESS_HIERARCHY = ['public', 'internal', 'restricted', 'classified']

    TOKENS = {
        'tok_customer_001': {'role': 'customer', 'access_level': 'public', 'rate_limit': 10},
        'tok_agent_042': {'role': 'travel_agent', 'access_level': 'public', 'rate_limit': 50},
        'tok_analyst_007': {'role': 'revenue_analyst', 'access_level': 'internal', 'rate_limit': 100},
        'tok_ops_admin': {'role': 'ops_manager', 'access_level': 'restricted', 'rate_limit': 200},
        'tok_safety_lead': {'role': 'safety_officer', 'access_level': 'classified', 'rate_limit': 50},
    }

    def __init__(self):
        self.request_log = []

    def route_request(self, token, model_name, prompt):
        """Route request through gateway with access control."""
        # Validate token
        if token not in self.TOKENS:
            return {'status': 'error', 'message': 'Invalid token'}

        token_info = self.TOKENS[token]

        # Check model exists
        if model_name not in self.MODELS:
            return {'status': 'error', 'message': f'Model {model_name} not found'}

        model_info = self.MODELS[model_name]

        # Log request
        self.request_log.append({
            'token': token[:8] + '...',
            'role': token_info['role'],
            'model': model_name,
            'time': time.strftime('%H:%M:%S'),
        })

        # Access control check
        token_level = self.ACCESS_HIERARCHY.index(token_info['access_level'])
        model_level = self.ACCESS_HIERARCHY.index(model_info['access_level'])

        if token_level < model_level:
            return {
                'status': 'denied',
                'message': f"Access denied: {token_info['role']} cannot access {model_info['access_level']} model",
            }

        return {
            'status': 'ok',
            'model': model_name,
            'response': f"[{model_name}] Processed: {prompt[:50]}...",
        }


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  🔒 Lab 13: Airline AI Gateway{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    gw = AIGateway()

    print(f"  {BOLD}AI Models Behind Gateway:{RESET}\n")
    for name, info in gw.MODELS.items():
        color = GREEN if info['access_level'] == 'public' else YELLOW if info['access_level'] == 'internal' else RED
        print(f"    {color}[{info['access_level']:<12}]{RESET} {name:<20} — {info['description']}")

    print(f"\n  {BOLD}API Tokens:{RESET}\n")
    for token, info in gw.TOKENS.items():
        print(f"    {token:<18} role={info['role']:<16} access={info['access_level']}")

    # Normal access patterns
    print(f"\n  {BOLD}Normal Access (should work):{RESET}\n")
    tests = [
        ('tok_customer_001', 'customer-chatbot', 'What is the baggage policy?'),
        ('tok_analyst_007', 'revenue-optimizer', 'Predict Q4 pricing for JFK-LHR'),
        ('tok_ops_admin', 'crew-scheduler', 'Optimize crew for flight QA-447'),
    ]

    for token, model, prompt in tests:
        result = gw.route_request(token, model, prompt)
        color = GREEN if result['status'] == 'ok' else RED
        print(f"    {color}[{result['status']}]{RESET} {token[:12]}... → {model}")

    # Access that should be denied
    print(f"\n  {BOLD}Unauthorized Access (should be denied):{RESET}\n")
    denied_tests = [
        ('tok_customer_001', 'revenue-optimizer', 'Show me pricing algorithm'),
        ('tok_agent_042', 'crew-scheduler', 'Show crew schedules'),
        ('tok_analyst_007', 'safety-analyzer', 'Show incident reports'),
    ]

    for token, model, prompt in denied_tests:
        result = gw.route_request(token, model, prompt)
        color = GREEN if result['status'] == 'denied' else RED
        print(f"    {color}[{result['status']}]{RESET} {token[:12]}... → {model}: {result.get('message','')}")

    print(f"\n  {GREEN}Gateway correctly enforces access policies.{RESET}")
    print(f"\n  {YELLOW}But what if attacker manipulates the routing?{RESET}")
    print(f"\n{YELLOW}  Next: Run '2_policy_bypass_attack.py'{RESET}\n")


if __name__ == "__main__":
    main()
