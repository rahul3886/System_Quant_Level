from quant_engine_v2.data.data_provider import DataProvider
from quant_engine_v2.core.v1.signal_engine import SignalEngine
from quant_engine_v2.configs.sweet_spots import SWEET_SPOTS
import time

def run_high_yield_xau():
    print("💎 RUNNING HIGH-YIELD VAULT SETUP: XAU/USD 5m @ 60")
    provider = DataProvider()
    signal_engine = SignalEngine()
    
    config = SWEET_SPOTS['XAU/USD']['5m']
    threshold = config['threshold']
    
    while True:
        try:
            df = provider.get_forex_metal_data('XAUUSD', timeframe='5m', limit=100)
            if df.empty: continue
            
            signal_pkg = signal_engine.generate_signal(df, threshold_override=threshold)
            
            if signal_pkg and signal_pkg['signal'] != "NEUTRAL":
                print(f"🔥 [HIGH YIELD GOLD] {signal_pkg['signal']} | Score: {signal_pkg['strength_score']} | Regime: {signal_pkg['regime']}")
            else:
                print(f"Sensing Gold... (Status: {signal_pkg['regime']} | Score: {signal_pkg['strength_score']})", end='\r')
                
        except Exception as e:
            print(f"Vault Error: {e}")
            
        time.sleep(300)

if __name__ == "__main__":
    run_high_yield_xau()
