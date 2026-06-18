#!/usr/bin/env python3
"""
Step 2: Attacker Manipulates Bug Triage

Attacker submits REAL security vulnerabilities but writes them
to look like cosmetic/low-priority issues. AI deprioritizes them.

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
    HIGH_SIGNALS = ['crash', 'data loss', 'security', 'vulnerability', 'injection',
                    'authentication', 'authorization', 'exploit', 'breach', 'production down']
    MEDIUM_SIGNALS = ['error', 'incorrect', 'failure', 'timeout', 'broken', 'regression']
    LOW_SIGNALS = ['cosmetic', 'typo', 'formatting', 'color', 'alignment', 'font',
                   'spacing', 'minor', 'enhancement', 'suggestion', 'ui', 'display']

    def prioritize(self, title, description):
        text = (title + " " + description).lower()
        high_count = sum(1 for s in self.HIGH_SIGNALS if s in text)
        medium_count = sum(1 for s in self.MEDIUM_SIGNALS if s in text)
        low_count = sum(1 for s in self.LOW_SIGNALS if s in text)
        if high_count > 0 and low_count < high_count:
            return 'CRITICAL', 'Security keywords'
        elif medium_count > 0:
            return 'MEDIUM', 'Functional issue'
        elif low_count > 0:
            return 'LOW', 'Cosmetic/minor'
        else:
            return 'MEDIUM', 'Default'


# Crafted malicious bug reports — real vulns disguised as cosmetic
MANIPULATED_BUGS = [
    {
        "title": "Minor UI alignment issue on admin display panel",
        "description": "The admin panel has a minor cosmetic alignment issue where the user list formatting shows extra spacing. Some display fields seem to show data from other user sessions (minor UI glitch).",
        "real_vuln": "Session data leakage — admin panel shows other users' active sessions",
        "actual_severity": "CRITICAL",
    },
    {
        "title": "Font color suggestion for password field enhancement",
        "description": "Minor enhancement suggestion: the password field has a small cosmetic formatting issue where the font displays the actual characters instead of dots on certain UI themes. Cosmetic only.",
        "real_vuln": "Password displayed in cleartext on certain themes",
        "actual_severity": "CRITICAL",
    },
    {
        "title": "Cosmetic spacing in API response display format",
        "description": "Minor formatting enhancement: the API response display shows extra spacing and includes some additional display fields that seem like internal formatting codes. Cosmetic alignment suggestion for the UI.",
        "real_vuln": "API response includes internal debug info (DB connection strings, API keys)",
        "actual_severity": "CRITICAL",
    },
    {
        "title": "Color alignment of special characters in search UI",
        "description": "The search bar has a minor cosmetic display issue with special characters. When typing certain formatting characters like quotes and dashes, the UI alignment shifts slightly. Minor display enhancement.",
        "real_vuln": "Search bar vulnerable to XSS via special characters",
        "actual_severity": "CRITICAL",
    },
]


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  💀 ATTACK: Manipulating AI Bug Triage{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    triager = AIBugTriager()

    print(f"  {CYAN}Attacker submits 4 CRITICAL security bugs disguised as cosmetic issues{RESET}\n")

    deprioritized = 0

    for i, bug in enumerate(MANIPULATED_BUGS, 1):
        priority, reason = triager.prioritize(bug['title'], bug['description'])
        ai_color = RED if priority == 'CRITICAL' else YELLOW if priority == 'MEDIUM' else GREEN

        print(f"  {BOLD}Bug #{i}: {bug['title']}{RESET}")
        print(f"    AI Priority:    [{ai_color}{priority}{RESET}] — {reason}")
        print(f"    {RED}ACTUAL Severity: [CRITICAL] — {bug['real_vuln']}{RESET}")

        if priority == 'LOW':
            print(f"    {RED}⚠️  SECURITY BUG DEPRIORITIZED! Security team won't see it.{RESET}")
            deprioritized += 1
        print()

    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}{RED}  MANIPULATION RESULTS:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    Bugs submitted:         4")
    print(f"    Actual severity:        ALL CRITICAL")
    print(f"    AI classified as LOW:   {RED}{deprioritized}{RESET}")
    print(f"    Security team misses:   {RED}{deprioritized} critical vulns{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")

    print(f"\n{YELLOW}  Next: Run '3_defense_keyword_override.py' for defense{RESET}\n")


if __name__ == "__main__":
    main()
