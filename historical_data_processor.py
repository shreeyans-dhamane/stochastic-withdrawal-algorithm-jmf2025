import pandas as pd
import sys
from analysis_utilities import OutlierRemover

class MarketDataProcessor:
    def __init__(self, csv_path, price_column_name):
        self.csv_path = csv_path
        self.price_column_name = price_column_name
        self.data = None

    def _load_data(self):
        self.data = pd.read_csv(self.csv_path)
        
        if self.price_column_name not in self.data.columns:
            if "Adj Close" in self.data.columns:
                self.price_column_name = "Adj Close"
                print(f"   > Note: '{self.price_column_name}' not found, using 'Adj Close'.")
            else:
                possible_cols = [col for col in self.data.columns if "Close" in col]
                if possible_cols:
                    self.price_column_name = possible_cols[0]
                    print(f"   > Note: '{self.price_column_name}' not found, using '{self.price_column_name}'.")
                else:
                    print(f"Error: Could not find '{self.price_column_name}' or 'Adj Close' in CSV.", file=sys.stderr)
                    raise KeyError(f"Missing required price column: {self.price_column_name}")
        
        self.data[self.price_column_name] = pd.to_numeric(self.data[self.price_column_name], errors='coerce')
        self.data = self.data.dropna(subset=[self.price_column_name])


    def _calculate_monthly_returns(self):
        monthly_returns = self.data[self.price_column_name].pct_change()
        
        percentage_returns = monthly_returns * 100
        
        return percentage_returns.dropna()

    def calculate_return_statistics(self):
        try:
            self._load_data()
            
            if self.data.empty or len(self.data) < 2:
                print(f"Error: Not enough data in '{self.csv_path}' to calculate returns.", file=sys.stderr)
                return None, None

            returns = self._calculate_monthly_returns()

            if returns.empty:
                print(f"Error: Could not calculate any returns from data.", file=sys.stderr)
                return None, None

            remover = OutlierRemover(returns)
            cleaned_returns = remover.remove_iqr_outliers(factor=1.5)
            
            print(f"   > Analyzed {len(returns)} monthly returns.")
            print(f"   > Removed {len(returns) - len(cleaned_returns)} outliers from source data.")

            if cleaned_returns.empty:
                print(f"Error: All return values were filtered as outliers.", file=sys.stderr)
                return None, None

            mu = cleaned_returns.mean()
            sigma = cleaned_returns.std()

            return mu, sigma

        except Exception as e:
            print(f"Error in MarketDataProcessor: {e}", file=sys.stderr)
            return None, None
