import numpy as np
import random


# Define the WindowStrategy interface
class WindowStrategy:
    def window(self,seed, n_times):
        pass

# Concrete strategy: Assign time to every x position
class RandomWindowStrategy(WindowStrategy):
    def window(self, seed, n_times):
        random.seed(seed)
        start = random.randint(0, n_times)
        width = random.randint(1, int(n_times//2))
        return start, width


class PredefinedWindowStrategy(WindowStrategy):
    def __init__(self, defined_window):
        self.defined_window = defined_window
        
    def window(self, seed, n_times):
        tuple_ = self.defined_window[seed]
        start = tuple_[0]
        width = tuple_[1]
        return start, width
