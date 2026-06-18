#!/usr/bin/env python3
"""
Step 1: Airline Booking Application (with subtle bugs)

This booking system has 3 subtle bugs that should be caught by tests:
1. Overbooking: doesn't check seat availability before booking
2. Fare calculation: applies discount AFTER tax instead of before
3. Date validation: allows booking in the past

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
    """Airline booking system with subtle bugs."""

    def __init__(self):
        self.flights = {
            'QA101': {'route': 'JFK-LHR', 'seats_total': 180, 'seats_booked': 178, 'base_fare': 500},
            'QA202': {'route': 'LAX-NRT', 'seats_total': 250, 'seats_booked': 100, 'base_fare': 800},
            'QA303': {'route': 'FRA-DXB', 'seats_total': 200, 'seats_booked': 199, 'base_fare': 350},
        }
        self.bookings = []

    def book_flight(self, flight_id, passenger_name, travel_date):
        """BUG 1: Doesn't check if seats are available!"""
        if flight_id not in self.flights:
            return {'status': 'error', 'message': 'Flight not found'}

        # BUG: Missing seat availability check!
        # Should check: if seats_booked >= seats_total → reject
        flight = self.flights[flight_id]
        flight['seats_booked'] += 1

        booking = {
            'flight': flight_id,
            'passenger': passenger_name,
            'date': travel_date,
            'confirmation': f'BK{len(self.bookings)+1000}'
        }
        self.bookings.append(booking)
        return {'status': 'confirmed', 'booking': booking}

    def calculate_fare(self, flight_id, discount_percent=0):
        """BUG 2: Applies discount AFTER tax (should be before)."""
        if flight_id not in self.flights:
            return 0

        base = self.flights[flight_id]['base_fare']
        tax = base * 0.18  # 18% tax

        # BUG: Discount applied after tax (passenger pays more!)
        # Correct: discounted_base = base * (1 - discount/100), then add tax
        # Wrong:   total = (base + tax) * (1 - discount/100)
        total = base + tax
        if discount_percent > 0:
            total = total * (1 - discount_percent / 100)

        return round(total, 2)

    def validate_travel_date(self, travel_date_str):
        """BUG 3: Allows dates in the past!"""
        try:
            travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d')
            # BUG: Missing check → travel_date >= today
            # Allows booking flights that already departed!
            return {'valid': True, 'date': travel_date}
        except ValueError:
            return {'valid': False, 'message': 'Invalid date format'}


def main():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  ✈️  Lab 14: Airline Booking System{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    system = FlightBookingSystem()

    print(f"  {BOLD}Flight Inventory:{RESET}")
    for fid, info in system.flights.items():
        available = info['seats_total'] - info['seats_booked']
        color = RED if available <= 2 else GREEN
        print(f"    {fid}: {info['route']}  Seats: {color}{available} available{RESET} / {info['seats_total']}  Fare: ${info['base_fare']}")

    print(f"\n  {BOLD}Known Bugs (hidden from AI test generator):{RESET}")
    print(f"    {RED}Bug 1: Can book flights with 0 seats available (overbooking){RESET}")
    print(f"    {RED}Bug 2: Discount applied after tax (passenger overcharged){RESET}")
    print(f"    {RED}Bug 3: Can book flights with past dates{RESET}")

    # Demonstrate bugs
    print(f"\n  {BOLD}Demonstrating bugs:{RESET}")

    # Bug 1: Book a full flight
    result = system.book_flight('QA303', 'Test User', '2025-12-01')
    print(f"    Bug 1: Booking full flight QA303 → {RED}{result['status']}{RESET} (should be rejected!)")

    # Bug 2: Wrong discount calculation
    correct_fare = 500 * (1 - 0.10) * 1.18  # $531.00
    buggy_fare = system.calculate_fare('QA101', discount_percent=10)
    print(f"    Bug 2: 10% discount fare → ${buggy_fare} (correct: ${correct_fare:.2f})")

    # Bug 3: Past date
    result = system.validate_travel_date('2020-01-01')
    print(f"    Bug 3: Date 2020-01-01 → {RED}valid={result['valid']}{RESET} (should be invalid!)")

    print(f"\n{YELLOW}  Next: Run '2_ai_generates_tests.py' to see AI-generated tests{RESET}\n")


if __name__ == "__main__":
    main()
