import numpy as np
import random


# Define the TimeAssignmentStrategy interface
class TimeAssignmentStrategy:
    
    def assign_time(self, flights, n_times):
        pass

# Implement concrete strategies
class RandomTimeAssignmentStrategy(TimeAssignmentStrategy):
    
    def __init__(self, time_assignment_seed):
        self.time_assignment_seed = time_assignment_seed
    
    def assign_time(self, flights, n_times):
        random.seed(self.time_assignment_seed)
        selected_time = random.sample(range(0,n_times), len(flights))
        random.shuffle(flights)
        flights_in_times_list = [1 if i in selected_time else 0 for i in range(n_times)]
        counter = 0
        for index, has_flight in enumerate(flights_in_times_list):
            if has_flight == 1:
                flights[counter].scheduled_time = index
                counter += 1
        return flights


class FixedAssignmentStrategy(TimeAssignmentStrategy):
    
    def __init__(self, schedule):
        self.schedule = schedule
        
    def assign_time(self, flights, n_times):
        for i, flight in enumerate(flights):
            flight.scheduled_time = self.schedule[i]
        return flights


class SequentialTimeAssignmentStrategy(TimeAssignmentStrategy):
    
    def assign_time(self, flights, n_times):
        for i, flight in enumerate(flights):
            flight.scheduled_time = i % n_times
        return flights


class EverySixTimeAssignmentStrategy(TimeAssignmentStrategy):
    
    def assign_time(self, flights, n_times):
        for i, flight in enumerate(flights):
            flight.scheduled_time = i//10 + (i % 10) * 6
        return flights
