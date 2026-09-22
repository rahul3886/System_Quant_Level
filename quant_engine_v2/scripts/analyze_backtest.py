import json
import pandas as pd
import sys
import os

def analyze_backtest(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as f:
        data = json.load(f)

    metrics = data.get('metrics', {})
    trades = data.get('trades', [])

    if not trades:
        print("No trades found in this backtest.")
        return

    df = pd.DataFrame(trades)
    df['pnl'] = pd.to_numeric(df['pnl'])
    
    print("="*50)
    print(f"DEEP ANALYSIS: {os.path.basename(file_path)}")
    print("="*50)
    
    # 1. High Level Metrics
    print("\n📈 [CORE METRICS]")
    print(f"Total Trades:   {metrics.get('total_trades')}")
    print(f"Win Rate:       {metrics.get('win_rate', 0)*100:.2f}%")
    print(f"Profit Factor:  {metrics.get('profit_factor', 0):.2f}")
    print(f"Total PnL:     {metrics.get('total_pnl', 0):.2f}")
    print(f"Max Drawdown:   {metrics.get('max_drawdown', 0):.2f}")

    # 2. Performance by Regime
    print("\n📊 [REGIME BREAKDOWN]")
    regime_pnl = df.groupby('regime')['pnl'].agg(['count', 'sum', 'mean']).rename(columns={'sum': 'total_pnl', 'mean': 'avg_pnl'})
    print(regime_pnl)

    # 3. Winning vs Losing Streaks (Simplified)
    df['is_win'] = df['pnl'] > 0
    df['streak'] = (df['is_win'] != df['is_win'].shift()).cumsum()
    streaks = df.groupby(['streak', 'is_win']).size()
    max_win_streak = streaks[streaks.index.get_level_values('is_win') == True].max() if any(df['is_win']) else 0
    max_loss_streak = streaks[streaks.index.get_level_values('is_win') == False].max() if any(~df['is_win']) else 0
    
    print("\n🔥 [STREAKS]")
    print(f"Max Win Streak:  {max_win_streak}")
    print(f"Max Loss Streak: {max_loss_streak}")

    # 4. Signal Type Analysis (Buy vs Sell)
    print("\n🏹 [SIGNAL TYPE PERFORMANCE]")
    signal_perf = df.groupby('signal')['pnl'].agg(['count', 'sum', 'mean'])
    print(signal_perf)

    # 5. Market Session Analysis
    def identify_session(ts):
        try:
            # Handle string timestamps
            if isinstance(ts, str):
                dt = pd.to_datetime(ts)
            else:
                dt = ts
            hour = dt.hour
            if 0 <= hour < 8: return "ASIAN"
            if 8 <= hour < 16: return "LONDON"
            return "NEW_YORK"
        except:
            return "UNKNOWN"

    df['session'] = df['timestamp'].apply(identify_session)
    print("\n🌍 [MARKET SESSION PERFORMANCE]")
    session_perf = df.groupby('session')['pnl'].agg(['count', 'sum', 'mean']).rename(columns={'sum': 'total_pnl', 'mean': 'avg_pnl'})
    print(session_perf)

    # 6. Distribution of PnL
    print("\n💰 [PnL DISTRIBUTION]")
    print(f"Largest Win:     {df['pnl'].max():.2f}")
    print(f"Largest Loss:    {df['pnl'].min():.2f}")
    print(f"Avg Win:         {df[df['pnl'] > 0]['pnl'].mean():.2f}")
    print(f"Avg Loss:        {df[df['pnl'] <= 0]['pnl'].mean():.2f}")

    print("\n" + "="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_backtest.py <path_to_json_result>")
    else:
        analyze_backtest(sys.argv[1])
