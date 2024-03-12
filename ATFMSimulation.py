import mesa
import MesaScheduler
import Regulation

import numpy as np
np.set_printoptions(suppress=True, precision=2)
import random 

import AirlineAgent
import PlatformAgent



class ATFMSimulationModel(mesa.Model):
    
    def __init__(self, **kwargs):
        '''' initialize parameters as attributes'''
        # Mesa Schedulder
        self.scheduler = MesaScheduler.SequentialScheduler(self)
        self.step_number = 1
        # Attributes
        self.set_attributes(**kwargs)

        self.list_mesa_airline_agents = []
        for agent in self.list_airline_agents:
            mesa_airline_agent = AirlineAgent.AirlineAgent(agent.unique_id,
                                                           self,
                                                           agent.name,
                                                           agent.number_of_flights,
                                                           agent.priority_assignment_strategy,
                                                           agent.desired_time_strategy,
                                                           agent.assign_margins_strategy
                                                          )
            self.list_mesa_airline_agents.append(mesa_airline_agent)
            self.add_agent_to_scheduler(mesa_airline_agent)
            
        mesa_platform_agent = PlatformAgent.PlatformAgent(self.platform_agent.unique_id,
                                                          self,
                                                         self.platform_agent.base_value_weight_map,
                                                         self.platform_agent.percentage_reduction_weight_map,
                                                         self.platform_agent.optimization_strategy,
                                                         self.platform_agent.equity_handler
                                                         )
        self.add_agent_to_scheduler(mesa_platform_agent)

        self.flight_schedule_ = self.flights_schedule(self.list_mesa_airline_agents,self.n_times, self.seed)

        
    def set_attributes(self, **kwargs):
        ''' helper function to initialize parameters'''
        for key, value in kwargs.items():
            setattr(self, 
                    key, 
                    value)
    
    def add_agent_to_scheduler(self, agent):
        self.scheduler.add_agent_to_sequence(agent)
    
    def flights_schedule(self, list_of_airlines, n_times, seed):
        # instanciate flight objects in a list
        self.scheduled_flights_object_list = [scheduled_flight for airline in list_of_airlines for scheduled_flight in airline.scheduled_flights_objects_list]
        self.scheduled_flights_object_list = self.time_assignment_strategy.assign_time(self.scheduled_flights_object_list,
                                                                                 n_times, 
                                                                                 seed)
        return self.scheduled_flights_object_list
        
    def step(self):
        """Advance the model by one step."""
        self.regulation_ = Regulation.Regulation(self.step_number,
                                                 self.seed,
                                                 self.n_times,
                                                 self.scheduled_flights_object_list,
                                                 self.window_strategy,
                                                 self.regulation_strategy,
                                                 self.capacity
                                                )
        self.slot_array = self.regulation_.start_regulation()
        
        self.scheduler.step()
        self.seed += 1
        self.step_number += 1
        

