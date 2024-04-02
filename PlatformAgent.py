import mesa
import numpy as np
np.set_printoptions(suppress=True, precision=2)
import logging
import json


logger = logging.getLogger(__name__)


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
                 equity_strategy,
                 intervene_weight_map_strategy,
                 intervene_optimization_output_strategy
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
        self.intervene_weight_map_strategy = intervene_weight_map_strategy
        self.intervene_optimization_output_strategy = intervene_optimization_output_strategy
        
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

    def reorder_weight_map(self, weight_map):
        '''
        Reorder the weight map for the optimizer.

        Returns:
            list: Reordered weight map.
        '''
        new_order = sorted(range(len(weight_map)), key=lambda i: next(
            (idx for idx, val in enumerate(weight_map[i]) if np.any(val == 0)), len(weight_map[i])))
        reordered_weight_map = [weight_map[i] for i in new_order]
        return reordered_weight_map
    
    def new_flight_list_(self, original_schedule, optimization_result):
        # Ensure inputs are NumPy arrays
        original_schedule = np.array(original_schedule)
        optimization_result = np.array(optimization_result)
            
        # Find the indices of '1' in each row
        positions = np.where(optimization_result == 1)[1]
        # Reorder the original schedule based on the positions
        reordered_numbers = original_schedule[positions]
        return reordered_numbers

    def assign_optimized_time_(self, original_schedule, new_list, airlines_list):
        #Function to assign optimized time to actual flights
        original_schedule = np.array(original_schedule)
        new_schedule = np.array(new_list)
        for airline in airlines_list:
            for actual_flight in airline.step_actual_flights:
                if actual_flight.assigned_time in original_schedule:
                    index = np.where(original_schedule == actual_flight.assigned_time)[0][0]
                    actual_flight.optimization_time = new_schedule[index]
                else:
                    pass
    
    def convert_to_json_serializable(self, data):
        """
        Recursively convert NumPy arrays, int32 values, and float values to JSON serializable types.
    
        Args:
        - data: Data to be converted.
    
        Returns:
        - JSON serializable data.
        """
        if isinstance(data, np.ndarray):
            return data.tolist()
        elif isinstance(data, (np.int32, np.int64)):
            return int(data)
        elif isinstance(data, (np.float32, np.float64)):
            return float(data)
        elif isinstance(data, dict):
            return {key: self.convert_to_json_serializable(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_to_json_serializable(item) for item in data]
        else:
            return data
    
    def write_list_of_dicts_to_json(self, data, filename):
        """
        Write a list of dictionaries to a JSON file.
    
        Args:
        - data: List of dictionaries to be written to JSON.
        - filename: Name of the JSON file to write to.
        """
        # Convert NumPy arrays, int32 values, and float values to JSON serializable types
        converted_data = self.convert_to_json_serializable(data)
        # Write data to the JSON file
        with open(filename, 'w') as json_file:
            json.dump(converted_data, json_file)
            
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

        # Apply intervention to weight map
        self.intervened_weight_map = self.intervene_weight_map_strategy.intervene_weight_map(weight_map = self.weight_map)

        # Reorder the weight map
        self.reordered_weight_map = self.reorder_weight_map(self.intervened_weight_map)
        logger.info("\n")
        logger.info("-----")
        logger.info("Results PlatformAgent.py")
        logger.info("\n")
        logger.info("Weight map")
        logger.info("\n")
        logger.info(self.reordered_weight_map)
        logger.info("\n")
        
        '''optimization''' 
        if self.reordered_weight_map and self.regulation_schedule:
            logger.info("Optimization process")
            logger.info("\n")
            self.optimizer = self.optimization_strategy.run_optimizer(flight_list = self.regulation_schedule, 
                                                                 slot_list = self.regulation_schedule, 
                                                                 au_preferences = self.reordered_weight_map)
            
            # intevene optimization output
            self.intervene_optimization_output = self.intervene_optimization_output_strategy.intervene_optimization_output(
                optimization_results = self.optimizer,
                weight_map = self.reordered_weight_map,
            )
            
            # define new flight list
            self.new_flight_list = self.new_flight_list_(self.regulation_schedule, self.intervene_optimization_output)

            #assign optimized time to actual flights
            self.assign_optimized_time_(self.regulation_schedule, self.new_flight_list, self.airline_list)

            logger.info("\n")
            logger.info("Optimized flights:")
            for airline in self.airline_list:
                for actual_flight in airline.step_actual_flights:
                    logger.info("flight_number:%s, Scheduled_time:%s, Assigned_time: %s, Optimized_time:%s",
                                actual_flight.scheduled_flight.flight_number,
                                actual_flight.scheduled_flight.scheduled_time,
                                actual_flight.assigned_time, 
                                actual_flight.optimization_time
                         )
        
            '''Equity'''
            if self.new_flight_list.any():
                self.equity = self.equity_strategy.run_equity(original_list = self.regulation_schedule,
                                                              new_list = self.new_flight_list,
                                                             optimization_result = self.intervene_optimization_output,
                                                             airlines_preferences = self.reordered_weight_map,
                                                             base_value_weight_map = self.base_value_weight_map,
                                                             airline_list = self.airline_list,
                                                             step_number = self.model.step_number)
                # export output data as json file
                self.write_list_of_dicts_to_json(self.equity_strategy.all_credit_data, "output_data.json")
            else:
                print("There was no new flight list")
                logger.info("There was no new flight list")
        else:
            print("There was no weight map or no regulation schedule")
            logger.info("There was no weight map or no regulation schedule")

        