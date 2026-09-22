import os
import json
import pandas as pd
from quant_engine_v2.data.data_provider import DataProvider
from quant_engine_v2.core.v1.signal_engine import SignalEngine

def run_targeted_btc():
    provider = DataProvider()
    symbol = 'BTC/USDT'
    tf = '5m'
    threshold = 80
    limit = 1000
    
    df = provider.get_crypto_data(symbol, tf, limit=limit)
    if df.empty: return
    
    backtester = BacktestEngine(initial_balance=10000)
    output = backtester.run(df, threshold_override=threshold)
    
    # Save to a temporary analysis folder
    os.makedirs("quant_engine_v2/analysis_temp", exist_ok=True)
    file_path = "quant_engine_v2/analysis_temp/btc_5m_80.json"
    
    # Clean timestamps for JSON
    for t in output['trades']:
        t['timestamp'] = str(t['timestamp'])
        
    with open(file_path, 'w') as f:
        json.dump(output, f, indent=4)
        
    print(f"Log saved for analysis: {file_path}")

if __name__ == "__main__":
    run_targeted_btc()
