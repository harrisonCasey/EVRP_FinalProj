import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from models.vehicle import Vehicle
from models.depot import Depot
from models.customer import Customer
from models.charging_station import ChargingStation
from models.fuel_station import FuelStation
from data_parser import parse_data

# Define fixtures for mock dataframes

@pytest.fixture
def mock_depots_df():
    return pd.DataFrame({
        'location_x': [1.0, 2.0],
        'location_y': [1.0, 2.0],
        'id': [1, 2]
    })

@pytest.fixture
def mock_vehicles_df():
    return pd.DataFrame({
        'type': ['electric', 'fossil'],
        'range': [100.0, 200.0],
        'recharge_time': [30.0, 0],
        'id': [1, 2],
        'emission_rate': [0.5, 2.0],
        'package_capacity': [50, 100],
        'port_type': ['fast', None]
    })

@pytest.fixture
def mock_customers_df():
    return pd.DataFrame({
        'location_x': [3.0, 4.0],
        'location_y': [3.0, 4.0],
        'packages': [5, 10],
        'id': [1, 2]
    })

@pytest.fixture
def mock_charging_stations_df():
    return pd.DataFrame({
        'location_x': [5.0, 6.0],
        'location_y': [5.0, 6.0],
        'station_type': ['standard', 'fast'],
        'charging_speed': [1.0, 2.0],
        'id': [1, 2]
    })

@pytest.fixture
def mock_fuel_stations_df():
    return pd.DataFrame({
        'location_x': [7.0, 8.0],
        'location_y': [7.0, 8.0],
        'station_type': ['type1', 'type2'],
        'id': [1, 2]
    })

# Define the test function

@patch('pandas.read_csv')
def test_parse_data(mock_read_csv, mock_depots_df, mock_vehicles_df, mock_customers_df, mock_charging_stations_df, mock_fuel_stations_df):
    # Mock the return values of pd.read_csv
    mock_read_csv.side_effect = [
        mock_depots_df, mock_vehicles_df, mock_customers_df, mock_charging_stations_df, mock_fuel_stations_df
    ]

    # Call the function under test
    depots, vehicles, customers, charging_stations, fuel_stations = parse_data()

    # Verify depots
    assert len(depots) == len(mock_depots_df)
    for depot, (_, row) in zip(depots, mock_depots_df.iterrows()):
        assert depot.location_x == row['location_x']
        assert depot.location_y == row['location_y']
        assert depot.id == row['id']

    # Verify vehicles
    assert len(vehicles) == len(mock_vehicles_df)
    for vehicle, (_, row) in zip(vehicles, mock_vehicles_df.iterrows()):
        assert vehicle.vehicle_type == row['type']
        assert vehicle.range == row['range']
        assert vehicle.recharge_time == row['recharge_time']
        assert vehicle.id == row['id']
        assert vehicle.emission_rate == row['emission_rate']
        assert vehicle.package_capacity == row['package_capacity']
        assert vehicle.port_type == row['port_type']

    # Verify customers
    assert len(customers) == len(mock_customers_df)
    for customer, (_, row) in zip(customers, mock_customers_df.iterrows()):
        assert customer.location_x == row['location_x']
        assert customer.location_y == row['location_y']
        assert customer.packages == row['packages']
        assert customer.id == row['id']

    # Verify charging stations
    assert len(charging_stations) == len(mock_charging_stations_df)
    for station, (_, row) in zip(charging_stations, mock_charging_stations_df.iterrows()):
        assert station.location_x == row['location_x']
        assert station.location_y == row['location_y']
        assert station.station_type == row['station_type']
        assert station.charging_speed == row['charging_speed']
        assert station.id == row['id']

    # Verify fuel stations
    assert len(fuel_stations) == len(mock_fuel_stations_df)
    for station, (_, row) in zip(fuel_stations, mock_fuel_stations_df.iterrows()):
        assert station.location_x == row['location_x']
        assert station.location_y == row['location_y']
        assert station.station_type == row['station_type']
        assert station.id == row['id']
