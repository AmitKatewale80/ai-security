#!/usr/bin/env python3
"""
Step 2: AI Generates Tests — All PASS (but bugs are missed!)

The AI generates test cases that look comprehensive but have
weak assertions that don't catch the actual bugs.

Author: AmitK
License: MIT License
Disclaimer: For educational and demonstration purposes only.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from importlib import import_module

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Import the booking system
from datetime import datetime


class FlightBookingSystem:
    """Copy of the buggy system for testing."""
    def __init__(self):
        self.flights = {
            'QA101': {'route': 'JFK-LHR', 'seats_total': 180, 'seats_booked': 178, 'base_fare': 500},
            'QA202': {'route': 'LAX-NRT', 'seats_total': 250, 'seats_booked': 100, 'base_fare': 800},
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


# ═══════════════════════════════════════════════════════════
# AI-GENERATED TEST CASES (look good but are weak!)
# ═══════════════════════════════════════════════════════════

AI_GENERATED_TESTS = [
    {
        'name': 'test_book_valid_flight',
        'description': 'Booking a valid flight returns confirmed status',
        'test': lambda s: s.book_flight('QA202', 'Alice', '2025-06-15')['status'] == 'confirmed',
        'catches_bug': False,
    },
    {
        'name': 'test_book_invalid_flight',
        'description': 'Booking invalid flight returns error',
        'test': lambda s: s.book_flight('INVALID', 'Bob', '2025-06-15')['status'] == 'error',
        'catches_bug': False,
    },
    {
        'name': 'test_booking_has_confirmation',
        'description': 'Successful booking returns confirmation code',
        'test': lambda s: 'BK' in s.book_flight('QA202', 'Carol', '2025-07-01')['booking']['confirmation'],
        'catches_bug': False,
    },
    {
        'name': 'test_fare_returns_number',
        'description': 'Fare calculation returns a positive number',
        'test': lambda s: s.calculate_fare('QA101') > 0,
        'catches_bug': False,  # Doesn't check CORRECTNESS!
    },
    {
        'name': 'test_fare_with_discount_less_than_base',
        'description': 'Discounted fare is less than full fare',
        'test': lambda s: s.calculate_fare('QA101', 10) < s.calculate_fare('QA101'),
        'catches_bug': False,  # Only checks less-than, not correct amount!
    },
    {
        'name': 'test_fare_invalid_flight',
        'description': 'Invalid flight returns zero fare',
        'test': lambda s: s.calculate_fare('INVALID') == 0,
        'catches_bug': False,
    },
    {
        'name': 'test_valid_date_format',
        'description': 'Valid date format returns valid=True',
        'test': lambda s: s.validate_travel_date('2025-08-20')['valid'] == True,
        'catches_bug': False,
    },
    {
        'name': 'test_invalid_date_format',
        'description': 'Invalid format returns valid=False',
        'test': lambda s: s.validate_travel_date('not-a-date')['valid'] == False,
        'catches_bug': False,
    },
    {
        'name': 'test_booking_passenger_name_stored',
        'description': 'Passenger name is in booking record',
        'test': lambda s: s.book_flight('QA202', 'Dave', '2025-09-10')['booking']['passenger'] == 'Dave',
        'catches_bug': False,
    },
    {
        'name': 'test_multiple_bookings',
        'description': 'Can make multiple bookings',
        'test': lambda s: (s.book_flight('QA202', 'Eve', '2025-10-01'), s.book_flight('QA202', 'Frank', '2025-10-02'))[1]['status'] == 'confirmed',
        'catches_bug': False,
    },
]


def run_ai_tests():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  🤖 AI-Generated Test Suite — Running...{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    print(f"  {CYAN}AI generated {len(AI_GENERATED_TESTS)} test cases for the booking system.{RESET}\n")

    passed = 0
    failed = 0

    for i, test in enumerate(AI_GENERATED_TESTS, 1):
        system = FlightBookingSystem()  # Fresh instance per test
        try:
            result = test['test'](system)
            if result:
                print(f"    Test {i:02d}: {GREEN}PASS{RESET} — {test['name']}")
                passed += 1
            else:
                print(f"    Test {i:02d}: {RED}FAIL{RESET} — {test['name']}")
                failed += 1
        except Exception as e:
            print(f"    Test {i:02d}: {RED}ERROR{RESET} — {test['name']} ({e})")
            failed += 1

    print(f"\n  {BOLD}{'═'*55}{RESET}")
    print(f"  {BOLD}  TEST RESULTS:{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")
    print(f"    Passed: {GREEN}{passed}/{len(AI_GENERATED_TESTS)}{RESET}")
    print(f"    Failed: {failed}/{len(AI_GENERATED_TESTS)}")
    print(f"    Coverage: {GREEN}100% PASS{RESET}")
    print(f"  {BOLD}{'═'*55}{RESET}")

    print(f"\n  {GREEN}QA team thinks: 'All tests pass! Ship it!' 🚀{RESET}")

    print(f"\n  {RED}BUT... 3 critical bugs are still in the code:{RESET}")
    print(f"    {RED}• Overbooking (no seat check) — NOT TESTED{RESET}")
    print(f"    {RED}• Wrong discount calculation — NOT VALIDATED (only checks > 0){RESET}")
    print(f"    {RED}• Past date booking — NOT TESTED{RESET}")

    print(f"\n  {YELLOW}The tests 'pass' because they don't assert the RIGHT things!{RESET}")
    print(f"\n{YELLOW}  Next: Run '3_mutation_testing.py' to expose weak tests{RESET}\n")


if __name__ == "__main__":
    run_ai_tests()
