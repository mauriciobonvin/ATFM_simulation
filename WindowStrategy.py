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
        start = np.random.randint(0, n_times)
        width = np.random.randint(1, n_times/2)
        return start, width
