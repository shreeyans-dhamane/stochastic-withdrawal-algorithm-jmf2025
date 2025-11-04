import numpy as np
from tqdm import tqdm 

class StochasticSWPSimulator:
    def __init__(self, initial_alpha, beta, inflation_factor, rg_mean, rg_sd, max_t_limit):
        self.alpha = initial_alpha
        self.beta = beta
        self.mi = inflation_factor
        self.mu = rg_mean
        self.sigma = rg_sd
        self.max_t = max_t_limit

    def _run_single_simulation(self):
        fund = self.alpha  
        t = 0             

        while True:
            rg = np.random.normal(self.mu, self.sigma)
            
            mg_this_month = (1 + rg / 100)
            
            
            withdrawal = self.beta * (self.mi ** t)
            
            fund_next = (fund * mg_this_month) - withdrawal
            
            t += 1 

            if fund_next < 0:
                return t
            
            if t >= self.max_t:
                return None
                
            fund = fund_next 

    def run_simulations(self, num_simulations):
        t_values = []
        
        for _ in tqdm(range(num_simulations), desc="Running Simulations", unit="sim"):
            t = self._run_single_simulation()
            if t is not None:
                t_values.append(t)
                
        return np.array(t_values)
