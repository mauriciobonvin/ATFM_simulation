import numpy as np
import random


# Define the WindowStrategy interface
class RegulationStrategy:
    def regulation(self, delayed_flights, start, end):
        pass

# Concrete strategy: Assign time to every x position
class ReducedCapacityStrategy(RegulationStrategy):
    def __init__(self, capacity=2):
        self.capacity = capacity
        
    def regulation(self, delayed_flights, start, end):
        if delayed_flights: 
            start_from = delayed_flights[0]
        else:
            start_from = start
        available_slots = list(range(start_from, end, self.capacity))
        return available_slots


class NoCapacityStrategy(RegulationStrategy):  

    
    def regulation(self, delayed_flights, start, end):
        no_capacity = []
        return no_capacity
        