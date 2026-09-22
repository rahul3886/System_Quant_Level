import pandas as pd
import os
import sys

def analyze_portfolio(summary_path):
    if not os.path.exists(summary_path):
        print(f"Summary file not found: {summary_path}")
        return

    df = pd.read_csv(summary_path)
    
    print("="*60)
    print("📈 MASTER PORTFOLIO PERFORMANCE SUMMARY")
    print("="*60)
    
    # Clean up empty rows (thresholds with no trades)
    df = df.dropna(subset=['total_trades'])
    
    # 1. Asset Participation
    print("\n📡 [TRADE VOLUME BY ASSET]")
    asset_vol = df.groupby('symbol')['total_trades'].sum().sort_values(ascending=False)
    print(asset_vol)
    
    # 2. Top Performers by Profit Factor
    print("\n🏆 [TOP 5 SETUPS BY PROFIT FACTOR]")
    top_pf = df.sort_values(by='profit_factor', ascending=False).head(5)
    print(top_pf[['symbol', 'timeframe', 'threshold', 'win_rate', 'profit_factor', 'total_pnl']])
    
    # 3. Overall Portfolio Stats
    print("\n📊 [AGGREGATED STATS]")
    print(f"Total Portfolio Assets:    {df['symbol'].nunique()}")
    print(f"Total Simulated Trades:    {df['total_trades'].sum():.0f}")
    print(f"Total Combined PnL:        {df['total_pnl'].sum():.2f}")
    print(f"Average Win Rate:          {df['win_rate'].mean()*100:.2f}%")
    
    # 4. Success Rate by Category
    df['is_profitable'] = df['total_pnl'] > 0
    print("\n✅ [PROFITABILITY FREQUENCY]")
    success_rate = df.groupby('symbol')['is_profitable'].mean().mul(100).round(2).astype(str) + '%'
    print(success_rate)

    print("\n" + "="*60)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "quant_engine_v2/backtest_results/latest/sweep_summary.csv"
    # If using 'latest', find the most recent folder
    if 'latest' in path:
        base = "quant_engine_v2/backtest_results"
        folders = [f for f in os.listdir(base) if os.path.isdir(os.path.join(base, f))]
        if folders:
            latest_folder = sorted(folders)[-1]
            path = os.path.join(base, latest_folder, "sweep_summary.csv")
    
    analyze_portfolio(path)
