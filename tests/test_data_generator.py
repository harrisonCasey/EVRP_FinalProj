import pytest
import random
import csv

from src.data_generator import (
    generate_vehicles,
    generate_depots,
    generate_charging_stations,
    generate_fuel_stations,
    generate_customers,
    save_to_csv
)

# Fixture to provide configuration data for tests
@pytest.fixture
def config():
    return {
        'num_electric_vehicles': 5,
        'num_fossil_vehicles': 5,
        'num_depots': 3,
        'num_charging_stations': 4,
        'num_fuel_stations': 4,
        'num_customers': 10,
        'grid_size': (100, 100),
        'fuel_station_types': ['type1', 'type2', 'type3']
    }

# Test case for generate_vehicles function
def test_generate_vehicles(config):
    vehicles = generate_vehicles(config)
    assert len(vehicles) == config['num_electric_vehicles'] + config['num_fossil_vehicles']
    for vehicle in vehicles:
        assert 'type' in vehicle
        assert 'range' in vehicle
        assert 'recharge_time' in vehicle
        assert 'emission_rate' in vehicle
        assert 'package_capacity' in vehicle
        assert 'id' in vehicle
        if vehicle['type'] == 'electric':
            assert vehicle['port_type'] in ['standard', 'fast', 'super']
        else:
            assert vehicle['port_type'] is None

# Test case for generate_depots function
def test_generate_depots(config):
    depots = generate_depots(config)
    assert len(depots) == config['num_depots']
    for depot in depots:
        assert 'location_x' in depot
        assert 'location_y' in depot
        assert 'id' in depot
        assert 0 <= depot['location_x'] <= config['grid_size'][0]
        assert 0 <= depot['location_y'] <= config['grid_size'][1]

# Test case for generate_charging_stations function
def test_generate_charging_stations(config):
    stations = generate_charging_stations(config)
    assert len(stations) == config['num_charging_stations']
    for station in stations:
        assert 'location_x' in station
        assert 'location_y' in station
        assert 'charging_speed' in station
        assert 'id' in station
        assert 0 <= station['location_x'] <= config['grid_size'][0]
        assert 0 <= station['location_y'] <= config['grid_size'][1]

# Test case for generate_fuel_stations function
def test_generate_fuel_stations(config):
    stations = generate_fuel_stations(config)
    assert len(stations) == config['num_fuel_stations']
    for station in stations:
        assert 'location_x' in station
        assert 'location_y' in station
        assert 'station_type' in station
        assert 'id' in station
        assert station['station_type'] in config['fuel_station_types']
        assert 0 <= station['location_x'] <= config['grid_size'][0]
        assert 0 <= station['location_y'] <= config['grid_size'][1]

# Test case for generate_customers function
def test_generate_customers(config):
    customers = generate_customers(config)
    assert len(customers) == config['num_customers']
    for customer in customers:
        assert 'location_x' in customer
        assert 'location_y' in customer
        assert 'packages' in customer
        assert 'id' in customer
        assert 0 <= customer['location_x'] <= config['grid_size'][0]
        assert 0 <= customer['location_y'] <= config['grid_size'][1]
        assert 1 <= customer['packages'] <= 10

# Test case for save_to_csv function
def test_save_to_csv(tmpdir):
    data = [
        {'field1': 'value1', 'field2': 'value2'},
        {'field1': 'value3', 'field2': 'value4'}
    ]
    filename = tmpdir.join('test.csv')
    fieldnames = ['field1', 'field2']
    
    save_to_csv(data, str(filename), fieldnames)
    
    with open(str(filename), 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]['field1'] == 'value1'
        assert rows[0]['field2'] == 'value2'
        assert rows[1]['field1'] == 'value3'
        assert rows[1]['field2'] == 'value4'
