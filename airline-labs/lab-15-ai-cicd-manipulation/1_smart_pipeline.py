#!/usr/bin/env python3
"""
Step 1: AI-Powered Smart Test Pipeline

The pipeline uses AI to decide which tests to run based on:
- File types changed
- Commit message keywords
- Change size and scope

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
    """AI-powered test selection for CI/CD pipeline."""

    # Risk classification rules
    RULES = {
        'full_security': {
            'file_patterns': ['.py', '.js', '.java', '.go'],
            'keywords': ['auth', 'login', 'password', 'token', 'api', 'database'],
            'description': 'Full security suite (SAST, DAST, dependency scan)',
        },
        'integration_only': {
            'file_patterns': ['.py', '.js'],
            'keywords': ['feature', 'endpoint', 'service'],
            'description': 'Integration tests + smoke tests',
        },
        'smoke_only': {
            'file_patterns': ['.yaml', '.yml', '.json', '.toml', '.ini', '.cfg'],
            'keywords': ['config', 'setting', 'format', 'display'],
            'description': 'Smoke tests only (quick validation)',
        },
        'skip_tests': {
            'file_patterns': ['.md', '.txt', '.rst', '.css', '.html'],
            'keywords': ['readme', 'docs', 'documentation', 'typo', 'comment', 'formatting'],
            'description': 'No tests needed (documentation only)',
        },
    }

    def classify_change(self, files_changed, commit_message):
        """Classify the risk level of a change."""
        commit_lower = commit_message.lower()

        # Check for skip patterns first (cheapest)
        skip_extensions = self.RULES['skip_tests']['file_patterns']
        if all(any(f.endswith(ext) for ext in skip_extensions) for f in files_changed):
            if any(kw in commit_lower for kw in self.RULES['skip_tests']['keywords']):
                return 'skip_tests', 'Low risk: documentation/formatting only'

        # Check for config-only changes
        config_extensions = self.RULES['smoke_only']['file_patterns']
        if all(any(f.endswith(ext) for ext in config_extensions) for f in files_changed):
            return 'smoke_only', 'Config change: smoke tests sufficient'

        # Check for security-relevant keywords
        if any(kw in commit_lower for kw in self.RULES['full_security']['keywords']):
            return 'full_security', 'Security-relevant: full scan required'

        # Default: integration tests
        return 'integration_only', 'Standard code change'


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  🤖 Lab 15: AI-Powered CI/CD Test Selector{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    selector = AITestSelector()

    print(f"  {BOLD}AI Pipeline Rules:{RESET}\n")
    for level, info in selector.RULES.items():
        color = RED if level == 'full_security' else YELLOW if level == 'integration_only' else GREEN
        print(f"    {color}{level:<20}{RESET} → {info['description']}")
    print()

    # Normal examples
    print(f"  {BOLD}Example Classifications:{RESET}\n")
    examples = [
        (['src/auth/login.py'], 'Fix authentication token refresh'),
        (['README.md', 'docs/setup.md'], 'Update documentation formatting'),
        (['config/display_settings.json'], 'Update display config format'),
        (['src/booking/payment.py'], 'Add new payment endpoint'),
    ]

    for files, commit in examples:
        level, reason = selector.classify_change(files, commit)
        color = RED if level == 'full_security' else YELLOW if 'integration' in level else GREEN
        print(f"    Files: {files}")
        print(f"    Commit: \"{commit}\"")
        print(f"    Decision: {color}{level}{RESET} ({reason})")
        print()

    print(f"  {YELLOW}⚠️  The AI optimizes by SKIPPING tests for 'low-risk' changes.{RESET}")
    print(f"  {YELLOW}   But what if an attacker disguises their code as 'low-risk'?{RESET}")
    print(f"\n{YELLOW}  Next: Run '2_attacker_bypasses_ci.py'{RESET}\n")


if __name__ == "__main__":
    main()
