# RSI-Accumulator
Built a SIP strategy investing ₹1,00,000 when monthly RSI &lt; 45 to capture undervaluation opportunities. Backtested with historical data, computed key metrics (CAGR, drawdown, Sharpe, hit ratio), and visualized portfolio growth. Compared RSI-timed SIP vs fixed SIP, highlighting benefits and risks of timing."

# Monthly RSI-Based SIP Backtesting Tool

## 📌 Overview
This project implements and backtests a **Systematic Investment Plan (SIP)** strategy that invests a fixed amount (default: ₹1,00,000) whenever the **monthly Relative Strength Index (RSI)** drops below a specified threshold (default: 45).

The goal is to test whether buying during weaker market momentum periods leads to better long-term results compared to a fixed-interval SIP.

---

## 🎯 Strategy Logic
1. Load historical price data from a CSV.
2. Calculate **RSI** (default 14-period) on monthly price data.
3. If RSI < threshold → invest the fixed amount (fractional units allowed).
4. Track total units purchased and portfolio value.
5. Calculate performance metrics and visualize portfolio growth.

---

## ⚙️ Features
- **Customizable Parameters**
  - Investment amount per trade
  - RSI threshold
  - RSI window length
- **Performance Metrics**
  - CAGR (Compound Annual Growth Rate)
  - Sharpe Ratio
  - Maximum Drawdown (MDD)
  - Annualized Volatility
  - Hit Ratio (12-month forward returns)
  - Average Return per Trade (12-month forward)
  - Capital Utilization
- **Visualization**
  - Saves a PNG chart showing portfolio value over time

---

## 📊 Example Output
When running the script, you’ll get metrics like:

--- METRICS ---
Number of Trades: 48
Capital Deployed (INR): 4800000
Capital Utilization (%): 16.0
CAGR (%): 12.54
Monthly Volatility (std): 0.0321
Annualized Volatility (%): 11.13
Max Drawdown (%): -18.22
Sharpe Ratio: 1.126
Hit Ratio (%) (12m horizon): 72.92
Avg Return per Trade (%) (12m horizon): 27.19
