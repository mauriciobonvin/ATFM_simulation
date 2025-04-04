import credits_clearing
import pandas as pd

import logging

logger = logging.getLogger(__name__)

class EquityMonitorStrategy:
    
    def run_equity(self,
                   original_list: list,
                   new_list: list,
                   optimization_result: list,
                   airlines_preferences: list,
                   base_value_weight_map: int,
                   airline_list:list,
                   step_number:int):
        pass

class CreditsCLearingStrategy(EquityMonitorStrategy):
    
    equity_data = [] 
    
    def __init__(self, 
                 initial_credits
                ):
        self.initial_credits = initial_credits
        self.initial_credits_bool = False
        
    def run_equity(self,
                   original_list: list,
                   new_list: list,
                   optimization_result: list,
                   airlines_preferences: list,
                   base_value_weight_map: int,
                   airline_list:list,
                   step_number:int):
        
        if not self.initial_credits_bool:
            
            clearing = credits_clearing.Clearing(original_list,
                                                 new_list,
                                                 optimization_result,
                                                 airlines_preferences,
                                                 base_value_weight_map
                                                )
            clearing.perform_clearing()
            
            initial_credits = clearing.initial_credits(airline_list, self.initial_credits)
            self.initial_credits_bool = True
            equity_data_ = clearing.movements_to_credit(airline_list,
                                                        step_number)
            logger.info("\n")
            logger.info(f"Credits for step number {step_number}:")
            df = pd.DataFrame(equity_data_)
            logger.info(df)
            logger.info("\n")
            CreditsCLearingStrategy.equity_data.extend(initial_credits)
            CreditsCLearingStrategy.equity_data.extend(equity_data_)

            logger.info("Credits standing")
            df2 = pd.DataFrame(CreditsCLearingStrategy.equity_data)
            result = df2.groupby('airline')['credits'].sum().reset_index()
            logger.info(result)
            logger.info("\n")

        else:
            
            clearing = credits_clearing.Clearing(original_list,
                                                 new_list,
                                                 optimization_result,
                                                 airlines_preferences,
                                                 base_value_weight_map
                                                )
            clearing.perform_clearing()
            equity_data_ = clearing.movements_to_credit(airline_list,
                                                        step_number)
            logger.info("\n")
            logger.info(f"Credits for step number {step_number}:")
            df = pd.DataFrame(equity_data_)
            logger.info(df)
            CreditsCLearingStrategy.equity_data.extend(equity_data_)
            logger.info("\n")
            logger.info("Credits standing")
            df2 = pd.DataFrame(CreditsCLearingStrategy.equity_data)
            result = df2.groupby('airline')['credits'].sum().reset_index()
            logger.info(result)
            logger.info("\n")