class Depot:
    """
    Represents a depot in the routing problem.
    """

    def __init__(self, location_x, location_y, id):
        """
        Initializes a Depot object.

        Args:
            location_x (float): The x-coordinate of the depot's location.
            location_y (float): The y-coordinate of the depot's location.
            id (int): The unique identifier of the depot.
        """
        self.id = id
        self.location_x = location_x
        self.location_y = location_y

    def __repr__(self):
        """
        Returns a string representation of the Depot object.

        Returns:
            str: A string representation of the Depot object.
        """
        return f"<Depot {self.id} at ({self.location_x}, {self.location_y})>"
