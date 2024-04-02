import numpy as np
import random


class InterveneWeightMapStrategy:
    
    def intervene_weight_map(self, **kwargs):
        pass

# Implement concrete strategies
class IncreaseWeightMapStrategy(InterveneWeightMapStrategy):
    
    def __init__(self, increase_amount):
        self.increase_amount = increase_amount
        
    def intervene_weight_map(self, weight_map):
        result_weight_map = []
        for row in weight_map:
            new_row = []
            for element in row:
                new_row.append(element + self.increase_amount)
            result_weight_map .append(new_row)
        return result_weight_map
