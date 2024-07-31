import pytest
import logging
from models.vehicle import Vehicle
from models.charging_station import ChargingStation
from models.fuel_station import FuelStation

logging.basicConfig(level=logging.DEBUG)

# Define a fixture for an electric vehicle
@pytest.fixture
def electric_vehicle():
    return Vehicle(
        vehicle_type='electric',
        range=200,
        recharge_time=30,
        id=1,
        emission_rate=0.5,
        package_capacity=100,
        port_type='fast'
    )

# Define a fixture for a fossil fuel vehicle
@pytest.fixture
def fossil_vehicle():
    return Vehicle(
        vehicle_type='fossil',
        range=400,
        recharge_time=5,
        id=2,
        emission_rate=2.0,
        package_capacity=150
    )

# Define a fixture for a charging station
@pytest.fixture
def charging_station():
    return ChargingStation(
        location_x=50,
        location_y=50,
        station_type='fast',
        charging_speed=1.5,
        id=1
    )

# Define a fixture for a fuel station
@pytest.fixture
def fuel_station():
    return FuelStation(
        location_x=100,
        location_y=100,
        station_type='standard',
        id=1
    )

# Test the calculate_emissions method of the Vehicle class
def test_calculate_emissions(electric_vehicle, fossil_vehicle):
    distance = 100
    assert electric_vehicle.calculate_emissions(distance) == 50
    assert fossil_vehicle.calculate_emissions(distance) == 200

# Test the refuel_or_recharge method of the Vehicle class for electric vehicles
def test_refuel_or_recharge_electric(electric_vehicle, charging_station):
    electric_vehicle.remaining_range = 50
    logging.debug(f"Before recharge: {electric_vehicle.remaining_range}")
    electric_vehicle.refuel_or_recharge(charging_station)
    logging.debug(f"After recharge: {electric_vehicle.remaining_range}")
    assert electric_vehicle.remaining_range == electric_vehicle.range

# Test the refuel_or_recharge method of the Vehicle class for fossil fuel vehicles
def test_refuel_or_recharge_fossil(fossil_vehicle, fuel_station):
    fossil_vehicle.remaining_range = 100
    logging.debug(f"Before refuel: {fossil_vehicle.remaining_range}")
    fossil_vehicle.refuel_or_recharge(fuel_station)
    logging.debug(f"After refuel: {fossil_vehicle.remaining_range}")
    assert fossil_vehicle.remaining_range == fossil_vehicle.range

# Test the travel method of the Vehicle class for successful travel
def test_travel_success(electric_vehicle, fossil_vehicle):
    distance = 150
    assert electric_vehicle.travel(distance) is True
    assert electric_vehicle.remaining_range == 50

    assert fossil_vehicle.travel(distance) is True
    assert fossil_vehicle.remaining_range == 250

# Test the travel method of the Vehicle class for failed travel
def test_travel_failure(electric_vehicle, fossil_vehicle):
    distance = 250
    assert electric_vehicle.travel(distance) is False
    assert electric_vehicle.remaining_range == 200

    assert fossil_vehicle.travel(distance) is True
    assert fossil_vehicle.remaining_range == 150

# Test the needs_refuel_or_recharge method of the Vehicle class
def test_needs_refuel_or_recharge(electric_vehicle, fossil_vehicle):
    electric_vehicle.remaining_range = 0
    assert electric_vehicle.needs_refuel_or_recharge() is True

    fossil_vehicle.remaining_range = 1
    assert fossil_vehicle.needs_refuel_or_recharge() is False
