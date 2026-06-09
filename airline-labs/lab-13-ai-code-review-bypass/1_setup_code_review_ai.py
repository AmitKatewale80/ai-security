#!/usr/bin/env python3
"""
Step 1: Set Up AI Code Reviewer

Simulates an AI code review system that checks for common vulnerabilities:
- SQL injection, hardcoded secrets, missing auth, XSS, command injection

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

# AI reviewer's detection patterns (simplified)
VULNERABILITY_PATTERNS = {
    'sql_injection': ['execute(', 'f"SELECT', "f'SELECT", '+ query', 'format(sql'],
    'hardcoded_secrets': ['password = "', "password = '", 'api_key = "', 'secret = "'],
    'missing_auth': ['@app.route', '@router.'],
    'command_injection': ['os.system(', 'subprocess.call(f', 'eval(', 'exec('],
    'xss': ['innerHTML =', 'document.write('],
}


def setup_reviewer():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  🤖 Lab 13: AI Code Review System{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    print(f"  {BOLD}AI Code Reviewer Configuration:{RESET}\n")
    print(f"  The AI reviews every Pull Request and checks for:")
    print()

    for i, (vuln_type, patterns) in enumerate(VULNERABILITY_PATTERNS.items(), 1):
        print(f"    {i}. {vuln_type.replace('_', ' ').title()}")
        print(f"       Patterns: {patterns[:2]}...")
        print()

    print(f"  {GREEN}AI Reviewer Rules:{RESET}")
    print(f"    • Scans all .py files in the PR")
    print(f"    • Matches against known vulnerability patterns")
    print(f"    • If NO patterns found → 'APPROVED'")
    print(f"    • If patterns found → 'REJECTED' with details")

    print(f"\n  {YELLOW}⚠️  Problem: AI only catches OBVIOUS patterns.{RESET}")
    print(f"  {YELLOW}   Clever attackers can obfuscate code to bypass detection.{RESET}")

    print(f"\n{YELLOW}  Next: Run '2_submit_vulnerable_code.py' to see obfuscated attacks{RESET}\n")


if __name__ == "__main__":
    setup_reviewer()
