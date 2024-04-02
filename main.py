import ATFMSimulation
import setup
import logging
import logging_config

if __name__ == "__main__":

    model = ATFMSimulation.ATFMSimulationModel(n_times = setup.n_times_, 
                        seed = setup.starting_seed_,
                        window_strategy = setup.window_strategy_,
                        regulation_strategy = setup.regulation_strategy_,
                        capacity = setup.capacity_,
                        list_airline_agents = setup.list_airline_agents_,
                        platform_agent = setup.platform_agent_,
                        time_assignment_strategy = setup.time_assignment_strategy,
                        intervene_weight_map_strategy = setup.intervene_weight_map_,
                        intervene_optimization_output_strategy = setup.intervene_optimization_output_       
                                              )
    
    for i in range(setup.steps):
        model.step()
        logging_config.configure_logging()
        
