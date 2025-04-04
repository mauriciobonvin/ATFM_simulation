import mesa
import numpy as np
np.set_printoptions(suppress=True, precision=2)
import Flight

import logging

logger = logging.getLogger(__name__)


class AirlineAgent(mesa.Agent):
    
    def __init__(self,
                 unique_id,
                 model,
                 name: str,
                 n_flights:int,
                 priority_assignment_strategy,
                 desired_time_strategy,
                 assign_margins_strategy):
       
        #attributes
        
        super().__init__(unique_id, model)
        self.model = model
        self.name = str(name)
        self.n_flights = n_flights
        self.priority_assignment_strategy = priority_assignment_strategy
        self.desired_time_strategy = desired_time_strategy
        self.assign_margins_strategy = assign_margins_strategy
        
        self.scheduled_flights_objects_list = []
        self.create_scheduled_flights()
        
    def create_scheduled_flights(self):
        """
        Create a list of ScheduledFlight objects based on the provided number of flights.
            """
        self.scheduled_flights_objects_list = [
            Flight.ScheduledFlight(f"{self.name}_{flight_number}") for flight_number in range(1, self.n_flights + 1)
        ]
        
        return self.scheduled_flights_objects_list
    
    def set_actual_flights_list(self):
        """
        Set the list of actual flights for the current step, based on scheduled flights.
            """
        self.step_actual_flights = []
        for scheduled_flight in self.scheduled_flights_objects_list:
            scheduled_flight.time_assignment_seed = self.model.time_assignment_strategy.time_assignment_seed
            for actual_flight in scheduled_flight.list_of_actual_flights:
                if actual_flight.step_number == self.model.step_number:
                    self.step_actual_flights.append(actual_flight)
        return self.step_actual_flights
    
    def assign_priority(self):
        """
        Assign priorities to actual flights based on a priority assignment strategy.
        """
        flight_array = self.priority_assignment_strategy.assign_priority(len(self.step_actual_flights),self.model.seed)
        for index, actual_flight in enumerate(self.step_actual_flights):
            actual_flight.priority = flight_array[index]
            logger.info("Flight number:%s, Priority:%s",
                        actual_flight.scheduled_flight.flight_number,
                        actual_flight.priority
                       )
  

    def assign_desired_time(self):
        """
        Assign desired times to actual flights based on a desired time assignment strategy.
        """
        for index, actual_flight in enumerate(self.step_actual_flights):
            if actual_flight.priority > 0 and actual_flight.assigned_time in self.model.mesa_network_manager_agent.new_flight_list:
                desired_time_ = self.desired_time_strategy.assign_desired_time(actual_flight,
                                                                               self.model.mesa_network_manager_agent.new_flight_list,
                                                                               self.model.seed
                                                                              )
                actual_flight.desired_time = desired_time_
    
    def assign_margins(self):
        """
        Assign margins to actual flights based on a margins assignment strategy.
        """
        for index, actual_flight in enumerate(self.step_actual_flights):
            if actual_flight.desired_time:
                margin_tuple = self.assign_margins_strategy.assign_margins(actual_flight,
                                                                           self.model.mesa_network_manager_agent.new_flight_list,
                                                                           self.model.seed
                                                                          )
                actual_flight.margins = margin_tuple
                logger.info("Priority strategy for flight %s -> Lower margin:%s, Upper margin:%s, Desired time:%s",
                           actual_flight.scheduled_flight.flight_number,
                            margin_tuple[0],
                            margin_tuple[1],
                            margin_tuple[2]
                           )
                
    def define_flight_preferences(self):
        """
        Define flight preferences for impacted flights based on assigned times, desired times, and priorities.
            """
        slot_array = np.array(self.model.mesa_network_manager_agent.new_flight_list)
        slot_array_len = len(slot_array)
        self.impacted_flights = []
        
        for index, actual_flight in enumerate(self.step_actual_flights):
            if actual_flight.assigned_time in slot_array:
                self.impacted_flights.append(actual_flight)
        impacted_flights_len = len(self.impacted_flights)
        self.matrix_flight_preferences = np.zeros((impacted_flights_len, slot_array_len))
        
        for index, impacted_flight in enumerate(self.impacted_flights):
            flight_preferences_array = np.full(slot_array_len, -1e6)
            assigned_time_index = np.where(slot_array == impacted_flight.assigned_time)[0][0]
            if impacted_flight.priority > 0:
                desired_time_index = np.where(slot_array == impacted_flight.desired_time)[0][0]
                margins = impacted_flight.margins
                if margins:
                    flight_preferences_array[margins[0]:margins[1]+1] = 2
                flight_preferences_array[desired_time_index] = 1
                flight_preferences_array[assigned_time_index] = 0
            else:
                flight_preferences_array[assigned_time_index:] = 0
            self.matrix_flight_preferences[index] = flight_preferences_array
        return self.matrix_flight_preferences
                
    
    def step(self):
        """
        Perform a step, updating slot array, actual flights, and assigning priorities, desired times,
        margins, and flight preferences.
            """
        logger.info("\n")
        logger.info(f"Airline Agent: {self.name}")
        logger.info("\n")
        self.set_actual_flights_list()
        logger.info("\n")
        logger.info("Actual flights priority (1: priority, 0: non priority):")
        self.assign_priority()
        self.assign_desired_time()
        logger.info("\n")
        logger.info("Margins assginment and desired time:")
        self.assign_margins()
        self.define_flight_preferences()
        logger.info("\n")
        logger.info("Flight preferences:")
        logger.info(self.matrix_flight_preferences)

        
        

