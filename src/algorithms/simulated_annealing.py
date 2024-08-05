import random
import copy
import math
import logging
from models.fuel_station import FuelStation
from models.charging_station import ChargingStation

class SimulatedAnnealingOptimization:
    def __init__(self, depots, customers, vehicles, charging_stations, fuel_stations, optimization_criteria):
        """
        Initializes the SimulatedAnnealingOptimization class.

        Args:
            depots (list): List of depot locations.
            customers (list): List of customer locations.
            vehicles (list): List of vehicles.
            charging_stations (list): List of charging stations.
            fuel_stations (list): List of fuel stations.
            optimization_criteria (str): The optimization criteria ('distance', 'emissions', or 'time').
        """
        self.depots = depots
        self.customers = customers
        self.vehicles = sorted(vehicles, key=lambda v: v.emission_rate)
        self.charging_stations = charging_stations
        self.fuel_stations = fuel_stations
        self.optimization_criteria = optimization_criteria

    def optimize(self):
        """
        Optimizes the solution using the Simulated Annealing algorithm.

        Returns:
            tuple: The optimized solution, total distance, total emissions, and parallel delivery time.
        """
        best_solution = self.initial_solution()
        best_cost = self.calculate_cost(best_solution)

        temperature = 100.0
        cooling_rate = 0.003

        current_solution = best_solution
        current_cost = best_cost

        while temperature > 1.0:
            new_solution = self.perturb_solution(current_solution)
            new_cost = self.calculate_cost(new_solution)

            if new_cost < current_cost or random.uniform(0, 1) < self.acceptance_probability(current_cost, new_cost, temperature):
                current_solution = new_solution
                current_cost = new_cost

            if current_cost < best_cost:
                best_solution = current_solution
                best_cost = current_cost

            temperature *= 1 - cooling_rate

        for vehicle_id, route in best_solution.items():
            if route[0] != route[-1]:
                route.append(route[0])

        best_solution = self.add_refueling_stops(best_solution)

        return best_solution, self.calculate_total_distance(best_solution), self.calculate_total_emissions(best_solution), self.calculate_parallel_delivery_time(best_solution)

    def calculate_parallel_delivery_time(self, solution):
        """
        Calculates the maximum delivery time among all vehicles in the solution.

        Args:
            solution (dict): The solution to evaluate.

        Returns:
            float: The maximum delivery time.
        """
        max_time = 0
        for vehicle_id, route in solution.items():
            vehicle = self.vehicles[vehicle_id]
            route_time = 0
            for i in range(len(route) - 1):
                route_time += self.calculate_distance(route[i], route[i + 1])
                if isinstance(route[i + 1], (ChargingStation)):
                    if vehicle.vehicle_type == 'electric' and vehicle.port_type == 'fast':
                        route_time += route[i + 1].charging_speed * 0.5
                    elif vehicle.vehicle_type == 'electric' and vehicle.port_type == 'super':
                        route_time += route[i + 1].charging_speed * 0.25
                    else:
                        route_time += route[i + 1].charging_speed
            if route_time > max_time:
                max_time = route_time
        return max_time
    
    def initial_solution(self):
        """
        Generates an initial solution by randomly assigning customers to vehicles.

        Returns:
            dict: Initial solution with vehicle routes.
        """
        solution = {}
        depot_indices = list(range(len(self.depots)))
        random.shuffle(depot_indices)

        for i in range(len(self.vehicles)):
            depot = self.depots[depot_indices[i % len(depot_indices)]]
            solution[i] = [depot, depot]  # Start and end at depot

        for customer in self.customers:
            vehicle = random.choice(list(solution.keys()))
            solution[vehicle].insert(-1, customer)

        return solution

    def perturb_solution(self, solution):
        """
        Perturbs the solution by moving a customer from one vehicle's route to another.

        Args:
            solution (dict): The current solution.

        Returns:
            dict: The perturbed solution.
        """
        new_solution = copy.deepcopy(solution)
        vehicle_from = random.choice(list(new_solution.keys()))
        if len(new_solution[vehicle_from]) <= 3:  # 1 depot at start, 1 depot at end, 1 customer in between
            return new_solution
        customer = random.choice(new_solution[vehicle_from][1:-1])  # do not pick depot
        new_solution[vehicle_from].remove(customer)
        vehicle_to = random.choice(list(new_solution.keys()))
        new_solution[vehicle_to].insert(-1, customer)
        return new_solution


    def calculate_cost(self, solution):
        """
        Calculates the cost of a solution based on the chosen optimization criteria.

        Args:
            solution (dict): The solution to evaluate.

        Returns:
            float: The cost of the solution.
        """
        if self.optimization_criteria == 'distance':
            return self.calculate_total_distance(solution)
        elif self.optimization_criteria == 'emissions':
            return self.calculate_total_emissions(solution)
        elif self.optimization_criteria == 'time':
            return self.calculate_parallel_delivery_time(solution)
        else:
            raise ValueError("Invalid optimization criteria")

    def calculate_total_distance(self, solution):
        """
        Calculates the total distance traveled by all vehicles in the solution.

        Args:
            solution (dict): The solution to evaluate.

        Returns:
            float: The total distance traveled.
        """
        total_distance = 0
        for vehicle_id, route in solution.items():
            vehicle = self.vehicles[vehicle_id]
            for i in range(len(route) - 1):
                distance = self.calculate_distance(route[i], route[i + 1])
                logging.debug(f"Vehicle {vehicle.id} traveling from {type(route[i]).__name__} {route[i].id} to {type(route[i + 1]).__name__} {route[i + 1].id} with distance {distance}")
                total_distance += distance
        return total_distance

    def add_refueling_stops(self, solution):
        """
        Adds refueling or recharging stops to the vehicle routes if needed.

        Args:
            solution (dict): The current solution.

        Returns:
            dict: The solution with refueling stops added.
        """
        new_solution = copy.deepcopy(solution)
        for vehicle_id, route in new_solution.items():
            vehicle = self.vehicles[vehicle_id]
            vehicle.remaining_range = vehicle.range  # Reset the remaining range for each iteration
            i = 0
            while i < len(route) - 1:
                distance = self.calculate_distance(route[i], route[i + 1])
                if not self.can_reach_next_destination_and_station(vehicle, route[i], route[i + 1]):
                    logging.debug(f"Vehicle {vehicle.id} cannot reach {type(route[i + 1]).__name__} {route[i + 1].id} from {type(route[i]).__name__} {route[i].id} without refueling/recharging")
                    self.add_refuel_stop(vehicle, route, i)
                elif not vehicle.travel(distance):
                    logging.debug(f"Vehicle {vehicle.id} needs to refuel/recharge again at {type(route[i]).__name__} {route[i].id}")
                    self.add_refuel_stop(vehicle, route, i)
                    vehicle.travel(distance)
                i += 1
        return new_solution

    def add_refuel_stop(self, vehicle, route, i):
        """
        Adds a refuel or recharge stop to the route if the vehicle cannot travel the required distance.

        Args:
            vehicle (Vehicle): The vehicle that needs refueling.
            route (list): The route of the vehicle.
            i (int): The index in the route where refueling is needed.
        """
        if vehicle.vehicle_type == 'electric':
            station = self.find_nearest_station(route[i], self.charging_stations)
        else:
            station = self.find_nearest_station(route[i], self.fuel_stations)

        logging.debug(f"Vehicle {vehicle.id} refueling/recharging at {type(station).__name__} {station.id}. Current range: {vehicle.remaining_range}. Station location: ({station.location_x}, {station.location_y})")

        if route[i] != station:
            route.insert(i + 1, station)
            logging.debug(f"Vehicle {vehicle.id} added refuel/recharge stop at {type(station).__name__} {station.id} on route at index {i + 1}.")
            vehicle.refuel_or_recharge(station)

    def find_nearest_station(self, current_location, stations):
        """
        Finds the nearest station to the current location.

        Args:
            current_location (Location): The current location.
            stations (list): List of stations to search.

        Returns:
            Station: The nearest station.
        """
        min_distance = float('inf')
        nearest_station = None
        for station in stations:
            distance = self.calculate_distance(current_location, station)
            if distance < min_distance:
                min_distance = distance
                nearest_station = station
        logging.debug(f"Nearest station to {type(current_location).__name__} {current_location.id} is {type(nearest_station).__name__} {nearest_station.id} at distance {min_distance}")
        return nearest_station

    def calculate_total_emissions(self, solution):
        """
        Calculates the total emissions for the solution.

        Args:
            solution (dict): The solution to evaluate.

        Returns:
            float: The total emissions produced.
        """
        total_emissions = 0
        for vehicle_id, route in solution.items():
            vehicle = self.vehicles[vehicle_id]
            for i in range(len(route) - 1):
                distance = self.calculate_distance(route[i], route[i + 1])
                total_emissions += vehicle.calculate_emissions(distance)
        return total_emissions


    def calculate_distance(self, point1, point2):
        """
        Calculates the Euclidean distance between two points.

        Args:
            point1 (Location): The first point.
            point2 (Location): The second point.

        Returns:
            float: The Euclidean distance between the points.
        """
        return ((point1.location_x - point2.location_x) ** 2 + (point1.location_y - point2.location_y) ** 2) ** 0.5

    def can_reach_next_destination_and_station(self, vehicle, current_location, next_location):
        """
        Checks if the vehicle can reach the next location and a charging/refueling station from the next location.

        Args:
            vehicle (Vehicle): The vehicle to check.
            current_location (Location): The current location of the vehicle.
            next_location (Location): The next location the vehicle needs to travel to.

        Returns:
            bool: True if the vehicle can reach the next location and a station, False otherwise.
        """
        distance_to_next = self.calculate_distance(current_location, next_location)
        nearest_station_distance = float('inf')
        if vehicle.vehicle_type == 'electric':
            nearest_station_distance = min(self.calculate_distance(next_location, station) for station in self.charging_stations)
        else:
            nearest_station_distance = min(self.calculate_distance(next_location, station) for station in self.fuel_stations)

        logging.debug(f"Vehicle {vehicle.id} checking if it can reach {type(next_location).__name__} {next_location.id}. Distance to next: {distance_to_next}, nearest station distance: {nearest_station_distance}, remaining range: {vehicle.remaining_range}")
        return vehicle.remaining_range >= distance_to_next + nearest_station_distance

    def acceptance_probability(self, old_cost, new_cost, temperature):
        """
        Calculates the acceptance probability for a new solution.

        Args:
            old_cost (float): The cost of the current solution.
            new_cost (float): The cost of the new solution.
            temperature (float): The current temperature.

        Returns:
            float: The acceptance probability.
        """
        return 1 if new_cost < old_cost else math.exp((old_cost - new_cost) / temperature)
