"""Customer module for managing customer entities and persistence."""

import json
import os


class Customer:
    """Represents a customer and supports CRUD operations."""

    DATA_FILE = os.path.join(
        os.path.dirname(__file__), "data", "customers.json"
    )

    def __init__(self, customer_id, name, email):
        """Initialize a Customer instance.

        Args:
            customer_id: Unique identifier for the customer.
            name: Name of the customer.
            email: Email address of the customer.
        """
        self.customer_id = str(customer_id)
        self.name = name
        self.email = email

    def create_customer(self):
        """Add this customer to the JSON data file.

        Returns:
            True if created successfully, False otherwise.
        """
        if not self.name or not isinstance(self.name, str):
            print("Error: Customer name must be a non-empty string.")
            return False

        if not self._is_valid_email(self.email):
            print("Error: Invalid email format, must contain '@'.")
            return False

        customers = Customer.load_from_file()

        for customer in customers:
            if customer["customer_id"] == self.customer_id:
                print(f"Error: Customer with id '{self.customer_id}' "
                      f"already exists.")
                return False

        customers.append(self._to_dict())
        Customer.save_to_file(customers)
        return True

    @staticmethod
    def delete_customer(customer_id):
        """Remove a customer from the JSON data file.

        Args:
            customer_id: ID of the customer to delete.

        Returns:
            True if deleted successfully, False otherwise.
        """
        customer_id = str(customer_id)
        customers = Customer.load_from_file()
        updated = [c for c in customers
                   if c["customer_id"] != customer_id]

        if len(updated) == len(customers):
            print(f"Error: Customer with id '{customer_id}' not found.")
            return False

        Customer.save_to_file(updated)
        return True

    @staticmethod
    def display_customer_info(customer_id):
        """Display customer information.

        Args:
            customer_id: ID of the customer to display.

        Returns:
            Dictionary with customer info, or None if not found.
        """
        customer_id = str(customer_id)
        customers = Customer.load_from_file()

        for customer in customers:
            if customer["customer_id"] == customer_id:
                print(f"Customer ID: {customer['customer_id']}")
                print(f"Name: {customer['name']}")
                print(f"Email: {customer['email']}")
                return customer

        print(f"Error: Customer with id '{customer_id}' not found.")
        return None

    @staticmethod
    def modify_customer_info(customer_id, **kwargs):
        """Update customer attributes in the JSON data file.

        Args:
            customer_id: ID of the customer to modify.
            **kwargs: Attributes to update (name, email).

        Returns:
            True if modified successfully, False otherwise.
        """
        customer_id = str(customer_id)
        customers = Customer.load_from_file()

        for customer in customers:
            if customer["customer_id"] == customer_id:
                if "name" in kwargs:
                    if not kwargs["name"] or not isinstance(
                        kwargs["name"], str
                    ):
                        print("Error: name must be a non-empty string.")
                        return False
                    customer["name"] = kwargs["name"]

                if "email" in kwargs:
                    if not Customer._is_valid_email(kwargs["email"]):
                        print("Error: Invalid email format, "
                              "must contain '@'.")
                        return False
                    customer["email"] = kwargs["email"]

                Customer.save_to_file(customers)
                return True

        print(f"Error: Customer with id '{customer_id}' not found.")
        return False

    @staticmethod
    def save_to_file(customers):
        """Save a list of customer dictionaries to the JSON data file.

        Args:
            customers: List of customer dictionaries to save.
        """
        try:
            with open(
                Customer.DATA_FILE, "w", encoding="utf-8"
            ) as file:
                json.dump(customers, file, indent=4)
        except (OSError, TypeError) as exc:
            print(f"Error saving to file: {exc}")

    @staticmethod
    def load_from_file():
        """Load customers from the JSON data file.

        Returns:
            List of customer dictionaries, or empty list on error.
        """
        if not os.path.exists(Customer.DATA_FILE):
            return []
        try:
            with open(
                Customer.DATA_FILE, "r", encoding="utf-8"
            ) as file:
                data = json.load(file)
            if not isinstance(data, list):
                print("Error: Corrupted JSON file, expected a list.")
                return []
            return data
        except (json.JSONDecodeError, OSError) as exc:
            print(f"Error loading from file: {exc}")
            return []

    @staticmethod
    def _is_valid_email(email):
        """Check if an email address has a valid format.

        Args:
            email: Email string to validate.

        Returns:
            True if valid, False otherwise.
        """
        return isinstance(email, str) and "@" in email

    def _to_dict(self):
        """Convert the customer instance to a dictionary.

        Returns:
            Dictionary representation of the customer.
        """
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }
