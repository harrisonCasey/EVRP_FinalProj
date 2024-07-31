import pulp
import logging
import copy
from models.charging_station import ChargingStation
from models.fuel_station import FuelStation
from models.depot import Depot

class MILPOptimization:
    def __init__(self, depots, customers, vehicles, charging_stations, fuel_stations, optimization_criteria):
        """
        Initializes the MILPOptimization class.

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
        self.vehicles = vehicles
        self.charging_stations = charging_stations
        self.fuel_stations = fuel_stations
        self.optimization_criteria = optimization_criteria
        logging.basicConfig(level=logging.DEBUG)

    def optimize(self):
        """
        Solves the vehicle routing problem using MILP optimization.

        Returns:
            tuple: A tuple containing the solution, total distance, total emissions, and total delivery time.
        """
        num_locations = len(self.depots) + len(self.customers)
        num_customers = len(self.customers)
        num_depots = len(self.depots)
        num_vehicles = len(self.vehicles)

        prob = pulp.LpProblem("VehicleRoutingProblem", pulp.LpMinimize)

        # Variables
        x = pulp.LpVariable.dicts("x", (range(num_vehicles), range(num_locations), range(num_locations)), cat='Binary')
        u = pulp.LpVariable.dicts("u", (range(num_vehicles), range(num_locations)), lowBound=0, cat='Continuous')

        # Objective function
        if self.optimization_criteria == 'distance':
            prob += pulp.lpSum(self.calculate_distance(i, j) * x[v][i][j] for v in range(num_vehicles) for i in range(num_locations) for j in range(num_locations))
        elif self.optimization_criteria == 'emissions':
            prob += pulp.lpSum(self.calculate_emissions(v, self.calculate_distance(i, j)) * x[v][i][j] for v in range(num_vehicles) for i in range(num_locations) for j in range(num_locations))
        elif self.optimization_criteria == 'time':
            max_time = pulp.LpVariable("max_time", lowBound=0)
            prob += max_time
        else:
            raise ValueError("Invalid optimization criteria")

        # Constraints

        # Each customer must be visited exactly once
        for j in range(num_depots, num_locations):
            prob += pulp.lpSum(x[v][i][j] for v in range(num_vehicles) for i in range(num_locations) if i != j) == 1

        # Flow conservation constraint
        for v in range(num_vehicles):
            for h in range(num_depots, num_locations):
                prob += pulp.lpSum(x[v][i][h] for i in range(num_locations) if i != h) - pulp.lpSum(x[v][h][j] for j in range(num_locations) if j != h) == 0

        # Subtour elimination constraint
        for v in range(num_vehicles):
            for i in range(num_depots, num_locations):
                for j in range(num_depots, num_locations):
                    if i != j:
                        prob += u[v][i] - u[v][j] + (num_customers + 1) * x[v][i][j] <= num_customers

        # Each location can be visited at most once by each vehicle
        for v in range(num_vehicles):
            for i in range(num_locations):
                prob += pulp.lpSum(x[v][i][j] for j in range(num_locations) if i != j) <= 1
                prob += pulp.lpSum(x[v][j][i] for j in range(num_locations) if i != j) <= 1

        # Each vehicle must start and end at the same depot
        for v in range(num_vehicles):
            prob += pulp.lpSum(x[v][d][i] for d in range(num_depots) for i in range(num_locations) if d != i) == 1
            prob += pulp.lpSum(x[v][i][d] for d in range(num_depots) for i in range(num_locations) if d != i) == 1

        # Each vehicle must visit at least one customer if it is used
        for v in range(num_vehicles):
            prob += pulp.lpSum(x[v][i][j] for i in range(num_depots) for j in range(num_depots, num_locations)) >= 1

        # Subtour elimination constraint
        for v in range(num_vehicles):
            for i in range(1, num_locations):
                for j in range(1, num_locations):
                    if i != j:
                        prob += u[v][i] - u[v][j] + num_locations * x[v][i][j] <= num_locations - 1

        # Ensure each vehicle starts and ends at the same depot
        for v in range(num_vehicles):
            for d in range(num_depots):
                prob += pulp.lpSum(x[v][d][i] for i in range(num_locations) if i != d) == pulp.lpSum(x[v][i][d] for i in range(num_locations) if i != d)

        # Time constraint for each vehicle
        if self.optimization_criteria == 'time':
            for v in range(num_vehicles):
                total_time_expr = pulp.lpSum(self.calculate_distance(i, j) * x[v][i][j] for i in range(num_locations) for j in range(num_locations))
                for loc in range(num_locations):
                    if isinstance(self.get_location(loc), (ChargingStation)):
                        total_time_expr += self.get_location(loc).charging_speed * pulp.lpSum(x[v][loc][j] for j in range(num_locations))
                prob += total_time_expr <= max_time

        # Solve the problem
        solver = pulp.PULP_CBC_CMD(msg=False)
        prob.solve(solver)

        # Extract the solution
        solution = self.extract_solution(x)
        solution = self.add_refueling_stops(solution)
        total_distance = self.calculate_total_distance(solution)
        total_emissions = self.calculate_total_emissions(solution)
        total_delivery_time = self.calculate_parallel_delivery_time(solution)

        # Logging range checks
        for v in range(num_vehicles):
            vehicle_total_distance = self.calculate_total_distance({v: solution[v]})
            logging.debug(f"Vehicle {v}: Total distance traveled = {vehicle_total_distance}, Range = {self.vehicles[v].range}")
            if vehicle_total_distance > self.vehicles[v].range:
                logging.warning(f"Vehicle {v} exceeds its range limit!")

        return solution, total_distance, total_emissions, total_delivery_time

    def calculate_parallel_delivery_time(self, solution):
        """
        Calculates the maximum delivery time among all vehicles in the solution.

        Args:
            solution (dict): The solution containing routes for each vehicle.

        Returns:
            float: The maximum delivery time.
        """
        max_time = 0
        for vehicle_id, route in solution.items():
            vehicle = self.vehicles[vehicle_id]
            route_time = 0
            for i in range(len(route) - 1):
                route_time += self.calculate_distance(route[i].id, route[i + 1].id)
                if isinstance(route[i + 1], (ChargingStation)):
                    route_time += route[i + 1].charging_speed
            if route_time > max_time:
                max_time = route_time
        return max_time

    def calculate_distance(self, i, j):
        """
        Calculates the Euclidean distance between two locations.

        Args:
            i (int): The index of the first location.
            j (int): The index of the second location.

        Returns:
            float: The distance between the two locations.
        """
        point1 = self.get_location(int(i))
        point2 = self.get_location(int(j))
        return ((point1.location_x - point2.location_x) ** 2 + (point1.location_y - point2.location_y) ** 2) ** 0.5

    def calculate_emissions(self, vehicle_index, distance):
        """
        Calculates the emissions produced by a vehicle for a given distance.

        Args:
            vehicle_index (int): The index of the vehicle.
            distance (float): The distance traveled by the vehicle.

        Returns:
            float: The emissions produced by the vehicle.
        """
        vehicle = self.vehicles[vehicle_index]
        return vehicle.emission_rate * distance

    def extract_solution(self, x):
        """
        Extracts the solution from the optimization variables.

        Args:
            x (dict): The optimization variables.

        Returns:
            dict: The solution containing routes for each vehicle.
        """
        solution = {v: [] for v in range(len(self.vehicles))}
        for v in range(len(self.vehicles)):
            visited = set()
            current_location = next((i for i in range(len(self.depots)) if any(pulp.value(x[v][i][j]) == 1 for j in range(len(self.depots) + len(self.customers)))), None)
            while current_location is not None:
                solution[v].append(self.get_location(current_location))
                visited.add(current_location)
                next_location = next((j for j in range(len(self.depots) + len(self.customers)) if pulp.value(x[v][current_location][j]) == 1 and j not in visited), None)
                if next_location is None:
                    break
                current_location = next_location

            # Ensure the route returns to the starting depot if it visited any customers
            if len(solution[v]) > 1:
                solution[v].append(solution[v][0])

        # Mark unused vehicles explicitly
        for vehicle_id in range(len(self.vehicles)):
            if vehicle_id not in solution:
                solution[vehicle_id] = []

        # Filter out vehicles that only travel between depots
        for vehicle_id, route in list(solution.items()):
            if all(isinstance(loc, Depot) for loc in route) and len(route) > 1:
                solution.pop(vehicle_id)
                logging.info(f"Vehicle {vehicle_id + 1} is unused.")

        return solution

    def get_location(self, index):
        """
        Gets the location object based on its index.

        Args:
            index (int): The index of the location.

        Returns:
            Location: The location object.
        """
        if index < len(self.depots):
            return self.depots[index]
        else:
            return self.customers[index - len(self.depots)]

    def calculate_total_distance(self, solution):
        """
        Calculates the total distance traveled by all vehicles in the solution.

        Args:
            solution (dict): The solution containing routes for each vehicle.

        Returns:
            float: The total distance traveled.
        """
        total_distance = 0
        for vehicle_id, route in solution.items():
            for i in range(len(route) - 1):
                total_distance += self.calculate_distance(route[i].id, route[i + 1].id)
        return total_distance

    def calculate_total_emissions(self, solution):
        """
        Calculates the total emissions produced by all vehicles in the solution.

        Args:
            solution (dict): The solution containing routes for each vehicle.

        Returns:
            float: The total emissions produced.
        """
        total_emissions = 0
        for vehicle_id, route in solution.items():
            vehicle = self.vehicles[vehicle_id]
            for i in range(len(route) - 1):
                total_emissions += self.calculate_emissions(vehicle_id, self.calculate_distance(route[i].id, route[i + 1].id))
        return total_emissions

    def calculate_total_delivery_time(self, solution):
        """
        Calculates the total delivery time for all vehicles in the solution.

        Args:
            solution (dict): The solution containing routes for each vehicle.

        Returns:
            float: The total delivery time.
        """
        total_delivery_time = 0
        for vehicle_id, route in solution.items():
            for i in range(len(route) - 1):
                total_delivery_time += self.calculate_distance(route[i].id, route[i + 1].id)
            # Add refueling/recharging time
            for loc in route:
                if isinstance(loc, (ChargingStation, FuelStation)):
                    total_delivery_time += loc.charging_speed
        return total_delivery_time

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
                distance = self.calculate_distance(route[i].id, route[i + 1].id)
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
            distance = self.calculate_distance(current_location.id, station.id)
            if distance < min_distance:
                min_distance = distance
                nearest_station = station
        logging.debug(f"Nearest station to {type(current_location).__name__} {current_location.id} is {type(nearest_station).__name__} {nearest_station.id} at distance {min_distance}")
        return nearest_station

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
        distance_to_next = self.calculate_distance(current_location.id, next_location.id)
        nearest_station_distance = float('inf')
        if vehicle.vehicle_type == 'electric':
            nearest_station_distance = min(self.calculate_distance(next_location.id, station.id) for station in self.charging_stations)
        else:
            nearest_station_distance = min(self.calculate_distance(next_location.id, station.id) for station in self.fuel_stations)

        logging.debug(f"Vehicle {vehicle.id} checking if it can reach {type(next_location).__name__} {next_location.id}. Distance to next: {distance_to_next}, nearest station distance: {nearest_station_distance}, remaining range: {vehicle.remaining_range}")
        return vehicle.remaining_range >= distance_to_next + nearest_station_distance
