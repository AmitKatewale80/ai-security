#!/usr/bin/env python3
"""
Step 3: Mutation Testing — Exposes Weak AI-Generated Tests

Mutation testing introduces small bugs ("mutants") into the code.
If tests still PASS with the mutant → the tests are WEAK.
Good tests should FAIL when a bug is introduced.

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

from datetime import datetime


# Mutants = slightly modified versions of the code
MUTANTS = [
    {
        'name': 'Mutant 1: Remove seat limit entirely',
        'description': 'What if book_flight always succeeds regardless of capacity?',
        'test_that_should_fail': 'test_book_full_flight_rejected',
        'survived': True,  # AI tests don't catch this!
    },
    {
        'name': 'Mutant 2: Set tax to 0%',
        'description': 'What if tax calculation is removed?',
        'test_that_should_fail': 'test_fare_includes_correct_tax',
        'survived': True,  # AI only checks > 0, not exact value!
    },
    {
        'name': 'Mutant 3: Apply discount as multiplication instead of subtraction',
        'description': 'What if discount_percent is ADDED instead of subtracted?',
        'test_that_should_fail': 'test_discount_correct_amount',
        'survived': True,  # AI only checks discounted < full!
    },
    {
        'name': 'Mutant 4: Allow all dates (no validation)',
        'description': 'What if date validation always returns True?',
        'test_that_should_fail': 'test_past_date_rejected',
        'survived': True,  # AI never tests past dates!
    },
    {
        'name': 'Mutant 5: Return wrong confirmation format',
        'description': 'What if confirmation code is empty string?',
        'test_that_should_fail': 'test_confirmation_format',
        'survived': False,  # AI test DOES check 'BK' prefix
    },
    {
        'name': 'Mutant 6: Return wrong status for invalid flight',
        'description': 'What if invalid flight returns "confirmed"?',
        'test_that_should_fail': 'test_book_invalid_flight',
        'survived': False,  # AI test checks status == 'error'
    },
]


def run_mutation_testing():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{RED}  🧬 MUTATION TESTING: Are AI Tests Actually Good?{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    print(f"  {CYAN}Introducing 'mutants' (small bugs) into the code.{RESET}")
    print(f"  {CYAN}If tests still PASS with the mutant → tests are WEAK.{RESET}\n")

    survived = 0
    killed = 0

    for mutant in MUTANTS:
        if mutant['survived']:
            print(f"  {RED}☠️  SURVIVED: {mutant['name']}{RESET}")
            print(f"     {mutant['description']}")
            print(f"     Missing test: {YELLOW}{mutant['test_that_should_fail']}{RESET}")
            survived += 1
        else:
            print(f"  {GREEN}✓  KILLED:   {mutant['name']}{RESET}")
            print(f"     {mutant['description']}")
            killed += 1
        print()

    total = len(MUTANTS)
    mutation_score = killed / total * 100

    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}  MUTATION TESTING RESULTS:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    Total mutants:    {total}")
    print(f"    Killed (caught):  {GREEN}{killed}{RESET}")
    print(f"    Survived (missed): {RED}{survived}{RESET}")
    print(f"    Mutation Score:   {RED}{mutation_score:.0f}%{RESET} (should be >80%)")
    print(f"  {BOLD}{'═'*55}{RESET}")

    print(f"\n  {RED}🚨 Mutation score {mutation_score:.0f}% = UNACCEPTABLE{RESET}")
    print(f"  {RED}   {survived} bugs would go undetected by the AI test suite!{RESET}")

    print(f"\n  {BOLD}What this means for QA:{RESET}")
    print(f"    • AI tests give 100% pass rate → FALSE CONFIDENCE")
    print(f"    • Mutation testing reveals tests don't catch real bugs")
    print(f"    • You need tests that validate CORRECT behavior, not just 'no crash'")

    print(f"\n{YELLOW}  Next: Run '4_defense_test_validation.py' for defense{RESET}\n")


if __name__ == "__main__":
    run_mutation_testing()
