import pandas as pd
import numpy as np

class LiquidityEngine:
    def __init__(self):
        pass

    def detect_liquidity(self, df):
        # SSL (Sell Side Liquidity) - Equal Lows
        # BSL (Buy Side Liquidity) - Equal Highs
        
        df = df.copy()
        ssl_levels = []
        bsl_levels = []
        
        # Simple clustering for equal highs/lows
        highs = df['high'].values
        lows = df['low'].values
        
        # Identify pools (3+ touches within 0.1% tolerance)
        tolerance = 0.001
        
        for i in range(len(highs)):
            level = highs[i]
            touches = np.sum(np.abs(highs - level) / level < tolerance)
            if touches >= 3:
                if not any(np.abs(np.array(bsl_levels) - level) / level < tolerance):
                    bsl_levels.append(level)
                    
            level = lows[i]
            touches = np.sum(np.abs(lows - level) / level < tolerance)
            if touches >= 3:
                if not any(np.abs(np.array(ssl_levels) - level) / level < tolerance):
                    ssl_levels.append(level)

        # Sweep Detection
        # Price goes below SSL then closes above -> SSL Sweep
        # Price goes above BSL then closes below -> BSL Sweep
        sweep_detected = None
        pool_sweep = False
        
        current_close = df['close'].iloc[-1]
        current_low = df['low'].iloc[-1]
        current_high = df['high'].iloc[-1]
        
        for level in ssl_levels:
            if current_low < level and current_close > level:
                sweep_detected = "SSL_SWEEP"
                pool_sweep = True
                break
                
        for level in bsl_levels:
            if current_high > level and current_close < level:
                sweep_detected = "BSL_SWEEP"
                pool_sweep = True
                break

        # Asian Range Mapping (Simplified: last 24 1h bars if on 1h)
        asian_range = {'high': df['high'].tail(24).max(), 'low': df['low'].tail(24).min()}

        return {
            'ssl_levels': ssl_levels,
            'bsl_levels': bsl_levels,
            'sweep_detected': sweep_detected,
            'pool_sweep': pool_sweep,
            'asian_range': asian_range
        }
