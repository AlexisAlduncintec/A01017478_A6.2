"""Hotel module for managing hotel entities and persistence."""

import json
import os


class Hotel:
    """Represents a hotel with rooms and supports CRUD operations."""

    DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "hotels.json")

    def __init__(self, hotel_id, name, location, rooms):
        """Initialize a Hotel instance.

        Args:
            hotel_id: Unique identifier for the hotel.
            name: Name of the hotel.
            location: Location of the hotel.
            rooms: Total number of rooms.
        """
        self.hotel_id = str(hotel_id)
        self.name = name
        self.location = location

        if not isinstance(rooms, int) or rooms < 0:
            print("Error: rooms must be a non-negative integer.")
            self.rooms = 0
            self.rooms_available = 0
        else:
            self.rooms = rooms
            self.rooms_available = rooms

    def create_hotel(self):
        """Add this hotel to the JSON data file.

        Returns:
            True if created successfully, False otherwise.
        """
        if not self.name or not isinstance(self.name, str):
            print("Error: Hotel name must be a non-empty string.")
            return False

        hotels = Hotel.load_from_file()

        for hotel in hotels:
            if hotel["hotel_id"] == self.hotel_id:
                print(f"Error: Hotel with id '{self.hotel_id}' "
                      f"already exists.")
                return False

        hotels.append(self._to_dict())
        Hotel.save_to_file(hotels)
        return True

    @staticmethod
    def delete_hotel(hotel_id):
        """Remove a hotel from the JSON data file.

        Args:
            hotel_id: ID of the hotel to delete.

        Returns:
            True if deleted successfully, False otherwise.
        """
        hotel_id = str(hotel_id)
        hotels = Hotel.load_from_file()
        updated = [h for h in hotels if h["hotel_id"] != hotel_id]

        if len(updated) == len(hotels):
            print(f"Error: Hotel with id '{hotel_id}' not found.")
            return False

        Hotel.save_to_file(updated)
        return True

    @staticmethod
    def display_hotel_info(hotel_id):
        """Display hotel information.

        Args:
            hotel_id: ID of the hotel to display.

        Returns:
            Dictionary with hotel info, or None if not found.
        """
        hotel_id = str(hotel_id)
        hotels = Hotel.load_from_file()

        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                print(f"Hotel ID: {hotel['hotel_id']}")
                print(f"Name: {hotel['name']}")
                print(f"Location: {hotel['location']}")
                print(f"Total Rooms: {hotel['rooms']}")
                print(f"Rooms Available: {hotel['rooms_available']}")
                return hotel

        print(f"Error: Hotel with id '{hotel_id}' not found.")
        return None

    @staticmethod
    def modify_hotel_info(hotel_id, **kwargs):
        """Update hotel attributes in the JSON data file.

        Args:
            hotel_id: ID of the hotel to modify.
            **kwargs: Attributes to update (name, location, rooms).

        Returns:
            True if modified successfully, False otherwise.
        """
        hotel_id = str(hotel_id)
        hotels = Hotel.load_from_file()

        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if "name" in kwargs:
                    if not kwargs["name"] or not isinstance(
                        kwargs["name"], str
                    ):
                        print("Error: name must be a non-empty string.")
                        return False
                    hotel["name"] = kwargs["name"]

                if "location" in kwargs:
                    hotel["location"] = kwargs["location"]

                if "rooms" in kwargs:
                    new_rooms = kwargs["rooms"]
                    if not isinstance(new_rooms, int) or new_rooms < 0:
                        print("Error: rooms must be a non-negative "
                              "integer.")
                        return False
                    diff = new_rooms - hotel["rooms"]
                    hotel["rooms"] = new_rooms
                    hotel["rooms_available"] = max(
                        0, hotel["rooms_available"] + diff
                    )

                Hotel.save_to_file(hotels)
                return True

        print(f"Error: Hotel with id '{hotel_id}' not found.")
        return False

    @staticmethod
    def reserve_room(hotel_id):
        """Reserve a room by decrementing rooms_available.

        Args:
            hotel_id: ID of the hotel to reserve a room in.

        Returns:
            True if reserved successfully, False otherwise.
        """
        hotel_id = str(hotel_id)
        hotels = Hotel.load_from_file()

        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if hotel["rooms_available"] <= 0:
                    print("Error: No rooms available.")
                    return False
                hotel["rooms_available"] -= 1
                Hotel.save_to_file(hotels)
                return True

        print(f"Error: Hotel with id '{hotel_id}' not found.")
        return False

    @staticmethod
    def cancel_reservation(hotel_id):
        """Cancel a reservation by incrementing rooms_available.

        Args:
            hotel_id: ID of the hotel to cancel a reservation in.

        Returns:
            True if cancelled successfully, False otherwise.
        """
        hotel_id = str(hotel_id)
        hotels = Hotel.load_from_file()

        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if hotel["rooms_available"] >= hotel["rooms"]:
                    print("Error: All rooms are already available.")
                    return False
                hotel["rooms_available"] += 1
                Hotel.save_to_file(hotels)
                return True

        print(f"Error: Hotel with id '{hotel_id}' not found.")
        return False

    @staticmethod
    def save_to_file(hotels):
        """Save a list of hotel dictionaries to the JSON data file.

        Args:
            hotels: List of hotel dictionaries to save.
        """
        try:
            with open(Hotel.DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(hotels, file, indent=4)
        except (OSError, TypeError) as exc:
            print(f"Error saving to file: {exc}")

    @staticmethod
    def load_from_file():
        """Load hotels from the JSON data file.

        Returns:
            List of hotel dictionaries, or empty list on error.
        """
        if not os.path.exists(Hotel.DATA_FILE):
            return []
        try:
            with open(Hotel.DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                print("Error: Corrupted JSON file, expected a list.")
                return []
            return data
        except (json.JSONDecodeError, OSError) as exc:
            print(f"Error loading from file: {exc}")
            return []

    def _to_dict(self):
        """Convert the hotel instance to a dictionary.

        Returns:
            Dictionary representation of the hotel.
        """
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "rooms": self.rooms,
            "rooms_available": self.rooms_available,
        }
