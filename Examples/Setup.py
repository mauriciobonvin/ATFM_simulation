# Import modules for setup

# Time assignment strategy
import TimeAssignmentStrategy

# Network manager agent strategies
import WindowStrategy
import RegulationStrategy

# Airline agent strategies
import PriorityAssignmentStrategy
import DesiredTimeStrategy
import AssignMarginsStrategy

# Platform agent strategies
import OptimizationStrategy
import EquityMonitorStrategy
import InterveneEquityStrategy


# set parameters
steps = 100 # number of simulation iterations
n_times_ = 100 # number of available time slots
starting_seed_ = 0
# weight map parameters
base_value_weight_map_ = 100
percentage_reduction_weight_map_ = 0.1

'''
time_schedule = [1,	3,	13,	18,	24,	28,	34,	44,	49,	56,	2,	8,	12,	19,	26,	31,	36,	42,	48,	53,	0,	7,	15,	21,	25,	33,	41,	38,	50,	55,	4,	9,	14,	20,	27,	32,	43,	40,	51,	58,	6,	11,	17,	23,	29,	35,	46,	45,	52,	59,	5,	10,	16,	22,	30,	37,	39,	47,	54,	57]

predefined_window = [(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),
                    (5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),
                    (10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),
                    (15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),
                    (20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),
                    (25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),
                    (30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),
                    (35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),
                    (40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),
                    (45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),
                    (50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),
                    (0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),
                    (5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),
                    (10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),
                    (15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),
                    (20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),
                    (25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),
                    (30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),
                    (35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),
                    (40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),
                    (45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),
                    (50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),
                    (0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),
                    (5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),
                    (10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),
                    (15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),
                    (20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),
                    (25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),
                    (30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),
                    (35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),
                    (40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),
                    (45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),
                    (50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),
                    (0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),
                    (5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),
                    (10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),
                    (15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),
                    (20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),
                    (25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),
                    (30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),
                    (35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),
                    (40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),
                    (45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),
                    (50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),
                    (0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),
                    (5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),
                    (10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),(10,5),
                    (15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),(15,5),
                    (20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),(20,5),
                    (25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),(25,5),
                    (30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),(30,5),
                    (35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),(35,5),
                    (40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),(40,5),
                    (45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),(45,5),
                    (50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5),(50,5)]

'''

# strategies used 
# Regular schedule time assignment strategy
time_assignment_strategy = TimeAssignmentStrategy.RandomTimeAssignmentStrategy(time_assignment_seed = 29) #  #FixedAssignmentStrategy(time_schedule)
# Network manager agent strategies
window_strategy_ = WindowStrategy.RandomWindowStrategy() #PredefinedWindowStrategy(predefined_window) 
regulation_strategy_ = RegulationStrategy.NoCapacityStrategy()  
# Airline's flight prioritization strategies
priority_assignment_strategy = PriorityAssignmentStrategy.PriorityRandomAssignmentStrategy()  
desired_time_strategy = DesiredTimeStrategy.DesiredTimeRandomAssignmentStrategy()
assign_margins_strategy = AssignMarginsStrategy.MarginsRandomAssignmentStrategy()
# Platform agent strategies
optimization_strategy_ = OptimizationStrategy.LinearAssignmentStrategy()
equity_monitor_strategy_ = EquityMonitorStrategy.CreditsCLearingStrategy(initial_credits = 100)
intervene_equity_strategy_ = InterveneEquityStrategy.CreditBasedInterventionStrategy(equity_threshold= 0) #LowerUpperInterventionStrategy(50,150) 

# Network manager agent

class NetworkManager:
    
    def __init__(self,
                 unique_id,
                 window_strategy,
                 regulation_strategy
                ):
        self.unique_id = unique_id
        self.window_strategy = window_strategy
        self.regulation_strategy = regulation_strategy


network_manager_agent_ = NetworkManager(1,
                                        window_strategy_,
                                        regulation_strategy_
                                       )


# Airline agents

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

# Create airline agents
def airline_agents(airlines_flights,
                   priority_assignment_strategy,
                   desired_time_strategy,
                   assign_margins_strategy
                  ):
    
    airline_list = []
    counter = 2 #ID for scheduler
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


airlines_flights = { 'Airline_1': 10,
                  'Airline_2': 10,
                  'Airline_3': 10,
                  'Airline_4': 10,
                  'Airline_5': 10,
                  'Airline_6': 10
              } # airline name and number of flights


list_airline_agents_ = airline_agents(airlines_flights,
                                      priority_assignment_strategy,
                                      desired_time_strategy,
                                      assign_margins_strategy
                                      )


# Platform agent

class Platform:
    def __init__(
                    self, 
                    unique_id,
                    base_value_weight_map, 
                    percentage_reduction_weight_map, 
                    optimization_strategy, 
                    equity_monitor_strategy, 
                    intervene_equity_strategy
                ):
        self.unique_id = unique_id
        self.base_value_weight_map = base_value_weight_map
        self.percentage_reduction_weight_map = percentage_reduction_weight_map
        self.optimization_strategy = optimization_strategy
        self.equity_monitor_strategy = equity_monitor_strategy
        self.intervene_equity_strategy = intervene_equity_strategy


platform_agent_= Platform(len(airlines_flights) +2,
                          base_value_weight_map_,
                          percentage_reduction_weight_map_,
                          optimization_strategy_,
                          equity_monitor_strategy_,
                          intervene_equity_strategy_
                         )

