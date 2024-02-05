import numpy as np
np.set_printoptions(suppress=True, precision=2)
import pandas as pd
import random
import copy

class Clearing:
    
    """
       Represents a Clearing object responsible for performing clearing operations in a simulation.
       """
 
    def __init__(self,
                 original_list: list,
                 new_list: list,
                 optimization_result:list,
                 airlines_preferences: list,
                 base_value_weight_map: int,
                 bonus: float):
        '''
                Initializes the Clearing object with the given parameters.

                Args:
                    original_list (list): List of original flight slots.
                    new_list (list): List of new flight slots.
                    utility (list): List of flight utilities.
                    airlines_preferences (list): List of airlines' preferences.
                    base_value_weight_map (int): Base value weight map.
                    bonus (float): Bonus factor.
                '''
        self.original_list = np.array(original_list)
        self.optimization_result = optimization_result
        self.airlines_preferences = np.array(airlines_preferences)
        self.bonus = bonus
        self.base_value_weight_map = base_value_weight_map
        self.utility = None
        self.new_list = new_list
        
        #print("original_list", self.original_list)
        #print("new_list", self.new_list)
    
    '''Data preparation'''
    
    def array_to_utility(self):
        '''
        Convert a binary array representation of flights to an array with flight utilities.

        Parameters:
            array (list): Binary array representation of flights.
            preference (list): Flight-slot preference matrix.

        Returns:
            list: A modified copy of the input array with flight utilities instead of binary values.
         '''
        self.array_utility = copy.deepcopy(self.optimization_result)
        for i, row in enumerate(self.array_utility):
            for j, element in enumerate(row):
                if element == 1:
                    self.array_utility[i][j] = self.airlines_preferences[i][j]
        return self.array_utility
    
    def search_list_of_lists(self):
        '''
        Search a list of lists and return all the float values found.

        Parameters:
            list_of_lists (list): List of lists containing numeric values.

        Returns:
            list: A list containing all the float values found in the input list of lists.
        '''
        self.utility = []
        for i in range(len(self.array_utility[0])):
            for sublist in self.array_utility:
                if isinstance(sublist[i], float):
                    self.utility.append(sublist[i])
        #print("ulti", self.utility)
        return self.utility
    
    ''' Clearing'''
    
    def additional_utility(self):
        '''
        Calculates the additional utility and index of each flight in the new list.

        Returns:
            tuple: A tuple containing the additional utility array and index array.
        '''

        # return the index of the flight in the new list flight and
        # the distance from previous to new slot
        add_util = []
        index = []
        for i in range(len(self.original_list)):
            original_flight = self.original_list[i]
            index_new_in_original = np.where(self.new_list == original_flight)[0][0]
            to_new_slot_distance = int(index_new_in_original) - i
            add_util.append(to_new_slot_distance)
            index.append(index_new_in_original)
        self.add_util = np.array(add_util)
        self.index = np.array(index)
        print("add_util", self.add_util)
        print("index", self.index)
        return self.add_util, self.index

    def net_optimized(self):

        '''
        Calculates the net optimized utility for each flight.

        Returns:
            tuple: A tuple containing the net optimized utility array and index array.
        '''
        self.net_opt = []
        self.net_index = []
        add_util_ = np.copy(self.add_util)
        index_ = self.index
        for i in range(len(self.utility)):
            flight_generated_utility = self.utility[i]
            flight_additional_utility_index = np.where(index_ == i)[0][0]
            net_utility = flight_generated_utility + add_util_[flight_additional_utility_index]
            self.net_opt.append(net_utility)
            self.net_index.append(flight_additional_utility_index)
        self.net_opt = np.array(self.net_opt)
        #print("net_opt", self.net_opt)
        #print("net_index", self.net_index)
        self.matrix_copy_ = np.copy(self.airlines_preferences)
        self.matrix_copy_[self.matrix_copy_ < 0] = 0
        empty_list = [None] * len(self.net_index)
        # fill empty list with utility obtain by each flight
        for i in range(len(self.matrix_copy_[0])):
            net_index_ = self.net_index[i]
            empty_list[net_index_] = self.matrix_copy_[net_index_][i]
        #print("empty list", empty_list)
        # substract distance
        add_util_[add_util_ > 0] = 0
        self.net_opt_util = np.array(empty_list) + np.array(add_util_)
        #print("self.net_opt_util", self.net_opt_util)
        return self.net_opt, self.net_index, self.net_opt_util

    def contested_slots(self):
        '''
               Identifies contested flight slots.

               Returns:
                   numpy.ndarray: Array containing indexes of contested flight slots.
               '''

        # identify max values per column
        self.matrix_copy = np.copy(self.airlines_preferences)
        self.matrix_copy[self.matrix_copy < 0] = 0
        # print("matrix", self.matrix_copy)
        self.max_values = np.max(self.matrix_copy, axis=0)
        # obtain index of all max values of the columns
        self.all_max_indices = [np.where(column == max_val)[0]
                                for column, max_val in zip(self.airlines_preferences.T, self.max_values)]
        self.contested_slot_indexes = []
        for i in range(len(self.max_values)):
            if self.utility[i] > 0 and len(self.all_max_indices[i]) > 1 and self.max_values[i] == self.base_value_weight_map:
                self.contested_slot_indexes.append(i)
        self.contested_slot_indexes = np.array(self.contested_slot_indexes)
        #print("allmaxindeces", self.all_max_indices)
        #print("utility", self.utility)
        #print("index", self.contested_slot_indexes)
        return self.contested_slot_indexes

    def ideal_utility(self):
        '''
               Calculates the ideal utility for contested flight slots.

               Returns:
                   numpy.ndarray: Array containing ideal utility values for contested slots.
               '''

        index_contested_slot = self.contested_slot_indexes
        self.matrix_ideal = np.copy(self.matrix_copy)
        self.matrix_ideal[self.matrix_ideal < self.base_value_weight_map] = 0
        self.net_equis = []
        for i in index_contested_slot:
            self.ideal = []
            for _ in range(len(self.matrix_ideal[i])):
                pre_ideal_value = self.matrix_ideal[:, i][_] - _
                self.ideal.append(pre_ideal_value)
            self.ideal = np.array(self.ideal)
            self.ideal[self.ideal < 0] = 0
            self.matrix_ideal[:, i] = self.ideal
            self.net_equis.append(self.ideal)
        # self.matrix_ideal[self.matrix_ideal < 0] = 0
        self.net_ideal_util = []
        for i in range(len(self.matrix_ideal[0])):
            if i in index_contested_slot:
                self.net_ideal_util.append(sum(self.matrix_ideal[:, i]))
            else:
                self.net_ideal_util.append(0)
        self.net_ideal_util = np.array(self.net_ideal_util)
        #print("net_ideal_util", self.net_ideal_util)
        return self.net_ideal_util

    def nou(self):
        '''
               Calculates the Net Optimized Utility (NOU) for each flight.

               Returns:
                   numpy.ndarray: Array containing NOU values for contested slots.
               '''

        # copy matrix
        matrix = np.copy(self.matrix_copy)
        #print("nou_matrix", matrix)
        net_index = self.net_index
        add_util = np.copy(self.add_util)
        # initialize empty list
        empty_list = [None] * len(net_index)
        # fill empty list with utility obtain by each flight
        for i in range(len(matrix[0])):
            net_index_ = net_index[i]
            empty_list[net_index_] = matrix[net_index_][i]
        #print("empty list", empty_list)
        # substract distance
        add_util[add_util > 0] = 0
        self.net_opt_util = np.array(empty_list) + np.array(add_util)
        #print("self.net_opt_util", self.net_opt_util)
        # calculate nou per contested slot
        max_indices = self.all_max_indices
        index_contested_slot = self.contested_slot_indexes
        self.net_opt_ = []
        for i in range(len(matrix[0])):
            if i in index_contested_slot:
                net_opt_lst = []
                for _ in range(len(matrix[0])):
                    if _ in max_indices[i]:
                        net_opt_lst.append(self.net_opt_util[_])
                    else:
                        net_opt_lst.append(0)
                if self.utility[i] != self.base_value_weight_map:
                    print("utility is not achieved by max value")
                    index_ = self.net_index[i]
                    net_opt_lst[index_] = self.net_opt_util[index_]
                self.net_opt_.append(net_opt_lst)
        #print("net_opt", self.net_opt_)
        self.sum_net_opt = []
        # create an array of len(matrix[0]) that contains the sum of net optimized utility of contested slots
        counter = 0
        for i in range(len(matrix[0])):
            if i in index_contested_slot:
                suma = sum(self.net_opt_[counter])
                if suma == 0:
                    self.sum_net_opt.append(self.net_opt_util[self.net_index[i]])
                else:
                    self.sum_net_opt.append(suma)
                counter += 1

            else:
                self.sum_net_opt.append(0)
        self.sum_net_opt = np.array(self.sum_net_opt)
        #print("sum_net_opt", self.sum_net_opt)
        return self.sum_net_opt

    def degradation_ratio(self):
        '''
        Calculates the degradation ratio of the flights.

        Returns:
            float: The degradation ratio.
        '''
        self.ratio = (self.sum_net_opt - self.net_ideal_util) / self.net_ideal_util
        # print("ratio", self.ratio)
        return self.ratio

    def net_equitable_utility(self):
        '''
           Calculates the net equitable utility for contested flight slots.

           Returns:
               list: List of net equitable utility values.
           '''

        ideal_ = np.array(self.net_equis)
        #print("ideal", ideal_)
        degr_ratio = self.ratio
        multiplier = (1 + degr_ratio)
        #print("mutilple", multiplier)
        index_contested_slot = self.contested_slot_indexes
        self.net_equi = []
        for i in range(len(index_contested_slot)):
            self.net_equi.append(ideal_[i] * multiplier[index_contested_slot[i]])
        #print("net_equi", self.net_equi)

        return self.net_equi

    def cash_flow(self):
        '''
                Calculates cash flows for contested flight slots.

                Returns:
                    numpy.ndarray: Array containing cash flow values.
                '''
        optim_ = np.array(self.net_opt_)
        ideal_ = np.array(self.net_equi)
        cf_ideal = optim_ - ideal_
        self.flattened_cf = np.sum(cf_ideal, axis=0)
        #print("cf",self.flattened_cf)
        return self.flattened_cf
        
    def social_utility(self):
        """
        Calculate social utility for each participant.

        Returns:
            numpy.ndarray: Net bonus for each participant.
        """
        # Retrieve bonus percentage
        bonus = self.bonus
        # Determine market creators
        add_util = self.add_util
        market_creators = [i if i > 0 else 0 for i in add_util]
        # Convert to NumPy array and calculate total market creators
        market_creators = np.array(market_creators)
        total_market_creators = np.sum(market_creators)
        # Calculate corresponding percentages for market creators
        if total_market_creators != 0:
            corresponding_percentage = market_creators / total_market_creators
        else:
            corresponding_percentage = np.zeros_like(market_creators)
        # Obtain bonus from non-contested slots
        net_opt_utility = np.array(self.net_opt_util)
        # Obtain bonus from contested slots through equitable utilities
        contested_slots = self.contested_slot_indexes
        if contested_slots.size > 0:
            all_max_index = self.all_max_indices
            net_equi = self.net_equi
            net_equi_sum = np.sum(net_equi, axis=0)
            # Determine bonuses for contested slots
            bonus_cont = [net_equi_sum[i] if net_equi_sum[i] > 0 else net_opt_utility[i] for i in range(len(net_equi_sum))]
            bonus_cont = np.array(bonus_cont)
            bonus_ = bonus_cont * bonus
        else:
            # Determine bonuses for non-contested slots
            bonus_ = net_opt_utility * bonus
        # Calculate the sum of bonuses
        sum_bonus = np.sum(bonus_)
        # Calculate distributed bonus based on corresponding percentages
        distributed_bonus = corresponding_percentage * sum_bonus
        # Calculate net bonus by subtracting initial bonus from distributed bonus
        self.net_bonus = distributed_bonus - bonus_
        # Return the net bonus for each participant
        return self.net_bonus

    def clearing(self):
        '''
              Performs the clearing process and calculates movement.

              Returns:
                  numpy.ndarray: Array containing movement values.
              '''
        # utility for non contested flights
        self.movement = self.add_util
        self.movement = self.movement.astype(float)
        # print("movement", self.movement)
        # utility and cash flow for contested flights
        contested = self.contested_slot_indexes
        if contested.size > 0:
            print("there are contested slots")
            cash_flow = self.flattened_cf
            self.movement = self.movement - cash_flow
        bonus = self.net_bonus
        self.movement = self.movement + bonus
        self.movement = np.around(self.movement, decimals=2)
        print("after cf", self.movement)
        print("check", sum(self.movement))
        return self.movement

    def perform_clearing(self):
        '''
                Performs the entire clearing process.

                Returns:
                    numpy.ndarray: Array containing movement values.
                '''
        self.array_to_utility()
        self.search_list_of_lists()
        self.additional_utility()
        self.net_optimized()
        self.contested_slots()
        if self.contested_slot_indexes.size > 0:
            self.ideal_utility()
            self.nou()
            self.degradation_ratio()
            self.net_equitable_utility()
            self.cash_flow()
        self.social_utility()
        return self.clearing()
    
    def initial_credits(self, airlines_list: list):
        all_credit_data_ = []
        airlines = airlines_list
        for airline in airlines:
            credits = 100
            data_values_ = {'airline': airline.name,
                                   'flight_number': -1,
                                   'assigned_time': 0,
                                   'optimization_time': 0,
                                   'credits': credits,
                                   'step_counter': 0}
            all_credit_data_.append(data_values_)
        return all_credit_data_
            
    def movements_to_credit(self, airlines_list: list, step_number: int):
        '''
        Convert movements data to credit data for each airline.

        Args:
            clearing_moves (list): List of clearing movements.
            airlines_list (list): List of airlines.

        '''
        all_credit_data = []
        original_list = np.array(self.original_list)
        movements_ = self.movement
        airlines = airlines_list
        for airline in airlines:
            credits = 0
            for actual_flight in airline.step_actual_flights:
                if actual_flight.assigned_time in original_list:
                    index = np.where(original_list == actual_flight.assigned_time)[0][0]
                    credits += movements_[index]
                    data_values = {'airline': airline.name,
                                   'flight_number': actual_flight.scheduled_flight.flight_number,
                                   'assigned_time': actual_flight.assigned_time,
                                   'optimization_time': actual_flight.optimization_time,
                                   'credits': credits,
                                   'step_counter': step_number}
                    all_credit_data.append(data_values)
        return all_credit_data
            