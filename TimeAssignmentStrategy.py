import numpy as np
import random


# Define the TimeAssignmentStrategy interface
class TimeAssignmentStrategy:
    def assign_time(self, flights, n_times, seed):
        pass

# Implement concrete strategies
class RandomTimeAssignmentStrategy(TimeAssignmentStrategy):
    def assign_time(self, flights, n_times, seed):
        set_seed = random.seed(seed)
        selected_time = random.sample(range(0,n_times), len(flights))
        random.shuffle(flights)
        flights_in_times_list = [1 if i in selected_time else 0 for i in range(n_times)]
        counter = 0
        for index, has_flight in enumerate(flights_in_times_list):
            if has_flight == 1:
                flights[counter].scheduled_time = index
                counter += 1
        return flights

class SequentialTimeAssignmentStrategy(TimeAssignmentStrategy):
    def assign_time(self, flights, n_times, seed):
        for i, flight in enumerate(flights):
            flight.scheduled_time = i % n_times
        return flights


