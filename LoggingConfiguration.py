import logging

def configure_logging():
    logging.basicConfig(filename='Simulation_log.log', 
                        level=logging.INFO
                       )