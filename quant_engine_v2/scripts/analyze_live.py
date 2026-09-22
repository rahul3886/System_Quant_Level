import json
import pandas as pd
import sys
import os

def analyze_live_logs(file_path="quant_engine_v2/logs/signal_history.jsonl"):
    if not os.path.exists(file_path):
        print(f"Log file not found: {file_path}")
        return

    records = []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                records.append(json.loads(line))
            except:
                continue

    if not records:
        print("No records found in the live logs.")
        return

    df = pd.DataFrame(records)
    
    print("="*50)
    print(f"LIVE SESSION ANALYSIS: {file_path}")
    print("="*50)
    
    # 1. Volume of Signals
    print("\n📡 [SIGNAL VOLUME]")
    print(f"Total Signals:  {len(df)}")
    if 'signal' in df.columns:
        print(df['signal'].value_counts())

    # 2. Performance by Asset
    if 'symbol' in df.columns and 'strength_score' in df.columns:
        print("\n📈 [ASSET BREAKDOWN]")
        asset_stats = df.groupby('symbol')['strength_score'].agg(['count', 'mean', 'max']).rename(columns={'mean': 'avg_score', 'max': 'max_score'})
        print(asset_stats)

    # 3. Regime Distribution
    if 'regime' in df.columns:
        print("\n📊 [REGIME DISTRIBUTION]")
        print(df['regime'].value_counts(normalize=True).mul(100).round(2).astype(str) + '%')

    # 4. Strength Score Stats
    if 'strength_score' in df.columns:
        print("\n🔥 [SIGNAL STRENGTH]")
        print(f"Average Score:  {df['strength_score'].mean():.2f}")
        print(f"Signals > 80:   {len(df[df['strength_score'] > 80])}")

    print("\n" + "="*50)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "quant_engine_v2/logs/signal_history.jsonl"
    analyze_live_logs(path)
