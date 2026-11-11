from datetime import datetime
from math import ceil

from config import HOURLY_RATE


def get_current_time():
    return datetime.now()


def format_datetime(value):
    return value.strftime("%Y-%m-%d %H:%M:%S")


def calculate_parking_duration(entry_time, exit_time):
    entry = datetime.fromisoformat(entry_time)
    exit = datetime.fromisoformat(exit_time)

    duration = exit - entry
    return duration.total_seconds() / 3600


def calculate_parking_charge(entry_time, exit_time):
    hours = calculate_parking_duration(entry_time, exit_time)

    billed_hours = max(1, ceil(hours))
    amount = billed_hours * HOURLY_RATE

    return billed_hours, amount


def get_valid_registration():
    while True:
        registration = input(
            "Enter vehicle registration number: "
        ).strip().upper()

        if registration:
            return registration

        print("Registration number cannot be empty.")


def get_valid_id(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value > 0:
                return value

            print("ID must be greater than zero.")

        except ValueError:
            print("Please enter a valid numeric ID.")
