class FuelStation:
    """
    Represents a fuel station in the routing problem.
    """

    def __init__(self, location_x, location_y, station_type, id):
        """
        Initializes a FuelStation object.

        Args:
            location_x (float): The x-coordinate of the fuel station's location.
            location_y (float): The y-coordinate of the fuel station's location.
            station_type (str): The type of the fuel station.
            id (int): The unique identifier of the fuel station.
        """
        self.id = id
        self.location_x = location_x
        self.location_y = location_y
        self.station_type = station_type

    def __repr__(self):
        """
        Returns a string representation of the FuelStation object.

        Returns:
            str: A string representation of the FuelStation object.
        """
        return f"<FuelStation {self.id} ({self.station_type}) at ({self.location_x}, {self.location_y})>"
