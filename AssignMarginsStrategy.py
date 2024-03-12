import numpy as np
import random


class AssignMarginsStrategy:
    def assign_margins(self, actual_flight, slot_array, seed):
        pass

# Implement concrete strategies
class MarginsRandomAssignmentStrategy(AssignMarginsStrategy):
    def assign_margins(self, actual_flight, slot_array, seed):
        random.seed(seed)
        slot_array_ = np.array(slot_array)
        #print("sa", slot_array_)
        #print("fst", flight.scheduled_time)
        #print("fat", flight.assigned_time)
        scheduled_time_ = actual_flight.scheduled_flight.scheduled_time
        end = np.where(slot_array_ == actual_flight.assigned_time)[0][0]
        smaller_possible_number = min(slot_array_ , key=lambda x: (x - scheduled_time_ ) if x >= scheduled_time_ else end)

        start = np.where(slot_array_ == scheduled_time_)[0][0] if any(slot_array_ == scheduled_time_) else  np.where(slot_array_ == smaller_possible_number)[0][0]
        desired_time_index = np.where(slot_array_ == actual_flight.desired_time)[0][0]
        print("Priority strategy for flight",actual_flight.scheduled_flight.flight_number,"-> Lower margin:",start,"Upper margin:",end,"Desired time:",desired_time_index)
        lower_margin = random.randint(start, desired_time_index)
        upper_margin = random.randint(desired_time_index, end)
    
        return (lower_margin, upper_margin)
  

