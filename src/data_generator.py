import csv
import random
import json

def generate_vehicles(config):
    """
    Generates a list of vehicles based on the configuration.

    Args:
        config (dict): Configuration dictionary containing vehicle parameters.

    Returns:
        list: List of vehicle dictionaries.
    """
    vehicles = []
    vehicle_id = 1
    for _ in range(config['num_electric_vehicles']):
        vehicles.append({
            'type': 'electric',
            'range': random.uniform(100, 250),
            'recharge_time': random.uniform(25, 50),
            'emission_rate': 0.5,  # Assuming lower emission rate for electric vehicles
            'port_type': random.choice(['standard', 'fast', 'super']),
            'package_capacity': random.randint(50, 100),
            'id': vehicle_id
        })
        vehicle_id += 1
    for _ in range(config['num_fossil_vehicles']):
        vehicles.append({
            'type': 'fossil',
            'range': random.uniform(100, 400),
            'recharge_time': 3,
            'emission_rate': 2.0,  # Assuming higher emission rate for fossil fuel vehicles
            'port_type': None,
            'package_capacity': random.randint(50,100),
            'id': vehicle_id
        })
        vehicle_id += 1
    return vehicles

def generate_depots(config):
    """
    Generates a list of depots based on the configuration.

    Args:
        config (dict): Configuration dictionary containing depot parameters.

    Returns:
        list: List of depot dictionaries.
    """
    depots = []
    for depot_id in range(1, config['num_depots'] + 1):
        depots.append({
            'location_x': random.uniform(0, config['grid_size'][0]),
            'location_y': random.uniform(0, config['grid_size'][1]),
            'id': depot_id
        })
    return depots

def generate_charging_stations(config):
    """
    Generates a list of charging stations based on the configuration.

    Args:
        config (dict): Configuration dictionary containing charging station parameters.

    Returns:
        list: List of charging station dictionaries.
    """
    stations = []
    for station_id in range(1, config['num_charging_stations'] + 1):
        stations.append({
            'location_x': random.uniform(0, config['grid_size'][0]),
            'location_y': random.uniform(0, config['grid_size'][1]),
            'charging_speed': random.uniform(1, 2),
            'id': station_id
        })
    return stations

def generate_fuel_stations(config):
    """
    Generates a list of fuel stations based on the configuration.

    Args:
        config (dict): Configuration dictionary containing fuel station parameters.

    Returns:
        list: List of fuel station dictionaries.
    """
    stations = []
    for station_id in range(1, config['num_fuel_stations'] + 1):
        stations.append({
            'location_x': random.uniform(0, config['grid_size'][0]),
            'location_y': random.uniform(0, config['grid_size'][1]),
            'station_type': random.choice(config['fuel_station_types']),
            'id': station_id
        })
    return stations

def generate_customers(config):
    """
    Generates a list of customers based on the configuration.

    Args:
        config (dict): Configuration dictionary containing customer parameters.

    Returns:
        list: List of customer dictionaries.
    """
    customers = []
    for customer_id in range(1, config['num_customers'] + 1):
        customers.append({
            'location_x': random.uniform(0, config['grid_size'][0]),
            'location_y': random.uniform(0, config['grid_size'][1]),
            'packages': random.randint(1,10),
            'id': customer_id
        })
    return customers

def save_to_csv(data, filename, fieldnames):
    """
    Saves data to a CSV file.

    Args:
        data (list): List of dictionaries containing data to be saved.
        filename (str): The name of the CSV file.
        fieldnames (list): List of field names for the CSV file.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    """
    Main function that generates data based on the configuration and saves it to CSV files.
    """
    # Load configuration from JSON file
    with open('config.json', 'r') as file:
        config = json.load(file)

    # Generate data based on configuration
    vehicles = generate_vehicles(config)
    depots = generate_depots(config)
    charging_stations = generate_charging_stations(config)
    fuel_stations = generate_fuel_stations(config)
    customers = generate_customers(config)

    # Save data to CSV files
    save_to_csv(vehicles, 'data/Vehicles.csv', ['type', 'range', 'recharge_time', 'emission_rate', 'package_capacity', 'port_type', 'id'])
    save_to_csv(depots, 'data/Depots.csv', ['location_x', 'location_y', 'id'])
    save_to_csv(charging_stations, 'data/ChargingStations.csv', ['location_x', 'location_y', 'station_type', 'charging_speed', 'id'])
    save_to_csv(fuel_stations, 'data/FuelStations.csv', ['location_x', 'location_y', 'station_type', 'id'])
    save_to_csv(customers, 'data/Customers.csv', ['location_x', 'location_y', 'packages', 'id'])

if __name__ == "__main__":
    main()
