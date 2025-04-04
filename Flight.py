class ScheduledFlight:
    
    def __init__(self, flight_number):
        self.flight_number = flight_number
        self.scheduled_time = None
        self.time_assignment_seed = None
        self.list_of_actual_flights = []
        

class ActualFlight:
    
    def __init__(self, step_number, scheduled_flight):
        
        self.step_number = step_number
        self.scheduled_flight = scheduled_flight
        self.priority = None
        self.assigned_time = None
        self.desired_time = None
        self.margins = None
        self.optimization_time = None
        self.intervened = 0
        
        