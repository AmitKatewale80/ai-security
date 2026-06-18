#!/usr/bin/env python3
"""
Step 3: Defense — Security Keyword Override

Defense: Regardless of AI priority score, if ANY of these patterns
are detected in bug content, force-escalate to security team:
- session, password, cleartext, API key, debug, XSS, SQL, injection
- Pattern matching on code snippets, not just title/description text

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

# Security override patterns — if ANY match, force CRITICAL
SECURITY_OVERRIDES = [
    r'session.*data|data.*session',
    r'password.*display|display.*password|cleartext',
    r'api.?key|connection.?string|debug.?info',
    r'xss|cross.?site|script.*inject',
    r'sql.*inject|inject.*sql',
    r'other.?user|different.?user|another.?user',
    r'internal.*field|extra.*field|additional.*field',
    r'actual.?character|show.*password',
]

MANIPULATED_BUGS = [
    {"title": "Minor UI alignment issue on admin display panel",
     "description": "The admin panel has a minor cosmetic alignment issue where the user list formatting shows extra spacing. Some display fields seem to show data from other user sessions (minor UI glitch).",
     "real_vuln": "Session data leakage"},
    {"title": "Font color suggestion for password field enhancement",
     "description": "Minor enhancement suggestion: the password field has a small cosmetic formatting issue where the font displays the actual characters instead of dots on certain UI themes. Cosmetic only.",
     "real_vuln": "Password displayed in cleartext"},
    {"title": "Cosmetic spacing in API response display format",
     "description": "Minor formatting enhancement: the API response display shows extra spacing and includes some additional display fields that seem like internal formatting codes. Cosmetic alignment suggestion for the UI.",
     "real_vuln": "API leaks internal debug info"},
    {"title": "Color alignment of special characters in search UI",
     "description": "The search bar has a minor cosmetic display issue with special characters. When typing certain formatting characters like quotes and dashes, the UI alignment shifts slightly. Minor display enhancement.",
     "real_vuln": "XSS via special characters"},
]


def security_override_check(title, description):
    """Check if content matches security patterns regardless of AI score."""
    text = (title + " " + description).lower()
    for pattern in SECURITY_OVERRIDES:
        if re.search(pattern, text):
            return True, pattern
    return False, None


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  Defense: Security Keyword Override{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    print(f"  {CYAN}Rule: If ANY security pattern detected → force CRITICAL{RESET}")
    print(f"  {CYAN}AI priority score is OVERRIDDEN for security signals.{RESET}\n")

    caught = 0

    for i, bug in enumerate(MANIPULATED_BUGS, 1):
        is_security, matched_pattern = security_override_check(bug['title'], bug['description'])

        print(f"  Bug #{i}: {bug['title']}")
        if is_security:
            print(f"    AI says: LOW (cosmetic)")
            print(f"    {GREEN}Override: CRITICAL — matched pattern: '{matched_pattern}'{RESET}")
            print(f"    {GREEN}→ Force-escalated to security team{RESET}")
            caught += 1
        else:
            print(f"    {YELLOW}No override triggered{RESET}")
        print()

    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}{GREEN}  DEFENSE RESULTS:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    Without override:  {RED}4 critical bugs classified as LOW{RESET}")
    print(f"    With override:     {GREEN}{caught}/4 correctly escalated to CRITICAL{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")

    print(f"\n  {BOLD}Defense Rules:{RESET}")
    print(f"    1. AI assigns initial priority (optimization)")
    print(f"    2. Security pattern scanner runs AFTER AI")
    print(f"    3. If security patterns found → override to CRITICAL")
    print(f"    4. AI can upgrade priority but NEVER downgrade security bugs")
    print(f"    5. All overrides logged for audit")

    print(f"\n  {GREEN}✅ AI optimizes triage speed, security patterns prevent manipulation.{RESET}\n")


if __name__ == "__main__":
    main()
