import mesa
import MesaScheduler

import NetworkManagerAgent
import AirlineAgent
import PlatformAgent

import logging

logger = logging.getLogger(__name__)


class ATFMSimulationModel(mesa.Model):
    
    def __init__(self, 
                 n_times,
                 seed,
                 network_manager_agent,
                 list_airline_agents,
                 platform_agent,
                 time_assignment_strategy):
        
     
        # Attributes
        self.n_times = n_times
        self.seed = seed
        self.network_manager_agent = network_manager_agent
        self.list_airline_agents = list_airline_agents
        self.platform_agent = platform_agent
        self.time_assignment_strategy = time_assignment_strategy
        
        # Mesa Schedulder
        self.scheduler = MesaScheduler.SequentialScheduler(self)
        self.step_number = 1

        # Agents
        
        # Network manager agent

        self.mesa_network_manager_agent = NetworkManagerAgent.NetworkManagerAgent(self.network_manager_agent.unique_id,
                                                                             self,
                                                                             self.network_manager_agent.window_strategy,
                                                                             self.network_manager_agent.regulation_strategy
                                                                            )

        # Airline agent
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

        

        # Platform agent
        
        self.mesa_platform_agent = PlatformAgent.PlatformAgent(self.platform_agent.unique_id,
                                                          self,
                                                         self.platform_agent.base_value_weight_map,
                                                         self.platform_agent.percentage_reduction_weight_map,
                                                         self.platform_agent.optimization_strategy,
                                                         self.platform_agent.equity_monitor_strategy,
                                                         self.platform_agent.intervene_equity_strategy
                                                         )
        

        # Add agents to scheduler

        self.scheduler.add_agent_to_sequence(self.mesa_network_manager_agent)
        
        for agent_ in self.list_mesa_airline_agents:
            self.scheduler.add_agent_to_sequence(agent_)
    
        self.scheduler.add_agent_to_sequence(self.mesa_platform_agent)

        # Flight schedule

        self.regular_flight_schedule = self.flights_schedule(self.list_mesa_airline_agents, self.n_times)
        #print("regular flight schedule", self.regular_flight_schedule)

        # Flight data

        self.flight_data = []

        # Equity metrics
        
        self.equity_data = []

    # helper function 
    
    def flights_schedule(self, list_of_airlines, n_times):
        # instanciate flight objects in a list
        self.scheduled_flights_object_list = [scheduled_flight for airline in list_of_airlines for scheduled_flight in airline.scheduled_flights_objects_list]
        self.scheduled_flights_object_list = self.time_assignment_strategy.assign_time(self.scheduled_flights_object_list,
                                                                                 n_times)
        return self.scheduled_flights_object_list

    # simulation step
    
    def step(self):
        """Advance the model by one step.
        """
        logger.info("Start of simulation step:%s", self.step_number)
        logger.info("Seed number:%s", self.seed)
        self.scheduler.step()
        logger.info("End of simulation step:%s", self.step_number)
        self.seed += 1
        self.step_number += 1
                

