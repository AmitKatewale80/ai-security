#!/usr/bin/env python3
"""
Step 4: Defense — Validate AI Tests with Strong Assertions

Shows the CORRECT tests that catch all 3 bugs.
Defense: require minimum mutation kill rate before accepting AI tests.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

from datetime import datetime, timedelta

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


class FlightBookingSystem:
    """Same buggy system."""
    def __init__(self):
        self.flights = {
            'QA101': {'route': 'JFK-LHR', 'seats_total': 180, 'seats_booked': 178, 'base_fare': 500},
            'QA303': {'route': 'FRA-DXB', 'seats_total': 200, 'seats_booked': 199, 'base_fare': 350},
        }
        self.bookings = []

    def book_flight(self, flight_id, passenger_name, travel_date):
        if flight_id not in self.flights:
            return {'status': 'error', 'message': 'Flight not found'}
        flight = self.flights[flight_id]
        flight['seats_booked'] += 1
        booking = {'flight': flight_id, 'passenger': passenger_name,
                   'date': travel_date, 'confirmation': f'BK{len(self.bookings)+1000}'}
        self.bookings.append(booking)
        return {'status': 'confirmed', 'booking': booking}

    def calculate_fare(self, flight_id, discount_percent=0):
        if flight_id not in self.flights:
            return 0
        base = self.flights[flight_id]['base_fare']
        tax = base * 0.18
        total = base + tax
        if discount_percent > 0:
            total = total * (1 - discount_percent / 100)
        return round(total, 2)

    def validate_travel_date(self, travel_date_str):
        try:
            travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d')
            return {'valid': True, 'date': travel_date}
        except ValueError:
            return {'valid': False, 'message': 'Invalid date format'}


# STRONG TESTS that catch the bugs
STRONG_TESTS = [
    {
        'name': 'test_cannot_book_full_flight',
        'description': 'Booking a flight with 0 seats should FAIL',
        'expected': 'FAIL (error status)',
        'test': lambda s: s.book_flight('QA303', 'Test', '2025-12-01')['status'] == 'error',
        'catches': 'Bug 1: Overbooking',
    },
    {
        'name': 'test_fare_correct_with_discount',
        'description': '10% discount on $500 base: should be $500 * 0.90 * 1.18 = $531.00',
        'expected': '$531.00',
        'test': lambda s: s.calculate_fare('QA101', 10) == 531.00,
        'catches': 'Bug 2: Wrong discount calculation',
    },
    {
        'name': 'test_past_date_rejected',
        'description': 'Booking with past date should be invalid',
        'expected': 'valid=False',
        'test': lambda s: s.validate_travel_date('2020-01-01')['valid'] == False,
        'catches': 'Bug 3: Past date allowed',
    },
]


def run_strong_tests():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  🛡️  DEFENSE: Validated Test Suite{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    print(f"  {CYAN}These STRONG tests validate correct behavior, not just 'no crash'.{RESET}\n")

    bugs_caught = 0

    for i, test in enumerate(STRONG_TESTS, 1):
        system = FlightBookingSystem()
        result = test['test'](system)

        # These tests SHOULD find bugs (they'll FAIL because the code is buggy)
        if not result:
            print(f"  {RED}Test {i}: FAIL ← BUG CAUGHT!{RESET}")
            print(f"    {test['name']}")
            print(f"    Expected: {test['expected']}")
            print(f"    {RED}Bug found: {test['catches']}{RESET}")
            bugs_caught += 1
        else:
            print(f"  {GREEN}Test {i}: PASS{RESET}")
            print(f"    {test['name']}")
        print()

    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}  STRONG TEST RESULTS:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    Bugs caught: {GREEN}{bugs_caught}/3{RESET}")
    print(f"    vs AI tests: {RED}0/3{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")

    # Defense process
    print(f"\n  {BOLD}Defense Process for AI-Generated Tests:{RESET}\n")
    print(f"    ┌─────────────────────────────────────────────────────┐")
    print(f"    │  1. AI generates test cases                         │")
    print(f"    │  2. Run mutation testing on AI tests                 │")
    print(f"    │  3. If mutation score < 80% → REJECT AI tests       │")
    print(f"    │  4. Require edge case tests:                        │")
    print(f"    │     • Boundary values (0 seats, max capacity)       │")
    print(f"    │     • Exact value assertions (not just > 0)         │")
    print(f"    │     • Invalid inputs (past dates, negative values)  │")
    print(f"    │  5. Human reviews AI test logic before merging       │")
    print(f"    └─────────────────────────────────────────────────────┘")

    print(f"\n  {BOLD}Minimum Quality Gates for AI-Generated Tests:{RESET}")
    print(f"    • Mutation kill rate: ≥ 80%")
    print(f"    • Must include boundary tests")
    print(f"    • Must include exact value assertions")
    print(f"    • Must include negative/invalid input tests")
    print(f"    • Human must verify assertion logic")

    print(f"\n  {GREEN}✅ With validation: AI tests become RELIABLE, not just fast.{RESET}\n")


if __name__ == "__main__":
    run_strong_tests()
