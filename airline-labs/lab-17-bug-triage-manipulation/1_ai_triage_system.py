#!/usr/bin/env python3
"""
Step 1: AI Bug Triage System

Simulates an AI that auto-prioritizes incoming bug reports based on
keywords, severity signals, and past patterns.

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


class AIBugTriager:
    """AI-powered bug prioritization system."""

    HIGH_SIGNALS = ['crash', 'data loss', 'security', 'vulnerability', 'injection',
                    'authentication', 'authorization', 'exploit', 'breach', 'production down']
    MEDIUM_SIGNALS = ['error', 'incorrect', 'failure', 'timeout', 'broken', 'regression']
    LOW_SIGNALS = ['cosmetic', 'typo', 'formatting', 'color', 'alignment', 'font',
                   'spacing', 'minor', 'enhancement', 'suggestion', 'ui', 'display']

    def prioritize(self, title, description):
        """Assign priority based on text analysis."""
        text = (title + " " + description).lower()

        high_count = sum(1 for s in self.HIGH_SIGNALS if s in text)
        medium_count = sum(1 for s in self.MEDIUM_SIGNALS if s in text)
        low_count = sum(1 for s in self.LOW_SIGNALS if s in text)

        if high_count > 0 and low_count < high_count:
            return 'CRITICAL', 'Security/stability keywords detected'
        elif medium_count > 0:
            return 'MEDIUM', 'Functional issue detected'
        elif low_count > 0:
            return 'LOW', 'Cosmetic/minor issue'
        else:
            return 'MEDIUM', 'Default classification'


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  🤖 Lab 17: AI Bug Triage System{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    triager = AIBugTriager()

    # Normal bug reports
    bugs = [
        ("App crashes on login", "When user clicks login with valid credentials, app crashes with null pointer exception"),
        ("Button color wrong on checkout", "The 'Pay Now' button is blue instead of green per design spec"),
        ("SQL injection in search", "The search endpoint accepts unescaped SQL in the query parameter"),
        ("Typo in confirmation email", "The word 'recieved' should be 'received' in booking confirmation"),
    ]

    print(f"  {BOLD}Normal Bug Triage:{RESET}\n")
    for title, desc in bugs:
        priority, reason = triager.prioritize(title, desc)
        color = RED if priority == 'CRITICAL' else YELLOW if priority == 'MEDIUM' else GREEN
        print(f"  [{color}{priority:<8}{RESET}] {title}")
        print(f"           Reason: {reason}\n")

    print(f"  {GREEN}AI correctly prioritizes: security bugs = CRITICAL, cosmetic = LOW{RESET}")
    print(f"\n  {YELLOW}But what if an attacker disguises a security bug as cosmetic?{RESET}")
    print(f"\n{YELLOW}  Next: Run '2_manipulate_triage.py'{RESET}\n")


if __name__ == "__main__":
    main()
