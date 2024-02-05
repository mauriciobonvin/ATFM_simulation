import numpy as np
import random



class PriorityAssignmentStrategy:
    def assign_priority(self, num_flights, seed):
        pass

# Implement concrete strategies
class PriorityRandomAssignmentStrategy(PriorityAssignmentStrategy):
    def assign_priority(self, num_flights, seed):
        random.seed(seed)
        random_array = [random.randint(0, 1) for _ in range(num_flights)]
        return random_array
    
class OtherAssignmentStrategy(PriorityAssignmentStrategy):
    def assign_priority(self, num_flights, seed):
        pass

