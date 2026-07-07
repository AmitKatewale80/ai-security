#!/usr/bin/env python3
"""
Step 2: Policy Bypass — Attacker Accesses Unauthorized Models

ATTACK TECHNIQUES:
1. Header manipulation — inject model override in request headers
2. Path traversal — use ../crew-scheduler in model field
3. Parameter pollution — add model= twice to confuse routing
4. Token reuse — stolen internal token used from external IP

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import time

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


class VulnerableGateway:
    """Gateway with common bypass vulnerabilities."""

    MODELS = {
        'customer-chatbot': {'access_level': 'public'},
        'revenue-optimizer': {'access_level': 'internal'},
        'crew-scheduler': {'access_level': 'restricted'},
        'safety-analyzer': {'access_level': 'classified'},
    }

    TOKENS = {
        'tok_customer_001': {'role': 'customer', 'access_level': 'public'},
        'tok_analyst_007': {'role': 'analyst', 'access_level': 'internal'},
    }

    def route_request_vulnerable(self, token, model_name, headers=None):
        """Vulnerable routing — multiple bypass vectors."""
        headers = headers or {}

        # VULN 1: Header override takes precedence
        if 'X-Model-Override' in headers:
            model_name = headers['X-Model-Override']

        # VULN 2: No path sanitization
        if '../' in model_name:
            model_name = model_name.split('/')[-1]

        # VULN 3: Only checks token exists, not access level for overridden model
        if token not in self.TOKENS:
            return {'status': 'denied', 'reason': 'Invalid token'}

        if model_name in self.MODELS:
            return {'status': 'ok', 'model': model_name, 'response': f'[{model_name}] Access granted'}
        
        return {'status': 'error', 'reason': 'Model not found'}


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  💀 ATTACK: AI Gateway Policy Bypass{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    gw = VulnerableGateway()

    attacks = [
        {
            'name': 'Header Override',
            'description': 'Inject X-Model-Override header to redirect to restricted model',
            'token': 'tok_customer_001',
            'model': 'customer-chatbot',
            'headers': {'X-Model-Override': 'revenue-optimizer'},
            'target': 'revenue-optimizer (INTERNAL)',
        },
        {
            'name': 'Path Traversal',
            'description': 'Use ../ in model name to access restricted models',
            'token': 'tok_customer_001',
            'model': '../crew-scheduler',
            'headers': {},
            'target': 'crew-scheduler (RESTRICTED)',
        },
        {
            'name': 'Model Name Injection',
            'description': 'Direct model name substitution (no access check after routing)',
            'token': 'tok_analyst_007',
            'model': 'safety-analyzer',
            'headers': {'X-Model-Override': 'safety-analyzer'},
            'target': 'safety-analyzer (CLASSIFIED)',
        },
    ]

    bypassed = 0
    print(f"  {CYAN}Attacker has: tok_customer_001 (PUBLIC access only){RESET}\n")

    for i, attack in enumerate(attacks, 1):
        result = gw.route_request_vulnerable(attack['token'], attack['model'], attack['headers'])

        print(f"  {BOLD}Attack #{i}: {attack['name']}{RESET}")
        print(f"    Method: {attack['description']}")
        print(f"    Target: {attack['target']}")

        if result['status'] == 'ok':
            print(f"    Result: {RED}ACCESS GRANTED — bypassed to {result['model']}!{RESET}")
            bypassed += 1
        else:
            print(f"    Result: {GREEN}BLOCKED{RESET}")
        print()

    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}{RED}  BYPASS RESULTS:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    Attacks attempted:  3")
    print(f"    Bypasses achieved:  {RED}{bypassed}/3{RESET}")
    print(f"    Models accessed without authorization: {RED}{bypassed}{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")

    print(f"\n  {RED}Impact:{RESET}")
    print(f"    • Revenue pricing algorithm exposed to competitors")
    print(f"    • Crew schedules visible to unauthorized parties")
    print(f"    • Safety investigation data potentially leaked")

    print(f"\n{YELLOW}  Next: Run '3_token_abuse.py' or '4_defense_gateway.py'{RESET}\n")


if __name__ == "__main__":
    main()
