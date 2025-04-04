import mesa
import numpy as np
np.set_printoptions(suppress=True, precision=2)
import pandas as pd
import logging
import json


logger = logging.getLogger(__name__)


class PlatformAgent(mesa.Agent):

    def __init__(self,
                 unique_id, 
                 model,
                 base_value_weight_map: int,
                 percentage_reduction_weight_map: float,
                 optimization_strategy,
                 equity_monitor_strategy,
                 intervene_equity_strategy
                ):
        
        super().__init__(unique_id, model)
        # Attributes
        self.model = model
        self.base_value_weight_map = base_value_weight_map
        self.percentage_reduction_weight_map = percentage_reduction_weight_map
        self.optimization_strategy = optimization_strategy 
        self.equity_monitor_strategy = equity_monitor_strategy
        self.intervene_equity_strategy = intervene_equity_strategy
        
        self.weight_map = []

    def convert_to_weight_map(self, 
                              preferences_matrix_row: list,
                             ):
        '''
        Convert flight preferences into a weight map.

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
        reordered_numbers = np.zeros_like(original_schedule)
        # Reorder the original schedule based on the positions
        for idx, pos in enumerate(positions):
            if pos < len(original_schedule):
                reordered_numbers[pos] = original_schedule[idx]
        return reordered_numbers

    def assign_optimized_time_(self, original_schedule, new_list, airlines_list):
        #Function to assign optimized time to actual flights
        original_schedule = np.array(original_schedule)
        new_schedule = np.array(new_list)
        for airline in airlines_list:
            for actual_flight in airline.step_actual_flights:
                if actual_flight.assigned_time in original_schedule:
                    index = np.where(new_schedule == actual_flight.assigned_time)[0][0]
                    actual_flight.optimization_time = original_schedule[index]
                    
                else:
                    pass
    
    def convert_to_json_serializable(self, data):
        """
        Recursively convert NumPy arrays, int32, and float values to JSON serializable types.
    
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

        """
        # Convert NumPy arrays, int32, and float values to JSON serializable types
        converted_data = self.convert_to_json_serializable(data)
        # Write data to the JSON file
        with open(filename, 'w') as json_file:
            json.dump(converted_data, json_file)
            
    def step(self):
        '''
        Parameters
        '''
        self.airline_list = self.model.list_mesa_airline_agents
        self.matrix_preferences = []
        self.regulation_schedule = self.model.mesa_network_manager_agent.new_flight_list
        self.equity_data = self.model.equity_data
        
        '''
        Weight map
        '''
        self.weight_map = []
        # Convert preferences into weight map for each flight
        for airline in self.airline_list:
            for row in airline.matrix_flight_preferences:
                 self.matrix_preferences.append(row)
                
        # Apply intervention to weight map
        self.intervened_weight_map = self.intervene_equity_strategy.intervene_equity(
                                                                                        matrix_preferences = self.matrix_preferences,
                                                                                        equity_data = self.equity_data,
                                                                                        airline_list = self.airline_list
                                                                                            )
        
        for row in self.intervened_weight_map:
            self.convert_to_weight_map(row)
  
        # Reorder the weight map
        
        self.reordered_weight_map = self.reorder_weight_map(self.weight_map)
        logger.info("\n")
        logger.info("-----")
        logger.info("PlatformAgent")
        logger.info("\n")
        logger.info("Weight map")
        logger.info("\n")
        logger.info(self.reordered_weight_map)
        logger.info("\n")

        
        '''optimization''' 
        # optimization algorithm
        if self.reordered_weight_map and self.regulation_schedule:
            logger.info("Optimization process")
            logger.info("\n")
            self.optimizer = self.optimization_strategy.run_optimizer(flight_list = self.regulation_schedule, 
                                                                 slot_list = self.regulation_schedule, 
                                                                 au_preferences = self.reordered_weight_map)

            # define new flight list
            self.new_flight_list = self.new_flight_list_(self.regulation_schedule, self.optimizer)

            #assign optimized time to actual flights
            self.assign_optimized_time_(self.regulation_schedule, self.new_flight_list, self.airline_list)

            logger.info("\n")
            logger.info("Optimized flights:")

            # Prepare flight data
            self.flight_data = []
            
            for airline in self.airline_list:
                for actual_flight in airline.step_actual_flights:
                    data_values = {'step': self.model.step_number,
                                   'airline': airline.name,
                                   'flight_number': actual_flight.scheduled_flight.flight_number,
                                   'scheduled_time': actual_flight.scheduled_flight.scheduled_time,
                                   'assigned_time': actual_flight.assigned_time,
                                   'desired_time': actual_flight.desired_time,
                                   'optimization_time': actual_flight.optimization_time,
                                   'intervened': actual_flight.intervened,
                                   "time_assignment_seed" :actual_flight.scheduled_flight.time_assignment_seed
                                   }
                    self.flight_data.append(data_values)

                    logger.info("flight_number:%s, Scheduled_time:%s, Assigned_time: %s, Desired_time: %s, Optimized_time:%s",
                                actual_flight.scheduled_flight.flight_number,
                                actual_flight.scheduled_flight.scheduled_time,
                                actual_flight.assigned_time, 
                                actual_flight.desired_time,
                                actual_flight.optimization_time
                         )
            
            self.model.flight_data.extend(self.flight_data) 
            
            '''Equity'''
            # equity monitor
            if self.new_flight_list.any():
                self.equity = self.equity_monitor_strategy.run_equity(original_list = self.regulation_schedule,
                                                              new_list = self.new_flight_list,
                                                             optimization_result = self.optimizer,
                                                             airlines_preferences = self.reordered_weight_map,
                                                             base_value_weight_map = self.base_value_weight_map,
                                                             airline_list = self.airline_list,
                                                             step_number = self.model.step_number)
                # equity data
                self.model.equity_data = self.equity_monitor_strategy.equity_data
            else:
                print("There was no new flight list")
                logger.info("There was no new flight list")
        else:
            print("There was no weight map or no regulation schedule")
            logger.info("There was no weight map or no regulation schedule")
            
        # Prepare output data

        self.flight_data_frame = pd.DataFrame(self.model.flight_data)
        self.equity_data_frame = pd.DataFrame(self.model.equity_data)
        self.merged_df = pd.merge(self.flight_data_frame, self.equity_data_frame, on=['step', 'airline', 'flight_number'], how='outer')
        
        json_data = self.merged_df.to_dict(orient='records') # transform data frame to dict for JSON file
        self.write_list_of_dicts_to_json(json_data, "output_data.json") # write output file
        
        
        

        