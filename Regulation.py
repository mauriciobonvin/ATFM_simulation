import numpy as np
import random
import WindowStrategy
import RegulationStrategy
import Flight

import logging

logger = logging.getLogger(__name__)

class Regulation:
    def __init__(self,
                 step_number, 
                 seed, 
                 n_times,
                 flights_object_list, 
                 window_strategy, 
                 regulation_strategy, 
                 capacity=2):
        
        self.step_number = step_number
        self.seed = seed
        self.n_times = n_times
        self.scheduled_flights_object_list = flights_object_list
        self.window_strategy = window_strategy
        self.regulation_strategy = regulation_strategy
        self.capacity = capacity
        logger.info("--")
        logger.info("Outputs of file Regulation.py")
        logger.info("\n")
        
    def generate_window(self):
        window_ = self.window_strategy.window(self.seed, self.n_times)
        self.start = window_[0]
        self.end = self.start + window_[1] - 1

        logger.info("Start of the regulation in time number:%s",self.start)
        logger.info("End of the regulation in time number:%s",self.end)
        logger.info("\n")
        
    def delayed_flights(self):
        self.delayed_flights_ = []
        logger.info("List of flights and its scheduled time (scheduled times goes from 0 until %s):",self.n_times-1)
        for flight in self.scheduled_flights_object_list:
            logger.info("Flight number:%s, Scheduled time:%s",flight.flight_number,flight.scheduled_time)
            if flight.scheduled_time in range(self.start, self.end):
                self.delayed_flights_.append(flight.scheduled_time)
        self.delayed_flights_.sort()
        logger.info("\n")
        logger.info("List of delayed flights (showing scheduled time):")
        logger.info(self.delayed_flights_)
        logger.info("\n")
        
    def run_regulation_strategy(self):
        self.regulated_times = self.regulation_strategy.regulation(self.delayed_flights_,
                                                                   self.start,
                                                                   self.end, 
                                                                   self.capacity)
        logger.info("List of available time slots after regulation applied:")
        logger.info(self.regulated_times)
        logger.info("\n")
        
    def assign_slots(self):
        #print("o", self.start, self.end)
        self.actual_flights = []
        last_regulated_time = self.end
        list_of_scheduled_times = []
        for flight in self.scheduled_flights_object_list:
            list_of_scheduled_times.append(flight.scheduled_time)
            
        while self.delayed_flights_:
            if not self.regulated_times:
                if last_regulated_time in list_of_scheduled_times and last_regulated_time not in self.delayed_flights_:
                    self.delayed_flights_.append(last_regulated_time)
                    scheduled_flight = [flight for flight in self.scheduled_flights_object_list if flight.scheduled_time == self.delayed_flights_[0]][0]
                    actual_flight_ = Flight.ActualFlight(self.step_number, scheduled_flight)
                    actual_flight_.assigned_time = last_regulated_time
                    self.actual_flights.append(actual_flight_)
                    self.delayed_flights_.pop(0)
                    last_regulated_time += 1
                else:
                    scheduled_flight = [flight for flight in self.scheduled_flights_object_list if flight.scheduled_time == self.delayed_flights_[0]][0]
                    actual_flight_ = Flight.ActualFlight(self.step_number, scheduled_flight)
                    actual_flight_.assigned_time = last_regulated_time
                    self.actual_flights.append(actual_flight_)
                    self.delayed_flights_.pop(0)
                    last_regulated_time += 1
           
        
            else:
                scheduled_time = self.delayed_flights_[0]
                if scheduled_time <= self.regulated_times[0]:
                    scheduled_flight = [flight for flight in self.scheduled_flights_object_list if flight.scheduled_time == scheduled_time][0]
                    actual_flight_ = Flight.ActualFlight(self.step_number, scheduled_flight)
                    actual_flight_.assigned_time = self.regulated_times[0]
                    self.actual_flights.append(actual_flight_)
                    self.delayed_flights_.pop(0)
                    self.regulated_times.pop(0)
                else:
                    self.regulated_times.pop(0)

        logger.info("List of affected flights, scheduled times and assigned times after the regulation:")
        for flight in self.actual_flights:
            logger.info("flight number:%s, Scheduled time:%s, Assigned time: %s",
                        flight.scheduled_flight.flight_number,
                        flight.scheduled_flight.scheduled_time,
                        flight.assigned_time
                       )
            flight.scheduled_flight.list_of_actual_flights.append(flight)
            
    def assigned_time_array(self):
        
        self.assigned_scheduled_differences = []
        for flight in self.actual_flights:
            self.assigned_scheduled_differences.append(flight.assigned_time)
            
        logger.info("\n")
        logger.info("List of new slots assigned to delayed flights:")
        logger.info(self.assigned_scheduled_differences)
        logger.info("--")
        return self.assigned_scheduled_differences
    
    def start_regulation(self):
        self.generate_window()
        self.delayed_flights()
        self.run_regulation_strategy()
        self.assign_slots()
        return  self.assigned_time_array()

