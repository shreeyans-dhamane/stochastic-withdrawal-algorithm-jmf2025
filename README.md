# stochastic-withdrawal-algorithm-jmf2025

This project implements the stochastic algorithm described in the paper "Modeling A Systematic Withdrawal Plan: A Stochastic Algorithm to Estimate Initial Fund Requirement" (Dhamane, 2025).

Paper Link: https://www.scirp.org/journal/paperinformation?paperid=140552

PDF Link: https://www.scirp.org/pdf/jmf2025151_71491166.pdf

Citiation: Dhamane, S. (2025) Modeling A Systematic Withdrawal Plan: A Stochastic Algorithm to Estimate Initial Fund Requirement. Journal of Mathematical Finance, 15, 155-168. https://doi.org/10.4236/jmf.2025.151007

It allows you to calculate the required initial fund ($\alpha$) for a systematic withdrawal plan based on any historical stock data CSV, a target duration, and a desired safety percentile. The simulation dynamically calculates the mean ($\mu$) and standard deviation ($\sigma$) from your data instead of using hard-coded values.

