import pandas as pd
from models.vehicle import Vehicle
from models.depot import Depot
from models.customer import Customer
from models.charging_station import ChargingStation
from models.fuel_station import FuelStation

def parse_data():
    """
    Parses data from CSV files and returns lists of depots, vehicles, customers, charging stations, and fuel stations.

    Returns:
        tuple: Lists of depots, vehicles, customers, charging stations, and fuel stations.
    """
    # Initialize empty lists for depots, vehicles, customers, charging stations, and fuel stations
    depots = []
    vehicles = []
    customers = []
    charging_stations = []
    fuel_stations = []

    # Parse Depots
    depots_df = pd.read_csv('data/Depots.csv')
    for index, row in depots_df.iterrows():
        # Create a Depot object for each row in the Depots.csv file and append it to the depots list
        depots.append(Depot(row['location_x'], row['location_y'], row['id']))

    # Parse Vehicles
    vehicles_df = pd.read_csv('data/Vehicles.csv')
    for index, row in vehicles_df.iterrows():
        # Create a Vehicle object for each row in the Vehicles.csv file and append it to the vehicles list
        vehicles.append(Vehicle(row['type'], row['range'], row['recharge_time'], row['id'], row['emission_rate'], row['package_capacity'], row.get('port_type')))

    # Parse Customers
    customers_df = pd.read_csv('data/Customers.csv')
    for index, row in customers_df.iterrows():
        # Create a Customer object for each row in the Customers.csv file and append it to the customers list
        customers.append(Customer(row['location_x'], row['location_y'], row['packages'], row['id']))

    # Parse Charging Stations
    charging_stations_df = pd.read_csv('data/ChargingStations.csv')
    for index, row in charging_stations_df.iterrows():
        # Create a ChargingStation object for each row in the ChargingStations.csv file and append it to the charging_stations list
        charging_stations.append(ChargingStation(row['location_x'], row['location_y'], row['station_type'], row['charging_speed'], row['id']))

    # Parse Fuel Stations
    fuel_stations_df = pd.read_csv('data/FuelStations.csv')
    for index, row in fuel_stations_df.iterrows():
        # Create a FuelStation object for each row in the FuelStations.csv file and append it to the fuel_stations list
        fuel_stations.append(FuelStation(row['location_x'], row['location_y'], row['station_type'], row['id']))

    # Return the lists of depots, vehicles, customers, charging stations, and fuel stations as a tuple
    return depots, vehicles, customers, charging_stations, fuel_stations
