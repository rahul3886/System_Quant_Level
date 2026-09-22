import sys
import time
from quant_engine_v2.data.data_provider import DataProvider
from quant_engine_v2.core.signal_engine import SignalEngine
from quant_engine_v2.execution.signal_router import SignalRouter
from quant_engine_v2.configs.asset_config import ASSETS

def main():
    print("💎 QUANT ENGINE v2 - Regime-Adaptive Structural Engine")
    provider = DataProvider()
    signal_engine = SignalEngine()
    router = SignalRouter()
    
    # Simple loop for Crypto demonstration
    crypto_symbols = ASSETS['CRYPTO']['symbols']
    
    print(f"🔍 Monitoring {len(crypto_symbols)} Crypto assets...")
    
    while True:
        for symbol in crypto_symbols:
            try:
                df = provider.get_crypto_data(symbol, timeframe='1h', limit=100)
                if df.empty: continue
                
                signal_pkg = signal_engine.generate_signal(df)
                if signal_pkg:
                    print(f"[{symbol}] Regime: {signal_pkg['regime']} | Score: {signal_pkg['strength_score']} | Signal: {signal_pkg['signal']}")
                    router.route_signal(signal_pkg)
                    
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                
        time.sleep(60) # Scan every minute (simulated h1 updates)

if __name__ == "__main__":
    main()
