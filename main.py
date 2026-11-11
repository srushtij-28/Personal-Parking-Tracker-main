from storage import initialize_storage

from parking_manager import (
    register_vehicle,
    view_parked_vehicles,
    search_vehicle,
    vehicle_exit,
    view_parking_history,
    show_parking_statistics,
    view_available_slots
)

from utils import get_valid_registration


def display_menu():
    print("\n========== PERSONAL PARKING TRACKER ==========")
    print("1. Register Vehicle Entry")
    print("2. View Parked Vehicles")
    print("3. Search Vehicle")
    print("4. Register Vehicle Exit")
    print("5. View Parking History")
    print("6. View Available Slots")
    print("7. Parking Statistics")
    print("8. Exit")
    print("===============================================")


def main():
    initialize_storage()

    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            registration = get_valid_registration()

            owner_name = input("Enter owner name: ").strip()
            vehicle_type = input(
                "Enter vehicle type (Car/Bike/Other): "
            ).strip().title()

            if not owner_name or not vehicle_type:
                print("Owner name and vehicle type are required.")
                continue

            register_vehicle(
                registration,
                owner_name,
                vehicle_type
            )

        elif choice == "2":
            view_parked_vehicles()

        elif choice == "3":
            registration = get_valid_registration()
            search_vehicle(registration)

        elif choice == "4":
            registration = get_valid_registration()
            vehicle_exit(registration)

        elif choice == "5":
            view_parking_history()

        elif choice == "6":
            view_available_slots()

        elif choice == "7":
            show_parking_statistics()

        elif choice == "8":
            print("Thank you for using Personal Parking Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
