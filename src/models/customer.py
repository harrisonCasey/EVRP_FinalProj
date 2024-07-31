class Customer:
    """
    Represents a customer in the routing problem.
    """

    def __init__(self, location_x, location_y, packages, id):
        """
        Initializes a Customer object.

        Args:
            location_x (float): The x-coordinate of the customer's location.
            location_y (float): The y-coordinate of the customer's location.
            packages (list): A list of packages associated with the customer.
            id (int): The unique identifier of the customer.
        """
        self.location_x = location_x
        self.location_y = location_y
        self.packages = packages
        self.id = id

    def __repr__(self):
        """
        Returns a string representation of the Customer object.

        Returns:
            str: A string representation of the Customer object.
        """
        return f"<Customer {self.id} at ({self.location_x}, {self.location_y})>"
