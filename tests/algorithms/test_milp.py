import pytest
from src.models.vehicle import Vehicle
from src.models.depot import Depot
from src.models.customer import Customer
from src.models.charging_station import ChargingStation
from src.models.fuel_station import FuelStation
from src.algorithms.milp import MILPOptimization

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
        Customer(5, 5, 5, 1),
        Customer(15, 15, 10, 2)
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

# Test the optimize method of MILPOptimization class
def test_optimize(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Call the optimize method
    solution, total_distance, total_emissions, parallel_delivery_time = optimizer.optimize()
    # Assert that the solution is not None
    assert solution is not None
    # Assert that the total distance is greater than or equal to 0
    assert total_distance >= 0
    # Assert that the total emissions is greater than or equal to 0
    assert total_emissions >= 0
    # Assert that the parallel delivery time is greater than or equal to 0
    assert parallel_delivery_time >= 0

# Test the calculate_parallel_delivery_time method of MILPOptimization class
def test_calculate_parallel_delivery_time(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'time')
    # Call the optimize method and get the solution
    solution = optimizer.optimize()[0]
    # Calculate the parallel delivery time
    parallel_delivery_time = optimizer.calculate_parallel_delivery_time(solution)
    # Assert that the parallel delivery time is greater than or equal to 0
    assert parallel_delivery_time >= 0

# Test the calculate_distance method of MILPOptimization class
def test_calculate_distance(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Calculate the distance between two points
    distance = optimizer.calculate_distance(0, 1)
    # Assert that the distance is greater than or equal to 0
    assert distance >= 0

# Test the calculate_emissions method of MILPOptimization class
def test_calculate_emissions(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'emissions')
    # Calculate the emissions between two points
    emissions = optimizer.calculate_emissions(0, 10)
    # Assert that the emissions is greater than or equal to 0
    assert emissions >= 0

# Test the calculate_total_distance method of MILPOptimization class
def test_calculate_total_distance(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Call the optimize method and get the solution
    solution = optimizer.optimize()[0]
    # Calculate the total distance of the solution
    total_distance = optimizer.calculate_total_distance(solution)
    # Assert that the total distance is greater than or equal to 0
    assert total_distance >= 0

# Test the calculate_total_emissions method of MILPOptimization class
def test_calculate_total_emissions(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'emissions')
    # Call the optimize method and get the solution
    solution = optimizer.optimize()[0]
    # Calculate the total emissions of the solution
    total_emissions = optimizer.calculate_total_emissions(solution)
    # Assert that the total emissions is greater than or equal to 0
    assert total_emissions >= 0

# Test the calculate_total_delivery_time method of MILPOptimization class
def test_calculate_total_delivery_time(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'time')
    # Call the optimize method and get the solution
    solution = optimizer.optimize()[0]
    # Calculate the total delivery time of the solution
    total_delivery_time = optimizer.calculate_total_delivery_time(solution)
    # Assert that the total delivery time is greater than or equal to 0
    assert total_delivery_time >= 0

# Test the find_nearest_station method of MILPOptimization class
def test_find_nearest_station(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Find the nearest station for a customer
    nearest_station = optimizer.find_nearest_station(customers[0], charging_stations + fuel_stations)
    # Assert that the nearest station is not None
    assert nearest_station is not None

# Test the can_reach_next_destination_and_station method of MILPOptimization class
def test_can_reach_next_destination_and_station(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Check if a vehicle can reach the next destination and station
    can_reach = optimizer.can_reach_next_destination_and_station(vehicles[0], depots[0], customers[0])
    # Assert that the result is a boolean value
    assert isinstance(can_reach, bool)
