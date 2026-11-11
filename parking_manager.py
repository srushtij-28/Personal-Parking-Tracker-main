from datetime import datetime

from storage import load_records, save_records
from config import TOTAL_PARKING_SLOTS
from utils import (
    get_current_time,
    format_datetime,
    calculate_parking_charge
)


def get_available_slots():
    records = load_records()

    occupied_slots = {
        record["slot_number"]
        for record in records
        if record["status"] == "Parked"
    }

    available_slots = [
        slot
        for slot in range(1, TOTAL_PARKING_SLOTS + 1)
        if slot not in occupied_slots
    ]

    return available_slots


def register_vehicle(registration, owner_name, vehicle_type):
    records = load_records()

    for record in records:
        if (
            record["registration"] == registration
            and record["status"] == "Parked"
        ):
            print("\nThis vehicle is already parked.")
            return

    available_slots = get_available_slots()

    if not available_slots:
        print("\nParking is full. No available slots.")
        return

    slot_number = available_slots[0]

    record_id = max(
        [record["id"] for record in records],
        default=0
    ) + 1

    entry_time = get_current_time()

    record = {
        "id": record_id,
        "registration": registration,
        "owner_name": owner_name,
        "vehicle_type": vehicle_type,
        "slot_number": slot_number,
        "entry_time": format_datetime(entry_time),
        "exit_time": "",
        "duration_hours": 0,
        "parking_charge": 0,
        "status": "Parked"
    }

    records.append(record)
    save_records(records)

    print("\nVehicle registered successfully!")
    print(f"Parking Slot: {slot_number}")
    print(f"Entry Time: {record['entry_time']}")


def view_parked_vehicles():
    records = load_records()

    parked_vehicles = [
        record for record in records
        if record["status"] == "Parked"
    ]

    if not parked_vehicles:
        print("\nNo vehicles are currently parked.")
        return

    print("\n" + "-" * 105)
    print(
        f"{'ID':<5} {'Registration':<18} {'Owner':<20} "
        f"{'Type':<15} {'Slot':<8} {'Entry Time':<22}"
    )
    print("-" * 105)

    for record in parked_vehicles:
        print(
            f"{record['id']:<5} "
            f"{record['registration']:<18} "
            f"{record['owner_name'][:19]:<20} "
            f"{record['vehicle_type']:<15} "
            f"{record['slot_number']:<8} "
            f"{record['entry_time']:<22}"
        )

    print("-" * 105)


def search_vehicle(registration):
    records = load_records()

    matching_records = [
        record for record in records
        if registration.lower() in record["registration"].lower()
    ]

    if not matching_records:
        print("\nNo matching vehicle records found.")
        return

    print("\nSearch Results:")

    for record in matching_records:
        print(
            f"\nID: {record['id']}"
            f"\nRegistration: {record['registration']}"
            f"\nOwner: {record['owner_name']}"
            f"\nVehicle Type: {record['vehicle_type']}"
            f"\nParking Slot: {record['slot_number']}"
            f"\nEntry Time: {record['entry_time']}"
            f"\nExit Time: {record['exit_time'] or 'Not exited'}"
            f"\nStatus: {record['status']}"
            f"\nParking Charge: ₹{record['parking_charge']}"
        )


def vehicle_exit(registration):
    records = load_records()

    for record in records:
        if (
            record["registration"] == registration
            and record["status"] == "Parked"
        ):
            exit_time = get_current_time()
            formatted_exit = format_datetime(exit_time)

            billed_hours, charge = calculate_parking_charge(
                record["entry_time"],
                formatted_exit
            )

            entry = datetime.fromisoformat(record["entry_time"])
            duration = (
                exit_time - entry
            ).total_seconds() / 3600

            record["exit_time"] = formatted_exit
            record["duration_hours"] = round(duration, 2)
            record["parking_charge"] = charge
            record["status"] = "Exited"

            save_records(records)

            print("\nVehicle exit recorded successfully!")
            print(f"Registration: {record['registration']}")
            print(f"Parking Slot: {record['slot_number']}")
            print(f"Entry Time: {record['entry_time']}")
            print(f"Exit Time: {formatted_exit}")
            print(f"Actual Duration: {duration:.2f} hours")
            print(f"Charged Hours: {billed_hours}")
            print(f"Total Parking Charge: ₹{charge}")

            return

    print("\nNo active parking record found for this vehicle.")


def view_parking_history():
    records = load_records()

    if not records:
        print("\nNo parking history available.")
        return

    print("\n" + "-" * 105)
    print(
        f"{'ID':<5} {'Registration':<18} {'Slot':<8} "
        f"{'Entry Time':<22} {'Status':<12} {'Charge':<10}"
    )
    print("-" * 105)

    for record in records:
        print(
            f"{record['id']:<5} "
            f"{record['registration']:<18} "
            f"{record['slot_number']:<8} "
            f"{record['entry_time']:<22} "
            f"{record['status']:<12} "
            f"₹{record['parking_charge']:<9}"
        )

    print("-" * 105)


def show_parking_statistics():
    records = load_records()

    if not records:
        print("\nNo parking statistics available.")
        return

    total_vehicles = len(records)

    parked = sum(
        1 for record in records
        if record["status"] == "Parked"
    )

    exited = sum(
        1 for record in records
        if record["status"] == "Exited"
    )

    total_revenue = sum(
        record["parking_charge"]
        for record in records
    )

    available = TOTAL_PARKING_SLOTS - parked

    print("\n========== PARKING STATISTICS ==========")
    print(f"Total Registered Entries: {total_vehicles}")
    print(f"Currently Parked Vehicles: {parked}")
    print(f"Vehicles Exited: {exited}")
    print(f"Available Slots: {available}")
    print(f"Total Parking Revenue: ₹{total_revenue}")
    print("========================================")


def view_available_slots():
    available_slots = get_available_slots()

    print("\n========== PARKING SLOT STATUS ==========")
    print(f"Total Slots: {TOTAL_PARKING_SLOTS}")
    print(f"Available Slots: {len(available_slots)}")

    if available_slots:
        print(f"Available Slot Numbers: {available_slots}")
    else:
        print("Parking is currently full.")

    print("=========================================")
