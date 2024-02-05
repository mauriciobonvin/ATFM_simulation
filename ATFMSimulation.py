import mesa
import MesaScheduler
import Regulation

import numpy as np
np.set_printoptions(suppress=True, precision=2)
import random 


class ATFMSimulationModel(mesa.Model):
    
    def __init__(self, **kwargs):
        '''' initialize parameters as attributes'''
        # Mesa Schedulder
        self.scheduler = MesaScheduler.SequentialScheduler(self)
        self.step_number = 1
        # Attributes
        self.set_attributes(**kwargs)
        
        for agent in self.list_airline_agents:
            self.add_agent_to_scheduler(agent)
            
        self.add_agent_to_scheduler(self.platform_agent)
        
    def set_attributes(self, **kwargs):
        ''' helper function to initialize parameters'''
        for key, value in kwargs.items():
            setattr(self, 
                    key, 
                    value)
    
    def add_agent_to_scheduler(self, agent):
        agent.model = self
        self.scheduler.add_agent_to_sequence(agent)
    
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
        

