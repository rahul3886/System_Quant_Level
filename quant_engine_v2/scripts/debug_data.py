import sys
import os
# Add project root to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from quant_engine_v2.data.data_provider import DataProvider
import pandas as pd

dp = DataProvider()
assets = ['BTC/USDT', 'XAUUSD', 'EURAUD']

print("🔍 DATA DIAGNOSTIC START")
for asset in assets:
    print(f"--- Testing {asset} ---")
    df = dp.get_data(asset, '5m', limit=5)
    if df.empty:
        print(f"❌ {asset}: RETURNED EMPTY DATAFRAME")
    else:
        print(f"✅ {asset}: SUCCESS | Rows: {len(df)}")
        print(df.tail(2))
print("🔍 DIAGNOSTIC COMPLETE")
