from quant_engine_v2.data.data_provider import DataProvider
from quant_engine_v2.core.v1.signal_engine import SignalEngine
from quant_engine_v2.configs.sweet_spots import SWEET_SPOTS
import time

def run_high_yield_btc():
    print("💎 RUNNING HIGH-YIELD VAULT SETUP: BTC/USDT 5m @ 80")
    provider = DataProvider()
    signal_engine = SignalEngine()
    
    config = SWEET_SPOTS['BTC/USDT']['5m']
    threshold = config['threshold']
    
    while True:
        try:
            df = provider.get_crypto_data('BTC/USDT', timeframe='5m', limit=100)
            if df.empty: continue
            
            signal_pkg = signal_engine.generate_signal(df, threshold_override=threshold)
            
            if signal_pkg and signal_pkg['signal'] != "NEUTRAL":
                print(f"🔥 [HIGH YIELD SIGNAL] {signal_pkg['signal']} | Score: {signal_pkg['strength_score']} | Regime: {signal_pkg['regime']}")
                # Router can be added here
            else:
                print(f"Sensing... (Status: {signal_pkg['regime']} | Score: {signal_pkg['strength_score']})", end='\r')
                
        except Exception as e:
            print(f"Vault Error: {e}")
            
        time.sleep(300) # Check every 5m

if __name__ == "__main__":
    run_high_yield_btc()
