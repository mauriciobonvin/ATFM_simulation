import mesa
from mesa.time import BaseScheduler

# Define a custom scheduler class called SequentialScheduler that inherits from BaseScheduler
class SequentialScheduler(BaseScheduler):
    def __init__(self, model):
        super().__init__(model)
        # empty list to store the sequence of agents to be executed
        self.agent_sequence = []

    # Method to add an agent to the execution sequence
    def add_agent_to_sequence(self, agent):
        self.agent_sequence.append(agent)

    def step(self):
        # Iterate through agents in the order specified by agent_sequence
        for agent in self.agent_sequence:
            agent.step()

