import json
import pandas as pd
import sys
import os
from datetime import datetime

def analyze_daily(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as f:
        data = json.load(f)

    trades = data.get('trades', [])
    if not trades:
        print(f"No trades for {os.path.basename(file_path)}")
        return

    df = pd.DataFrame(trades)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    # 1. Daily Volume
    daily_vol = df.groupby('date').size()
    
    print("-" * 40)
    print(f"ASSET: {os.path.basename(file_path)}")
    print("-" * 40)
    print(f"Total Days with Trades: {len(daily_vol)}")
    print(f"Avg Trades/Day:        {daily_vol.mean():.2f}")
    print(f"Max Trades in a Day:   {daily_vol.max()}")
    print("\n[DAILY BREAKDOWN]")
    print(daily_vol)
    print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_daily_metrics.py <json_path>")
    else:
        analyze_daily(sys.argv[1])
