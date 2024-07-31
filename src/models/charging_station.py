class ChargingStation:
    """
    Represents a charging station in the routing problem.
    """

    def __init__(self, location_x, location_y, station_type, charging_speed, id):
        """
        Initializes a ChargingStation object.

        Args:
            location_x (float): The x-coordinate of the charging station's location.
            location_y (float): The y-coordinate of the charging station's location.
            station_type (str): The type of the charging station.
            charging_speed (float): The charging speed of the station.
            id (int): The unique identifier of the charging station.
        """
        self.id = id
        self.location_x = location_x
        self.location_y = location_y
        self.station_type = station_type
        self.charging_speed = charging_speed

    def __repr__(self):
        """
        Returns a string representation of the ChargingStation object.

        Returns:
            str: A string representation of the ChargingStation object.
        """
        return f"<ChargingStation {self.id} ({self.station_type}) at ({self.location_x}, {self.location_y})>"
