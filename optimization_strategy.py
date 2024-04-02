from docplex.mp.model import Model
import numpy as np
import copy
import logging

logger = logging.getLogger(__name__)


class OptimizationStrategy:
    def run_optimizer(self, **kwargs):
        pass
    
class LinearAssignmentStrategy(OptimizationStrategy):
    def run_optimizer(self, flight_list:list, slot_list:list, au_preferences:list):

        #data preparation
            # create range of flight and slot lists to use in the model
        F = range(len(flight_list))
        S = range(len(slot_list))
        
        # create model
        m = Model(name='Slot optimizer', log_output=True)

            # define variables
                # a matrix variable where 1 means slot assigned, 0 otherwise
        x = m.binary_var_matrix(F,S, name= "slot assignment")

            # objective
                # maximize the utility of the slot assignment
        m.maximize(m.sum(au_preferences[i][j]*x[i,j] for i in F for j in S))

            # constraints
                # This pair of constraints ensures that each flight is assigned 1 slot
        for i in F:
            m.add_constraint(sum(x[i,j] for j in S) == 1)
        for j in S:
            m.add_constraint(sum(x[i,j] for i in F) == 1)

            # solve and print results
        solution = m.solve()
        display_solution = m.print_solution()

        logger.info("Optimization process:")
        logger.info(solution)

        values_list = []

        for var in m.iter_variables():
            x_values = solution.get_value(var)
            values_list.append(x_values)

        list_of_list = [values_list[i:i+len(slot_list)] for i in range(0, len(values_list), len(slot_list))]

        result = [list_of_list]
        
        return result
        

