import ATFMSimulation
import Setup
import logging
import LoggingConfiguration


if __name__ == "__main__":
    # Initialize the simulation model with parameters from Setup
    model = ATFMSimulation.ATFMSimulationModel(
                                                n_times = Setup.n_times_, 
                                                seed = Setup.starting_seed_,
                                                time_assignment_seed = Setup.time_assignment_seed,
                                                time_assignment_strategy = Setup.time_assignment_strategy,   
                                                network_manager_agent = Setup.network_manager_agent_,
                                                list_airline_agents = Setup.list_airline_agents_,
                                                platform_agent = Setup.platform_agent_
                                              )
    LoggingConfiguration.configure_logging()
    
    for i in range(Setup.steps):
        model.step()
        
        
