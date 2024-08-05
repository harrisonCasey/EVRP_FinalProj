import pulp
import logging
from itertools import product

class MILPOptimization:
    def __init__(self, depots, customers, vehicles, charging_stations, fuel_stations, optimization_criteria, initial_solution=None):
        self.depots = depots
        self.customers = customers
        self.vehicles = vehicles
        self.charging_stations = charging_stations
        self.fuel_stations = fuel_stations
        self.optimization_criteria = optimization_criteria
        self.locations = depots + customers + charging_stations + fuel_stations
        self.distance_matrix = self.calculate_distance_matrix()
        self.initial_solution = initial_solution
        logging.basicConfig(level=logging.DEBUG)

    def calculate_distance_matrix(self):
            """
            Calculates the distance matrix between all locations.

            Returns:
                distance_matrix (dict): A dictionary representing the distance matrix.
                    The keys are the indices of the locations, and the values are dictionaries
                    representing the distances between each pair of locations.
            """
            distance_matrix = {}
            for i, loc1 in enumerate(self.locations):
                distance_matrix[i] = {}
                for j, loc2 in enumerate(self.locations):
                    if i != j:
                        distance_matrix[i][j] = self.calculate_distance(loc1, loc2)
                    else:
                        distance_matrix[i][j] = 0
            return distance_matrix

    def calculate_distance(self, loc1, loc2):
            """
            Calculates the Euclidean distance between two locations.

            Args:
                loc1 (Location): The first location.
                loc2 (Location): The second location.

            Returns:
                float: The Euclidean distance between the two locations.
            """
            return ((loc1.location_x - loc2.location_x) ** 2 + (loc1.location_y - loc2.location_y) ** 2) ** 0.5

    def calculate_emissions(self, vehicle, distance):
            """
            Calculates the emissions produced by a vehicle for a given distance.

            Args:
                vehicle (Vehicle): The vehicle for which emissions are calculated.
                distance (float): The distance traveled by the vehicle.

            Returns:
                float: The emissions produced by the vehicle for the given distance.
            """
            return vehicle.calculate_emissions(distance)

    def optimize(self):
        """
        Optimizes the MILP problem using the specified optimization criteria.

        Returns:
            tuple: A tuple containing the optimized routes, total distance, total emissions, and maximum delivery time.
        """
        logging.debug("Starting optimization with MILP...")
        num_locations = len(self.locations)
        num_customers = len(self.customers)
        num_vehicles = len(self.vehicles)

        problem = pulp.LpProblem("GVRP", pulp.LpMinimize)
        
        x = pulp.LpVariable.dicts("x", (range(num_locations), range(num_locations), range(num_vehicles)), cat='Binary')
        u = pulp.LpVariable.dicts("u", (range(num_vehicles), range(num_locations)), lowBound=0, cat='Continuous')

        # Objective function based on optimization criteria
        if self.optimization_criteria == 'distance':
            problem += pulp.lpSum(self.distance_matrix[i][j] * x[i][j][k] 
                                  for i in range(num_locations) for j in range(num_locations) 
                                  for k in range(num_vehicles))
        elif self.optimization_criteria == 'emissions':
            problem += pulp.lpSum(self.calculate_emissions(self.vehicles[k], self.distance_matrix[i][j]) * x[i][j][k] 
                                  for i in range(num_locations) for j in range(num_locations) 
                                  for k in range(num_vehicles))
        elif self.optimization_criteria == 'time':
            max_time = pulp.LpVariable('max_time', lowBound=0)
            problem += max_time
            for k in range(num_vehicles):
                problem += (pulp.lpSum(self.distance_matrix[i][j] * x[i][j][k] 
                                       for i in range(num_locations) for j in range(num_locations)) <= max_time, 
                            f"MaxTimeConstraint_{k}")
        else:
            raise ValueError("Invalid optimization criteria")

        # Each vehicle starts and ends at the same depot
        for k in range(num_vehicles):
            for d in range(len(self.depots)):
                problem += (pulp.lpSum(x[d][j][k] for j in range(num_locations) if d != j) == 1, f"StartAtDepot_{k}_{d}")
                problem += (pulp.lpSum(x[i][d][k] for i in range(num_locations) if i != d) == 1, f"EndAtDepot_{k}_{d}")

        # Each customer is visited exactly once by one vehicle
        for j in range(len(self.depots), len(self.depots) + num_customers):
            problem += (pulp.lpSum(x[i][j][k] for i in range(num_locations) for k in range(num_vehicles) if i != j) == 1, f"VisitCustomer_{j}")
            problem += (pulp.lpSum(x[j][i][k] for i in range(num_locations) for k in range(num_vehicles) if i != j) == 1, f"LeaveCustomer_{j}")

        # Flow conservation constraints
        for k in range(num_vehicles):
            for h in range(len(self.depots), len(self.depots) + num_customers):
                problem += (pulp.lpSum(x[i][h][k] for i in range(num_locations) if i != h) - 
                            pulp.lpSum(x[h][j][k] for j in range(num_locations) if j != h) == 0, f"FlowConservation_{k}_{h}")

        # Subtour elimination constraints
        for k in range(num_vehicles):
            for i in range(1, num_locations):
                for j in range(1, num_locations):
                    if i != j:
                        problem += u[k][i] - u[k][j] + num_locations * x[i][j][k] <= num_locations - 1

        # Vehicle range constraints
        for k in range(num_vehicles):
            vehicle_range = self.vehicles[k].range
            for i, j in product(range(num_locations), repeat=2):
                if i != j:
                    nearest_station_distance = self.find_nearest_station_distance(j, self.vehicles[k])
                    problem += (self.distance_matrix[i][j] * x[i][j][k] <= vehicle_range - nearest_station_distance, f"RangeConstraint_{k}_{i}_{j}")

        # Initial solution constraints (if provided)
        if self.initial_solution:
            for k, route in self.initial_solution.items():
                for i in range(len(route) - 1):
                    loc_i = self.find_location_index(route[i])
                    loc_j = self.find_location_index(route[i + 1])
                    problem += x[loc_i][loc_j][k] == 1, f"InitialSolution_{k}_{loc_i}_{loc_j}"

        # Solver with verbosity and logging intermediate solutions
        solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=180)  # Set a time limit and a higher relative gap for faster solutions
        logging.info("Solving the MILP problem with CBC solver...")
        problem.solve(solver)

        if pulp.LpStatus[problem.status] == 'Optimal':
            logging.info("Optimal solution found.")
            routes = self.extract_solution(x)
            total_distance, total_emissions, total_delivery_time = self.calculate_cost(routes)
            return routes, total_distance, total_emissions, total_delivery_time
        else:
            logging.warning(f"Solver status: {pulp.LpStatus[problem.status]}.")
            routes = self.extract_solution(x)
            total_distance, total_emissions, total_delivery_time = self.calculate_cost(routes)
            return routes, total_distance, total_emissions, total_delivery_time

    def find_location_index(self, location):
        for idx, loc in enumerate(self.locations):
            if loc.id == location.id and type(loc) == type(location):
                return idx
        raise ValueError(f"{location} is not in list")

    def extract_solution(self, x):
        """
        Extracts the solution from the MILP optimization problem.

        Args:
            x: The decision variable matrix representing the routes.

        Returns:
            dict: A dictionary containing the routes for each vehicle.

        """
        routes = {k: [] for k in range(len(self.vehicles))}
        for k in range(len(self.vehicles)):
            current_route = []
            current_location = None
            for i in range(len(self.locations)):
                for j in range(len(self.locations)):
                    if pulp.value(x[i][j][k]) == 1:
                        if current_location is None:
                            current_location = i
                            current_route.append(self.locations[i])
                        current_route.append(self.locations[j])
                        current_location = j
                        break
            # Check if the vehicle actually visited any customers
            if any(isinstance(loc, type(self.customers[0])) for loc in current_route):
                if current_route and current_route[0] != current_route[-1]:
                    current_route.append(current_route[0])
                routes[k] = current_route
            else:
                routes[k] = []
        return routes

    def calculate_cost(self, routes):
        """
        Calculates the total distance, total emissions, and maximum delivery time for the given routes.

        Args:
            routes (dict): A dictionary containing the routes for each vehicle.

        Returns:
            tuple: A tuple containing the total distance, total emissions, and maximum delivery time.
        """
        total_distance = 0
        total_emissions = 0
        total_delivery_time = 0
        
        for vehicle_idx, route in routes.items():
            if route:  # Only consider vehicles that have a valid route
                vehicle = self.vehicles[vehicle_idx]
                vehicle_distance = 0
                vehicle_emissions = 0
                vehicle_time = 0

                for loc in route:
                    if route.index(loc) > 0:
                        prev_loc = route[route.index(loc) - 1]
                        distance = self.distance_matrix[self.locations.index(prev_loc)][self.locations.index(loc)]
                        vehicle_distance += distance
                        vehicle_emissions += vehicle.calculate_emissions(distance)
                        vehicle_time += distance

                total_distance += vehicle_distance
                total_emissions += vehicle_emissions
                total_delivery_time = max(total_delivery_time, vehicle_time)  # Max time for parallel routes

        return total_distance, total_emissions, total_delivery_time

    def find_nearest_station_distance(self, loc_index, vehicle):
        """
        Finds the nearest station distance for a given location and vehicle.

        Args:
            loc_index (int): The index of the location.
            vehicle (Vehicle): The vehicle for which the nearest station distance is calculated.

        Returns:
            float: The nearest station distance.
        """
        nearest_station_distance = float('inf')
        if vehicle.vehicle_type == 'electric':
            for station in self.charging_stations:
                distance = self.calculate_distance(self.locations[loc_index], station)
                if distance < nearest_station_distance:
                    nearest_station_distance = distance
        else:
            for station in self.fuel_stations:
                distance = self.calculate_distance(self.locations[loc_index], station)
                if distance < nearest_station_distance:
                    nearest_station_distance = distance
        return nearest_station_distance
