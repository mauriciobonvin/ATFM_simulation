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
    
class PercentageAssignmentStrategy(PriorityAssignmentStrategy):
    def __init__(self, percentage = 0.5):
        self.percentage = percentage
    
    def assign_priority(self, num_flights, seed):
        random.seed(seed)
        classes = [1,0]
        weights = [self.percentage, 1 - self.percentage]
        random_array = random.choices(classes, weights=weights, k=num_flights)
        return random_array
