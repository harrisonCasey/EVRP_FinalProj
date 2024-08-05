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

# Generate a mock decision variable matrix for testing extract_solution
def generate_mock_decision_variable_matrix(num_locations, num_vehicles):
    decision_variable_matrix = {}
    for i in range(num_locations):
        decision_variable_matrix[i] = {}
        for j in range(num_locations):
            decision_variable_matrix[i][j] = {}
            for k in range(num_vehicles):
                decision_variable_matrix[i][j][k] = 0
    # Populate the matrix with some valid routes
    decision_variable_matrix[0][2][0] = 1
    decision_variable_matrix[2][4][0] = 1
    decision_variable_matrix[4][0][0] = 1

    decision_variable_matrix[1][3][1] = 1
    decision_variable_matrix[3][5][1] = 1
    decision_variable_matrix[5][1][1] = 1

    return decision_variable_matrix

# Test the extract_solution method of MILPOptimization class
def test_extract_solution(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    num_locations = len(depots) + len(customers) + len(charging_stations) + len(fuel_stations)
    num_vehicles = len(vehicles)
    mock_decision_variable_matrix = generate_mock_decision_variable_matrix(num_locations, num_vehicles)
    extracted_solution = optimizer.extract_solution(mock_decision_variable_matrix)
    assert extracted_solution is not None
    for route in extracted_solution.values():
        assert isinstance(route, list)

# Test the optimize method of MILPOptimization class
def test_optimize_distance(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Call the optimize method
    solution, total_distance, total_emissions, total_delivery_time = optimizer.optimize()
    # Assert that the solution is not None
    assert solution is not None
    # Assert that the total distance is greater than or equal to 0
    assert total_distance >= 0
    # Assert that the total emissions is greater than or equal to 0
    assert total_emissions >= 0
    # Assert that the total delivery time is greater than or equal to 0
    assert total_delivery_time >= 0

def test_optimize_emissions(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'emissions')
    # Call the optimize method
    solution, total_distance, total_emissions, total_delivery_time = optimizer.optimize()
    # Assert that the solution is not None
    assert solution is not None
    # Assert that the total distance is greater than or equal to 0
    assert total_distance >= 0
    # Assert that the total emissions is greater than or equal to 0
    assert total_emissions >= 0
    # Assert that the total delivery time is greater than or equal to 0
    assert total_delivery_time >= 0

def test_optimize_time(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'time')
    # Call the optimize method
    solution, total_distance, total_emissions, total_delivery_time = optimizer.optimize()
    # Assert that the solution is not None
    assert solution is not None
    # Assert that the total distance is greater than or equal to 0
    assert total_distance >= 0
    # Assert that the total emissions is greater than or equal to 0
    assert total_emissions >= 0
    # Assert that the total delivery time is greater than or equal to 0
    assert total_delivery_time >= 0

# Test the calculate_distance method of MILPOptimization class
def test_calculate_distance(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Calculate the distance between two points
    distance = optimizer.calculate_distance(depots[0], customers[0])
    # Assert that the distance is greater than or equal to 0
    assert distance >= 0

# Test the calculate_emissions method of MILPOptimization class
def test_calculate_emissions(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'emissions')
    # Calculate the emissions for a vehicle
    emissions = optimizer.calculate_emissions(vehicles[0], 10)
    # Assert that the emissions is greater than or equal to 0
    assert emissions >= 0

# Test the find_nearest_station_distance method of MILPOptimization class
def test_find_nearest_station_distance(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Find the nearest station distance
    nearest_station_distance = optimizer.find_nearest_station_distance(0, vehicles[0])
    # Assert that the nearest station distance is greater than or equal to 0
    assert nearest_station_distance >= 0

# Test the calculate_cost method of MILPOptimization class
def test_calculate_cost(mock_data):
    depots, customers, vehicles, charging_stations, fuel_stations = mock_data
    # Create an instance of MILPOptimization class
    optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, 'distance')
    # Call the optimize method to get the solution
    solution = optimizer.optimize()[0]
    # Calculate the cost
    total_distance, total_emissions, total_delivery_time = optimizer.calculate_cost(solution)
    # Assert that the total distance is greater than or equal to 0
    assert total_distance >= 0
    # Assert that the total emissions is greater than or equal to 0
    assert total_emissions >= 0
    # Assert that the total delivery time is greater than or equal to 0
    assert total_delivery_time >= 0