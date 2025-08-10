#!/usr/bin/env python3
\"\"\"SIP RSI Backtest Bot
Usage:
    python backtest_sip_rsi.py path/to/data.csv --invest 100000 --rsi-threshold 45 --rsi-window 14
The script expects a CSV with columns: Date, Price (can have commas), Change % (optional).
Outputs: prints metrics and saves a portfolio value plot (portfolio_value.png).
\"\"\"
import argparse, pandas as pd, numpy as np, matplotlib.pyplot as plt
from datetime import datetime

def load_data(path):
    df = pd.read_csv(path)
    df = df.rename(columns={df.columns[0]:'Date', df.columns[1]:'Price'})
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df['Price'] = df['Price'].astype(str).str.replace(',','').astype(float)
    df = df.sort_values('Date').reset_index(drop=True)
    return df

def compute_rsi(df, window=14):
    delta = df['Price'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def backtest(df, invest_per_trade=100000, rsi_threshold=45):
    df = df.copy()
    df['signal'] = ((df['RSI'] < rsi_threshold) & (~df['RSI'].isna())).astype(int)
    units = 0.0
    cash_deployed = 0.0
    units_history = []
    portfolio_value = []
    cash_balance = 0.0
    for i, row in df.iterrows():
        if row['signal'] == 1:
            units += invest_per_trade / row['Price']
            cash_deployed += invest_per_trade
        units_history.append(units)
        pv = units * row['Price'] + cash_balance
        portfolio_value.append(pv)
    df['Units'] = units_history
    df['PortfolioValue'] = portfolio_value

    # Metrics
    num_trades = int(df['signal'].sum())
    total_months = df.shape[0]
    intended_total = invest_per_trade * total_months
    capital_utilization = cash_deployed / intended_total * 100 if intended_total>0 else 0.0

    # 12-month horizon returns per trade
    returns_12m = []
    for i,row in df[df['signal']==1].iterrows():
        start_price = row['Price']
        target_date = row['Date'] + pd.DateOffset(months=12)
        future = df[df['Date']>=target_date]
        if not future.empty:
            end_price = future.iloc[0]['Price']
            ret = (end_price - start_price) / start_price
            returns_12m.append(ret)
    hit_ratio = (sum(1 for r in returns_12m if r>0) / len(returns_12m) * 100) if len(returns_12m)>0 else None
    avg_return_per_trade = (np.mean(returns_12m)*100) if len(returns_12m)>0 else None

    # CAGR via IRR (monthly)
    cashflows = [(-invest_per_trade if row['signal']==1 else 0.0) for _,row in df.iterrows()]
    cashflows[-1] += df.iloc[-1]['PortfolioValue']
    try:
        monthly_irr = np.irr(cashflows)
        annual_irr = (1+monthly_irr)**12 - 1
        CAGR = annual_irr*100
    except:
        monthly_irr = None; annual_irr = None; CAGR = None

    df['PV_returns'] = df['PortfolioValue'].pct_change()
    vol_monthly = df['PV_returns'].std(ddof=0)
    vol_annual = vol_monthly * (12**0.5) if not np.isnan(vol_monthly) else None
    vol_annual_pct = vol_annual*100 if vol_annual is not None else None

    pv = df['PortfolioValue'].values
    if len(pv)>0 and not np.all(pv==0):
        cum_max = np.maximum.accumulate(pv)
        drawdowns = (pv - cum_max) / cum_max
        max_dd = drawdowns.min()*100
    else:
        max_dd = None

    sharpe = (annual_irr / vol_annual) if (annual_irr is not None and vol_annual not in (None,0) and not np.isnan(vol_annual)) else None

    metrics = {
        "Number of Trades": num_trades,
        "Capital Deployed (INR)": int(cash_deployed),
        "Capital Utilization (%)": round(capital_utilization,2),
        "CAGR (%)": round(CAGR,2) if CAGR is not None else None,
        "Monthly Volatility (std)": round(vol_monthly,4) if vol_monthly is not None else None,
        "Annualized Volatility (%)": round(vol_annual*100,2) if vol_annual is not None else None,
        "Max Drawdown (%)": round(max_dd,2) if max_dd is not None else None,
        "Sharpe Ratio": round(sharpe,4) if sharpe is not None else None,
        "Hit Ratio (%) (12m horizon)": round(hit_ratio,2) if hit_ratio is not None else None,
        "Avg Return per Trade (%) (12m horizon)": round(avg_return_per_trade,2) if avg_return_per_trade is not None else None
    }
    return df, metrics

def plot_portfolio(df, out_path='portfolio_value.png'):
    plt.figure(figsize=(10,6))
    plt.plot(df['Date'], df['PortfolioValue'])
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (INR)')
    plt.title('Portfolio Value Over Time (INR)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv', help='path to CSV file')
    parser.add_argument('--invest', type=float, default=100000, help='INR per signal')
    parser.add_argument('--rsi-threshold', type=float, default=45, help='RSI threshold to trigger buy')
    parser.add_argument('--rsi-window', type=int, default=14, help='RSI window')
    args = parser.parse_args()

    df = load_data(args.csv)
    df = compute_rsi(df, window=args.rsi_window)
    df, metrics = backtest(df, invest_per_trade=args.invest, rsi_threshold=args.rsi_threshold)

    print(\"--- METRICS ---\")
    for k,v in metrics.items():
        print(f\"{k}: {v}\")
    plot_portfolio(df)

if __name__ == '__main__':
    main()
