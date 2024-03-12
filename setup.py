# import third party libraries
import numpy as np
np.set_printoptions(suppress=True, precision=2)
import random
# import own modules
#Regulation modules
import TimeAssignmentStrategy
import WindowStrategy
import RegulationStrategy
# Airline modules
import PriorityAssignmentStrategy
import DesiredTimeStrategy
import AssignMarginsStrategy
# Platform modules
import optimization_strategy
import equity_handler


# set parameters
steps = 10 # number of simulation runs
n_times_ = 100 # number of available times for arrival in a day
starting_seed_ = 0
capacity_ = 2 # gap number of capacity reduction in a regulation
airlines_flights = { 'Airline_1': 10,
                  'Airline_2': 10,
                  'Airline_3': 10,
                  'Airline_4': 10,
                  'Airline_5': 10,
                  'Airline_6': 10,
              } # airline name and amount of flights
# weight map parameters
base_value_weight_map_ = 100
percentage_reduction_weight_map_ = 0.1


# strategies used here
# Time assignment strategy
time_assignment_strategy = TimeAssignmentStrategy.RandomTimeAssignmentStrategy()
# airline agent strategies
priority_assignment_strategy = PriorityAssignmentStrategy.PriorityRandomAssignmentStrategy()
desired_time_strategy = DesiredTimeStrategy.DesiredTimeRandomAssignmentStrategy()
assign_margins_strategy = AssignMarginsStrategy.MarginsRandomAssignmentStrategy()
# Platform agent strategies
optimization_strategy_ = optimization_strategy.LinearAssignmentStrategy()
equity_handler_ = equity_handler.CreditsCLearingStrategy(bonus = 0.1, initial_credits = 100)

# strategies used during simulation
# Regulation strategies
window_strategy_ = WindowStrategy.RandomWindowStrategy()
regulation_strategy_ = RegulationStrategy.ReducedCapacityStrategy()


class Airline:
    def __init__(self,
                 unique_id, 
                 name, 
                 number_of_flights, 
                 priority_assignment_strategy, 
                 desired_time_strategy, 
                 assign_margins_strategy
                ):
        self.unique_id = unique_id
        self.name = name
        self.number_of_flights = number_of_flights
        self.priority_assignment_strategy = priority_assignment_strategy
        self.desired_time_strategy = desired_time_strategy
        self.assign_margins_strategy = assign_margins_strategy

# Create ariline agents
def airline_agents(airlines_flights,
                   priority_assignment_strategy,
                   desired_time_strategy,
                   assign_margins_strategy
                  ):
    
    airline_list = []
    counter = 1 #ID for scheduler
    for airline_name, number_of_flights in airlines_flights.items():
        # Create an AirlineAgent with the specified attributes
        airline_ = Airline(counter,
                           airline_name,
                           number_of_flights,
                           priority_assignment_strategy,
                           desired_time_strategy,
                           assign_margins_strategy
                                            ) 
        airline_list.append(airline_)
        # Increase the counter for agent IDs
        counter += 1
        
    return airline_list


list_airline_agents_ = airline_agents(airlines_flights,
                                      priority_assignment_strategy,
                                      desired_time_strategy,
                                      assign_margins_strategy
                                      )

class Platform:
    def __init__(self, unique_id, base_value_weight_map, percentage_reduction_weight_map, optimization_strategy, equity_handler):
        self.unique_id = unique_id
        self.base_value_weight_map = base_value_weight_map
        self.percentage_reduction_weight_map = percentage_reduction_weight_map
        self.optimization_strategy = optimization_strategy
        self.equity_handler = equity_handler


platform_agent_= Platform(len(airlines_flights) +1,
                          base_value_weight_map_,
                          percentage_reduction_weight_map_,
                          optimization_strategy_,
                          equity_handler_
                         )

