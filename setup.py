import numpy as np
np.set_printoptions(suppress=True, precision=2)
import random

import AirlineAgent

import TimeAssignmentStrategy
import WindowStrategy
import RegulationStrategy

import PriorityAssignmentStrategy
import DesiredTimeStrategy
import AssignMarginsStrategy

import PlatformAgent

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
# equity parameter
bonus_ = 0.1


# strategies used here
# Time assignment strategy
time_assignment_strategy = TimeAssignmentStrategy.RandomTimeAssignmentStrategy()
# airline agent strategies
priority_assignment_strategy = PriorityAssignmentStrategy.PriorityRandomAssignmentStrategy()
desired_time_strategy = DesiredTimeStrategy.DesiredTimeRandomAssignmentStrategy()
assign_margins_strategy = AssignMarginsStrategy.MarginsRandomAssignmentStrategy()
# Platform agent strategies
optimization_strategy_ = optimization_strategy.LinearAssignmentStrategy()
equity_handler_ = equity_handler.CreditsCLearingStrategy()

# strategies used during simulation
# Regulation strategies
window_strategy_ = WindowStrategy.RandomWindowStrategy()
regulation_strategy_ = RegulationStrategy.ReducedCapacityStrategy()


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
        airline_ = AirlineAgent.AirlineAgent(counter, 
                                             None, # initialize without model
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



platform_agent_= PlatformAgent.PlatformAgent(len(airlines_flights) +1, 
                                            None, # initialize without model
                                            base_value_weight_map_,
                                            percentage_reduction_weight_map_,
                                            optimization_strategy_,
                                            bonus_,
                                            equity_handler_
                                           )


def flights_schedule(list_of_airlines, n_times, seed):
    # instanciate flight objects in a list
    scheduled_flights_object_list = [scheduled_flight for airline in list_of_airlines for scheduled_flight in airline.scheduled_flights_objects_list]
    scheduled_flights_object_list = time_assignment_strategy.assign_time(scheduled_flights_object_list,
                                                                                 n_times, 
                                                                                 seed)
    
    return scheduled_flights_object_list


flight_schedule_ = flights_schedule(list_airline_agents_,n_times_, starting_seed_)

