import matplotlib.pyplot as plt

def plot_routes(solution, depots, charging_stations, fuel_stations, title):
    """
    Plots the routes of the vehicles on a map.

    Args:
        solution (dict): The solution dictionary containing routes for each vehicle.
        depots (list): List of depot objects.
        charging_stations (list): List of charging station objects.
        fuel_stations (list): List of fuel station objects.
        title (str): The title of the plot.
    """
    # Define colors for different vehicles
    colors = ['r', 'b', 'g', 'y', 'm', 'c']
    
    # Create a new figure for the plot
    plt.figure(figsize=(10, 8))

    # Plot the routes for each vehicle
    for vehicle_id, route in solution.items():
        vehicle_id = int(vehicle_id)
        if len(route) > 1:
            # Extract x and y coordinates from each location in the route
            x = [loc.location_x for loc in route]
            y = [loc.location_y for loc in route]
            
            # Plot the route with markers and labels
            plt.plot(x, y, marker='o', color=colors[vehicle_id % len(colors)], label=f'Vehicle {vehicle_id + 1}')
            for i, loc in enumerate(route):
                plt.text(loc.location_x, loc.location_y, f'{type(loc).__name__} {loc.id}', fontsize=9)
        else:
            # Plot an empty route for unused vehicles
            plt.plot([], [], color=colors[vehicle_id % len(colors)], label=f'Vehicle {vehicle_id + 1} (Unused)')

    # Plot depots, charging stations, and fuel stations
    for depot in depots:
        plt.scatter(depot.location_x, depot.location_y, color='k', marker='s', s=100, label=f'Depot {depot.id}')

    for station in charging_stations:
        plt.scatter(station.location_x, station.location_y, color='g', marker='^', s=100, label=f'Charging Station {station.id}')

    for station in fuel_stations:
        plt.scatter(station.location_x, station.location_y, color='r', marker='x', s=100, label=f'Fuel Station {station.id}')

    # Set the title, x and y labels, legend, and grid
    plt.title(title)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid(True)
    
    # Show the plot
    plt.show()

def plot_metrics(total_distance, total_emissions, total_delivery_time, optimization_criteria, title):
    """
    Plots the metrics (distance, emissions, delivery time) as a bar chart.

    Args:
        total_distance (float): The total distance traveled.
        total_emissions (float): The total emissions produced.
        total_delivery_time (float): The total delivery time taken.
        optimization_criteria (str): The optimization criteria used.
        title (str): The title of the plot.
    """
    # Define the metrics and their corresponding values
    metrics = ['Total Distance', 'Total Emissions', 'Total Delivery Time']
    values = [total_distance, total_emissions, total_delivery_time]
    colors = ['blue', 'green', 'red']

    # Create a new figure for the plot
    plt.figure(figsize=(8, 6))
    
    # Plot the metrics as a bar chart
    plt.bar(metrics, values, color=colors)
    
    # Set the title, x and y labels
    plt.title(f"{title} (Optimized for {optimization_criteria})")
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    
    # Show the plot
    plt.show()
