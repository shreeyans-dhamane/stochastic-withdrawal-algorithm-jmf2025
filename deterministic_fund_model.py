import math

class DeterministicSWPModel:
    def __init__(self, beta, mean_growth_factor, inflation_factor):
        self.beta = beta
        self.mg = mean_growth_factor  
        self.mi = inflation_factor    

    def calculate_alpha(self, target_t):
        int_t = int(target_t)

        if int_t < 1:
            return 0.0 

        try:
            sum_term = sum(
                (self.mg ** (int_t - k)) * (self.mi ** k)
                for k in range(1, int_t + 1)  
            )

            denominator = self.mg ** int_t

            if denominator == 0:
                return float('inf')

            alpha = self.beta * sum_term / denominator
            
            return alpha

        except OverflowError:
            print(f"Error: Calculation overflowed. Target t '{target_t}' may be too large.", file=sys.stderr)
            return float('inf')
