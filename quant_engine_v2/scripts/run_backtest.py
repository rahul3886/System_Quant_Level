import pandas as pd
from quant_engine_v2.data.data_provider import DataProvider
from quant_engine_v2.backtesting.backtest_engine import BacktestEngine
from quant_engine_v2.configs.asset_config import ASSETS

def run_backtest_demo():
    print("📊 STARTING BACKTEST DEMO")
    provider = DataProvider()
    backtester = BacktestEngine(initial_balance=10000)
    
    # Fetch data for BTC/USDT
    symbol = 'BTC/USDT'
    df = provider.get_crypto_data(symbol, timeframe='1h', limit=500)
    
    if df.empty:
        print("No data found for backtest.")
        return
        
    results = backtester.run(df)
    
    print("\n📈 BACKTEST RESULTS:")
    for k, v in results.items():
        print(f"{k.replace('_', ' ').title()}: {v if isinstance(v, int) else f'{v:.2f}'}")

if __name__ == "__main__":
    run_backtest_demo()
