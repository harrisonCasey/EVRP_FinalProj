# Green Vehicle Routing Problem (GVRP)

## Overview

The Green Vehicle Routing Problem (GVRP) simulation aims to optimize the routing of a fleet of electric and fossil-fueled vehicles for delivery purposes. The optimization considers sustainability constraints, refueling/recharging requirements, and minimizing total distance, emissions, and delivery times.

## Key Objectives

1. Minimize total distance traveled by all vehicles.
2. Minimize emissions, considering the type of vehicles.
3. Ensure vehicles do not run out of fuel/charge during routes.
4. Optimize routes for the fastest delivery times within the constraints.

## Constraints

### Vehicle Constraints
- **Types**: Electric and fossil-fueled.
- **Range**: Each vehicle has a maximum range it can travel before needing to refuel/recharge.
- **Charging/Refueling Time**: Time required for vehicles to recharge/refuel.

### Depot Constraints
- **Locations**: Fixed locations where vehicles start and end their routes.

### Charging and Fuel Station Constraints
- **Types**: Different types of charging stations (standard, fast, super) and fuel stations.
- **Locations**: Fixed locations within the grid.

### Customer Constraints
- **Locations**: Fixed delivery locations.
- **Delivery Quantities**: The amount of goods to be delivered to each customer.

## Assumptions

1. Static Problem: The locations of depots, customers, and stations are fixed and known beforehand.
2. No Queue Times: No waiting time at charging or fueling stations.
3. No Delivery Time Windows: No specific time windows for deliveries.

## Data Input

The input data will be provided in CSV format:

1. **Vehicles.csv**: Details of each vehicle (type, capacity, range, recharge/refuel time, emission rate).
2. **Depots.csv**: Locations of each depot.
3. **ChargingStations.csv**: Locations and types of charging stations.
4. **FuelStations.csv**: Locations and types of fuel stations.
5. **Customers.csv**: Locations and packages for each customer.

## Optimization Algorithms

We will explore and implement the following algorithms:

1. **Simulated Annealing**: A metaheuristic algorithm for finding a good approximation of the optimal route.
2. **Mixed-Integer Linear Programming (MILP)**: An exact optimization algorithm for finding the optimal route.

## Performance Metrics

1. **Total Distance Traveled**: Sum of distances covered by all vehicles.
2. **Total Emissions**: Calculated based on the type of vehicle and distance traveled.
3. **Total Delivery Time**: Including travel and refuel/recharge times.

## Visualization

1. **Route Maps**: Visual representation of vehicle routes.
2. **Emission Graphs**: Emissions per route.
3. **Delivery Times**: Bar charts or other visual formats.

## Running the Simulation

1. Ensure the CSV data files are present in the `data` directory.
   - You can generate test data by updating `config.json` and running the following command:
   ```bash
   python src/data_generator.py
   ```
2. Run the simulation using the following command:
   ```bash
   python src/simulation.py
   ```
The simulation will output the optimized routes for each vehicle, total distance traveled, total emissions, and total delivery time. Visualizations will be generated to illustrate the routes, emissions, and delivery times, providing insights into the efficiency and sustainability of the routes.

3. Run tests with the following command:
```bash
pytest
```