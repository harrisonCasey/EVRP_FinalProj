import logging
from models.charging_station import ChargingStation
from models.fuel_station import FuelStation

class Vehicle:
    """
    Represents a vehicle in the routing problem.
    """
    def __init__(self, vehicle_type, range, recharge_time, id, emission_rate, package_capacity, port_type=None):
        """
        Initializes a Vehicle object.

        Args:
            vehicle_type (str): The type of the vehicle ('electric' or 'fossil').
            range (float): The maximum range of the vehicle.
            recharge_time (float): The time it takes to recharge the vehicle.
            id (int): The unique identifier of the vehicle.
            emission_rate (float): The emission rate of the vehicle.
            package_capacity (int): The maximum capacity of the vehicle for carrying packages.
            port_type (str, optional): The type of port the vehicle uses for charging. Defaults to None.
        """
        self.id = id
        self.vehicle_type = vehicle_type
        self.range = range
        self.recharge_time = recharge_time
        self.remaining_range = range
        self.emission_rate = emission_rate
        self.package_capacity = package_capacity
        self.port_type = port_type

    def calculate_emissions(self, distance):
        """
        Calculates emissions based on the distance traveled.

        Args:
            distance (float): The distance traveled.

        Returns:
            float: The emissions produced.
        """
        return distance * self.emission_rate

    def refuel_or_recharge(self, station):
        """
        Refuels or recharges the vehicle at a station.

        Args:
            station (Station): The station where the vehicle refuels or recharges.
        """
        logging.debug(f"Vehicle {self.id} refuel_or_recharge called with station: {station} (type: {type(station)})")
        
        if self.vehicle_type == 'electric' and isinstance(station, ChargingStation):
            logging.debug(f"Vehicle {self.id} is an electric vehicle and the station is a ChargingStation.")
            self.remaining_range = self.range
            logging.debug(f"Vehicle {self.id} recharged at ChargingStation {station.id}. Remaining range: {self.remaining_range}")
        elif self.vehicle_type == 'fossil' and isinstance(station, FuelStation):
            logging.debug(f"Vehicle {self.id} is a fossil vehicle and the station is a FuelStation.")
            self.remaining_range = self.range
            logging.debug(f"Vehicle {self.id} refueled at FuelStation {station.id}. Remaining range: {self.remaining_range}")
        else:
            logging.debug(f"Vehicle {self.id} could not refuel/recharge at the provided station. Type: {type(station)}")

    def travel(self, distance):
        """
        Travels the specified distance, updating the remaining range.

        Args:
            distance (float): The distance to travel.

        Returns:
            bool: True if the travel was successful, False otherwise.
        """
        logging.debug(f"Vehicle {self.id} attempting to travel {distance} units. Current range: {self.remaining_range}. Needed range: {distance}.")
        if self.remaining_range - distance < 0:
            logging.debug(f"Vehicle {self.id} cannot travel {distance} units. Remaining range: {self.remaining_range}.")
            return False
        self.remaining_range -= distance
        logging.debug(f"Vehicle {self.id} traveled {distance} units. Remaining range: {self.remaining_range}.")
        return True

    def needs_refuel_or_recharge(self):
        """
        Checks if the vehicle needs to refuel or recharge.

        Returns:
            bool: True if refuel or recharge is needed, False otherwise.
        """
        needs_refuel = self.remaining_range <= 0
        if needs_refuel:
            logging.info(f"Vehicle {self.id} needs to refuel/recharge.")
        return needs_refuel

    def __repr__(self):
        return f"<Vehicle {self.id} ({self.vehicle_type})>"
