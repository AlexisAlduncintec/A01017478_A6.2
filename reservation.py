"""Reservation module for managing reservation entities."""

import json
import os

from customer import Customer
from hotel import Hotel


class Reservation:
    """Represents a reservation and supports CRUD operations."""

    DATA_FILE = os.path.join(
        os.path.dirname(__file__), "data", "reservations.json"
    )

    def __init__(self, reservation_id, customer_id, hotel_id):
        """Initialize a Reservation instance.

        Args:
            reservation_id: Unique identifier for the reservation.
            customer_id: ID of the customer making the reservation.
            hotel_id: ID of the hotel being reserved.
        """
        self.reservation_id = str(reservation_id)
        self.customer_id = str(customer_id)
        self.hotel_id = str(hotel_id)

    def create_reservation(self):
        """Add this reservation to the JSON data file.

        Validates that the customer and hotel exist, then reserves
        a room in the hotel.

        Returns:
            True if created successfully, False otherwise.
        """
        if Customer.display_customer_info(self.customer_id) is None:
            print(f"Error: Customer '{self.customer_id}' not found.")
            return False

        if Hotel.display_hotel_info(self.hotel_id) is None:
            print(f"Error: Hotel '{self.hotel_id}' not found.")
            return False

        reservations = Reservation.load_from_file()

        for reservation in reservations:
            if reservation["reservation_id"] == self.reservation_id:
                print(
                    f"Error: Reservation with id "
                    f"'{self.reservation_id}' already exists."
                )
                return False

        if not Hotel.reserve_room(self.hotel_id):
            return False

        reservations.append(self._to_dict())
        Reservation.save_to_file(reservations)
        return True

    @staticmethod
    def cancel_reservation(reservation_id):
        """Cancel a reservation and free the hotel room.

        Args:
            reservation_id: ID of the reservation to cancel.

        Returns:
            True if cancelled successfully, False otherwise.
        """
        reservation_id = str(reservation_id)
        reservations = Reservation.load_from_file()
        target = None

        for reservation in reservations:
            if reservation["reservation_id"] == reservation_id:
                target = reservation
                break

        if target is None:
            print(
                f"Error: Reservation with id "
                f"'{reservation_id}' not found."
            )
            return False

        Hotel.cancel_reservation(target["hotel_id"])

        updated = [
            r for r in reservations
            if r["reservation_id"] != reservation_id
        ]
        Reservation.save_to_file(updated)
        return True

    @staticmethod
    def display_reservation_info(reservation_id):
        """Display reservation information.

        Args:
            reservation_id: ID of the reservation to display.

        Returns:
            Dictionary with reservation info, or None if not found.
        """
        reservation_id = str(reservation_id)
        reservations = Reservation.load_from_file()

        for reservation in reservations:
            if reservation["reservation_id"] == reservation_id:
                print(
                    f"Reservation ID: "
                    f"{reservation['reservation_id']}"
                )
                print(
                    f"Customer ID: {reservation['customer_id']}"
                )
                print(f"Hotel ID: {reservation['hotel_id']}")
                return reservation

        print(
            f"Error: Reservation with id "
            f"'{reservation_id}' not found."
        )
        return None

    @staticmethod
    def save_to_file(reservations):
        """Save a list of reservation dicts to the JSON data file.

        Args:
            reservations: List of reservation dictionaries to save.
        """
        try:
            with open(
                Reservation.DATA_FILE, "w", encoding="utf-8"
            ) as file:
                json.dump(reservations, file, indent=4)
        except (OSError, TypeError) as exc:
            print(f"Error saving to file: {exc}")

    @staticmethod
    def load_from_file():
        """Load reservations from the JSON data file.

        Returns:
            List of reservation dictionaries, or empty list on error.
        """
        if not os.path.exists(Reservation.DATA_FILE):
            return []
        try:
            with open(
                Reservation.DATA_FILE, "r", encoding="utf-8"
            ) as file:
                data = json.load(file)
            if not isinstance(data, list):
                print("Error: Corrupted JSON file, expected a list.")
                return []
            return data
        except (json.JSONDecodeError, OSError) as exc:
            print(f"Error loading from file: {exc}")
            return []

    def _to_dict(self):
        """Convert the reservation instance to a dictionary.

        Returns:
            Dictionary representation of the reservation.
        """
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
        }
