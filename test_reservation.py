"""Unit tests for the Reservation class."""

import json
import os
import unittest

from customer import Customer
from hotel import Hotel
from reservation import Reservation


class TestReservation(unittest.TestCase):
    """Test cases for Reservation CRUD operations."""

    def setUp(self):
        """Set up test fixtures with separate test data files."""
        self.orig_res_file = Reservation.DATA_FILE
        self.orig_hotel_file = Hotel.DATA_FILE
        self.orig_cust_file = Customer.DATA_FILE

        data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.test_res_file = os.path.join(
            data_dir, "test_reservations.json"
        )
        self.test_hotel_file = os.path.join(
            data_dir, "test_hotels.json"
        )
        self.test_cust_file = os.path.join(
            data_dir, "test_customers.json"
        )

        Reservation.DATA_FILE = self.test_res_file
        Hotel.DATA_FILE = self.test_hotel_file
        Customer.DATA_FILE = self.test_cust_file

        Reservation.save_to_file([])
        Hotel.save_to_file([])
        Customer.save_to_file([])

        hotel = Hotel("H001", "Grand Hotel", "New York", 5)
        hotel.create_hotel()

        customer = Customer("C001", "John Doe", "john@mail.com")
        customer.create_customer()

    def tearDown(self):
        """Remove test data files and restore original paths."""
        for path in (
            self.test_res_file,
            self.test_hotel_file,
            self.test_cust_file,
        ):
            if os.path.exists(path):
                os.remove(path)

        Reservation.DATA_FILE = self.orig_res_file
        Hotel.DATA_FILE = self.orig_hotel_file
        Customer.DATA_FILE = self.orig_cust_file

    # ---- Positive test cases ----

    def test_create_reservation_success(self):
        """Test that a valid reservation is created successfully."""
        res = Reservation("R001", "C001", "H001")
        result = res.create_reservation()
        self.assertTrue(result)
        reservations = Reservation.load_from_file()
        self.assertEqual(len(reservations), 1)
        self.assertEqual(
            reservations[0]["reservation_id"], "R001"
        )

    def test_cancel_reservation_success(self):
        """Test that an existing reservation is cancelled."""
        res = Reservation("R001", "C001", "H001")
        res.create_reservation()
        result = Reservation.cancel_reservation("R001")
        self.assertTrue(result)
        reservations = Reservation.load_from_file()
        self.assertEqual(len(reservations), 0)

    def test_display_reservation_info_success(self):
        """Test that reservation info is displayed and returned."""
        res = Reservation("R001", "C001", "H001")
        res.create_reservation()
        result = Reservation.display_reservation_info("R001")
        self.assertIsNotNone(result)
        self.assertEqual(result["customer_id"], "C001")
        self.assertEqual(result["hotel_id"], "H001")

    def test_create_reservation_decrements_rooms(self):
        """Test that creating a reservation decrements availability."""
        res = Reservation("R001", "C001", "H001")
        res.create_reservation()
        info = Hotel.display_hotel_info("H001")
        self.assertEqual(info["rooms_available"], 4)

    def test_cancel_reservation_increments_rooms(self):
        """Test that cancelling a reservation increments availability."""
        res = Reservation("R001", "C001", "H001")
        res.create_reservation()
        Reservation.cancel_reservation("R001")
        info = Hotel.display_hotel_info("H001")
        self.assertEqual(info["rooms_available"], 5)

    # ---- Negative test cases ----

    def test_create_reservation_customer_not_found(self):
        """Test that reservation fails with invalid customer."""
        res = Reservation("R001", "INVALID", "H001")
        result = res.create_reservation()
        self.assertFalse(result)

    def test_create_reservation_hotel_not_found(self):
        """Test that reservation fails with invalid hotel."""
        res = Reservation("R001", "C001", "INVALID")
        result = res.create_reservation()
        self.assertFalse(result)

    def test_create_reservation_no_rooms(self):
        """Test that reservation fails when no rooms available."""
        for i in range(5):
            res = Reservation(f"R{i}", "C001", "H001")
            res.create_reservation()
        res_full = Reservation("R999", "C001", "H001")
        result = res_full.create_reservation()
        self.assertFalse(result)

    def test_create_reservation_duplicate_id(self):
        """Test that creating a reservation with duplicate ID fails."""
        res = Reservation("R001", "C001", "H001")
        res.create_reservation()
        duplicate = Reservation("R001", "C001", "H001")
        result = duplicate.create_reservation()
        self.assertFalse(result)

    def test_cancel_reservation_not_found(self):
        """Test that cancelling a non-existent reservation fails."""
        result = Reservation.cancel_reservation("INVALID")
        self.assertFalse(result)

    def test_display_reservation_not_found(self):
        """Test that displaying non-existent reservation is None."""
        result = Reservation.display_reservation_info("INVALID")
        self.assertIsNone(result)

    def test_load_corrupted_json(self):
        """Test that a corrupted JSON file returns empty list."""
        with open(
            self.test_res_file, "w", encoding="utf-8"
        ) as file:
            file.write("{corrupted data}")
        result = Reservation.load_from_file()
        self.assertEqual(result, [])

    def test_load_non_list_json(self):
        """Test that a JSON file with non-list data is handled."""
        with open(
            self.test_res_file, "w", encoding="utf-8"
        ) as file:
            json.dump({"not": "a list"}, file)
        result = Reservation.load_from_file()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
