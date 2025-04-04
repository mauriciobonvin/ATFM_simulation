import numpy as np
import pandas as pd
import random


class InterveneEquityStrategy:
    
    def intervene_equity(self, 
                         matrix_preferences, 
                         equity_data, 
                         airline_list
                        ):
        pass

# Implement concrete strategies
class CreditBasedInterventionStrategy(InterveneEquityStrategy):
    
    def __init__(self, 
                 equity_threshold
                ):
        self.equity_threshold = equity_threshold

        
    def intervene_equity(self, 
                         matrix_preferences, 
                         equity_data, 
                         airline_list
                        ):
        matrix_preferences_new = []
        if equity_data:
            eq_information = pd.DataFrame(equity_data)
            eq_information_df = eq_information.groupby('airline')['credits'].sum().reset_index()
            for airline in airline_list:
                filtered_eq_info = eq_information_df[eq_information_df['airline'] == airline.name]
                if not filtered_eq_info.empty:
                    current_equity = filtered_eq_info.iloc[0]['credits']
                else:
                    pass
                    
                if current_equity < self.equity_threshold:
                    for row in airline.matrix_flight_preferences:
                        intervened_preference = np.full(len(row), -1e6)
                        assigned_time_index = np.where(row == 0)[0][0]
                        intervened_preference[assigned_time_index] = 0
                        intervened_preference[assigned_time_index:] = 0
                        matrix_preferences_new.append(intervened_preference)
                    for actual_flight in airline.step_actual_flights:
                        actual_flight.intervened = 1
                else: 
                    for row in airline.matrix_flight_preferences:
                        matrix_preferences_new.append(row)
                        
        if matrix_preferences_new:
            return matrix_preferences_new
        else:
            return matrix_preferences


# Implement concrete strategies
class LowerUpperInterventionStrategy(InterveneEquityStrategy):
    
    def __init__(self, 
                 lower_bound, 
                 upper_bound
                ):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
    def intervene_equity(self, 
                         matrix_preferences, 
                         equity_data, 
                         airline_list
                        ):
        matrix_preferences_new = []
        if equity_data:
            eq_information = pd.DataFrame(equity_data)
            eq_information_df = eq_information.groupby('airline')['credits'].sum().reset_index()
            for airline in airline_list:
                filtered_eq_info = eq_information_df[eq_information_df['airline'] == airline.name]
                if not filtered_eq_info.empty:
                    current_equity = filtered_eq_info.iloc[0]['credits']
                else:
                    pass
                    
                if current_equity < self.lower_bound:
                    for row in airline.matrix_flight_preferences:
                        intervened_preference = np.full(len(row), -1e6)
                        assigned_time_index = np.where(row == 0)[0][0]
                        intervened_preference[assigned_time_index] = 0
                        intervened_preference[assigned_time_index:] = 0
                        matrix_preferences_new.append(intervened_preference)
                    for actual_flight in airline.step_actual_flights:
                        actual_flight.intervened = 1
                        
                elif current_equity > self.upper_bound:

                    
                    for row, actual_flight in zip(airline.matrix_flight_preferences, airline.step_actual_flights):
                        slot_array = np.array(airline.model.mesa_network_manager_agent.new_flight_list)
                        if not actual_flight.desired_time:
                            intervened_preference = np.full(len(row), -1e6)  # Initialize all slots to -1e6
                            # Determine indices for desired time, margins, and assigned time
                            assigned_time_index = np.where(slot_array == actual_flight.assigned_time)[0][0]
                            desired_time = self.assign_desired_time_for_flight(actual_flight, airline)
                            desired_time_index = np.where(slot_array == desired_time)[0][0]
    
                            # Update actual flight properties
                            actual_flight.priority = 1  # Set priority to high
                            actual_flight.desired_time = desired_time  # Assign desired time
                            
                            margins = self.assign_margins_for_flight(actual_flight, airline)
                            actual_flight.margins = margins  # Assign margins
                            actual_flight.intervened = 2  # Mark as intervened for high equity
                            
                            # Update matrix preferences
                            if margins:
                                intervened_preference[margins[0]:margins[1]+1] = 2  # Margin range slots
                            intervened_preference[desired_time_index] = 1  # Desired time slot
                            intervened_preference[assigned_time_index] = 0  # Assigned slot
                            
                            # Append updated preferences to the matrix
                            matrix_preferences_new.append(intervened_preference)
                                 
                        else:
                            matrix_preferences_new.append(row)
                else: 
                    for row in airline.matrix_flight_preferences:
                        matrix_preferences_new.append(row)
                        
        if matrix_preferences_new:
            return matrix_preferences_new
        else:
            return matrix_preferences

    
    def assign_desired_time_for_flight(self, 
                                       flight, 
                                       airline
                                      ):
        """
        Assigns a desired time for a flight based on the airline's strategy and flight data.
        """
        return airline.desired_time_strategy.assign_desired_time(
            flight, airline.model.mesa_network_manager_agent.new_flight_list, airline.model.seed
            )
    
    def assign_margins_for_flight(self, 
                                  flight, 
                                  airline
                                 ):
        """
        Assigns margins for a flight based on the airline's strategy and flight data.
        """
        return airline.assign_margins_strategy.assign_margins(
            flight, airline.model.mesa_network_manager_agent.new_flight_list, airline.model.seed
            )
