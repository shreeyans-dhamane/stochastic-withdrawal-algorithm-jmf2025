This project implements the stochastic algorithm described in the paper "Modeling A Systematic Withdrawal Plan: A Stochastic Algorithm to Estimate Initial Fund Requirement" (Dhamane, 2025).

Paper Link: https://www.scirp.org/journal/paperinformation?paperid=140552

PDF Link: https://www.scirp.org/pdf/jmf2025151_71491166.pdf

Citiation: Dhamane, S. (2025) Modeling A Systematic Withdrawal Plan: A Stochastic Algorithm to Estimate Initial Fund Requirement. Journal of Mathematical Finance, 15, 155-168. https://doi.org/10.4236/jmf.2025.151007

It allows you to calculate the required initial fund ($\alpha$) for a systematic withdrawal plan based on any historical stock data CSV, a target duration, and a desired safety percentile. The simulation dynamically calculates the mean ($\mu$) and standard deviation ($\sigma$) from your data instead of using hard-coded values.

Project Structure

simulation_orchestrator.py: The main entry point to run the simulation.

historical_data_processor.py: Module to analyze historical stock data from a CSV and calculate $\mu$ and $\sigma$.

deterministic_fund_model.py: Implements the deterministic formula (Eq. 13) for $\alpha$.

stochastic_longevity_model.py: The core Monte Carlo simulation logic.

analysis_utilities.py: Helper functions for outlier removal.

project_config.py: Contains global constants and default values.

statistical_visualizer.R: R script to generate a histogram of simulation results.

sample_sp500_data.csv: Sample S&P 500-like monthly closing data.

requirements.txt: Python dependencies.

README.md: This file.

Setup

1. Python Environment

It's recommended to use a virtual environment.

python -m venv venv
On macOS/Linux:
source venv/bin/activate
On Windows:
venv\Scripts\activate


Install the required Python libraries:

pip install -r requirements.txt


2. R Environment

You must have R installed on your system and accessible from the command line (i.e., the Rscript command must work).

You also need to install the following R packages. Run this in your R console:

install.packages("ggplot2")
install.packages("readr")
install.packages("optparse")
install.packages("scales")


How to Run

You run the simulation from your terminal using simulation_orchestrator.py. It accepts several command-line arguments:

--csv_path (Required): Path to your CSV file of monthly stock data. (e.g., sample_sp500_data.csv). Must contain a 'Close' or 'Adj Close' column.

--beta (Required): The initial monthly withdrawal amount (e.g., 5000).

--target_t (Required): Your target fund duration in months (e.g., 127).

--percentile (Required): The desired safety percentile (1-99). The paper uses 90.

--inflation_rate (Optional): The average monthly inflation rate as a percentage. Default is 0.21 (which corresponds to the paper's 1.0021 factor).

--simulations (Optional): Number of Monte Carlo simulations. Default is 10000.

Example Command

This command runs the simulation using the sample data, for a $5000 initial withdrawal, a target of 127 months, and a 90% safety margin.

python simulation_orchestrator.py \
    --csv_path "sample_sp500_data.csv" \
    --beta 5000 \
    --target_t 127 \
    --percentile 90


Output

Console: The script will print:

The calculated mean ($\mu$) and standard deviation ($\sigma$) from your stock data.

The 50% safety $\alpha$ (based on the deterministic model).

The t-value at your specified percentile.

The final, percentile-adjusted $\alpha$ (your required initial fund).

Files:

simulation_longevity_results.csv: A CSV file containing the t-values (fund longevity in months) from all simulations.


simulation_longevity_plot.tiff: A TIFF image file showing the histogram of simulation results, with a vertical line marking your chosen percentile.



