import logging
import time
from visualization import plot_metrics, plot_routes
from data_parser import parse_data
from algorithms.simulated_annealing import SimulatedAnnealingOptimization
from algorithms.milp import MILPOptimization
from algorithms.hybrid import HybridOptimization

def log_solution(solution, total_distance, total_emissions, total_delivery_time, algorithm, optimization_criteria):
    """
    Logs the solution details.

    Args:
        solution (dict): The solution dictionary containing routes for each vehicle.
        total_distance (float): The total distance traveled.
        total_emissions (float): The total emissions produced.
        total_delivery_time (float): The total delivery time taken.
        algorithm (str): The name of the algorithm used.
        optimization_criteria (str): The optimization criteria used.
    """
    logging.info(f"{algorithm} optimization completed.")
    logging.info(f"Optimized for: {optimization_criteria}")
    logging.info(f"Total Distance: {total_distance}")
    logging.info(f"Total Emissions: {total_emissions}")
    # Assume 30 mph average speed
    logging.info(f"Total Delivery Time: {total_delivery_time/30} hours")
    for vehicle_id, route in solution.items():
        if len(route) > 2:
            route_details = " -> ".join([f"{type(loc).__name__} {loc.id}" for loc in route])
            logging.info(f"Vehicle {vehicle_id + 1} route: {route_details}")
        else:
            logging.info(f"Vehicle {vehicle_id + 1} is unused.")

def main():
    """
    The main function that runs the simulation.
    """
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.basicConfig(level=logging.INFO)

    # Parse data
    depots, vehicles, customers, charging_stations, fuel_stations = parse_data()
    optimization_criteria = 'distance'  # Change this to 'distance', 'emissions', or 'time' as needed

    # Simulated Annealing Optimization
    logging.info("\nSimulated Annealing Started")
    start_time = time.time()
    sa_optimizer = SimulatedAnnealingOptimization(depots, customers, vehicles, charging_stations, fuel_stations, optimization_criteria)
    sa_solution, sa_total_distance, sa_total_emissions, sa_total_delivery_time = sa_optimizer.optimize()
    sa_time_taken = time.time() - start_time
    logging.info("\nSimulated Annealing Results:")
    log_solution(sa_solution, sa_total_distance, sa_total_emissions, sa_total_delivery_time, "Simulated Annealing", optimization_criteria)
    plot_routes(sa_solution, depots, charging_stations, fuel_stations, "Simulated Annealing Routes")
    plot_metrics(sa_total_distance, sa_total_emissions, sa_total_delivery_time, optimization_criteria, "Simulated Annealing Metrics")
    logging.info(f"\nSimulated Annealing Completed in {sa_time_taken:.2f} seconds")

    # MILP Optimization
    logging.info("\nMILP Started")
    start_time = time.time()
    milp_optimizer = MILPOptimization(depots, customers, vehicles, charging_stations, fuel_stations, optimization_criteria)
    milp_solution, milp_total_distance, milp_total_emissions, milp_total_delivery_time = milp_optimizer.optimize()
    milp_time_taken = time.time() - start_time
    logging.info("\nMILP Results:")
    log_solution(milp_solution, milp_total_distance, milp_total_emissions, milp_total_delivery_time, "MILP", optimization_criteria)
    plot_routes(milp_solution, depots, charging_stations, fuel_stations, "MILP Routes")
    plot_metrics(milp_total_distance, milp_total_emissions, milp_total_delivery_time, optimization_criteria, "MILP Metrics")
    logging.info(f"\nMILP Completed in {milp_time_taken:.2f} seconds")

    # Hybrid Optimization
    logging.info("\nHybrid Started")
    start_time = time.time()
    hybrid_optimizer = HybridOptimization(depots, customers, vehicles, charging_stations, fuel_stations, optimization_criteria)
    hybrid_solution, hybrid_total_distance, hybrid_total_emissions, hybrid_total_delivery_time = hybrid_optimizer.optimize()
    hybrid_time_taken = time.time() - start_time
    logging.info("\nHybrid Results:")
    log_solution(hybrid_solution, hybrid_total_distance, hybrid_total_emissions, hybrid_total_delivery_time, "Hybrid", optimization_criteria)
    plot_routes(hybrid_solution, depots, charging_stations, fuel_stations, "Hybrid Routes")
    plot_metrics(hybrid_total_distance, hybrid_total_emissions, hybrid_total_delivery_time, optimization_criteria, "Hybrid Metrics")
    logging.info(f"\nHybrid Completed in {hybrid_time_taken:.2f} seconds")

    # Comparison of Results
    logging.info(f"\nComparison of Results for {optimization_criteria}:")
    logging.info(f"Simulated Annealing: Distance = {sa_total_distance}, Emissions = {sa_total_emissions}, Time = {sa_total_delivery_time/30:.2f} hours, Time Taken = {sa_time_taken:.2f} seconds")
    logging.info(f"MILP: Distance = {milp_total_distance}, Emissions = {milp_total_emissions}, Time = {milp_total_delivery_time/30:.2f} hours, Time Taken = {milp_time_taken:.2f} seconds")
    logging.info(f"Hybrid: Distance = {hybrid_total_distance}, Emissions = {hybrid_total_emissions}, Time = {hybrid_total_delivery_time/30:.2f} hours, Time Taken = {hybrid_time_taken:.2f} seconds")

if __name__ == "__main__":
    main()
