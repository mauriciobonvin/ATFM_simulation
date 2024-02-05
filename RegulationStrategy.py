import numpy as np
import random


# Define the WindowStrategy interface
class RegulationStrategy:
    def regulation(self, delayed_flights, start, end, capacity = 2):
        pass

# Concrete strategy: Assign time to every x position
class ReducedCapacityStrategy(RegulationStrategy):
    def regulation(self, delayed_flights, start, end, capacity = 2):
        if delayed_flights: 
            start_from = delayed_flights[0]
        else:
            start_from = start
        available_slots = list(range(start_from, end, capacity))
        return available_slots
    
class NoCapacityStrategy(RegulationStrategy):
    def regulation(self, delayed_flights, start, end, capacity = 2):
        pass

