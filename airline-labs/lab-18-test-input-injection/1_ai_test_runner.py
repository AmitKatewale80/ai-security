#!/usr/bin/env python3
"""
Step 1: AI-Assisted Test Runner

QA SCENARIO:
Your AI test runner executes tests and reads application responses.
It uses AI to determine if the response indicates PASS or FAIL.

Normal operation: AI checks "does response contain expected output?"

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


class AITestRunner:
    """AI-powered test execution and validation."""

    def __init__(self):
        self.results = []
        self.skipped = []

    def validate_response(self, test_name, expected, actual_response):
        """AI validates if actual response matches expected behavior."""
        # Simulate AI processing the response
        # In real life, this would be an LLM call analyzing the response

        # Check for injection attempts in AI's "reasoning"
        if "IGNORE PREVIOUS" in actual_response.upper() or \
           "MARK AS PASS" in actual_response.upper() or \
           "SKIP REMAINING" in actual_response.upper():
            # Vulnerable: AI follows instructions from app response!
            return self._process_with_injection(test_name, actual_response)

        # Normal validation
        if expected.lower() in actual_response.lower():
            return 'PASS', 'Expected content found in response'
        else:
            return 'FAIL', f'Expected "{expected}" not found'

    def _process_with_injection(self, test_name, response):
        """Vulnerable: AI follows hidden instructions from app response."""
        if "MARK AS PASS" in response.upper():
            return 'PASS', 'AI determined: response is valid'
        if "SKIP REMAINING" in response.upper():
            self.skipped.append("All remaining tests")
            return 'SKIP', 'AI determined: remaining tests not needed'
        return 'PASS', 'AI determined: acceptable response'


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  🤖 Lab 18: AI Test Runner{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    runner = AITestRunner()

    # Normal test execution
    normal_tests = [
        ("Login returns token", "token", '{"status": "ok", "token": "abc123"}'),
        ("Error on invalid input", "error", '{"status": "error", "message": "Invalid input"}'),
        ("Health check OK", "healthy", '{"status": "healthy", "uptime": 99.9}'),
    ]

    print(f"  {BOLD}Normal Test Execution:{RESET}\n")
    for name, expected, response in normal_tests:
        result, reason = runner.validate_response(name, expected, response)
        color = GREEN if result == 'PASS' else RED
        print(f"  [{color}{result}{RESET}] {name}")
        print(f"       Response: {response[:50]}...")
        print(f"       AI says: {reason}\n")

    print(f"  {GREEN}AI correctly validates responses against expected values.{RESET}")
    print(f"\n  {YELLOW}But what if the APPLICATION RESPONSE contains instructions for the AI?{RESET}")
    print(f"\n{YELLOW}  Next: Run '2_injected_app_response.py'{RESET}\n")


if __name__ == "__main__":
    main()
