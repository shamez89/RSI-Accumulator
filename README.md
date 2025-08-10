# RSI-Accumulator

A quantitative investment strategy that invests ₹1,00,000 whenever the monthly RSI drops below 45, aiming to capture undervaluation opportunities.  
Backtested with historical data, calculated key metrics (CAGR, Drawdown, Sharpe, Hit Ratio), visualized portfolio growth, and compared RSI-timed SIP vs fixed SIP to highlight benefits and risks.

---

# Monthly RSI-Based SIP Backtesting Tool

## Overview
This project implements and backtests a **Systematic Investment Plan (SIP)** strategy that invests a fixed amount (default: ₹1,00,000) whenever the **monthly Relative Strength Index (RSI)** falls below a chosen threshold (default: 45).  

The objective:  
> Does buying during weaker market momentum lead to better long-term results than a fixed monthly SIP?

---

## Strategy Logic
1. Load historical price data from a CSV.  
2. Resample to **monthly** and compute RSI (default period: 14).  
3. If RSI < threshold → invest ₹1,00,000 (fractional units allowed).  
4. Track units purchased and portfolio value.  
5. Compute performance metrics and visualize growth.

---

## Features
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
  - Portfolio value chart
  - Buy markers

---

## Example Output

### Key Metrics


---

### Portfolio Growth Chart
![Portfolio Value Over Time](df02745e-35f5-4f2a-8eda-d5638ee943be.png)  

---

### Example Trades
| Date       | Price (INR) | Units Bought | Investment (INR) |
|------------|------------:|-------------:|-----------------:|
| 2001-03-01 | 1528.45     | 65.41         | 100000           |
| 2002-07-01 | 1402.22     | 71.29         | 100000           |
| 2004-09-01 | 1750.10     | 57.14         | 100000           |
| ...        | ...         | ...           | ...              |

For the full trade log, see [`trades.csv`](4866a25a-6091-4ddd-ad5c-85901ce00c5f.csv).

---

## Installation
```bash
git clone https://github.com/yourusername/monthly-rsi-sip.git
cd monthly-rsi-sip
pip install pandas numpy matplotlib


Notes
Uses np.irr for CAGR — in newer NumPy versions this is deprecated; consider replacing with numpy_financial.irr or a date-aware XIRR method for better accuracy.

No reinvestment of dividends is assumed.

Works best with monthly price data; resample daily data before running

License
This project is licensed under the MIT License.

