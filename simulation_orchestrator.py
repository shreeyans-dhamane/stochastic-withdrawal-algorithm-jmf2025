import argparse
import sys
import subprocess
import numpy as np
import pandas as pd
from historical_data_processor import MarketDataProcessor
from deterministic_fund_model import DeterministicSWPModel
from stochastic_longevity_model import StochasticSWPSimulator
from analysis_utilities import OutlierRemover
from project_config import (
    DEFAULT_INFLATION_RATE_PCT,
    DEFAULT_SIMULATIONS,
    DEFAULT_T_LIMIT,
    SIMULATION_OUTPUT_CSV,
    PLOT_OUTPUT_TIFF,
    R_SCRIPT_NAME,
    PRICE_COLUMN_NAME
)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Stochastic algorithm."
    )
    parser.add_argument(
        "--csv_path",
        type=str,
        required=True,
        help="Path to the CSV file of monthly stock data (must have a 'Close' or 'Adj Close' column)."
    )
    parser.add_argument(
        "--beta",
        type=float,
        required=True,
        help="The initial monthly withdrawal amount (e.g., 5000)."
    )
    parser.add_argument(
        "--target_t",
        type=int,
        required=True,
        help="Your target fund duration in months (e.g., 127)."
    )
    parser.add_argument(
        "--percentile",
        type=int,
        required=True,
        choices=range(1, 100),
        metavar="[1-99]",
        help="The desired safety percentile (1-99). The paper uses 90."
    )
    parser.add_argument(
        "--inflation_rate",
        type=float,
        default=DEFAULT_INFLATION_RATE_PCT,
        help=f"The average *monthly* inflation *rate* as a percentage. Default is {DEFAULT_INFLATION_RATE_PCT}%%."
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=DEFAULT_SIMULATIONS,
        help=f"Number of Monte Carlo simulations. Default is {DEFAULT_SIMULATIONS}."
    )
    return parser.parse_args()

def run_simulation_workflow():
    try:
        args = parse_arguments()

        print("--- Stochastic Simulation Initializing ---")
        print(f"Parameters:\n  Target Duration (t): {args.target_t} months\n  Initial Withdrawal (beta): ${args.beta:,.2f}\n  Safety Percentile: {args.percentile}th\n  Monthly Inflation: {args.inflation_rate}%\n  Simulations: {args.simulations:,}\n")

        print(f"1. Analyzing historical data from '{args.csv_path}'...")
        processor = MarketDataProcessor(args.csv_path, PRICE_COLUMN_NAME)
        rg_mean, rg_sd = processor.calculate_return_statistics()
        if rg_mean is None:
            sys.exit(1)  
            
        print(f"   > Calculated Mean Return (mu): {rg_mean:.4f}%")
        print(f"   > Calculated Std Dev (sigma): {rg_sd:.4f}%")

        inflation_factor = 1 + (args.inflation_rate / 100)
        mean_growth_factor = 1 + (rg_mean / 100)
        
        deterministic_model = DeterministicSWPModel(
            args.beta, mean_growth_factor, inflation_factor
        )
        
        print("\n2. Calculating 50% safety alpha (deterministic model)...")
        alpha_50_percent = deterministic_model.calculate_alpha(args.target_t)
        print(f"   > 50% Safety Alpha (for t={args.target_t}): ${alpha_50_percent:,.2f}")

        print(f"\n3. Running {args.simulations:,} stochastic simulations...")
        simulator = StochasticSWPSimulator(
            alpha_50_percent,
            args.beta,
            inflation_factor,
            rg_mean,
            rg_sd,
            DEFAULT_T_LIMIT
        )
        t_values = simulator.run_simulations(args.simulations)
        print(f"   > Simulations complete. Found {len(t_values)} finite t-values.")

        remover = OutlierRemover(t_values)
        filtered_t_values = remover.remove_simulation_outliers()
        print(f"   > Removed {len(t_values) - len(filtered_t_values)} outliers. {len(filtered_t_values)} t-values remain.")

        if len(filtered_t_values) == 0:
            print("Error: All simulation values were filtered as outliers. Cannot proceed.", file=sys.stderr)
            sys.exit(1)
            
        pd.DataFrame(filtered_t_values, columns=["t_value"]).to_csv(SIMULATION_OUTPUT_CSV, index=False)
        print(f"   > Simulation results saved to '{SIMULATION_OUTPUT_CSV}'")

        print(f"\n4. Calculating final {args.percentile}th percentile alpha...")
        t_percentile_value = np.percentile(filtered_t_values, args.percentile)
        print(f"   > {args.percentile}th Percentile t-value: {t_percentile_value:.2f} months")

        final_alpha = deterministic_model.calculate_alpha(t_percentile_value)
        print("\n--- SIMULATION COMPLETE ---")
        print(f"Required Initial Fund (Alpha) for {args.percentile}% safety:")
        print(f"${final_alpha:,.2f}")
        print("---------------------------\n")

        print(f"5. Generating visualization using R...")
        try:
            subprocess.run(
                [
                    "Rscript",
                    R_SCRIPT_NAME,
                    "--input", SIMULATION_OUTPUT_CSV,
                    "--output", PLOT_OUTPUT_TIFF,
                    "--percentile", str(t_percentile_value)
                ],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"   > Plot saved to '{PLOT_OUTPUT_TIFF}'")
        except FileNotFoundError:
            print(f"   > Error: 'Rscript' command not found. Please ensure R is installed and in your system's PATH.", file=sys.stderr)
        except subprocess.CalledProcessError as e:
            print(f"   > Error running R script '{R_SCRIPT_NAME}':", file=sys.stderr)
            print(e.stderr, file=sys.stderr)

    except FileNotFoundError as e:
        print(f"\nError: Input file not found.\nDetails: {e}", file=sys.stderr)
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"\nError: CSV file '{args.csv_path}' is empty.", file=sys.stderr)
        sys.exit(1)
    except KeyError:
        print(f"\nError: Could not find required price column ('{PRICE_COLUMN_NAME}') in '{args.csv_path}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred:\n{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_simulation_workflow()
