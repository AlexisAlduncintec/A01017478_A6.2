"""Unit tests for the Hotel class."""

import json
import os
import unittest

from hotel import Hotel


class TestHotel(unittest.TestCase):
    """Test cases for Hotel CRUD operations."""

    def setUp(self):
        """Set up test fixtures and backup original data file."""
        self.original_file = Hotel.DATA_FILE
        self.test_file = os.path.join(
            os.path.dirname(__file__), "data", "test_hotels.json"
        )
        Hotel.DATA_FILE = self.test_file
        Hotel.save_to_file([])
        self.hotel = Hotel("H001", "Grand Hotel", "New York", 100)

    def tearDown(self):
        """Remove test data file and restore original path."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        Hotel.DATA_FILE = self.original_file

    # ---- Positive test cases ----

    def test_create_hotel_success(self):
        """Test that a valid hotel is created successfully."""
        result = self.hotel.create_hotel()
        self.assertTrue(result)
        hotels = Hotel.load_from_file()
        self.assertEqual(len(hotels), 1)
        self.assertEqual(hotels[0]["hotel_id"], "H001")
        self.assertEqual(hotels[0]["name"], "Grand Hotel")

    def test_delete_hotel_success(self):
        """Test that an existing hotel is deleted successfully."""
        self.hotel.create_hotel()
        result = Hotel.delete_hotel("H001")
        self.assertTrue(result)
        hotels = Hotel.load_from_file()
        self.assertEqual(len(hotels), 0)

    def test_display_hotel_info_success(self):
        """Test that hotel info is displayed and returned."""
        self.hotel.create_hotel()
        result = Hotel.display_hotel_info("H001")
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Grand Hotel")
        self.assertEqual(result["location"], "New York")
        self.assertEqual(result["rooms"], 100)

    def test_modify_hotel_info_success(self):
        """Test that hotel attributes are modified correctly."""
        self.hotel.create_hotel()
        result = Hotel.modify_hotel_info(
            "H001", name="Updated Hotel", location="Boston"
        )
        self.assertTrue(result)
        info = Hotel.display_hotel_info("H001")
        self.assertEqual(info["name"], "Updated Hotel")
        self.assertEqual(info["location"], "Boston")

    def test_reserve_room_success(self):
        """Test that a room is reserved successfully."""
        self.hotel.create_hotel()
        result = Hotel.reserve_room("H001")
        self.assertTrue(result)
        info = Hotel.display_hotel_info("H001")
        self.assertEqual(info["rooms_available"], 99)

    def test_cancel_reservation_success(self):
        """Test that a reservation is cancelled successfully."""
        self.hotel.create_hotel()
        Hotel.reserve_room("H001")
        result = Hotel.cancel_reservation("H001")
        self.assertTrue(result)
        info = Hotel.display_hotel_info("H001")
        self.assertEqual(info["rooms_available"], 100)

    # ---- Negative test cases ----

    def test_create_hotel_empty_name(self):
        """Test that creating a hotel with empty name fails."""
        hotel = Hotel("H002", "", "Miami", 50)
        result = hotel.create_hotel()
        self.assertFalse(result)

    def test_create_hotel_invalid_rooms(self):
        """Test that negative room count defaults to zero."""
        hotel = Hotel("H003", "Bad Hotel", "Dallas", -5)
        self.assertEqual(hotel.rooms, 0)
        self.assertEqual(hotel.rooms_available, 0)

    def test_create_hotel_duplicate_id(self):
        """Test that creating a hotel with duplicate ID fails."""
        self.hotel.create_hotel()
        duplicate = Hotel("H001", "Another Hotel", "Chicago", 50)
        result = duplicate.create_hotel()
        self.assertFalse(result)

    def test_delete_hotel_not_found(self):
        """Test that deleting a non-existent hotel fails."""
        result = Hotel.delete_hotel("INVALID")
        self.assertFalse(result)

    def test_display_hotel_not_found(self):
        """Test that displaying a non-existent hotel returns None."""
        result = Hotel.display_hotel_info("INVALID")
        self.assertIsNone(result)

    def test_reserve_room_no_availability(self):
        """Test that reserving with no rooms available fails."""
        hotel = Hotel("H004", "Tiny Hotel", "Austin", 1)
        hotel.create_hotel()
        Hotel.reserve_room("H004")
        result = Hotel.reserve_room("H004")
        self.assertFalse(result)

    def test_reserve_room_hotel_not_found(self):
        """Test that reserving in a non-existent hotel fails."""
        result = Hotel.reserve_room("INVALID")
        self.assertFalse(result)

    def test_modify_hotel_not_found(self):
        """Test that modifying a non-existent hotel fails."""
        result = Hotel.modify_hotel_info("INVALID", name="New Name")
        self.assertFalse(result)

    def test_modify_hotel_invalid_values(self):
        """Test that modifying with invalid name or rooms fails."""
        self.hotel.create_hotel()
        result_name = Hotel.modify_hotel_info("H001", name="")
        self.assertFalse(result_name)
        result_rooms = Hotel.modify_hotel_info("H001", rooms=-10)
        self.assertFalse(result_rooms)

    def test_cancel_reservation_hotel_not_found(self):
        """Test that cancelling in a non-existent hotel fails."""
        result = Hotel.cancel_reservation("INVALID")
        self.assertFalse(result)

    def test_load_corrupted_json(self):
        """Test that a corrupted JSON file returns empty list."""
        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write("{corrupted data}")
        result = Hotel.load_from_file()
        self.assertEqual(result, [])

    def test_load_non_list_json(self):
        """Test that a JSON file with non-list data is handled."""
        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump({"not": "a list"}, file)
        result = Hotel.load_from_file()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
