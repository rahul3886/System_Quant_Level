import sys
import os
import pandas as pd

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.insert(0, project_root)

from quant_engine_v2.core.v1.signal_engine import SignalEngine

def test_mtf_targets():
    engine = SignalEngine()
    
    # 1. Mock 1m Data (LTF) - Very tight range
    df_1m = pd.DataFrame({
        'timestamp': pd.date_range(start='2026-01-01', periods=100, freq='1min'),
        'open': 615.0, 'high': 616.0, 'low': 614.0, 'close': 615.5, 'volume': 100
    })
    
    # 2. Mock 5m Data (HTF) - Much wider range
    df_5m = pd.DataFrame({
        'timestamp': pd.date_range(start='2026-01-01', periods=100, freq='5min'),
        'open': 610.0, 'high': 630.0, 'low': 601.0, 'close': 615.0, 'volume': 500
    })
    
    # Need to simulate peaks/troughs for StructureEngine
    df_5m.at[50, 'high'] = 630.0 # Swing High
    df_5m.at[50, 'low'] = 601.0  # Swing Low
    # We need enough candles to satisfy the window=5 in detect_swings
    for i in range(1, 6):
        df_5m.at[50-i, 'high'] = 625.0
        df_5m.at[50+i, 'high'] = 625.0
        df_5m.at[50-i, 'low'] = 605.0
        df_5m.at[50+i, 'low'] = 605.0

    print("--- TESTING MTF TARGETS ---")
    # Generate signal for 1m entry but with 5m context
    result = engine.generate_signal(df_1m, htf_df=df_5m, threshold_override=0) # Force signal
    
    if result:
        print(f"Asset Price (1m): {result['price']}")
        print(f"Signal: {result['signal']}")
        print(f"Stop Loss: {result['structural_sl']}")
        print(f"Take Profit: {result['structural_tp']}")
        
        # Verify if targets came from 5m (630/601) or 1m (616/614)
        if result['signal'] == 'BUY':
            if result['structural_tp'] == 630.0:
                print("✅ SUCCESS: TP pulled from 5m HTF High.")
            else:
                print(f"❌ FAILURE: TP is {result['structural_tp']}, expected 630.0 (5m High)")
        
        if result['signal'] == 'SELL':
             if result['structural_tp'] == 601.0:
                print("✅ SUCCESS: TP pulled from 5m HTF Low.")
             else:
                print(f"❌ FAILURE: TP is {result['structural_tp']}, expected 601.0 (5m Low)")

if __name__ == "__main__":
    test_mtf_targets()
