import numpy as np

class OutlierRemover:
    def __init__(self, data):
        self.data = data

    def remove_iqr_outliers(self, factor=1.5):
        if self.data.empty:
            return self.data
            
        Q1 = np.percentile(self.data, 25)
        Q3 = np.percentile(self.data, 75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - (factor * IQR)
        upper_bound = Q3 + (factor * IQR)
        
        return self.data[(self.data >= lower_bound) & (self.data <= upper_bound)]

    def remove_simulation_outliers(self, paper_factor=1000):
        if len(self.data) == 0:
            return self.data

        Q1 = np.percentile(self.data, 25)
        Q3 = np.percentile(self.data, 75)
        IQR = Q3 - Q1

        if IQR == 0:
            return self.data
            
        upper_bound = Q3 + (paper_factor * IQR)

        return self.data[self.data <= upper_bound]
