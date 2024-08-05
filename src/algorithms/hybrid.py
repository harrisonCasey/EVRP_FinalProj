from algorithms.simulated_annealing import SimulatedAnnealingOptimization
from algorithms.milp import MILPOptimization

class HybridOptimization:
    def __init__(self, depots, customers, vehicles, charging_stations, fuel_stations, optimization_criteria):
        self.depots = depots
        self.customers = customers
        self.vehicles = vehicles
        self.charging_stations = charging_stations
        self.fuel_stations = fuel_stations
        self.optimization_criteria = optimization_criteria

    def optimize(self):
        # Use Simulated Annealing to get an initial solution
        sa_optimizer = SimulatedAnnealingOptimization(self.depots, self.customers, self.vehicles, self.charging_stations, self.fuel_stations, self.optimization_criteria)
        initial_solution, _, _, _ = sa_optimizer.optimize()
        
        # Use MILP to refine the solution
        milp_optimizer = MILPOptimization(self.depots, self.customers, self.vehicles, self.charging_stations, self.fuel_stations, self.optimization_criteria, initial_solution)
        refined_solution, total_distance, total_emissions, total_delivery_time = milp_optimizer.optimize()
        
        return refined_solution, total_distance, total_emissions, total_delivery_time
