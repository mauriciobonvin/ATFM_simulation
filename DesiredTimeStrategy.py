import numpy as np
import random


class DesiredTimeStrategy:
    def assign_desired_time(self, actual_flight, slot_array, seed):
        pass

# Implement concrete strategies
class DesiredTimeRandomAssignmentStrategy(DesiredTimeStrategy):
    def assign_desired_time(self, actual_flight, slot_array, seed):
        random.seed(seed)
        slot_array_ = np.array(slot_array)
        scheduled_time = actual_flight.scheduled_flight.scheduled_time
        end = np.where(slot_array_ == actual_flight.assigned_time)[0][0]
        smaller_possible_number = min(slot_array_ , key=lambda x: (x - scheduled_time) if x >= scheduled_time else end)
        start = np.where(slot_array_ == scheduled_time)[0][0] if any(slot_array_ == scheduled_time) else  np.where(slot_array_ == smaller_possible_number)[0][0]
        desired_time_index = random.randint(start, end)
        desired_time = slot_array_[desired_time_index]
        #if scheduled_time in slot_array_:
        #    desired_time = min(start, end)
        # print("d", desired_time)
        return desired_time
    
class ScheduledTimeAssignmentStrategy(DesiredTimeStrategy):
    def assign_desired_time(self, actual_flight, slot_array, seed):
        slot_array_ = slot_array
        scheduled_time = actual_flight.scheduled_flight.scheduled_time
        if scheduled_time in slot_array_:
            desired_time = actual_flight.scheduled_flight.scheduled_time
        else:
            desired_time = slot_array_[0]
            
        return desired_time

class MiddleAssignmentStrategy(DesiredTimeStrategy):
    def assign_desired_time(self, actual_flight, slot_array, seed):
        slot_array_ = slot_array
        scheduled_time = actual_flight.scheduled_flight.scheduled_time
        end = np.where(slot_array_ == actual_flight.assigned_time)
        middle_number = end // 2
        desired_time = slot_array_[middle_number]
        if scheduled_time in slot_array_:
            desired_time = max(scheduled_time, desired_time)
        
        return desired_time
    
#a = RandomAssignmentStrategy()
#print(a.assign_desired_time(, 0))

