import credits_clearing


class EquityStrategy:
    def run_equity(self, **kwargs):
        pass
    

class CreditsCLearingStrategy(EquityStrategy):
    
    all_credit_data = []
    
    def run_equity(self,
                   original_list: list,
                   new_list: list,
                   optimization_result: list,
                   airlines_preferences: list,
                   base_value_weight_map: int,
                   bonus: float,
                   airline_list:list,
                   step_number:int):
        
        if step_number == 1:
            
            clearing = credits_clearing.Clearing(original_list,
                                                 new_list,
                                                 optimization_result,
                                                 airlines_preferences,
                                                 base_value_weight_map,
                                                 bonus)
            clearing.perform_clearing()
            
            initial_credits = clearing.initial_credits(airline_list)
            
            credits_data = clearing.movements_to_credit(airline_list,
                                                        step_number)
            
            CreditsCLearingStrategy.all_credit_data.extend(initial_credits)
            CreditsCLearingStrategy.all_credit_data.extend(credits_data)

        else:
            
            clearing = credits_clearing.Clearing(original_list,
                                                 new_list,
                                                 optimization_result,
                                                 airlines_preferences,
                                                 base_value_weight_map,
                                                 bonus)
            clearing.perform_clearing()
            credits_data = clearing.movements_to_credit(airline_list,
                                                        step_number)

            CreditsCLearingStrategy.all_credit_data.extend(credits_data)