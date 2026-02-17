"""Unit tests for the Customer class."""

import json
import os
import unittest

from customer import Customer


class TestCustomer(unittest.TestCase):
    """Test cases for Customer CRUD operations."""

    def setUp(self):
        """Set up test fixtures and redirect to test data file."""
        self.original_file = Customer.DATA_FILE
        self.test_file = os.path.join(
            os.path.dirname(__file__), "data", "test_customers.json"
        )
        Customer.DATA_FILE = self.test_file
        Customer.save_to_file([])
        self.customer = Customer("C001", "John Doe", "john@mail.com")

    def tearDown(self):
        """Remove test data file and restore original path."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        Customer.DATA_FILE = self.original_file

    # ---- Positive test cases ----

    def test_create_customer_success(self):
        """Test that a valid customer is created successfully."""
        result = self.customer.create_customer()
        self.assertTrue(result)
        customers = Customer.load_from_file()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]["customer_id"], "C001")
        self.assertEqual(customers[0]["name"], "John Doe")
        self.assertEqual(customers[0]["email"], "john@mail.com")

    def test_delete_customer_success(self):
        """Test that an existing customer is deleted successfully."""
        self.customer.create_customer()
        result = Customer.delete_customer("C001")
        self.assertTrue(result)
        customers = Customer.load_from_file()
        self.assertEqual(len(customers), 0)

    def test_display_customer_info_success(self):
        """Test that customer info is displayed and returned."""
        self.customer.create_customer()
        result = Customer.display_customer_info("C001")
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["email"], "john@mail.com")

    def test_modify_customer_info_success(self):
        """Test that customer attributes are modified correctly."""
        self.customer.create_customer()
        result = Customer.modify_customer_info(
            "C001", name="Jane Doe", email="jane@mail.com"
        )
        self.assertTrue(result)
        info = Customer.display_customer_info("C001")
        self.assertEqual(info["name"], "Jane Doe")
        self.assertEqual(info["email"], "jane@mail.com")

    # ---- Negative test cases ----

    def test_create_customer_empty_name(self):
        """Test that creating a customer with empty name fails."""
        customer = Customer("C002", "", "test@mail.com")
        result = customer.create_customer()
        self.assertFalse(result)

    def test_create_customer_invalid_email(self):
        """Test that creating a customer with invalid email fails."""
        customer = Customer("C003", "Bad Email", "no-at-sign")
        result = customer.create_customer()
        self.assertFalse(result)

    def test_create_customer_duplicate_id(self):
        """Test that creating a customer with duplicate ID fails."""
        self.customer.create_customer()
        duplicate = Customer("C001", "Other Name", "other@mail.com")
        result = duplicate.create_customer()
        self.assertFalse(result)

    def test_delete_customer_not_found(self):
        """Test that deleting a non-existent customer fails."""
        result = Customer.delete_customer("INVALID")
        self.assertFalse(result)

    def test_display_customer_not_found(self):
        """Test that displaying a non-existent customer returns None."""
        result = Customer.display_customer_info("INVALID")
        self.assertIsNone(result)

    def test_modify_customer_not_found(self):
        """Test that modifying a non-existent customer fails."""
        result = Customer.modify_customer_info(
            "INVALID", name="New Name"
        )
        self.assertFalse(result)

    def test_modify_customer_invalid_email(self):
        """Test that modifying with invalid email fails."""
        self.customer.create_customer()
        result = Customer.modify_customer_info(
            "C001", email="no-at-sign"
        )
        self.assertFalse(result)

    def test_modify_customer_empty_name(self):
        """Test that modifying with empty name fails."""
        self.customer.create_customer()
        result = Customer.modify_customer_info("C001", name="")
        self.assertFalse(result)

    def test_load_corrupted_json(self):
        """Test that a corrupted JSON file returns empty list."""
        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write("{corrupted data}")
        result = Customer.load_from_file()
        self.assertEqual(result, [])

    def test_load_non_list_json(self):
        """Test that a JSON file with non-list data is handled."""
        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump({"not": "a list"}, file)
        result = Customer.load_from_file()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
