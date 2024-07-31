import pytest
from src.models.vehicle import Vehicle
from src.models.depot import Depot
from src.models.customer import Customer
from src.models.charging_station import ChargingStation
from src.models.fuel_station import FuelStation
from src.algorithms.simulated_annealing import SimulatedAnnealingOptimization

# Define a fixture to provide mock data for the tests
@pytest.fixture
def mock_data():
    # Create depots
    depots = [
        Depot(0, 0, 1),
        Depot(10, 10, 2)
    ]
    # Create customers
    customers = [
        Customer(5, 5, 3, 1),
        Customer(15, 15, 5, 2)
    ]
    # Create vehicles
    vehicles = [
        Vehicle('electric', 100, 30, 1, 0.5, 50, 'fast'),
        Vehicle('fossil', 200, 0, 2, 2.0, 100, None)
    ]
    # Create charging stations
    charging_stations = [
        ChargingStation(7, 7, 'fast', 10, 1)
    ]
    # Create fuel stations
    fuel_stations = [
        FuelStation(3, 3, 'type1', 1)
    ]
    # Return the mock data
    return depots, customers, vehicles, charging_stations, fuel_stations

# Test the initial_solution() method
def test_initial_solution(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of the SimulatedAnnealingOptimization class
    optimizer = SimulatedAnnealingOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Get the initial solution
    solution = optimizer.initial_solution()
    # Assert that the length of the solution is equal to the number of vehicles
    assert len(solution) == len(vehicles)
    # Assert that each route starts and ends at a depot
    for route in solution.values():
        assert route[0] in depots
        assert route[-1] in depots
        # Assert that each customer is visited in the route
        for customer in route[1:-1]:
            assert customer in customers

# Test the calculate_total_distance() method
def test_calculate_total_distance(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of the SimulatedAnnealingOptimization class
    optimizer = SimulatedAnnealingOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Get the initial solution
    solution = optimizer.initial_solution()
    # Calculate the total distance of the solution
    total_distance = optimizer.calculate_total_distance(solution)
    # Assert that the total distance is greater than or equal to 0
    assert total_distance >= 0

# Test the calculate_total_emissions() method
def test_calculate_total_emissions(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of the SimulatedAnnealingOptimization class
    optimizer = SimulatedAnnealingOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'emissions')
    # Get the initial solution
    solution = optimizer.initial_solution()
    # Calculate the total emissions of the solution
    total_emissions = optimizer.calculate_total_emissions(solution)
    # Assert that the total emissions is greater than or equal to 0
    assert total_emissions >= 0

# Test the calculate_parallel_delivery_time() method
def test_calculate_parallel_delivery_time(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of the SimulatedAnnealingOptimization class
    optimizer = SimulatedAnnealingOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'time')
    # Get the initial solution
    solution = optimizer.initial_solution()
    # Calculate the parallel delivery time of the solution
    parallel_delivery_time = optimizer.calculate_parallel_delivery_time(solution)
    # Assert that the parallel delivery time is greater than or equal to 0
    assert parallel_delivery_time >= 0

# Test the find_nearest_station() method
def test_find_nearest_station(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of the SimulatedAnnealingOptimization class
    optimizer = SimulatedAnnealingOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Find the nearest station for the first customer
    nearest_station = optimizer.find_nearest_station(customers[0], charging_stations + fuel_stations)
    # Assert that the nearest station is not None
    assert nearest_station is not None

# Test the can_reach_next_destination_and_station() method
def test_can_reach_next_destination_and_station(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of the SimulatedAnnealingOptimization class
    optimizer = SimulatedAnnealingOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Check if the first vehicle can reach the next destination and station
    can_reach = optimizer.can_reach_next_destination_and_station(vehicles[0], depots[0], customers[0])
    # Assert that the result is a boolean value
    assert isinstance(can_reach, bool)

# Test the optimize() method
def test_optimize(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of the SimulatedAnnealingOptimization class
    optimizer = SimulatedAnnealingOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Optimize the solution
    solution, total_distance, total_emissions, parallel_delivery_time = optimizer.optimize()
    # Assert that the solution is not None
    assert solution is not None
    # Assert that the total distance is greater than or equal to 0
    assert total_distance >= 0
    # Assert that the total emissions is greater than or equal to 0
    assert total_emissions >= 0
    # Assert that the parallel delivery time is greater than or equal to 0
    assert parallel_delivery_time >= 0
