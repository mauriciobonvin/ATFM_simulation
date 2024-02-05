import mesa
from mesa.time import BaseScheduler




# Define a custom scheduler class called SequentialScheduler that inherits from BaseScheduler
class SequentialScheduler(BaseScheduler):
    def __init__(self, model):
        # Call the constructor of the parent class (BaseScheduler)
        super().__init__(model)
        
        # Initialize an empty list to store the sequence of agents to be executed
        self.agent_sequence = []

    # Method to add an agent to the execution sequence
    def add_agent_to_sequence(self, agent):
        # Append the provided agent to the agent_sequence list
        self.agent_sequence.append(agent)

    # Method to execute one step of the scheduler
    def step(self):
        # Iterate through agents in the order specified by agent_sequence
        for agent in self.agent_sequence:
            # Execute the step() method of the current agent
            agent.step()

