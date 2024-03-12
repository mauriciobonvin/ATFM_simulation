import mesa
import numpy as np
np.set_printoptions(suppress=True, precision=2)


class PlatformAgent(mesa.Agent):

    """
        Represents an agent that models different mechanisms in the simulation.
        """

    def __init__(self,
                 unique_id, 
                 model,
                 base_value_weight_map: int,
                 percentage_reduction_weight_map: float,
                 optimization_strategy,
                 equity_strategy
                ):
        '''
        Initialize a PlatformAgent instance.

        Args:
            unique_id: Unique identifier for the agent.
            model: Reference to the model containing this agent.
        '''
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)
        # Attributes
        self.model = model
        self.base_value_weight_map = base_value_weight_map
        self.percentage_reduction_weight_map = percentage_reduction_weight_map
        self.optimization_strategy = optimization_strategy 
        self.equity_strategy = equity_strategy
        
        self.weight_map = []

    def convert_to_weight_map(self, 
                              preferences_matrix_row: list,
                             ):
        '''
        Convert flight preferences into a weight map.

        Args:
            preferences_matrix_row (list): List representing flight preferences.
        '''
        preferences_matrix_row = np.array(preferences_matrix_row)
        desired_slot_index = np.where(preferences_matrix_row == 1)[0]
        reduced_value_left = self.base_value_weight_map * (1 - self.percentage_reduction_weight_map)
        reduced_value_right = self.base_value_weight_map * (1 - self.percentage_reduction_weight_map)
        if len(desired_slot_index) == 0:
            return self.weight_map.append(preferences_matrix_row)
        else:
            for i in range(desired_slot_index[0], -1, -1):
                if preferences_matrix_row[i] == 2:
                    preferences_matrix_row[i] = reduced_value_left
                    reduced_value_left = reduced_value_left * (1 - self.percentage_reduction_weight_map)
                else:
                    pass
            for i in range(desired_slot_index[0], len(preferences_matrix_row)):
                if preferences_matrix_row[i] == 2:
                    preferences_matrix_row[i] = reduced_value_right
                    reduced_value_right = reduced_value_right * (1 - self.percentage_reduction_weight_map)
                else:
                    pass
            preferences_matrix_row[desired_slot_index] = self.base_value_weight_map
            return self.weight_map.append(preferences_matrix_row)

    def reorder_weight_map(self):
        '''
        Reorder the weight map for the optimizer.

        Returns:
            list: Reordered weight map.
        '''
        new_order = sorted(range(len(self.weight_map)), key=lambda i: next(
            (idx for idx, val in enumerate(self.weight_map[i]) if np.any(val == 0)), len(self.weight_map[i])))
        reordered_weight_map = [self.weight_map[i] for i in new_order]
        return reordered_weight_map

    def step(self):
        '''Parameters'''
        # Get airline_list from model and parameters
        self.airline_list = self.model.list_mesa_airline_agents
        self.matrix_preferences = []
        self.regulation_schedule = self.model.slot_array
        
        '''Weight map'''
        self.weight_map = []
        # Convert preferences into weight map for each flight
        for airline in self.airline_list:
            for row in airline.matrix_flight_preferences:
                 self.matrix_preferences.append(row)
        
        for row in self.matrix_preferences:
            self.convert_to_weight_map(row)
        #print("weight_map",self.weight_map)
        # Reorder the weight map
        self.reordered_weight_map = self.reorder_weight_map()
        print("\n")
        print("-----")
        print("Results PlatformAgent.py")
        print("\n")
        print("Weight map")
        print("\n")
        print(self.reordered_weight_map)
        print("\n")
        
        '''optimization''' 
        if self.reordered_weight_map and self.regulation_schedule:
            print("Optimization process")
            print("\n")
            self.optimizer = self.optimization_strategy.run_optimizer(flight_list = self.regulation_schedule, 
                                                                 slot_list = self.regulation_schedule, 
                                                                 au_preferences = self.reordered_weight_map)

            #print("optimization output", self.optimizer)
            # assign optimized time to actual flights and provide the new flight list
            self.new_flight_list = self.optimization_strategy.new_flight_list_assign_optimized_time(
                self.regulation_schedule,
                self.optimizer,
                self.airline_list
            )
            
                    
            #print("nl", self.new_flight_list)
            print("\n")
            print("Optimized flights:")
            for airline in self.airline_list:
                for actual_flight in airline.step_actual_flights:
                    print("flight_number",
                          actual_flight.scheduled_flight.flight_number,
                          "Scheduled_time",
                          actual_flight.scheduled_flight.scheduled_time,
                          "Assigned_time",
                          actual_flight.assigned_time,
                          "Optimized_time",
                          actual_flight.optimization_time
                         )
        
            '''Equity'''
            if self.new_flight_list.any():
                self.equity = self.equity_strategy.run_equity(original_list = self.regulation_schedule,
                                                              new_list = self.new_flight_list,
                                                             optimization_result = self.optimizer,
                                                             airlines_preferences = self.reordered_weight_map,
                                                             base_value_weight_map = self.base_value_weight_map,
                                                             airline_list = self.airline_list,
                                                             step_number = self.model.step_number)
            else:
                pass
        else:
            pass

