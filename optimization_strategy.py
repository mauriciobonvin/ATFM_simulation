from docplex.mp.model import Model
import numpy as np
import copy

class OptimizationStrategy:
    def run_optimizer(self, **kwargs):
        pass
    
    def new_flight_list_assign_optimized_time(self,original_schedule, optimization_result, airlines_list):
        self.list_to_flight(original_schedule, optimization_result)
        self.new_flight_list_ = self.new_flight_list()
        self.assign_optimized_time(airlines_list)
        return self.new_flight_list_
    
    def list_to_flight(self, original_schedule, optimization_result):
        '''
        Convert a binary array representation of flights to a list with flight numbers.

        Parameters:
            array (list): Binary array representation of flights.
            flights_list (list): List of flights assigned to each airline.

        Returns:
            list: A modified copy of the input array with flight numbers instead of binary values.
        '''
        self.original_schedule = original_schedule
        self.optimization_result = optimization_result
        self.list_to_flights = copy.deepcopy(optimization_result)
        for i, row in enumerate(self.list_to_flights):
            for j, element in enumerate(row):
                if element == 1:
                    self.list_to_flights [i][j] = float(self.original_schedule[i])
        return self.list_to_flights 
    
    def new_flight_list(self):
        '''
        Generate a list of newly assigned flights.

        Parameters:
            list_to_flights (list): List of flights assigned to each airline.

        Returns:
            list: A list containing the flight numbers of newly assigned flights.

        '''
        self.new_list = []
        for i in range (len(self.list_to_flights[0])):
            for sublist in self.list_to_flights:
                if isinstance(sublist[i], float):
                    self.new_list.append(int(sublist[i]))
        return np.array(self.new_list)
    
    def assign_optimized_time(self, airlines_list):
        original_schedule = np.array(self.original_schedule)
        new_schedule = np.array(self.new_list)
        for airline in airlines_list:
            for actual_flight in airline.step_actual_flights:
                if actual_flight.assigned_time in original_schedule:
                    index = np.where(original_schedule == actual_flight.assigned_time)[0][0]
                    actual_flight.optimization_time = new_schedule[index]
                else:
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

        values_list = []

        for var in m.iter_variables():
            x_values = solution.get_value(var)
            values_list.append(x_values)

        list_of_list = [values_list[i:i+len(slot_list)] for i in range(0, len(values_list), len(slot_list))]
        
        return list_of_list

