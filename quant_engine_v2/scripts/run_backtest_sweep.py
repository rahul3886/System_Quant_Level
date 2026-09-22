import os
import json
import pandas as pd
from datetime import datetime, timedelta
from quant_engine_v2.data.data_provider import DataProvider
from quant_engine_v2.backtesting.backtest_engine import BacktestEngine

def run_sweep():
    # Configuration
    symbols = {
        'CRYPTO': ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT'],
        'FOREX': ['EURUSD', 'GBPUSD', 'GBPJPY', 'USDCHF', 'EURAUD'],
        'METALS': ['XAUUSD']
    }
    timeframes = ['1m', '5m']
    thresholds = [60, 70, 80, 100]
    version = 'v1' # Baseline version for discovering sweet spots
    
    provider = DataProvider()
    
    # Generate timestamp for this run
    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_dir = f"quant_engine_v2/backtest_results/{run_id}"
    os.makedirs(base_dir, exist_ok=True)
    
    print(f"🚀 STARTING BACKTEST SWEEP | ID: {run_id}")
    
    records = []

    for category, asset_list in symbols.items():
        for symbol in asset_list:
            for tf in timeframes:
                print(f"\n--- Processing {symbol} | {tf} ---")
                
                # Fetch 3 days of data (approximate candles)
                # 1m: 3 days * 24h * 60m = 4320 candles
                # 5m: 3 days * 24h * 12 = 864 candles
                limit = 4320 if tf == '1m' else 1000
                
                if category == 'CRYPTO':
                    df = provider.get_crypto_data(symbol, tf, limit=limit)
                else:
                    df = provider.get_forex_metal_data(symbol, tf, limit=limit)
                
                if df.empty:
                    print(f"⚠️ No data for {symbol} {tf}")
                    continue
                
                # Create asset-specific folder
                # Replace slash with underscore for folder name
                asset_folder_name = f"{symbol.replace('/', '_')}_{tf}"
                asset_dir = os.path.join(base_dir, asset_folder_name)
                os.makedirs(asset_dir, exist_ok=True)
                
                for threshold in thresholds:
                    backtester = BacktestEngine(initial_balance=10000, version=version)
                    backtest_output = backtester.run(df, threshold_override=threshold)
                    
                    results = backtest_output['metrics']
                    trades = backtest_output['trades']
                    
                    # Save individual result with full trade log
                    result_data = {
                        'metrics': results,
                        'trades': trades
                    }
                    
                    result_file = os.path.join(asset_dir, f"threshold_{threshold}.json")
                    with open(result_file, 'w') as f:
                        # Convert timestamps to string for JSON serialization
                        for trade in trades:
                            if 'timestamp' in trade:
                                trade['timestamp'] = str(trade['timestamp'])
                        json.dump(result_data, f, indent=4)
                    
                    summary_row = results.copy()
                    summary_row['symbol'] = symbol
                    summary_row['timeframe'] = tf
                    summary_row['threshold'] = threshold
                    records.append(summary_row)

    # Save master summary
    summary_df = pd.DataFrame(records)
    summary_df.to_csv(os.path.join(base_dir, "sweep_summary.csv"), index=False)
    
    print(f"\n✅ SWEEP COMPLETED. Results saved to {base_dir}")
    return base_dir

if __name__ == "__main__":
    run_sweep()
