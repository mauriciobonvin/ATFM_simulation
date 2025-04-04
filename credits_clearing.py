import numpy as np
np.set_printoptions(suppress=True, precision=2)
import pandas as pd
import random
import copy

import logging
logger = logging.getLogger(__name__)


class Clearing:
    
    def __init__(self,
                 original_list: list,
                 new_list: list,
                 optimization_result:list,
                 airlines_preferences: list,
                 base_value_weight_map: int
                ):
        #attributes
        self.original_list = np.array(original_list)
        self.optimization_result = optimization_result
        self.airlines_preferences = np.array(airlines_preferences)
        self.base_value_weight_map = base_value_weight_map
        self.utility = None
        self.new_list = new_list
        
    
    '''Data preparation'''
    
    def array_to_utility(self):

        multiply_matrixes = self.optimization_result * self.airlines_preferences
        self.utility = np.sum(multiply_matrixes, axis = 0)
        return self.utility
        
    ''' Clearing'''
    
    def additional_utility(self):
        '''
        Calculates the additional utility and index of each flight in the new list.
        '''
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
        logger.info("-------")
        logger.info("Credits clearing process:")
        logger.info("\n")
        logger.info("Additional utility: %s", self.add_util)
        logger.info("\n")
        
        return self.add_util, self.index

    def net_optimized(self):
        '''
        Calculates the net optimized utility for each flight.
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
        self.matrix_copy_ = np.copy(self.airlines_preferences)
        self.matrix_copy_[self.matrix_copy_ < 0] = 0
        empty_list = [None] * len(self.net_index)
        # fill empty list with utility obtained by each flight
        for i in range(len(self.matrix_copy_[0])):
            net_index_ = self.net_index[i]
            empty_list[net_index_] = self.matrix_copy_[net_index_][i]
        # substract distance
        add_util_[add_util_ > 0] = 0
        self.net_opt_util = np.array(empty_list) + np.array(add_util_)

        logger.info("\n")
        logger.info("Net optimized utility: %s", self.net_opt_util)
        logger.info("\n")
        
        return self.net_opt, self.net_index, self.net_opt_util

    def contested_slots(self):
        '''
               Identifies contested flight slots.
               '''
        # identify max values per column
        self.matrix_copy = np.copy(self.airlines_preferences)
        self.matrix_copy[self.matrix_copy < 0] = 0
        self.max_values = np.max(self.matrix_copy, axis=0)
        # obtain index of all max values of the columns
        self.all_max_indices = [np.where(column == max_val)[0]
                                for column, max_val in zip(self.airlines_preferences.T, self.max_values)]        
        self.contested_slot_indexes = []
        for i in range(len(self.max_values)):
            if self.utility[i] > 0 and len(self.all_max_indices[i]) > 1 and self.max_values[i] == self.base_value_weight_map:
                self.contested_slot_indexes.append(i)
        self.contested_slot_indexes = np.array(self.contested_slot_indexes)
        logger.info("\n")
        logger.info("There are %s contested slots", self.contested_slot_indexes.size)
        logger.info("\n")
        return self.contested_slot_indexes

    def ideal_utility(self):
        '''
               Calculates the ideal utility for contested flight slots.
               '''
        index_contested_slot = self.contested_slot_indexes
        self.matrix_ideal = np.copy(self.matrix_copy)
        self.matrix_ideal[self.matrix_ideal < self.base_value_weight_map] = 0

        self.net_equis = []
        for i in index_contested_slot:
            self.ideal = []
            for _ in range(len(self.matrix_ideal[i])):
                distance_to_index = _ - i
                if distance_to_index >= 0:
                    pre_ideal_value = self.matrix_ideal[:, i][_] - distance_to_index
                    self.ideal.append(pre_ideal_value)
                else:
                    self.ideal.append(0)
            self.ideal = np.array(self.ideal)
            self.ideal[self.ideal < 0] = 0
            self.matrix_ideal[:, i] = self.ideal
            self.net_equis.append(self.ideal)
        self.net_ideal_util = []
        for i in range(len(self.matrix_ideal[0])):
            if i in index_contested_slot:
                self.net_ideal_util.append(sum(self.matrix_ideal[:, i]))
            else:
                self.net_ideal_util.append(0)
        self.net_ideal_util = np.array(self.net_ideal_util)
        logger.info("\n")
        logger.info("Ideal utility is :%s", self.net_ideal_util)
        logger.info("\n")
        return self.net_ideal_util

    def optimized_utility(self):
        '''
               Calculates the Net Optimized Utility (NOU) for each flight.
               '''
        # copy matrix
        matrix = np.copy(self.matrix_copy)
        net_index = self.net_index
        add_util = np.copy(self.add_util)
        # initialize empty list
        empty_list = [None] * len(net_index)
        # fill empty list with utility obtained by each flight
        for i in range(len(matrix[0])):
            net_index_ = net_index[i]
            empty_list[net_index_] = matrix[net_index_][i]
        # subtract distance
        add_util[add_util > 0] = 0
        self.net_opt_util = np.array(empty_list) + np.array(add_util)
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
                    index_ = self.net_index[i]
                    net_opt_lst[index_] = self.net_opt_util[index_]
                self.net_opt_.append(net_opt_lst)
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
        logger.info("\n")
        logger.info("Optimized utility is :%s", self.sum_net_opt)
        logger.info("\n")
        return self.sum_net_opt

    def degradation_ratio(self):
        '''
        Calculates the degradation ratio of the flights.
        '''
        self.ratio = (self.sum_net_opt - self.net_ideal_util) / self.net_ideal_util
        logger.info("\n")
        logger.info("Degradation ratio is :%s", self.ratio)
        logger.info("\n")
        return self.ratio

    def equitable_utility(self):
        '''
           Calculates the net equitable utility for contested flight slots.
           '''

        ideal_ = np.array(self.net_equis)
        degr_ratio = self.ratio
        multiplier = (1 + degr_ratio)
        index_contested_slot = self.contested_slot_indexes
        self.net_equi = []
        for i in range(len(index_contested_slot)):
            self.net_equi.append(ideal_[i] * multiplier[index_contested_slot[i]])
        logger.info("\n")
        logger.info("Equitable utility is :%s", self.net_equi)
        logger.info("\n")
        return self.net_equi

    def cash_flow(self):
        '''
                Calculates cash flows for contested flight slots.
                '''
        optim_ = np.array(self.net_opt_)
        ideal_ = np.array(self.net_equi)
        cf_ideal = optim_ - ideal_
        self.flattened_cf = np.sum(cf_ideal, axis=0)
        logger.info("\n")
        logger.info("Cash flow is :%s", self.flattened_cf)
        logger.info("\n")
        return self.flattened_cf
   
    def clearing(self):
        '''
              Performs the clearing process and calculates movement.
              '''
        # utility for non-contested flights
        self.movement = self.add_util
        self.movement = self.movement.astype(float)
        # utility and cash flow for contested flights
        contested = self.contested_slot_indexes
        if contested.size > 0:
            cash_flow = self.flattened_cf
            self.movement = self.movement - cash_flow
        self.movement = np.around(self.movement, decimals=2)
        logger.info("-------")
        logger.info("Credit Clearing results:")
        logger.info("\n")
        logger.info("Credit movements: %s", self.movement)
        logger.info("\n")
        logger.info("check sum for correctness of calculations (should be 0 or near 0): %s", sum(self.movement))
        return self.movement

    def perform_clearing(self):
        '''
                Performs the entire clearing process.
                '''
        self.array_to_utility()
        self.additional_utility()
        self.net_optimized()
        self.contested_slots()
        if self.contested_slot_indexes.size > 0:
            self.ideal_utility()
            self.optimized_utility()
            self.degradation_ratio()
            self.equitable_utility()
            self.cash_flow()
        return self.clearing()
    
    def initial_credits(self, airlines_list: list, initial_credits_:int):
        all_credit_data_ = []
        airlines = airlines_list
        for airline in airlines:
            credits = initial_credits_
            data_values_ = {'airline': airline.name,
                                  'credits': credits,
                                   'step': 0}
            all_credit_data_.append(data_values_)
            
        return all_credit_data_
            
    def movements_to_credit(self, airlines_list: list, step_number: int):
        '''
        Convert movements data to credit data for each airline.
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
                    credits = movements_[index]
                    data_values = {'step': step_number,
                                   'airline': airline.name,
                                   'flight_number': actual_flight.scheduled_flight.flight_number,
                                   'credits': credits
                                   }
                    all_credit_data.append(data_values)
        return all_credit_data
            