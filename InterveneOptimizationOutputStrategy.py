import numpy as np
import random


class InterveneOptimizationOutputStrategy:
    def intervene_optimization_output(self, **kwargs):
        pass

# Implement concrete strategies
class HighestValueStrategy(InterveneOptimizationOutputStrategy):
    def intervene_optimization_output(self, optimization_results, weight_map):
        max_sum = float('-inf') 
        final_result = None
        for i in optimization_results:
            result = np.multiply(i,weight_map)
            total_sum = np.sum(result)
            
            if total_sum > max_sum:
                max_sum = total_sum
                final_result = i
        
        return final_result
